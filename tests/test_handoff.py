import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import career_ai as a,visual_catalog as visuals
from tests.fixtures import SOURCE,make_map
class HandoffContracts(unittest.TestCase):
 def test_original_manifest_has_six_shapes_four_paths_and_semantic_alternatives(self):
  m=visuals.MANIFEST;self.assertGreaterEqual(len({p['shapeVariant']for p in m['platforms']}),6);self.assertGreaterEqual(len(m['pathways']),4);self.assertTrue(all(len(v)>=3 for v in m['concepts'].values()))
 def test_visual_requests_preserve_map_and_require_explicit_generation(self):
  previous=make_map();before=copy.deepcopy(previous)
  for message in ['Make the colors warmer','Use a new island shape','Change only the background to blue']:
   with patch('career_ai.provider')as provider:out=a.process_refine({'sources':[SOURCE],'previous':previous,'message':message,'context_consent':True})
   provider.assert_not_called();self.assertEqual(previous,before);self.assertEqual(out['map']['status'],'needs_more_info');self.assertNotIn('presentation_patch',out)
 def test_visual_paths_are_not_available_in_refinement_schema(self):
  from semantic_refinement import patch_schema
  schema=patch_schema(make_map(),[SOURCE]);paths=[p for b in schema['properties']['changes']['items']['anyOf']for p in b['properties']['path']['enum']]
  self.assertFalse(any(p.startswith('/visual/')or p.endswith('/icon')for p in paths))
 def test_quoted_heading_can_address_the_insight_beneath_it(self):
  from semantic_refinement import quoted_targets
  previous=make_map();paths=quoted_targets(previous,'Rewrite only the insight sentence under “Systems Design” using my actual evidence.');self.assertIn('/strengths/k2/description',paths);self.assertFalse(any('/k1/'in p for p in paths));self.assertEqual(quoted_targets(previous,'Change “Systems Design” to “Platform Judgement”.'),{'/strengths/k2/label'})
 def test_invalid_asset_ids_css_and_target_ids_are_rejected(self):
  for operation in [{'path':'/visual/icons/k1','value':'https://evil.example/icon.svg'},{'path':'/visual/theme_id','value':'background:red'},{'path':'/visual/platforms/unknown','value':'garden'},{'path':'/visual/pathway_id','value':'invented'}]:
   with self.assertRaises(ValueError):visuals.apply({},[operation],make_map())
 def test_followup_preserves_icons_and_supports_original_icon_restore(self):
  old={'theme_id':'peach_coral','icon_overrides':{'k1':'strategy'}};new,patch=visuals.apply(old,[{'path':'/visual/softness','value':'soft'}],make_map());self.assertEqual(new['icon_overrides'],old['icon_overrides']);self.assertEqual(patch,{'softness':'soft'});restored,_=visuals.apply(new,[{'path':'/visual/reset_icons','value':True}],make_map());self.assertEqual(restored['icon_overrides'],{})
 def test_copy_and_privacy_are_central_and_do_not_promise_provider_nonretention(self):
  c=json.loads((Path(__file__).resolve().parents[1]/'preview/copy.json').read_text());self.assertEqual(c['brand'],'PM Career Studio');self.assertEqual(c['heroSubtitle'],"See the person that you have become. Be inspired by who you are.");self.assertNotIn("isn't saved",c['privacyFallback']);self.assertFalse(c['feedbackUrl']);self.assertEqual(c['counter'],'PM Career DNAs Created')
