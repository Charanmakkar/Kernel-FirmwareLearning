# Buses, IIO, DMA and power

## Q121 — Compare I2C, SPI and UART integration concerns.

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Transaction and physical/protocol distinctions.

**Spoken answer:** I2C has addressed shared-bus transactions, SPI controller/chip-select/mode transactions, and UART an asynchronous byte stream needing explicit framing.

**Deeper explanation/example:** Electrical levels, clocks, chip selects, pull-ups and error observability differ. A peripheral interface name alone does not specify application protocol, voltage or Linux subsystem API.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** All three buses automatically deliver application packets.

**Follow-up:** Which conditions are visible only with a logic analyzer?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Transaction and physical/protocol distinctions. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q122 — An I2C register read returns NACK. What investigate?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Datasheet-based, bounded, non-destructive investigation.

**Spoken answer:** Check power/voltage, address convention, wiring/pull-ups, controller configuration and the documented transaction sequence.

**Deeper explanation/example:** Separate a 7-bit address from an 8-bit address byte. Confirm repeated-start and register pointer behavior against the actual device. Do not scan/write arbitrary buses indiscriminately.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Shift every failing address until it works.

**Follow-up:** How do you distinguish absent hardware from transient bus error?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Datasheet-based, bounded, non-destructive investigation. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q123 — What must match for an SPI peripheral?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Complete transaction contract.

**Spoken answer:** Controller chip-select routing, clock polarity/phase, frequency, word size and device-specific command framing.

**Deeper explanation/example:** A correct mode still leaves byte order, dummy cycles and transfer continuity. Validate against datasheet/logic trace, not only successful ioctl return.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** SPI has addressing exactly like I2C.

**Follow-up:** What happens if chip select toggles between command and response?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Complete transaction contract. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q124 — Convert ADXL345 register bytes to physical units.

**Tags:** KD; intermediate; coding practical; coding. **Assesses:** Configuration-aware numeric/unit conversion and independent fixtures.

**Spoken answer:** Decode according to configured range/resolution and register format, then apply the documented scale and units exposed by IIO.

**Deeper explanation/example:** Do not assume a generic int16_t always represents the full device format. Test negative/raw fixtures and check orientation sanity with the actual configured scale; no measurement is supplied here.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Raw count is already acceleration in m/s².

**Follow-up:** What does the IIO scale represent?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Configuration-aware numeric/unit conversion and independent fixtures. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q125 — Why expose sensor channels through IIO?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Subsystem semantics and production maintenance tradeoff.

**Spoken answer:** It supplies established channel/raw/scale/buffer conventions and userspace discoverability for appropriate sensors.

**Deeper explanation/example:** Reuse or extend an existing supported driver rather than deploy a duplicate casually. A teaching variant belongs in an isolated tree and must explain its scope.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Every sensor requires a private /dev node and ioctl.

**Follow-up:** When would hwmon be a better fit?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Subsystem semantics and production maintenance tradeoff. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q126 — Sensor samples are plausible but scaled incorrectly. What inspect?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Independent numeric oracle and configuration traceability.

**Spoken answer:** Compare configured range/resolution, sign extension, byte order, scale units and client conversion path.

**Deeper explanation/example:** Use a known register fixture before physical orientation tests. Plausible numbers are weak validation; record actual configuration and the expected physical relation.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Calibrate until the graph looks smooth.

**Follow-up:** How would you separate offset error from scale error?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Independent numeric oracle and configuration traceability. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q127 — What is a triggered IIO buffer?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Explicit binary layout and mode/lifetime handling.

**Spoken answer:** It captures defined channel scans associated with a trigger, with specified layout/timestamp semantics.

**Deeper explanation/example:** Scan masks, alignment and timestamp units must match userspace decoding. Buffer mode and direct register access can need exclusion/serialization; follow the selected IIO API.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Read a C struct from the buffer using host padding.

**Follow-up:** How do you validate scan layout?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explicit binary layout and mode/lifetime handling. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q128 — A bus read sleeps inside a hard IRQ and warns. What change?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Context-correct transfer and interrupt/lifetime analysis.

**Spoken answer:** Move appropriate bus work to a threaded/deferred sleepable context and keep the hard path within its legal operations.

**Deeper explanation/example:** Preserve source acknowledgement, event coalescing, ownership and teardown. Simply substituting an atomic allocation does not make I2C transfer sleep-free.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Use GFP_ATOMIC around the bus read.

**Follow-up:** How do you avoid losing level-triggered events during deferral?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Context-correct transfer and interrupt/lifetime analysis. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q129 — What is runtime PM versus system suspend?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** State/refcount balance and recovery semantics.

**Spoken answer:** Runtime PM manages individual devices during normal operation; system suspend coordinates a broader system power transition.

**Deeper explanation/example:** Balance active references and error paths; avoid accessing powered-down registers. A pending worker and its lifetime must be reconciled with suspend/removal.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Runtime PM is just calling sleep in idle code.

**Follow-up:** How do you test failure during resume?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: State/refcount balance and recovery semantics. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.

## Q130 — DMA completion occurs after the client buffer was released. What failed?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Complete submit→device→completion→release ownership timeline.

**Spoken answer:** The transfer's ownership/lifetime outlasted the caller's storage; cancellation/completion synchronization was incomplete.

**Deeper explanation/example:** Define who owns buffers until completion and how shutdown prevents new submissions, cancels/drains transfers and returns ownership. A completion flag alone does not pin memory.

**Assumptions/version:** Sensor register/board assumptions must follow actual datasheet and selected kernel source.

**Common incorrect answer:** Free immediately after submitting because DMA is asynchronous.

**Follow-up:** How does mapping/unmapping fit the lifetime?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Complete submit→device→completion→release ownership timeline. [Learning: M13](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m13). References: R14; R15; R24.
