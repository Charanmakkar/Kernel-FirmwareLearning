# Version record

FreeRTOS-Kernel V11.1.0 GCC POSIX port; host GCC 13.3.0; Python 3.12.14; Linux x86-64. STM32 NUCLEO-F446RE physical target source is also supplied and cross-built with GCC ARM 13.2.1; physical execution remains pending.

Accessed official references on 2026-10-27. Host tools observed during authoring: GCC 13.3.0, Python 3.12.14, OpenSSL 3.0.13, Linux host kernel 6.18.55. Host-kernel version is evidence about this environment only; it is not the target kernel for the 6.12 driver labs. Record exact tool output, source revision, configuration hash and command with every new run. Release labels select reproducible exercises and are not claims of current production support.

**STM32 target build evidence:** Complete firmware cross-built and linked with arm-none-eabi GCC 13.2.1, yielding 6296 bytes text, 4 bytes data and 33084 bytes bss in this build. This is a build-size observation, not measured stack high-water usage. Physical flashing, UART framing, watchdog timeout and task stack margins remain pending. See evidence/mcu-build.log and hardware/MCU_PORT.md.
