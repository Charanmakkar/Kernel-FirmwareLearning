#!/usr/bin/env python3
"""Optional synthetic diagnostics experiment; never commands motion."""
import argparse,json,math,random,resource,time,tracemalloc
from pathlib import Path

def data(seed,n):
    r=random.Random(seed);out=[]
    for i in range(n):
        label=int(i%4==0);expected=r.uniform(.1,.8);actual=max(0,expected+r.gauss(-.22 if label else 0,.035));out.append((expected,actual,label))
    return out

def feature(row):return abs(row[0]-row[1])
def metrics(rows,predict):
    tp=fp=tn=fn=0
    for row in rows:
        y=bool(row[2]);p=predict(row)
        tp+=int(p and y);fp+=int(p and not y);tn+=int(not p and not y);fn+=int(not p and y)
    return dict(tp=tp,fp=fp,tn=tn,fn=fn,accuracy=(tp+tn)/len(rows),precision=tp/(tp+fp) if tp+fp else 0,recall=tp/(tp+fn) if tp+fn else 0)

def run(out):
    train=data(100,400);valid=data(200,200);test=data(300,200)
    # Supervised one-feature decision stump: candidate split points come only
    # from training. Validation selects one; final test remains untouched.
    xs=sorted(set(feature(x) for x in train));cuts=[(a+b)/2 for a,b in zip(xs,xs[1:])]
    trained=sorted(cuts,key=lambda t:metrics(train,lambda row:feature(row)>t)['accuracy'],reverse=True)[:15]
    cut=max(trained,key=lambda t:metrics(valid,lambda row:feature(row)>t)['accuracy'])
    model={'model':'one_feature_decision_stump','threshold':cut,'feature':'abs(expected_mps-measured_mps)','seeds':{'train':100,'validation':200,'test':300},'synthetic':True}
    blob=json.dumps(model,sort_keys=True).encode();out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'model.json').write_bytes(blob)
    tracemalloc.start();cpu=time.process_time_ns();t=time.perf_counter_ns()
    for _ in range(1000):
        for row in test:_=feature(row)>cut
    elapsed=time.perf_counter_ns()-t;cpu=time.process_time_ns()-cpu;current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    result={'fixed_threshold_baseline':metrics(test,lambda row:feature(row)>.15),'learned_stump':metrics(test,lambda row:feature(row)>cut),'inferences':200000,'mean_latency_ns':elapsed/200000,'cpu_time_s':cpu/1e9,'traced_peak_bytes':peak,'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'model_bytes':len(blob),'warning':'Synthetic IID datasets from separate seeds; results do not establish real-robot accuracy or bounded latency. Tracemalloc adds overhead; whole process RSS includes Python.'}
    (out/'metrics.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='evidence/ai');a=p.parse_args();print(json.dumps(run(a.out),indent=2))
