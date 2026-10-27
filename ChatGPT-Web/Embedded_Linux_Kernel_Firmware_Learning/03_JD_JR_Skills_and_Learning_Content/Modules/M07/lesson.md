# M07 Concurrency synchronization and IPC

## Objectives and prerequisites

Prerequisites: M06.

Protect invariants, use condition variables correctly, reason about deadlock and choose an IPC mechanism for a measured need.

## Lesson


A data race is not merely a bad interleaving observed in a test. In C, conflicting unsynchronized accesses can invalidate language-level reasoning. Protect a shared invariant, not just isolated assignment statements. A queue's count, indices and contents must agree; locking only count leaves the queue inconsistent.

A mutex provides exclusive access under its contract. A condition variable waits for a predicate protected by a mutex. The wait atomically releases that mutex and blocks, then reacquires it before returning. Recheck the predicate in a loop because wakeups can be spurious and another consumer can take the item first. A notification is not a stored unit of data; the predicate records the state. [COND]

For a bounded producer-consumer queue, the producer waits while full and not stopping; the consumer waits while empty and not stopping. Shutdown changes a state variable while holding the mutex and wakes every class of waiter. Decide whether consumers drain queued items or exit immediately. Join threads before freeing queue storage. A thread that is asleep forever is still a resource-lifetime bug.

Deadlock prevention begins with a global lock order or with a design that avoids holding multiple locks. Logging and callbacks can acquire hidden locks. Calling an unknown callback while holding an internal lock exports a dangerous lock-order dependency. Keep critical sections small, but do not move an operation outside protection if it needs the invariant. Priority inheritance may reduce priority inversion for supported mutexes; it cannot fix a circular wait or an unbounded critical section.

Atomics are appropriate when a well-defined atomic invariant is simpler than a mutex. For a publication flag, release/acquire can connect initialization with observation when used correctly. Relaxed operations maintain atomicity of the atomic object but do not publish unrelated data. Learning to recognize these contracts matters before writing a lock-free queue. Use a mutex-based queue first and measure before replacing it.

Pipes provide streams, Unix sockets provide local communication with useful connection semantics, shared memory gives direct access but still requires synchronization and lifetime rules, and message queues provide bounded messages under their particular APIs. Serialization costs and failure isolation can be worth more than avoiding one copy. For a small telemetry application, a Unix socket with explicit framing often gives a clearer ownership boundary than shared-memory structures with process-shared synchronization.


## Worked lab and expected behavior


Run B04's multithreaded logger tests. Change producer rate and queue capacity. Record produced, consumed and dropped counts according to the chosen policy; the counts must reconcile. Request shutdown while empty and while full. Expected acceptance is no deadlock, no use-after-free, bounded memory and the documented drain policy.

If ThreadSanitizer is available and supported, run it in a separate build; it cannot generally be combined with AddressSanitizer in one executable. A tool failure caused by host memory mapping is not a clean race result. Diagnose a hang with all thread backtraces and identify the predicate each blocked thread expects. [GCC13]


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain why volatile cannot repair the queue. Draw one deadlock cycle and remove it. Interview bank: concurrency and scenario questions.

## Mastery checklist

- Name the protected invariant.
- Demonstrate shutdown in all waiting states.
- Explain spurious wakeup and lost notification.
- Separate atomicity, ordering and lifetime.

## Primary references

[COND] POSIX condition-wait manual. [GCC13] GCC sanitizer options. [KLOCK] Kernel lock context comparison.
