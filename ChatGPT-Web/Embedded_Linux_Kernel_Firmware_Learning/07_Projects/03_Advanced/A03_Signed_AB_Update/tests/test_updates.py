import unittest,tempfile,subprocess,sys,json
from pathlib import Path
sys.path.insert(0,'src');import update as u
class Updates(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.d=Path(self.t.name);self.key=self.d/'private.pem';self.pub=self.d/'public.pem';self.root=self.d/'device'
  subprocess.run(['openssl','genpkey','-algorithm','EC','-pkeyopt','ec_paramgen_curve:P-256','-out',str(self.key)],check=True,capture_output=True)
  subprocess.run(['openssl','pkey','-in',str(self.key),'-pubout','-out',str(self.pub)],check=True,capture_output=True)
  self.b1=self.make(1);self.b2=self.make(2);u.initialize(self.root,self.pub,self.b1)
 def tearDown(self):self.t.cleanup()
 def make(self,n):
  payload=self.d/f'payload{n}';payload.write_bytes(f'learning image {n}'.encode());b=self.d/f'bundle{n}';u.bundle(b,payload,n,self.key);return b
 def test_confirm(self):
  self.assertEqual(u.install(self.root,self.b2),'B');self.assertEqual(u.boot(self.root),'B');u.mark_good(self.root,'B');self.assertEqual(u.state(self.root)['active'],'B');self.assertEqual(u.state(self.root)['min_version'],2)
 def test_rollback(self):
  u.install(self.root,self.b2);self.assertEqual([u.boot(self.root) for _ in range(3)],['B','B','A'])
 def test_payload_tamper(self):
  (self.b2/'image.bin').write_bytes(b'evil')
  with self.assertRaises(ValueError):u.install(self.root,self.b2)
  self.assertEqual(u.state(self.root)['active'],'A')
 def test_manifest_tamper(self):
  m=json.loads((self.b2/'manifest.json').read_text());m['version']=90;(self.b2/'manifest.json').write_text(json.dumps(m))
  with self.assertRaises(ValueError):u.install(self.root,self.b2)
 def test_interruption(self):
  with self.assertRaises(InterruptedError):u.install(self.root,self.b2,True)
  self.assertEqual(u.boot(self.root),'A');self.assertIsNone(u.state(self.root)['pending'])
 def test_downgrade(self):
  u.install(self.root,self.b2);u.boot(self.root);u.mark_good(self.root,'B')
  with self.assertRaises(ValueError):u.install(self.root,self.b1)
 def test_no_early_confirmation(self):
  u.install(self.root,self.b2)
  with self.assertRaises(ValueError):u.mark_good(self.root,'B')
 def test_pending_block(self):
  u.install(self.root,self.b2)
  with self.assertRaises(ValueError):u.install(self.root,self.b2)
 def test_corrupt_trial_fallback(self):
  u.install(self.root,self.b2);(self.root/'slots/B/image.bin').write_bytes(b'bad')
  self.assertEqual(u.boot(self.root),'A')
if __name__=='__main__':unittest.main()
