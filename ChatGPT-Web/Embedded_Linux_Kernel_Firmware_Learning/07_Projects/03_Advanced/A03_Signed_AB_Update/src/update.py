#!/usr/bin/env python3
"""Signed A/B file-slot simulator; never writes a block device."""
import argparse,contextlib,fcntl,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
MAX_IMAGE=8*1024*1024

def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('duplicate JSON key')
        out[k]=v
    return out

def readjson(data):return json.loads(data,object_pairs_hook=unique)

def atomic(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.new-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
        d=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(d)
        finally:os.close(d)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def save(root,s):atomic(Path(root)/'state.json',(json.dumps(s,sort_keys=True)+'\n').encode())

def state(root):
    s=readjson((Path(root)/'state.json').read_bytes())
    if s['active'] not in ('A','B') or s['pending'] not in ('A','B',None) or s['attempts'] not in (0,1,2):raise ValueError('invalid state')
    return s

@contextlib.contextmanager
def lock(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    with (root/'.lock').open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX);yield

def verified(bundle,pub):
    b=Path(bundle)
    for n,cap in [('manifest.json',4096),('manifest.sig',4096),('image.bin',MAX_IMAGE)]:
        q=b/n
        if q.is_symlink() or not q.is_file() or q.stat().st_size>cap:raise ValueError('invalid bundle file')
    # Snapshot authenticated bytes into a private directory to avoid re-opening a
    # different payload after verification. Local trusted directory is assumed.
    raw=(b/'manifest.json').read_bytes();sig=(b/'manifest.sig').read_bytes();image=(b/'image.bin').read_bytes()
    with tempfile.TemporaryDirectory() as d:
        m=Path(d)/'m';sg=Path(d)/'s';m.write_bytes(raw);sg.write_bytes(sig)
        r=subprocess.run(['openssl','dgst','-sha256','-verify',str(pub),'-signature',str(sg),str(m)],capture_output=True)
        if r.returncode:raise ValueError('signature rejected')
    m=readjson(raw)
    if set(m)!={'format','compatible','version','sha256'} or m['format']!=1 or m['compatible']!='learning-x86_64' or type(m['version'])is not int or m['version']<1:raise ValueError('manifest rejected')
    if hashlib.sha256(image).hexdigest()!=m['sha256']:raise ValueError('payload digest rejected')
    return m,{'manifest.json':raw,'manifest.sig':sig,'image.bin':image}

def write_slot(root,slot,data):
    d=Path(root)/'slots'/slot;d.mkdir(parents=True,exist_ok=True)
    for name,raw in data.items():atomic(d/name,raw)

def initialize(root,pub,bundle):
    root=Path(root)
    with lock(root):
        if (root/'state.json').exists():raise ValueError('already initialized')
        m,data=verified(bundle,pub);atomic(root/'trust.pem',Path(pub).read_bytes());write_slot(root,'A',data)
        save(root,dict(active='A',pending=None,attempts=0,booted='A',min_version=m['version']))

def install(root,bundle,fail_before_commit=False):
    root=Path(root)
    with lock(root):
        s=state(root)
        if s['pending']:raise ValueError('pending update must finish or roll back')
        m,data=verified(bundle,root/'trust.pem')
        if m['version']<=s['min_version']:raise ValueError('rollback version rejected')
        slot='B' if s['active']=='A' else 'A';write_slot(root,slot,data)
        verified(root/'slots'/slot,root/'trust.pem')
        if fail_before_commit:raise InterruptedError('injected interruption before metadata commit')
        s.update(pending=slot,attempts=0);save(root,s);return slot

def boot(root):
    root=Path(root)
    with lock(root):
        s=state(root);slot=s['active']
        if s['pending']:
            if s['attempts']<2:
                slot=s['pending'];s['attempts']+=1
            else:s.update(pending=None,attempts=0)
        try:verified(root/'slots'/slot,root/'trust.pem')
        except ValueError:
            if slot==s['active']:raise
            slot=s['active'];s.update(pending=None,attempts=0)
            verified(root/'slots'/slot,root/'trust.pem')
        s['booted']=slot;save(root,s);return slot

def mark_good(root,slot):
    root=Path(root)
    with lock(root):
        s=state(root)
        if slot!=s['pending'] or slot!=s['booted'] or s['attempts']<1:raise ValueError('slot not trial-booted')
        m,_=verified(root/'slots'/slot,root/'trust.pem')
        s.update(active=slot,pending=None,attempts=0,min_version=m['version']);save(root,s)

def bundle(directory,payload,version,key):
    b=Path(directory);b.mkdir(parents=True,exist_ok=False);data=Path(payload).read_bytes()
    if not data or len(data)>MAX_IMAGE or version<1:raise ValueError('invalid image or version')
    (b/'image.bin').write_bytes(data)
    (b/'manifest.json').write_text(json.dumps(dict(format=1,compatible='learning-x86_64',version=version,sha256=hashlib.sha256(data).hexdigest()),sort_keys=True,separators=(',',':'))+'\n')
    subprocess.run(['openssl','dgst','-sha256','-sign',str(key),'-out',str(b/'manifest.sig'),str(b/'manifest.json')],check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('bundle');a.add_argument('directory');a.add_argument('payload');a.add_argument('version',type=int);a.add_argument('key')
    a=sub.add_parser('init');a.add_argument('root');a.add_argument('pub');a.add_argument('bundle')
    a=sub.add_parser('install');a.add_argument('root');a.add_argument('bundle')
    a=sub.add_parser('boot');a.add_argument('root')
    a=sub.add_parser('good');a.add_argument('root');a.add_argument('slot',choices=['A','B'])
    a=sub.add_parser('status');a.add_argument('root')
    a=p.parse_args()
    try:
        if a.cmd=='bundle':bundle(a.directory,a.payload,a.version,a.key)
        elif a.cmd=='init':initialize(a.root,a.pub,a.bundle)
        elif a.cmd=='install':print(install(a.root,a.bundle))
        elif a.cmd=='boot':print(boot(a.root))
        elif a.cmd=='good':mark_good(a.root,a.slot)
        else:print(json.dumps(state(a.root),indent=2))
    except (ValueError,OSError,KeyError) as e:p.exit(1,str(e)+'\n')
