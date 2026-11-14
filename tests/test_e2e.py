"""Browser workflow through the real HTTP boundary; only OpenAI transport is mocked."""
import copy,json,os,threading,time,unittest,shutil,urllib.request
from pathlib import Path
from unittest.mock import patch
from playwright.sync_api import sync_playwright
import ai_server,career_ai
from tests.fixtures import make_map
ROOT=Path(__file__).resolve().parents[1]
ART=Path(os.environ.get('TEST_ARTIFACT_DIR',str(ROOT/'work/test-artifacts')))

def model_transport(path,payload,timeout=90):
 if path=='moderations':return {'results':[{'flagged':'TEST_UNSAFE' in payload['input']}]}
 data=json.loads(payload['input'][-1]['content'])
 if 'export_review'in data:return {'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps({'english_only':True})}]}]}
 src=data['sources'][0];quote=career_ai.generation_schema([src])['properties']['journey']['items']['properties']['evidence_quotes']['items']['anyOf'][0]['properties']['quote']['enum'][0]
 if 'previous'in data:
  previous=copy.deepcopy(data['previous']);request=data['refinement_request'].lower()
  if 'certified surgeon'in request:
   response={'map':career_ai.clarification('What qualification or clinical experience supports that credential?'),'changed_fields':[],'change_summary':'That credential needs supporting evidence.'}
  else:
   previous['strengths'][0]['label']='Applied Discovery'
   # Deliberately unrelated model drift: the server must NOT copy this field.
   previous['superpower']='An unrelated change that should never be accepted'
   response={'status':'ready','changes':[{'path':'/strengths/'+previous['strengths'][0]['id']+'/label','value':'Applied Discovery'}],'clarification_question':None,'change_summary':'Shortened the first strength while keeping the rest unchanged.'}
 elif 'career_facts' not in data:
  response={'status':'ready','facts':[{'id':'f1','claim':'Owned product decisions and prioritisation','role_type':'Growth PM','ownership':'owned','evidence_quotes':[{'source_id':src['source_id'],'quote':quote}]}],'clarification_question':None}
 else:
  d=make_map(3,3)
  for group in ['journey','strengths']:
   for item in d[group]:
    item.update(evidence_refs=[src['source_id']],evidence_quotes=[{'source_id':src['source_id'],'quote':quote}])
    for method in item.get('methods',[])+item.get('highlights',[]):method['evidence_quote']={'source_id':src['source_id'],'quote':quote}
  from tests.fixtures import REFLECTIONS
  response={**d,**copy.deepcopy(REFLECTIONS)}
 return {'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(response)}]}]}

class CompleteFlow(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  ART.mkdir(parents=True,exist_ok=True)
  cls.env=patch.dict(os.environ,{'OPENAI_API_KEY':'test-key-not-real','DAILY_GENERATION_LIMIT':'100','TRIAL_START_DATE':'','PM_INTERNAL_TEST_TOKEN':'test-internal-only','PUBLIC_COUNTER_ENV':'production'});cls.env.start()
  cls.provider=patch('career_ai.provider',side_effect=model_transport);cls.provider.start()
  cls.server=ai_server.ThreadingHTTPServer(('127.0.0.1',0),ai_server.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url='http://127.0.0.1:'+str(cls.server.server_port)
  cls.p=sync_playwright().start();browser_path=os.environ.get('CHROMIUM_PATH')or shutil.which('chromium');cls.browser=cls.p.chromium.launch(**({'executable_path':browser_path}if browser_path else {}),headless=True,args=['--no-sandbox'])
 @classmethod
 def tearDownClass(cls):
  cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close();cls.provider.stop();cls.env.stop()
 def setUp(self):
  # Each browser case is independent; the shared localhost transport has one IP.
  ai_server.RECENT.clear()
 def page(self,width=1440):
  context=self.browser.new_context(extra_http_headers={'X-PM-Internal-Test':'test-internal-only'},viewport={'width':width,'height':1000});context.route('https://fonts.googleapis.com/**',lambda r:r.abort());context.route('https://fonts.gstatic.com/**',lambda r:r.abort());page=context.new_page();page.goto(self.url);page.evaluate('pmFontsReady');page.locator('#begin').click();return page,context


 def test_full_highlights_header_safe_art_and_layout_variants(self):
  from tests.test_v2 import LABELS
  page,context=self.page()
  for j in range(1,5):
   for k in range(1,5):
    d=make_map(j,k)
    for item in d['journey']:item['highlights']=[{'label':label,'evidence_quote':item['evidence_quotes'][0]}for label in LABELS]
    for mobile in [False,True]:
     for side in ['left','right']:
      m=page.evaluate('([d,m,s])=>buildDNAScene(d,m,{character_side:s}).metrics',[d,mobile,side]);self.assertTrue(m['ok']or bool(m['overflowFields']),(j,k,mobile,side,m['issues']));self.assertEqual(m['collisions'],[]);self.assertEqual(m['header']['title_center_x'],m['width']/2);self.assertGreater(m['header']['logo_gap'],0)
  context.close()

 def test_long_copy_is_shortened_before_display_without_regeneration(self):
  page,context=self.page();posts=[]
  def overlong(route):
   r=route.fetch();body=r.json();body['map']['strengths'][0]['label']='W'*35;route.fulfill(response=r,json=body)
  context.route('**/api/career-dna/generate',overlong);page.on('request',lambda r:posts.append(r.post_data_json)if r.url.endswith('/refine')else None)
  page.evaluate("()=>{cvText='I am a platform product manager. I owned shared product requirements and customer discovery.';cvName='fixture.docx';cvId='src_primary';cvDirty=true;syncCV();updateButtons()}");page.locator('#generate').click();page.wait_for_function('activeVersion?.number===1&&!busy')
  self.assertEqual(page.evaluate('result.strengths[0].label'),'Applied Discovery');self.assertTrue(page.evaluate('exportCanvas.renderMetrics.ok'));self.assertEqual(len(posts),1);self.assertEqual(posts[0]['fit_fields'],['/strengths/k1/label']);self.assertNotIn('Regenerate for shorter wording',page.locator('#map-visual').inner_text());self.assertEqual(page.locator('#story').get_attribute('placeholder'),"What would you like to change?");context.close()

 def test_local_rounded_fonts_match_measurement_and_export(self):
  page,context=self.page()
  details=page.evaluate("""()=>{const ctx=document.createElement('canvas').getContext('2d');ctx.fontKerning='none';return Object.entries(PM_DNA_FONTS).map(([kind,f])=>{const sample='Scalable Platform Design',s=30;ctx.font=`600 ${s}px ${f.family}`;const measured=ctx.measureText(sample).width,outline=[...sample].reduce((n,ch)=>n+f.glyphs[ch].advance,0)*s/f.units;ctx.font='600 30px Arial';return {loaded:document.fonts.check(`600 30px ${f.family}`),difference:Math.abs(measured-outline),distinct:Math.abs(measured-ctx.measureText(sample).width)>1}})}""")
  self.assertTrue(all(x['loaded']and x['distinct']and x['difference']<.5 for x in details),details)
  page.evaluate('(d)=>renderDNAPoster(exportCanvas,d,nextPMVariant())',make_map(4,4))
  self.assertTrue(page.evaluate('exportCanvas.renderMetrics.outlinedText&&exportCanvas.renderMetrics.exportTextCount>20&&exportCanvas.renderMetrics.fontsLoaded'))
  context.close()
 def test_all_layouts_and_explicit_overflow_fallback(self):
  page,context=self.page()
  for j in range(1,5):
   for k in range(1,5):
    for mobile in [False,True]:
     metrics=page.evaluate('([d,m])=>buildDNAScene(d,m).metrics',[make_map(j,k),mobile]);self.assertTrue(metrics['ok'],(j,k,mobile,metrics['issues'],metrics.get('collisions')));self.assertEqual(metrics['collisions'],[])
     for box in metrics['boxes']:self.assertLessEqual(box['paintedHeight'],box['height'])
  for k in range(1,5):
   page.evaluate('(d)=>renderDNAMap(document.querySelector("#map-visual"),d)',make_map(4,k));page.locator('#step-two').evaluate('(e)=>e.classList.remove("hidden")');page.locator('#result-panel').evaluate('(e)=>e.classList.remove("hidden")');page.locator('#map-visual').screenshot(path=str(ART/f'career-{k}-strengths.png'))
  d=make_map(1,1);d['strengths'][0]['description']='Unreasonablylongtext'*100
  metrics=page.evaluate('(d)=>buildDNAScene(d).metrics',d);self.assertFalse(metrics['ok'])
  # User/model text cannot introduce SVG elements or handlers.
  d=make_map(1,1);d['career_signature']='<script>alert(1)</script>'
  page.evaluate('(d)=>renderDNAMap(document.querySelector("#map-visual"),d)',d)
  self.assertEqual(page.locator('#map-visual script').count(),0)
  with self.assertRaises(Exception):page.evaluate('(d)=>buildDNAScene(d)',make_map(5,1))
  context.close()
 def test_chronological_mobile_dates_have_readable_reserved_height(self):
  page,context=self.page()
  for j in range(1,5):
   for k in range(1,5):
    d=make_map(j,k);d['journey_type']='chronological'
    for item in d['journey']:item['date_label']='2020–2022'
    d['superpower']='Turning funnel evidence and platform contracts into reliable AI features'
    for mobile in [False,True]:
     metrics=page.evaluate('([d,m])=>buildDNAScene(d,m).metrics',[d,mobile]);self.assertTrue(metrics['ok'],metrics['issues']);self.assertEqual(metrics['collisions'],[])
  context.close()
 def test_compact_cards_fit_zero_to_three_methods_across_layouts(self):
  page,context=self.page()
  for j in range(1,5):
   for k in range(1,5):
    for count in range(4):
     d=make_map(j,k);d['journey_type']='chronological'
     for item in d['journey']:item['date_label']='2020–2022'
     for item in d['strengths']:item['methods']=[{'label':label,'evidence_quote':item['evidence_quotes'][0]}for label in ['Golden-set evaluation','Reliability trade-offs','Controlled experiments'][:count]]
     for mobile in [False,True]:
      metrics=page.evaluate('([d,m])=>buildDNAScene(d,m).metrics',[d,mobile]);self.assertTrue(metrics['ok'],(j,k,count,mobile,metrics['issues']));self.assertEqual(metrics['collisions'],[])
      if not mobile:self.assertLessEqual(metrics['height'],1300)
  context.close()
 def test_real_benchmark_highlight_wraps_without_shrinking_or_overlap(self):
  page,context=self.page()
  for j in range(1,5):
   for k in range(1,5):
    d=make_map(j,k);d['journey'][0]['highlights'][0]['label']='Discovery and workflow mapping'
    for dated in [False,True]:
     if dated:
      d['journey_type']='chronological'
      for item in d['journey']:item['date_label']='2020–2022'
     metrics=page.evaluate('(d)=>buildDNAScene(d,true).metrics',d);self.assertTrue(metrics['ok'],metrics['issues']);self.assertEqual(metrics['collisions'],[]);self.assertTrue(all(b['size']>=27 for b in metrics['boxes']if b['text']=='Discovery and workflow mapping'))
  context.close()
 def test_actual_painted_foreground_bounds_do_not_overlap(self):
  page,context=self.page();d=make_map(4,4);d['journey_type']='chronological'
  for item in d['journey']:item['date_label']='2020–2022'
  for item in d['strengths']:item['methods']=[{'label':label,'evidence_quote':item['evidence_quotes'][0]}for label in ['Golden-set evaluation','Reliability trade-offs','Controlled experiments']]
  page.evaluate('(d)=>{renderDNAMap(document.querySelector("#map-visual"),d);document.querySelector("#step-two").classList.remove("hidden");document.querySelector("#result-panel").classList.remove("hidden")}',d)
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000});page.wait_for_function('(mode)=>document.querySelector("#map-visual").dataset.layout===mode',arg='mobile'if width==390 else'desktop')
   bad=page.evaluate("""()=>{const rect=e=>{if(e.tagName.toLowerCase()!=='svg')return e.getBoundingClientRect();/* SVG getBBox includes the full atlas behind the clipped viewport. Use its actual viewport, transformed to screen coordinates. */const m=e.parentElement.getScreenCTM(),x=e.x.baseVal.value,y=e.y.baseVal.value,w=parseFloat(getComputedStyle(e).width),h=parseFloat(getComputedStyle(e).height),p=new DOMPoint(x,y).matrixTransform(m),q=new DOMPoint(x+w,y+h).matrixTransform(m);return {left:p.x,top:p.y,right:q.x,bottom:q.y}};const a=[...document.querySelectorAll('#map-visual [data-foreground]')].map(e=>({id:e.dataset.foreground,r:rect(e)}));const out=[];for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){let p=a[i],q=a[j];if(Math.min(p.r.right,q.r.right)-Math.max(p.r.left,q.r.left)>1&&Math.min(p.r.bottom,q.r.bottom)-Math.max(p.r.top,q.r.top)>1)out.push([p.id,q.id])}return out}""")
   self.assertEqual(bad,[],(width,bad))
  context.close()
 def test_variant_rotation_and_stable_export(self):
  page,context=self.page()
  values=page.evaluate('Array.from({length:24},()=>nextPMVariant())')
  self.assertEqual(len({v['avatar_id']for v in values}),24)
  for start in range(0,24,6):self.assertEqual(len({v['theme_id']for v in values[start:start+6]}),6)
  for variant in values:
   data=page.evaluate('([d,v])=>buildDNAScene(d,false,v).metrics',[make_map(4,4),variant]);self.assertTrue(data['ok'],data['issues']);self.assertEqual(data['avatar_id'],variant['avatar_id']);self.assertEqual(data['theme_id'],variant['theme_id'])
  context.close()


if __name__=='__main__':unittest.main()
