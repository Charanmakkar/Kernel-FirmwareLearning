#!/usr/bin/env python3
import argparse,binascii,struct,sys,time

def frame(seq,value):
    b=b'TL\x01\x01'+struct.pack('>Hi',seq&65535,value)
    return b+struct.pack('>H',binascii.crc_hqx(b,0xffff))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--count',type=int,default=20);p.add_argument('--corrupt',action='store_true');p.add_argument('--replay',action='store_true');a=p.parse_args()
    for i in range(a.count):
        b=frame(i,25000+i*10)
        if a.corrupt and i==5:b=b[:-1]+bytes([b[-1]^1])
        sys.stdout.buffer.write(b);sys.stdout.buffer.flush()
        if a.replay and i==7:sys.stdout.buffer.write(b);sys.stdout.buffer.flush()
        time.sleep(.02)
