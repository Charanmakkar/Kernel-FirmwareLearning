import concurrent.futures,json,os,pathlib,subprocess,tempfile
exe=str(pathlib.Path('build/telemetry-once').resolve())
def run(d,crash=None):
    env=os.environ.copy()
    if crash:env['LEARN_CRASH_AT']=crash
    return subprocess.run([exe,d],capture_output=True,text=True,env=env)
with tempfile.TemporaryDirectory() as d:
    assert json.loads(run(d).stdout)['counter']==1
    assert run(d,'after_file_sync').returncode==99
    assert json.loads(run(d).stdout)['counter']==2
    assert run(d,'after_rename').returncode==99
    assert json.loads(run(d).stdout)['counter']==4
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        outputs=list(pool.map(lambda _:run(d),range(40)))
    assert all(p.returncode==0 for p in outputs)
    assert sorted(json.loads(p.stdout)['counter'] for p in outputs)==list(range(5,45))
    f=pathlib.Path(d)/'counter';f.write_text('v1 123 9\n')
    assert run(d).returncode==2 and f.read_text()=='v1 123 9\n'
    f.unlink();f.symlink_to('/dev/null')
    assert run(d).returncode==1
assert run('/nonexistent-learning-directory').returncode==1
print('PASS initial/increment; crash before/after rename; 40 concurrent writers; corruption preserved; symlink/missing-dir rejection')
