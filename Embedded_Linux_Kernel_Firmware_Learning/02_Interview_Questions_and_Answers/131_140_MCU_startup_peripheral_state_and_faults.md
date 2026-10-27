# MCU startup, peripheral state and faults

## Q131 — What happens before main on a Cortex-M firmware target?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Trace actual reset-to-main dependencies.

**Spoken answer:** Reset uses the vector table/startup path, establishes initial execution state and initializes the C runtime's required memory before main.

**Deeper explanation/example:** Typical startup copies .data and zeroes .bss, with clock/FPU/cache setup according to the target. Bootloader relocation changes vector/address assumptions; inspect actual startup and linker files.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** main is always the first instruction executed.

**Follow-up:** Where do initial stack pointer and reset vector come from?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Trace actual reset-to-main dependencies. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q132 — Write the logic for nonblocking UART receive processing.

**Tags:** FW; intermediate; coding practical; coding. **Assesses:** Bounded ISR work and explicit ownership/recovery.

**Spoken answer:** Use a bounded ISR/DMA-to-task handoff and a stateful parser; the task processes available bytes and timeouts without waiting forever.

**Deeper explanation/example:** One actor owns each buffer/index or a documented synchronization primitive protects it. Define overflow, partial frame and error reset. Actual UART register/DMA configuration is target-specific.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** Read until a full packet inside the ISR with no bound.

**Follow-up:** How do overrun/framing flags affect parser recovery?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bounded ISR work and explicit ownership/recovery. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q133 — Firmware enters a fault handler after an interrupt. What capture?

**Tags:** FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Artifact identity, minimal safe capture and competing hypotheses.

**Spoken answer:** Preserve stacked PC/LR/registers, relevant fault status and stack/context information before destructive logging/reset.

**Deeper explanation/example:** Decode addresses using the exact ELF/map and fault registers for the core. A corrupt stack can make the frame unreliable. Avoid complex allocation or unsafe peripheral calls in the handler.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** Always assume the last source line caused the fault.

**Follow-up:** How do you persist a small crash record across reset?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Artifact identity, minimal safe capture and competing hypotheses. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q134 — What are .text, .data, .bss and stack?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Load/run memory distinction and measured stack margin.

**Spoken answer:** They represent code/constant placement, initialized writable data, zero-initialized storage and call/task execution storage under the selected toolchain.

**Deeper explanation/example:** Linker placement and startup establish runtime addresses; RTOS tasks usually need separate stacks. A map file can reveal RAM pressure but not all dynamic peak usage.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** .bss occupies identical bytes in the load image and runtime RAM.

**Follow-up:** How would you budget multiple task stacks?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Load/run memory distinction and measured stack margin. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q135 — How should a watchdog be fed?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Health/progress criteria and actual stall-injection test.

**Spoken answer:** Only after required system components demonstrate progress within policy, using the correct watchdog timing/window contract.

**Deeper explanation/example:** A periodic ISR feeding unconditionally can hide a deadlocked application. Test stopped workers, reset reason and boot recovery. Independent watchdog clock behavior is target-specific.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** Feed as fast as possible from any loop.

**Follow-up:** What if one task is alive but its data is stale?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Health/progress criteria and actual stall-injection test. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q136 — Timer periods drift when other work increases. Why?

**Tags:** FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Clock/scheduling distinction and measured timeline.

**Spoken answer:** Relative scheduling, blocked execution, interrupt latency or incorrect clock assumptions may affect the observed period.

**Deeper explanation/example:** Use a hardware/monotonic reference, schedule against intended deadlines where appropriate and measure jitter. A nominal timer reload is not end-to-end periodic behavior.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** Increase optimization until drift disappears.

**Follow-up:** How do missed periods change the state machine?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Clock/scheduling distinction and measured timeline. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q137 — What must peripheral initialization establish?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Manual-based sequence and observable verification.

**Spoken answer:** Clock/reset/pinmux, transfer format, buffers/interrupts and status-clearing sequence according to the specific peripheral contract.

**Deeper explanation/example:** Enable interrupts only after state and handlers are ready; clear stale conditions safely. Reverse dependencies during shutdown. Register-write order may matter.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** Copy register values from a different MCU family.

**Follow-up:** How do you verify actual peripheral clock?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Manual-based sequence and observable verification. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q138 — Design a debounced button state machine.

**Tags:** FW; intermediate; coding practical; coding. **Assesses:** Defined timing semantics, bounded ISR and transition tests.

**Spoken answer:** Sample or timestamp edges, require a defined stable interval and emit one logical transition under an explicit policy.

**Deeper explanation/example:** Keep raw electrical edges separate from stable application state; handle timer wrap and repeated edges. Choose interval from measured behavior/requirements, not a universal magic number.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** Sleep inside the ISR until bounce ends.

**Follow-up:** How do you preserve fast legitimate events?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Defined timing semantics, bounded ISR and transition tests. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q139 — When use polling, interrupt or DMA?

**Tags:** FW; intermediate; technical screen; conceptual. **Assesses:** Workload-based tradeoff and ownership overhead.

**Spoken answer:** Choose by data rate, deadline, CPU budget, complexity and peripheral support.

**Deeper explanation/example:** Polling can be simplest for bounded short checks; interrupts avoid constant polling; DMA reduces per-byte CPU work but adds buffer/cache/lifetime complexity. Measure rather than assuming DMA always wins.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** DMA makes transfers free of CPU and correctness costs.

**Follow-up:** What happens for tiny infrequent transfers?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Workload-based tradeoff and ownership overhead. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.

## Q140 — MCU application works after debugger download but not power-cycle. Why?

**Tags:** FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Cold-boot versus debug-state distinction and reproducible checks.

**Spoken answer:** Debugger initialization, reset type, vector/link address, boot mode, startup memory or timing dependencies may differ.

**Deeper explanation/example:** Test a real cold boot and inspect boot pins/options, reset reason and startup trace. A debugger can mask uninitialized RAM or clock setup defects.

**Assumptions/version:** STM32F446RE planned hardware; exact registers/startup require its reference manual and build.

**Common incorrect answer:** The board is defective because debug run succeeds.

**Follow-up:** How would bootloader offset change startup?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Cold-boot versus debug-state distinction and reproducible checks. [Learning: M11](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m11). References: R12; R18.
