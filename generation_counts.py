"""Auditable v2 aggregates plus random-request receipts; legacy totals stay untouched."""
import hashlib,os,threading,time
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
_LOCK=threading.Lock();_DAYS={};_RECEIPTS={};_START=None

def day():return datetime.now(ZoneInfo('Australia/Sydney')).date().isoformat()
def _metadata(total,daily,today,scope,start,legacy=None,ordinal=None):
 return {'total_generations':int(total),'today_generations':int(daily),'day':today,'timezone':'Australia/Sydney','scope':scope,'tracking_version':2,'tracking_started_on':str(start),'legacy_total_unverified':legacy,'generation_number':ordinal}
def _database_snapshot(conn,increment,today,receipt):
 with conn.cursor()as cur:
  cur.execute("SELECT pg_advisory_xact_lock(hashtext('pm_dna_counter_v2'))")
  cur.execute('CREATE TABLE IF NOT EXISTS pm_dna_public_counts_v2(generation_day DATE PRIMARY KEY,generated_count BIGINT NOT NULL CHECK(generated_count>=0))')
  cur.execute('CREATE TABLE IF NOT EXISTS pm_dna_count_meta_v2(singleton BOOLEAN PRIMARY KEY DEFAULT TRUE CHECK(singleton),started_on DATE NOT NULL)')
  cur.execute('INSERT INTO pm_dna_count_meta_v2(singleton,started_on) VALUES(TRUE,%s) ON CONFLICT DO NOTHING',(today,))
  cur.execute('CREATE TABLE IF NOT EXISTS pm_dna_count_receipts_v2(request_hash CHAR(64) PRIMARY KEY,generation_day DATE NOT NULL,generation_number BIGINT NOT NULL,created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())')
  cur.execute("DELETE FROM pm_dna_count_receipts_v2 WHERE created_at<NOW()-INTERVAL '48 hours'")
  cur.execute('SELECT COALESCE(SUM(generated_count),0),COALESCE(SUM(generated_count) FILTER(WHERE generation_day=%s),0) FROM pm_dna_public_counts_v2',(today,));total,daily=cur.fetchone();ordinal=None
  if increment:
   cur.execute('SELECT generation_number FROM pm_dna_count_receipts_v2 WHERE request_hash=%s',(receipt,));existing=cur.fetchone()
   if existing:ordinal=int(existing[0])
   else:
    total+=1;daily+=1;ordinal=int(total)
    cur.execute('INSERT INTO pm_dna_public_counts_v2(generation_day,generated_count) VALUES(%s,1) ON CONFLICT(generation_day) DO UPDATE SET generated_count=pm_dna_public_counts_v2.generated_count+1',(today,))
    cur.execute('INSERT INTO pm_dna_count_receipts_v2(request_hash,generation_day,generation_number) VALUES(%s,%s,%s)',(receipt,today,ordinal))
  cur.execute('SELECT started_on FROM pm_dna_count_meta_v2 WHERE singleton=TRUE');start=cur.fetchone()[0]
  cur.execute("SELECT to_regclass('public.career_dna_generation_counts')");legacy_table=cur.fetchone()[0];legacy=None
  if legacy_table:
   cur.execute('SELECT COALESCE(SUM(generated_count),0) FROM career_dna_generation_counts');legacy=int(cur.fetchone()[0])
 return _metadata(total,daily,today,'persistent',start,legacy,ordinal)
def snapshot(increment=False,request_id=None,eligible=True):
 global _START
 today=day();url=os.environ.get('COUNTER_DATABASE_URL','').strip();increment=bool(increment and eligible)
 receipt=hashlib.sha256(request_id.encode()).hexdigest()if request_id else None
 if not url:
  with _LOCK:
   if _START is None:_START=today
   ordinal=None
   if increment:
    if receipt and receipt in _RECEIPTS:ordinal=_RECEIPTS[receipt][0]
    else:
     _DAYS[today]=_DAYS.get(today,0)+1;ordinal=sum(_DAYS.values())
     if receipt:_RECEIPTS[receipt]=(ordinal,today,time.monotonic())
   cutoff=(datetime.fromisoformat(today).date()-timedelta(days=2)).isoformat()
   for key,value in list(_RECEIPTS.items()):
    if value[2]<time.monotonic()-48*3600:del _RECEIPTS[key]
   return _metadata(sum(_DAYS.values()),_DAYS.get(today,0),today,'process',_START,ordinal=ordinal)
 import psycopg,secrets
 if increment and not receipt:receipt=hashlib.sha256(secrets.token_bytes(32)).hexdigest()
 with psycopg.connect(url,connect_timeout=5)as conn:return _database_snapshot(conn,increment,today,receipt)
def verify_storage_rollback():
 """Admin-only production self-test: all synthetic writes are force-rolled back."""
 import psycopg,secrets
 url=os.environ.get('COUNTER_DATABASE_URL','').strip()
 if not url:return {'verified':False,'reason':'No persistent counter configured'}
 with psycopg.connect(url,connect_timeout=5)as conn:
  with conn.transaction(force_rollback=True):
   rid=hashlib.sha256(secrets.token_bytes(32)).hexdigest();before=_database_snapshot(conn,False,day(),None);a=_database_snapshot(conn,True,day(),rid);b=_database_snapshot(conn,True,day(),rid)
   assert a['total_generations']==before['total_generations']+1 and b['total_generations']==a['total_generations']and a['generation_number']==b['generation_number']
 return {'verified':True,'test_writes_rolled_back':True,'deduplicated':True}
