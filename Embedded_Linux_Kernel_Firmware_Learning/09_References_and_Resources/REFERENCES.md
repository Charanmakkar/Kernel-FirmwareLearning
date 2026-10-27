# Primary references and research notes

Accessed 27 October 2026. These are official project/language/board/component documents and Linux man-pages; no employer JD has been sampled. This is targeted primary-source research performed for release 1. It is not a claim that an external long-running research job exists or that every referenced tool was executed. Code and worked examples are original educational material.

- **R01** [C11 committee draft N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) — C11. Language-rule reference; draft, not claimed to be the latest ISO edition.
- **R02** [Buildroot AArch64 virt defconfig](https://raw.githubusercontent.com/buildroot/buildroot/2026.08.1/configs/qemu_aarch64_virt_defconfig) — 2026.08.1. Inspected target selection and Linux 6.18.7 pin.
- **R03** [QEMU virt machine documentation](https://www.qemu.org/docs/master/system/arm/virt.html) — moving master. Virtual board scope; generated run script/version still to be locked.
- **R04** [Yocto system requirements](https://docs.yoctoproject.org/5.0.14/ref-manual/system-requirements.html) — 5.0.14. Supported hosts and build prerequisites; no build performed.
- **R05** [Kernel circular-buffer concepts](https://docs.kernel.org/6.12/core-api/circular-buffers.html) — 6.12. Conceptual comparison only; not selected driver API baseline.
- **R06** [Kernel rationale on volatile](https://docs.kernel.org/6.12/process/volatile-considered-harmful.html) — 6.12. Concurrency rationale; not a C11 atomic API reference.
- **R07** [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) — moving docs. Capabilities and limitations; actual compiler recorded separately.
- **R08** [Clang UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) — moving docs. Supported checks vary; no complete correctness proof.
- **R09** [GCC atomic builtins](https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html) — moving docs. Compiler atomic support; M01 uses standard C discussion, not kernel atomics.
- **R10** [Zephyr native_sim](https://docs.zephyrproject.org/4.2.0/boards/native/native_sim/doc/index.html) — 4.2.0. Simulation target and 64-bit qualifier verified.
- **R11** [Zephyr Nucleo F446RE board](https://docs.zephyrproject.org/latest/boards/st/nucleo_f446re/doc/index.html) — latest. Board capabilities checked; v4.2.0 board compatibility still pending.
- **R12** [ST Nucleo-64 user manual UM1724](https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf) — Rev 17 September 2025. Board family/revision reference; inspect exact board and jumpers before wiring.
- **R13** [Kernel GPIO descriptor consumer](https://docs.kernel.org/6.18/driver-api/gpio/consumer.html) — 6.18. Descriptor interface preferred over legacy integer GPIO.
- **R14** [IIO introduction](https://docs.kernel.org/6.18/driver-api/iio/intro.html) — 6.18. Subsystem fit for accelerometer project.
- **R15** [ADXL345 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/adxl345.pdf) — Rev G. Selected sensor; breakout schematic and wiring not yet verified.
- **R16** [RAUC basics](https://rauc.readthedocs.io/en/v1.13/basic.html) — 1.13. Signed update framework; no boot integration test claimed.
- **R17** [Active kernel releases](https://www.kernel.org/releases.html) — live status. 6.18 and 6.12 longterm lines; status can change.
- **R18** [GNU ld linker scripts](https://sourceware.org/binutils/docs/ld/Scripts.html) — moving docs. Sections/memory-map reference.
- **R19** [GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) — moving docs. Debugger reference; selected executable version must be recorded.
- **R20** [Linux read syscall](https://man7.org/linux/man-pages/man2/read.2.html) — Linux man-pages. Return/EOF/error behavior.
- **R21** [Linux write syscall](https://man7.org/linux/man-pages/man2/write.2.html) — Linux man-pages. Short I/O and persistence distinctions.
- **R22** [Linux poll syscall](https://man7.org/linux/man-pages/man2/poll.2.html) — Linux man-pages. Readiness/error/timeout semantics.
- **R23** [POSIX condition-variable wait](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html) — POSIX manual mirror. Predicate and mutex semantics; inspect implementation support.
- **R24** [Kernel dynamic DMA mapping guide](https://docs.kernel.org/6.18/core-api/dma-api-howto.html) — 6.18. CPU/physical/device addresses and ownership.
- **R25** [Buildroot manual](https://buildroot.org/downloads/manual/manual.html) — moving manual. Architecture/packaging overview; release-matched manual required during implementation.
- **R26** [Kernel lock types](https://docs.kernel.org/6.18/locking/locktypes.html) — 6.18. Context restrictions and PREEMPT_RT differences.
- **R27** [Kernel workqueues](https://docs.kernel.org/6.18/core-api/workqueue.html) — 6.18. Deferred process context; teardown must quiesce work.
- **R28** [Kernel RCU explanation](https://docs.kernel.org/6.18/RCU/whatisRCU.html) — 6.18. Read/copy/update and deferred reclamation concepts.
- **R29** [Kernel platform driver model](https://docs.kernel.org/6.18/driver-api/driver-model/platform.html) — 6.18. Matching/probe/remove model.
- **R30** [Kernel memory and user-access APIs](https://docs.kernel.org/6.18/core-api/mm-api.html) — 6.18. User access and allocation contracts.
- **R31** [Kernel device-tree binding guidelines](https://raw.githubusercontent.com/torvalds/linux/v6.18/Documentation/devicetree/bindings/writing-bindings.rst) — v6.18. Hardware description and binding ABI rules.
- **R32** [Zephyr threads reference source](https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/v4.2.0/doc/kernel/services/threads/index.rst) — v4.2.0. Thread ownership/lifecycle; API support must be checked per target.
- **R33** [Kernel ftrace](https://docs.kernel.org/6.18/trace/ftrace.html) — 6.18. Tracing reference; no measured latency results yet.
- **R34** [SPDX overview](https://spdx.dev/learn/overview/) — live documentation. Software bill of materials and license metadata context.
- **R35** [Kernel selftests](https://docs.kernel.org/6.18/dev-tools/kselftest.html) — 6.18. Kernel regression methodology.
- **R36** [LiteRT for Microcontrollers](https://developers.google.com/edge/litert/microcontrollers/overview) — live documentation. Optional MCU inference context; no runtime selected/benchmarked.
- **R37** [BeagleBone Black board](https://www.beagleboard.org/boards/beaglebone-black) — live board page. Cortex-A8 platform and board documentation entry point.

## Decisions supported by the sources

R02 explicitly selects Linux 6.18.7 for the selected Buildroot tag. That is a coherent teaching image baseline; it does not prove this patch release is the most secure choice today. The moving Buildroot manual is used for orientation only; implementation must use the selected source tree's own manual and generated build records.

R10 establishes that native_sim is a host executable and does not model a particular MCU. R11/R12 support selecting a Nucleo family board but do not establish that the exact versioned firmware, jumpers or UART routing have been validated. R03 establishes that QEMU virt is not a physical board. These distinctions constrain what later evidence can claim.

R13/R14 support descriptor-based GPIO and an established sensor subsystem. A01 will study the existing ADXL345 driver before producing an isolated teaching variant or justified patch; the program does not recommend deploying a duplicate driver for supported hardware.

R16 supports using an established signed-update framework. The program adds a required boot-attempt/health/recovery test design; that design is an engineering inference to validate, not a successful RAUC integration result.

Several attempted URLs were unavailable: older 6.12 GPIO/DMA paths, a guessed Buildroot 2026.02.6 target URL, docs.rauc.io for the selected version, and the rendered versioned Zephyr thread page. No technical claim relies on those failed fetches. Working official alternatives are recorded above. Source branches, current docs and accessed dates are never substitutes for build hashes.

## How to research a version-sensitive answer

Find the selected release's API declaration, implementation, in-tree callers, Kconfig/build constraints and official documentation. Record a source revision and a minimal compile/use test. If docs/source differ, explain the discrepancy and follow the selected source contract. Check device datasheet and board schematic separately: a chip capability does not identify a board pin or jumper route. A tutorial from a different kernel is a hypothesis source, not final authority.
