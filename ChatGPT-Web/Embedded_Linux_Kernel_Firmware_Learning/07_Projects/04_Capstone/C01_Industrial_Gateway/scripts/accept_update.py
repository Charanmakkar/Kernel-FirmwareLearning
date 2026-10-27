#!/usr/bin/env python3
"""Integrates gateway acceptance tests with A03 trial-slot confirmation."""
import pathlib,sys,subprocess
advanced=pathlib.Path(__file__).resolve().parents[3]/'03_Advanced'/'A03_Signed_AB_Update'/'src'
sys.path.insert(0,str(advanced));import update
if len(sys.argv)!=3:raise SystemExit('usage: accept_update.py DEVICE_ROOT BUNDLE_DIRECTORY')
root,bundle=sys.argv[1:];update.install(root,bundle);slot=update.boot(root)
r=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'])
if r.returncode:raise SystemExit('Health tests failed; trial remains unconfirmed for rollback')
update.mark_good(root,slot);print('confirmed',slot)
