#!/usr/bin/env python3
import binascii,struct,sys

def parse(data):
    records=[];bad=0
    while len(data)>=12:
        if data[:4]!=b'TL\x01\x01' or binascii.crc_hqx(data[:10],0xffff)!=int.from_bytes(data[10:12],'big'):
            data=data[1:];bad+=1;continue
        seq,value=struct.unpack('>Hi',data[4:10]);records.append((seq,value));data=data[12:]
    return records,data,bad
if __name__=='__main__':
    import os
    data=b'';errors=0
    while True:
        chunk=os.read(0,4096)
        if not chunk:break
        records,data,bad=parse(data+chunk);errors+=bad
        for seq,value in records:print(f'seq={seq} temperature_mC={value}',flush=True)
    if data or errors:raise SystemExit('Rejected noise or incomplete packet')
