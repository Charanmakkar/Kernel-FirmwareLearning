#!/bin/sh
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
test_build_dir=$(mktemp -d)
trap 'rm -rf "$test_build_dir"' EXIT HUP INT TERM
for name in coding_reference posix_reference streaming_reference parser_repair; do
    "${CC:-cc}" -std=c11 -Wall -Wextra -Werror -pedantic "$script_dir/$name.c" -o "$test_build_dir/$name"
    "$test_build_dir/$name"
done
