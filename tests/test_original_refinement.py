"""Complete-original iteration contracts and focused user-visible regressions."""
import copy,json,unittest
from unittest.mock import patch
from pathlib import Path
import career_ai as a,semantic_refinement as refine,refinement_validation as validation
from tests.fixtures import SOURCE,make_map,REFLECTIONS
from tests import test_core_experience as core
from tests.test_core_experience import provider,ART
class EditContracts(unittest.TestCase):
 def test_exact_unquoted_tag_target_preserves_sibling_and_proof(self):
  previous=make_map(1,1);previous['strengths'][0]['methods']=[{'label':'Launch requirements','evidence_quote':previous['strengths'][0]['evidence_quotes'][0]},{'label':'User research','evidence_quote':previous['strengths'][0]['evidence_quotes'][0]}]
  message='Change Launch requirements to Design for lasting value.'
  self.assertEqual(refine.quoted_targets(previous,message),{'/strengths/k1/methods/0/label'})
  patch_value={'status':'ready','changes':[{'path':'/strengths/k1/methods/0/label','value':'Design for lasting value'}],'clarification_question':None,'change_summary':'Updated the chosen skill indicator.'}
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=patch_value):out=a.process_refine({'sources':[SOURCE],'previous':previous,'message':message,'context_consent':True})
  expected=copy.deepcopy(previous);expected['strengths'][0]['methods'][0]['label']='Design for lasting value';self.assertEqual(out['map'],expected);self.assertEqual(out['presentation_patch'],{})
 def test_conclusion_is_the_summary_banner_not_a_reflection_question(self):
  self.assertEqual(refine.named_sections('Make only the conclusion less generic.'),{'/superpower'})
  seen={}
  def response(payload,*args,**kwargs):
   seen.update(payload);return {'status':'ready','changes':[{'path':'/superpower','value':'Turning user research into evidence led growth decisions'}],'clarification_question':None,'change_summary':'Made the concluding summary more specific.'}
  previous=make_map(1,1)
  with patch('career_ai.moderate'),patch('career_ai.structured',side_effect=response):out=a.process_refine({'sources':[SOURCE],'previous':previous,'reflections':REFLECTIONS,'message':'Make only the conclusion less generic.','context_consent':True})
  self.assertEqual(out['changed_fields'],['/superpower']);self.assertEqual(out['reflections'],REFLECTIONS);self.assertIn('/superpower',seen['section_definitions']);self.assertEqual(seen['map_context']['capabilities'][0]['id'],'k1')
 def test_blank_instruction_has_inline_error_without_model(self):
  for message in ['Clear the description','Leave the theme blank','Change the title to ""','Make this field empty','把标题清空']:
   with patch('career_ai.structured')as model,patch('career_ai.moderate'):
    with self.assertRaises(a.AppError)as failure:a.process_refine({'sources':[SOURCE],'previous':make_map(),'message':message,'context_consent':True})
   self.assertEqual(failure.exception.code,'required_field_blank');model.assert_not_called()
 def test_model_blank_patch_is_rejected_without_alternative_confirmation(self):
  response={'status':'ready','changes':[{'path':'/strengths/k1/description','value':''}],'clarification_question':None,'change_summary':'Changed.'}
  with patch('career_ai.structured',return_value=response)as model,patch('career_ai.moderate'):
   with self.assertRaises(a.AppError)as failure:a.process_refine({'sources':[SOURCE],'previous':make_map(),'message':'Make my first insight more precise','context_consent':True})
  self.assertEqual(failure.exception.code,'required_field_blank');self.assertEqual(model.call_count,1)
 def test_no_unbounded_index_or_visual_or_reorder_paths(self):
  schema=refine.patch_schema(make_map(),[SOURCE]);paths=[x for branch in schema['properties']['changes']['items']['anyOf']for x in branch['properties']['path']['enum']];self.assertNotIn('/strength_order',paths);self.assertFalse(any('/icon'in p or '/visual/'in p or '/999/'in p for p in paths))
class OriginalBrowser(unittest.TestCase):
 setUpClass=classmethod(core.CoreBrowser.setUpClass.__func__)
 tearDownClass=classmethod(core.CoreBrowser.tearDownClass.__func__)
 setUp=core.CoreBrowser.setUp
 page=core.CoreBrowser.page
 upload=core.CoreBrowser.upload
 ready=core.CoreBrowser.ready
 # Inherit the real HTTP/parser/transport fixture; new cases target the new acceptance criteria.
 def test_panels_match_and_only_two_reflection_sections(self):
  page,context=self.ready();self.assertFalse(page.locator('#reflection-reading').evaluate('(e)=>e.open'));self.assertFalse(page.locator('#full-journey').evaluate('(e)=>e.open'));self.assertEqual(page.locator('#reflection-reading h4').all_text_contents(),['Recognition','Possibilities to Explore']);boxes=[page.locator('#'+key).bounding_box()for key in ['reflection-reading','full-journey']];self.assertAlmostEqual(boxes[0]['x'],boxes[1]['x'],delta=1);self.assertAlmostEqual(boxes[0]['width'],boxes[1]['width'],delta=1);page.locator('#reflection-reading summary').click();page.locator('#full-journey summary').click();self.assertTrue(page.locator('#reflection-reading').evaluate('(e)=>e.open'));self.assertTrue(page.locator('#full-journey').evaluate('(e)=>e.open'));page.locator('#result-panel').screenshot(path=str(ART/'reading-panels.png'));context.close()
 def test_fixed_modal_header_empty_new_session_and_no_history(self):
  page,context=self.ready();page.set_viewport_size({'width':390,'height':540});page.locator('#edit-map').click();page.locator('#story').fill('An abandoned instruction');page.locator('#close-refine').click();page.locator('#edit-map').click();self.assertEqual(page.locator('#story').input_value(),'');self.assertEqual(page.locator('#voice,#refine-history').count(),0);before=page.locator('.refine-modal-header').bounding_box();page.locator('#refine-scroll').evaluate('(e)=>e.scrollTop=e.scrollHeight');after=page.locator('.refine-modal-header').bounding_box();self.assertAlmostEqual(before['y'],after['y'],delta=1);self.assertTrue(page.locator('#close-refine').is_visible());page.screenshot(path=str(ART/'mobile-sticky-modal.png'));page.locator('#close-refine').click();self.assertFalse(page.locator('#refine-dialog').is_visible());context.close()
 def test_blank_edit_and_api_error_keep_input_and_current_map(self):
  page,context=self.ready();previous=page.evaluate('structuredClone(result)');page.locator('#edit-map').click();page.locator('#story').fill('Clear the description');page.locator('#generate').click();page.wait_for_function('!busy&&document.getElementById("refine-status").textContent.includes("blank")');self.assertTrue(page.locator('#refine-dialog').is_visible());self.assertEqual(page.evaluate('result'),previous);self.assertEqual(page.locator('#story').input_value(),'Clear the description');self.assertTrue(page.locator('#generate').is_enabled());self.assertNotIn('Would you like',page.locator('#refine-status').inner_text());context.close()
 def test_processing_indicator_tracks_real_pending_operation(self):
  page,context=self.ready();held=[];context.route('**/api/career-dna/refine',lambda r:held.append(r));page.locator('#edit-map').click();page.locator('#story').fill('Shorten my first capability.');page.locator('#generate').click();page.wait_for_function('busy');self.assertTrue(page.locator('#refine-progress').is_visible());self.assertTrue(page.locator('#generate').is_disabled());self.assertEqual(page.evaluate('versions.length'),1);page.locator('#close-refine').click();page.wait_for_function('!busy');self.assertEqual(page.evaluate('versions.length'),1)
  for route in held:
   try:route.abort()
   except Exception:pass
  context.close()
 def test_uniform_platforms_integrated_theme_summary_and_curves(self):
  page,context=self.ready()
  for mobile in [False,True]:
   for count in [1,2,3,4]:
    data=make_map(count,count);metrics=page.evaluate('([d,m])=>buildDNAScene(d,m,{platform_overrides:{j1:"garden",j2:"crystal",j3:"steps"}}).metrics',[data,mobile]);self.assertTrue(metrics['ok'],metrics['issues']);self.assertEqual(len(set(metrics['platforms'].values())),1);self.assertTrue(metrics['header']['theme_in_header']);self.assertEqual(metrics['collisions'],[])
  self.assertEqual(page.locator('[data-component="JourneyToDNA"] path').count(),6);self.assertEqual(page.locator('[data-component="CareerDNASummary"]').count(),1);page.locator('#map-visual').screenshot(path=str(ART/'approved-composition.png'));context.close()

class ModelAndScopeHTTP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import ai_server,threading
  cls.server=ai_server.ThreadingHTTPServer(('127.0.0.1',0),ai_server.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url='http://127.0.0.1:'+str(cls.server.server_port)
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
 def test_exact_supported_model_ids_are_reported_without_silent_alias(self):
  import urllib.request,model_config
  before=model_config.career_model('refinement')
  for ids,expected in [({'gpt-6-sol','gpt-6.1-sol'},True),({'gpt-6-astra','gpt-6.1-sol'},False)]:
   with patch('ai_server.available_models',return_value={'state':'checked','ids':ids}):data=json.load(urllib.request.urlopen(self.url+'/api/refinement-model'))
   self.assertEqual(data['requested_model_available'],expected);self.assertEqual(data['requested_model'],'gpt-6-sol');self.assertNotIn('gpt-6.1-sol',data['supported_model_ids']);self.assertNotIn('key',data)
  self.assertEqual(model_config.career_model('refinement'),before)
 def test_voice_routes_are_removed(self):
  import urllib.request,urllib.error
  for path in ['/api/transcribe','/api/internal/audio-fixture']:
   request=urllib.request.Request(self.url+path,data=b'{}',headers={'Content-Type':'application/json'})
   with self.assertRaises(urllib.error.HTTPError)as failure:urllib.request.urlopen(request)
   self.assertEqual(failure.exception.code,404)
 def test_distinct_pm_cv_evidence_does_not_cross_contaminate(self):
  from tests.fixtures import QUOTES
  for index in [0,1,3]:
   data=make_map(4,4);data['journey']=[data['journey'][index]];data['journey'][0]['order']=1;data['strengths']=[data['strengths'][index]]
   source={**SOURCE,'source_type':'cv','content':'I am '+data['journey'][0]['label']+'. '+QUOTES[index]}
   self.assertEqual(a.validate_map(data,[source])['strengths'][0]['label'],data['strengths'][0]['label'])
   other={**source,'content':'I am a product manager. '+QUOTES[(index+1)%4]}
   with self.assertRaises(ValueError):a.validate_map(data,[other])
