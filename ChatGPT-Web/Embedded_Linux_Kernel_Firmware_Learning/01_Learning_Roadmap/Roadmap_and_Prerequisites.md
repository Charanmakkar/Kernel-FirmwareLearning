# Roadmap and prerequisite sequence

The core schedule contains 52 weeks at 11 hours per week, for 572 hours. It assumes deliberate practice with the complete reference implementations available after an independent attempt. Weeks are planning slots, not automatic promotions. Repeat or split a week when its exit test fails. Project estimates overlap the scheduled lab hours; they are not extra hours to add to the total.

## Phase milestones

| Weeks | Phase | Core evidence | Gate |
| --- | --- | --- | --- |
| 1 to 4 | Shared C and tools | B01 tests and independent parser/ring exercise | G01 |
| 5 to 10 | Linux system software | B02 B03 B04 with error and shutdown tests | G02 |
| 11 to 22 | Cross builds images and kernel drivers | B05 I01 I02 I03 plus matching-kernel checks | G03 |
| 23 to 28 | MCU and RTOS foundations | I05 real RTOS host port and physical-port plan | G04 |
| 29 to 40 | Image integration sensors performance updates | I04 A01 A02 A03 and production review | G05 |
| 41 to 50 | Two integrated capstones | C01 and C02 acceptance tests and defenses | Capstone tests |
| 51 to 52 | Hiring evidence | Final practical primary-track mock and portfolio | G06 |

The complete week-by-week records include prerequisites, objectives, lesson links, exercises, revision and exit tests in `Weekly_Roadmap.csv` and the companion workbook. Update the evidence column with your own files, logs and commits. Supplied implementation test logs describe the package, not your proficiency.

## Prerequisite map

M01 tools enables M02 C. M02 enables M03 parsing and M04 build/link ownership. M05 architecture and M06 POSIX require C competence. M07 concurrency follows POSIX resource handling. M08 cross/boot follows build tools and architecture. M09 kernel contexts follows concurrency and boot. M10 drivers follows kernel lifetimes; M11 hardware subsystems follows drivers. M12 MCU startup follows linking/architecture; M13 RTOS follows concurrency and MCU foundations. M14 image systems follows cross/boot and services. M15 debugging runs throughout and deepens after concurrency/kernel study. M16 production follows image integration. M17 capstones combine protocol, RTOS and recovery. M18 AI assists every phase only after the independent attempt.

Use the prerequisite diagram in the handbook to identify parallel study: you can study MCU startup while a Linux image builds, but do not begin a concurrent driver before you can explain synchronization and object lifetime.

## Full path and role emphasis

For embedded Linux roles, give extra repetitions to M06, M07, M14, M15 and M16, with C01 as the main defense. For kernel/BSP roles, deepen M08 through M11 and obtain real driver runtime/hardware evidence before claiming board bring-up skill. For firmware roles, deepen M12 and M13 and complete the physical MCU port, timing and peripheral measurements. The same completed B01 parser can support all three tracks, while the evidence standards for specialized claims differ.

The optional C02 AI extension is scheduled as a choice in week 49. If core control or protocol acceptance is weak, use that week for correction and verification. Optional machine learning must not displace required control behavior.

## Minimum interview path

This is a revision and gap-closure path for someone who already passes G01 and basic POSIX work. It is not a beginner-to-kernel-developer promise.

| Week | Shared work | Primary-track extension | Required evidence |
| --- | --- | --- | --- |
| 1 | Diagnostic C pointers bounds integer rules | Review target JD and label explicit requirements | Independent C exercise and gap list |
| 2 | I/O partial progress errors timeouts | Linux service or MCU framing | One fault-tested parser/I/O task |
| 3 | Threads ownership shutdown | Kernel contexts or RTOS queues | Race/deadlock diagnosis and fix |
| 4 | Build cross tools debugging | Boot/DT for BSP or startup/linker for MCU | Reproducible build and failure explanation |
| 5 | One project end-to-end | I02 for kernel I05 for firmware C01 for applications | Demo with limits and test evidence |
| 6 | Timed coding and debugging | Mock for chosen role | Correct solution under stated tool rules |
| 7 | Architecture and failure design | JD-specific gaps | Design answer with explicit tradeoffs |
| 8 | Final mock and portfolio | Targeted remediation | No unresolved critical correctness failure |

At 10 to 12 hours per week, this path provides roughly 80 to 96 hours. It leaves substantial gaps in production depth, hardware integration and secondary tracks. Use the separate 30-day calendar only after foundations, and prioritize the actual interview scope if time is shorter.

## Remediation

If G01 fails, repeat ownership and parser exercises with smaller inputs, use a memory diagram and add boundary tests before proceeding to concurrency. If G02 fails, reduce the system to one pipe or queue, trace every descriptor/buffer owner and test shutdown. If G03 fails, pause new driver features, annotate context and lifetime, compile against the exact source, then reproduce in a disposable guest. If G04 fails, simplify to two tasks and one bounded queue, measure progress and define the watchdog. If G05 fails, enumerate persisted states and inject a failure after each state transition. If a capstone fails, map the failure to its lowest responsible interface and correct the requirement/test before adding features.

For a failed gate, record the failed requirement, evidence, root-cause hypothesis, targeted exercise and retest date. Retest with changed data after at least one study session of separation. Do not average away a memory safety, concurrency, unsafe-command or evidence-integrity failure.
