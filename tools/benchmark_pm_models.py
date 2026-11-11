"""Opt-in real API-project benchmark through authenticated app diagnostics.
No OpenAI secret leaves Render; synthetic calls are excluded from public counts.
"""
import argparse,json,sys,time,uuid,urllib.request,urllib.error
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from career_ai import validate_map
PROFILES={
 'traditional_pm':'''I am a Product Manager. I owned roadmap and release priorities for a customer scheduling product. Used customer interviews and funnel analysis to diagnose onboarding friction. Defined acceptance criteria and prioritised controlled experiments with design and engineering. Resolved usability versus delivery-scope trade-offs. I did not manage people and claim no quantified outcome.''',
 'engineering_to_pm':'''2016–2021: Software Engineer. Implemented API services and investigated reliability failures. Worked with product managers to clarify customer constraints. 2021–2026: Technical Product Manager. Owned the product roadmap and product requirements for integration capabilities. Prioritised reliability versus adoption trade-offs with engineers, who owned the implementation. Used customer interviews and product contracts to frame release scope. Do not relabel my engineering job as a PM position. I have never managed people.''',
 'ai_ml_pm':'''I am an AI Product Manager. Owned user-facing conversational and multimodal AI requirements and release decisions. Compared model capability boundaries and failure modes against real product use cases. Built golden-set evaluation cases and representative evaluation data with engineering and research. Used failure analysis and use-case comparison to judge model fit before rollout. Partnered with safety teams to review abuse cases and privacy requirements and define release safeguards. I have not managed people. 请提炼能力、判断和取舍，不要虚构成果。''',
 'platform_pm':'''I am a Platform Product Manager. Owned the roadmap for shared capabilities used by several product teams. Defined product contracts and stable interface requirements. Evaluated reliability and extensibility trade-offs in system design reviews with engineering. Prioritised adoption requirements and migration sequencing based on product-team feedback. Engineering partners owned architecture implementation. I claim no quantified improvements.''',
 'consulting_to_pm':'''2017–2021: Business Consultant. Conducted customer discovery, mapped operational workflows and analysed business-case assumptions for a merchant service. I recommended options but did not own a product roadmap in that job. 2021–2026: Commerce Product Manager. Owned checkout product requirements and roadmap priorities. Used merchant interviews, funnel analysis and controlled experiments to prioritise conversion friction against delivery constraints. Reviewed unit-economics assumptions with finance partners. Do not call my consulting job a PM job. No team management or invented numerical outcomes.'''
}
RATES={'gpt-6.1-sol':(2,10,.1,2.5),'gpt-6-astra':(10,50,1,12.5)}
def estimated_cost(metrics):
 total=0
 for entry in metrics:
  if entry['model']not in RATES:return None
  rate_in,rate_out,rate_cached,rate_write=RATES[entry['model']];usage=entry.get('usage')or{};n=usage.get('input_tokens',0);details=usage.get('input_tokens_details')or{};cached=details.get('cached_tokens',0);writes=details.get('cache_write_tokens',0);long_writes=(details.get('cache_write_tokens_details')or{}).get('ttl_12h_tokens',0)
  total+=(max(0,n-cached-writes)*rate_in+cached*rate_cached+max(0,writes-long_writes)*rate_write+long_writes*rate_in*2.5+usage.get('output_tokens',0)*rate_out)/1000000
 return round(total,6)
def post(origin,path,body,token):
 req=urllib.request.Request(origin+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-PM-Internal-Test':token})
 try:r=urllib.request.urlopen(req,timeout=280)
 except urllib.error.HTTPError as e:r=e
 with r:data=json.load(r)
 if r.status!=200:raise RuntimeError(json.dumps({'status':r.status,'response':data}))
 return data
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--origin',default='https://product-dna-studio-ai.onrender.com');parser.add_argument('--token-file',required=True);parser.add_argument('--output',required=True);args=parser.parse_args();token=Path(args.token_file).read_text().strip();dest=Path(args.output);dest.mkdir(parents=True,exist_ok=True)
 diag=post(args.origin,'/api/internal/models',{},token);(dest/'model-access.json').write_text(json.dumps(diag,indent=2));print(json.dumps(diag),flush=True)
 available={m['id']for m in diag['models']if m['listed_for_active_project']};primary='gpt-6.1-sol'if'gpt-6.1-sol'in available else diag['career_model'];jobs=[(name,primary)for name in PROFILES]
 if primary=='gpt-6.1-sol'and'gpt-6-astra'in available:jobs.extend((name,'gpt-6-astra')for name in ['ai_ml_pm','consulting_to_pm'])
 baseline=json.load(urllib.request.urlopen(args.origin+'/api/stats'));records=[]
 for name,model in jobs:
  src={'source_id':'src_benchmark','source_type':'typed_story','source_label':'Synthetic PM benchmark','content':PROFILES[name]};start=time.monotonic();result=post(args.origin,'/api/career-dna/generate',{'sources':[src],'request_id':'req_'+uuid.uuid4().hex,'benchmark_model':model},token);duration=round(time.monotonic()-start,2)
  assert result['map']['status']=='ready',(name,model,result['map']);validate_map(result['map'],[src]);assert result.get('counted')is False
  labels=[j['label']for j in result['map']['journey']]
  if name=='engineering_to_pm':assert'Software Engineer'in labels,labels
  if name=='consulting_to_pm':assert'Business Consultant'in labels,labels
  record={'profile':name,'model':result['model'],'seconds':duration,'estimated_usd':estimated_cost(result.get('usage_metrics',[])),'roles':labels,'capabilities':[s['label']for s in result['map']['strengths']],'response':result};records.append(record);(dest/(name+'-'+model+'.json')).write_text(json.dumps(record,indent=2));(dest/'results.json').write_text(json.dumps(records,indent=2));print(json.dumps({k:v for k,v in record.items()if k!='response'}),flush=True)
 after=json.load(urllib.request.urlopen(args.origin+'/api/stats'));assert baseline['total_generations']==after['total_generations'];print('All synthetic generations excluded from public count.',flush=True)
