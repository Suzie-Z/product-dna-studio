"""Opt-in billable PM-only smoke flow. Credentials remain in process memory."""
import copy,getpass,json,os,sys,threading,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import career_ai,ai_server
from playwright.sync_api import sync_playwright
ART=ROOT/'work/live-smoke';ART.mkdir(parents=True,exist_ok=True)
if not os.environ.get('OPENAI_API_KEY'):os.environ['OPENAI_API_KEY']=getpass.getpass('OpenAI API credential (hidden): ')
os.environ['DAILY_GENERATION_LIMIT']='10';os.environ['TRIAL_START_DATE']=''
provider=career_ai.provider;usage=[]
def observed(path,payload,timeout=90):
 out=provider(path,payload,timeout)
 if path=='responses':usage.append(out.get('usage',{}))
 return out
career_ai.provider=observed
server=ai_server.ThreadingHTTPServer(('127.0.0.1',0),ai_server.Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
STORY='我是平台产品经理，负责共享产品能力的路线图、需求优先级和产品交付。我与工程团队一起评估可靠性和规模化取舍，通过用户研究理解产品团队的采用障碍，制定阶段性的产品发布计划。我没有管理过团队，不要添加人员管理经历。'
try:
 nonpm=career_ai.process_generate({'sources':[{'source_id':'src_nonpm','source_type':'typed_story','source_label':'Story','content':'I am a chef planning menus. I want to become a product manager.'}]})
 assert nonpm['map']['status']=='needs_more_info'and not usage
 with sync_playwright()as p:
  path=shutil.which('chromium');browser=p.chromium.launch(**({'executable_path':path}if path else {}),headless=True,args=['--no-sandbox'],env={k:v for k,v in os.environ.items()if k!='OPENAI_API_KEY'})
  page=browser.new_page(viewport={'width':1440,'height':1000});page.goto('http://127.0.0.1:'+str(server.server_port));page.locator('#begin').click();page.locator('#story').fill(STORY)
  def generate():
   page.locator('#generate').click();page.wait_for_function("!document.querySelector('#result-panel').classList.contains('hidden')&&exportCanvas.renderMetrics?.ok",timeout=240000)
   d=page.evaluate('structuredClone(result)');assert d['output_language']=='en';assert all(j['label']in career_ai.PM_ROLE_LABELS for j in d['journey']);assert page.locator('#result-panel canvas').count()==0;assert page.locator('#map-visual > svg').count()==1;return d
  first=generate();v1=page.evaluate('structuredClone(renderVariant)')
  with page.expect_download(timeout=60000)as e:page.locator('#save').click()
  e.value.save_as(str(ART/'real-pm-career-dna.png'));assert e.value.suggested_filename=='my-pm-career-dna.png';assert page.evaluate('renderVariant')==v1
  page.locator('#story').fill(STORY+' 请重点体现系统设计和用户洞察。');second=generate();v2=page.evaluate('structuredClone(renderVariant)');assert v1['avatar_id']!=v2['avatar_id']and v1['theme_id']!=v2['theme_id']
  page.set_viewport_size({'width':390,'height':844});page.wait_for_function("document.querySelector('#map-visual').dataset.layout==='mobile'");assert page.locator('#map-visual').evaluate('(e)=>e.renderMetrics.collisions.length===0');assert page.evaluate('renderVariant')==v2
  page.screenshot(path=str(ART/'mobile.png'),full_page=True);browser.close()
 report={'passed':True,'checks':['PM-only scope','Chinese PM input to English output','one visible map','single branded PNG','new variant for regeneration','stable mobile variant','no overlaps'],'response_calls':len(usage),'input_tokens':sum(v.get('input_tokens',0)for v in usage),'output_tokens':sum(v.get('output_tokens',0)for v in usage)}
 (ART/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
finally:server.shutdown();server.server_close();os.environ.pop('OPENAI_API_KEY',None)
