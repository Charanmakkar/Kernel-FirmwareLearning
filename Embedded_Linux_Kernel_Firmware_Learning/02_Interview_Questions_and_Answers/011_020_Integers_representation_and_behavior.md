# Integers, representation and behavior

## Q011 — Create a checked single-bit uint32_t mask.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Unsigned operand, valid shift bound and explicit output semantics.

**Spoken answer:** Reject position>=32 and shift UINT32_C(1) by the validated count.

**Deeper explanation/example:** Use a valid output object and leave it unchanged on failure. Test positions 0,31,32 and null output. B01 eu_bit32 supplies a reference.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** Use signed 1<<31 unconditionally.

**Follow-up:** What changes if uint32_t is unavailable?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Unsigned operand, valid shift bound and explicit output semantics. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q012 — Replace only selected bits of an integer.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Preserve all outside-mask bits and identify MMIO qualification.

**Spoken answer:** Compute (old & ~mask) combined by bitwise OR with (value & mask).

**Deeper explanation/example:** The second mask prevents value from modifying unrelated bits. This is for ordinary integers, not universally safe register read-modify-write. See B01 eu_bits_update32.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** OR value into old without clearing the field.

**Follow-up:** What about write-one-to-clear registers?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Preserve all outside-mask bits and identify MMIO qualification. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q013 — Decode a signed 16-bit sensor sample portably.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Correct sign extension based on specified wire bits, not host layout.

**Spoken answer:** Assemble an unsigned 16-bit value, then map values above INT16_MAX to their intended negative numeric value in a wider signed type.

**Deeper explanation/example:** For two's-complement wire encoding, int32_t signed_value = u<=32767 ? (int32_t)u : (int32_t)u-65536. Avoid relying on an out-of-range unsigned-to-signed conversion under C11.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** Cast an unaligned byte pointer to int16_t pointer.

**Follow-up:** How would a 12-bit left-aligned sample change decoding?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct sign extension based on specified wire bits, not host layout. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q014 — Parse an unsigned decimal CLI argument robustly.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Full syntax/range/error distinction.

**Spoken answer:** Use a checked conversion, reject a leading minus for an unsigned contract, detect overflow and require full consumption.

**Deeper explanation/example:** With strtoul, reset/check errno, end pointer and destination maximum; reject empty input and undesired whitespace/sign policy explicitly. Do not silently truncate to a smaller type.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** atoi followed by a range check catches every error.

**Follow-up:** How do you reject 12abc or a value above UINT32_MAX?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Full syntax/range/error distinction. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q015 — What is the result of comparing int n=-1 with size_t cap=8?

**Tags:** All; foundation; technical screen; code-output analysis. **Assesses:** State implementation assumptions and safe comparison order.

**Spoken answer:** Under common selected data models n converts to an unsigned size type, so n<cap is false; explain the actual types first.

**Deeper explanation/example:** Validate n>=0 before casting to size_t. The surprising result arises from the usual arithmetic conversions, not a runtime bounds check.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** Negative values are always less than positive values regardless of types.

**Follow-up:** How do integer rank and representability affect the rule?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: State implementation assumptions and safe comparison order. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q016 — Test whether a positive integer is a power of two.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Zero/one/high-bit tests and explain representation tradeoff.

**Spoken answer:** Require n!=0 and test that n & (n-1) is zero using an unsigned type.

**Deeper explanation/example:** The zero guard matters because zero also satisfies the second expression. Do not assume every ring must use power-of-two capacity; B01 deliberately does not.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** Zero is a power of two.

**Follow-up:** How does this enable index masking?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Zero/one/high-bit tests and explain representation tradeoff. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q017 — Why should a protocol not serialize a native struct?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Separate representation from semantic schema and compatibility.

**Spoken answer:** Padding, alignment, endian and ABI choices are not a wire contract.

**Deeper explanation/example:** Encode fields at specified byte offsets and validate lengths. Packed layout alone does not specify byte order or make unaligned field access safe on every architecture.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** Packed guarantees portability and interoperability.

**Follow-up:** How would you evolve the wire version?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate representation from semantic schema and compatibility. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q018 — Add two size values with overflow detection.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Bound before addition and test SIZE_MAX boundaries.

**Spoken answer:** Reject a>SIZE_MAX-b before computing a+b, with b already a valid size_t.

**Deeper explanation/example:** This is needed when adding a header after checked payload multiplication. Multiplication safety does not imply total allocation safety. Keep output unchanged on rejection.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** Check whether result is negative.

**Follow-up:** How would signed addition require different checks?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bound before addition and test SIZE_MAX boundaries. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q019 — Classify char c=255 and signed right shift under C11.

**Tags:** All; foundation; technical screen; code-output analysis. **Assesses:** Do not invent one universal representation outcome.

**Spoken answer:** The conversion depends on plain-char signedness/range and implementation rules; right shift of a negative signed value is implementation-defined.

**Deeper explanation/example:** State compiler/target before describing an observed result. Prefer unsigned bit manipulation and explicit numeric reconstruction for protocol work.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** All C implementations use signed char and arithmetic shift.

**Follow-up:** Which behaviors are undefined rather than implementation-defined?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Do not invent one universal representation outcome. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.

## Q020 — What do alignment and effective type protect?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Identify alignment, alias/type and byte-order concerns separately.

**Spoken answer:** They constrain which addresses and access types may be used for objects; violating them can invalidate an otherwise plausible byte cast.

**Deeper explanation/example:** A correctly sized byte array is not automatically a suitably aligned uint32_t object. Use byte assembly or copying into a declared integer, then convert endian.

**Assumptions/version:** C11; widths and plain-char signedness must be stated.

**Common incorrect answer:** It works on x86, so the cast is portable.

**Follow-up:** Does memcpy solve endian conversion?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Identify alignment, alias/type and byte-order concerns separately. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01; R08.
