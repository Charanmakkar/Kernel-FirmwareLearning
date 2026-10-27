import unittest

def decode(raw):
    n=(raw>>4)&0xfff
    if n&0x800:n-=4096
    return n*0.0625
class Decode(unittest.TestCase):
    def test_zero(self): self.assertEqual(decode(0),0)
    def test_25(self): self.assertEqual(decode(0x1900),25)
    def test_negative(self): self.assertEqual(decode(0xe700),-25)
    def test_lsb(self): self.assertEqual(decode(0xfff0),-0.0625)
    def test_positive_boundary(self): self.assertEqual(decode(0x7ff0),127.9375)
    def test_negative_boundary(self): self.assertEqual(decode(0x8000),-128)
    def test_wire_order(self): self.assertEqual(int.from_bytes(bytes([0x19,0]),'big'),0x1900)
if __name__=='__main__':unittest.main()
