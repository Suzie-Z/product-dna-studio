"""Internal career facts are not poster display copy."""
import copy,unittest
from unittest.mock import patch
import career_ai as a,career_pipeline as pipeline
from tests.fixtures import SOURCE,make_map

def fact(claim='Owned a product roadmap'):
 return {'status':'ready','facts':[{'id':'f1','claim':claim,'role_type':'Platform PM','ownership':'owned','evidence_quotes':[{'source_id':SOURCE['source_id'],'quote':SOURCE['content'][10:70]}]}],'clarification_question':None}
class FactValidation(unittest.TestCase):
 def test_literal_partial_quote_is_valid_without_excerpt_enum(self):
  d=fact();self.assertEqual(pipeline.validate(d,[SOURCE])['status'],'ready')
 def test_real_percentages_and_evaluation_ratios_are_allowed_in_internal_facts(self):
  for claim in ['Reviewed 20/100 model outputs before release.','Reduced response time by 20%.','Evaluated 6/10 sampled cases.','A'*235+' 20%']:
   self.assertEqual(pipeline.validate(fact(claim),[SOURCE])['status'],'ready')
 def test_display_ratings_still_rejected(self):
  d=make_map(1,1);d['strengths'][0]['label']='95% expert'
  with self.assertRaises(ValueError):a.validate_map(d,[SOURCE])
 def test_ready_empty_question_and_duplicate_internal_ids_normalise(self):
  d=fact();d['facts'].append(copy.deepcopy(d['facts'][0]));d['clarification_question']='';out=pipeline.validate(d,[SOURCE]);self.assertIsNone(out['clarification_question']);self.assertEqual([f['id']for f in out['facts']],['fact_1','fact_2'])
 def test_invented_or_empty_quotes_and_non_english_claims_remain_invalid(self):
  for quote in ['','x','I invented this job.']:
   d=fact();d['facts'][0]['evidence_quotes'][0]['quote']=quote
   with self.assertRaises(ValueError):pipeline.validate(d,[SOURCE])
  with self.assertRaises(ValueError):pipeline.validate(fact('我管理产品需求'),[SOURCE])
 def test_repair_receives_rejected_draft_and_targeted_field_feedback(self):
  bad=fact();bad['facts'][0]['evidence_quotes'][0]['quote']='Invented source quotation.'
  with patch('career_ai.structured',side_effect=[bad,fact(),make_map(1,1)])as model,patch('career_ai.moderate'):
   self.assertEqual(pipeline.generate([SOURCE],'')['map']['status'],'ready')
  repair=model.call_args_list[1].args[0];self.assertEqual(repair['previous_draft'],bad);self.assertIn('/facts/0/evidence_quotes',repair['validation_feedback']['issue'])
