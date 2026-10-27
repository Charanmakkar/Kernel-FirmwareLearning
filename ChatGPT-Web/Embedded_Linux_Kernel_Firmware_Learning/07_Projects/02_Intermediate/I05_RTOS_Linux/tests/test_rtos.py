import os,subprocess,tempfile,unittest,sys
sys.path.insert(0,'src')
from receiver import parse
class RTOS(unittest.TestCase):
 def execute(self,stall=False):
  with tempfile.TemporaryDirectory() as d:
   fifo=d+'/uart';os.mkfifo(fifo)
   fd=os.open(fifo,os.O_RDONLY|os.O_NONBLOCK)
   p=subprocess.Popen(['./firmware',fifo]+(['stall'] if stall else []),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   out,err=p.communicate(timeout=5)
   data=b''
   while True:
    part=os.read(fd,4096)
    if not part:break
    data+=part
   os.close(fd)
   return p.returncode,parse(data),err
 def test_samples(self):
  status,(rows,left,bad),err=self.execute()
  self.assertEqual(status,0,err);self.assertEqual(len(rows),20);self.assertEqual([r[0] for r in rows],list(range(20)));self.assertFalse(left);self.assertEqual(bad,0)
 def test_watchdog(self):
  status,(rows,left,bad),err=self.execute(True)
  self.assertEqual(status,1,err);self.assertEqual(len(rows),5)
 def test_resynchronization(self):
  import binascii,struct
  x=b'TL\x01\x01'+struct.pack('>Hi',3,-100)
  x+=struct.pack('>H',binascii.crc_hqx(x,0xffff))
  rows,left,bad=parse(b'noise'+x)
  self.assertEqual(rows,[(3,-100)]);self.assertEqual(bad,5)
 def test_corruption(self):
  rows,left,bad=parse(b'TL\x01\x01'+b'\0'*8)
  self.assertEqual(rows,[]);self.assertGreater(bad,0)
if __name__=='__main__':unittest.main()
