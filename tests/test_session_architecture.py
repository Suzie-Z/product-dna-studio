import copy,json,os,threading,unittest,urllib.request,urllib.error
from unittest.mock import patch
import ai_server as server,career_ai,request_state,generation_counts,model_config
from tests.fixtures import SOURCE,make_map
class Architecture(unittest.TestCase):
 def setUp(self):
  request_state.CACHE.clear();generation_counts._DAYS.clear();generation_counts._RECEIPTS.clear();generation_counts._START=None;server.RECENT.clear()
  self.env=patch.dict(os.environ,{'COUNTER_DATABASE_URL':'','PUBLIC_COUNTER_ENV':'production','PM_INTERNAL_TEST_TOKEN':'local-test-only','OPENAI_MODEL':'legacy-model','OPENAI_CAREER_MODEL':''});self.env.start()
  self.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);threading.Thread(target=self.http.serve_forever,daemon=True).start();self.origin='http://127.0.0.1:'+str(self.http.server_port)
 def tearDown(self):self.http.shutdown();self.http.server_close();self.env.stop()
 def post(self,path,body,internal=False):
  headers={'Content-Type':'application/json'}
  if internal:headers['X-PM-Internal-Test']='local-test-only'
  req=urllib.request.Request(self.origin+path,data=json.dumps(body).encode(),headers=headers)
  try:r=urllib.request.urlopen(req,timeout=10)
  except urllib.error.HTTPError as e:r=e
  with r:return r.status,json.load(r)
 def test_idempotent_public_initial_and_refinement_never_double_count(self):
  body={'sources':[SOURCE],'request_id':'req_same_initial_0123456789'}
  with patch.dict(server.__dict__['Handler'].do_POST.__globals__,{}):
   with patch('ai_server.process_generate',return_value={'map':make_map(1,1)})as generate,patch('ai_server.process_refine',return_value={'map':make_map(1,1)}):
    code,a=self.post('/api/career-dna/generate',body);code,b=self.post('/api/career-dna/generate',body)
    self.assertEqual(code,200);self.assertEqual(generate.call_count,1);self.assertEqual(a,b);self.assertEqual(generation_counts.snapshot()['total_generations'],1)
    code,edit=self.post('/api/career-dna/refine',{'request_id':'req_refine_unique_01234567','map_version':1,'next_version':3})
    self.assertEqual(code,200);self.assertEqual(edit['map_version'],3);self.assertEqual(edit['base_version'],1);self.assertEqual(generation_counts.snapshot()['total_generations'],1)
    code,_=self.post('/api/career-dna/generate',{**body,'sources':[{**SOURCE,'content':'Different input'}]});self.assertEqual(code,409)
 def test_internal_and_nonproduction_initials_do_not_count(self):
  with patch('ai_server.process_generate',return_value={'map':make_map(1,1)}):
   code,value=self.post('/api/career-dna/generate',{'sources':[SOURCE],'request_id':'req_internal_0123456789'},internal=True);self.assertEqual(code,200);self.assertFalse(value['counted'])
   with patch.dict(os.environ,{'PUBLIC_COUNTER_ENV':'staging'}):code,value=self.post('/api/career-dna/generate',{'sources':[SOURCE],'request_id':'req_staging_0123456789'})
   self.assertEqual(code,200);self.assertFalse(value['counted']);self.assertEqual(generation_counts.snapshot()['total_generations'],0)
 def test_failed_and_clarification_do_not_count_and_can_retry(self):
  body={'sources':[SOURCE],'request_id':'req_failure_0123456789'}
  with patch('ai_server.process_generate',side_effect=[career_ai.AppError(502,'Try again.','provider_timeout'),{'map':make_map(1,1)}])as generate:
   self.assertEqual(self.post('/api/career-dna/generate',body)[0],502);self.assertEqual(generation_counts.snapshot()['total_generations'],0)
   self.assertEqual(self.post('/api/career-dna/generate',body)[0],200);self.assertEqual(generate.call_count,2)
  with patch('ai_server.process_generate',return_value={'map':career_ai.clarification('Which product responsibility did you own?')}):self.assertEqual(self.post('/api/career-dna/generate',{'sources':[SOURCE],'request_id':'req_question_0123456789'})[0],200)
  self.assertEqual(generation_counts.snapshot()['total_generations'],1)
 def test_receipt_survives_response_cache_loss_without_storing_content(self):
  r='req_receipt_0123456789';a=generation_counts.snapshot(True,r);request_state.CACHE.clear();b=generation_counts.snapshot(True,r)
  self.assertEqual((a['generation_number'],b['generation_number'],b['total_generations']),(1,1,1));self.assertNotIn(r,json.dumps(generation_counts._RECEIPTS));self.assertNotIn(SOURCE['content'],json.dumps(generation_counts._RECEIPTS))
 def test_pending_duplicate_does_not_erase_original_and_ttl_cleans(self):
  r='req_pending_0123456789';self.assertEqual(request_state.begin(r,{'sources':[SOURCE]})[0],'new');self.assertEqual(request_state.begin(r,{'sources':[SOURCE]})[0],'pending');request_state.finish(r,{'map':make_map(1,1)});self.assertEqual(request_state.begin(r,{'sources':[SOURCE]})[0],'replay')
  with patch('request_state.time.monotonic',return_value=request_state.CACHE[r]['expires']+1):self.assertEqual(request_state.begin('req_next_01234567890123',{})[0],'new')
  self.assertNotIn(r,request_state.CACHE)
 def test_cost_estimate_includes_new_model_cache_write_charges(self):
  from tools.benchmark_pm_models import estimated_cost
  sample=[{'model':'gpt-6.1-sol','usage':{'input_tokens':3000,'input_tokens_details':{'cached_tokens':1000,'cache_write_tokens':1000},'output_tokens':500}}]
  self.assertEqual(estimated_cost(sample),.0096)
 def test_pure_visual_changes_preserve_all_facts_without_model_call(self):
  for message,patch_value in [('Change only the background to blue',{'theme_id':'sky_blue'}),('把背景换成绿色',{'theme_id':'mint_green'}),('Use another character',{'next_neutral_avatar':True})]:
   before=make_map(1,1)
   with patch('career_ai.provider')as provider:
    out=career_ai.process_refine({'sources':[SOURCE],'previous':before,'message':message,'context_consent':True})
   provider.assert_not_called();self.assertEqual(out['map']['status'],'needs_more_info');self.assertNotIn('presentation_patch',out)
 def test_model_priority_and_private_diagnostics(self):
  self.assertEqual(model_config.career_model(),'legacy-model')
  with patch.dict(os.environ,{'OPENAI_CAREER_MODEL':'separate-career-model','OPENAI_API_KEY':'never-print-this-secret'}):
   self.assertEqual(model_config.career_model(),'separate-career-model');self.assertNotIn('never-print',json.dumps(model_config.configuration()))
  with patch('ai_server.diagnostics',return_value={'career_model':'legacy-model'}):
   self.assertEqual(self.post('/api/internal/models',{})[0],403);self.assertEqual(self.post('/api/internal/models',{},True)[0],200)
 def test_invalid_version_rejected_before_model_and_public_override_ignored(self):
  with patch('ai_server.process_generate',return_value={'map':make_map(1,1)})as generate:
   self.assertEqual(self.post('/api/career-dna/generate',{'next_version':-1})[0],400);generate.assert_not_called()
   code,value=self.post('/api/career-dna/generate',{'benchmark_model':'expensive-unapproved-model','request_id':'req_override_0123456789'})
   self.assertEqual(code,200);self.assertEqual(value['model'],'legacy-model')
 def test_multilingual_actual_pm_titles_pass_scope_without_english_titles(self):
  for content in ['Soy gerente de producto y priorizo requisitos con clientes.','Je suis chef de produit et je définis les priorités.','Ich bin Produktmanager und priorisiere Kundenanforderungen.','Sou gerente de produto e priorizo requisitos.','私はプロダクトマネージャーです。','저는 프로덕트 매니저입니다.','أنا مدير منتج وأحدد الأولويات.']:
   self.assertTrue(career_ai.has_pm_context([{**SOURCE,'content':content}]),content)
 def test_prior_roles_are_not_relabeled_as_pm_and_transition_requires_evidence(self):
  src={**SOURCE,'content':'I am a platform product manager. Previously I was a software engineer who built API services and reviewed reliability constraints.'};m=make_map(1,1);m['journey'][0]['label']='Software Engineer'
  for item in m['journey']+m['strengths']:
   item['evidence_quotes'][0]['quote']='Previously I was a software engineer who built API services and reviewed reliability constraints.'
   for detail in item.get('highlights',[])+item.get('methods',[]):detail['evidence_quote']['quote']=item['evidence_quotes'][0]['quote']
  self.assertEqual(career_ai.validate_map(m,[src])['journey'][0]['label'],'Software Engineer')
  self.assertFalse(career_ai.has_pm_transition([{**SOURCE,'content':'I am an engineer and hope to become a product manager.'}]))
  self.assertTrue(career_ai.has_pm_transition([{**SOURCE,'content':'I am transitioning into product management after working as a consultant. I conducted customer discovery and prioritised product requirements for an internal customer portal.'}]))
