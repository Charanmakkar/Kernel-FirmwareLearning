#!/usr/bin/env python3
"""Portable user-space wakeup experiment. Not a real-time guarantee."""
import argparse,csv,json,multiprocessing as mp,os,platform,time,statistics
from pathlib import Path

def load(stop):
    x=1
    while not stop.is_set():
        for _ in range(10000):x=(x*1103515245+12345)&0x7fffffff

def sample(n,period,absolute):
    start=time.monotonic_ns();rows=[]
    for i in range(1,n+1):
        deadline=start+i*period
        if absolute:
            remaining=deadline-time.monotonic_ns()
            if remaining>0:time.sleep(remaining/1e9)
        else:time.sleep(period/1e9)
        now=time.monotonic_ns()
        rows.append({'sample':i,'deadline_ns':deadline,'actual_ns':now,'lateness_us':max(0,now-deadline)/1000})
    return rows

def stats(rows):
    x=sorted(r['lateness_us'] for r in rows)
    return {'n':len(x),'median_us':statistics.median(x),'p99_us':x[min(len(x)-1,int(.99*len(x)))],'max_us':max(x),'meaning':'cumulative schedule lateness'}

def experiment(out,n=200,period=2000000,loaded=False):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    cpus=sorted(os.sched_getaffinity(0)) if hasattr(os,'sched_getaffinity') else []
    original=set(cpus)
    if cpus:os.sched_setaffinity(0,{cpus[0]})
    stop=mp.Event();p=None
    if loaded:p=mp.Process(target=load,args=(stop,));p.start()
    try:
        results={}
        for name,absolute in [('relative_sleep',False),('absolute_deadline',True)]:
            rows=sample(n,period,absolute);results[name]=stats(rows)
            with (out/(name+'.csv')).open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
        results.update(environment={'kernel':platform.release(),'python':platform.python_version(),'cpu_affinity':cpus[:1],'load_process':loaded,'period_ns':period},caveat='Small host sample, relative sleep drift and absolute schedule lateness are different policies; no worst-case bound.')
        (out/'summary.json').write_text(json.dumps(results,indent=2)+'\n');return results
    finally:
        if p:stop.set();p.join(timeout=2)
        if original:os.sched_setaffinity(0,original)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',default='evidence/run');a.add_argument('--samples',type=int,default=200);a.add_argument('--period-us',type=int,default=2000);a.add_argument('--load',action='store_true');x=a.parse_args()
    if x.samples<10 or x.period_us<100:a.error('use >=10 samples and >=100 us')
    print(json.dumps(experiment(x.out,x.samples,x.period_us*1000,x.load),indent=2))
