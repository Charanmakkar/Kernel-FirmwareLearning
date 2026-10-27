#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_dir"
cross_prefix=${CROSS_COMPILE:-aarch64-linux-gnu-}
emulator=${QEMU_AARCH64:-qemu-aarch64}
command -v "$emulator" >/dev/null
command -v "${cross_prefix}gcc" >/dev/null
make cross CROSS_COMPILE="$cross_prefix"
file build/target_sum_aarch64
"${cross_prefix}readelf" -h build/target_sum_aarch64
target_sysroot=${TARGET_SYSROOT:-$("${cross_prefix}gcc" -print-sysroot)}
if [ "$target_sysroot" = / ]; then target_sysroot=/usr/aarch64-linux-gnu; fi
"$emulator" ./build/target_sum_aarch64_static 1000000
"$emulator" -L "$target_sysroot" ./build/target_sum_aarch64 1000000
