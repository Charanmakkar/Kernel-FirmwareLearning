CC ?= cc
CFLAGS ?= -std=c11 -O2 -g -Wall -Wextra -Wpedantic -Werror
.PHONY: all test clean
all: build/uart_frame
build/uart_frame: src/uart_frame.c src/util.c include/util.h
	mkdir -p build
	$(CC) -Iinclude $(CFLAGS) src/uart_frame.c src/util.c -o $@
test: all
	python3 tests/test_pty.py
clean:
	rm -rf build
