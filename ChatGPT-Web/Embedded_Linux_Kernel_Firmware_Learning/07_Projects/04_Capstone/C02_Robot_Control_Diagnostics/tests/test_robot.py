import sys,unittest,math
sys.path.insert(0,'src');from robot import MCU,Robot,command,simulate
class RobotTests(unittest.TestCase):
 def test_start_disabled(self):self.assertEqual(MCU().tick(0),(0,0))
 def test_expiry_boundary(self):
  m=MCU();m.receive(command(0,.5,.5),0);self.assertEqual(m.tick(.199),(.5,.5));self.assertEqual(m.tick(.2),(0,0));self.assertEqual(m.state,'STALE')
 def test_duplicate_cannot_refresh(self):
  m=MCU();f=command(1,.3,.3);m.receive(f,0);self.assertFalse(m.receive(f,.15));self.assertEqual(m.tick(.2),(0,0))
 def test_bad_crc(self):
  m=MCU();f=command(0,.3,.3);self.assertFalse(m.receive(f[:-1]+bytes([f[-1]^1]),0));self.assertEqual(m.tick(0),(0,0))
 def test_estop_latched(self):
  m=MCU();m.receive(command(0,.5,.5),0);m.emergency_stop();self.assertFalse(m.receive(command(1,.5,.5),.01));self.assertEqual(m.tick(.01),(0,0));m.rearm();self.assertEqual(m.tick(.02),(0,0));self.assertTrue(m.receive(command(1,.1,.1),.03))
 def test_invalid_speed(self):
  for x in [2,float('nan'),float('inf')]:
   with self.assertRaises(ValueError):command(0,x,0)
 def test_wrap(self):
  m=MCU();self.assertTrue(m.receive(command(65535,.1,.1),0));self.assertTrue(m.receive(command(0,.2,.2),.1))
 def test_integrated_stop(self):
  rows=simulate();stale=[r for r in rows if r['state']=='STALE'];self.assertLessEqual(stale[0]['t'],1.15+1e-9);self.assertTrue(all(r['left']==0 and r['right']==0 for r in stale));self.assertAlmostEqual(rows[-1]['x'],.345,places=6)
 def test_turn(self):
  r=Robot();r.step(-.2,.2,1);self.assertAlmostEqual(r.yaw,1);self.assertEqual(r.x,0)
if __name__=='__main__':unittest.main()
