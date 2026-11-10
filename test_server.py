import unittest,tempfile,os,threading,json,urllib.request,urllib.error,base64,importlib.util
class Workflow(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();os.environ['DNA_DATA_DIR']=cls.tmp.name;os.environ['DNA_ADMIN_PASSWORD']='test-password-only-123'
  spec=importlib.util.spec_from_file_location('studio',os.path.join(os.path.dirname(__file__),'server.py'));cls.app=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.app)
  cls.server=cls.app.ThreadingHTTPServer(('127.0.0.1',0),cls.app.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url='http://127.0.0.1:'+str(cls.server.server_port)
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.tmp.cleanup()
 def req(self,path,body=None,cookie=None,origin=None):
  h={};h.update({'Cookie':cookie} if cookie else {});h.update({'Origin':origin} if origin else {})
  if body is not None:h['Content-Type']='application/json'
  request=urllib.request.Request(self.url+path,data=json.dumps(body).encode() if body is not None else None,headers=h)
  try:r=urllib.request.urlopen(request)
  except urllib.error.HTTPError as e:r=e
  return r.status,json.loads(r.read()),r.headers
 def test_full_workflow(self):
  self.assertEqual(self.req('/api/admin/records')[0],401)
  payload=dict(participant='<script>alert(1)</script>',contact='tester@example.test',story='I developed analytics dashboards and platform APIs for customer teams.',result={'strengths':[{'name':'Data','details':'analytics dashboards'}]},image='data:image/png;base64,'+base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'test').decode(),consent=False)
  self.assertEqual(self.req('/api/submissions',payload)[0],400)
  payload['consent']=True
  code,item,_=self.req('/api/submissions',payload);self.assertEqual(code,201);ident=item['id']
  self.assertEqual(self.req('/api/admin/login',{'password':'wrong'})[0],401)
  code,_,headers=self.req('/api/admin/login',{'password':os.environ['DNA_ADMIN_PASSWORD']});self.assertEqual(code,200);cookie=headers['Set-Cookie'].split(';')[0]
  self.assertIn('HttpOnly',headers['Set-Cookie']);self.assertIn('SameSite=Strict',headers['Set-Cookie'])
  records=self.req('/api/admin/records',cookie=cookie)[1];self.assertEqual(len(records),1)
  code,detail,_=self.req('/api/admin/records/'+ident,cookie=cookie);self.assertEqual(detail['story'],payload['story']);self.assertEqual(detail['image'],payload['image']);self.assertEqual(detail['result'],payload['result'])
  update={'status':'reviewed','note':'Evidence needs further verification'}
  self.assertEqual(self.req('/api/admin/records/'+ident,update,cookie,'https://evil.example')[0],403)
  self.assertEqual(self.req('/api/admin/records/'+ident,update,cookie)[0],200)
  exported=self.req('/api/admin/export',cookie=cookie)[1];self.assertEqual(exported[0]['note'],update['note'])
  # Re-open a separate SQLite connection to verify durable data.
  with self.app.db() as c:self.assertEqual(c.execute('SELECT status FROM submissions WHERE id=?',(ident,)).fetchone()[0],'reviewed')
  self.assertEqual(self.req('/api/admin/records/'+ident,{'action':'delete'},cookie)[0],200)
  self.assertEqual(self.req('/api/admin/records/'+ident,cookie=cookie)[0],404)
if __name__=='__main__':unittest.main()
