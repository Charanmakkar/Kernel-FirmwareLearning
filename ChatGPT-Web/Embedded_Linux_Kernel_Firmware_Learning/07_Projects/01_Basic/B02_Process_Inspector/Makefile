CC ?= cc
CFLAGS ?= -std=c11 -O2 -g -Wall -Wextra -Wpedantic -Werror
.PHONY: all test clean
all: build/inspect
build/inspect: src/inspect.c
	mkdir -p build
	$(CC) $(CFLAGS) $< -o $@
test: all
	python3 tests/test_inspect.py
clean:
	rm -rf build
