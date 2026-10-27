#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_dir"
[ "$(id -u)" -eq 0 ] || { echo 'Run inside a disposable guest as root' >&2; exit 1; }
insmod ./learn_fifo.ko
trap 'rmmod learn_fifo' EXIT INT TERM
./build/fifo_client /dev/learn_fifo hello
python3 tests/test_device.py
./build/test_faults
dmesg | tail -n 20
