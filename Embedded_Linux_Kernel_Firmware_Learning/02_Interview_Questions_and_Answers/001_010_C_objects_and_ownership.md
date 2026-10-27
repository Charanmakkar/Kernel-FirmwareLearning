# C objects and ownership

## Q001 — Implement a bounded big-endian 16-bit read.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Bounds proof plus unchanged-output test.

**Spoken answer:** Validate pointer/output and offset before subtracting remaining size; assemble two unsigned bytes; commit output only on success.

**Deeper explanation/example:** Check offset>size first, then size-offset<2. Test offsets 0, size-2, size-1 and SIZE_MAX. See E-M01 for the separate complete solution.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** Testing offset+2<=size can wrap; casting to uint16_t pointer assumes alignment and endian.

**Follow-up:** What if output aliases input?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bounds proof plus unchanged-output test. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q002 — Write a checked allocation-size helper.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Pre-multiplication check and explicit zero/output semantics.

**Spoken answer:** Reject multiplication when b is nonzero and a>SIZE_MAX/b, then assign a*b.

**Deeper explanation/example:** Zero factors are valid zero-size results. Keep output unchanged on overflow; the caller still decides whether zero allocation is meaningful. B01 eu_size_mul is the implementation.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** Multiply then compare against SIZE_MAX.

**Follow-up:** How does subsequent header-size addition change the check?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Pre-multiplication check and explicit zero/output semantics. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q003 — Copy a bounded string into a fixed buffer with an explicit policy.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Distinguish string from byte span and state truncation/overlap contract.

**Spoken answer:** Accept source length separately, reserve one byte for the terminator and reject insufficient capacity before copying.

**Deeper explanation/example:** For reject-on-truncation, require cap>0 and source_length<cap. Only copy a promised readable region; source length cannot validate arbitrary memory. Specify overlap policy or use memmove.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** Calling strlen on untrusted unterminated bytes.

**Follow-up:** How do you represent embedded zero bytes?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Distinguish string from byte span and state truncation/overlap contract. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q004 — Design an ownership-safe function returning parsed data.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Identify owner, lifetime, valid bounds and cleanup on every return.

**Spoken answer:** Return copied fields in caller-owned output, or explicitly document a borrowed view and its lifetime.

**Deeper explanation/example:** B01 copies at most 64 payload bytes. A zero-copy view can be useful but must not outlive the receive buffer or survive its reuse without ownership transfer.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** Return a pointer to an automatic local array.

**Follow-up:** How would a buffer pool change ownership?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Identify owner, lifetime, valid bounds and cleanup on every return. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q005 — What does const guarantee?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Separate access qualification from the actual object's definition.

**Spoken answer:** It restricts modification through a qualified access path; it does not confer ownership or synchronization.

**Deeper explanation/example:** A const byte pointer can still observe data changed through another legal non-const alias. A const pointer object and pointer-to-const protect different operations.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** Const means stored in ROM or immutable everywhere.

**Follow-up:** Can casting away const ever be legal?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate access qualification from the actual object's definition. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q006 — Implement a resource cleanup path after several allocations.

**Tags:** All; foundation; coding practical; coding. **Assesses:** No leaks, double free or dependency inversion on each injected failure.

**Spoken answer:** Track acquired resources and unwind in reverse dependency order; one cleanup section can keep failure paths consistent.

**Deeper explanation/example:** Initialize handles to invalid values. If buffer allocation follows opening a file, free the buffer before closing dependent context. Do not retry close blindly after an ambiguous platform error.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** Return immediately on every error without releasing earlier resources.

**Follow-up:** When is goto cleanup preferable to nested conditionals?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: No leaks, double free or dependency inversion on each injected failure. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q007 — Explain automatic, static and allocated storage duration.

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Distinguish scope, duration, linkage and ownership.

**Spoken answer:** Automatic objects last for their block activation, static objects for program execution, and allocated objects until release.

**Deeper explanation/example:** Scope governs name visibility; lifetime governs valid object access. A static local has block scope and program lifetime. Stack/heap terminology alone does not describe C's rules.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** A pointer keeps its pointee alive.

**Follow-up:** Can a returned struct contain a dangling pointer?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Distinguish scope, duration, linkage and ownership. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q008 — Predict int i=1; int j=i++ + i++; under C11.

**Tags:** All; foundation; technical screen; code-output analysis. **Assesses:** Correct behavior category and a well-defined rewrite.

**Spoken answer:** The modifications are unsequenced, so the behavior is undefined; there is no portable numeric result.

**Deeper explanation/example:** Split the intended updates into separate full expressions. One compiler result is an observation, not an answer guaranteed by the language.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** It always prints 3 or depends only on left-to-right evaluation.

**Follow-up:** How does independent argument evaluation differ?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct behavior category and a well-defined rewrite. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q009 — Implement overlapping byte movement safely.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Correct overlap policy and zero-length boundaries.

**Spoken answer:** Use memmove for potentially overlapping regions, or choose copy direction after a valid same-object range analysis.

**Deeper explanation/example:** memcpy requires nonoverlapping regions. A manual reverse loop must avoid unsigned underflow at zero length. Library use is often clearer than recreating optimized primitives.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** memcpy is safe because both pointers are valid.

**Follow-up:** How would you test forward/backward overlap?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct overlap policy and zero-length boundaries. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.

## Q010 — How do arrays differ from pointers at function boundaries?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Explain adjustment and caller size obligations.

**Spoken answer:** A real array has a compile-time object size; array parameters adjust to pointers and lose that size information.

**Deeper explanation/example:** sizeof local_array measures its bytes, whereas sizeof parameter measures a pointer. Pass count or an explicit span contract. Pointer arithmetic remains bounded by the original array.

**Assumptions/version:** ISO C11; valid live pointer regions are caller preconditions.

**Common incorrect answer:** sizeof parameter gives original array capacity.

**Follow-up:** What does a static array parameter annotation promise?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explain adjustment and caller size obligations. [Learning: M01](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m01). References: R01.
