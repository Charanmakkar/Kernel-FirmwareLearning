import json,sys,subprocess,tempfile,unittest
from pathlib import Path
sys.path.insert(0,'src');from gateway import Gateway,config,atomic_json
from simulated_mcu import frame
class GatewayTests(unittest.TestCase):
 def setUp(self):self.g=Gateway({'limit_mC':30000,'stale_seconds':.3})
 def test_fragmented(self):
  b=frame(0,25000)
  for x in b:self.g.feed(bytes([x]),1)
  self.assertEqual(self.g.accepted,1);self.assertTrue(self.g.health(1.1)['healthy'])
 def test_corrupt_counter_units(self):
  b=frame(0,25000);b=b[:-1]+bytes([b[-1]^1]);self.g.feed(b+frame(1,25000),1)
  self.assertEqual(self.g.accepted,1);self.assertEqual(self.g.rejected,1);self.assertEqual(self.g.discarded_bytes,12)
 def test_stale(self):
  self.g.feed(frame(0,25000),1);self.assertFalse(self.g.health(1.31)['healthy'])
 def test_replay(self):
  self.g.feed(frame(2,25000)*2,1);self.assertEqual(self.g.accepted,1);self.assertEqual(self.g.rejected,1)
 def test_alarm(self):
  self.g.feed(frame(1,31000),1);self.assertTrue(self.g.health(1)['alarm'])
 def test_wrap(self):
  self.g.feed(frame(65535,25000)+frame(0,25001),1);self.assertEqual(self.g.accepted,2)
 def test_invalid_config(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'c.json';atomic_json(f,{'schema':1,'limit_mC':999999,'stale_seconds':.1})
   with self.assertRaises(ValueError):config(f)
 def test_process_integration(self):
  with tempfile.TemporaryDirectory() as d:
   source=subprocess.Popen([sys.executable,'src/simulated_mcu.py','--corrupt','--replay'],stdout=subprocess.PIPE)
   sink=subprocess.run([sys.executable,'src/gateway.py','--state',d],stdin=source.stdout,capture_output=True,text=True,timeout=5)
   source.stdout.close();source.wait(timeout=2)
   self.assertEqual(sink.returncode,0,sink.stderr);h=json.loads(sink.stdout);self.assertEqual(h['accepted'],19);self.assertGreater(h['rejected'],0);self.assertEqual(h['transport'],'closed')
if __name__=='__main__':unittest.main()
