"""Stateless HTTP boundary. Request bodies, transcripts and model content are not logged."""
import json,os,threading,time,hashlib,hmac,secrets
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from career_ai import AppError,process_generate,process_refine,process_review
from generation_counts import snapshot as generation_stats,verify_storage_rollback
from model_config import configuration,diagnostics,available_models,MODEL_OVERRIDE,USAGE
import request_state
ROOT=Path(__file__).parent/'preview'
ALLOWED_ORIGINS={'https://product-dna-studio-preview.onrender.com'}|set(filter(None,os.environ.get('ALLOWED_ORIGINS','').split(',')))
REQUEST_LOCK=threading.Lock();RECENT={};ACTIVE=threading.BoundedSemaphore(2)

def rate_limit(client):
 # Short-lived hashed network identifiers only; no durable visitor database.
 ident=hashlib.sha256(client.encode()).hexdigest()[:20];now=time.monotonic()
 with REQUEST_LOCK:
  for key in list(RECENT):
   if not any(t>now-60 for t in RECENT[key]):del RECENT[key]
  times=[t for t in RECENT.get(ident,[])if t>now-60]
  if len(times)>=8:raise AppError(429,'Too many requests. Please wait a minute.','rate_limit')
  RECENT[ident]=times+[now]
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def origin_allowed(self):
  origin=self.headers.get('Origin')
  return not origin or origin in ALLOWED_ORIGINS or origin.split('://',1)[-1]==self.headers.get('Host')
 def reply(self,status,data,typ='application/json; charset=utf-8'):
  body=json.dumps(data,ensure_ascii=False).encode()if typ.startswith('application/json')else data
  self.send_response(status)
  for k,v in {'Content-Type':typ,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY','Referrer-Policy':'same-origin'}.items():self.send_header(k,v)
  origin=self.headers.get('Origin')
  if origin and self.origin_allowed():self.send_header('Access-Control-Allow-Origin',origin);self.send_header('Vary','Origin')
  self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def do_OPTIONS(self):
  if not self.origin_allowed():return self.reply(403,{'error':'Origin not allowed.'})
  self.send_response(204);self.send_header('Access-Control-Allow-Origin',self.headers.get('Origin',''));self.send_header('Vary','Origin');self.send_header('Access-Control-Allow-Methods','POST, GET, OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.send_header('Access-Control-Max-Age','600');self.end_headers()
 def do_GET(self):
  path=self.path.split('?')[0]
  if path=='/api/stats':
   try:return self.reply(200,generation_stats())
   except Exception:return self.reply(503,{'error':'Generation count temporarily unavailable.'})
  if path=='/health':return self.reply(200,{'ok':True,'ai_configured':bool(os.environ.get('OPENAI_API_KEY')),'schema_version':'1.0',**configuration()})
  paths={'/':('index.html','text/html; charset=utf-8'),'/studio.js':('studio.js','text/javascript; charset=utf-8'),'/poster.js':('poster.js','text/javascript; charset=utf-8'),'/studio.css':('studio.css','text/css; charset=utf-8')}
  if path not in paths:return self.reply(404,{'error':'Not found.'})
  name,typ=paths[path];return self.reply(200,(ROOT/name).read_bytes(),typ)
 def do_POST(self):
  internal=False;acquired=False;cache_key=None;cache_finished=False;model_token=None;usage_token=None
  try:
   if not self.origin_allowed():raise AppError(403,'Origin not allowed.','origin_rejected')
   handlers={'/api/internal/models':lambda b:diagnostics(),'/api/internal/counter-check':lambda b:verify_storage_rollback(),'/api/career-dna/generate':process_generate,'/api/career-dna/refine':process_refine,'/api/career-dna/review':process_review}
   if self.path not in handlers:raise AppError(404,'Not found.','not_found')
   if not self.headers.get('Content-Type','').startswith('application/json'):raise AppError(415,'Use a JSON request.','content_type')
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<=240000:raise AppError(413,'Your request is too long. Shorten your experience or refinement history.','request_too_large')
   self.connection.settimeout(15);body=json.loads(self.rfile.read(length))
   if not isinstance(body,dict):raise AppError(400,'This request could not be read.','invalid_body')
   internal_key=os.environ.get('PM_INTERNAL_TEST_TOKEN','')
   internal=bool(internal_key and hmac.compare_digest(self.headers.get('X-PM-Internal-Test',''),internal_key))
   if self.path.startswith('/api/internal/'):
    if not internal:raise AppError(403,'This diagnostic is restricted.','forbidden')
    return self.reply(200,handlers[self.path](body))
   rate_limit(self.client_address[0]);acquired=ACTIVE.acquire(blocking=False)
   if not acquired:raise AppError(429,'The studio is busy. Try again shortly.','busy')
   base_version=body.get('map_version',1)
   if type(base_version)is not int or not 1<=base_version<=1000:raise AppError(400,'The map version is invalid.','invalid_version')
   next_version=body.get('next_version',1 if self.path.endswith('/generate')else base_version+1)
   if type(next_version)is not int or next_version<1 or next_version>1001 or(self.path.endswith('/refine')and next_version<=base_version):raise AppError(400,'The next map version is invalid.','invalid_version')
   override=body.get('benchmark_model')if internal else None
   if override:
    if override not in available_models()['ids']:raise AppError(400,'The requested benchmark model is not available to this API project.','model_unavailable')
    model_token=MODEL_OVERRIDE.set(override)
   usage_token=USAGE.set([])
   rid=body.get('request_id')or'req_'+secrets.token_hex(16)
   cache_key=self.path+':'+rid
   state,cached=request_state.begin(rid,{**body,'_endpoint':self.path,'_internal':internal})
   cache_key=rid
   if state=='replay':cache_finished=True;return self.reply(200,cached)
   if state=='conflict':cache_key=None;raise AppError(409,'This request identifier was already used for different input.','idempotency_conflict')
   if state=='pending':cache_key=None;raise AppError(409,'Your earlier request is still running. Wait a moment, then retry.','request_in_progress')
   started=time.monotonic();result=handlers[self.path](body)
   result['map_version']=next_version
   result['base_version']=base_version if self.path.endswith('/refine')else None
   result['model']=configuration()['career_model'];result['elapsed_seconds']=round(time.monotonic()-started,2)
   if internal:result['usage_metrics']=USAGE.get()
   if self.path=='/api/career-dna/generate'and result.get('map',{}).get('status')=='ready':
    eligible=os.environ.get('PUBLIC_COUNTER_ENV','')=='production'and not internal
    try:
     stats=generation_stats(increment=True,request_id=rid,eligible=eligible);result['stats']=stats;result['generation_number']=stats.get('generation_number');result['counted']=eligible
    except Exception:result['stats_unavailable']=True
   request_state.finish(cache_key,result);cache_finished=True
   return self.reply(200,result)
  except AppError as e:
   failure={'error':e.message,'code':e.code}
   if getattr(e,'validation_issue',None):failure['validation_issue']=e.validation_issue
   if internal and getattr(e,'provider_detail',None):failure['provider_detail']=e.provider_detail
   return self.reply(e.status,failure)
  except (ValueError,TypeError,AttributeError,KeyError):return self.reply(400,{'error':'This request could not be read. Check your sources and try again.','code':'invalid_request'})
  except (BrokenPipeError,ConnectionResetError):return
  except Exception:return self.reply(500,{'error':'Something went wrong. Please try again later.','code':'internal_error'})
  finally:
   if cache_key and not cache_finished:request_state.discard(cache_key)
   if model_token is not None:MODEL_OVERRIDE.reset(model_token)
   if usage_token is not None:USAGE.reset(usage_token)
   if acquired:ACTIVE.release()
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','10000'))),Handler).serve_forever()
