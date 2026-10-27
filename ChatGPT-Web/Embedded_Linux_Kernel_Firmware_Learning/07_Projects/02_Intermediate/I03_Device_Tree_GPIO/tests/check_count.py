#!/usr/bin/env python3
"""Target-only count observation; pulse generation stays external."""
import argparse,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('attribute');p.add_argument('--seconds',type=float,default=10);p.add_argument('--expected',type=int,required=True)
a=p.parse_args();f=Path(a.attribute);before=int(f.read_text());time.sleep(a.seconds);after=int(f.read_text())
assert after-before==a.expected,(before,after,a.expected)
print('PASS edges',after-before)
