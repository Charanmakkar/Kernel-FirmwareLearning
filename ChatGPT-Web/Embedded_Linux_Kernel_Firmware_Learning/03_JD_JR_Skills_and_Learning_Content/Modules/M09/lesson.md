# M09 Kernel execution contexts and resource lifetimes

## Objectives and prerequisites

Prerequisites: M07 M08.

Choose context-appropriate allocation and locks, reason about deferred work and prevent teardown races.

## Lesson


Kernel code can run in process context, interrupt-related contexts and deferred execution. The permitted operations depend on the context and configuration. A sleepable operation is forbidden when the context cannot schedule. `GFP_KERNEL` can reclaim and sleep; an atomic allocation flag changes behavior but does not make a poorly designed interrupt path reliable. Preallocate or defer work when the design permits it. kmalloc and vmalloc have different contiguity properties; neither authorizes bypassing the DMA API. [KALLOC]

For the baseline non-PREEMPT_RT driver examples, a spinlock protects short state updates where sleeping is not allowed, while a mutex protects sleepable task-context work. PREEMPT_RT changes `spinlock_t` semantics; `raw_spinlock_t` retains strict spinning behavior. State the selected configuration before asserting generic lock behavior. Disabling local interrupts alone does not serialize another CPU. [KLOCK]

A workqueue moves work to a worker context, but queuing it does not automatically solve lifetime. A device can be removed while work is pending or running. A typical teardown plan first prevents new work and user access, then disables or synchronizes event sources, cancels/drains deferred work, unregisters interfaces and releases storage in the required order. The exact order depends on which callbacks may requeue work and which resources they need. [WORK]

Managed device resources simplify probe failure and detach cleanup, but they do not grant indefinite validity to pointers stored in open files or asynchronous callbacks. Review every long-lived reference and its owner. Probe often builds state before publishing an interface; a partially initialized object must not be visible to users. Error paths should unwind only resources that were actually acquired. [DRIVER]

Read-copy-update, or RCU, can allow efficient concurrent readers under a particular read-side discipline. A writer publishes a replacement and waits for an appropriate grace period before freeing an old object that readers may still see. RCU does not automatically serialize writers or make arbitrary object mutation safe. At junior level, be able to explain publication and delayed reclamation; implement it only where the data structure and subsystem justify it. [RCU]

Modules execute with kernel privilege. A bad pointer can crash the system and a subtle race can corrupt unrelated data. Use a disposable matching-kernel VM, preserve logs and enable suitable debugging options. A successful object compile checks syntax and some API usage, not locking, teardown or real peripheral behavior.


## Worked lab and expected behavior


Study I02's read/write and wait paths. Mark every shared field, its lock, and every point that can sleep. Then draw a lifetime timeline from module load through open, concurrent I/O, close and unload. If a file operation can outlive device removal, identify the reference that keeps its state alive or the rule preventing removal.

Use kernel `W=1` build checks and sparse/checkpatch where available; record which tools actually ran. In a guest, run simultaneous readers/writers and unload only after descriptors are closed. Debugging extensions include lockdep and KASAN, selected for the kernel and target. A compiler warning is resolved by checking the contract, not by casting away the type mismatch.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Why can GFP_KERNEL sleep? Does devm solve every use-after-free? What changes under PREEMPT_RT? Interview bank: kernel locking and lifecycle.

## Mastery checklist

- Annotate sleepable and atomic paths.
- Identify every asynchronous owner.
- Design teardown before initialization.
- Separate build evidence from runtime evidence.

## Primary references

[KALLOC] Kernel allocation guide. [KLOCK] Kernel locking. [WORK] Workqueues. [DRIVER] Driver model. [RCU] RCU fundamentals.
