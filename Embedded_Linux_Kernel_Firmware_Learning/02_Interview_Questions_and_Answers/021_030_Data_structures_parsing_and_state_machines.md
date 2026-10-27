# Data structures, parsing and state machines

## Q021 — Implement a full-capacity byte ring.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Correct invariants, full/empty behavior and external serialization contract.

**Spoken answer:** Use head, tail and count with indexes bounded by capacity; push/pop update exactly one byte and wrap index.

**Deeper explanation/example:** Empty is count=0, full count=capacity. Caller owns backing storage. Test against a simple shifting-array model rather than duplicating ring internals.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Mix reserved-slot full test with count-based capacity.

**Follow-up:** What changes for multiple producers?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct invariants, full/empty behavior and external serialization contract. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q022 — Implement ring peek without mutation.

**Tags:** All; foundation; coding practical; coding. **Assesses:** No state change and correct oldest-byte selection.

**Spoken answer:** Validate ring/output, return empty without changing output, otherwise read storage[tail].

**Deeper explanation/example:** Do not pop then push: that can reorder a full queue and exposes temporary state. Compare metadata before/after and test wrapped/capacity-one cases.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Peek advances tail then restores only count.

**Follow-up:** What is the newest element's index?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: No state change and correct oldest-byte selection. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q023 — Implement CRC-16 for a precisely named variant.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Parameter completeness and known-vector test.

**Spoken answer:** Specify polynomial, initial value, reflection, final XOR and byte coverage; update a bounded unsigned accumulator.

**Deeper explanation/example:** B01 uses poly 0x1021, init 0xFFFF, no reflection/xorout, with 123456789 checking to 0x29B1. A polynomial alone does not identify a CRC variant.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Any CRC called CRC16 interoperates.

**Follow-up:** Why can an attacker modify a CRC-protected frame?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Parameter completeness and known-vector test. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q024 — Implement exact-frame validation with an owned result.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Each read/copy is justified by an earlier bound.

**Spoken answer:** Check minimum/maximum size, magic/version, declared length and checksum before copying into a local result and committing it.

**Deeper explanation/example:** For B01 require N=L+8 and L<=64. Reject trailing bytes. Stream accumulation is a separate layer, so parser failures do not partially consume a stream invisibly.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Copy declared payload first, then validate its length.

**Follow-up:** Why leave output unchanged on failure?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Each read/copy is justified by an earlier bound. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q025 — Design a bounded stream framing state machine.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Bounded memory, progress and explicit recovery semantics.

**Spoken answer:** Accumulate a fixed header, validate declared size, collect body, verify, deliver and resume; timeout/noise recovery is bounded.

**Deeper explanation/example:** Track consumed bytes and monotonic deadline. A malformed header must either consume input or reset with progress; prevent an infinite retry on the same byte.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Assume each read returns one whole packet.

**Follow-up:** How do you handle overlapping magic bytes?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bounded memory, progress and explicit recovery semantics. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q026 — When choose an array, linked list or ring?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Tie data structure to workload and resource constraints.

**Spoken answer:** Choose from access pattern, bounds, locality and ownership costs; small embedded queues often favor fixed arrays/rings.

**Deeper explanation/example:** A linked list supports flexible insertion but needs allocation/lifetime rules and poor locality can dominate. O(1) insertion does not imply predictable end-to-end timing.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Linked lists are always faster because insertion is O(1).

**Follow-up:** What changes in interrupt context?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Tie data structure to workload and resource constraints. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q027 — Implement a finite-state machine for a timed request.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Every event/state combination has a defined transition or rejection.

**Spoken answer:** Use explicit states and events, one owner, a monotonic deadline and defined timeout/retry limits.

**Deeper explanation/example:** Example IDLE→WAIT_ACK→COMPLETE or TIMEOUT. Match replies by session/sequence and make duplicate handling explicit; do not recursively retry forever.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** A boolean busy flag is enough to describe all errors.

**Follow-up:** How do reset and cancellation change the state graph?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Every event/state combination has a defined transition or rejection. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q028 — Implement a callback dispatch table safely.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Signature/index/lifetime correctness.

**Spoken answer:** Use a correctly typed function pointer array, validate an external index and handle missing callbacks.

**Deeper explanation/example:** Do not cast unrelated function pointer types to silence a compiler error. The registration/lifetime and execution context of callback data remain part of the interface.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Any function pointer can be cast and called safely.

**Follow-up:** Who owns callback context during unregister?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Signature/index/lifetime correctness. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q029 — Parse a type-length-value buffer defensively.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Bounded progress and independent validation at each level.

**Spoken answer:** At each step require header bytes, validate value_length<=remaining-header, process/skip known or unknown types and advance by a safe amount.

**Deeper explanation/example:** Decide duplicate-tag and unknown-tag policy. Validate before advancing; avoid adding untrusted lengths before overflow checks. Test zero-length entries and truncated final values.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Trust the outer length to make every inner field safe.

**Follow-up:** How do nested containers affect maximum work?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bounded progress and independent validation at each level. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.

## Q030 — Why are complexity and timing different claims?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Separate algorithmic work, observed latency and defensible upper bound.

**Spoken answer:** Big-O describes growth under a model; deadlines require concrete costs and interference bounds.

**Deeper explanation/example:** B01 queue operations are O(1), but cache misses, interrupts and scheduling still affect elapsed time. Report measurements with workload and target rather than turning O(1) into a deadline guarantee.

**Assumptions/version:** B01 is single-context or externally locked; packet CRC is not authentication.

**Common incorrect answer:** Constant time means constant nanoseconds.

**Follow-up:** How would you build a deadline argument?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate algorithmic work, observed latency and defensible upper bound. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: B01; R05.
