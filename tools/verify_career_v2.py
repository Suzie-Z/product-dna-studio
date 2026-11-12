"""Opt-in V2 real-provider verification. Uses server-only test authentication, not an API key."""
import argparse,json,sys,time,uuid,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from career_ai import validate_map
from tools.benchmark_pm_models import PROFILES,post,estimated_cost

def run(origin,token,out):
 out.mkdir(parents=True,exist_ok=True);before=json.load(urllib.request.urlopen(origin+'/api/stats',timeout=60));diag=post(origin,'/api/internal/models',{},token);(out/'model-access.json').write_text(json.dumps(diag,indent=2));available={m['id']for m in diag['models']if m['listed_for_active_project']}
 assert {'gpt-6-astra','gpt-6.1-sol'}<=available,diag
 jobs=[(name,'gpt-6-astra')for name in PROFILES]+[(name,'gpt-6.1-sol')for name in ['ai_ml_pm','consulting_to_pm']]
 def one(name,model):
  target=out/(name+'-'+model+'.json')
  if target.exists():return json.loads(target.read_text())
  source={'source_id':'src_v2_benchmark','source_type':'typed_story','source_label':'Synthetic V2 PM benchmark','content':PROFILES[name]};started=time.monotonic();result=post(origin,'/api/career-dna/generate',{'sources':[source],'request_id':'req_'+uuid.uuid4().hex,'benchmark_model':model},token)
  assert result['map']['status']=='ready',(name,model,result);validate_map(result['map'],[source]);assert result.get('counted')is False
  stages=result.get('usage_metrics',[]);assert {'career','summary'}<={s['stage']for s in stages};assert all(s['provider_model']==model for s in stages)
  labels=[j['label']for j in result['map']['journey']]
  if name=='engineering_to_pm':assert'Software Engineer'in labels,labels
  if name=='consulting_to_pm':assert'Business Consultant'in labels,labels
  record={'profile':name,'model':model,'seconds':round(time.monotonic()-started,2),'estimated_usd':estimated_cost(stages),'roles':labels,'response':result,'source':source};target.write_text(json.dumps(record,indent=2));return record
 records=[]
 with ThreadPoolExecutor(max_workers=2)as pool:
  tasks=[pool.submit(one,*job)for job in jobs]
  for task in as_completed(tasks):
   record=task.result();records.append(record);print(json.dumps({k:v for k,v in record.items()if k not in ['source','response']}),flush=True)
 after=json.load(urllib.request.urlopen(origin+'/api/stats',timeout=60));report={'before':before,'after':after,'tests_marked_internal':True,'results':records};(out/'benchmark-report.json').write_text(json.dumps(report,indent=2));assert after['total_generations']==before['total_generations'],'Counter changed during synthetic benchmark; inspect concurrent genuine traffic before attributing it.';print('Completed V2 two-stage model comparison. All synthetic requests explicitly excluded from counts.',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--origin',default='https://product-dna-studio-ai.onrender.com');p.add_argument('--token-file',required=True);p.add_argument('--output',required=True);args=p.parse_args();run(args.origin,Path(args.token_file).read_text().strip(),Path(args.output))
