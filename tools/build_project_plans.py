from build_program import ROOT, write, table

projects = [
('B01','01_Basic','Embedded C utility library',12,'M01; D01 attempted','Portable ISO C11; Windows or Linux host; no board',
 'S01–S03/S05','Caller-owned bytes → bounded ring and exact-frame codec → owned packet',
 'Reject new bytes on full; unchanged outputs on failed parse; no concurrent use without a lock',
 'Ring, bit helpers, checked multiplication, CRC codec, standalone tests and runner',
 'Strict warnings; queue model capacities 1–17; every payload length; malformed lengths; CRC mutation; sanitizer run',
 'All defined tests pass; learner explains invariants and independently implements peek',
 'B01 implementation delivered and host/sanitizer evidence available; independent learner grade not assessed',
 'Replace bytes with fixed records; add explicit drop metrics; compare reserved-slot design',
 'Why not serialize a struct? Where are output mutation and concurrency contracts enforced?'),
('B02','01_Basic','Linux process and resource inspector',10,'M01/M02/M03; Linux host ready','Ubuntu 24.04 x86-64; later AArch64 user space',
 'S04–S07','CLI arguments → proc enumeration → per-process snapshot → text/JSON output',
 'A process may exit or deny access mid-read; report partial snapshot and continue; bound file content and numeric conversion',
 'C CLI, /proc fixture adapter, stable output schema, Make build, help and exit-code policy',
 'Own test process; disappearing PID; malformed fixture; long comm field; denied access; no fd growth over repeated scans',
 'Correct PID/state/RSS units against same-time observations; errors named; memory/FD counts stable',
 'Plan only; complete source and Linux validation pending',
 'Add configurable sample interval and JSON lines; distinguish PID reuse with start time',
 'Why is /proc not a stable database snapshot? Why does RSS differ from virtual size?'),
('B03','01_Basic','UART terminal and framed-protocol tool',18,'B01; M03; Linux PTY support','Ubuntu 24.04 PTYs; hardware serial later',
 'S03/S07/S18','stdin or binary request → framed codec → nonblocking termios fd → bounded stream decoder',
 'Maintain write offset; absolute monotonic deadline; EOF/disconnect closes cleanly; reject bad frames and boundedly resynchronize',
 'C CLI, termios save/restore, poll state machine, frame accumulator, Python PTY fault tests',
 'Fragment every byte boundary; short writes/EAGAIN; bad CRC; noise; oversized length; silent peer; peer close; SIGTERM',
 'No busy spin on timeout/disconnect; exactly one accepted message per valid frame; bounded memory; original terminal state restored',
 'Plan only; complete source, PTY fixtures and serial evidence pending',
 'Add sequence/ACK/version handshake and explicit duplicate policy; support a documented USB serial adapter',
 'Why does one write not correspond to one read? What happens when readiness races?'),
('B04','01_Basic','Multithreaded sensor simulator and logger',16,'B01; M04','Ubuntu 24.04 pthreads; simulated values only',
 'S03/S08/S20','Periodic producers → bounded shared queue → logger → bounded file rotation',
 'One mutex protects queue/stop state; condition predicates in while loops; stop wakes all waiters; declare drain or discard',
 'C pthread program, deterministic sensor generator, overload counters, shutdown protocol, tests',
 'Queue capacity one; stalled consumer; producers blocked on full; idle consumer; repeated start/stop; supported race-tool run',
 'No deadlock or leaked thread/FD; accounted samples equal consumed+dropped; documented shutdown bound under test fixture',
 'Plan only; complete source, race-tool and Linux evidence pending',
 'Add one-writer per sensor ownership; compare queue policies without claiming lock-free correctness',
 'How are lost wakeups prevented? Is stop a predicate or an event?'),
('B05','01_Basic','Cross-compiled application running in QEMU',12,'B01/M02/M05; Linux environment','AArch64 QEMU virt; Linux guest selected by pinned Buildroot lane',
 'S04/S09/S10','Host source → cross compiler/sysroot → AArch64 ELF → guest execution/gdbserver',
 'Fail with useful architecture/interpreter diagnostics; isolate guest files and avoid host library leakage',
 'Small target info/packet verifier app, cross build file, deployment/start scripts and debug walkthrough',
 'readelf architecture/interpreter check; correct run; wrong-architecture fixture; missing-loader fixture; remote breakpoint',
 'Target reports architecture; deterministic packet result; matching symbols stop at source breakpoint',
 'Plan only; cross compiler, rootfs, guest and debug execution pending',
 'Compare static and dynamic deployment; record SDK package metadata',
 'How does the sysroot differ from an emulator? Why can an existing file report no such file?'),
('I01','02_Intermediate','Custom Buildroot appliance',22,'B02/B03/B05; M06','Buildroot 2026.08.1 qemu_aarch64_virt_defconfig; kernel 6.18.7',
 'S10/S11/S19/S21','Pinned source/package → Buildroot image → init-started telemetry → separate persistent configuration',
 'Validate configuration, keep last good value, bounded logs, recover missing config; avoid writing immutable rootfs',
 'br2-external tree, custom package with license/hash, overlay/init script, defconfig, persistence format and boot script',
 'Clean build/boot; package startup; first boot; reboot; malformed config; interrupted write; disk full',
 'Clean checkout reproduces accepted image behavior; source inputs/config hashes recorded; valid config survives restart',
 'Plan only; upstream target file inspected, image/package implementation and builds pending',
 'Read-only rootfs, reproducibility comparison, legal-info/SBOM artifacts using supported release tools',
 'Which change requires a full rebuild? How do configuration and image state differ?'),
('I02','02_Intermediate','Kernel character driver and user-space client',26,'G2/G3; M07/M08','Same configured Linux 6.18.7 AArch64 guest; matching module build output',
 'S12/S13/S20','Client read/write/poll → misc character device → bounded kernel queue/wait state',
 'Serialize state; explicit blocking/nonblocking semantics; handle user-copy faults; module ownership and no deferred UAF',
 'Complete module/Kbuild, ABI header where needed, userspace exercise client, multi-client/invalid-pointer fixtures',
 'Empty/full; partial ops; O_NONBLOCK EAGAIN; wake and signals; poll readiness; bad user pointers; concurrent clients; load/unload loop',
 'Read/poll state agrees; no invalid user dereference, sleep-in-atomic or unowned resource; guest logs clean under tests',
 'Plan only; complete driver/client and guest validation pending',
 'Add fixed-width versioned ioctl only for a justified operation; use appropriate existing subsystem for real devices',
 'Why can copy_to_user sleep? How does an open descriptor affect module lifetime?'),
('I03','02_Intermediate','Device-tree GPIO/interrupt platform driver',24,'I02; M09; electronics and selected board docs','QEMU context tests plus BeagleBone Black Rev C physical path; board kernel pin pending',
 'S09/S14','Device-tree node/binding → probe GPIO descriptor/IRQ → deferred event → standard observable interface',
 'Handle deferred resources; avoid sleeping bus operations in hard IRQ; stop IRQ/work before freeing state; bounded debounce',
 'Binding YAML, driver using descriptors/managed resources, board-specific DT change, event test client and unbind test',
 'Wrong compatible; missing GPIO; deferred provider; edge bursts/bounce; work pending during unbind; real input transitions',
 'Binding validates; supported probe/error paths clean; physical IRQ count/timing documented separately from simulated tests',
 'Plan only; exact board image, pins, wiring, binding and source pending; no physical validation',
 'Compare gpio-keys/gpio-leds first; implement custom driver only for a justified teaching event protocol',
 'What does devm clean up automatically, and what asynchronous activity must you stop first?'),
('I04','02_Intermediate','Custom Yocto telemetry image',32,'I01; M10; sufficient Linux disk/RAM','Poky yocto-5.0.14; MACHINE=qemuarm64; separate lineage from Buildroot',
 'S10/S11/S19/S21','Own layer/recipe → package + image → service → SDK-built client',
 'Explicit dependencies and license checks; immutable metadata inputs; avoid downloads from arbitrary moving branches',
 'Layer.conf, application recipe, image recipe/config, service unit and enablement, build configuration and SDK instructions',
 'Parse/build; boot/service status; runtime dependency missing fixture; SDK compile; clean configuration replay; license manifest',
 'Image starts intended service; client from generated SDK runs; layers/revisions/config and actual versions archived',
 'Plan only; tag/build environment, recipe implementation and boot/SDK checks pending',
 'Compare sstate cache versus reproducibility; add application package feed only with a maintenance policy',
 'How do build-time DEPENDS and runtime RDEPENDS differ? What is a layer versus an image?'),
('I05','02_Intermediate','RTOS MCU firmware connected to Linux',30,'M11/M12; B03; G1/G2','Zephyr v4.2.0 native_sim/native/64; NUCLEO-F446RE hardware path pending exact tool lock',
 'S16–S18','Sample task → bounded queue → serial task → B03 Linux tool; supervisor evaluates health',
 'Single UART owner; queue overload metrics; watchdog feed requires progress of all required tasks; disconnect resets protocol session',
 'west manifest/config, C firmware tasks and UART abstraction, deterministic simulation adapter, Linux bridge, protocol tests',
 'Queue overflow; stalled sampling; serial reconnect; invalid CRC/version; priority inversion review; hardware watchdog reset/fault record',
 'Simulation acceptance passes independently; MCU timing/stack/watchdog and UART evidence separately recorded before hardware claim',
 'Plan only; complete firmware/startup walkthrough/protocol bridge and simulation/MCU tests pending',
 'DMA-backed UART and bounded ISR handoff after baseline; measure stack high-water with supported tools',
 'Why should a timer interrupt not blindly feed the watchdog? What does native_sim not validate?'),
('A01','03_Advanced','Sensor driver using the IIO subsystem',28,'I03; M13; ADXL345 datasheet','ADXL345 I2C on BeagleBone Black Rev C; exact board kernel/image pin pending',
 'S09/S14/S15','Bus register reads → IIO channels/raw/scale → userspace acquisition → fault report',
 'Check identity and supported config; propagate bus failures; serialize mode changes; release active work before teardown',
 'Read existing ADXL345 driver; implement isolated educational IIO variant or a justified tested patch; register fixture tests and client',
 'Known signed sample fixtures; wrong identity; bus NACK/timeout; invalid config; unbind; orientation sanity and reported scale',
 'Use documented IIO ABI; known raw-to-unit conversions correct; physical orientation agrees within stated device/test tolerances',
 'Plan only; no invented wiring; exact breakout, pinmux, driver implementation and physical readings pending',
 'Add triggered buffer/interrupt and runtime PM only after raw acquisition/lifetimes pass',
 'Why IIO rather than a custom ioctl? How do raw value, scale and physical units relate?'),
('A02','03_Advanced','Linux latency and performance investigation',24,'B04/I02; M14','Recorded Linux guest configuration; physical follow-up for real-time claims',
 'S08/S12/S20','Defined workload → monotonic timestamps/traces → hypothesis → one controlled change → rerun',
 'Bound trace overhead; preserve raw samples; distinguish scheduler latency, queueing and processing time; no universal worst-case claim',
 'Reproducible workload and load generator, ftrace/perf collection scripts, analysis script, raw CSV and report',
 'Idle/loaded repetitions; warmup; timestamp ordering; observer overhead; contention seeded fixture; regression workload',
 'Report sample count/duration/config, p50/p95/p99/max and raw data; show trace-supported explanation and comparative experiment',
 'Plan only; no benchmark run, speedup or latency number asserted',
 'Compare PREEMPT_RT on a separately pinned build; distinguish emulated timing from physical deadline evidence',
 'Why is a measured maximum not a proven upper bound? How do you control confounders?'),
('A03','03_Advanced','Signed A/B update and rollback system',28,'I01; M15; boot/persistence understanding','RAUC 1.13; disposable QEMU disk; bootloader/version integration still to be selected and locked',
 'S11/S19/S21','Signed compatible bundle → inactive slot → candidate boot attempts → health → commit or rollback',
 'Never overwrite active known-good slot; verification before activation; bounded attempts; durable metadata; key kept out of image',
 'Disk layout, RAUC config/bundle manifest, development signing script, boot-state integration, health gate, interruption harness',
 'Bad signature; wrong target; full disk; partial install; reset before/after activation; failed health; attempt exhaustion; successful commit',
 'Every defined interrupted transition yields old or candidate bootable state; unsigned/wrong-target rejected; unhealthy candidate rolls back',
 'Plan only; no complete updater/boot integration or disk fault tests delivered',
 'Separate production key custody/rotation, anti-rollback requirements and secure boot chain; do not confuse these with bundle signing',
 'What durable state allows rollback after power loss? Which component consumes the attempt counter?'),
('C01','04_Capstone','Industrial monitoring and edge gateway',50,'B03/I01/I05/A03; G2/G3/G5','Linux QEMU appliance + MCU simulator first; chosen Linux/Nucleo boards later',
 'S07/S08/S11/S18/S19/S21/S22','One serial path → validated telemetry → bounded log + health snapshot; persistent config and signed image update',
 'Monotonic freshness, bounded storage, validated atomic config replacement, reconnect with epoch, health-gated rollback',
 'Integrated image, serial service, MCU/sim endpoint, config schema/store, health CLI, CI fixtures and acceptance report',
 'Nominal sample; bad CRC/version; link loss; duplicate/old frame; worker stall; disk full; corrupt config; interrupted/rejected update',
 'All C01-R requirements in CAPSTONE_REQUIREMENTS.md have reproducible evidence and independent architecture defense',
 'Plan only; dependency integrations, complete source/config, fixtures and capstone execution pending',
 'Add MQTT/SocketCAN only if target JD needs it; optional anomaly score remains outside health-critical acquisition',
 'What is the primary failure boundary? Which evidence distinguishes a transport fault from a sensor fault?'),
('C02','04_Capstone','Linux–MCU robot control and diagnostics platform',54,'B03/I05/A02; C01 integration methods; M16','Deterministic simulated differential-drive plant first; no connected actuators',
 'S08/S16/S17/S18/S20/S22','Linux goal/planner → leased bounded command → MCU control/state → simulated plant → diagnostic telemetry',
 'MCU owns control cadence and lease/safety state; Linux loss triggers safe output; reject stale sequence/epoch; inference never blocks control',
 'Linux supervisory app, firmware control core, simulated plant, deterministic clock/fault runner, diagnostic UI/CLI and acceptance tests',
 'Nominal trajectory; dropped/reordered/stale commands; Linux exit; sensor freeze; control overrun; reset epoch; malformed packet',
 'All C02-R criteria pass in simulation; independent defense; hardware gaps documented without production safety claims',
 'Plan only; complete simulation/control/firmware reference implementations and execution pending',
 'After explicit hardware integration design: current-limited test rig, documented driver/encoder, emergency-stop and independent safety review',
 'What stops motion if Linux hangs? Which simulated timing results cannot establish physical safety?'),
]
assert len(projects)==15
assert sum(p[3] for p in projects)==386
rows=[]
overview='# Exactly 15 projects — complete plan, staged implementations\n\nThe catalog contains 5 basic, 5 intermediate, 3 advanced and 2 capstone projects. Total estimated implementation effort is 386 hours; lesson/revision/assessment time is additional. Only B01 currently has a complete reference implementation. Other project folders intentionally contain specification documents, not source stubs masquerading as implementations.\n\n'
for p in projects:
    pid,level,title,hours,pre,target,skills,flow,failure,minimum,tests,accept,status,extensions,interview=p
    folder=pid+'_'+title.replace('–','_').replace('/','_').replace(' ','_').replace('—','_').replace(',','')
    if pid=='B01':folder='B01_Embedded_C_Utility_Library'
    path='07_Projects/'+level+'/'+folder
    rows.append({'ID':pid,'Level':level,'Project':title,'Hours':hours,'Prerequisites':pre,'Target':target,'Skills':skills,
                 'Folder':path,'Implementation status':status,'Acceptance':accept})
    overview+=f'- [{pid} — {title}](../{path}/README.md): {hours} h; {status}.\n'
    if pid=='B01':continue
    write(path+'/README.md',f'''
# {pid} — {title}

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: {level.split('_',1)[1]}. Estimated effort: {hours} hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: {minimum}. Prerequisites: {pre}. Role/skills mapping: {skills} in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: {target}. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
{flow}
```

State/failure obligations: {failure}. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: {minimum}. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: {tests}.

Exit criteria: **{accept}.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: {status}. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: {interview}

Extensions after minimum acceptance: {extensions}. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
''')
write('01_Learning_Roadmap/PROJECT_CATALOG.md',overview)
table('01_Learning_Roadmap/project_plan.csv',rows)

write('07_Projects/04_Capstone/CAPSTONE_REQUIREMENTS.md',r'''
# Capstone requirements and acceptance design

These are authored requirements and proposed test criteria, not executed results. The two capstones will reuse earlier components but add integration, versioned contracts, failure boundaries and fresh acceptance evidence. All tests currently pending.

## C01 — Manageable industrial gateway

Scope: one MCU or simulator sending one sensor stream at 10 Hz over one serial framing protocol to one Linux service. The gateway stores bounded JSON-line telemetry, persistent configuration and an observable health snapshot. A 10 Hz rate is a design target, not measured capability. Remote cloud, dashboards and multiple fieldbuses are extensions.

| ID | Requirement and rationale | Acceptance input and expected result |
|---|---|---|
| C01-R1 | One versioned serial communication path; all frames length/CRC checked | 100 nominal fixture frames plus corruption; only valid frames counted and errors observed |
| C01-R2 | Fresh/stale/disconnected states based on monotonic time | Stop sender; stale within configured 500 ms plus declared scheduling margin; reconnect requires compatible session |
| C01-R3 | Persistent config schema version with range validation | Restart preserves accepted config; unknown version/bad range leaves previous accepted config active |
| C01-R4 | Durable replacement policy | Inject stop before/after write, file fsync, rename and directory fsync; restart selects valid old/new config, never malformed content |
| C01-R5 | Bounded resource consumption | Fixture overload for 30 minutes; queue/log bounds maintained; consumed+dropped/error accounting reconciled |
| C01-R6 | Observable health | Health output names build/protocol/session, last valid sample age, dropped frames, queue utilization and update state |
| C01-R7 | Signed update and health-gated activation | Wrong signature/target rejected; unhealthy candidate exhausts attempts and returns to known-good slot |
| C01-R8 | Automated integration regression | Fresh isolated test setup runs nominal, bad CRC/version, link loss, disk-full, config-corruption and interrupted-update cases |
| C01-R9 | Honest reproduction and defense | New checkout reproduces accepted behavior; report identifies reused/supplied and learner-authored components and physical gaps |

Durability depends on filesystem/storage guarantees; file+directory fsync is a designed protocol to test on selected storage, not a universal promise against defective hardware. Do not add networking before these core requirements pass. Planned integration adds health-state policy, persistence and update semantics beyond a serial demo.

## C02 — Simulated robot with explicit Linux/MCU boundary

Linux owns goals/planning/diagnostics. MCU owns a 100 Hz control state machine, bounded output, command lease, watchdog progress and safe transition. A deterministic plant supplies wheel/state measurements. No real motors are connected. Proposed periods and thresholds below are requirements to evaluate in simulation and later re-establish on hardware.

| ID | Requirement and rationale | Acceptance input and expected result |
|---|---|---|
| C02-R1 | Explicit states INIT, DISARMED, ARMED, FAULT | Outputs zero until initialization and explicit arm conditions hold; no startup actuation |
| C02-R2 | Command lease max 200 ms in MCU monotonic domain | Linux exit/link loss expires lease; command setpoint becomes zero within one 10 ms control tick after expiry in deterministic simulation |
| C02-R3 | Bounded and versioned commands | Out-of-range, malformed, unknown version, replayed/stale sequence rejected; defined wrap and reset-epoch semantics |
| C02-R4 | Independent control cadence | Add Linux delays and slow optional inference; MCU control scheduling decisions unchanged in the deterministic model |
| C02-R5 | Sensor freshness and overrun fault | Freeze sensor or exceed configured control budget; latch FAULT and zero command; controlled explicit recovery only |
| C02-R6 | Diagnostic evidence | Timestamp state transitions and accepted/rejected commands; test output includes source/build/config/seed |
| C02-R7 | Testable simulated dynamics | Known stationary/straight/turn inputs meet specified model invariants; integration tests expose overshoot/error rather than inventing motion accuracy |
| C02-R8 | Optional AI does not alter safety boundary | Missing/slow/invalid score falls back to deterministic threshold diagnostic; commands never depend on inference completion |
| C02-R9 | Declared production gaps | Document real sensor latency, actuator inertia, electrical limits, independent e-stop, hazard analysis, power behavior and physical timing tests still required |

Zero command is a software state, not proof of physical stopping distance or safety certification. Hardware integration is a separate stage requiring actual motor driver, encoder, current/voltage limits, mechanical rig and an independently reviewed stop path. Keep simulation results separate from measurements on NUCLEO-F446RE and any Linux board.
''')

if __name__=='__main__':print('Created exactly 15 project plans; B01 implementation preserved')
