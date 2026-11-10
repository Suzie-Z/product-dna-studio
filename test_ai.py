import unittest,json,os,copy,io,threading,urllib.request,urllib.error
from unittest.mock import patch
import ai_server as app
STORY='I built checkout experiments and analyzed conversion funnels. I designed reusable APIs and improved delivery workflows. I evaluated model outputs and reviewed reliability risks with engineers.'
def fixture():
 return {'sufficient':True,'headline':'Connecting customer insight with reliable product delivery','journey':[{'title':'Commerce Products','summary':'Checkout experiments and conversion funnels','icon':'chart','evidence':'I built checkout experiments and analyzed conversion funnels.'},{'title':'Platform Tools','summary':'Reusable APIs and delivery workflows','icon':'layers','evidence':'I designed reusable APIs and improved delivery workflows.'}], 'strengths':[{'title':'Customer Insight','summary':'Turn customer signals into focused experiments','keywords':['Funnels','Experiments'],'icon':'chart','basis':'direct','evidence':'I built checkout experiments and analyzed conversion funnels.'},{'title':'Systems Thinking','summary':'Connect reusable capabilities and delivery workflows','keywords':['Reusable APIs','Workflows'],'icon':'layers','basis':'direct','evidence':'I designed reusable APIs and improved delivery workflows.'}]}
class AIContracts(unittest.TestCase):
 def setUp(self):app.COUNTER.update(day='',count=0)
 def test_verified_evidence(self):self.assertEqual(app.validate_result(fixture(),STORY)['journey'][0]['title'],'Commerce Products')
 def test_fabricated_evidence_rejected(self):
  d=fixture();d['strengths'][0]['evidence']='Invented 200% revenue gain'
  with self.assertRaises(ValueError):app.validate_result(d,STORY)
 def test_overlong_and_non_english_rejected(self):
  for title in ['A'*24,'产品能力']:
   d=fixture();d['strengths'][0]['title']=title
   with self.assertRaises(ValueError):app.validate_result(d,STORY)
 def test_multilingual_evidence_allowed(self):
  d=fixture();source=STORY+' 我设计了支付产品并进行转化率实验。';d['strengths'][0]['evidence']='我设计了支付产品并进行转化率实验。'
  self.assertTrue(app.validate_result(d,source)['sufficient'])
 def test_inference_must_be_qualified(self):
  d=fixture();d['strengths'][0]['basis']='transferable'
  with self.assertRaises(ValueError):app.validate_result(d,STORY)
 def test_insufficient_experience(self):
  d=fixture();d['sufficient']=False
  with self.assertRaises(app.AppError)as e:app.validate_result(d,STORY)
  self.assertEqual(e.exception.status,422)
 def test_missing_key_is_not_demo(self):
  with patch.dict(os.environ,{'OPENAI_API_KEY':''}):
   with self.assertRaises(app.AppError)as e:app.generate(STORY,'')
  self.assertEqual(e.exception.status,503)
 def test_provider_contract_and_daily_cap(self):
  response={'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(fixture())}]}]}
  def upstream(req,timeout):
   data=json.loads(req.data);self.assertFalse(data['store']);self.assertTrue(data['text']['format']['strict']);self.assertEqual(data['model'],'gpt-5-mini');return io.BytesIO(json.dumps(response).encode())
  with patch.dict(os.environ,{'OPENAI_API_KEY':'test-not-a-real-key','DAILY_GENERATION_LIMIT':'1','TRIAL_START_DATE':''}),patch('ai_server.urllib.request.urlopen',side_effect=upstream)as mock:
   self.assertTrue(app.generate(STORY,'')['sufficient'])
   with self.assertRaises(app.AppError)as e:app.generate(STORY,'')
   self.assertEqual(e.exception.status,429);self.assertEqual(mock.call_count,1)
 def test_service_without_key_and_cors(self):
  server=app.ThreadingHTTPServer(('127.0.0.1',0),app.Handler);threading.Thread(target=server.serve_forever,daemon=True).start();url='http://127.0.0.1:'+str(server.server_port)
  try:
   with urllib.request.urlopen(url+'/health')as r:self.assertTrue(json.load(r)['ok'])
   for origin,expected in [('https://evil.example',403),('https://product-dna-studio-preview.onrender.com',503)]:
    req=urllib.request.Request(url+'/api/generate',data=json.dumps({'experience':STORY}).encode(),headers={'Origin':origin,'Content-Type':'application/json'})
    with patch.dict(os.environ,{'OPENAI_API_KEY':''}):
     with self.assertRaises(urllib.error.HTTPError)as e:urllib.request.urlopen(req)
    self.assertEqual(e.exception.code,expected)
  finally:server.shutdown();server.server_close()
if __name__=='__main__':unittest.main()
