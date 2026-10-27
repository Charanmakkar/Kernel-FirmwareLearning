#!/bin/sh
set -eu
# Run only inside a disposable VM with trace-cmd installed and trace access.
# Trace-cmd records and cleans up the selected event configuration.
exec trace-cmd record -o latency-trace.dat -e sched:sched_switch -e sched:sched_wakeup python3 src/latency.py --samples 1000 --load
