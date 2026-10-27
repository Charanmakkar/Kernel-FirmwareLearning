import subprocess,time,unittest
class Telemetry(unittest.TestCase):
 def test_lines_and_shutdown(self):
  subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','meta-learning/recipes-apps/telemetry/files/telemetry.c','-o','/tmp/learning-yocto-telemetry'],check=True)
  p=subprocess.Popen(['/tmp/learning-yocto-telemetry'],stdout=subprocess.PIPE,text=True)
  a=p.stdout.readline();b=p.stdout.readline();p.terminate();tail,_=p.communicate(timeout=2)
  self.assertIn('seq=0',a);self.assertIn('seq=1',b);self.assertEqual(p.returncode,0)
if __name__=='__main__':unittest.main()
