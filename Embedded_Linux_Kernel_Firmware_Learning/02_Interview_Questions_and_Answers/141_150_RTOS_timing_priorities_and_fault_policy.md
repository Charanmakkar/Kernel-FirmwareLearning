# RTOS timing, priorities and fault policy

## Q141 — How assign task priorities?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Deadline/resource reasoning and explicit scheduler assumptions.

**Spoken answer:** Start from deadlines and blocking/resource dependencies, then verify schedulability and measured interference on the selected RTOS.

**Deeper explanation/example:** High frequency alone is insufficient if critical work blocks behind long shared-resource ownership. Keep noncritical logging/inference from controlling essential deadlines.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Give all tasks equal highest priority.

**Follow-up:** What assumptions permit rate-monotonic analysis?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Deadline/resource reasoning and explicit scheduler assumptions. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q142 — A high-priority task starves lower-priority maintenance. What inspect?

**Tags:** FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Progress requirements and capacity-based remediation.

**Spoken answer:** Check whether it ever blocks/yields appropriately, workload exceeds capacity or priorities conflict with system progress requirements.

**Deeper explanation/example:** Measure execution and queueing; a watchdog may reset a system whose critical loop appears alive. Define bounded work per activation and overload behavior.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Raise the maintenance task until both are highest.

**Follow-up:** When is starvation intentionally acceptable?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Progress requirements and capacity-based remediation. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q143 — What can priority inheritance fix and not fix?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Bounded critical sections and accurate mechanism limits.

**Spoken answer:** It can reduce priority inversion caused by a lower-priority mutex owner, but not deadlock, excessive work or every interrupt-disabled delay.

**Deeper explanation/example:** Check actual mutex implementation and nested-lock behavior. A queue/semaphore may not provide the ownership needed for inheritance.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Priority inheritance guarantees all deadlines.

**Follow-up:** How would you reduce blocking before changing priorities?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bounded critical sections and accurate mechanism limits. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q144 — Design a watchdog supervisor with task progress counters.

**Tags:** FW; intermediate; coding practical; coding. **Assesses:** System-wide progress condition and deterministic stall test.

**Spoken answer:** Each required task advances a progress marker after meaningful work; supervisor feeds only if all required markers and freshness checks meet policy.

**Deeper explanation/example:** Guard counters/state consistently and account for legitimately idle tasks. A marker increment alone can miss stale sensor output; use a domain-relevant success predicate.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Every task feeds the hardware watchdog independently.

**Follow-up:** How do you test one stuck task without stopping the scheduler?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: System-wide progress condition and deterministic stall test. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q145 — How do queues, mutexes and semaphores differ?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Correct semantics and selected RTOS qualification.

**Spoken answer:** Queues transfer bounded data/ownership, mutexes protect owned critical sections, and semaphores represent counts/signals under their API rules.

**Deeper explanation/example:** Choose from invariant and context, not naming. ISR-safe variants and blocking restrictions are RTOS-specific; a counting semaphore alone does not carry packet identity.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** They are interchangeable ways to delay a task.

**Follow-up:** Which primitive supports priority inheritance here?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct semantics and selected RTOS qualification. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q146 — A task stack overflows only during error logging. How investigate?

**Tags:** FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Peak-path analysis and measurement limits.

**Spoken answer:** Capture stack usage/watermarks and call depth under worst relevant paths, including formatting and interrupt stacking rules.

**Deeper explanation/example:** Static stack estimates and observed high-water marks complement each other; neither guarantees all paths. Avoid recursion/large locals when unjustified and add defensible margin.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Double every stack forever without identifying usage.

**Follow-up:** Can a watermark miss an unexercised path?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Peak-path analysis and measurement limits. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q147 — What is a deadline miss and how should firmware react?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Explicit timing contract and measurable response.

**Spoken answer:** It is completion after the required time bound; reaction follows a specified fault/overload policy rather than silently accumulating stale work.

**Deeper explanation/example:** Choose skip/catch-up/degrade/fault based on control semantics. Count/report misses and preserve a safe output rule; a good average period can hide misses.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Average frequency proves no deadlines are missed.

**Follow-up:** How would you distinguish release jitter from execution overrun?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explicit timing contract and measurable response. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q148 — An ISR calls an RTOS queue API and crashes. What check?

**Tags:** FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Selected API/port/context constraints.

**Spoken answer:** Verify ISR-safe API/timeout restrictions, interrupt priority constraints, kernel state and buffer lifetime for this RTOS/port.

**Deeper explanation/example:** Some kernel services cannot be used from arbitrary interrupt priorities. Read the actual port documentation; do not assume FreeRTOS/Zephyr rules are identical.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Any API is safe if the ISR is short.

**Follow-up:** How does zero timeout differ from permission to call?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Selected API/port/context constraints. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q149 — What does native_sim validate and leave unverified?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Model scope and version/ABI awareness.

**Spoken answer:** It can test modeled RTOS application state and logic as a host program; it does not reproduce the chosen MCU's physical peripherals/timing.

**Deeper explanation/example:** Keep simulation, MCU build and actual board runs separate. Hardware startup, DMA coherency, IRQ priorities, clock accuracy and electrical behavior need their own evidence.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Passing native_sim proves the STM32 watchdog and deadlines.

**Follow-up:** Why choose its 64-bit qualifier explicitly?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Model scope and version/ABI awareness. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.

## Q150 — A task is running but the system produces no useful output. How diagnose?

**Tags:** FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Useful progress, not mere execution, as the health contract.

**Spoken answer:** Observe domain-level progress, queue age, resource waits and state transitions rather than just task heartbeat.

**Deeper explanation/example:** A livelock can keep counters moving while work never completes. Inject stale inputs/full queues to distinguish healthy idleness, blocking and useless retries.

**Assumptions/version:** Zephyr v4.2.0 planned; RTOS scheduling/ISR API rules are implementation-specific.

**Common incorrect answer:** Scheduler activity means the system is healthy.

**Follow-up:** What health metric would expose stale-but-active behavior?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Useful progress, not mere execution, as the health contract. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: R10; R32.
