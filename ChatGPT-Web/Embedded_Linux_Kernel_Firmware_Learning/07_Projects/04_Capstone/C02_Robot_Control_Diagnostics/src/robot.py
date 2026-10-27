#!/usr/bin/env python3
"""Deterministic differential-drive learning simulation; no physical outputs."""
import binascii,json,math,struct
from dataclasses import dataclass,field

def command(seq,left,right):
    # fixed-width versioned binary command, velocities encoded in mm/s
    if not all(math.isfinite(x) and abs(x)<=1 for x in [left,right]):raise ValueError('speed outside +/-1 m/s')
    body=b'RB'+bytes([1,1])+struct.pack('>Hhh',seq&65535,round(left*1000),round(right*1000))
    return body+struct.pack('>H',binascii.crc_hqx(body,0xffff))

@dataclass
class MCU:
    ttl:float=.2
    seq:int|None=None
    last:float|None=None
    demand:tuple=(0.,0.)
    estop:bool=False
    bad:int=0
    state:str='DISARMED'
    def receive(self,frame,now):
        if len(frame)!=12 or frame[:4]!=b'RB\x01\x01' or binascii.crc_hqx(frame[:10],0xffff)!=int.from_bytes(frame[10:12],'big'):
            self.bad+=1;return False
        seq,left,right=struct.unpack('>Hhh',frame[4:10])
        if abs(left)>1000 or abs(right)>1000 or self.seq is not None and not 0<((seq-self.seq)&65535)<32768:
            self.bad+=1;return False
        if self.estop:return False
        self.seq=seq;self.last=now;self.demand=(left/1000,right/1000);self.state='ACTIVE';return True
    def emergency_stop(self):
        self.estop=True;self.demand=(0.,0.);self.state='ESTOP'
    def rearm(self):
        # Local deliberate rearm only; no network command invokes this method.
        self.estop=False;self.last=None;self.demand=(0.,0.);self.state='DISARMED'
    def tick(self,now):
        if self.estop:self.state='ESTOP';return(0.,0.)
        if self.last is None:self.state='DISARMED';return(0.,0.)
        if now-self.last>=self.ttl-1e-9:self.state='STALE';self.demand=(0.,0.);return(0.,0.)
        return self.demand

@dataclass
class Robot:
    track:float=.4
    x:float=0.
    y:float=0.
    yaw:float=0.
    def step(self,left,right,dt):
        v=(left+right)/2;w=(right-left)/self.track
        self.x+=v*math.cos(self.yaw+w*dt/2)*dt
        self.y+=v*math.sin(self.yaw+w*dt/2)*dt
        self.yaw+=w*dt

def simulate(drop_after=1.,duration=2.):
    m=MCU();r=Robot();rows=[];seq=0
    for n in range(round(duration/.01)+1):
        now=n*.01
        if n%5==0 and now<drop_after:
            m.receive(command(seq,.3,.3),now);seq+=1
        left,right=m.tick(now);r.step(left,right,.01)
        rows.append({'t':now,'x':r.x,'y':r.y,'left':left,'right':right,'state':m.state})
    return rows
if __name__=='__main__':
    import argparse,csv,pathlib
    p=argparse.ArgumentParser();p.add_argument('--output',default='evidence/robot.csv');a=p.parse_args();rows=simulate()
    pathlib.Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    with open(a.output,'w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    print(json.dumps({'frames':len(rows),'final_x_m':rows[-1]['x'],'first_stale_s':next(x['t'] for x in rows if x['state']=='STALE')}))
