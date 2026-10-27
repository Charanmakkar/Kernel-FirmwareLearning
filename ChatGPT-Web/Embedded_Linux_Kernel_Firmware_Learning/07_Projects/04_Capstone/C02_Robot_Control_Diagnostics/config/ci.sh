#!/bin/sh
set -eu
python3 -m unittest discover -s tests -v
python3 src/robot.py --output evidence/robot.csv
python3 src/anomaly.py --out evidence/ai
