#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
work=${1:?Usage: setup.sh ABSOLUTE_EMPTY_BUILD_PARENT}
mkdir -p "$work"
case "$work" in /*) ;; *) echo 'Use an absolute path' >&2; exit 2;; esac
if [ ! -d "$work/poky/.git" ]; then
 git clone --branch yocto-5.0.9 --depth 1 https://git.yoctoproject.org/poky "$work/poky"
fi
cd "$work/poky"
test "$(git describe --tags --exact-match)" = yocto-5.0.9
# The environment init script is sourced in a supported bash shell below.
export LEARNING_LAYER="$here/meta-learning" LEARNING_CONF="$here/config/local.conf.append"
bash -c '. ./oe-init-build-env build; bitbake-layers add-layer "$LEARNING_LAYER"; cat "$LEARNING_CONF" >> conf/local.conf; bitbake learning-image'
