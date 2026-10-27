# Fifteen project index

Each project has its own runbook, complete source for its stated minimum target, build/configuration files, tests, independent exercise, solution guidance and evidence record. Start with the README and VERSIONS.md before running commands. Estimates in the runbooks are learner practice estimates; the weekly roadmap allocates that practice within its 572-hour core schedule.

| ID | Level | Project runbook | Validation scope |
| --- | --- | --- | --- |
| B01 | Basic | [B01 Embedded C utility library](01_Basic/B01_C_Utility_Library/README.md) | Host build and tests; ASan and UBSan with leak detection disabled |
| B02 | Basic | [B02 Linux process and resource inspector](01_Basic/B02_Process_Inspector/README.md) | Host build live proc and deterministic fixture tests |
| B03 | Basic | [B03 UART terminal and framed protocol tool](01_Basic/B03_UART_Framed_Protocol/README.md) | Host build PTY framing corruption timeout and terminal cleanup tests |
| B04 | Basic | [B04 Multithreaded sensor simulator and logger](01_Basic/B04_Sensor_Logger/README.md) | Host build queue shutdown output-failure tests and separate TSan run |
| B05 | Basic | [B05 Cross compilation and QEMU application debugging](01_Basic/B05_Cross_Compile_QEMU/README.md) | AArch64 static/dynamic cross builds and QEMU user execution |
| I01 | Intermediate | [I01 Custom Buildroot appliance](02_Intermediate/I01_Buildroot_Appliance/README.md) | Host persistence tests and Buildroot external configuration resolution |
| I02 | Intermediate | [I02 Kernel character driver and user space client](02_Intermediate/I02_Kernel_Character_Driver/README.md) | Userspace build and Linux 6.12 kernel composite-object compile |
| I03 | Intermediate | [I03 Device tree GPIO interrupt platform driver](02_Intermediate/I03_Device_Tree_GPIO/README.md) | Linux 6.12 object compile and offline overlay application |
| I04 | Intermediate | [I04 Custom Yocto telemetry image](02_Intermediate/I04_Yocto_Telemetry/README.md) | Native telemetry build/test and complete Yocto metadata authored |
| I05 | Intermediate | [I05 RTOS telemetry connected to Linux](02_Intermediate/I05_RTOS_Linux/README.md) | Real FreeRTOS POSIX tests and STM32 firmware cross-build/link |
| A01 | Advanced | [A01 Sensor driver using the IIO subsystem](03_Advanced/A01_IIO_Sensor_Driver/README.md) | Conversion tests kernel object compile and offline overlay application |
| A02 | Advanced | [A02 Linux latency and performance investigation](03_Advanced/A02_Latency_Investigation/README.md) | Host functional tests and raw idle/loaded latency experiments |
| A03 | Advanced | [A03 Signed A B update and rollback simulator](03_Advanced/A03_Signed_AB_Update/README.md) | Signature tamper interruption health and rollback host simulation tests |
| C01 | Capstone | [C01 Industrial monitoring and edge gateway](04_Capstone/C01_Industrial_Gateway/README.md) | Gateway tests and real FreeRTOS to FIFO to gateway integration |
| C02 | Capstone | [C02 Linux MCU robot control and diagnostics simulation](04_Capstone/C02_Robot_Control_Diagnostics/README.md) | Deterministic robot tests simulation and optional synthetic AI evaluation |

## Minimum target and physical integration

Hardware absence is handled through explicit target choices. B05 uses foreign-architecture Linux user emulation. I05 includes both an executed real-RTOS host port and a cross-built physical STM32 target. A03's complete minimum is a signed file-slot update simulator. C01 integrates the real RTOS host producer with a gateway and includes image metadata. C02's minimum is a deterministic robot simulation. Kernel drivers and board overlays are authored and compile checked, with actual board behavior left unverified.

These choices preserve the learning progression while avoiding claims that simulated peripherals, boot selection or braking establish physical behavior. To complete target-level competence, follow each project's named hardware/runtime acceptance procedure and save your own evidence. Extensions are separate from the complete minimum implementation.

## Reproduce the offline checks

From the package root run `python3 tools/verify_host_package.py`. It rebuilds and tests 14 available host suites or components and reports external-target portions explicitly. It needs a Linux host, Python 3, a C/C++ compiler, make and OpenSSL. It does not download dependencies, load modules, run QEMU or require root. Run I05 and cross/emulator targets separately after following their setup instructions.

Generated build outputs are not substitutes for source. Rebuild them with the provided commands and capture versions. The project evidence logs remain useful even when a target dependency is not installed locally.
