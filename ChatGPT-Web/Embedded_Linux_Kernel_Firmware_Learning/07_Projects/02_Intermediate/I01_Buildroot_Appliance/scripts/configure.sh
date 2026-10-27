#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
buildroot_dir=${1:?Pass an extracted official buildroot-2025.02.1 directory}
buildroot_dir=$(CDPATH= cd -- "$buildroot_dir" && pwd)
output_dir=${2:-"$project_dir/buildroot-output"}
mkdir -p "$output_dir"
output_dir=$(CDPATH= cd -- "$output_dir" && pwd)
grep -q '^export BR2_VERSION := 2025.02.1$' "$buildroot_dir/Makefile" || { echo 'Expected Buildroot 2025.02.1' >&2; exit 1; }
make -C "$buildroot_dir" O="$output_dir" BR2_EXTERNAL="$project_dir/br2-external" qemu_x86_64_defconfig
cat "$project_dir/config/learning.fragment" >> "$output_dir/.config"
make -C "$buildroot_dir" O="$output_dir" BR2_EXTERNAL="$project_dir/br2-external" olddefconfig
echo "Configuration ready: $output_dir"
echo "Build with: make -C '$output_dir' -j4"
