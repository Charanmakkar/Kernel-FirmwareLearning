# Linux–MCU framing and recovery

## Q151 — What does a reliable serial protocol need beyond a CRC?

**Tags:** EL/FW; intermediate; technical screen; conceptual. **Assesses:** Separate integrity, delivery, compatibility and session semantics.

**Spoken answer:** Bounded framing, version/schema, sequence/session identity, deadlines, retries/duplicate policy and observable recovery.

**Deeper explanation/example:** UART supplies bytes, not application transactions. CRC detects accidental corruption, not malicious modification. A reset should establish a new session epoch so old commands are not accepted casually.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** CRC guarantees delivery, order and authenticity.

**Follow-up:** How do you distinguish lost command from lost ACK?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate integrity, delivery, compatibility and session semantics. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q152 — Design duplicate-safe command handling.

**Tags:** EL/FW; intermediate; coding practical; coding. **Assesses:** Explicit duplicate and reset semantics.

**Spoken answer:** Use session/sequence identifiers and cache a defined result or use idempotent commands; specify duplicate/retry retention bounds.

**Deeper explanation/example:** If an ACK is lost, repeating a toggle can undo the intended action. A set-target command is often easier to make idempotent. Persistent side effects need a durable transaction policy.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** Retry every timed-out command without considering its effects.

**Follow-up:** What happens after a receiver reset loses its cache?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explicit duplicate and reset semantics. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q153 — Implement bounded resynchronization after malformed input.

**Tags:** EL/FW; intermediate; coding practical; coding. **Assesses:** Memory/work/progress bound and deterministic noise fixtures.

**Spoken answer:** Consume input under a state machine, scan for a valid bounded header and reject bad size/version/checksum without unlimited growth.

**Deeper explanation/example:** Handle a candidate magic prefix at the end of a buffer; do not repeatedly retry the same bytes. Set a per-frame deadline and a bounded scan/work budget.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** Allocate the declared length and wait indefinitely.

**Follow-up:** How do you test noise followed by a valid frame?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Memory/work/progress bound and deterministic noise fixtures. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q154 — Design version negotiation for a Linux–MCU link.

**Tags:** EL/FW; intermediate; coding practical; coding. **Assesses:** Compatibility matrix and fail-safe unsupported behavior.

**Spoken answer:** Exchange protocol version/capabilities and session identity before commands; accept only explicitly compatible schemas.

**Deeper explanation/example:** Distinguish transport frame version from message payload version if needed. Unknown optional fields may be skipped only under a documented length/schema policy. Reject unsafe unsupported commands.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** Same compiler version means firmware protocols are compatible.

**Follow-up:** How do you upgrade one endpoint first?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Compatibility matrix and fail-safe unsupported behavior. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q155 — The same valid command executes twice after timeout. What failed?

**Tags:** EL/FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Correct distributed side-effect reasoning.

**Spoken answer:** The sender could not distinguish lost response from lost execution, and receiver duplicate handling was absent or insufficient.

**Deeper explanation/example:** Capture sequence/session and action/ACK timestamps. Fix transaction semantics rather than merely lengthening the timeout. Test ACK loss after action completion.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** Use a larger CRC.

**Follow-up:** Would TCP alone make the command exactly-once?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct distributed side-effect reasoning. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q156 — How choose a protocol timeout?

**Tags:** EL/FW; intermediate; technical screen; conceptual. **Assesses:** Budget-based timeout with stale-command policy.

**Spoken answer:** Derive it from allowed response budget, transport duration, processing/queueing and recovery policy, then validate under load.

**Deeper explanation/example:** At a configured baud, framing bits determine byte time; scheduling and buffering add delay. State assumptions and retain end-to-end absolute deadlines. No universal timeout fits every board.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** Pick one second because it is common.

**Follow-up:** How do retries affect worst-case command age?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Budget-based timeout with stale-command policy. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q157 — Communication stops after either endpoint resets. What investigate?

**Tags:** EL/FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Session-scoped authority and bounded recovery tests.

**Spoken answer:** Check session/sequence state, handshake, buffer reset, UART reinitialization and peer detection; old state may be mistaken for valid continuation.

**Deeper explanation/example:** Inject reset at each protocol state and require bounded return to a compatible session. Keep reset epoch observable; avoid carrying stale command authority across reconnect.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** Only reset both devices together.

**Follow-up:** How do you stop an old queued command after reconnect?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Session-scoped authority and bounded recovery tests. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q158 — Validate a packet field used as an array index.

**Tags:** EL/FW; intermediate; coding practical; coding. **Assesses:** Syntactic and semantic validation before action.

**Spoken answer:** Check field range against table length before access, then validate semantic support for that entry.

**Deeper explanation/example:** A CRC-valid packet can still contain invalid values. Bounds are necessary but a reserved command ID can still be forbidden. Reject before mutation/side effects.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** A valid checksum proves every field is safe.

**Follow-up:** What if index arithmetic adds an offset?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Syntactic and semantic validation before action. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q159 — How do checksums, CRCs and MACs differ?

**Tags:** EL/FW; intermediate; technical screen; conceptual. **Assesses:** Correct integrity/authentication/confidentiality boundaries.

**Spoken answer:** Checksums/CRCs target accidental corruption with different detection properties; a keyed MAC authenticates integrity under cryptographic assumptions.

**Deeper explanation/example:** A hostile sender can recompute an unkeyed CRC. Confidentiality is another property. Choose security primitives from a reviewed threat model, not a custom CRC-plus-secret scheme.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** CRC is encryption.

**Follow-up:** What key lifecycle does a MAC require?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct integrity/authentication/confidentiality boundaries. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.

## Q160 — A command is valid but dangerously stale. Where enforce freshness?

**Tags:** EL/FW; intermediate; debugging/code review; debugging/scenario. **Assesses:** Freshness independent of packet validity and defined reset behavior.

**Spoken answer:** At the authority boundary using a bounded lease/session/sequence policy in the receiving control domain.

**Deeper explanation/example:** Linux timestamps alone may not align with MCU time. Define clock/age assumptions and use receiver monotonic time for lease expiry. Reset must not renew an old queued command inadvertently.

**Assumptions/version:** B01 frame is exact-message only; B03/I05 stream/session layers remain pending.

**Common incorrect answer:** Check CRC and assume newest packet is current.

**Follow-up:** How do you handle sequence wrap and clock reset?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Freshness independent of packet validity and defined reset behavior. [Learning: M12](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m12). References: B01; R20; R21; R22.
