# M15 Debugging tracing and performance

## Objectives and prerequisites

Prerequisites: M06 and M07 for user-space work; M09 is additionally required for kernel-specific sections.

Form falsifiable bug hypotheses, interpret crash evidence and measure latency without confusing averages with guarantees.

## Lesson


Start a debugging note with expected behavior, actual behavior, reproducibility and the smallest relevant environment. Separate facts from hypotheses. Change one discriminating variable or add one observation that distinguishes the leading explanations. A fix that makes a failure disappear once is not a root-cause argument; demonstrate the mechanism and add a regression test.

GDB shows the stopped execution state. Backtraces identify frames; locals and register values add context, but optimized builds can omit variables or transform control flow. Preserve the exact executable and debug information that produced a core. A symbol file from another build can create a convincing false trace. In multithreaded hangs, inspect every thread and identify wait dependencies. [GDB]

strace observes system calls and signals, making it useful for permissions, missing files, repeated timeouts and blocking I/O. It changes timing and cannot show every application-level operation. perf samples execution and performance events where permissions and hardware support allow it. ftrace exposes kernel events and function-related tracing, including scheduling and latency paths, subject to kernel configuration. Trace the subsystem that can answer your question instead of enabling everything and drowning the event of interest. [FTRACE]

AddressSanitizer and UndefinedBehaviorSanitizer help user-space memory and selected language errors; ThreadSanitizer targets races in supported builds. KASAN detects kernel memory safety problems with modes dependent on architecture/configuration. KCSAN samples for races and its lack of a report is not a proof of absence. Instrumentation changes memory/timing, so compare like-for-like builds and do not present instrumented timing as production performance. [GCC13] [KASAN] [KCSAN]

For performance, specify metric, workload, warmup, duration, repetitions and environment before optimizing. Report a distribution: count, median, high percentiles and maximum observed delay. The maximum observed is not a proven worst case. CPU utilization and end-to-end latency can move in different directions; batching reduces overhead but can increase waiting. A02 measures wakeup delay on the host and records this limitation.

A kernel oops contains the fault location, process context, registers, call trace and kernel build information. First preserve it, then resolve symbols against the matching build. An oops can taint or damage state, so do not assume continued execution remains reliable. Reproduce in a disposable guest with the smallest workload and the appropriate detector.


## Worked lab and expected behavior


Run A02's baseline and contention experiments with its fixed input and output schema. Compare identical sample counts and workloads. Explain the expected mechanism before changing the implementation. Retain raw measurements and the summarizing script. If tracing is unavailable due to permissions, say it was not executed and use an available observation without claiming equivalent coverage.

Take a broken-code challenge in the assessment folder. Use one hypothesis per step, record the evidence and write the smallest regression test that fails before the fix. A test that only asserts the current implementation's internal choices is weaker than one that checks the externally required behavior.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

What does a backtrace prove? Why does a clean sanitizer run not prove safety? How would you investigate a tail-latency regression? Interview bank: debugging and performance.

## Mastery checklist

- Preserve exact build and raw evidence.
- Falsify a hypothesis with an observation.
- Report latency distributions honestly.
- Add a regression test tied to the failure.

## Primary references

[GDB] GDB backtraces. [FTRACE] Kernel ftrace. [KASAN] KASAN. [KCSAN] KCSAN. [GCC13] GCC sanitizers.
