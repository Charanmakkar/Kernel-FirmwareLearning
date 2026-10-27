# Device tree, GPIO and platform integration

## Q111 — What does device tree describe?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Hardware description versus implementation policy.

**Spoken answer:** It describes hardware topology/resources and compatible bindings for software to interpret, not an arbitrary driver-instantiation script.

**Deeper explanation/example:** Bindings are an ABI beyond one kernel driver. Clocks, interrupts and pinctrl resources must reflect hardware. Node names alone should not be used as a general stable matching interface.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** Add any property needed to store the driver's private runtime state.

**Follow-up:** Why should a binding cover hardware not yet used by the driver?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Hardware description versus implementation policy. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q112 — A device-tree node exists but probe never runs. What inspect?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Systematic enumeration/matching/probe boundary checks.

**Spoken answer:** Check the live tree, status, compatible match, driver build/module availability and bus/device creation path.

**Deeper explanation/example:** Inspect actual booted DTB rather than source alone. Overlay application or wrong deployment can make a correct source irrelevant. Differentiate missing match from probe returning an error.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** Rename the node to the driver function name.

**Follow-up:** What if the compatible is correct but provider is deferred?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Systematic enumeration/matching/probe boundary checks. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q113 — When should probe return deferred-probe error?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Correct transient versus permanent failure classification.

**Spoken answer:** When a required resource provider is expected but not ready under the relevant API contract.

**Deeper explanation/example:** Propagate the actual provider error rather than converting every failure to ENODEV. A malformed property or absent hardware is different from a deferred dependency.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** Always retry every probe error forever.

**Follow-up:** How do logs help avoid deferred-probe spam?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct transient versus permanent failure classification. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q114 — Outline a GPIO IRQ platform driver using modern resources.

**Tags:** KD; intermediate; coding practical; coding. **Assesses:** Descriptor/context/lifetime design plus board-doc verification.

**Spoken answer:** Match a binding, acquire a GPIO descriptor, derive/request IRQ as appropriate, keep hard handler minimal and expose the event through a fitting interface.

**Deeper explanation/example:** Use the selected tree's exact APIs and a threaded path if operations sleep. Document polarity/debounce and prevent work/IRQ after teardown. No arbitrary numeric GPIO assumption.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** Hardcode a global GPIO number from another board.

**Follow-up:** How do you prove physical pin routing?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Descriptor/context/lifetime design plus board-doc verification. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q115 — How do GPIO logical values differ from electrical levels?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Polarity and sleepable-access qualification.

**Spoken answer:** Descriptor polarity can map logical active/inactive to physical high/low; open-drain and controller capabilities further matter.

**Deeper explanation/example:** Use binding/controller semantics consistently. A logical one on an active-low line may drive low. Verify with a meter/analyzer and the exact circuit.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** Logical one always means 3.3 V.

**Follow-up:** What if a GPIO provider is on an I2C expander?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Polarity and sleepable-access qualification. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q116 — A GPIO driver works on a simulator but not the board. Why?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Separate modeled state from real physical verification.

**Spoken answer:** Pinmux, power, pull resistors, polarity, voltage, board routing or actual IRQ/controller behavior may differ.

**Deeper explanation/example:** Use board schematic and SoC pin control documentation; identify shared functions before writing. Simulation validates only modeled semantics, not electrical configuration.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** QEMU passing proves the pin and interrupt timing.

**Follow-up:** What measurement separates routing from driver logic?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate modeled state from real physical verification. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q117 — How do clocks and regulators affect probe and runtime?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Resource dependencies and balanced ownership.

**Spoken answer:** They provide required timing/power resources; enabling/configuring them and releasing references must follow device dependencies.

**Deeper explanation/example:** Check sequencing, rates and failure paths. Runtime PM can power down a device between uses, so register access requires the appropriate active state.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** A mapped register is usable regardless of clock/power.

**Follow-up:** What must happen during suspend/resume?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Resource dependencies and balanced ownership. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q118 — An overlay compiles but the wrong device appears. What inspect?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Syntax versus semantic/live-deployment checks.

**Spoken answer:** Inspect the applied live tree, target phandles, bus location, address cells and selected base DTB.

**Deeper explanation/example:** Compile success is syntax-level evidence, not correct hardware binding. Verify overlay deployment and conflicts with existing nodes/drivers; validate schemas when supported.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** If dtc accepts it, the hardware description is correct.

**Follow-up:** How would you detect duplicate address use?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Syntax versus semantic/live-deployment checks. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q119 — Why validate a device-tree binding schema?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Constraint/ABI reasoning and validation limits.

**Spoken answer:** It checks declared structure/constraints and catches many property and example mismatches before runtime.

**Deeper explanation/example:** It does not prove wiring, pinmux safety or actual device behavior. Keep examples consistent and avoid breaking the established ABI for convenience.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** Schema validation replaces hardware tests.

**Follow-up:** What should happen to unknown vendor properties?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Constraint/ABI reasoning and validation limits. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.

## Q120 — A button produces many interrupts for one press. How respond?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Signal semantics, measured debounce and context-correct implementation.

**Spoken answer:** Confirm bounce/electrical behavior and trigger configuration, then use an appropriate hardware/software debounce policy.

**Deeper explanation/example:** Measure bursts, define acceptable response/latency and avoid sleeping in a hard handler. Prefer an existing input/GPIO subsystem driver if it already fits.

**Assumptions/version:** Linux 6.18 interfaces; physical board image/pinmux still pending.

**Common incorrect answer:** Busy-wait in the hard IRQ for 100 ms.

**Follow-up:** What if legitimate fast edges must be retained?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Signal semantics, measured debounce and context-correct implementation. [Learning: M09](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m09). References: R13; R29; R31.
