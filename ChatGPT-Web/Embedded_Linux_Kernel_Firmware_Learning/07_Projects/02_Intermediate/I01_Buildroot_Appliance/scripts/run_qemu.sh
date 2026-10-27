#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
output_dir=${1:-"$project_dir/buildroot-output"}
state_image=${2:-"$project_dir/learning-data.ext4"}
command -v qemu-system-x86_64 >/dev/null
if [ ! -e "$state_image" ]; then
  truncate -s 64M "$state_image"
  mkfs.ext4 -F "$state_image"
fi
exec qemu-system-x86_64 -machine pc -m 512 -nographic -no-reboot \
  -kernel "$output_dir/images/bzImage" \
  -append 'root=/dev/vda console=ttyS0 ro' \
  -drive "file=$output_dir/images/rootfs.ext2,if=virtio,format=raw,snapshot=on" \
  -drive "file=$state_image,if=virtio,format=raw" -nic none
