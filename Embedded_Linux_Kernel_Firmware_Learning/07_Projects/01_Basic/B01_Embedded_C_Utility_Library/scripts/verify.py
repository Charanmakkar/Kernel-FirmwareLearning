"""Portable compile/test runner. It records actual subprocess results, not estimates."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--cc', default=os.environ.get('CC', 'clang'))
parser.add_argument('--sanitize', action='store_true')
args = parser.parse_args()
build = root / 'build' / ('sanitize' if args.sanitize else 'normal')
build.mkdir(parents=True, exist_ok=True)
record = {'host': platform.platform(), 'python': sys.version, 'sanitizers_requested': args.sanitize,
          'commands': [], 'source_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(root.rglob('*')) if p.is_file() and p.suffix in ['.c', '.h']}}

def run(command):
    proc = subprocess.run(command, cwd=root, capture_output=True, text=True)
    record['commands'].append({'argv': [str(x) for x in command], 'returncode': proc.returncode,
                              'stdout': proc.stdout, 'stderr': proc.stderr})
    if proc.returncode != 0:
        raise RuntimeError('Command failed: ' + ' '.join(str(x) for x in command))
    return proc.stdout

try:
    run([args.cc, '--version'])
    flags = ['-std=c11', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wshadow', '-Werror',
             '-g', '-O1' if args.sanitize else '-O2', '-Iinclude']
    if args.sanitize:
        flags += ['-fsanitize=address,undefined', '-fno-sanitize-recover=all', '-fno-omit-frame-pointer']
    suffix = '.exe' if os.name == 'nt' else ''
    test = build / ('test_util' + suffix)
    demo = build / ('demo' + suffix)
    run([args.cc, *flags, 'src/embedded_util.c', 'tests/test_util.c', '-o', str(test)])
    run([args.cc, *flags, 'src/embedded_util.c', 'src/demo.c', '-o', str(demo)])
    print(run([str(test)]), end='')
    actual = run([str(demo)])
    if actual != 'type=7 payload=3 frame=11\n':
        raise RuntimeError('Demo output differs from contract: ' + repr(actual))
    print(actual, end='')
    record['result'] = 'passed'
except (OSError, RuntimeError) as error:
    record['result'] = 'failed'
    record['error'] = str(error)
finally:
    evidence = root / 'evidence' / ('sanitize.json' if args.sanitize else 'host.json')
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print('Evidence:', evidence)
if record['result'] != 'passed':
    sys.exit(1)
