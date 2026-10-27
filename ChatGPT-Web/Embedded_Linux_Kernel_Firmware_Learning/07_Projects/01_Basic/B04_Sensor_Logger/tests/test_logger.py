import csv, pathlib, signal, subprocess, tempfile, time
exe=str(pathlib.Path('build/logger').resolve())
def rows(p):
    with open(p) as f:return list(csv.DictReader(f))
with tempfile.TemporaryDirectory() as d:
    out=pathlib.Path(d)/'samples.csv'
    p=subprocess.run([exe,str(out),'500','0'],capture_output=True,text=True,timeout=5)
    assert p.returncode==0,p.stderr
    r=rows(out);assert len(r)==1000
    for sensor in [0,1]:
        selected=[x for x in r if int(x['sensor'])==sensor]
        assert [int(x['sequence']) for x in selected]==list(range(500))
        assert all(int(x['value'])==sensor*100+int(x['sequence'])%50 for x in selected)
    subprocess.run([exe,str(out),'0'],check=True,capture_output=True);assert len(rows(out))==0
    p=subprocess.Popen([exe,str(out),'100000','1000'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    time.sleep(.04);p.send_signal(signal.SIGTERM);_,err=p.communicate(timeout=3)
    assert p.returncode==0 and b'stop=1' in err,err
    r=rows(out);assert len(r)<200000
    for sensor in [0,1]:assert [int(x['sequence']) for x in r if int(x['sensor'])==sensor]==list(range(sum(int(x['sensor'])==sensor for x in r)))
    p=subprocess.run([exe,'/dev/full','10000','0'],capture_output=True,timeout=3)
    assert p.returncode==1
    assert subprocess.run([exe,str(out),'-1'],capture_output=True).returncode==2
print('PASS 1000 samples no loss/duplicates; per-producer ordering; zero work; SIGTERM drain/join; failed output termination; invalid input')
