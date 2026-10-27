# STM32 NUCLEO F446RE target

## Scope and delivered files

The `stm32f446re` directory contains a complete small physical-target firmware: reset/vector code, FLASH/SRAM linker map, a minimal C runtime memory implementation, direct register board initialization, the FreeRTOS V11.1.0 Cortex M4F port configuration, sensor/serial/supervisor tasks and a Makefile. It transmits the same 12-byte TL packets as the tested POSIX build. Samples are synthetic; an ADC sensor is a separate extension.

## Board and interface

Use NUCLEO F446RE, MB1136 board family. Program and power through the onboard ST LINK USB interface. USART2 PA2 TX and PA3 RX connect to the ST LINK virtual COM interface with the default documented bridge configuration, normally SB13/SB14 on and SB62/SB63 off. Verify the exact board revision and schematic before changing any solder bridge. No external UART cable is needed when the default ST LINK link is intact. No motors or external power peripherals are connected.

The firmware selects internal HSI at 16 MHz, no PLL, APB1 and APB2 undivided, USART2 at nominal 115200 8N1, GPIOA alternate function 7 on PA2/PA3, and 1 kHz RTOS ticks. The independent watchdog uses LSI and a nominal approximately 2 s setting; actual timeout depends on LSI tolerance and must be measured. The supervisor feeds it only when both tasks have progressed within the 200 ms software policy. Assert, stack failure, allocation failure or stale progress stops feeding. No application code calls an RTOS API from a UART ISR because this minimum transmits through bounded task-level polling.

## Build and flash

From the project root fetch FreeRTOS with `sh scripts/fetch.sh`. Install GNU Arm Embedded GCC and newlib headers through a supported distribution or official Arm toolchain. Then:

```sh
cd hardware/stm32f446re
make
arm-none-eabi-size firmware.elf
```

Use `FREERTOS=/absolute/FreeRTOS-Kernel` and `CROSS=/absolute/bin/arm-none-eabi-` when required. Source is built for Cortex M4, Thumb, FPv4 single precision and hard-float ABI. The firmware deliberately avoids standard libc and links its small memory functions plus compiler support. Keep these ABI flags coherent across all object files.

Flash only the selected isolated Nucleo with STM32CubeProgrammer or OpenOCD. Example with OpenOCD installed:

```sh
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c 'program firmware.elf verify reset exit'
```

This command writes the board flash and is supplied for the owner to run on the correct board; it was not run during authoring. On Linux configure the observed VCP device, normally `/dev/ttyACM0`:

```sh
stty -F /dev/ttyACM0 115200 raw -echo
python3 ../../src/receiver.py < /dev/ttyACM0
```

Stop the reader with Ctrl C. To debug, start OpenOCD, load the ELF in `arm-none-eabi-gdb`, connect `target extended-remote localhost:3333`, reset halt and break at main. The watchdog continues according to debugger freeze configuration; a halted debugger is not proof of a live timeout failure.

## Hardware acceptance

Verify the reset vector and SRAM bounds; receive at least 1000 consecutive CRC-valid frames; measure the nominal 50 ms sample interval; record task stack high-water marks under maximum load; force a task stall and measure watchdog reset timing; verify that reset reasons and sequence restart are correctly handled by the Linux session policy. Build an injected-stall image using `make clean` then `make CPPFLAGS='-DINJECT_STALL -I. -I../../src -I../../third_party/FreeRTOS-Kernel/include -I../../third_party/FreeRTOS-Kernel/portable/GCC/ARM_CM4F'`. After the test, rebuild without the macro. A separate session handshake is needed for continuous host acceptance across MCU resets.

## Actual status

Cross-compiled and linked successfully against FreeRTOS V11.1.0 using arm-none-eabi GCC 13.2.1. The ELF and binary are build outputs; no board was attached, flashed or measured. BSS size includes the configured heap; it is not peak runtime consumption. The host simulator separately passed its integration tests.

Primary references accessed 2026-10-27: ST STM32F446RE product/datasheet https://www.st.com/en/microcontrollers-microprocessors/stm32f446re.html ; RM0390 https://www.st.com/st-web-ui/static/active/en/resource/technical/document/reference_manual/DM00135183.pdf ; UM1724 https://www.st.com/resource/en/user_manual/dm00105823.pdf ; FreeRTOS Cortex M guidance https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4 .
