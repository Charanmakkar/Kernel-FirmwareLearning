from build_program import write, table, DATE

refs=[
('R01','C11 committee draft N1570','https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf','C11','Language-rule reference; draft, not claimed to be the latest ISO edition'),
('R02','Buildroot AArch64 virt defconfig','https://raw.githubusercontent.com/buildroot/buildroot/2026.08.1/configs/qemu_aarch64_virt_defconfig','2026.08.1','Inspected target selection and Linux 6.18.7 pin'),
('R03','QEMU virt machine documentation','https://www.qemu.org/docs/master/system/arm/virt.html','moving master','Virtual board scope; generated run script/version still to be locked'),
('R04','Yocto system requirements','https://docs.yoctoproject.org/5.0.14/ref-manual/system-requirements.html','5.0.14','Supported hosts and build prerequisites; no build performed'),
('R05','Kernel circular-buffer concepts','https://docs.kernel.org/6.12/core-api/circular-buffers.html','6.12','Conceptual comparison only; not selected driver API baseline'),
('R06','Kernel rationale on volatile','https://docs.kernel.org/6.12/process/volatile-considered-harmful.html','6.12','Concurrency rationale; not a C11 atomic API reference'),
('R07','Clang AddressSanitizer','https://clang.llvm.org/docs/AddressSanitizer.html','moving docs','Capabilities and limitations; actual compiler recorded separately'),
('R08','Clang UndefinedBehaviorSanitizer','https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html','moving docs','Supported checks vary; no complete correctness proof'),
('R09','GCC atomic builtins','https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html','moving docs','Compiler atomic support; M01 uses standard C discussion, not kernel atomics'),
('R10','Zephyr native_sim','https://docs.zephyrproject.org/4.2.0/boards/native/native_sim/doc/index.html','4.2.0','Simulation target and 64-bit qualifier verified'),
('R11','Zephyr Nucleo F446RE board','https://docs.zephyrproject.org/latest/boards/st/nucleo_f446re/doc/index.html','latest','Board capabilities checked; v4.2.0 board compatibility still pending'),
('R12','ST Nucleo-64 user manual UM1724','https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf','Rev 17 September 2025','Board family/revision reference; inspect exact board and jumpers before wiring'),
('R13','Kernel GPIO descriptor consumer','https://docs.kernel.org/6.18/driver-api/gpio/consumer.html','6.18','Descriptor interface preferred over legacy integer GPIO'),
('R14','IIO introduction','https://docs.kernel.org/6.18/driver-api/iio/intro.html','6.18','Subsystem fit for accelerometer project'),
('R15','ADXL345 datasheet','https://www.analog.com/media/en/technical-documentation/data-sheets/adxl345.pdf','Rev G','Selected sensor; breakout schematic and wiring not yet verified'),
('R16','RAUC basics','https://rauc.readthedocs.io/en/v1.13/basic.html','1.13','Signed update framework; no boot integration test claimed'),
('R17','Active kernel releases','https://www.kernel.org/releases.html','live status','6.18 and 6.12 longterm lines; status can change'),
('R18','GNU ld linker scripts','https://sourceware.org/binutils/docs/ld/Scripts.html','moving docs','Sections/memory-map reference'),
('R19','GDB manual','https://sourceware.org/gdb/current/onlinedocs/gdb.html/','moving docs','Debugger reference; selected executable version must be recorded'),
('R20','Linux read syscall','https://man7.org/linux/man-pages/man2/read.2.html','Linux man-pages','Return/EOF/error behavior'),
('R21','Linux write syscall','https://man7.org/linux/man-pages/man2/write.2.html','Linux man-pages','Short I/O and persistence distinctions'),
('R22','Linux poll syscall','https://man7.org/linux/man-pages/man2/poll.2.html','Linux man-pages','Readiness/error/timeout semantics'),
('R23','POSIX condition-variable wait','https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html','POSIX manual mirror','Predicate and mutex semantics; inspect implementation support'),
('R24','Kernel dynamic DMA mapping guide','https://docs.kernel.org/6.18/core-api/dma-api-howto.html','6.18','CPU/physical/device addresses and ownership'),
('R25','Buildroot manual','https://buildroot.org/downloads/manual/manual.html','moving manual','Architecture/packaging overview; release-matched manual required during implementation'),
('R26','Kernel lock types','https://docs.kernel.org/6.18/locking/locktypes.html','6.18','Context restrictions and PREEMPT_RT differences'),
('R27','Kernel workqueues','https://docs.kernel.org/6.18/core-api/workqueue.html','6.18','Deferred process context; teardown must quiesce work'),
('R28','Kernel RCU explanation','https://docs.kernel.org/6.18/RCU/whatisRCU.html','6.18','Read/copy/update and deferred reclamation concepts'),
('R29','Kernel platform driver model','https://docs.kernel.org/6.18/driver-api/driver-model/platform.html','6.18','Matching/probe/remove model'),
('R30','Kernel memory and user-access APIs','https://docs.kernel.org/6.18/core-api/mm-api.html','6.18','User access and allocation contracts'),
('R31','Kernel device-tree binding guidelines','https://raw.githubusercontent.com/torvalds/linux/v6.18/Documentation/devicetree/bindings/writing-bindings.rst','v6.18','Hardware description and binding ABI rules'),
('R32','Zephyr threads reference source','https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/v4.2.0/doc/kernel/services/threads/index.rst','v4.2.0','Thread ownership/lifecycle; API support must be checked per target'),
('R33','Kernel ftrace','https://docs.kernel.org/6.18/trace/ftrace.html','6.18','Tracing reference; no measured latency results yet'),
('R34','SPDX overview','https://spdx.dev/learn/overview/','live documentation','Software bill of materials and license metadata context'),
('R35','Kernel selftests','https://docs.kernel.org/6.18/dev-tools/kselftest.html','6.18','Kernel regression methodology'),
('R36','LiteRT for Microcontrollers','https://developers.google.com/edge/litert/microcontrollers/overview','live documentation','Optional MCU inference context; no runtime selected/benchmarked'),
('R37','BeagleBone Black board','https://www.beagleboard.org/boards/beaglebone-black','live board page','Cortex-A8 platform and board documentation entry point'),
]
table('09_References_and_Resources/sources.csv',[{'Reference ID':i,'Title':title,'URL':url,'Version context':version,'Access date':DATE,'Access result':'opened/read via web tool','Use and qualification':use} for i,title,url,version,use in refs])
text='# Primary references and research notes\n\nAccessed 27 October 2026. These are official project/language/board/component documents and Linux man-pages; no employer JD has been sampled. This is targeted primary-source research performed for release 1. It is not a claim that an external long-running research job exists or that every referenced tool was executed. Code and worked examples are original educational material.\n\n'
for i,title,url,version,use in refs:text+=f'- **{i}** [{title}]({url}) — {version}. {use}.\n'
text+='''
## Decisions supported by the sources

R02 explicitly selects Linux 6.18.7 for the selected Buildroot tag. That is a coherent teaching image baseline; it does not prove this patch release is the most secure choice today. The moving Buildroot manual is used for orientation only; implementation must use the selected source tree's own manual and generated build records.

R10 establishes that native_sim is a host executable and does not model a particular MCU. R11/R12 support selecting a Nucleo family board but do not establish that the exact versioned firmware, jumpers or UART routing have been validated. R03 establishes that QEMU virt is not a physical board. These distinctions constrain what later evidence can claim.

R13/R14 support descriptor-based GPIO and an established sensor subsystem. A01 will study the existing ADXL345 driver before producing an isolated teaching variant or justified patch; the program does not recommend deploying a duplicate driver for supported hardware.

R16 supports using an established signed-update framework. The program adds a required boot-attempt/health/recovery test design; that design is an engineering inference to validate, not a successful RAUC integration result.

Several attempted URLs were unavailable: older 6.12 GPIO/DMA paths, a guessed Buildroot 2026.02.6 target URL, docs.rauc.io for the selected version, and the rendered versioned Zephyr thread page. No technical claim relies on those failed fetches. Working official alternatives are recorded above. Source branches, current docs and accessed dates are never substitutes for build hashes.

## How to research a version-sensitive answer

Find the selected release's API declaration, implementation, in-tree callers, Kconfig/build constraints and official documentation. Record a source revision and a minimal compile/use test. If docs/source differ, explain the discrepancy and follow the selected source contract. Check device datasheet and board schematic separately: a chip capability does not identify a board pin or jumper route. A tutorial from a different kernel is a hypothesis source, not final authority.
'''
write('09_References_and_Resources/REFERENCES.md',text)

days=[
('C ownership','Reimplement bounded endian read; defend valid region/lifetime','M01; Q001–Q010'),
('C integers','Fix overflow and signed/unsigned boundary cases','M01; Q011–Q020'),
('Data structures','Draw ring states and test capacity one/wrap','B01; Q021–Q030'),
('Tools','Trace compile/link; inspect ELF symbols and loader','M02; Q031–Q040'),
('Linux basics','Run permissions/process/proc practical in scratch area','B02; Q041–Q050'),
('I/O','Implement/defend partial-read and partial-write state','B03; Q051–Q060'),
('Mock 1','60-minute C/Linux mock; review two critical weaknesses','D01; G1/G2'),
('Concurrency','Queue predicate, mutex ownership and shutdown interleavings','B04; Q061–Q070'),
('Architecture','Draw address domains, cache/DMA ownership and IRQ context','M05; Q071–Q080'),
('Cross build','Explain sysroot/interpreter mismatch from ELF evidence','B05; Q081–Q085'),
('Boot','Localize kernel/rootfs/init failure with boot-stage diagram','I01; Q086–Q090'),
('Kernel contexts','Classify allocations/locks in each callback context','M07; Q091–Q100'),
('Driver ABI','Defend copies, poll readiness and open-file lifetime','I02; Q101–Q110'),
('Mock 2','Kernel/BSP mock with a probe/unbind review','G4; I02/I03'),
('Device tree','Explain compatible/resources, binding and deferred probe','I03; Q111–Q120'),
('Bus/subsystem','Review I2C/SPI/IIO unit conversion and error paths','A01; Q121–Q130'),
('MCU startup','Explain reset/vector/data/bss/linker/stack and fault record','I05; Q131–Q140'),
('RTOS','Analyze priority inversion and watchdog progress policy','I05; Q141–Q150'),
('Protocol','Version/sequence/CRC/deadline recovery fault matrix','B03/I05; Q151–Q160'),
('Images','Defend Buildroot package and Yocto layer/recipe/SDK','I01/I04; Q161–Q170'),
('Mock 3','Firmware timing and serial-fault mock','G5; I05'),
('Debugging','Reproduce one unknown fault with evidence-driven hypotheses','A02; Q171–Q180'),
('Reliability','Persist config safely; explain signing/rollback/trust chain','A03; Q181–Q190'),
('Design 1','Gateway requirements/interfaces/bounds/failure tradeoffs','C01; Q191–Q195'),
('Design 2','Robot control boundary, stale command and safe state','C02; Q196–Q200'),
('Portfolio','Run fresh demo; check every resume metric against artifact','08_Portfolio_and_Job_Readiness'),
('Behavioral','Practice honest contribution/failure/unknown answers','INTERVIEW_PLAYBOOK.md'),
('Mock 4','Selected role 60-minute mock; retest weakest category','G7'),
('Target JD','Reorder matrix by actual explicit requirements; close one gap','reference_skills_matrix.csv'),
('Final revision','Explain three failures without notes; verify demo and rest','INTERVIEW_PLAYBOOK.md'),
]
table('05_Interview_Strategy/revision_30_days.csv',[{'Day':n,'Minutes':90,'Focus':focus,'Independent task':task,'Links/IDs':links,'Exit evidence':'Actual attempt; rubric; one weakness; next retest','Status':'not started'} for n,(focus,task,links) in enumerate(days,1)])

write('05_Interview_Strategy/INTERVIEW_PLAYBOOK.md',r'''
# Interview preparation playbook

Prerequisite for the 30-day revision calendar: completed foundations and usable project evidence. It budgets 90 minutes/day, 45 hours total (roughly 10.5 hours/week). It is revision, not a replacement for first-time kernel or firmware learning. Question/module IDs may include planned material; use the bank index and module delivery catalog to identify what is available.

## Read the role before preparing

Extract exact JD requirements and separate required from desired. Choose EL, KD or FW depth, map each explicit requirement to code/test/defense evidence and identify prerequisites. Ask meaningful role clarifications in the actual interview: userspace versus kernel ownership, target board/kernel, real-time boundaries, update responsibility and required depth. Do not infer a company's exact interview process from general industry patterns.

## Answer structures that expose engineering judgment

Concept: state the definition in one sentence, its boundary/guarantee, one concrete example, then the relevant exception or version qualification. For volatile: describe observable accesses, say what synchronization it does not establish, give a target MMIO context, then identify the correct shared-data primitive.

Coding: clarify inputs/ownership/limits/error behavior; state invariants; propose a small correct implementation; test normal/boundary/invalid/failure input; discuss complexity and resources. Do not optimize away clarity before correctness. If asked for code output, classify undefined/unspecified/implementation-defined behavior before giving a number. A specific compiler observation must be labeled an observation.

Debugging: separate symptom from cause; state two or three hypotheses; choose the cheapest discriminating experiment; inspect an actual return code/trace; minimize; fix; add regression; explain remaining uncertainty. “I would add logs everywhere” is weaker than identifying a state boundary and the values needed to test one hypothesis.

Design: clarify functional requirements, rate/size/deadline/failure budgets and trust boundaries. Draw components/interfaces and owners; specify state/recovery, persistence, update and observability; estimate capacity with stated assumptions; name tradeoffs; define acceptance. Do not let a box diagram replace error handling or timing analysis.

Unknown: say which part you know, identify what is uncertain, reason from a known contract and name the source/experiment you would use. For a kernel callback, “I would verify the signature and context in our pinned tree” is credible; invented API confidence is not.

## Project defense and contribution

Prepare a two-minute account: problem/constraints; architecture/interface; your exact contribution; one serious failure; evidence/fix; limitation and next test. Distinguish authored code, adapted code, supplied reference and independent extension. Use STAR (Situation, Task, Action, Result) only with true events; if no industry example exists, use an honest course/project example. Results may be qualitative when no measurement exists.

Example bullet template, fill only with actual evidence: “Implemented [specific component] for [target/constraint]; validated [named normal/fault cases] using [actual tool]; measured [value/workload] in [report path].” Before independent contribution, say you studied or executed supplied material. Never fill a template with invented uptime, latency, performance percentage or ownership.

## Weekly mock and score review

Calendar days 7/14/21/28 reserve one 60-minute mock plus 30-minute review. Rotate C/Linux, KD, FW then chosen target role. Use a peer or AI interviewer, but record assistance and do the scored code/explanation independently. Score with the gate rubric and block critical failures. Keep recurring-weakness rows: topic, failed reasoning, minimal counterexample, remediation, changed-input retest, retention result. Do not simply rehearse the previous answer.

Revision sheets: (1) object lifetime/size/integer bounds; (2) read/write/EOF/EINTR/EAGAIN; (3) lock/context/owner/teardown table; (4) boot/ELF/sysroot; (5) MCU task/ISR/deadline/watchdog; (6) signature/slot/health/recovery. For each sheet write one invariant, one bug and one test from your own project.

Interview day: confirm time/timezone and allowed tools; ensure a known-good demo with local logs; have source/build IDs ready; check audio/editor; read the actual JD; state assumptions aloud; ask before using AI; preserve confidentiality; and end with known limitations. Do not covertly use assistance where independent work is expected. No learning plan guarantees selection.
''')

write('06_AI_Integration/AI_ASSISTED_ENGINEERING.md',r'''
# AI as a learning and engineering assistant

Use the same loop for every workflow: **attempt independently → request a hint → implement → compile/test → explain without AI**. Record where assistance changed your implementation. An AI-produced file does not demonstrate your competence or establish a working API.

| Workflow | Context to supply | Reusable request | Verification | Common failure |
|---|---|---|---|---|
| Tutor | Target level, own explanation, small misconception | “Ask three questions that expose gaps in my explanation; give one hint at a time, no solution yet.” | Re-derive concept and implement changed example independently | Fluent explanation conceals missing preconditions |
| Source reading | Exact version/commit, header and relevant call sites | “Trace owner/context/error path; cite exact supplied symbols; label unknowns.” | Open definitions and callers in pinned tree; compile tiny use | Invented APIs or stale signatures |
| Documentation lookup | Selected release, architecture and needed behavior | “Find primary references; quote at most a short excerpt; separate documented facts from inference.” | Open cited page/source; confirm release and access date | Link exists but does not support claim |
| Design review | Requirements, rates, state diagram, resource/lock owners | “List concrete failure interleavings and one test for each; prioritize contract violations.” | Walk interleavings and fault fixtures; revise requirements | Generic best practices without an executable test |
| Implementation plan | Interfaces, constraints, current code and accepted design | “Propose smallest complete change with cleanup and verification steps; do not invent dependencies.” | Review API availability; compile incrementally | Large patch hides partial error handling |
| Code review | Small diff, context/ownership contract, selected APIs | “For each suspected bug show input/interleaving and source line; separate certainty and hypothesis.” | Reproduce or reason from documented contract; inspect false positives | Confident but impossible bug scenario |
| Bug hypotheses | Actual error/log, exact command/config, expected behavior | “Rank three causes and propose a cheap discriminating experiment; do not claim diagnosis yet.” | Run one experiment and update hypothesis | Plausible causal story from insufficient trace |
| Tests/edge cases | Input contract and current tests | “Find missing normal/boundary/invalid/fault cases; avoid mirroring my algorithm.” | Independent oracle/model; prove fixture reaches defect | Tests repeat same wrong implementation |
| Build/log analysis | Compiler output, tool versions, relevant snippets | “Identify first meaningful failure and version-dependent assumptions; propose minimal reproduction.” | Run command; preserve full log; verify dependencies | Fixing downstream noise instead of first cause |
| Interview practice | Target track/JD, real project facts, allowed assistance | “Interview one question at a time; score reasoning and evidence; do not invent experience.” | Independent timed task and no-AI explanation | Memorized answer mistaken for competence |
| Documentation | Actual code/test artifacts, audience and limitations | “Write reproducible instructions; label authored/built/run/hardware-pending separately.” | Fresh checkout and link/command audit | Polished docs claim unrun tests passed |

## Gate a generated change

1. Check every API against the chosen headers/source version, not another model response. Confirm callback signatures, configuration dependencies and permissible context.
2. Inspect all allocation/error/cleanup paths, user pointers, integer bounds, concurrency and asynchronous teardown.
3. Compile with strict warnings. Use static analysis supported by the toolchain; warnings are hypotheses to understand, not dismiss blindly.
4. Run meaningful normal/boundary/invalid/failure tests; model a simpler independent oracle where useful. Use sanitizers where supported, with separate race and memory instrumentation if required.
5. Review the actual diff, test logs and coverage limits. Explain the implementation without opening the model answer. Retain evidence and update the matrix only for demonstrated work.

Check invented kernel APIs by searching the pinned tree for the declaration and in-tree users. A real function name can still be wrong for the selected kernel, target configuration or callback context. A patch that compiles can still leak resources, use freed state or mis-handle DMA ownership. Tests do not replace a resource-lifetime argument.

Provide the smallest relevant code/log context. Remove credentials, tokens, keys, customer data and confidential source you are not authorized to share. Follow actual employer/provider policy before sending private code. A model prompt is not a secret vault. Keep production signing keys out of training examples, repositories and chat. During independent assessments/interviews, obey the declared tool rules and disclose assistance honestly.
''')

write('06_AI_Integration/OPTIONAL_EMBEDDED_ANOMALY_EXTENSION.md',r'''
# Optional capstone extension — anomaly diagnostics

Status: complete experiment design; executable training/inference implementation and measurements pending. This extension cannot replace core C/Linux/kernel/firmware deliverables.

Start with C01 or C02 sensor/health telemetry. Choose one diagnostic question, such as identifying a simulated sensor that becomes stuck or increasingly noisy. Log timestamp, raw value, operating mode, load, fault injection ID, session ID and reset epoch. Do not infer ground truth solely from the model's output. Use deterministic injected faults first, then separately collect real device sessions with documented conditions.

Baseline: per-mode range/freshness/rate-of-change checks with thresholds chosen on training data. Evaluate false alarms and missed fault events before adding machine learning. A simple window-feature linear/logistic model can be a first learned comparator; a neural network is not an automatic improvement. Use an established runtime only if its model/operator/memory constraints justify it. R36 documents MCU inference context; no supported MCU runtime/model build is claimed here.

Split data by session/run/device *before* making overlapping windows, for example 60/20/20 percent train/validation/test sessions. These are proposed split proportions, not data that has been collected. Fit normalization only on training data. Tune features/thresholds on validation, freeze them, then evaluate held-out test sessions once. Randomly splitting adjacent overlapping windows leaks near-duplicate information and makes accuracy look better than deployment behavior.

Run Linux inference in a lower-priority userspace worker reading copied samples. It publishes a bounded-age diagnostic score through a queue; it must never block acquisition or the MCU control loop. A possible MCU deployment requires a supported toolchain/runtime, fixed memory budget and measured interference; it is a separate exercise. Preserve deterministic stale-data and lease/watchdog rules regardless of AI availability.

Fallback: use the baseline when model loading fails, score is invalid/stale, inference exceeds the declared budget or distribution checks warn. Mark the score unavailable and keep the control/health contract. Do not implement safety-critical control by waiting for an inference result.

Acceptance report template: dataset/session IDs and hashes; preprocessing fitted state; baseline and learned-model versions; confusion matrix, precision/recall, false alarms per hour, missed faults and detection delay by fault type; model bytes; peak resident/arena memory; CPU utilization; p50/p95/p99 inference latency; sample count and host/target configuration. Compare baseline and model on the same held-out sessions. All result fields remain **not measured** until executed. No accuracy/latency estimate is presented as a measurement.

Maintenance: version data/model/features together, monitor invalid/stale scores and input drift, retain rollback to baseline, and re-evaluate changed hardware/operating conditions with new session-separated tests. A simulated anomaly classifier does not establish predictive maintenance performance on an industrial machine.
''')

write('08_Portfolio_and_Job_Readiness/PORTFOLIO_EVIDENCE.md',r'''
# Portfolio and job-readiness evidence

Each portfolio project needs: problem/constraints; target and exact source/tool versions; architecture and interfaces; your contribution versus supplied code; reproducible build/run; tests including failures; actual evidence; limitations; short demo and next improvement. One credible complete project is stronger evidence than a list of unbuilt plans.

Use an evidence ledger with columns claim, artifact path, target/build ID, command, actual observation, measurement conditions, remaining limitation. Capture source hashes with logs. Keep authored, build verified, host executed, emulator executed and specified hardware executed separate. Copying output from a README is not execution evidence.

Readiness self-check: can you rebuild from a clean checkout, explain ownership/context for every callback, debug a changed input, show a real failure test, state the selected version contract, and defend your contribution without AI? If not, remediate before claiming independent proficiency. Complete the actual JD matrix rather than collecting unrelated technology names.

Resume examples with blanks intentionally awaiting evidence: “Implemented [own component] on [actual target]; tested [specific fault set] and documented [actual measurement/result].” If you only ran the supplied B01 project, say “Executed and studied a supplied bounded C library; independently added [only if true] and tested [artifact].” Do not claim production deployment or personal authorship of this package.

Recommended first evidence: D01 independent record, B01 strict/sanitizer logs, E-M01 source/tests, and B01 peek extension with a no-AI explanation. The pre-supplied host logs establish the package author's execution only; they do not assess you.
''')

if __name__=='__main__':print('Authored primary reference register, revision calendar, interview playbook, AI and portfolio guidance')
