#!/usr/bin/env python3
import argparse,binascii,json,os,selectors,signal,struct,sys,tempfile,time
from pathlib import Path

def atomic_json(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.new-',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f:json.dump(obj,f,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
        d=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(d)
        finally:os.close(d)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def config(path):
    p=Path(path)
    if not p.exists():atomic_json(p,{'schema':1,'limit_mC':30000,'stale_seconds':.3})
    v=json.loads(p.read_text())
    if set(v)!={'schema','limit_mC','stale_seconds'} or v['schema']!=1 or type(v['limit_mC'])is not int or not -40000<=v['limit_mC']<=125000 or type(v['stale_seconds'])not in (int,float) or not .05<=v['stale_seconds']<=60:raise ValueError('invalid configuration')
    return v

class Gateway:
    def __init__(self,cfg):
        self.cfg=cfg;self.buffer=b'';self.seq=None;self.last=None;self.value=None;self.accepted=0;self.rejected=0;self.discarded_bytes=0
    def feed(self,data,now):
        self.buffer+=data
        while len(self.buffer)>=12:
            f=self.buffer[:12]
            if f[:4]!=b'TL\x01\x01':
                self.buffer=self.buffer[1:];self.discarded_bytes+=1;continue
            if binascii.crc_hqx(f[:10],0xffff)!=int.from_bytes(f[10:12],'big'):
                self.buffer=self.buffer[1:];self.rejected+=1;self.discarded_bytes+=1;continue
            self.buffer=self.buffer[12:];seq,value=struct.unpack('>Hi',f[4:10])
            if not -40000<=value<=125000 or self.seq is not None and not 0<((seq-self.seq)&0xffff)<32768:
                self.rejected+=1;continue
            self.seq=seq;self.value=value;self.last=now;self.accepted+=1
    def health(self,now):
        fresh=self.last is not None and now-self.last<=self.cfg['stale_seconds']
        return {'healthy':fresh,'alarm':fresh and self.value>self.cfg['limit_mC'],'temperature_mC':self.value,'accepted':self.accepted,'rejected':self.rejected,'discarded_bytes':self.discarded_bytes,'last_sequence':self.seq,'source':'simulated-or-serial','age_s':None if self.last is None else round(now-self.last,6)}

def run(directory,fd=0):
    d=Path(directory);g=Gateway(config(d/'config.json'));sel=selectors.DefaultSelector();sel.register(fd,selectors.EVENT_READ)
    stop=False
    def halt(sig,frame):
        nonlocal stop;stop=True
    signal.signal(signal.SIGTERM,halt);signal.signal(signal.SIGINT,halt)
    try:
        while not stop:
            events=sel.select(.05);now=time.monotonic()
            if events:
                data=os.read(fd,4096)
                if not data:break
                g.feed(data,now)
            atomic_json(d/'health.json',g.health(now))
        out=g.health(time.monotonic());out['healthy']=False;out['transport']='closed'
        atomic_json(d/'health.json',out);print(json.dumps(out));return 0
    finally:sel.close()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--state',default='run');a=p.parse_args()
    try:raise SystemExit(run(a.state))
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
