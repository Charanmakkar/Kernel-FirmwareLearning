#!/bin/sh
set -eu
mkdir -p third_party
if [ ! -d third_party/FreeRTOS-Kernel ]; then
 git clone --depth 1 --branch V11.1.0 https://github.com/FreeRTOS/FreeRTOS-Kernel.git third_party/FreeRTOS-Kernel
fi
test "$(git -C third_party/FreeRTOS-Kernel describe --tags --exact-match)" = V11.1.0
