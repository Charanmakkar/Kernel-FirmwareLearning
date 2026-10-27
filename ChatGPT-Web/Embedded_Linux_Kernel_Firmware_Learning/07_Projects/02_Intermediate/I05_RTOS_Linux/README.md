# I05 RTOS telemetry connected to Linux

## Purpose and learning outcome

Execute a real RTOS scheduler on the supported POSIX port, transfer bounded records between tasks, serialize framed telemetry, and detect a stalled task through supervised progress. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 20–30 hours for simulator path; allow remediation time when a prerequisite fails. Relevant learning modules: M03 M07 M12 M13 M17. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Build B03/B04, explain CRC framing, queues, task priorities and the difference between elapsed time and a deadline guarantee.

## Minimum scope and version boundary

FreeRTOS-Kernel V11.1.0 GCC POSIX port; host GCC 13.3.0; Python 3.12.14; Linux x86-64. STM32 NUCLEO-F446RE physical target source is also supplied and cross-built with GCC ARM 13.2.1; physical execution remains pending.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

A periodic sensor task creates one sample every 50 RTOS ticks at 1 kHz. A four-element FreeRTOS queue transfers ownership by value to a serial task. Only the serial task writes the host transport. A higher-priority supervisor checks both producer and transmitter progress every 20 ticks; after 200 ticks without progress it ends the simulation with failure. The serial task implements partial writes, EAGAIN, EINTR and a bounded transmission timeout. The receiver verifies version, kind and CRC before decoding signed millidegrees Celsius.

## Build run debug and cleanup

1. Use a Linux x86-64 user account with GCC, Make, Python 3.12 and pthread support. No board purchase is needed for this first path.
2. Fetch exact FreeRTOS tag `V11.1.0` using `sh scripts/fetch.sh`. Its license remains with the fetched source; the learning package does not redistribute the kernel.
3. Run `make`. To use an existing checkout: `make FREERTOS=/absolute/FreeRTOS-Kernel`. The authoring build used GCC 13.3.0 and the real V11.1.0 source archive.
4. Run `python3 -m unittest discover -s tests -v`. Tests create temporary FIFOs, start a receiver before opening the transmitter, run the real RTOS executable and decode its binary output.
5. Manual demonstration: in one terminal `mkfifo /tmp/learning-uart` then `cat /tmp/learning-uart | python3 src/receiver.py`; in another terminal run `./firmware /tmp/learning-uart`. Twenty decoded samples are expected; remove the FIFO afterward.
6. Repeat with `./firmware /tmp/learning-uart stall`. The sensor deliberately stalls after five records; supervisor termination must return status 1.
7. Debug with `gdb --args ./firmware /tmp/learning-uart`. The POSIX port uses threads/signals, so inspect RTOS task state and host threads separately. `make clean` removes the executable.

## Acceptance criteria and evidence

Normal run transmits sequences 0–19 with correct CRC and no truncated records, exits successfully, and preserves signed decoding. Corrupt packets are rejected and valid packets after noise resynchronize. A sensor stall fails within the supervisory policy in RTOS ticks. A full/blocked transport must not prevent the supervisor from progressing. Hardware watchdog reset timing is not claimed.

Four executed tests cover normal ordered data, stalled-task detection, resynchronization and CRC rejection. The checks run the actual FreeRTOS POSIX port rather than a hand-written scheduler. Read evidence/build.log and evidence/tests.log. Extend the tests with a reader that stops consuming until the FIFO fills; then show that TX timeout/watchdog ends the run.

**Observed validation:** Code authored, real FreeRTOS kernel build verified, and four host-simulator tests passed. No MCU flash, peripheral, ISR, DMA, electrical or physical-watchdog test was executed. The complete STM32F446RE target is authored and cross-built; its board execution remains pending. See hardware/MCU_PORT.md.

## Troubleshooting and limitations

The tested runtime path uses FreeRTOS POSIX. A second complete target for STM32 NUCLEO-F446RE includes startup vectors, linker script, UART, hardware watchdog and the Cortex M4F port; it compiled and linked, but has not run on a board. A POSIX signal schedule cannot validate an MCU interrupt latency, ISR priority ceiling, stack margin or DMA cache policy. No claim of full hardware readiness follows from these tests.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Add command acknowledgement with sequence matching and a retry budget, then demonstrate that duplicate commands do not execute an action twice. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show task priorities and queue depth, run twenty records, inject the stall, show failure exit, then explain which tests still require a real MCU.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.

**STM32 target build evidence:** Complete firmware cross-built and linked with arm-none-eabi GCC 13.2.1, yielding 6296 bytes text, 4 bytes data and 33084 bytes bss in this build. This is a build-size observation, not measured stack high-water usage. Physical flashing, UART framing, watchdog timeout and task stack margins remain pending. See evidence/mcu-build.log and hardware/MCU_PORT.md.
