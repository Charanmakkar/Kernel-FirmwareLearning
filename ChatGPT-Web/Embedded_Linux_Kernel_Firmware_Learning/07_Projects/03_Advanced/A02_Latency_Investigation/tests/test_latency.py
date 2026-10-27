import sys,tempfile,unittest
sys.path.insert(0,'src')
from latency import sample,stats,experiment
class Latency(unittest.TestCase):
 def test_samples(self):
  rows=sample(10,1000000,True)
  self.assertEqual(len(rows),10);self.assertEqual(stats(rows)['n'],10)
  self.assertEqual(rows[-1]['deadline_ns']-rows[0]['deadline_ns'],9000000)
 def test_recording(self):
  with tempfile.TemporaryDirectory() as d:
   r=experiment(d,10,1000000);self.assertIn('max_us',r['absolute_deadline'])
if __name__=='__main__':unittest.main()
