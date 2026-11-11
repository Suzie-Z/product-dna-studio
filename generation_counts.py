"""Anonymous aggregate counts only: dates and integers, never content or visitor IDs."""
import os,threading
from datetime import datetime
from zoneinfo import ZoneInfo
_LOCK=threading.Lock();_DAYS={}
def day():return datetime.now(ZoneInfo('Australia/Sydney')).date().isoformat()
def snapshot(increment=False):
 today=day();url=os.environ.get('COUNTER_DATABASE_URL','').strip()
 if not url:
  with _LOCK:
   if increment:_DAYS[today]=_DAYS.get(today,0)+1
   return {'total_generations':sum(_DAYS.values()),'today_generations':_DAYS.get(today,0),'day':today,'timezone':'Australia/Sydney','scope':'process'}
 # Optional dependency, installed by the persistent-counter Render build.
 import psycopg
 with psycopg.connect(url,connect_timeout=5)as conn:
  with conn.cursor()as cursor:
   cursor.execute("SELECT pg_advisory_xact_lock(hashtext('career_dna_counter_v1'))")
   cursor.execute('CREATE TABLE IF NOT EXISTS career_dna_generation_counts (generation_day DATE PRIMARY KEY, generated_count BIGINT NOT NULL CHECK (generated_count >= 0))')
   if increment:cursor.execute('INSERT INTO career_dna_generation_counts(generation_day,generated_count) VALUES(%s,1) ON CONFLICT(generation_day) DO UPDATE SET generated_count=career_dna_generation_counts.generated_count+1',(today,))
   cursor.execute('SELECT COALESCE(SUM(generated_count),0),COALESCE(SUM(generated_count) FILTER(WHERE generation_day=%s),0) FROM career_dna_generation_counts',(today,))
   total,daily=cursor.fetchone()
 return {'total_generations':int(total),'today_generations':int(daily),'day':today,'timezone':'Australia/Sydney','scope':'persistent'}
