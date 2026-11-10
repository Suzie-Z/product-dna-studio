"""Stateless HTTP boundary. Request bodies, transcripts and model content are not logged."""
import json,os,threading,time,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from career_ai import AppError,process_generate,process_refine,process_review
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
  if path=='/health':return self.reply(200,{'ok':True,'ai_configured':bool(os.environ.get('OPENAI_API_KEY')),'schema_version':'1.0'})
  paths={'/':('index.html','text/html; charset=utf-8'),'/studio.js':('studio.js','text/javascript; charset=utf-8'),'/poster.js':('poster.js','text/javascript; charset=utf-8'),'/studio.css':('studio.css','text/css; charset=utf-8')}
  if path not in paths:return self.reply(404,{'error':'Not found.'})
  name,typ=paths[path];return self.reply(200,(ROOT/name).read_bytes(),typ)
 def do_POST(self):
  acquired=False
  try:
   if not self.origin_allowed():raise AppError(403,'Origin not allowed.','origin_rejected')
   handlers={'/api/career-dna/generate':process_generate,'/api/career-dna/refine':process_refine,'/api/career-dna/review':process_review}
   if self.path not in handlers:raise AppError(404,'Not found.','not_found')
   if not self.headers.get('Content-Type','').startswith('application/json'):raise AppError(415,'Use a JSON request.','content_type')
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<=240000:raise AppError(413,'Your request is too long. Shorten your experience or refinement history.','request_too_large')
   self.connection.settimeout(15);body=json.loads(self.rfile.read(length))
   if not isinstance(body,dict):raise AppError(400,'This request could not be read.','invalid_body')
   rate_limit(self.client_address[0]);acquired=ACTIVE.acquire(blocking=False)
   if not acquired:raise AppError(429,'The studio is busy. Try again shortly.','busy')
   return self.reply(200,handlers[self.path](body))
  except AppError as e:return self.reply(e.status,{'error':e.message,'code':e.code})
  except (ValueError,TypeError,AttributeError,KeyError):return self.reply(400,{'error':'This request could not be read. Check your sources and try again.','code':'invalid_request'})
  except (BrokenPipeError,ConnectionResetError):return
  except Exception:return self.reply(500,{'error':'Something went wrong. Please try again later.','code':'internal_error'})
  finally:
   if acquired:ACTIVE.release()
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','10000'))),Handler).serve_forever()
