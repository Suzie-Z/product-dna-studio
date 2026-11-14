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
