# Threads, locks and shutdown

## Q061 — Implement a mutex/condition-variable bounded queue.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Predicate correctness, ownership and shutdown of both wait sets.

**Spoken answer:** Protect queue and stop predicates with one mutex; wait in while loops; modify predicates before notifying.

**Deeper explanation/example:** Producer waits while full and not stopped; consumer while empty and not stopped. Define drain/discard policy and broadcast on stop so blocked producers and consumers can exit.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Use if instead of while because one signal means one item.

**Follow-up:** What if two consumers wake for one item?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Predicate correctness, ownership and shutdown of both wait sets. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q062 — Why can a condition wait return with no usable item?

**Tags:** All; foundation; debugging/code review; debugging/scenario. **Assesses:** Explain wake/reacquire/recheck interleaving.

**Spoken answer:** Wakeups can be spurious, or another thread may consume the item before this waiter regains the mutex.

**Deeper explanation/example:** The predicate is shared state, not the notification count. Recheck under the same mutex; an event-only mental model creates races.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** A signaled condition variable permanently stores one item.

**Follow-up:** When is broadcast necessary?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explain wake/reacquire/recheck interleaving. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q063 — Publish an immutable configuration snapshot between threads.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Separate publication from reclamation and justify simplest correct design.

**Spoken answer:** Use mutex-protected ownership or a correct atomic publication plus a safe reclamation scheme.

**Deeper explanation/example:** Release/acquire can publish initialized fields, but swapping a pointer does not keep the old snapshot alive for readers. A reference/lifetime strategy is still required.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** An atomic pointer eliminates use-after-free.

**Follow-up:** How would you choose mutex versus RCU-like design?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate publication from reclamation and justify simplest correct design. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q064 — The queue deadlocks only during shutdown when full. What inspect?

**Tags:** All; foundation; debugging/code review; debugging/scenario. **Assesses:** Concrete interleaving and lifetime-safe shutdown sequence.

**Spoken answer:** A producer may wait forever after the consumer stops, or stop may not wake the full-queue wait set.

**Deeper explanation/example:** Draw stop, queue occupancy and each waiter. Set stop under the lock, broadcast relevant conditions, define whether to drain, then join before destroying synchronization objects.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Set a volatile stop flag and sleep before freeing the queue.

**Follow-up:** Which order should joins and queue destruction follow?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Concrete interleaving and lifetime-safe shutdown sequence. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q065 — What is priority inversion?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Distinguish scheduling inversion from deadlock and resource contention.

**Spoken answer:** A high-priority task blocks on a resource held by a lower-priority task, which can be delayed by medium-priority work.

**Deeper explanation/example:** Priority inheritance can reduce that blocking but does not shorten long critical sections, prevent deadlock or fix interrupt masking. Actual mutex support/protocol must be verified.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Raise every task to the highest priority.

**Follow-up:** When does priority ceiling help?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Distinguish scheduling inversion from deadlock and resource contention. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q066 — Two individually correct mutex-protected functions deadlock together. Why?

**Tags:** All; foundation; debugging/code review; debugging/scenario. **Assesses:** Graph-based cause and a verified ordering change.

**Spoken answer:** Their composed lock acquisition order may form a cycle or callback reentry may acquire an already-held lock.

**Deeper explanation/example:** Write the lock graph and enforce a global order or reduce nesting. Use a minimal two-thread schedule to demonstrate the cycle; timeouts alone do not make the design correct.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Add another mutex around each function.

**Follow-up:** How do callbacks affect lock-order analysis?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Graph-based cause and a verified ordering change. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q067 — Why is volatile count++ unsafe across threads?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Separate access visibility, atomicity and ordering.

**Spoken answer:** It is a read-modify-write without atomicity or a happens-before relation; conflicting unsynchronized access can be a C data race.

**Deeper explanation/example:** A mutex protects a compound invariant. An atomic counter can count independently but may not protect associated payload fields. Tooling can find some races, not prove absence.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Volatile forces memory access, therefore it synchronizes threads.

**Follow-up:** Would relaxed fetch_add publish a queue entry?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate access visibility, atomicity and ordering. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q068 — Design a single-producer/single-consumer ring publication protocol.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Both publication and reuse ordering plus restricted concurrency model.

**Spoken answer:** Assign one writer to each index; publish produced slots with release/acquire and protect slot reuse with the reverse ordering.

**Deeper explanation/example:** Specify index width/wrap and no third writer. A count field written by both sides can defeat the design. Start with a mutex implementation unless the lock-free requirement is justified.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Make head and tail volatile and rely on x86.

**Follow-up:** Which access proves the consumer finished reading a slot?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Both publication and reuse ordering plus restricted concurrency model. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q069 — A test passes under a debugger but races in release. What next?

**Tags:** All; foundation; debugging/code review; debugging/scenario. **Assesses:** Reproducible evidence and a synchronization argument independent of timing.

**Spoken answer:** Treat debugger timing as an interference change; reproduce with controlled stress and supported race instrumentation, then reason about shared accesses.

**Deeper explanation/example:** Do not fix by inserting sleeps. Preserve the original failing workload/configuration and test a schedule that exposes the missing synchronization.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Optimization is broken, so ship -O0.

**Follow-up:** Can a race tool miss the bug?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Reproducible evidence and a synchronization argument independent of timing. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.

## Q070 — When should a thread own a resource exclusively?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Bounded handoff, overload/failure behavior and measurable tradeoffs.

**Spoken answer:** When single ownership simplifies state and avoids contended access, such as one UART writer or one logging task.

**Deeper explanation/example:** Other tasks send bounded messages to the owner; define queue overload and shutdown. Ownership avoids some locks but still requires synchronization at the handoff and lifecycle boundaries.

**Assumptions/version:** POSIX userspace unless stated; kernel and RTOS primitives have different contracts.

**Common incorrect answer:** Single-owner design removes every concurrency issue.

**Follow-up:** What if the owner stalls?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bounded handoff, overload/failure behavior and measurable tradeoffs. [Learning: M04](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m04). References: R23; R26.
