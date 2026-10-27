# Validation report — release 1

Date: 27 October 2026 (user timezone Asia/Calcutta). Execution host: Windows x86-64. Exact compiler/runtime/command/source hash details are in B01/evidence/host.json and sanitize.json. This report distinguishes observed execution from planned work.

| Item | Authored | Build verified | Host executed | Emulator executed | Specified hardware executed |
|---|---|---|---|---|---|
| B01 library/demo/tests | yes | yes, Clang strict warnings | yes, normal and ASan/UBSan | not attempted | not attempted/not required for its portable acceptance |
| B01 exercise snippets | yes | not separately checked | not separately checked | not attempted | not attempted |
| M01 exercise snippet | yes | not separately checked | not separately checked | not attempted | not attempted |
| B02–C02 implementations | pending | pending | pending | pending | pending |
| Linux setup commands | yes | not applicable | not executed on Linux | not attempted | not applicable |
| Word documents/ZIP | generated | structural checks in package_audit.json | package audit executed | not applicable | not applicable |

Actual B01 normal and sanitizer stdout: `PASS: 1146739 checks; 340000 ring operations; 100000 parser inputs`, followed by `type=7 payload=3 frame=11`. Both test and demo processes returned 0 in each build. The strict flags were -std=c11 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror, with -O2 normal and -O1 plus address/undefined instrumentation for the sanitized run. See the JSON for full argv and stderr.

What that means: queue/codec arithmetic and tested memory accesses passed these host fixtures on the recorded Clang 22.1.0-rc3 Windows GNU target. It does not prove all possible inputs, all compilers, Linux execution, kernel context correctness or hardware timing. The local executable named gcc is the same Clang toolchain; independent GCC coverage is pending. The learner's competence is not assessed by these author-run tests.

Environment limitation observed: `wsl -d Ubuntu -- bash -lc ...` failed before Linux startup with error 0xd0000022 / Wsl/Service/CreateInstance/STATUS_ACCESS_DENIED. No Linux, QEMU, Buildroot, Yocto, RTOS simulation or physical board test is reported as passed. No WSL reset, host reboot, driver loading, disk flashing or hardware purchase was performed.

Remaining physical checks: exact Linux board image/kernel/toolchain and pinmux, Nucleo revision/jumpers/toolchain/startup, UART voltage/routing, sensor breakout/schematic/address/IRQ, bus electrical behavior, DMA/cache ownership, cold boot/watchdog, measured task/interrupt latency, power-interruption recovery and any robot actuator safety mechanisms. These belong to future implemented projects, not B01's portable test grade.

Package audit checks: exact project count/distribution, roadmap total, interview/category counts/IDs/fields, delivered-file links, evidence/source hashes, DOCX ZIP/XML integrity and ZIP inventory integrity. The audit does not substitute for visual rendering in Word or execution of Linux commands. Render status is recorded separately if performed.

## Word rendering attempt

A hidden Microsoft Word COM export was attempted but did not complete. The newly created rendering processes were stopped. No PDF or visually reviewed pagination is claimed. The four DOCX editions have structural/text checks; refresh contents fields in Word (Ctrl+A, F9). See word_render_attempt.json.
