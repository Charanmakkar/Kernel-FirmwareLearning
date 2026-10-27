CC ?= cc
CFLAGS ?= -std=c11 -O2 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror
CPPFLAGS += -Iinclude
.PHONY: all test clean
all: build/test_util build/demo
build:
	mkdir -p build
build/test_util: src/embedded_util.c tests/test_util.c include/embedded_util.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) src/embedded_util.c tests/test_util.c -o $@
build/demo: src/embedded_util.c src/demo.c include/embedded_util.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) src/embedded_util.c src/demo.c -o $@
test: all
	./build/test_util
	./build/demo
clean:
	rm -f build/test_util build/demo
