FREERTOS ?= third_party/FreeRTOS-Kernel
PORT := $(FREERTOS)/portable/ThirdParty/GCC/Posix
CC ?= gcc
CPPFLAGS += -Iconfig -Isrc -I$(FREERTOS)/include -I$(PORT)
CFLAGS += -std=gnu11 -O2 -g -Wall -Wextra
KERNEL := $(FREERTOS)/tasks.c $(FREERTOS)/queue.c $(FREERTOS)/list.c $(FREERTOS)/portable/MemMang/heap_4.c $(PORT)/port.c $(PORT)/utils/wait_for_event.c
all: firmware
firmware: src/firmware_posix.c src/protocol.h config/FreeRTOSConfig.h
	$(CC) $(CPPFLAGS) $(CFLAGS) src/firmware_posix.c $(KERNEL) -pthread -o $@
clean:
	rm -f firmware
