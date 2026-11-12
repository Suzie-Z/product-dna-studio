"""Ten-minute request-memory replay; no CV/map persistence or body logging."""
import copy,hashlib,json,re,threading,time
LOCK=threading.Lock();CACHE={};TTL=600

def begin(key,body):
 if not isinstance(key,str)or not re.fullmatch(r'[A-Za-z0-9_-]{16,80}',key):raise ValueError('invalid request identifier')
 digest=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
 with LOCK:
  now=time.monotonic()
  for old,item in list(CACHE.items()):
   if item['expires']<=now:del CACHE[old]
  if key in CACHE:
   item=CACHE[key]
   if item['fingerprint']!=digest:return 'conflict',None
   return ('replay',copy.deepcopy(item['result']))if item['result']is not None else('pending',None)
  if len(CACHE)>=40:
   oldest=min((k for k,v in CACHE.items()if v['result']is not None),key=lambda k:CACHE[k]['expires'],default=None)
   if oldest:del CACHE[oldest]
   else:return 'pending',None
  CACHE[key]={'fingerprint':digest,'expires':now+TTL,'result':None}
  timer=threading.Timer(TTL,lambda:discard(key,now+TTL));timer.daemon=True;timer.start()
 return 'new',None

def finish(key,result):
 with LOCK:
  if key in CACHE:CACHE[key]['result']=copy.deepcopy(result)
def discard(key,expected_expiry=None):
 with LOCK:
  if expected_expiry is None or CACHE.get(key,{}).get('expires')==expected_expiry:CACHE.pop(key,None)
