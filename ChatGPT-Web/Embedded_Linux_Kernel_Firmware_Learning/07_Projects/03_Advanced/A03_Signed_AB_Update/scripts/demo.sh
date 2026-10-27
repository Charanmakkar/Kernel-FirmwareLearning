#!/bin/sh
set -eu
# All private keys are ephemeral local test keys. No key is included in package.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT HUP INT TERM
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out "$work/private.pem"
chmod 600 "$work/private.pem"
openssl pkey -in "$work/private.pem" -pubout -out "$work/public.pem"
printf 'factory image\n' > "$work/v1.bin"
printf 'updated image\n' > "$work/v2.bin"
python3 src/update.py bundle "$work/v1" "$work/v1.bin" 1 "$work/private.pem"
python3 src/update.py bundle "$work/v2" "$work/v2.bin" 2 "$work/private.pem"
python3 src/update.py init "$work/device" "$work/public.pem" "$work/v1"
python3 src/update.py install "$work/device" "$work/v2"
python3 src/update.py boot "$work/device"
python3 src/update.py good "$work/device" B
python3 src/update.py status "$work/device"
