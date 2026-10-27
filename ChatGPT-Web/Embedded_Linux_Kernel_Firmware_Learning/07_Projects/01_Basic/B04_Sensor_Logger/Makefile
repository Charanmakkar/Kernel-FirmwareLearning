CC ?= cc
CFLAGS ?= -std=c11 -O2 -g -Wall -Wextra -Wpedantic -Werror
.PHONY: all test tsan clean
all: build/logger
build/logger: src/logger.c
	mkdir -p build
	$(CC) $(CFLAGS) -pthread $< -o $@
test: all
	python3 tests/test_logger.py
tsan:
	mkdir -p build
	$(CC) -std=c11 -O1 -g -Wall -Wextra -pthread -fsanitize=thread src/logger.c -o build/logger_tsan
	./build/logger_tsan build/tsan.csv 1000 0
clean:
	rm -rf build
