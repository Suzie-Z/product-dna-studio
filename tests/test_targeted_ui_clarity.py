import copy,unittest,json
from unittest.mock import patch
from tests import test_original_refinement as original
from tests.fixtures import SOURCE,make_map,make_generation
import career_pipeline as pipeline
class JourneyPriorities(unittest.TestCase):
 def test_both_stages_receive_depth_pm_selection_without_reordering_input(self):
  seen=[];source=copy.deepcopy(SOURCE)
  def response(payload,schema,prompt,stage=None):
   seen.append((copy.deepcopy(payload),prompt,stage))
   if stage=='career':return {'status':'ready','facts':[{'id':'f1','claim':'Owned product evaluation decisions','role_type':'AI PM','ownership':'owned','evidence_quotes':[{'source_id':source['source_id'],'quote':'As AI PM, I defined model evaluation criteria and product release decisions.'}]}],'clarification_question':None}
   return make_generation(3,3)
  with patch('career_ai.structured',side_effect=response),patch('career_ai.moderate'):result=pipeline.generate([source],'')
  self.assertEqual([x[2]for x in seen],['career','summary']);self.assertEqual(seen[0][0]['sources'],[SOURCE]);self.assertEqual(seen[1][0]['journey_selection'],pipeline.JOURNEY_SELECTION);self.assertIn('chronology',seen[1][1]);self.assertIn('never relabel it as PM',seen[0][1]);self.assertEqual(source,SOURCE);self.assertEqual(result['map']['status'],'ready')
class ClarityBrowser(unittest.TestCase):
 setUpClass=classmethod(original.OriginalBrowser.setUpClass.__func__)
 tearDownClass=classmethod(original.OriginalBrowser.tearDownClass.__func__)
 setUp=original.OriginalBrowser.setUp
 tearDown=original.OriginalBrowser.tearDown
 page=original.OriginalBrowser.page
 upload=original.OriginalBrowser.upload
 ready=original.OriginalBrowser.ready
 def test_privacy_is_one_inline_disclosure_on_desktop_and_mobile(self):
  page,context=self.page()
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000});self.assertFalse(page.locator('#privacy').evaluate('(e)=>e.open'));self.assertEqual(page.locator('#privacy details').count(),0);self.assertEqual(page.locator('#privacy > p').count(),1);self.assertNotIn('Technical details',page.locator('#privacy').inner_text());page.locator('#privacy summary').focus();page.keyboard.press('Enter');page.wait_for_function('document.getElementById("privacy").open');copy_text=page.locator('#privacy > p').inner_text();self.assertIn('48-hour',copy_text);self.assertIn('10 minutes',copy_text);self.assertIn('OpenAI',copy_text);self.assertIn('disk save',copy_text);self.assertEqual(page.locator('#privacy summary').evaluate('(e)=>getComputedStyle(e).justifyContent'),'flex-end');page.locator('#privacy summary').click()
  context.close()
 def test_header_retains_data_but_has_no_theme_pill_and_single_line_brand(self):
  page,context=self.page();data=make_map(5,4)
  for mobile in [False,True]:
   scene=page.evaluate('([d,m])=>buildDNAScene(d,m)',[data,mobile]);self.assertTrue(scene['metrics']['ok'],scene['metrics']['issues']);self.assertFalse(scene['metrics']['header']['theme_in_header']);self.assertEqual(scene['metrics']['header']['title_center_x'],scene['metrics']['width']/2)
   page.locator('#map-visual').evaluate('(e,svg)=>e.innerHTML=svg',scene['svg']);self.assertEqual(page.locator('[data-component="BrandWatermark"] text').count(),1);self.assertEqual(page.locator('[data-component="BrandWatermark"] text').text_content(),'PM Career Studio');self.assertNotIn(data['career_signature'],page.locator('#map-visual text').evaluate_all('(els)=>els.map(e=>e.textContent)'));self.assertIn(data['career_signature'],scene['svg'])
  context.close()
 def test_journey_and_card_spacing_actual_bounds(self):
  page,context=self.ready()
  for n in [2,3,4,5]:
   d=make_map(n,4)
   for strength in d['strengths']:strength['methods']=[{'label':s,'evidence_quote':strength['evidence_quotes'][0]}for s in ['Golden-set evaluation','Reliability trade-offs','Controlled experiments']]
   for mobile in [False,True]:
    m=page.evaluate('([d,m])=>buildDNAScene(d,m).metrics',[d,mobile]);self.assertTrue(m['ok'],m['issues']);self.assertFalse(m['collisions']);self.assertFalse(m['clipped'])
  page.evaluate('d=>renderDNAMap(document.getElementById("map-visual"),d)',make_map(5,4));gaps=page.evaluate('''()=>[...document.querySelectorAll('[data-component="EvidenceCapsule"]')].map(e=>{const p=document.querySelector('[data-foreground="'+e.dataset.for+':description"]');return e.getBoundingClientRect().top-p.getBoundingClientRect().bottom})''');self.assertTrue(all(g>5 for g in gaps),gaps);context.close()
 def test_refine_has_exactly_one_loading_message_and_no_duplicate_submission(self):
  page,context=self.ready();held=[];context.route('**/api/career-dna/refine',lambda r:held.append(r));page.locator('#edit-map').click();page.locator('#story').fill('Shorten the first capability');page.locator('#generate').click();page.wait_for_function('busy&&document.getElementById("refine-progress").offsetHeight>0');self.assertTrue(page.locator('#generate').is_disabled());self.assertEqual(page.locator('#generate').inner_text(),'Apply Changes');self.assertEqual(page.locator('#refine-dialog').inner_text().count('Applying your changes'),1);self.assertFalse(page.locator('#loading').is_visible());self.assertEqual(page.locator('#refine-status').inner_text(),'');page.evaluate('generate()');self.assertEqual(len(held),1);page.locator('#close-refine').click()
  for r in held:
   try:r.abort()
   except Exception:pass
  context.close()

 def test_long_single_evidence_wraps_without_truncation(self):
  page,context=self.page();d=make_map(3,4);label='WWWWWWWWWW WWWWWWWWWW';d['strengths'][3]['methods'][0]['label']=label;m=page.evaluate('d=>buildDNAScene(d,false).metrics',d);self.assertTrue(m['ok'],m['issues']);box=next(b for b in m['boxes']if b['text']==label);self.assertEqual(box['lines'],2);self.assertEqual(box['text'],label);context.close()
