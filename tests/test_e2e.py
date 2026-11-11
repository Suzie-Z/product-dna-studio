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
 src=data['sources'][0];quote=src['content'][:min(120,len(src['content']))]
 if 'previous'in data:
  previous=copy.deepcopy(data['previous']);request=data['refinement_request'].lower()
  if 'certified surgeon'in request:
   response={'map':career_ai.clarification('What qualification or clinical experience supports that credential?'),'changed_fields':[],'change_summary':'That credential needs supporting evidence.'}
  else:
   previous['strengths'][0]['label']='Applied Discovery'
   # Deliberately unrelated model drift: the server must NOT copy this field.
   previous['superpower']='An unrelated change that should never be accepted'
   response={'map':previous,'changed_fields':['/strengths/'+previous['strengths'][0]['id']+'/label'],'change_summary':'Shortened the first strength while keeping the rest unchanged.'}
 else:
  d=make_map(3,3)
  for group in ['journey','strengths']:
   for item in d[group]:
    item.update(evidence_refs=[src['source_id']],evidence_quotes=[{'source_id':src['source_id'],'quote':quote}])
    for method in item.get('methods',[])+item.get('highlights',[]):method['evidence_quote']={'source_id':src['source_id'],'quote':quote}
  response=d
 return {'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(response)}]}]}

class CompleteFlow(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  ART.mkdir(parents=True,exist_ok=True)
  cls.env=patch.dict(os.environ,{'OPENAI_API_KEY':'test-key-not-real','DAILY_GENERATION_LIMIT':'100','TRIAL_START_DATE':''});cls.env.start()
  cls.provider=patch('career_ai.provider',side_effect=model_transport);cls.provider.start()
  cls.server=ai_server.ThreadingHTTPServer(('127.0.0.1',0),ai_server.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url='http://127.0.0.1:'+str(cls.server.server_port)
  cls.p=sync_playwright().start();browser_path=os.environ.get('CHROMIUM_PATH')or shutil.which('chromium');cls.browser=cls.p.chromium.launch(**({'executable_path':browser_path}if browser_path else {}),headless=True,args=['--no-sandbox'])
 @classmethod
 def tearDownClass(cls):
  cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close();cls.provider.stop();cls.env.stop()
 def page(self,width=1440):
  context=self.browser.new_context(viewport={'width':width,'height':1000});context.route('https://fonts.googleapis.com/**',lambda r:r.abort());context.route('https://fonts.gstatic.com/**',lambda r:r.abort());page=context.new_page();page.goto(self.url);page.evaluate('pmFontsReady');page.locator('#begin').click();return page,context
 def test_complete_flow(self):
  page,context=self.page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  self.assertTrue(page.locator('#generate').is_disabled());self.assertEqual(page.evaluate('document.activeElement.id'),'step-one')
  self.assertEqual(page.locator('#story').get_attribute('placeholder'),None)
  self.assertEqual(page.locator('#step-one h2').inner_text(),'Share Your PM Journey')
  for selector in ['#format','#refinement','#direct-editor','#step-three','#map-outline','#copy-caption']:
   self.assertEqual(page.locator(selector).count(),0)
  self.assertTrue(page.locator('.brand-symbol').evaluate('(e)=>e.complete&&e.naturalWidth>0'))
  initial=json.load(urllib.request.urlopen(self.url+'/api/stats'))['total_generations']
  page.locator('#story').fill('I work in tech.');page.locator('#generate').click();page.locator('#clarification').wait_for(state='visible')
  self.assertFalse(page.locator('#result-panel').is_visible());self.assertEqual(json.load(urllib.request.urlopen(self.url+'/api/stats'))['total_generations'],initial)
  page.locator('#clarification-answer').fill('I am a growth product manager. I owned onboarding requirements, researched customer needs and prioritised experiments with the product team.');page.locator('#answer').click()
  page.wait_for_function("exportCanvas.renderMetrics?.ok")
  self.assertEqual(page.locator('#generation-number').inner_text(),'Generation #'+str(initial+1))
  self.assertEqual(page.locator('#map-visual > svg text').first.text_content(),'My PM Career DNA')
  self.assertIn('My PM Journey',page.locator('#map-visual').text_content());self.assertIn('Shape My PM DNA',page.locator('#map-visual').text_content())
  self.assertEqual(page.locator('#result-panel button').count(),1)
  self.assertEqual(page.locator('#map-visual > svg').count(),1);self.assertEqual(page.locator('#result-panel canvas').count(),0)
  self.assertEqual(page.locator('[data-art=human-chibi]').count(),1)
  self.assertEqual(page.locator('[data-component=CareerJourneyIsland]').count(),3)
  page.locator('#full-journey summary').first.click();self.assertTrue(page.locator('#journey-evidence').is_visible());self.assertIn('The source',page.locator('#journey-evidence').inner_text());page.locator('#full-journey summary').first.click()
  self.assertNotIn('src_',page.locator('#map-visual').text_content());self.assertNotIn('First draft',page.locator('body').inner_text())
  page.screenshot(path=str(ART/'career-desktop.png'),full_page=True)
  with page.expect_download()as download:page.locator('#save').click()
  file=ART/'career-export.png';download.value.save_as(str(file));self.assertEqual(download.value.suggested_filename,'my-pm-career-dna.png')
  from PIL import Image
  with Image.open(file)as image:self.assertEqual(image.size,(3200,2100))
  self.assertGreater(file.stat().st_size,30000)
  self.assertEqual(json.load(urllib.request.urlopen(self.url+'/api/stats'))['total_generations'],initial+1)
  # Change requirements in the original input and regenerate through the same flow.
  page.locator('#story').fill('I am a platform product manager. I owned the product roadmap for reusable capabilities and prioritised adoption requirements for product teams.')
  self.assertFalse(page.locator('#result-panel').is_visible());page.locator('#generate').click()
  page.wait_for_function("document.querySelector('#result-panel').classList.contains('hidden')===false&&document.querySelector('#generation-number').textContent==='Generation #"+str(initial+2)+"'")
  self.assertEqual(page.locator('#generation-number').inner_text(),'Generation #'+str(initial+2))
  variant=page.evaluate('structuredClone(renderVariant)');page.set_viewport_size({'width':390,'height':844});self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  page.wait_for_function("document.querySelector('#map-visual').dataset.layout==='mobile'");self.assertEqual(page.evaluate('renderVariant'),variant);self.assertEqual(page.locator('#map-visual > svg').get_attribute('data-avatar'),variant['avatar_id']);self.assertEqual(page.locator('#map-visual > svg').count(),1);self.assertEqual(page.locator('#result-panel canvas').count(),0);page.screenshot(path=str(ART/'career-mobile.png'),full_page=True);page.locator('#map-visual').screenshot(path=str(ART/'career-mobile-map.png'))
  self.assertEqual(page.evaluate('Object.keys(localStorage).length'),0);self.assertFalse(errors,errors);context.close()
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
      if not mobile:self.assertLessEqual(metrics['height'],1100)
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
 def test_upload_clear_voice_and_fallback(self):
  page,context=self.page();page.locator('#story').fill('My typed notes will stay when the CV is removed.')
  page.locator('#file').set_input_files({'name':'resume.txt','mimeType':'text/plain','buffer':b'I am a platform product manager. I owned the product roadmap for reusable capabilities.'});page.wait_for_function("document.querySelector('#cv-status').textContent.includes('Ready')")
  self.assertIn('reusable capabilities',page.locator('#cv-text').input_value());page.locator('#cv-text').fill('I built reusable APIs and corrected this extracted text.')
  page.locator('#upload').click();self.assertIn('Only one CV',page.locator('#input-status').inner_text())
  page.once('dialog',lambda d:d.accept());page.locator('#clear-cv').click();self.assertIn('typed notes',page.locator('#story').input_value());self.assertFalse(page.locator('#cv-panel').is_visible())
  page.locator('#file').set_input_files({'name':'fake.pdf','mimeType':'application/pdf','buffer':b'not a pdf file'});page.wait_for_function("document.querySelector('#cv-panel').classList.contains('failed')");self.assertNotIn('Ready',page.locator('#cv-status').inner_text())
  page.evaluate('window.SpeechRecognition=undefined;window.webkitSpeechRecognition=undefined');page.locator('#voice').click();self.assertIn('unavailable',page.locator('#input-status').inner_text())
  page.add_script_tag(content="window.SpeechRecognition=class {start(){this.onstart();const a=[{transcript:'我研究用户需求并测试原型。'}];a.isFinal=true;this.onresult({resultIndex:0,results:[a]})} stop(){this.onend()}}")
  page.locator('#voice').click();self.assertIn('我研究',page.locator('#voice-text').input_value());self.assertTrue(page.locator('#voice-panel').is_visible());page.locator('#voice').click();context.close()
 def test_normal_pdf_docx_and_mixed_input(self):
  from reportlab.pdfgen import canvas
  from docx import Document
  pdf=ART/'resume.pdf';c=canvas.Canvas(str(pdf));c.drawString(72,760,'I am a platform product manager. I owned the product roadmap for reusable capabilities.');c.save()
  doc=Document();doc.add_paragraph('I am an operations PM. I prioritised product requirements for operational workflows.');doc.save(ART/'resume.docx')
  assets=ART/'parser-assets';assets.mkdir(exist_ok=True)
  links={'mammoth.browser.min.js':'https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.9.1/mammoth.browser.min.js','pdf.min.mjs':'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.min.mjs','pdf.worker.min.mjs':'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.worker.min.mjs'}
  for name,url in links.items():
   if not (assets/name).exists():(assets/name).write_bytes(urllib.request.urlopen(url,timeout=30).read())
  page,context=self.page()
  def parser_route(route):
   file=assets/route.request.url.rsplit('/',1)[-1]
   if file.is_file():route.fulfill(path=str(file),content_type='text/javascript',headers={'Access-Control-Allow-Origin':'*'})
   else:route.abort()
  context.route('https://cdnjs.cloudflare.com/**',parser_route)
  for name in ['resume.pdf','resume.docx']:
   page.locator('#file').set_input_files(str(ART/name));page.wait_for_function("document.querySelector('#cv-status').textContent.includes('Ready')",timeout=30000)
   self.assertGreater(len(page.locator('#cv-text').input_value()),30)
   page.once('dialog',lambda d:d.accept());page.locator('#clear-cv').click()
  page.locator('#file').set_input_files(str(ART/'resume.docx'));page.wait_for_function("document.querySelector('#cv-status').textContent.includes('Ready')")
  page.locator('#story').fill('I am a growth product manager. I owned scheduling-product onboarding and prioritised customer needs.')
  page.evaluate("document.querySelector('#voice-panel').classList.remove('hidden');document.querySelector('#voice-text').value='我协调交接流程并改进工作方式。';document.querySelector('#voice-text').dispatchEvent(new Event('input'))")
  kinds=page.evaluate('sources().map(s=>s.source_type)');self.assertEqual(set(kinds),{'cv','typed_story','voice_transcript'})
  page.locator('#generate').click();page.locator('#result-panel').wait_for(state='visible');self.assertEqual(page.evaluate('result.output_language'),'en');context.close()
if __name__=='__main__':unittest.main()
