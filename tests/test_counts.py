import os,threading,unittest
from unittest.mock import patch
import generation_counts as c
class Counts(unittest.TestCase):
 def setUp(self):c._DAYS.clear();self.env=patch.dict(os.environ,{'COUNTER_DATABASE_URL':''});self.env.start()
 def tearDown(self):self.env.stop()
 def test_only_integer_aggregates_and_date_are_retained(self):
  self.assertEqual(c.snapshot()['total_generations'],0)
  self.assertEqual(c.snapshot(True)['total_generations'],1)
  self.assertEqual(set(c._DAYS.values()),{1});self.assertEqual(c.snapshot()['today_generations'],1)
 def test_atomic_ordinals(self):
  ordinals=[]
  def increment():ordinals.append(c.snapshot(True)['total_generations'])
  threads=[threading.Thread(target=increment)for _ in range(20)]
  for t in threads:t.start()
  for t in threads:t.join()
  self.assertEqual(sorted(ordinals),list(range(1,21)))
 def test_day_rollover_preserves_total(self):
  with patch('generation_counts.day',return_value='2026-11-11'):c.snapshot(True)
  with patch('generation_counts.day',return_value='2026-11-12'):
   value=c.snapshot(True);self.assertEqual(value['total_generations'],2);self.assertEqual(value['today_generations'],1)
