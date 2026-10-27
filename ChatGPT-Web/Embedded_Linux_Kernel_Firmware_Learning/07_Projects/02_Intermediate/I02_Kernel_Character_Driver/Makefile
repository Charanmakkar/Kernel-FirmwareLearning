ifneq ($(KERNELRELEASE),)
obj-m := learn_fifo.o
learn_fifo-y := src/learn_fifo.o
else
KDIR ?= /lib/modules/$(shell uname -r)/build
CC ?= cc
.PHONY: all module client clean
all: client module
module:
	$(MAKE) -C $(KDIR) M=$(CURDIR) modules
client: build/fifo_client build/test_faults
build/fifo_client: src/fifo_client.c
	mkdir -p build
	$(CC) -std=c11 -Og -g -Wall -Wextra -Wpedantic -Werror $< -o $@
build/test_faults: tests/test_faults.c
	mkdir -p build
	$(CC) -std=c11 -Og -g -Wall -Wextra -Wpedantic -Werror $< -o $@
clean:
	rm -rf build
	$(MAKE) -C $(KDIR) M=$(CURDIR) clean
endif
