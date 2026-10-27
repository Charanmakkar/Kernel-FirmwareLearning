# Validation summary

Recorded 27 October 2026. The results below concern the delivered reference implementations. Learner competence remains not assessed. A status is claimed only when a corresponding log exists.

## Portable package check

A fresh relocated copy passed 14 offline host suites/builds with zero failures and zero unexpected skips. Ten external or optional portions were explicitly skipped by that runner; some have separate earlier evidence, such as B05 emulation and I05 RTOS/cross-builds. The runner never silently promotes a skip to a pass. Its durations are not performance benchmarks.

## Evidence by project

| ID | Executed or verified | Still pending or outside that evidence |
| --- | --- | --- |
| B01 | Host build and tests; ASan and UBSan with leak detection disabled | Physical MCU port optional; leak checking unavailable in the recorded environment |
| B02 | Host build live proc and deterministic fixture tests | Other target kernels and permission policies require retesting |
| B03 | Host build PTY framing corruption timeout and terminal cleanup tests | Physical UART electrical/timing checks; production session freshness |
| B04 | Host build queue shutdown output-failure tests and separate TSan run | Target timing and sustained-load qualification |
| B05 | AArch64 static/dynamic cross builds and QEMU user execution | Full-system guest boot not part of B05; GDB session not executed |
| I01 | Host persistence tests and Buildroot external configuration resolution | Full toolchain/image build QEMU boot reboot and power-loss checks |
| I02 | Userspace build and Linux 6.12 kernel composite-object compile | Final module linking loading runtime uaccess poll and unload stress |
| I03 | Linux 6.12 object compile and offline overlay application | Loadable module and real Raspberry Pi GPIO IRQ and remove tests |
| I04 | Native telemetry build/test and complete Yocto metadata authored | BitBake image/SDK builds service integration and guest boot |
| I05 | Real FreeRTOS POSIX tests and STM32 firmware cross-build/link | Flashing physical UART ISR watchdog timing and stack measurements |
| A01 | Conversion tests kernel object compile and offline overlay application | Real TMP102 IIO binding bus errors and power/runtime checks |
| A02 | Host functional tests and raw idle/loaded latency experiments | Target scheduler traces where unavailable and physical timing bounds |
| A03 | Signature tamper interruption health and rollback host simulation tests | Bootloader trust anchor protected rollback state and flash power cuts |
| C01 | Gateway tests and real FreeRTOS to FIFO to gateway integration | Full Yocto appliance build/boot physical sensor and recovery qualification |
| C02 | Deterministic robot tests simulation and optional synthetic AI evaluation | Real Linux MCU transport motors dynamics stopping and hardware safety |

## Evidence interpretation

Code authored means the reference source/configuration is present. Build verified means the stated compiler/link/configuration step completed. Host tested means the named checks ran in this Linux environment. Emulator tested means the named emulator and target ran; B05 uses Linux user mode, not a full guest kernel. Hardware tested would require the named physical board and setup. No physical hardware test is claimed in this edition.

I02, I03 and A01 compiled into kernel composite objects. Final loadable-module linking and kernel runtime checks remain pending. I01's Buildroot configuration resolved its selected components; this is not an image build. I04 and C01 include complete Yocto metadata, but no BitBake image or SDK build is claimed. I05's STM32 source produced an ELF/binary with 6296 bytes of text, 4 bytes of initialized data and 33084 bytes of BSS in the recorded cross-build. This is a link-size observation, not a measured runtime stack margin.

The real RTOS-to-gateway host integration accepted 20 samples with zero rejections in its recorded run. C02 generated 201 deterministic simulation samples. Its approximate scripted travel and command-expiry time are simulation observations, not physical stopping performance. Optional AI metrics use synthetic data and do not establish industrial detection accuracy.

The assessment reference suite also compiled and executed four complete C files with strict C11 warnings: 30 portable routines, a POSIX complete-write helper, a bounded streaming decoder and a repaired parser. AddressSanitizer and UndefinedBehaviorSanitizer passed for the portable suite with leak detection disabled. LeakSanitizer could not initialize under the recorded container restrictions; leak checking is not claimed. See 04_Skill_Assessments/answers/VALIDATION.md for exact commands and results.

## Independent review and regression

Independent review reproduced a UART cancellation defect: SIGTERM left terminal settings in raw mode. The implementation now uses signal-aware cancellation and restores settings on SIGINT, SIGTERM and broken output. PTY regression tests passed after the change. The project includes a debugging case study. This demonstrates a concrete review-to-fix-to-test cycle; it does not imply the tool has been exhaustively verified.

## Next validation work

Run the full Buildroot image and guest boot first, then complete a matching-kernel build and load/runtime tests in a disposable guest. Build the Yocto image/SDK on its documented host. Flash the Nucleo firmware and measure serial, watchdog and stack behavior. Test the GPIO and sensor drivers on the named Raspberry Pi configuration. Only then extend capstones toward physical devices, with separate electrical and control requirements.

Every new target or source revision requires a new version record and affected acceptance tests. Keep raw outputs and test inputs. Do not convert an earlier host pass into a hardware pass by editing a status cell.
