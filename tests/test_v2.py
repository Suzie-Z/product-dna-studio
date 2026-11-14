"""V2 regressions: literal testimony, typed patches and multilingual audio boundary."""
import copy,io,json,os,threading,unittest,urllib.request,urllib.error,uuid
from unittest.mock import patch
import ai_server,career_ai as a,career_pipeline,semantic_refinement as edit,model_config,request_state
from tests.fixtures import SOURCE,make_map
EN='Please update the ones under Trust and Safety PM for Version 1. We should summarise the key points for Trust and Safety PM because I constructed safety frameworks and created safety pipelines from 0 to 1.'
ZH='把 Trust & Safety PM 下面的描述改成更高层次的能力，突出我建设安全框架和从零到一搭建安全管线的经验，其他内容保持不变。'
LABELS=['Safety Framework Development','0-to-1 Safety Pipelines & Infrastructure']
def safety_map():
 d=make_map(3,3);j=d['journey'][1];j.update(label='Trust & Safety PM',icon='trust_safety');return a.validate_map(d,[SOURCE])
class V2Contracts(unittest.TestCase):
 def test_exact_english_chinese_updates_attach_new_evidence_preserve_everything_else(self):
  for message in [EN,ZH]:
   previous=safety_map();snapshot=copy.deepcopy(previous)
   def response(payload,*args,**kwargs):
    self.assertEqual(kwargs['stage'],'refinement');src=payload['sources'][-1];options=edit.patch_schema(previous,payload['sources'])['properties']['changes']['items']['anyOf'];self.assertTrue(options)
    q={'source_id':src['source_id'],'quote':a.generation_schema([src])['properties']['journey']['items']['properties']['evidence_quotes']['items']['anyOf'][0]['properties']['quote']['enum'][-1]}
    return {'status':'ready','changes':[{'path':'/journey/j2/highlights','value':[{'label':label,'evidence_quote':q}for label in LABELS]}],'clarification_question':None,'change_summary':'Elevated only the Trust and Safety role highlights.'}
   with patch('career_ai.moderate'),patch('career_ai.structured',side_effect=response):out=a.process_refine({'sources':[SOURCE],'previous':previous,'message':message,'context_consent':True,'map_version':1})
   self.assertEqual([h['label']for h in out['map']['journey'][1]['highlights']],LABELS);self.assertEqual(previous,snapshot)
   expected=copy.deepcopy(previous);actual=copy.deepcopy(out['map'])
   for key in ['highlights','evidence_quotes','evidence_refs']:actual['journey'][1][key]=expected['journey'][1][key]
   self.assertEqual(actual,expected);self.assertIn(out['accepted_source']['source_id'],out['map']['journey'][1]['evidence_refs'])
 def test_copied_sentence_scopes_schema_and_reduces_context(self):
  previous=make_map(3,3);phrase=previous['strengths'][0]['description'];seen={}
  def reply(payload,schema,prompt,**kwargs):
   seen.update(payload=payload,schema=schema,prompt=prompt)
   return {'status':'ready','changes':[{'path':'/strengths/k1/description','value':'Diagnoses onboarding friction through research'}],'clarification_question':None,'change_summary':'Shortened only the requested sentence.'}
  with patch('career_ai.moderate'),patch('career_ai.structured',side_effect=reply):out=a.process_refine({'sources':[SOURCE],'previous':previous,'message':'Change “'+phrase+'” to “Diagnoses onboarding friction through research”.','context_consent':True})
  self.assertEqual(len(seen['payload']['previous']['strengths']),1);self.assertEqual(seen['payload']['previous']['journey'],[]);self.assertLess(len(seen['prompt']),len(a.PROMPT));self.assertEqual(out['map']['journey'],previous['journey']);self.assertEqual(out['map']['strengths'][1:],previous['strengths'][1:])
  branches=seen['schema']['properties']['changes']['items']['anyOf'];self.assertEqual([p for b in branches for p in b['properties']['path']['enum']if not p.startswith('/visual/')],['/strengths/k1/description'])
 def test_old_literal_detail_quote_does_not_need_new_excerpt_enum(self):
  previous=make_map(1,1);sources=[SOURCE];schema=edit.patch_schema(previous,sources);q={'source_id':SOURCE['source_id'],'quote':SOURCE['content'][10:60]};value=[{'label':'Evidence-led decisions','evidence_quote':q}];response={'status':'ready','changes':[{'path':'/journey/j1/highlights','value':value}],'clarification_question':None,'change_summary':'Updated the requested highlight.'};a.schema_validate(response,schema);self.assertEqual(edit.merge(previous,response['changes'],sources)['journey'][0]['highlights'],value)
 def test_repeated_updates_keep_detail_proofs_within_parent_bound(self):
  previous=make_map(1,1);previous['journey'][0]['evidence_quotes']=[{'source_id':SOURCE['source_id'],'quote':SOURCE['content'][i:i+50]}for i in range(6)]
  out=edit.merge(previous,[{'path':'/journey/j1/highlights','value':previous['journey'][0]['highlights']}],[SOURCE]);self.assertLessEqual(len(out['journey'][0]['evidence_quotes']),6)
  for detail in out['journey'][0]['highlights']:self.assertIn(detail['evidence_quote'],out['journey'][0]['evidence_quotes'])
 def test_typed_patch_rejects_unknown_paths_values_and_nested_array_indices(self):
  schema=edit.patch_schema(safety_map(),[SOURCE])
  for change in [{'path':'/journey/j2/highlights/999/label','value':'Test'},{'path':'/strengths/k1/label','value':99},{'path':'/__proto__','value':'evil'}]:
   with self.assertRaises(ValueError):a.schema_validate({'status':'ready','changes':[change],'clarification_question':None,'change_summary':'Updated.'},schema)
 def test_stage_settings_are_independent_and_override_is_authenticated_context_only(self):
  with patch.dict(os.environ,{'OPENAI_CAREER_MODEL':'career','OPENAI_SUMMARY_MODEL':'summary','OPENAI_REFINEMENT_MODEL':'refine'}):
   self.assertEqual([model_config.career_model(x)for x in ['career','summary','refinement']],['career','summary','refine'])
 def test_internal_budget_never_consumes_public_budget(self):
  a.COUNTER.update(day='',count=0);a.TEST_COUNTER.update(day='',count=0)
  with patch.dict(os.environ,{'TRIAL_START_DATE':'','DAILY_GENERATION_LIMIT':'1','INTERNAL_TEST_DAILY_LIMIT':'2'}):
   tok=model_config.INTERNAL_TEST.set(True)
   try:a.reserve_attempt();a.reserve_attempt()
   finally:model_config.INTERNAL_TEST.reset(tok)
   self.assertEqual(a.COUNTER['count'],0);a.reserve_attempt()
   with self.assertRaises(a.AppError):a.reserve_attempt()
