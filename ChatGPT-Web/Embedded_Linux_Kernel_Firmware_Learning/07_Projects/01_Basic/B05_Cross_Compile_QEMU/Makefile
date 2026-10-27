CC ?= cc
CROSS_COMPILE ?= aarch64-linux-gnu-
CFLAGS ?= -std=c11 -Og -g3 -Wall -Wextra -Wpedantic -Werror
.PHONY: all native cross test clean
all: native
native: build/target_sum_native
cross: build/target_sum_aarch64 build/target_sum_aarch64_static
build/target_sum_native: src/target_sum.c
	mkdir -p build
	$(CC) $(CFLAGS) $< -o $@
build/target_sum_aarch64: src/target_sum.c
	mkdir -p build
	$(CROSS_COMPILE)gcc $(CFLAGS) $< -o $@
build/target_sum_aarch64_static: src/target_sum.c
	mkdir -p build
	$(CROSS_COMPILE)gcc $(CFLAGS) -static $< -o $@
test: native
	python3 tests/test_native.py
clean:
	rm -rf build
