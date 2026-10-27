# Kernel contexts, allocation and concurrency

## Q091 — What determines whether kernel code may sleep?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Classify caller/context and each potentially sleeping operation.

**Spoken answer:** The current execution context and held primitives determine whether sleeping is allowed, not merely the function's name.

**Deeper explanation/example:** Hard-IRQ and atomic sections cannot perform operations that may block. Task context can also become non-sleepable while holding relevant locks or disabling preemption/interrupts.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** All kernel code can sleep because it runs privileged.

**Follow-up:** What about a threaded IRQ handler?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Classify caller/context and each potentially sleeping operation. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q092 — A warning says sleeping function called from invalid context. What inspect?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Context analysis plus a lifetime-safe redesign.

**Spoken answer:** Trace the call path, held locks, IRQ/preemption state and a potentially sleeping operation such as allocation or user access.

**Deeper explanation/example:** Fix the context/ownership design; GFP_ATOMIC is not a universal patch for an operation that fundamentally needs sleep. Move appropriate work to a worker when justified.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** Replace every allocation flag with GFP_ATOMIC.

**Follow-up:** How would you prove cleanup remains safe after deferral?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Context analysis plus a lifetime-safe redesign. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q093 — How choose mutex, spinlock_t or raw_spinlock_t?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Version/configuration qualification and legal lock nesting.

**Spoken answer:** Choose by context, scope and configuration; mutexes sleep, while raw spinlocks remain strict spinning primitives.

**Deeper explanation/example:** PREEMPT_RT changes spinlock_t semantics, so “spinlocks always disable interrupts/preemption” is not a universal claim. Keep raw critical sections tiny and never perform sleepable bus access there.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** Use spinlocks for every kernel object because they are faster.

**Follow-up:** Which primitive fits a hard-IRQ-shared small state?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Version/configuration qualification and legal lock nesting. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q094 — How do kmalloc and vmalloc differ?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Address/layout distinction and appropriate allocation context.

**Spoken answer:** kmalloc gives kernel memory with relevant physical-contiguity properties; vmalloc maps virtually contiguous space that need not be physically contiguous.

**Deeper explanation/example:** Neither API alone establishes DMA suitability or device addressability. Allocation size, context and failure handling matter; use the DMA API for device buffers.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** vmalloc memory is always usable directly for DMA.

**Follow-up:** What about high-order allocation failures?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Address/layout distinction and appropriate allocation context. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q095 — A probe leaks resources on its third failure path. How fix?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Complete resource dependency/lifetime analysis.

**Spoken answer:** List acquisitions and dependencies, then unwind or use suitable managed resources while explicitly quiescing asynchronous activity.

**Deeper explanation/example:** Inject failure after each acquisition and verify no IRQ/work/timer can access released state. devm does not itself define the logical stop sequence.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** devm removes every cleanup requirement.

**Follow-up:** How do shared references survive unbind?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Complete resource dependency/lifetime analysis. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q096 — What does a wait queue provide?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Predicate, visibility and interruption reasoning.

**Spoken answer:** It coordinates sleeping waiters with a condition becoming true; the state predicate and synchronization remain the driver's responsibility.

**Deeper explanation/example:** Register/check/wake ordering must prevent lost wakeups. Recheck after wake and handle signal interruption; notification is not the data itself.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** One wake_up stores one event permanently.

**Follow-up:** Why is wake_up alone insufficient?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Predicate, visibility and interruption reasoning. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q097 — When use a workqueue?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Deferred-work ownership and quiescence order.

**Spoken answer:** For appropriate asynchronous process-context work that may need to sleep, with explicit scheduling and teardown rules.

**Deeper explanation/example:** Coalesce repeated work carefully; it may represent state needing service rather than one queued execution per event. Cancel/flush correctly and prevent requeue before freeing state.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** Queueing work guarantees one callback per hardware event.

**Follow-up:** How would unbind race with a self-requeueing worker?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Deferred-work ownership and quiescence order. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q098 — What problem does RCU solve?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Publication versus reclamation and relevant reader scope.

**Spoken answer:** It allows appropriate readers to observe published versions while reclamation waits until pre-existing readers are done.

**Deeper explanation/example:** Writers still need update coordination and correct publication; grace periods address lifetime, not every data race. Rules depend on RCU flavor/context.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** RCU means writers need no locks and can free immediately.

**Follow-up:** Why is synchronize_rcu not just a delay?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Publication versus reclamation and relevant reader scope. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q099 — A timer callback accesses freed driver state after removal. What happened?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Full asynchronous dependency graph and ordered quiescence.

**Spoken answer:** Teardown freed state before preventing new activity and synchronizing outstanding callbacks/work.

**Deeper explanation/example:** Disable the event source/rearming path, use the appropriate synchronous cancellation and avoid lock inversion with the callback. Mere removal from a registry does not stop execution already in flight.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** Set the pointer to NULL after free.

**Follow-up:** What if the timer queues work that rearms the timer?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Full asynchronous dependency graph and ordered quiescence. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.

## Q100 — Why are atomics insufficient for many kernel invariants?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Compound-state and lifetime reasoning beyond atomicity.

**Spoken answer:** An atomic operation protects a particular operation, not an arbitrary relationship among payload, count, lifetime and readiness.

**Deeper explanation/example:** Use appropriate ordering and ownership or a lock that covers the invariant. A refcount also has a different purpose from an arbitrary integer counter.

**Assumptions/version:** Linux 6.18 concepts; verify selected configuration, especially PREEMPT_RT.

**Common incorrect answer:** Making every field atomic makes the structure race-free and correct.

**Follow-up:** How do reference counts interact with object publication?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Compound-state and lifetime reasoning beyond atomicity. [Learning: M07](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m07). References: R26; R27; R28; R30.
