# Tools, ABI, C++ and workflow

## Q031 — Explain compilation versus linking.

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Differentiate declarations, definitions, object selection and runtime loading.

**Spoken answer:** Compilation translates each translation unit to object code; linking resolves symbols and lays out a complete image with libraries.

**Deeper explanation/example:** An undefined reference can come from a missing definition, omitted object, C/C++ linkage mismatch or library order. Inspect symbols and the exact link line instead of changing includes blindly.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** An include file causes its implementation to be linked.

**Follow-up:** How do static and shared libraries differ?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Differentiate declarations, definitions, object selection and runtime loading. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q032 — A declaration is visible but linking reports undefined reference. What next?

**Tags:** All; foundation; debugging/code review; debugging/scenario. **Assesses:** Evidence-driven symbol-resolution diagnosis.

**Spoken answer:** Inspect the expected symbol, object/library definitions and exact link inputs; check C++ name mangling and archive order.

**Deeper explanation/example:** Use nm/readelf equivalents on the actual target objects. Headers can declare a function whose source was never built. Record target architecture before comparing similarly named libraries.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** Add more header includes until the linker succeeds.

**Follow-up:** What if the symbol exists only as local/static?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Evidence-driven symbol-resolution diagnosis. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q033 — Write a minimal Make rule that rebuilds after header changes.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Correct dependencies plus clean-build verification.

**Spoken answer:** Declare source/header prerequisites, compile with explicit flags and use a generated output directory prerequisite.

**Deeper explanation/example:** B01 Makefile is a small complete example. Larger projects can generate dependencies with compiler -MMD/-MP; command/flag changes also need a consistent build strategy.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** Only .c timestamps affect outputs.

**Follow-up:** Why can a stale object hide an ABI mismatch?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct dependencies plus clean-build verification. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q034 — What is an ABI?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Connect a concrete layout/call mismatch to toolchain evidence.

**Spoken answer:** It is the binary interface contract for calling conventions, type layout, registers, symbols and related platform rules.

**Deeper explanation/example:** Two files can agree in C declarations but disagree in float ABI, struct packing or architecture. Inspect compiler target/options and binary metadata. Source API compatibility does not ensure binary compatibility.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** ABI is just the list of function names.

**Follow-up:** How does LLP64 differ from LP64?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Connect a concrete layout/call mismatch to toolchain evidence. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q035 — How do linker scripts and map files help firmware?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Explain sections, memory regions and startup relationship.

**Spoken answer:** A linker script maps sections into target memory; a map file shows actual placement, size and symbol allocation.

**Deeper explanation/example:** Startup must copy initialized .data from load location and zero .bss at run location. Verify stack/heap/vector placement against the MCU memory map.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** The linker automatically knows every board's memory layout.

**Follow-up:** What is load address versus execution address?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explain sections, memory regions and startup relationship. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q036 — What should a small code review prioritize?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Name concrete failure cases and evidence, not generic praise.

**Spoken answer:** Correctness contracts, resource lifetime, concurrency, error paths and tests before style preferences.

**Deeper explanation/example:** Walk one successful operation, one malformed input and each partial acquisition/cleanup path. A tidy diff can still introduce asynchronous use-after-free.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** Style compliance proves maintainability and correctness.

**Follow-up:** How would you reduce a review's uncertainty?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Name concrete failure cases and evidence, not generic praise. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q037 — How does C++ RAII help embedded software?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Tie destructor/lifetime semantics to explicit ownership.

**Spoken answer:** It binds resource release to object lifetime, reducing manual cleanup errors when ownership is clear.

**Deeper explanation/example:** A file/lock wrapper can release on all exits. Consider move-only ownership, exception policy, allocation budget and target runtime support. It does not solve dangling borrowed references or device ordering.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** RAII requires heap allocation or garbage collection.

**Follow-up:** How would you represent a unique DMA buffer owner?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Tie destructor/lifetime semantics to explicit ownership. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q038 — Design a move-only file-descriptor owner.

**Tags:** All; foundation; coding practical; coding. **Assesses:** Exactly-once ownership and valid moved-from state.

**Spoken answer:** Store one valid descriptor or invalid sentinel, close it once in destruction, delete copying and transfer ownership on move.

**Deeper explanation/example:** Move assignment must release its current resource before taking another and leave the source invalid; handle self-move policy. A complete implementation depends on the selected error/destructor policy.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** Copy the integer descriptor and let both destructors close it.

**Follow-up:** When should you dup instead of transfer?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Exactly-once ownership and valid moved-from state. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q039 — A build passes locally but fails in CI. How investigate?

**Tags:** All; foundation; debugging/code review; debugging/scenario. **Assesses:** Identify and declare the actual missing input/assumption.

**Spoken answer:** Compare pinned sources, tool versions, environment, clean state and exact failing command; reproduce in the CI environment.

**Deeper explanation/example:** Case-sensitive paths, undeclared dependencies, generated files and host-library leakage are candidates. A clean build is a discriminating test, not proof that CI is wrong.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** Disable warnings or retry until green.

**Follow-up:** How would you prevent the same class of failure?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Identify and declare the actual missing input/assumption. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.

## Q040 — What belongs in an engineering commit and automation script?

**Tags:** All; foundation; technical screen; conceptual. **Assesses:** Traceability and truthful command status.

**Spoken answer:** A focused change, reason, relevant verification and reproducible commands with explicit failures.

**Deeper explanation/example:** Scripts should propagate nonzero exit codes and avoid swallowing stderr. Keep secrets/generated binaries out of source history. Review the diff before committing; tests run on one host have a limited claim.

**Assumptions/version:** Linux ELF examples; C++ behavior follows the chosen standard/toolchain and target policy.

**Common incorrect answer:** A script printing PASS means the command succeeded.

**Follow-up:** How do you link logs to a source revision?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Traceability and truthful command status. [Learning: M02](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m02). References: R18; R19.
