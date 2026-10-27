CC ?= cc
CFLAGS ?= -std=c11 -O2 -g -Wall -Wextra -Wpedantic -Werror
CPPFLAGS += -Iinclude
.PHONY: all test sanitize clean
all: build/test_util
build/test_util: src/util.c tests/test_util.c include/util.h
	mkdir -p build
	$(CC) $(CPPFLAGS) $(CFLAGS) src/util.c tests/test_util.c -o $@
test: all
	./build/test_util
sanitize:
	mkdir -p build
	$(CC) $(CPPFLAGS) -std=c11 -g -O1 -Wall -Wextra -Werror -fsanitize=address,undefined -fno-omit-frame-pointer src/util.c tests/test_util.c -o build/test_sanitize
	./build/test_sanitize
clean:
	rm -rf build
