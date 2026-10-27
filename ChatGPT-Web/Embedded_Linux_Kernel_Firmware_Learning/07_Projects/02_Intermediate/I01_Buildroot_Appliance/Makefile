CC ?= cc
CFLAGS ?= -std=c11 -O2 -g -Wall -Wextra -Wpedantic -Werror
.PHONY: all test clean
all: build/telemetry-once
build/telemetry-once: src/telemetry_once.c
	mkdir -p build
	$(CC) $(CFLAGS) $< -o $@
test: all
	python3 tests/test_counter.py
clean:
	rm -rf build
