"""Product DNA Studio: Python 3.11+, no third-party dependencies."""
import os,json,sqlite3,secrets,time,hashlib,hmac,base64,io,csv
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
ROOT=Path(__file__).parent
DATA=Path(os.environ.get('DNA_DATA_DIR',str(ROOT/'data'))); DATA.mkdir(parents=True,exist_ok=True)
PASSWORD=os.environ.get('DNA_ADMIN_PASSWORD')
if not PASSWORD or len(PASSWORD)<12: raise SystemExit('Set DNA_ADMIN_PASSWORD to at least 12 characters.')
KEY=secrets.token_bytes(32)
def db():
 c=sqlite3.connect(DATA/'studio.sqlite'); c.row_factory=sqlite3.Row; return c
with db() as c:
 c.execute('''CREATE TABLE IF NOT EXISTS submissions(id TEXT PRIMARY KEY, participant TEXT NOT NULL, contact TEXT NOT NULL, story TEXT NOT NULL, result TEXT NOT NULL, image TEXT NOT NULL, created TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending', note TEXT NOT NULL DEFAULT '', consent_version TEXT NOT NULL)''')
ATTEMPTS={}
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args): pass
 def reply(self,status,data,typ='application/json; charset=utf-8',headers=None):
  body=json.dumps(data,ensure_ascii=False).encode() if typ.startswith('application/json') else data.encode() if isinstance(data,str) else data
  self.send_response(status)
  for k,v in {'Content-Type':typ,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'same-origin','X-Frame-Options':'DENY',**(headers or {})}.items():self.send_header(k,v)
  self.end_headers();self.wfile.write(body)
 def authorized(self):
  import http.cookies
  ck=http.cookies.SimpleCookie();ck.load(self.headers.get('Cookie',''))
  token=ck.get('dna_admin')
  if not token:return False
  try:
   payload,sig=token.value.split('.')
   return hmac.compare_digest(sig,hmac.new(KEY,payload.encode(),hashlib.sha256).hexdigest()) and 0<=time.time()-int(payload)<28800
  except Exception:return False
 def body(self):
  n=int(self.headers.get('Content-Length','0'))
  if n>3500000:raise ValueError('Request too large')
  return json.loads(self.rfile.read(n))
 def do_GET(self):
  path=self.path.split('?')[0]
  if path in ['/','/admin']:
   return self.reply(200,(ROOT/'public'/('index.html' if path=='/' else 'admin.html')).read_bytes(),'text/html; charset=utf-8')
  if path.startswith('/api/admin'):
   if not self.authorized():return self.reply(401,{'error':'请先登录后台'})
   with db() as c:
    if path=='/api/admin/records':
     rows=[dict(x) for x in c.execute('SELECT id,participant,contact,created,status,note FROM submissions ORDER BY created DESC')];return self.reply(200,rows)
    if path=='/api/admin/export':
     rows=[dict(x) for x in c.execute('SELECT * FROM submissions ORDER BY created DESC')]
     return self.reply(200,rows,headers={'Content-Disposition':'attachment; filename="dna-submissions.json"'})
    row=c.execute('SELECT * FROM submissions WHERE id=?',(path.rsplit('/',1)[-1],)).fetchone()
    if row:
     item=dict(row);item['result']=json.loads(item['result']);return self.reply(200,item)
    return self.reply(404,{'error':'记录不存在'})
  return self.reply(404,{'error':'Not found'})
 def do_POST(self):
  try:
   # Reject cross-origin mutations even if a browser has an admin cookie.
   origin=self.headers.get('Origin')
   if origin and origin.split('://',1)[-1]!=self.headers.get('Host'):return self.reply(403,{'error':'Cross-origin request rejected'})
   body=self.body();path=self.path
   if path=='/api/admin/login':
    ip=self.client_address[0];times=[x for x in ATTEMPTS.get(ip,[]) if x>time.time()-900];ATTEMPTS[ip]=times
    if len(times)>=8:return self.reply(429,{'error':'尝试次数过多，请15分钟后再试'})
    if not hmac.compare_digest(str(body.get('password','')),PASSWORD):
     times.append(time.time());return self.reply(401,{'error':'密码不正确'})
    ATTEMPTS.pop(ip,None);p=str(int(time.time()));token=p+'.'+hmac.new(KEY,p.encode(),hashlib.sha256).hexdigest()
    secure='; Secure' if os.environ.get('DNA_COOKIE_SECURE')=='1' else ''
    return self.reply(200,{'ok':True},headers={'Set-Cookie':'dna_admin='+token+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800'+secure})
   if path=='/api/admin/logout':return self.reply(200,{'ok':True},headers={'Set-Cookie':'dna_admin=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'})
   if path=='/api/submissions':
    if body.get('consent') is not True:raise ValueError('需要明确同意保存')
    for field,lo,hi in [('participant',1,100),('contact',0,200),('story',30,20000)]:
     if not isinstance(body.get(field),str) or not lo<=len(body[field].strip())<=hi:raise ValueError('Invalid '+field)
    result=body.get('result');image=body.get('image','')
    if not isinstance(result,dict) or len(json.dumps(result))>30000:raise ValueError('Invalid result')
    if not image.startswith('data:image/png;base64,'):raise ValueError('PNG snapshot required')
    raw=base64.b64decode(image.split(',',1)[1],validate=True)
    if not raw.startswith(b'\x89PNG\r\n\x1a\n') or len(raw)>2300000:raise ValueError('Invalid PNG')
    ident=secrets.token_urlsafe(16)
    with db() as c:c.execute('INSERT INTO submissions(id,participant,contact,story,result,image,created,consent_version) VALUES(?,?,?,?,?,?,?,?)',(ident,body['participant'].strip(),body['contact'].strip(),body['story'],json.dumps(result,ensure_ascii=False),image,time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'2026-11-10-v1'))
    return self.reply(201,{'id':ident})
   if path.startswith('/api/admin/'):
    if not self.authorized():return self.reply(401,{'error':'请先登录后台'})
    ident=path.rsplit('/',1)[-1]
    with db() as c:
     if body.get('action')=='delete':cur=c.execute('DELETE FROM submissions WHERE id=?',(ident,))
     else:
      if body.get('status') not in ['pending','reviewed','followup']:raise ValueError('Invalid review status')
      if not isinstance(body.get('note'),str) or len(body['note'])>5000:raise ValueError('Note too long')
      cur=c.execute('UPDATE submissions SET status=?,note=? WHERE id=?',(body['status'],body['note'],ident))
     if not cur.rowcount:return self.reply(404,{'error':'记录不存在'})
    return self.reply(200,{'ok':True})
   return self.reply(404,{'error':'Not found'})
  except (ValueError,TypeError,KeyError):return self.reply(400,{'error':'提交格式不正确，请检查姓名、内容、同意选项和产出图片大小。'})
  except Exception:return self.reply(500,{'error':'保存失败，请稍后重试；请勿关闭本页。'})
if __name__=='__main__':
 print('Product DNA Studio: http://localhost:'+os.environ.get('PORT','8080'),flush=True)
 ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8080'))),Handler).serve_forever()
