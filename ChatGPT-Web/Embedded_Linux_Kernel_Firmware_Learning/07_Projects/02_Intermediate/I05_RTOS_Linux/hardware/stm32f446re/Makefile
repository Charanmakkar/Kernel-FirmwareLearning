FREERTOS ?= ../../third_party/FreeRTOS-Kernel
CROSS ?= arm-none-eabi-
CC := $(CROSS)gcc
PORT := $(FREERTOS)/portable/GCC/ARM_CM4F
CPPFLAGS += -I. -I../../src -I$(FREERTOS)/include -I$(PORT)
CFLAGS += -std=gnu11 -Os -g3 -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -ffreestanding -fno-builtin -ffunction-sections -fdata-sections -Wall -Wextra
KERNEL := $(FREERTOS)/tasks.c $(FREERTOS)/queue.c $(FREERTOS)/list.c $(FREERTOS)/portable/MemMang/heap_4.c $(PORT)/port.c
all: firmware.elf firmware.bin
firmware.elf: main.c startup.c memory.c FreeRTOSConfig.h link.ld ../../src/protocol.h
	$(CC) $(CPPFLAGS) $(CFLAGS) main.c startup.c memory.c $(KERNEL) -Tlink.ld -nostdlib -Wl,--gc-sections,-Map=firmware.map -lgcc -o $@
	$(CROSS)size $@
firmware.bin: firmware.elf
	$(CROSS)objcopy -O binary $< $@
clean:
	rm -f firmware.elf firmware.bin firmware.map
