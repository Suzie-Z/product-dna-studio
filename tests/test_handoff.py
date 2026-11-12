import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import career_ai as a,visual_catalog as visuals
from tests.fixtures import SOURCE,make_map
class HandoffContracts(unittest.TestCase):
 def test_original_manifest_has_six_shapes_four_paths_and_semantic_alternatives(self):
  m=visuals.MANIFEST;self.assertGreaterEqual(len({p['shapeVariant']for p in m['platforms']}),6);self.assertGreaterEqual(len(m['pathways']),4);self.assertTrue(all(len(v)>=3 for v in m['concepts'].values()))
 def test_freeform_visual_patch_changes_presentation_only_and_keeps_evidence(self):
  previous=make_map();current={'theme_id':'lilac_light','icon_overrides':{'k1':'analytics'},'pathway_id':'glow'}
  operations=[{'path':'/visual/theme_id','value':'peach_coral'},{'path':'/visual/pathway_id','value':'constellation'},{'path':'/visual/platforms/j2','value':'modular'},{'path':'/visual/icons/k3','value':'collaboration'},{'path':'/visual/contrast','value':'high'}]
  response={'status':'ready','changes':operations,'clarification_question':None,'change_summary':'A warmer palette, constellation path and more varied platforms.'}
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=response)as call:
   out=a.process_refine({'sources':[SOURCE],'previous':previous,'visual':current,'edit_history':[{'instruction':'Please use softer colors','visual':current}],'message':'Warm this up and use a star trail; give the second island a modular shape and the third card a people icon.','context_consent':True})
  self.assertEqual(out['map'],previous);self.assertTrue(out['visual_only']);self.assertIsNone(out['accepted_source']);self.assertEqual(out['presentation_patch']['icon_overrides'],{'k1':'analytics','k3':'collaboration'});self.assertEqual(current['theme_id'],'lilac_light');self.assertIn('visual_manifest',call.call_args.args[0]);self.assertEqual(len(call.call_args.args[0]['edit_history']),1)
 def test_mixed_copy_and_visual_instruction_are_both_allowed(self):
  previous=make_map();response={'status':'ready','changes':[{'path':'/strengths/k1/label','value':'Growth Judgement'},{'path':'/visual/softness','value':'soft'}],'clarification_question':None,'change_summary':'Updated the title and softened the palette.'}
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=response):out=a.process_refine({'sources':[SOURCE],'previous':previous,'message':'Change “Growth Experimentation” to “Growth Judgement” and soften the colors.','context_consent':True})
  self.assertEqual(out['map']['strengths'][0]['label'],'Growth Judgement');self.assertEqual(out['presentation_patch'],{'softness':'soft'});self.assertEqual(out['map']['journey'],previous['journey'])
 def test_invalid_asset_ids_css_and_target_ids_are_rejected(self):
  for operation in [{'path':'/visual/icons/k1','value':'https://evil.example/icon.svg'},{'path':'/visual/theme_id','value':'background:red'},{'path':'/visual/platforms/unknown','value':'garden'},{'path':'/visual/pathway_id','value':'invented'}]:
   with self.assertRaises(ValueError):visuals.apply({},[operation],make_map())
 def test_followup_preserves_icons_and_supports_original_icon_restore(self):
  old={'theme_id':'peach_coral','icon_overrides':{'k1':'strategy'}};new,patch=visuals.apply(old,[{'path':'/visual/softness','value':'soft'}],make_map());self.assertEqual(new['icon_overrides'],old['icon_overrides']);self.assertEqual(patch,{'softness':'soft'});restored,_=visuals.apply(new,[{'path':'/visual/reset_icons','value':True}],make_map());self.assertEqual(restored['icon_overrides'],{})
 def test_copy_and_privacy_are_central_and_do_not_promise_provider_nonretention(self):
  c=json.loads((Path(__file__).resolve().parents[1]/'preview/copy.json').read_text());self.assertEqual(c['brand'],'PM Career Studio');self.assertEqual(c['heroSubtitle'],"See how far you've come. Be inspired by who you are.");self.assertNotIn("isn't saved",c['privacyFallback']);self.assertFalse(c['feedbackUrl']);self.assertEqual(c['counter'],'PM Career DNAs Created')
