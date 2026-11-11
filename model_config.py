"""Non-secret model selection and authenticated diagnostics; no SDK/key disclosure."""
import contextvars,json,os,threading,time,urllib.request,urllib.error
MODEL_OVERRIDE=contextvars.ContextVar('career_model_override',default=None)
USAGE=contextvars.ContextVar('career_usage',default=None)
MODEL_LOCK=threading.Lock();_CACHE={'at':0,'ids':set(),'state':'unchecked'}
PROPOSED=['gpt-6.1-sol','gpt-6-astra','gpt-image-2.6-sunburst']
def career_model():return MODEL_OVERRIDE.get()or os.environ.get('OPENAI_CAREER_MODEL','').strip()or os.environ.get('OPENAI_MODEL','').strip()or'gpt-5-mini'
def configuration():
 return {'career_model':career_model(),'configuration_source':'OPENAI_CAREER_MODEL'if os.environ.get('OPENAI_CAREER_MODEL','').strip()else'OPENAI_MODEL'if os.environ.get('OPENAI_MODEL','').strip()else'default','image_model':None,'visual_engine':'deterministic SVG with local illustration assets','provider_endpoint':'https://api.openai.com/v1/responses','transport':'Python urllib.request; no OpenAI SDK','reasoning':'medium','provider_store':False}
def available_models():
 with MODEL_LOCK:
  if time.monotonic()-_CACHE['at']<300:return _CACHE
  key=os.environ.get('OPENAI_API_KEY','').strip()
  if not key:return {'at':time.monotonic(),'ids':set(),'state':'not_configured'}
  try:
   request=urllib.request.Request('https://api.openai.com/v1/models',headers={'Authorization':'Bearer '+key})
   with urllib.request.urlopen(request,timeout=25)as response:ids={x['id']for x in json.load(response).get('data',[])}
   _CACHE.update(at=time.monotonic(),ids=ids,state='checked')
  except (urllib.error.URLError,TimeoutError,ValueError):_CACHE.update(at=time.monotonic(),ids=set(),state='unavailable')
  return _CACHE

def diagnostics():
 result=configuration();access=available_models();candidates=list(dict.fromkeys([career_model(),*PROPOSED,'gpt-5','gpt-5-mini']))
 result.update(availability_check=access['state'],models=[{'id':m,'listed_for_active_project':m in access['ids']if access['state']=='checked'else None}for m in candidates]);return result
