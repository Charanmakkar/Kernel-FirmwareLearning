# System design and project defense

## Q191 — Design a one-path industrial monitoring gateway.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Requirements→interfaces→bounds→fault tests traceability.

**Spoken answer:** Clarify rate/size/storage/update needs; separate serial acquisition, bounded storage, config, health and signed-image recovery with explicit owners.

**Deeper explanation/example:** Use C01's 10 Hz stream as an assumed workload. Derive queue/log bounds from stall/retention budgets; test bad frames, disconnect, disk full and interrupted updates. Do not add cloud complexity before core acceptance.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Draw boxes without failure, persistence or recovery semantics.

**Follow-up:** How would you prove a stale sensor is observable?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Requirements→interfaces→bounds→fault tests traceability. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q192 — Design a Linux service supervising several device tasks.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Lifecycle, health and overload policy with observable recovery.

**Spoken answer:** Use bounded interfaces and a supervisor health policy that distinguishes process existence, useful data progress and recoverable failures.

**Deeper explanation/example:** Choose process/thread isolation from fault boundaries; define restart/backoff, stale-data marking and persistent state. A restart loop needs bounds and diagnostic preservation.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Restart everything immediately for every error.

**Follow-up:** What state must survive a restart?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Lifecycle, health and overload policy with observable recovery. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q193 — Design a sensor acquisition driver interface.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Subsystem fit, ABI, context and lifetime design.

**Spoken answer:** Choose an existing fitting subsystem, define channels/units/buffering/timestamps and expose errors/power transitions consistently.

**Deeper explanation/example:** For an accelerometer consider IIO and existing support first. Draw bus/IRQ/worker/user paths with contexts and teardown dependencies; test invalid configuration, bus faults and unbind.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Expose raw internal pointers through a custom ioctl.

**Follow-up:** How would direct mode and buffered mode interact?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Subsystem fit, ABI, context and lifetime design. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q194 — Design a safe field-update workflow for a gateway.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Trust/persistence/boot/health integration and concrete fault matrix.

**Spoken answer:** Separate signing authority, compatibility verification, inactive-slot installation, durable boot attempts and useful health confirmation.

**Deeper explanation/example:** Specify rollback, key rotation/revocation, schema migration and recovery if metadata or power fails. Test rejected bundles and every interruption boundary on disposable disks.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Treat HTTPS download as sufficient authenticity and rollback.

**Follow-up:** How can a data migration prevent rollback?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Trust/persistence/boot/health integration and concrete fault matrix. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q195 — Design a low-latency Linux telemetry pipeline.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Budgeted stages, overload behavior and credible measurement plan.

**Spoken answer:** Specify event-to-consumer deadline, rates/bursts and queue policy; assign owners and measure each stage under representative load.

**Deeper explanation/example:** Bound allocation/logging in critical paths and locate contention with traces. Separate empirical max from a proven timing bound; compare changes with raw repeated measurements.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Raise all priorities and claim hard real time.

**Follow-up:** Which work belongs outside the latency path?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Budgeted stages, overload behavior and credible measurement plan. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q196 — Design Linux–MCU robot control responsibilities.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Authority/timing/fault boundaries and explicit physical gaps.

**Spoken answer:** Linux handles planning/diagnostics; MCU owns periodic control, command lease, output bounds and local fault transition.

**Deeper explanation/example:** Start C02 with deterministic plant simulation. Define session/sequence, receiver-time freshness, sensor stall and reset behavior. Zero command in simulation does not prove physical stopping safety.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Linux sends PWM continuously and MCU follows forever if link dies.

**Follow-up:** How would you add an independent emergency stop later?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Authority/timing/fault boundaries and explicit physical gaps. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q197 — Design diagnostic anomaly inference without disturbing control.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Data/evaluation/resource/fallback design and preserved control contract.

**Spoken answer:** Keep a deterministic baseline, session-separated dataset and lower-priority bounded-age inference output outside the control deadline.

**Deeper explanation/example:** Evaluate false alarms/missed faults/delay and resource cost on held-out sessions. Fall back when score/model is unavailable or late; record no invented benchmarks.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Put a neural network directly in the hard IRQ control path.

**Follow-up:** How do you prevent overlapping-window leakage?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Data/evaluation/resource/fallback design and preserved control contract. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q198 — Design shared DMA buffer ownership for acquisition.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** End-to-end mapping/ownership/reclamation timeline.

**Spoken answer:** Define CPU/device ownership transitions, mapping/direction/sync rules, completion and shutdown before selecting a zero-copy interface.

**Deeper explanation/example:** Address domains, cache-line sharing and userspace lifetime require explicit handling. Start from supported subsystem APIs; test cancellation, reset and completion after close. Zero-copy is a tradeoff, not an initial goal.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Share one raw pointer between userspace and hardware with no reference management.

**Follow-up:** How does an IOMMU change addressing but not lifetime?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: End-to-end mapping/ownership/reclamation timeline. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q199 — Design an automated embedded CI test ladder.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Layered evidence, meaningful tests and truthful scope.

**Spoken answer:** Use host logic/model tests, target cross-build/static checks, isolated emulator integration and separately scheduled hardware tests.

**Deeper explanation/example:** Tie each result to source/config/tool/image identity; distinguish authored/built/run and never promote a simulated pass to electrical/timing validation. Retain failure artifacts and minimal reproducers.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** A host unit-test pass means the entire board image is validated.

**Follow-up:** Which faults can only be verified on hardware?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Layered evidence, meaningful tests and truthful scope. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.

## Q200 — Defend a capstone and plan its next production step.

**Tags:** All; advanced; design/project defense; system design. **Assesses:** Honest ownership, evidence-backed tradeoff and actionable next validation.

**Spoken answer:** State actual requirements, your contribution, architecture, one reproduced failure, real test evidence and limitations; prioritize the highest-risk unverified assumption.

**Deeper explanation/example:** Use actual reports for numbers. For C02 disclose simulated plant, missing physical timing/e-stop/hazard analysis. Supplied reference code is not your industry experience; choose a concrete next experiment.

**Assumptions/version:** Design targets are assumptions to validate, not measured results or production safety certification.

**Common incorrect answer:** Invent uptime/performance numbers and claim production readiness.

**Follow-up:** Which design choice would you change with a tighter budget?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Honest ownership, evidence-backed tradeoff and actionable next validation. [Learning: M16](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m16). References: C01/C02 requirements; R16; R24; R33.
