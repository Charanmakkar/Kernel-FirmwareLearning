"""Package only the separate reader; never rebuild the original course ZIP."""
from pathlib import Path
import hashlib
import json
import zipfile

APP=Path(__file__).resolve().parent
SKIP={'.qa','__pycache__','.git'}
target=APP.parent/'Learning_Reader_Offline.zip'
files=sorted(p for p in APP.rglob('*') if p.is_file() and not any(part in SKIP for part in p.relative_to(APP).parts))
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for file in files:
        archive.write(file,file.relative_to(APP.parent).as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
print(json.dumps({'zip':str(target),'files':len(files),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
