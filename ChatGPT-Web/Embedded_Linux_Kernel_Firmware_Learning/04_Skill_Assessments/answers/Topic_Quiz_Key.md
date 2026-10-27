# Topic quiz marking key

Use the indicated spoken answer as a core mechanism and the four criteria as the rubric. Accept equivalent correct reasoning. An answer that repeats the wording but cannot handle its follow-up is not strong evidence; ask for a changed example.

## T01 Module M01

**Q041:** Preprocessing expands includes and macros, compilation produces assembly, assembly produces objects, and linking resolves references and creates an executable or library. **Marking:** 1 point each: stages; plausible symbol causes; object inspection; declaration/definition distinction.

**Q049:** Define a reliable good/bad test, identify known boundary revisions, and bisect while controlling environment. Mark untestable commits explicitly rather than labeling them good. **Marking:** 1 point each: classifier; environment; intermittent handling; exposure versus root cause.

**Q050:** Warnings catch many suspicious constructs, static analysis reasons about paths without normal execution, and sanitizers instrument executed paths to detect selected runtime violations. **Marking:** 1 point each: tool roles; separate builds/support; coverage limitation; recorded evidence.

## T02 Module M02

**Q001:** An array owns a sequence of elements; a pointer holds an address. An array parameter is adjusted to a pointer, so pass its length separately. **Marking:** 1 point each: object distinction; parameter adjustment; length contract; correct one-past rule.

**Q006:** No. The two modifications of the same scalar are unsequenced in C11, so the expression has undefined behavior and no valid universal output. **Marking:** 1 point each: UB classification; unsequenced conflict; valid rewrite; distinction from unspecified order.

**Q018:** Volatile does not make an increment atomic or establish synchronization between threads. Use a mutex or a suitable C atomic operation, depending on the required invariant. **Marking:** 1 point each: race; atomic RMW; relaxed limit; multi-field invariant.

## T03 Module M03

**Q023:** Track head, tail, and count. Push only when count is below capacity; pop only when count is nonzero. Advance indices modulo the fixed capacity. **Marking:** 1 point each: invariant; wraparound; no mutation on failure; concurrency qualification.

**Q028:** Require at least one decimal digit and reject signs, whitespace, and trailing characters under the stated grammar. Before each step, ensure the next multiply-add fits. **Marking:** 1 point each: grammar; precheck; status contract; maximum and malformed cases.

**Q039:** Turn the alarm on at or above the high threshold and off at or below the low threshold. Between thresholds, preserve the prior alarm state. **Marking:** 1 point each: two transitions; hold band; boundary tests; invalid/stale-data policy.

## T04 Module M04

**Q043:** An API defines source-level interfaces and behavior. An ABI defines binary conventions such as calling convention, data layout, symbol naming, and object format. **Marking:** 1 point each: API/ABI distinction; concrete conventions; compatibility checks; kernel qualification.

**Q044:** Resource Acquisition Is Initialization ties resource ownership to an object's lifetime so destructors release resources on every normal scope-exit path, including exceptions. **Marking:** 1 point each: lifetime cleanup; move-only ownership; nonthrowing destructor; explicit error tradeoff.

**Q047:** Many traditional linkers scan archives to satisfy unresolved symbols known at that point, so objects that require symbols commonly precede their providing archives. **Marking:** 1 point each: unresolved-symbol scan; example order; linker qualification; dependency reasoning.

## T05 Module M05

**Q051:** A process provides a resource context and address space; threads execute within it and share many resources. A file descriptor is a per-process integer handle to an open file description. **Marking:** 1 point each: process; thread sharing; open description; descriptor reuse consequence.

**Q101:** An application processor commonly runs a rich OS with virtual memory and external memory; a microcontroller commonly emphasizes integrated peripherals, bounded resources, and direct or RTOS-controlled execution. **Marking:** 1 point each: practical distinction; hardware verification; software services; portable boundary.

**Q102:** An MMU can translate virtual addresses and enforce permissions through mappings. An MPU typically applies access permissions and attributes to regions without providing the same general virtual-memory model. **Marking:** 1 point each: translation; region protection; limitations; non-CPU access caveat.

## T06 Module M06

**Q052:** A successful read or write may transfer fewer bytes than requested. Track progress, handle interruptions and nonblocking conditions, and treat EOF according to the operation's contract. **Marking:** 1 point each: partial progress; errors; stream framing; absolute deadline.

**Q055:** Convert the signal into normal control flow, stop accepting work, notify blocked workers, drain or discard by policy, join them, then release shared resources. **Marking:** 1 point each: safe notification; blocked-worker wake; join-before-free; deadline policy.

**Q059:** A monotonic clock is intended for measuring elapsed time without civil-time jumps. Use a single deadline and recompute remaining time after interruptions or partial progress. **Marking:** 1 point each: elapsed-time clock; absolute deadline; suspend semantics; conversion/expiry.

## T07 Module M07

**Q071:** The condition variable is a notification mechanism; shared state is the truth. Protect the predicate with a mutex and wait in a loop that rechecks it after waking. **Marking:** 1 point each: predicate; atomic wait transition; while loop; correct notification scope.

**Q074:** A high-priority task can wait for a lower-priority lock owner while unrelated medium-priority work delays that owner. Priority inheritance temporarily raises the owner's effective priority. **Marking:** 1 point each: three-task mechanism; temporary boost; limits; measurement.

**Q077:** A flag expresses intent but does not wake blocked I/O, condition waits, or sleeping threads. Cancellation must reach each blocking point and define ownership of unfinished work. **Marking:** 1 point each: wake paths; synchronized state; completion race; lifetime barrier.

## T08 Module M08

**Q103:** A platform may execute immutable ROM, early firmware, a bootloader, the kernel, and init or a service manager. Each stage initializes enough state and verifies or loads the next as configured. **Marking:** 1 point each: stages; responsibilities; board qualification; stage-specific evidence.

**Q105:** Device tree describes hardware connections and properties according to bindings; the driver implements the device's behavior using those resources and subsystem interfaces. **Marking:** 1 point each: description; binding contract; resource dependencies; validation.

**Q108:** A sysroot provides the target-facing headers and libraries used by a cross toolchain. It prevents accidental use of incompatible host interfaces when building target applications. **Marking:** 1 point each: sysroot role; ABI/libc match; ELF check; dependency isolation.

## T09 Module M09

**Q112:** Process context runs on behalf of a schedulable task, although held locks or disabled preemption can restrict it. Hard interrupt context cannot perform operations that may sleep. **Marking:** 1 point each: task context; IRQ restriction; held-lock caveat; deferred-context selection.

**Q114:** A mutex is a sleeping lock for eligible task contexts. A conventional spinlock protects short non-sleeping sections; PREEMPT_RT changes spinlock_t semantics, so configuration matters. **Marking:** 1 point each: sleeping distinction; context; RT qualification; per-state locking contract.

**Q116:** Managed resources simplify release when a device detaches or probe fails. They do not automatically stop work, timers, open-file users, or callbacks that still reference those resources. **Marking:** 1 point each: managed scope; asynchronous users; teardown order; open-file lifetime.

## T10 Module M10

**Q123:** A user pointer must be accessed through the appropriate user-copy APIs, with validated sizes and error handling. Direct dereference can fault or violate the kernel's access rules. **Marking:** 1 point each: user-copy boundary; return semantics; context; state/initialization policy.

**Q125:** Not necessarily: another consumer may have consumed the data. Readiness is not a reservation. A nonblocking read should then return EAGAIN under the documented contract. **Marking:** 1 point each: race distinction; nonblocking outcome; shared predicate; wait registration.

**Q129:** Mark the device disconnected, prevent new hardware operations, wake blocked users, and return the documented EOF or error behavior. Keep backing state alive until existing references are released. **Marking:** 1 point each: disconnected state; wake behavior; references; teardown tests.

## T11 Module M11

**Q134:** IIO commonly separates raw readings and conversion attributes so userspace can interpret samples consistently without requiring floating-point work in the kernel. **Marking:** 1 point each: raw/scale; units/offset; buffer layout; calibration test.

**Q137:** A DMA address is the address the device uses after the platform's mapping rules, potentially including an IOMMU. It is not generally a cast of the CPU pointer. **Marking:** 1 point each: domains; DMA API/type; mask; mapped-segment semantics.

**Q139:** System suspend coordinates a broader system sleep transition. Runtime suspend idles an individual device while the system remains active, subject to dependencies and usage references. **Marking:** 1 point each: scope; usage/dependencies; state restoration; transition tests.

## T12 Module M12

**Q141:** Startup establishes the stack and vector handling as required by the architecture, initializes writable data, clears zero-initialized storage, and performs necessary runtime setup before main. **Marking:** 1 point each: stack/vector; data copy; bss clear; toolchain/platform qualification.

**Q143:** Identify and acknowledge the event as required, capture minimal necessary data, and notify deferred processing through an ISR-safe mechanism. Keep execution bounded and respect interrupt-priority rules. **Marking:** 1 point each: acknowledge; bounded capture; ISR-safe notification; measured overload behavior.

**Q147:** Feed the watchdog only when required subsystems demonstrate timely health under a defined policy. A dedicated feeder that runs regardless of failures can mask a dead system. **Marking:** 1 point each: useful progress; supervision; reset evidence; special-state behavior.

## T13 Module M13

**Q153:** An interrupt cannot block waiting for a task-owned resource, and ordinary mutex ownership/priority-inheritance semantics are designed for tasks. Use an appropriate ISR-safe signaling or data-transfer mechanism. **Marking:** 1 point each: no blocking/ownership; FromISR; priority restrictions; data ownership.

**Q157:** Specify framing, length bounds, byte order, version, message type, sequence or request ID, integrity check, timeouts, and recovery behavior. Define ownership and state transitions on both sides. **Marking:** 1 point each: wire contract; command semantics; reset/replay; fault tests.

**Q158:** The MCU should enforce a local deadline for motion commands and transition to a defined stopped or disabled state when commands become stale, independent of Linux remaining alive. **Marking:** 1 point each: MCU-local deadline; state transition; stale/replay tests; safety scope.

## T14 Module M14

**Q171:** Choose from required customization, package workflow, reusable metadata, team familiarity, supported BSPs, and maintenance needs. Buildroot and Yocto can both produce embedded Linux systems through different models. **Marking:** 1 point each: requirements; models; maintenance/resource tradeoff; validated target support.

**Q172:** A layer groups related metadata; a recipe describes how to obtain, configure, build, install, and package a component; an image selects a filesystem composition and related outputs. **Marking:** 1 point each: three roles; layer separation; append/version; task diagnostics.

**Q173:** Store the product's board configuration, custom package definitions, overlays or post-build steps, and documented external-tree metadata so the build can be reproduced from versioned inputs. **Marking:** 1 point each: external organization; versioned inputs; package/overlay boundary; image test.

## T15 Module M15

**Q081:** Capture a short syscall trace and loop counters. Look for repeated readiness or hangup returns followed by zero-byte reads, unhandled errors, or a retry path with no wait. **Marking:** 1 point each: trace hypothesis; EOF interpretation; state transition; regression/CPU check.

**Q088:** A loop that does work and then sleeps a fixed period adds its work and scheduling delay to every cycle. Schedule against successive absolute deadlines instead. **Marking:** 1 point each: relative-drift mechanism; absolute schedule; overrun policy; latency measurements.

**Q098:** Inspect use of the DMA API, transfer direction, map/unmap or sync transitions, and ownership between CPU and device. CPU virtual addresses are not interchangeable with DMA addresses. **Marking:** 1 point each: ownership; API mapping; address domains; target coherency test.

## T16 Module M16

**Q176:** Signed update verification authenticates an update package before accepting it under the update policy. Verified boot checks the boot chain or loaded components according to a trust model at startup. **Marking:** 1 point each: two boundaries; trust anchor; uncovered modification; key/recovery plan.

**Q177:** Boot the candidate slot, run meaningful bounded health checks, and confirm only when required functions and persistent-state compatibility meet the defined policy. Retain rollback until that decision. **Marking:** 1 point each: bounded meaningful health; attempt/rollback; inactive-slot write; data compatibility.

**Q180:** Define workload, faults, metrics, duration, and pass conditions, then preserve evidence. Long duration is useful only when it exercises relevant states and detects failure meaningfully. **Marking:** 1 point each: specified workload; metrics; targeted faults; recovery/integrity criteria.

## T17 Module M17

**Q181:** Keep acquisition and local timing on the MCU, transfer versioned framed telemetry over one primary link, and let Linux validate, persist, expose health, and manage remote integration. **Marking:** 1 point each: boundary architecture; bounded interface; recovery; measurable acceptance.

**Q186:** Choose a bounded frame with version, type, length, session/request identity, payload, and CRC, plus escaping or another unambiguous framing method and explicit deadlines. **Marking:** 1 point each: full wire contract; semantics; bounded recovery; vectors/compatibility.

**Q190:** Extract pure parsing and state logic for host tests, compile target code against pinned interfaces, simulate the communication peer, and use supported QEMU targets for integration where meaningful. **Marking:** 1 point each: portable logic; target build/simulation; explicit gaps; risk-based hardware plan.

## T18 Module M18

**Q191:** Describe the problem, your decisions and implementation work, where AI assisted, how you verified suggestions, and which results you personally reproduced. Separate generated code from demonstrated competence. **Marking:** 1 point each: truthful role; decisions; independent verification; live understanding.

**Q196:** Check the exact target source and documentation, determine whether the helper exists in another version or subsystem, and redesign against supported APIs rather than forcing an undeclared symbol. **Marking:** 1 point each: source check; version/context; supported redesign; focused validation.

**Q197:** A model may repeat the implementation's assumptions, test only happy paths, or assert the same incorrect formula. Use independently specified behavior and fixed external vectors where appropriate. **Marking:** 1 point each: independent oracle; edge cases; mutation limit; independent competence.
