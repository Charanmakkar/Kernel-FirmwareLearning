from pathlib import Path
import csv
import json
import shutil
import textwrap

WORKSPACE = Path(__file__).resolve().parents[1]
ROOT = WORKSPACE / 'Embedded_Linux_Kernel_Firmware_Learning'
DATE = '2026-10-27'

def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).strip() + '\n', encoding='utf-8', newline='\n')

def table(path, rows, fields=None):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

for folder in ['00_Start_Here', '01_Learning_Roadmap', '02_Interview_Questions_and_Answers',
               '03_JD_JR_Skills_and_Learning_Content', '04_Skill_Assessments/questions',
               '04_Skill_Assessments/answer_keys', '05_Interview_Strategy', '06_AI_Integration',
               '07_Projects/01_Basic', '07_Projects/02_Intermediate', '07_Projects/03_Advanced',
               '07_Projects/04_Capstone', '08_Portfolio_and_Job_Readiness',
               '09_References_and_Resources', '10_Progress_Tracking', 'Word_Edition']:
    (ROOT / folder).mkdir(parents=True, exist_ok=True)

write('00_Start_Here/PROFILE_AND_ASSUMPTIONS.md', r'''
# Profile, assumptions, and scope

Prepared 27 October 2026. This is release 1 of a staged program, not a claim that the entire master prompt has been completed. Read PROGRESS.md for exact coverage. A learning artifact existing is never evidence of the learner's skill.

No experience profile, target job description (JD), job requirements (JR), interview date, board inventory, or budget was supplied. Your workspace is Windows with PowerShell. We observed Python 3.13.2 and an LLVM-MinGW Clang 22.1.0-rc3 toolchain; the executable called gcc is also Clang, not a second compiler. WSL lists Ubuntu but launching it failed with STATUS_ACCESS_DENIED. We did not change your WSL installation or computer settings.

Provisional learner: junior-to-mid-level applicant, 10–12 hours weekly, no presumed proficiency. C, Linux, electronics, and debugging are **not assessed**. These assumptions choose a starting point; they do not estimate your current ability. Complete D01 before deciding what to skip.

The requested 9–12 months is an initial planning window. At 11 hours/week, 39–52 weeks supplies 429–572 hours. The complete three-track program below budgets 704 hours over 64 weeks: 386 project hours and 318 lesson, practice, assessment, review, and contingency hours. That is roughly 15 months, with another 8–16 weeks possible if C/Linux prerequisites fail. These are planning estimates, not measured learning times or a mastery guarantee. The tracks share foundations but require different evidence. Preparing for one role can fit a shorter path; completing all 15 projects should not delay a well-supported application to a narrower role.

## Three tracks

| Track | Core evidence | Additional depth | Recognize initially; defer until relevant |
|---|---|---|---|
| EL: Embedded Linux/system software | Robust C service, IPC, cross-built executable, image boot, logs and failure tests | Packaging, sysroots, deployment, networking, storage, updates, service operations | Deep scheduler modifications, custom bus controller drivers |
| KD: Kernel/drivers/BSP | Build the selected kernel; defend driver lifetimes and locking; device-tree binding and probe evidence | Execution contexts, subsystem interfaces, IRQ/DMA ownership, power management, platform boot | New filesystem, GPU, or network stack implementation |
| FW: MCU/bare metal/RTOS | Link/start a target, peripheral state machine, bounded task/ISR design, measured timing and recovery | MCU memory map, startup/vector/linker work, interrupt priorities, watchdog and stack budgeting | Linux VM internals and Yocto layer internals unless the role integrates them |

Shared foundations: C object lifetime and integer behavior, interfaces, state machines, reproducible builds, Git, debugging, test design, and accurate technical communication. An application processor with a Memory Management Unit (MMU) running Linux and a Cortex-M microcontroller running firmware are different targets. QEMU virt is a virtual application processor board; Zephyr native_sim is a host simulation of RTOS application behavior, not a model of the chosen STM32's electrical or interrupt timing.

## Personalization inputs to add after D01

Record the actual JD text and URL; target track and seniority; diagnostic artifacts; available hours and deadline; host RAM/disk; boards and tools already owned; budget and industry. These materially change priorities. Until then, all skills-matrix requirements are an explicitly authored reference framework, not an employer's requirements. Do not assign a numeric proficiency score from a chat description alone.

## Start today (about two hours)

1. Attempt D01 without AI and save source, command transcript, and explanations.
2. Install no board software yet. Read ENVIRONMENT.md and run the B01 portable test command if your compiler is available.
3. Study M01, implement exercise E01 independently, then compare the separate solution.
4. Put your result and artifact path in skills_tracker.csv; leave all other skills unassessed.

Keep reference answers closed until you attempt a task. A Windows-native C pass supports portable utility logic only; it says nothing about POSIX APIs, kernel modules, or MCU peripherals.
''')

write('00_Start_Here/ENVIRONMENT.md', r'''
# Environment and target policy

## Host lanes

**Portable lane, available now:** Windows x86-64, Python 3.13.2 and LLVM-MinGW Clang 22.1.0-rc3. B01 uses ISO C11, fixed-width unsigned bytes, and no OS APIs. The Python runner invokes the compiler directly, so Make is optional. Windows uses LLP64; a Linux x86-64 host commonly uses LP64. Never assume long or pointers have equal widths.

**Linux lane, required for B02 onward:** choose a disposable Ubuntu 24.04 LTS x86-64 VM, native installation, or working WSL2 Ubuntu. Use a Linux filesystem such as ~/embedded-labs for builds; a Windows-mounted directory can introduce permission, case, and filesystem differences. A VM snapshot is recommended before module experiments. WSL alone does not provide the target QEMU kernel or physical board environment. Use QEMU guests for driver tests; never load these experimental drivers into a daily-use host.

Recommended planning capacity (estimates): 16 GB host RAM and 100 GB free for the early Linux/Buildroot work; for Yocto prefer 32 GB RAM, 8 CPU threads, and 250–350 GB free SSD space. These are program planning allowances, not vendor minimums. Recheck the selected Yocto release's official requirements [R04] before building. Reduce parallelism if the out-of-memory killer terminates compilers.

On the Linux lane, from a normal user shell:

```sh
sudo apt update
sudo apt install build-essential clang gdb git cmake ninja-build python3 python3-venv \
  pkg-config strace valgrind socat qemu-system-arm qemu-user gcc-aarch64-linux-gnu \
  binutils-aarch64-linux-gnu bc bison flex libssl-dev libelf-dev \
  libncurses-dev cpio rsync unzip file wget xz-utils
mkdir -p ~/embedded-labs
cd ~/embedded-labs
uname -a
cc --version
git --version
qemu-system-aarch64 --version
```

This installs common tools, not a complete Yocto dependency set. Follow R04 for its additional host packages. The commands are authored instructions and have not been executed on a Linux host in this release. Save exact apt package versions with `dpkg-query -W > host-packages.txt` once installed. No root privileges are needed to compile B01. Do not run entire builds with sudo.

## Selected future project targets (planned, not validated)

| Lane | Selection | Boundary |
|---|---|---|
| Buildroot/QEMU | Buildroot tag 2026.08.1; qemu_aarch64_virt_defconfig; AArch64 virt with Cortex-A53; kernel 6.18.7 from that defconfig | Upstream file inspected [R02]. Source/build/toolchain hashes still pending. This is a teaching baseline, not a claim of current security patch status. |
| Kernel labs | Same Linux 6.18.7 configured build and guest; match module build tree, configuration, and compiler | Use 6.18 documentation/source for implementation, not arbitrary tutorials. R05/R06 are explicitly older conceptual references, not API authority for future code. |
| Yocto | Poky tag yocto-5.0.14 (Scarthgap), MACHINE=qemuarm64 | Separate image lineage. Its kernel and toolchain must be recorded from BitBake; do not inject the Buildroot kernel or modules. Tag/recipe build not yet validated. |
| RTOS simulation | Zephyr v4.2.0, native_sim/native/64 | Simulation choice checked against versioned docs [R10]. SDK/tool manifest must be locked when I05 is authored. |
| MCU hardware | ST NUCLEO-F446RE, MB1136; STM32F446RE Cortex-M4; Zephyr v4.2.0 pending board-tag verification | Board docs [R11/R12] checked; exact revision, jumpers and firmware build not verified. Current board docs are not silently treated as a v4.2.0 API guarantee. |
| Linux GPIO/IIO hardware | BeagleBone Black Rev C, AM335x Cortex-A8; ADXL345 breakout at 3.3 V | This is ARMv7, not AArch64 virt. Board-specific kernel/configuration/image must be pinned separately before I03/A01 source is written. No wiring procedure is authorized by this plan alone. |
| Update capstone | RAUC 1.13 + isolated QEMU disk + explicit boot attempt/health state | Full A/B boot integration remains to be implemented and tested; a signed file copy alone is not rollback. |

The Buildroot tag's checked defconfig selects Linux 6.18.7 [R02]. Reproduction will also require a manifest of actual downloaded inputs, generated `.config`, compiler, and image hashes. For production, review advisories and move to supported patched releases with regression tests; this package is not a security-maintenance service.

## Why start without hardware

B01–B05 and I01/I02/I04 can establish memory safety, protocol behavior, IPC, toolchain and image skills with host tests or QEMU. I03/A01 need physical validation of pinmux, IRQ behavior and the actual sensor bus. I05 can establish RTOS state and protocol logic in native_sim, but MCU timing, stack limits, startup, fault registers and watchdog wiring need the Nucleo. C02 begins with a simulated plant, with no motor connected.

Do not buy boards before completing B01 and choosing a role. Hardware additions by outcome: Nucleo + existing USB cable for MCU debugging and serial; Linux board + microSD + documented power supply for boot/GPIO; ADXL345 breakout for IIO integration; logic analyzer for timing/bus verification. Prices and availability are not assumed. Verify breakout schematic, voltage, board revision and shared-pin conflicts before wiring. Use documented 3.3 V logic, not RS-232 voltage. Use the Nucleo ST-LINK virtual COM port as the first serial path; check board solder bridges and UART routing before adding external wires.

## Record versions before interpreting a failure

```sh
uname -r
cc -dumpmachine
cc --version
file ./application
readelf -h ./application
git rev-parse HEAD
sha256sum ./application
```

Wrong executable architecture gives an exec-format error; a missing ELF interpreter can look like a missing file even when the executable exists. Check `readelf -l`. A sysroot supplies target headers/libraries; it is not a CPU emulator. For out-of-tree modules use the target kernel's configured build output, not `/lib/modules/$(uname -r)/build` on an unrelated host.

## Troubleshooting the observed host limitation

WSL failed with error 0xd0000022 / Wsl/Service/CreateInstance/STATUS_ACCESS_DENIED. This package records that failure as evidence; it does not diagnose a specific Windows policy or perform invasive repair. Use the portable lane now, then a working Linux environment for B02. Do not reset or unregister an existing distribution to follow a tutorial. No emulator, guest, Linux syscall, or hardware result is reported as passed here.
''')

write('01_Learning_Roadmap/PREREQUISITES_AND_GATES.md', r'''
# Prerequisite map and competence gates

```text
D01 diagnostic
  +--> C lifetime, byte arithmetic, compiler/debugger --> B01
  |      +--> POSIX files/processes --> B02 --> B03 protocol
  |      +--> threads/ownership --> B04
  +--> architecture/ELF/toolchains --> B05 --> I01 Buildroot
          +--> contexts/locking/driver model --> I02 --> I03 --> A01
          +--> image metadata/packages --> I04 Yocto
  +--> MCU startup/peripheral state machines --> I05 RTOS/protocol
B04 + I02 --> A02 latency investigation
I01 + boot/persistence/keys --> A03 updates
B03 + I01 + I05 + A03 --> C01 gateway
B03 + I05 + A02 + C01 integration methods --> C02 simulated robot
```

Study deeply: pointer/object lifetime, integer bounds, error contracts, shared-data ownership, execution context, resource lifetime and state transitions. Implement immediately: byte decoding, bounded queues, file I/O loops, shutdown, packaging and recovery tests. Recognize initially: page-table levels, RCU read-side principles, DMA coherency, verified boot trust chains. Defer advanced architecture-specific barriers, new scheduler algorithms, complex bus controllers and ML accelerators until the actual JD asks for them.

| Gate | Required evidence | Pass rule | If failed |
|---|---|---|---|
| G0 prerequisite | D01 independent attempt + explanation | >=70/100 overall, C>=15/25 and Linux>=12/20, no critical memory/concurrency misconception | Spend 2 weeks on M01 and Linux file/process labs; retake different data |
| G1 safe C | B01 tests + unseen parser/ring change + M01 exit | >=80/100; no out-of-bounds, lifetime violation, unchecked length or fabricated output | Reproduce failing invariant, add regression, explain failure; retest independently |
| G2 Linux user space | B02–B04 artifacts + syscall and thread review | Partial I/O, errors, timeouts and shutdown all defended; >=80 | Rebuild a single-producer queue and bounded poll loop before adding features |
| G3 platform | B05/I01 boot and cross-debug record | Independently identify ELF ABI, loader, kernel/rootfs/init and persist config across reboot | Trace boot stage by stage and compare known-good configs |
| G4 kernel | I02/I03 guest/hardware evidence + locking review | No sleep-in-atomic, unsafe user dereference or lifetime race; >=80 | Draw each callback context and cleanup dependency; add failure injection |
| G5 firmware | I05 simulation plus specified MCU evidence | Bounded queues, watchdog policy and timeout-to-safe-state demonstrated | Measure one task and one interrupt path; simplify ownership and task graph |
| G6 integration | A01–A03 acceptance reports | Measurement reproducible; recovery tested; signature failure rejected | Repeat the specific fault with recorded build IDs; no average-score waiver |
| G7 portfolio | C01/C02 defense + final practical | Fresh reproduction, honest scope, failure test and independent explanation | Fix missing evidence before resume claim; focused mock interview |

An authored solution does not satisfy a gate. Grade correctness 30, reasoning 15, debugging method 15, resource handling 10, concurrency/timing 10, tests 10, communication 10. Critical failures block passage irrespective of average: memory unsafety; uncontrolled actuator behavior; sleeping in hard-IRQ context; secret exposure; bypassed signature checks; claiming unexecuted tests passed. Non-applicable categories are declared before the assessment and their points reassigned to correctness/testing, not silently granted.

## Shorter role paths

**Minimum readiness after foundations: 12 weeks, about 132 hours.** Weeks 1–2: D01/G1 remediation and B01. Weeks 3–4: B02/B03 partial I/O and protocol. Weeks 5–6: B04 concurrency and B05 ELF/cross build. Weeks 7–8: EL chooses I01; KD chooses the complete I02 driver before adding hardware; FW chooses I05 after a startup/peripheral lab. Weeks 9–10: timed practical, failure injection and code review. Weeks 11–12: targeted mock interviews, fresh reproduction and portfolio defense. This is a narrow junior interview path, not evidence of all three tracks, BSP bring-up or production firmware expertise. If foundations fail, add prerequisite weeks instead of compressing them.

**A 9–12-month single-track path:** work through shared weeks 1–18, select the role's depth work, finish one relevant capstone and revise. Keep the other projects planned in the 15-project catalog. The 64-week complete path retains all projects; branch priorities change order, not the catalog's counts.

Weekly 11-hour rhythm: 2 hours concept/source reading; 5 hours implementation/testing; 1 hour debugging notes; 1 hour independent assessment; 1 hour spaced review/mock answers; 1 hour contingency. Allocate 10–12 based on real availability. Every fourth week revisit two old questions and one old bug using different input data. Missed gates move subsequent milestones; calendar time is not competence.
''')

# Each row is an explicit weekly task; later module links land on a catalog that labels delivery status.
weeks = [
('Orientation','D01 and environment','D01; M01','B01','Capture diagnostic; compile one C file','Produce source + transcript; explain each diagnostic failure'),
('C foundations','Objects, arrays and pointers','M01','B01','Draw lifetimes; fix array decay mistakes','Explain sizeof at caller and callee with correct bounds'),
('C foundations','Integers, bytes and parsing','M01','B01','Decode big-endian length; reject malformed frames','Reject short/oversized/trailing/bad-CRC data without mutation'),
('C foundations','Ring buffer and tests','M01','B01','Finish reference comparison and unseen extension','Pass G1 independently and defend all queue invariants'),
('Tools','Compilation, linking, ELF and Git','M02','B02','Inspect object symbols; isolate a linker error','Identify declaration/definition and ABI mismatch from evidence'),
('Tools','Debugging and automation','M02','B02','Break on parse failure; save backtrace and repeat command','Locate a seeded defect and add a regression'),
('Linux','Files, permissions and procfs','M03','B02','Build process inspector with bounded input','Handle process disappearance and access-denied without crashing'),
('Linux','Processes, signals and cleanup','M03','B02','Add graceful termination and error exit codes','Pass fresh /proc fixture and resource-leak review'),
('Linux','File descriptors and partial I/O','M03','B03','Implement retry accounting and absolute timeout','Explain short write, EINTR, EAGAIN and EOF separately'),
('Linux','PTY serial and terminal setup','M03','B03','Run fragmented frames through pseudo-terminal','Restore termios; reject truncated/bad-CRC frames'),
('Linux','Framing, versioning and recovery','M03','B03','Bound resynchronization and buffer growth','Recover after noise and incompatible version without hanging'),
('Concurrency','Threads and queue ownership','M04','B04','Build producer-consumer logger','No shared unsynchronized payload or lost wakeup'),
('Concurrency','Condition variables and shutdown','M04','B04','Test full queue, idle consumer and stop races','Join all threads; drain or discard by documented policy'),
('Concurrency','Race investigation and G2','M04','B04','Seed a race; use supported race tooling','Explain finding and pass independent G2 task'),
('Platform','Architecture, ABI and sysroot','M05','B05','Cross-build and inspect AArch64 ELF','Identify interpreter and target library paths'),
('Platform','QEMU execution and remote debug','M05','B05','Run target executable and stop in gdbserver','Show target backtrace with symbols and matching build ID'),
('Platform','Boot flow and root filesystem','M06','I01','Trace firmware/kernel/init/rootfs roles','Diagnose wrong root device versus missing /sbin/init'),
('Buildroot','Custom package and overlay','M06','I01','Add telemetry binary with recorded source hash','Image boots and starts the selected package'),
('Buildroot','Persistence and recovery','M06','I01','Separate immutable image from writable config','Reboot retains valid config and rejects corrupt record'),
('Buildroot','Image reproduction and G3','M06','I01','Clean rebuild; archive configs and versions','Reproduce accepted behavior from clean source; G3 pass'),
('Kernel','Build/config/module interface','M07','I02','Build matching guest kernel and external module','Module loads only against correct configured guest build'),
('Kernel','Contexts, locking and lifetimes','M07','I02','Map every callback and lock dependency','No user access or sleep while holding raw spinlock'),
('Kernel','Character I/O and user copies','M08','I02','Define byte-queue ABI and error semantics','Test invalid user pointer, short operations and empty queue'),
('Kernel','Wait queues and poll','M08','I02','Add blocking/nonblocking behavior','Predicate recheck prevents lost wakeups; poll agrees with read'),
('Kernel','Driver concurrent teardown','M08','I02','Exercise multiple clients and module ownership','Open-handle lifetime and failure paths defended'),
('Platform drivers','Device tree and bindings','M09','I03','Validate binding and explain matching/probe','Differentiate wrong compatible from deferred resources'),
('Platform drivers','GPIO and interrupt path','M09','I03','Use descriptors; defer sleepable bus work','IRQ acknowledged correctly; physical pin test still distinct'),
('Platform drivers','Cleanup, debounce and G4','M09','I03','Test bounce/burst/unbind with work pending','No deferred access after cleanup; pass G4 review'),
('Yocto','Metadata, layers and recipes','M10','I04','Create own layer and telemetry recipe','Explain parsing, task graph, package and image difference'),
('Yocto','Service and image integration','M10','I04','Enable service with declared runtime dependencies','Guest starts service and reports build metadata'),
('Yocto','SDK and clean configuration','M10','I04','Build SDK; compile external client against it','SDK-built client runs with expected target loader'),
('Yocto','Reproducibility and license evidence','M10','I04','Record layers, revisions, config and license manifest','Second build comparison has explained differences'),
('Firmware','Cortex-M startup and linker','M11','I05','Trace vectors, .data copy and .bss zero','Explain reset-to-main and locate stack in map file'),
('Firmware','MMIO, clocks and interrupts','M11','I05','Implement nonblocking UART/timer state machine','No busy wait in ISR; clear peripheral flags as documented'),
('Firmware','RTOS tasks and queue design','M12','I05','Create bounded sample/serial/watchdog tasks','Demonstrate queue overload policy and priority rationale'),
('Firmware','Protocol Linux–MCU integration','M12','I05','Use one framed serial path with version handshake','Reconnect and duplicate request behavior verified'),
('Firmware','Watchdog, fault and G5','M12','I05','Inject stalled worker and disconnect','Independent deadline-safe recovery; G5 evidence separated by target'),
('IIO','Sensor register and subsystem reading','M13','A01','Read ADXL345 datasheet and existing IIO driver','Select channel/scale ABI; avoid duplicate production driver'),
('IIO','IIO core and register transport','M13','A01','Implement educational sensor acquisition in isolated tree','Known raw register fixtures and sign conversion pass'),
('IIO','Faults, lifecycle and hardware evidence','M13','A01','Inject bus error; test unbind and physical readings','One-g orientation sanity with documented scale and tolerance'),
('Performance','Baseline and measurement design','M14','A02','Define latency timestamps, load and experiment seed','Report raw distribution/sample count and measurement overhead'),
('Performance','Trace contention and scheduling','M14','A02','Collect ftrace/perf and isolate bottleneck','Trace supports hypothesis; no causal claim from one percentile'),
('Performance','Improve and regress','M14','A02','Change one factor; rerun comparable trials','Publish before/after and regressions without invented speedups'),
('Updates','Trust, partitions and boot attempts','M15','A03','Define A/B state machine and signing workflow','Reject wrong signer/target; distinguish verified boot and updater'),
('Updates','Install, health and rollback','M15','A03','Integrate slots, attempt count and health confirmation','Unhealthy candidate rolls back to working slot'),
('Updates','Interrupted update and G6','M15','A03','Interrupt every transition on disposable guest disks','No unrecoverable test state; pass G6 evidence review'),
('C01','Gateway requirements and architecture','M16','C01','Write one-path contract, persistent config and health schema','Requirements map to tests and dependency build IDs'),
('C01','Serial acquisition and diagnostics','M16','C01','Integrate B03/I05 with bounded logging','Disconnect produces stale health within declared timeout'),
('C01','Configuration and persistence','M16','C01','Validate/write/rename/fsync configuration','Invalid or interrupted write preserves last valid config'),
('C01','Update/recovery integration','M16','C01','Connect health gating to A03 slots','Rejected update leaves active service running'),
('C01','Fault injection and CI','M16','C01','Run corruption, disconnect and disk-full matrix','Every requirement has actual pass/fail evidence'),
('C01','Demonstration and defense','M16','C01','Fresh setup reproduction and 15-minute demo','Defend boundaries and failures without AI assistance'),
('C02','Robot plant and control boundaries','M16','C02','Define simulated dynamics, command lease and safe state','Linux can disappear without unbounded actuator command'),
('C02','MCU control loop and telemetry','M16','C02','Implement deterministic controller and timestamped samples','Bound speed command and enforce monotonic lease expiry'),
('C02','Integration and sequence handling','M16','C02','Bridge Linux planner to firmware simulation','Drop stale/replayed command; detect reset/epoch change'),
('C02','Faults and timing','M16','C02','Inject jitter, loss, sensor stall and worker overrun','State transitions and maximum response time recorded'),
('C02','Diagnostics and optional AI baseline','M17','C02','Implement threshold baseline; isolate optional anomaly score','Control unaffected by inference delay; evaluate held-out sessions'),
('C02','Acceptance and integration report','M16','C02','Complete simulated acceptance matrix and hardware gap list','Explain simulation limits and all missing hardware validation'),
('Readiness','Independent final practical','M16','C01/C02','Fresh unseen fault and feature task','>=80/100 and every critical gate satisfied'),
('Readiness','EL mock and system design','M03/M10','C01','Run EL role mock and telemetry design','Specific weak answers lead to a focused retest'),
('Readiness','KD mock and code review','M07/M13','I02/A01','Review teardown/IRQ patch and defend own code','No unsupported API or context claims'),
('Readiness','FW mock and timing defense','M11/M12','I05/C02','Analyze priorities, watchdog and startup','Measured bounds distinguished from average timing'),
('Portfolio','Resume evidence and fresh reproduction','M16','C01/C02','Make two accurate project bullets and demo artifacts','Each numerical statement links to a real report'),
('Portfolio','Final review and application decision','M16','C01/C02','JD-specific matrix; redo recurring weak task','G7 pass for selected track; remaining gaps openly recorded'),
]
assert len(weeks) == 64
rows=[]
for n,(phase,objective,modules,project,lab,exit_test) in enumerate(weeks,1):
    rows.append({'Week':n,'Phase':phase,'Prerequisites':'D01 attempt' if n==1 else f'Week {n-1} exit; applicable gate must pass',
      'Learning objectives':objective,'Estimated hours':11,'Lesson links': '../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#'+modules.split(';')[0].split('/')[0].lower(),
      'Module IDs':modules,'Practical exercise':lab,'Project milestone':project,
      'Revision work':'Re-answer two earlier questions; reproduce one old defect with changed input',
      'Objective exit test':exit_test,'Evidence required':'source revision; commands; actual result; independent explanation','Status':'not started'})
table('01_Learning_Roadmap/roadmap_64_weeks.csv',rows)

modules=[
('M01','C objects, bytes and bounded interfaces','complete lesson','M01_C_Objects_Bytes_and_Contracts.md','D01 attempt','B01','R01; R05; R06; R07; R08; R09'),
('M02','Toolchain, symbols, ELF, ABI, Git, Make/CMake and automation','planned','', 'M01','B02/B05','R18; R19'),
('M03','Linux files, processes, signals, IPC, sockets, poll/epoll and services','planned','', 'M01/M02','B02/B03','R20; R21; R22'),
('M04','Threads, ownership, mutex/condition predicates and graceful shutdown','planned','', 'M03','B04','R23'),
('M05','Architecture, ARM, caches, MMU/MPU, MMIO, cross toolchains and DMA','planned','', 'M02','B05','R03; R24'),
('M06','Boot, U-Boot roles, kernel/rootfs/init, Buildroot and persistence','planned','', 'M05','I01','R02; R25'),
('M07','Kernel execution contexts, allocation, locking, RCU, work/timers and tracing','planned','', 'M04/M05','I02','R26; R27; R28'),
('M08','Modules, driver model, char ABI, copies, waits, poll and teardown','planned','', 'M07','I02','R29; R30'),
('M09','Device tree, bindings, pinctrl, clocks, regulators, GPIO and interrupts','planned','', 'M07/M08','I03','R13; R31'),
('M10','Yocto, recipes, layers, SDK, packaging, networking and licenses','planned','', 'M06','I04','R04'),
('M11','MCU reset/startup, vectors, linker, peripherals, ISR/DMA and fault state','planned','', 'M01/M05','I05','R11; R12'),
('M12','RTOS priorities, queues, deadlines, stack, watchdog and serial recovery','planned','', 'M11/M04','I05','R10; R32'),
('M13','IIO sensor drivers, register transport, scale and power management','planned','', 'M09','A01','R14; R15'),
('M14','GDB, strace, perf, ftrace, sanitizers, latency and fault isolation','planned','', 'M04/M07','A02','R07; R08; R33'),
('M15','Storage durability, SBOM, least privilege, signed updates/rollback and boot trust','planned','', 'M06/M10','A03','R16; R34'),
('M16','Integration requirements, acceptance, CI, code review and project defense','planned','', 'G2 plus chosen track gates','C01/C02','R25; R35'),
('M17','Optional anomaly detection: baseline, data split, inference and maintenance','workflow delivered; executable extension pending','', 'C01 or C02 core complete','C02 extension','R36'),
]
catalog='# Module catalog and delivery boundary\n\nA catalog entry is a plan, not a delivered lesson. Only M01 currently has all ten required lesson elements. Future week links intentionally land here until the named full module exists. References are an entry point, not a replacement for missing lesson content.\n\n'
for mid,title,status,file,pre,projects,refs in modules:
    catalog+=f'## {mid}\n\n**{title}** — {status}. Prerequisites: {pre}. Practice: {projects}. References: {refs}.\n\n'
    if file: catalog+=f'[Open lesson]({file}). Independent exercise and solution are separate linked files.\n\n'
write('03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md',catalog)

skills=[
('S01','All','must-have','implement/debug','C object lifetime and ownership','M01','B01','G1','Q001-Q010'),
('S02','All','must-have','implement/debug','Integer conversions, alignment, endian and bounds','M01','B01','G1','Q011-Q020'),
('S03','All','must-have','implement/test','Ring buffers, parsing, state machines, complexity','M01','B01/B03','G1','Q021-Q030'),
('S04','All','must-have','build/inspect','Compilation, linking, ELF and ABI','M02','B05','G3','Q031-Q035'),
('S05','All','must-have','demonstrate','Git, reviews, shell/Python, test automation','M02','B01','G1','Q036-Q040'),
('S06','EL/KD','must-have','operate/debug','Linux CLI, users, permissions, /proc /sys /dev and services','M03','B02','G2','Q041-Q050'),
('S07','EL','must-have','implement/debug','POSIX I/O, signals, IPC, sockets, poll/epoll','M03','B03','G2','Q051-Q060'),
('S08','All','must-have','design/debug','Synchronization, races, deadlocks, shutdown','M04','B04','G2','Q061-Q070'),
('S09','KD/FW','must-have','explain/measure','ARM, MMIO, caches, interrupts, MMU/MPU and DMA','M05','B05/I05','G3/G5','Q071-Q080'),
('S10','EL/KD','must-have','build/debug','Cross toolchain, sysroot and target deployment','M05','B05','G3','Q081-Q085'),
('S11','EL/KD','must-have','integrate/debug','Boot, kernel config, initramfs, rootfs, BSP','M06','I01','G3','Q086-Q090'),
('S12','KD','must-have','implement/review','Kernel contexts, allocation, locking, waits, RCU','M07','I02','G4','Q091-Q100'),
('S13','KD','must-have','implement/test','Driver model, user copies, ABI and resource lifetimes','M08','I02','G4','Q101-Q110'),
('S14','KD','must-have','implement/debug','Device tree/bindings, GPIO/IRQ, clocks/regulators','M09','I03','G4','Q111-Q120'),
('S15','KD','must-have','integrate/review','I2C/SPI/UART, IIO, DMA and runtime PM','M13','A01','G6','Q121-Q130'),
('S16','FW','must-have','implement/debug','Startup, vectors, linker, MMIO/peripheral state machines','M11','I05','G5','Q131-Q140'),
('S17','FW','must-have','design/measure','RTOS tasks, queues, inversion, timing, watchdog, stack','M12','I05','G5','Q141-Q150'),
('S18','EL/FW','must-have','implement/test','Framing, CRC, timeout, versioning and recovery','M12','B03/I05','G2/G5','Q151-Q160'),
('S19','EL/KD','must-have','integrate/reproduce','Buildroot/Yocto, layers, recipes, SDK','M10','I01/I04','G3','Q161-Q170'),
('S20','All','must-have','investigate/measure','Debuggers, traces, sanitizers, latency and reliability','M14','A02','G6','Q171-Q180'),
('S21','EL/KD','must-have','design/test','Persistence, licensing/SBOM, least privilege, updates','M15','A03','G6','Q181-Q190'),
('S22','All','must-have','design/defend','Integration, acceptance, CI and project communication','M16','C01/C02','G7','Q191-Q200'),
('S23','EL/FW','nice-to-have','implement when JD requires','C++ RAII, ownership, move semantics and exceptions policy','M02','B02 extension','G2','Q031-Q040'),
('S24','EL/FW','nice-to-have','recognize then implement for JD','SocketCAN, fieldbus, protocol diagnostics','M10','C01 extension','G7','Q191-Q200'),
('S25','EL/FW','nice-to-have','evaluate separately','Embedded anomaly detection and measured inference','M17','C02 extension','G7','Q191-Q200'),
]
matrix=[]
for sid,track,priority,depth,req,mid,project,gate,qs in skills:
    matrix.append({'Requirement ID':sid,'JD/source':'Reference framework authored for this program; no employer JD supplied',
      'Requirement':req,'Role track':track,'Must-have/nice-to-have':priority,'Expected depth':depth,
      'Prerequisites':'See MODULE_CATALOG.md: '+mid,'Current evidence':'not assessed','Skill gap':'not assessed',
      'Learning module':mid,'Lab/project':project,'Interview questions':qs,'Assessment':gate,
      'Completion evidence':'Independent task; source revision; actual test log; oral defense','Priority rationale':'Shared safety foundation' if sid in ['S01','S02','S03','S08'] else 'Choose against actual target JD',
      'Material delivery':'M01 delivered' if mid=='M01' else 'Lesson pending; question mapping is reserved unless bank item exists'})
table('03_JD_JR_Skills_and_Learning_Content/reference_skills_matrix.csv',matrix)
table('10_Progress_Tracking/skills_tracker.csv',[{'Skill ID':s[0],'Skill':s[4],'Assessed on':'','Independent score':'not assessed','Evidence path':'','Reviewer':'','Critical failure':'not assessed','Next remediation':'Complete D01 then relevant gate','Status':'not assessed'} for s in skills])

write('03_JD_JR_Skills_and_Learning_Content/JD_ANALYSIS_AND_GAP_CLOSURE.md', r'''
# JD analysis and prioritized gap closure

No actual employer posting was supplied or sampled. The CSV is a reference skills framework. Its must-have labels are this program's track-level recommendations, not claims about any company. Current evidence and gap remain “not assessed.” The interview ranges reserve a taxonomy across Q001–Q200; check the bank's delivery index before assuming an answer exists.

When a JD arrives, retain exact requirement text and source URL/access date locally. Give it a JD-specific ID, mark explicit wording versus inference, and classify requirement/desired qualification. For example, “develop SPI drivers” explicitly points to driver depth; “embedded Linux” alone does not establish Yocto, a particular RTOS, or GPU expertise. Record those as inferred possibilities until clarified.

For each requirement: state observable expected depth; map prerequisites; attach existing evidence without inventing a proficiency score; identify missing evidence; link module, project, assessment and question IDs. Use `not assessed`, `attempted`, `demonstrated with help`, `independent pass`, or `retention pass`. A copied reference implementation cannot be `independent pass`.

Prioritization: P0 safety/correctness foundations S01–S03/S08, P1 explicit must-have requirements in the selected role, P2 gaps blocking a relevant portfolio project, P3 desired requirements, P4 optional extensions. Within one priority choose the dependency that unlocks the most required work, not the newest technology. Do not assign numerical gap scores before assessment.

After D01: if C fails, start M01/B01 and postpone kernel work; if Linux practical fails, practice files/processes before image building; if synchronization fails, implement a bounded producer-consumer queue before lock-free or ISR-shared structures. Reassess using changed inputs, an independent explanation and a new fault. Update the tracker and source evidence after each gate, not after reading a chapter.

A focused KD interview path may put I02/I03 ahead of I04. A firmware JD may prioritize startup, UART DMA, RTOS and measured watchdog behavior, while postponing Yocto. An EL systems role usually needs robust process/service and deployment evidence before custom kernel interfaces. Keep a dated explanation for each branch decision.
''')

if __name__ == '__main__':
    print(f'Created program structure, roadmap and skills matrix: {ROOT}')
