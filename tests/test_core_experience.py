"""Original-map CV-first flow. Actual browser, DOCX parser and API; provider mocked."""
import copy,io,json,unittest,urllib.request
from pathlib import Path
from unittest.mock import patch
from docx import Document
import career_ai as a,career_reflection as reflection
from tests.fixtures import SOURCE,make_map
from tests import test_e2e as e2e
ART=e2e.ART/'core-experience'
SECTIONS={'recognition':{'text':'Your experience connects user insight with practical product trade-offs, making decisions clearer across teams.','evidence_ids':['k1']},'aspiration':{'text':'Your evidenced strengths could inform discovery-led products or experimentation-focused work.','evidence_ids':['k1']}}
def provider(path,payload,timeout=90):
 response=e2e.model_transport(path,payload,timeout)
 if path=='responses':
  schema=payload.get('text',{}).get('format',{}).get('schema',{})
  if 'recognition'in schema.get('properties',{}):
   text=response['output'][0]['content'][0];d=json.loads(text['text']);d.update(copy.deepcopy(SECTIONS));text['text']=json.dumps(d)
 return response
class ReflectionContracts(unittest.TestCase):
 def test_generation_schema_requires_grounded_distinct_sections(self):
  schema=reflection.generation_schema(a.generation_schema([SOURCE]));self.assertIn('recognition',schema['required']);self.assertIn('aspiration',schema['required']);reflection.validate(SECTIONS,make_map())
 def test_unknown_evidence_and_prescribed_future_are_rejected(self):
  for update in [{'text':'You will become a director.','evidence_ids':['k1']},{'text':'You could explore products or platforms.','evidence_ids':['invented']}]:
   sections=copy.deepcopy(SECTIONS);sections['aspiration']=update
   with self.assertRaises(ValueError):reflection.validate(sections,make_map())
 def test_targeted_recognition_edit_preserves_map_and_aspiration(self):
  previous=make_map();updated={'text':'Your research and experiments make uncertain growth decisions more concrete.','evidence_ids':['k1']};response={'status':'ready','changes':[{'path':'/recognition','value':updated}],'clarification_question':None,'change_summary':'Made Recognition more specific.'}
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=response):out=a.process_refine({'sources':[SOURCE],'previous':previous,'reflections':SECTIONS,'message':'Make Recognition more specific to my research and experiments.','context_consent':True})
  self.assertEqual(out['map'],previous);self.assertEqual(out['reflections']['aspiration'],SECTIONS['aspiration']);self.assertEqual(out['reflections']['recognition'],updated);self.assertEqual(out['presentation_patch'],{})
 def test_model_cannot_smuggle_icon_change_in_whole_category_patch(self):
  previous=make_map();items=copy.deepcopy(previous['strengths']);items[0]['icon']='ai';response={'status':'ready','changes':[{'path':'/strengths','value':items}],'clarification_question':None,'change_summary':'Adjusted emphasis.'}
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=response):
   with self.assertRaises(a.AppError):a.process_refine({'sources':[SOURCE],'previous':previous,'message':'Adjust the emphasis in my first capability.','context_consent':True})
class CoreBrowser(unittest.TestCase):
 setUpClass=classmethod(e2e.CompleteFlow.setUpClass.__func__)
 tearDownClass=classmethod(e2e.CompleteFlow.tearDownClass.__func__)
 setUp=e2e.CompleteFlow.setUp
 page=e2e.CompleteFlow.page
 def upload(self,page,name='original.docx',text=None):
  assets=e2e.ART/'parser-assets';assets.mkdir(exist_ok=True);js=assets/'mammoth.browser.min.js'
  if not js.exists():js.write_bytes(urllib.request.urlopen('https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.9.1/mammoth.browser.min.js',timeout=30).read())
  page.context.route('https://cdnjs.cloudflare.com/ajax/libs/mammoth/**',lambda route:route.fulfill(path=str(js),content_type='text/javascript',headers={'Access-Control-Allow-Origin':'*'}))
  doc=Document();doc.add_paragraph(text or SOURCE['content']);buf=io.BytesIO();doc.save(buf);page.locator('#file').set_input_files({'name':name,'mimeType':'application/vnd.openxmlformats-officedocument.wordprocessingml.document','buffer':buf.getvalue()});page.wait_for_function('(name)=>!reading&&cvName===name',arg=name)
 def ready(self):
  page,context=self.page();self.upload(page)
  with patch('career_ai.provider',side_effect=provider):page.locator('#generate').click();page.wait_for_function('activeVersion?.number===1&&!busy')
  return page,context
 def test_upload_generate_refine_twice_undo_single_export(self):
  ART.mkdir(parents=True,exist_ok=True);page,context=self.page();self.assertFalse(page.locator('#refine-dialog').is_visible());self.assertFalse(page.locator('#story').is_visible());self.upload(page);self.assertTrue(page.locator('#generate').is_enabled());page.screenshot(path=str(ART/'cv-first.png'),full_page=True)
  with patch('career_ai.provider',side_effect=provider):
   page.locator('#generate').click();page.wait_for_function('activeVersion?.number===1&&!busy');self.assertFalse(page.locator('#refine-dialog').is_visible());self.assertEqual(page.evaluate('activeVersion.reflections.recognition.text'),SECTIONS['recognition']['text']);before=page.evaluate('structuredClone(renderVariant)');original=page.evaluate('structuredClone(result)');page.locator('#result-panel').screenshot(path=str(ART/'original-map.png'))
   for version in [2,3]:
    page.locator('#edit-map').click();self.assertTrue(page.locator('#story').is_visible());page.locator('#story').fill('Rename only the first capability to Applied Discovery.');page.locator('#generate').click();page.wait_for_function('(v)=>activeVersion.number===v&&!busy',arg=version);self.assertEqual(page.evaluate('renderVariant'),before);self.assertEqual(page.evaluate('result.journey'),original['journey']);self.assertFalse(page.locator('#refine-dialog').is_visible())
  page.locator('#undo').click();page.wait_for_function('activeVersion.number===2&&!busy');page.locator('#edit-map').click();page.screenshot(path=str(ART/'refine-on-demand.png'),full_page=True);page.locator('#close-refine').click()
  with page.expect_download()as download:page.locator('#save').click()
  file=ART/'single-map.png';download.value.save_as(str(file));from PIL import Image
  with_image=Image.open(file);self.assertEqual(with_image.size,(3200,1800));with_image.close();self.assertEqual(page.locator('#map-visual > svg').count(),1);context.close()
 def test_replacement_cv_runs_full_analysis_without_old_sources(self):
  page,context=self.ready();requests=[];page.on('request',lambda r:requests.append(r.post_data_json)if r.url.endswith('/generate')else None);page.locator('#edit-map').click();self.upload(page,'replacement.docx','I am a growth product manager. I owned onboarding requirements, user research and prioritised growth experiments.');self.assertIn('new analysis',page.locator('.replacement-cv').inner_text());self.assertEqual(page.locator('#generate').inner_text(),'Analyze New CV')
  with patch('career_ai.provider',side_effect=provider):page.locator('#generate').click();page.wait_for_function('activeVersion.number===2&&!busy')
  self.assertEqual(len(requests),1);self.assertEqual(len(requests[0]['sources']),1);self.assertEqual(requests[0]['sources'][0]['source_label'],'replacement.docx');self.assertNotIn('previous',requests[0]);self.assertEqual(page.evaluate('activeVersion.parent_id'),None);context.close()
 def test_visual_request_asks_question_and_keeps_existing_map(self):
  page,context=self.ready();old=page.evaluate('({map:result,visual:renderVariant})');page.locator('#edit-map').click();page.locator('#story').fill('Change the background to blue');page.locator('#generate').click();page.wait_for_function('!busy&&pendingQuestion.length>0');self.assertEqual(page.evaluate('({map:result,visual:renderVariant})'),old);self.assertEqual(page.evaluate('versions.length'),1);self.assertIn('Generate a New Map',page.locator('#refine-status').inner_text());context.close()
 def test_failed_update_retries_same_request_and_keeps_visuals(self):
  page,context=self.ready();old=page.evaluate('structuredClone(renderVariant)');requests=[]
  def intercept(route):
   requests.append(route.request.post_data_json)
   if len(requests)==1:route.fulfill(status=502,content_type='application/json',body=json.dumps({'error':'Temporary service interruption.'}))
   else:route.continue_()
  context.route('**/api/career-dna/refine',intercept);page.locator('#edit-map').click();page.locator('#story').fill('Shorten the first capability title.');page.locator('#generate').click();page.locator('#refine-retry').wait_for(state='visible');self.assertEqual(page.evaluate('versions.length'),1)
  with patch('career_ai.provider',side_effect=provider):page.locator('#refine-retry').click();page.wait_for_function('activeVersion.number===2&&!busy')
  self.assertEqual(requests[0],requests[1]);self.assertEqual(page.evaluate('renderVariant'),old);context.close()
 def test_close_during_update_cannot_commit_late_version(self):
  page,context=self.ready();held=[];context.route('**/api/career-dna/refine',lambda route:held.append(route));page.locator('#edit-map').click();page.locator('#story').fill('Shorten my first description.');page.locator('#generate').click();page.wait_for_function('busy');page.locator('#close-refine').click();page.wait_for_function('!busy');self.assertEqual(page.evaluate('versions.length'),1);self.assertFalse(page.locator('#refine-dialog').is_visible())
  for route in held:
   try:route.abort()
   except Exception:pass
  context.close()
 def test_pdf_upload_uses_original_browser_parser(self):
  from reportlab.pdfgen import canvas
  assets=e2e.ART/'parser-assets';assets.mkdir(exist_ok=True)
  for name in ['pdf.min.mjs','pdf.worker.min.mjs']:
   file=assets/name
   if not file.exists():file.write_bytes(urllib.request.urlopen('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/'+name,timeout=30).read())
  page,context=self.page();context.route('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/**',lambda route:route.fulfill(path=str(assets/route.request.url.rsplit('/',1)[-1]),content_type='text/javascript',headers={'Access-Control-Allow-Origin':'*'}));buf=io.BytesIO();c=canvas.Canvas(buf);c.drawString(30,700,'I am a platform product manager. I owned reusable product capabilities and prioritised requirements.');c.save();page.locator('#file').set_input_files({'name':'resume.pdf','mimeType':'application/pdf','buffer':buf.getvalue()});page.wait_for_function('!reading&&cvName==="resume.pdf"');self.assertIn('product manager',page.evaluate('cvText'));self.assertTrue(page.locator('#generate').is_enabled());context.close()
 def test_mobile_modal_voice_fallback_and_txt_rejection(self):
  page,context=self.ready();page.set_viewport_size({'width':390,'height':844});page.locator('#edit-map').click();page.evaluate('window.MediaRecorder=undefined;window.SpeechRecognition=undefined;window.webkitSpeechRecognition=undefined');page.locator('#voice').click();self.assertIn('unavailable',page.locator('#refine-status').inner_text());self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'));page.locator('#file').set_input_files({'name':'resume.txt','mimeType':'text/plain','buffer':b'Unsupported text input'});self.assertIn('PDF or DOCX',page.locator('#refine-status').inner_text());context.close()
