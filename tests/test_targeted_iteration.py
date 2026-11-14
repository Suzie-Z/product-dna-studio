import os,threading,unittest
from unittest.mock import patch
import generation_counts as counts
from tests import test_original_refinement as original
from tests.fixtures import make_map
class Downloads(unittest.TestCase):
 def setUp(self):
  self.env=patch.dict(os.environ,{'COUNTER_DATABASE_URL':''});self.env.start();counts._DOWNLOADS=0;counts._DOWNLOAD_RECEIPTS.clear()
 def tearDown(self):self.env.stop()
 def test_concurrent_retry_counts_once_without_creations(self):
  before=counts.snapshot()['total_generations']
  threads=[threading.Thread(target=counts.downloads,kwargs={'increment':True,'request_id':'download_test_0123456789'})for _ in range(20)]
  for t in threads:t.start()
  for t in threads:t.join()
  self.assertEqual(counts.public_stats()['total_downloads'],1);self.assertEqual(counts.snapshot()['total_generations'],before)
 def test_failed_retrieval_omits_metric(self):
  with patch('generation_counts.downloads',side_effect=RuntimeError):self.assertNotIn('total_downloads',counts.public_stats())
 def test_missing_or_content_receipt_is_rejected(self):
  for rid in [None,'cv text',{},'a'*101]:
   with self.assertRaises(ValueError):counts.downloads(True,rid)
class IterationBrowser(unittest.TestCase):
 setUpClass=classmethod(original.OriginalBrowser.setUpClass.__func__)
 tearDownClass=classmethod(original.OriginalBrowser.tearDownClass.__func__)
 setUp=original.OriginalBrowser.setUp
 tearDown=original.OriginalBrowser.tearDown
 page=original.OriginalBrowser.page
 upload=original.OriginalBrowser.upload
 ready=original.OriginalBrowser.ready
 def test_download_handoff_copy_and_summary_gap(self):
  page,context=self.ready();requests=[]
  context.route('**/api/downloads',lambda r:(requests.append(r.request.post_data_json),r.fulfill(json={'total_generations':7,'total_downloads':1,'scope':'persistent'})))
  self.assertEqual(' '.join(page.locator('#save').inner_text().split()),'Download ↓')
  self.assertIn('only read in your browser',page.locator('.cv-upload .helper').inner_text())
  self.assertNotIn('Evidence: Career source',page.locator('#journey-evidence').inner_text())
  for n in [2,3,4]:
   metrics=page.evaluate('d=>buildDNAScene(d,false,nextPMVariant(d)).metrics',make_map(n,n));self.assertTrue(metrics['ok'],metrics['issues']);self.assertFalse(metrics['collisions']);self.assertFalse(metrics['clipped'])
  with page.expect_download():page.locator('#save').click()
  page.wait_for_function('document.getElementById("usage-count").textContent.includes("1 Downloads")');self.assertEqual(len(requests),1)
  context.close()
class DownloadHTTP(unittest.TestCase):
 setUpClass=classmethod(original.ModelAndScopeHTTP.setUpClass.__func__)
 tearDownClass=classmethod(original.ModelAndScopeHTTP.tearDownClass.__func__)
 def test_real_endpoint_deduplicates_without_model_calls(self):
  import json,urllib.request,ai_server
  ai_server.RECENT.clear()
  with patch.dict(os.environ,{'COUNTER_DATABASE_URL':''}),patch('career_ai.provider',side_effect=AssertionError('No AI for downloads')):
   before=counts.downloads();body=json.dumps({'request_id':'http_download_0123456789'}).encode()
   for _ in range(2):
    request=urllib.request.Request(self.url+'/api/downloads',data=body,headers={'Content-Type':'application/json'})
    response=json.load(urllib.request.urlopen(request));self.assertEqual(response['total_downloads'],before+1)
