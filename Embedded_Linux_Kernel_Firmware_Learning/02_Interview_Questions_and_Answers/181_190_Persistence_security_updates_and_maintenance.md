# Persistence, security, updates and maintenance

## Q181 — How replace persistent configuration robustly?

**Tags:** EL/KD; advanced; technical screen; conceptual. **Assesses:** Explicit visibility/durability/recovery distinction.

**Spoken answer:** Validate, write a new file in the intended filesystem, synchronize as required, atomically rename and synchronize the directory under the selected storage contract.

**Deeper explanation/example:** Preserve last-known-good schema/version recovery. Atomic visibility and power-loss durability are different; test interruption at each transition on selected filesystem/storage.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Rename alone guarantees durability against all power failures.

**Follow-up:** How do disk-full and permission errors affect the active config?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explicit visibility/durability/recovery distinction. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q182 — Power loss leaves a zero-length config. What investigate?

**Tags:** EL/KD; advanced; debugging/code review; debugging/scenario. **Assesses:** State-transition diagnosis and recoverable replacement design.

**Spoken answer:** Inspect whether the active file was truncated before replacement, write/fsync errors were ignored or metadata durability was assumed.

**Deeper explanation/example:** Reproduce with a disposable fixture and inject interruption at each write/rename/sync state. Validate old/new records at boot; never silently treat corrupt data as valid defaults without policy.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Add a checksum and keep the same truncation path.

**Follow-up:** How would you retain the previous valid generation?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: State-transition diagnosis and recoverable replacement design. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q183 — What does signing an update guarantee?

**Tags:** EL/KD; advanced; technical screen; conceptual. **Assesses:** Cryptographic boundary plus operational/key-lifecycle limits.

**Spoken answer:** It can authenticate integrity/origin under the chosen key/trust policy; it does not prove the software is healthy, safe or non-vulnerable.

**Deeper explanation/example:** Validate target compatibility and key trust before activation, then health-check a candidate. Keep private signing keys off target and out of repositories.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Signed software is automatically secure and cannot fail boot.

**Follow-up:** What happens if the signing key is compromised?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Cryptographic boundary plus operational/key-lifecycle limits. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q184 — How does A/B rollback work?

**Tags:** EL/KD; advanced; technical screen; conceptual. **Assesses:** Durable boot-attempt/health state and actual boot integration.

**Spoken answer:** Install into an inactive slot, mark a candidate with bounded boot attempts, and commit only after health criteria; otherwise boot the known-good slot.

**Deeper explanation/example:** Boot state must survive resets consistently. An updater alone cannot guarantee rollback if the bootloader never consumes attempt state or falls back. Test every interrupted transition.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Two partitions and a signed copy automatically provide rollback.

**Follow-up:** Who marks the new slot good and when?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Durable boot-attempt/health state and actual boot integration. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q185 — An image is signed but for another product. What must happen?

**Tags:** EL/KD; advanced; debugging/code review; debugging/scenario. **Assesses:** Compatibility and downgrade/migration policy.

**Spoken answer:** Reject it based on authenticated compatibility metadata before activation or writing incompatible critical state.

**Deeper explanation/example:** Signatures answer who approved bytes, not whether these bytes fit this hardware/schema. Keep product/board/storage compatibility explicit and tested.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Accept anything signed by the organization's key.

**Follow-up:** How do configuration migrations interact with rollback?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Compatibility and downgrade/migration policy. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q186 — Design a health gate before committing an update.

**Tags:** EL/KD; advanced; coding practical; coding. **Assesses:** Meaningful bounded health and fallback ownership.

**Spoken answer:** Require bounded successful boot plus essential service/data progress checks, then record success durably; failure leaves fallback available.

**Deeper explanation/example:** A running PID alone can mask deadlock or stale sensors. Define timeout and minimum checks from product requirements, and test false positives/false negatives.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Mark good immediately when the kernel starts.

**Follow-up:** What if the health service itself crashes?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Meaningful bounded health and fallback ownership. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q187 — How do secure boot, verified filesystems and signed updates differ?

**Tags:** EL/KD; advanced; technical screen; conceptual. **Assesses:** Distinct trust stages and explicit integration assumptions.

**Spoken answer:** They protect different parts of a trust chain: booted code, runtime content verification and accepted installation artifacts under their chosen policies.

**Deeper explanation/example:** Specify roots of trust, keys and rollback policy. A signed bundle does not automatically enforce boot verification; a verified rootfs does not validate mutable configuration semantics.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** They are interchangeable names for encryption.

**Follow-up:** Where does anti-rollback state live?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Distinct trust stages and explicit integration assumptions. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q188 — What is least privilege for an embedded service?

**Tags:** EL/KD; advanced; technical screen; conceptual. **Assesses:** Concrete resource permissions and tested failure behavior.

**Spoken answer:** Give only required identities, device/file access and capabilities, with isolation supported by the selected image/runtime.

**Deeper explanation/example:** Avoid root by default where feasible; separate update authority from telemetry parsing. Test denied access and preserve recovery observability. Security claims require an actual configuration review.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Run everything as root because the device is single-user.

**Follow-up:** How does hardware device access constrain sandboxing?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Concrete resource permissions and tested failure behavior. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q189 — An SBOM reports an old component version. What next?

**Tags:** EL/KD; advanced; debugging/code review; debugging/scenario. **Assesses:** Artifact/advisory/backport traceability without unsupported security claims.

**Spoken answer:** Identify the shipped artifact, patch/backport status, reachable use and relevant advisories before deciding remediation and retest scope.

**Deeper explanation/example:** Inventory is the start, not a vulnerability verdict. Record evidence and maintain an update plan; do not infer safety solely from a vendor version string or scanner score.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** An SBOM means no vulnerable dependencies exist.

**Follow-up:** How do local patches affect version interpretation?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Artifact/advisory/backport traceability without unsupported security claims. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.

## Q190 — What should a product maintenance plan contain?

**Tags:** EL/KD; advanced; technical screen; conceptual. **Assesses:** Lifecycle ownership and recoverable update strategy.

**Spoken answer:** Supported versions, dependency/security review, regression tests, key/update policy, fleet observability, recovery and end-of-support responsibilities.

**Deeper explanation/example:** A reproducible initial image does not maintain itself. Retain source/config/license/build evidence and rehearse restoration; test migrations with rollback constraints.

**Assumptions/version:** Threat/storage/boot guarantees must be stated; A03 implementation remains pending.

**Common incorrect answer:** Ship once and freeze forever because changes cause bugs.

**Follow-up:** Which obligations remain after a field update fails?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Lifecycle ownership and recoverable update strategy. [Learning: M15](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m15). References: R16; R21; R34.
