import json, pathlib, subprocess, tempfile
exe=str(pathlib.Path('build/inspect').resolve())
p=subprocess.run([exe,'self'],capture_output=True,text=True,check=True)
d=json.loads(p.stdout);assert d['threads']>=1 and d['user_ticks']>=0
for pid in ['-1','0','xyz','9999999999999999999999999']:
    assert subprocess.run([exe,pid],capture_output=True).returncode==2
with tempfile.TemporaryDirectory() as tmp:
    p=pathlib.Path(tmp)/'123';p.mkdir();(p/'fd').mkdir()
    for n in ['0','1','2']:(p/'fd'/n).touch()
    (p/'status').write_text('Name:\ta "worker"\nState:\tS (sleeping)\nThreads:\t2\nVmRSS:\t400 kB\n')
    # field 3 state, fields 4..13 ten numbers, 14/15 user/system.
    (p/'stat').write_text('123 (worker ) with spaces) S '+' '.join(['0']*10)+' 42 7 0\n')
    d=json.loads(subprocess.check_output([exe,'--root',tmp,'123']))
    assert d['user_ticks']==42 and d['system_ticks']==7 and d['open_fds']==3
    assert d['rss_kib']==400 and '"worker"' in d['name']
    (p/'stat').write_text('broken\n')
    assert subprocess.run([exe,'--root',tmp,'123'],capture_output=True).returncode==1
    (p/'status').write_text('Threads:\tbad\n')
    assert subprocess.run([exe,'--root',tmp,'123'],capture_output=True).returncode==1
    assert subprocess.run([exe,'--root',tmp,'124'],capture_output=True).returncode==1
print('PASS live proc; PID rejection; quoted/spaced comm; counters; malformed and disappearing proc entries')
