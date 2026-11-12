import copy,json,unittest
from unittest.mock import patch
from tests import test_e2e as e2e
from tests.fixtures import make_map,SOURCE
class HandoffBrowser(unittest.TestCase):
 setUpClass=classmethod(e2e.CompleteFlow.setUpClass.__func__)
 tearDownClass=classmethod(e2e.CompleteFlow.tearDownClass.__func__)
 setUp=e2e.CompleteFlow.setUp
 page=e2e.CompleteFlow.page
 def ready(self,width=1440):
  page,context=self.page(width);d=make_map(3,3);v={'number':1,'parent_id':None,'map':d,'sources':[SOURCE],'variant':{'theme_id':'lilac_light','avatar_id':'pm_avatar_04','pathway_id':'glow','density':'compact'},'cv':{'name':'','text':'','id':'src_cv'},'intelligence':None}
  page.evaluate('async(v)=>{versions=[v];versionSerial=1;activeVersion=v;result=v.map;renderVariant=v.variant;document.getElementById("step-two").classList.remove("hidden");await renderResult();updateButtons()}',v);return page,context,d
 def test_conversational_visual_changes_history_undo_and_original_icons(self):
  page,context,d=self.ready();payloads=[]
  def model(payload,*args,**kwargs):
   payloads.append(payload);m=payload['refinement_request'].lower()
   if 'warmer'in m:changes=[{'path':'/visual/theme_id','value':'peach_coral'}]
   elif 'compass'in m:changes=[{'path':'/visual/icons/k3','value':'strategy'}]
   elif 'pathway'in m:changes=[{'path':'/visual/pathway_id','value':'constellation'},{'path':'/visual/platforms/j2','value':'crystal'}]
   elif 'original'in m:changes=[{'path':'/visual/reset_icons','value':True}]
   else:changes=[{'path':'/visual/softness','value':'soft'}]
   return {'status':'ready','changes':changes,'clarification_question':None,'change_summary':'Updated your chosen visual details.'}
  with patch('career_ai.structured',side_effect=model),patch('career_ai.moderate'):
   for number,message in enumerate(['Can we make this feel warmer while keeping my story?','Give the third card a compass icon.','Try a constellation pathway and a crystal second platform.','No, keep the icons; just soften the colors.','Please restore the original icons.'],2):
    page.locator('#story').fill(message);page.locator('#generate').click();page.wait_for_function('(n)=>activeVersion.number===n&&!busy',arg=number);self.assertEqual(page.evaluate('result'),d)
  self.assertEqual(page.locator('#refine-history .conversation-user').count(),3);self.assertEqual(page.evaluate('activeVersion.sources.length'),1);self.assertEqual(page.evaluate('renderVariant.icon_overrides'),{});self.assertEqual(page.evaluate('renderVariant.theme_id'),'peach_coral');self.assertEqual(page.evaluate('renderVariant.softness'),'soft');self.assertEqual(page.evaluate('renderVariant.pathway_id'),'constellation');self.assertEqual(page.locator('[data-platform="crystal"]').count(),1);self.assertEqual(payloads[-1]['edit_history'][-1]['instruction'],'No, keep the icons; just soften the colors.')
  page.locator('#undo').click();page.wait_for_function('activeVersion.number===5&&!busy');self.assertEqual(page.evaluate('renderVariant.icon_overrides.k3'),'strategy');page.locator('#version-select').select_option('1');page.wait_for_function('activeVersion.number===1&&!busy');self.assertEqual(page.evaluate('renderVariant.theme_id'),'lilac_light');context.close()
 def test_cancelled_edit_cannot_replace_current_version(self):
  page,context,d=self.ready();held=[];context.route('**/api/career-dna/refine',lambda route:held.append(route));page.locator('#story').fill('Please try warmer colors.');page.locator('#generate').click();page.wait_for_function('busy');page.locator('#cancel').click();page.wait_for_function('!busy');self.assertEqual(page.evaluate('versions.length'),1);self.assertEqual(page.evaluate('result'),d);self.assertIn('warmer',page.locator('#story').input_value());
  for route in held:
   try:route.abort()
   except Exception:pass
  context.close()
 def test_original_version_survives_bounded_history(self):
  page,context,d=self.ready();page.evaluate('()=>{const first=structuredClone(activeVersion);versions=Array.from({length:30},(_,i)=>({...structuredClone(first),number:i+1,parent_id:i||null}));activeVersion=versions[29];versionSerial=30;updateButtons()}');page.locator('#story').fill('Change only the background to blue');page.locator('#generate').click();page.wait_for_function('activeVersion.number===31&&!busy');self.assertEqual(page.evaluate('versions.length'),30);self.assertEqual(page.evaluate('versions[0].number'),1);page.locator('#version-select').select_option('1');page.wait_for_function('activeVersion.number===1&&!busy');self.assertEqual(page.evaluate('result'),d);context.close()
 def test_desktop_viewports_export_mobile_and_zoom(self):
  page,context,d=self.ready()
  for w,h in [(1440,900),(1366,768)]:
   page.set_viewport_size({'width':w,'height':h});page.wait_for_timeout(50);page.locator('#result-panel').evaluate('(e)=>e.scrollIntoView({block:"start",behavior:"instant"})');box=page.locator('#result-panel').bounding_box();self.assertLessEqual(box['y']+box['height'],h+2);m=page.locator('#map-visual').evaluate('(e)=>e.renderMetrics');self.assertTrue(m['ok'],m['issues']);self.assertEqual(m['width']/m['height'],16/9)
  page.evaluate('async()=>renderDNAPoster(exportCanvas,result,renderVariant)');self.assertEqual(page.evaluate('[exportCanvas.width,exportCanvas.height]'),[3200,1800]);self.assertTrue(page.evaluate('exportCanvas.renderMetrics.outlinedText'))
  page.set_viewport_size({'width':1092,'height':614});self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'));self.assertEqual(page.locator('#map-visual').evaluate('(e)=>e.renderMetrics.collisions'),[])
  page.set_viewport_size({'width':390,'height':844});page.wait_for_function('document.getElementById("map-visual").dataset.layout==="mobile"');self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'));self.assertTrue(page.locator('#map-visual').evaluate('(e)=>e.renderMetrics.ok'));context.close()
 def test_all_platforms_paths_and_missing_asset_fallback(self):
  page,context,d=self.ready();m=page.evaluate('([d,v])=>buildDNAScene(d,false,v).metrics',[d,{}]);self.assertEqual(len(set(m['platforms'].values())),3)
  for shape in ['garden','crystal','modular','steps','nebula','circuit']:
   for path in ['glow','stones','constellation','streams']:
    m=page.evaluate('([d,s,p])=>buildDNAScene(d,false,{platform_overrides:{j1:s},pathway_id:p}).metrics',[d,shape,path]);self.assertTrue(m['ok'],m['issues']);self.assertEqual(m['platforms']['j1'],shape)
  for mobile in [False,True]:
   m=page.evaluate('([d,m])=>buildDNAScene(d,m,{mascot_visible:false,density:"comfortable",decorations:"none"}).metrics',[d,mobile]);self.assertTrue(m['ok'],m['issues']);self.assertEqual(m['collisions'],[])
  page.evaluate('(d)=>{d.strengths[0].icon="missing-asset";renderDNAMap(document.getElementById("map-visual"),d,{platform_overrides:{j1:"missing-platform"}})}',d);self.assertGreater(page.locator('[data-icon="strategy"]').count(),0);self.assertGreater(page.locator('[data-platform="garden"]').count(),0);context.close()
