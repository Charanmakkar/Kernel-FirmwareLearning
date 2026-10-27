# Architecture, MMIO, interrupts and DMA

## Q071 — How do MMU and MPU differ?

**Tags:** KD/FW; intermediate; technical screen; conceptual. **Assesses:** Target-specific capability and OS consequence.

**Spoken answer:** An MMU translates virtual addresses with protection; an MPU generally enforces protection over configured regions without full virtual translation.

**Deeper explanation/example:** Capabilities vary by core. Linux application processors and Cortex-M firmware have different memory models and boot responsibilities; do not infer features from the ARM name alone.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** Every ARM target runs the same virtual-memory Linux.

**Follow-up:** How does an MPU help isolate firmware tasks?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Target-specific capability and OS consequence. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q072 — What is MMIO and why not use an ordinary pointer casually?

**Tags:** KD/FW; intermediate; technical screen; conceptual. **Assesses:** Side effects, access width and ordering qualifications.

**Spoken answer:** Device registers are accessed through mapped addresses with device-specific width, side-effect and ordering rules.

**Deeper explanation/example:** In Linux use mapped I/O and accessors; MCU code follows vendor/compiler register definitions. A read can clear a flag and a write can acknowledge it, so normal variable assumptions fail.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** Volatile makes every register sequence correct.

**Follow-up:** What about posted writes or required readback?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Side effects, access width and ordering qualifications. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q073 — A register read always returns zero. How investigate?

**Tags:** KD/FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Ordered, non-destructive checks tied to target documentation.

**Spoken answer:** Verify address mapping, clock/reset/power, access width, permissions and pin/peripheral configuration before assuming the register value is meaningful.

**Deeper explanation/example:** Compare target reference manual and a known identity/status register. A disabled clock or wrong physical-to-virtual assumption can imitate broken hardware. Record fault/status evidence.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** Write random values to neighboring registers.

**Follow-up:** How would you distinguish bus fault from legitimate zero?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Ordered, non-destructive checks tied to target documentation. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q074 — Why can DMA fail despite correct CPU memory contents?

**Tags:** KD/FW; intermediate; technical screen; conceptual. **Assesses:** Address-domain and ownership distinctions.

**Spoken answer:** Device addressing, mapping, ownership, cache maintenance, alignment or ordering may be wrong.

**Deeper explanation/example:** A CPU virtual pointer is not a DMA address. Use the DMA API, check mapping errors/direction and transfer ownership correctly. Coherent allocation still needs ordering of descriptors/status.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** Cast the pointer to an integer and program the device.

**Follow-up:** What changes with an IOMMU?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Address-domain and ownership distinctions. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q075 — A DMA buffer works on one board but contains stale data on another. Why?

**Tags:** KD/FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Concrete ownership timeline and portable API correction.

**Spoken answer:** A coherence/ownership assumption may differ; inspect mapping direction, sync transitions and cache-line sharing.

**Deeper explanation/example:** Use the selected platform's DMA APIs rather than ad hoc cache flushing. A small adjacent CPU field sharing a cache line can complicate streaming-buffer ownership.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** Disable all caches permanently.

**Follow-up:** How would you test CPU/device simultaneous access misuse?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Concrete ownership timeline and portable API correction. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q076 — What is interrupt latency versus handler execution time?

**Tags:** KD/FW; intermediate; technical screen; conceptual. **Assesses:** Explicit timeline and observer-effect awareness.

**Spoken answer:** Latency is delay from the relevant event to service; handler time is work after entry, and end-to-end response includes later scheduling/queueing.

**Deeper explanation/example:** Define measurement timestamps and instrument the physical event if claiming external latency. A userspace log alone may omit controller/firmware delays.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** Measure printf duration in the ISR.

**Follow-up:** How does deferred processing change the response budget?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explicit timeline and observer-effect awareness. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q077 — How do barriers differ from locks?

**Tags:** KD/FW; intermediate; technical screen; conceptual. **Assesses:** Match guarantee to actual shared-state protocol.

**Spoken answer:** Barriers constrain ordering; locks also implement a mutual-exclusion/ownership protocol under their contract.

**Deeper explanation/example:** A barrier does not stop two CPUs updating the same compound state. Compiler, CPU and device ordering are distinct concerns. Use high-level primitives appropriate to the selected memory model.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** A memory barrier makes increment atomic.

**Follow-up:** When can release/acquire replace a full barrier?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Match guarantee to actual shared-state protocol. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q078 — An IRQ fires continuously after enabling a peripheral. What inspect?

**Tags:** KD/FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Target-specific cause acknowledgement and safe diagnostic sequence.

**Spoken answer:** Check source status, trigger/polarity, acknowledgement semantics and whether the underlying level condition has been cleared.

**Deeper explanation/example:** Do not indiscriminately mask every IRQ or use an unrelated clear sequence. Record status before/after the documented acknowledgement; shared IRQ handlers must identify ownership.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** The interrupt controller is always faulty.

**Follow-up:** How do edge and level triggers change recovery?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Target-specific cause acknowledgement and safe diagnostic sequence. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q079 — Implement rollover-safe elapsed-time comparison for a timer.

**Tags:** KD/FW; intermediate; coding practical; coding. **Assesses:** State arithmetic width, bound and missed-wrap limitation.

**Spoken answer:** Use unsigned modular subtraction under a documented maximum-interval bound and compare elapsed with the timeout.

**Deeper explanation/example:** For a fixed-width counter, require observations/intervals within the intended wrap model; common ordering schemes restrict intervals to less than half the range. Never transplant formulas across unknown widths.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** Compare now>=start+timeout without considering overflow.

**Follow-up:** What if the device sleeps through multiple wraps?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: State arithmetic width, bound and missed-wrap limitation. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.

## Q080 — Why is disabling local interrupts not a multicore lock?

**Tags:** KD/FW; intermediate; technical screen; conceptual. **Assesses:** Enumerate actors and primitive scope.

**Spoken answer:** It prevents selected local interrupt interleavings, not another CPU from accessing the same object.

**Deeper explanation/example:** Also consider nonmaskable exceptions, preemption and target-specific RT semantics. Choose a lock/context design for every actual concurrent actor rather than relying on one CPU's state.

**Assumptions/version:** Architecture and cache/controller details must be checked against actual target manuals.

**Common incorrect answer:** No interrupt means no concurrency anywhere.

**Follow-up:** How would an ISR and task share state on a uniprocessor MCU?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Enumerate actors and primitive scope. [Learning: M05](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R24; R13.
