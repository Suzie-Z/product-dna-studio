"""Consolidated one-step contracts and actual browser QA, with no paid test calls."""
import copy,json,unittest
from unittest.mock import patch
from pathlib import Path
import career_ai as a,semantic_refinement as edit
from tests import test_original_refinement as original
from tests.fixtures import SOURCE,make_map
class OneStep(unittest.TestCase):
 def data(self):
  d=make_map(1,1);d['journey'][0]['highlights'][0]['label']='Automated enforcement';d['strengths'][0]['methods'][0]['label']='Automated enforcement';return d
 def response(self,paths,value='Design safety systems'):
  return {'status':'ready','changes':[{'path':p,'value':value}for p in sorted(paths)],'clarification_question':None,'change_summary':'Updated the requested wording.'}
 def test_duplicate_dash_replacement_is_all_matches_and_atomic(self):
  d=self.data();message='Automated enforcement - design safety system';paths=edit.exact_replacement(d,message);self.assertEqual(len(paths),2)
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=self.response(paths)):
   out=a.process_refine({'sources':[SOURCE],'previous':d,'message':message,'context_consent':True})
  self.assertEqual(set(out['changed_fields']),paths);self.assertEqual(out['map']['journey'][0]['highlights'][0]['label'],'Design safety systems');self.assertEqual(out['map']['strengths'][0]['methods'][0]['label'],'Design safety systems');self.assertEqual(d,self.data());self.assertEqual(out['presentation_patch'],{})
 def test_explicit_role_scope_only_one_occurrence(self):
  d=self.data();paths=edit.exact_replacement(d,'Change "Automated enforcement" under Growth PM to "Design safety systems"');self.assertEqual(paths,{'/journey/j1/highlights/0/label'})
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=self.response(paths)):
   out=a.process_refine({'sources':[SOURCE],'previous':d,'message':'Change "Automated enforcement" under Growth PM to "Design safety systems"','context_consent':True})
  self.assertEqual(out['map']['strengths'],d['strengths'])
 def test_missing_target_is_single_error_never_question_response(self):
  d=self.data();response={'status':'needs_more_info','changes':[],'clarification_question':'Which one?','change_summary':'Clarify.'}
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=response):
   with self.assertRaises(a.AppError)as failure:a.process_refine({'sources':[SOURCE],'previous':d,'message':'Change the unknown sentence','context_consent':True})
  self.assertEqual(failure.exception.status,422);self.assertEqual(failure.exception.code,'invalid_edit_target');self.assertEqual(d,self.data())
 def test_partial_duplicate_patch_cannot_commit(self):
  d=self.data();paths={'/journey/j1/highlights/0/label'}
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=self.response(paths)):
   with self.assertRaises(a.AppError):a.process_refine({'sources':[SOURCE],'previous':d,'message':'Automated enforcement - design safety system','context_consent':True})
  self.assertEqual(d,self.data())
 def test_five_evidenced_journey_stages_are_supported(self):self.assertEqual(len(a.validate_map(make_map(5,4),[SOURCE])['journey']),5)
class ApprovedBrowser(unittest.TestCase):
 setUpClass=classmethod(original.OriginalBrowser.setUpClass.__func__)
 tearDownClass=classmethod(original.OriginalBrowser.tearDownClass.__func__)
 setUp=original.OriginalBrowser.setUp
 tearDown=original.OriginalBrowser.tearDown
 page=original.OriginalBrowser.page
 upload=original.OriginalBrowser.upload
 ready=original.OriginalBrowser.ready
 def test_homepage_privacy_fonts_and_no_duplicate_cta(self):
  page,context=self.page();self.assertEqual(page.locator('#begin').count(),0);self.assertTrue(page.locator('#upload').is_visible());self.assertTrue(page.locator('#generate').is_visible());self.assertFalse(page.locator('#privacy').evaluate('(e)=>e.open'))
  self.assertEqual(page.locator('#privacy > p').count(),1);self.assertEqual(page.locator('#clarification').count(),0)
  page.locator('#privacy > summary').click();page.wait_for_function('document.querySelector("#privacy > summary").getAttribute("aria-expanded")==="true"');self.assertEqual(page.locator('#privacy > summary').get_attribute('aria-expanded'),'true');self.assertEqual(page.locator('#privacy-technical').count(),0)
  self.assertTrue(page.evaluate('document.fonts.check("600 32px PMDNAHeading")&&document.fonts.check("600 16px PMDNABody")&&!document.documentElement.classList.contains("fonts-loading")'));context.close()
 def test_approved_geometry_two_to_five_stages_one_to_four_cards(self):
  page,context=self.page()
  for mobile in [False,True]:
   for n in [2,3,4,5]:
    for k in [1,2,3,4]:
     m=page.evaluate('([d,m])=>buildDNAScene(d,m,nextPMVariant(d)).metrics',[make_map(n,k),mobile]);self.assertTrue(m['ok'],m['issues']);self.assertEqual(m['header']['title_center_x'],m['width']/2);self.assertEqual(len(set(m['platforms'].values())),1);self.assertEqual(len(m['pathAnchors']),n);self.assertGreaterEqual(m['summary']['y']-m['summary']['cardBottom'],30)
     if not mobile:self.assertEqual((m['width'],m['height']),(1600,1200))
     for anchor in m['pathAnchors']:self.assertGreaterEqual(anchor['end']['y'],m['hub']['y']);self.assertLessEqual(abs(anchor['end']['x']-m['hub']['x']),m['hub']['width']/2)
  context.close()
 def test_cold_reload_has_no_visible_fallback_and_modal_no_question(self):
  page,context=self.page();page.add_init_script('window.fontFrames=[];requestAnimationFrame(function sample(){fontFrames.push({visible:getComputedStyle(document.body).visibility!=="hidden",ready:document.fonts.check("600 32px PMDNAHeading")&&document.fonts.check("600 16px PMDNABody")});if(fontFrames.length<15)requestAnimationFrame(sample)})');page.reload();page.evaluate('pmFontsReady');page.wait_for_function('fontFrames.length>=10');self.assertFalse(page.evaluate('fontFrames.some(f=>f.visible&&!f.ready)'));self.assertTrue(page.locator('#upload').is_visible());context.close()

 def test_one_step_duplicate_update_reopen_and_missing_target_error(self):
  page,context=self.ready();page.evaluate("result.journey[0].highlights[0].label='User research';activeVersion.map=result")
  current=page.evaluate('structuredClone(result)');paths=edit.exact_replacement(current,'User research - Customer discovery');self.assertEqual(len(paths),2)
  response={'status':'ready','changes':[{'path':p,'value':'Customer discovery'}for p in paths],'clarification_question':None,'change_summary':'Updated both matching phrases.'}
  page.locator('#edit-map').click();page.locator('#story').fill('User research - Customer discovery')
  with patch('career_ai.moderate'),patch('career_ai.structured',return_value=response):page.locator('#generate').click();page.wait_for_function('activeVersion.number===2&&!busy',timeout=30000)
  self.assertFalse(page.locator('#refine-dialog').is_visible());self.assertEqual(page.evaluate('result.journey[0].highlights[0].label'),'Customer discovery');self.assertEqual(page.evaluate('result.strengths[0].methods[0].label'),'Customer discovery');page.locator('#edit-map').click();self.assertEqual(page.locator('#story').input_value(),'')
  page.locator('#story').fill('Nonexistent copied sentence - New wording');before=page.evaluate('structuredClone(result)');page.locator('#generate').click();page.wait_for_function('!busy&&document.getElementById("refine-status").textContent.includes("identify")');self.assertEqual(page.evaluate('result'),before);self.assertEqual(page.locator('#story').input_value(),'Nonexistent copied sentence - New wording');self.assertEqual(page.locator('#clarification').count(),0);self.assertTrue(page.locator('#refine-dialog').is_visible());context.close()
