# Buildroot, Yocto and reproducibility

## Q161 — Compare Buildroot and Yocto for a product.

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Requirements-based comparison and lifecycle tradeoffs.

**Spoken answer:** Both can produce embedded Linux systems, with different configuration/metadata/package workflows and integration costs.

**Deeper explanation/example:** Choose from team expertise, BSP ecosystem, customization, package/update strategy and maintenance needs. Do not equate a quick first build with lower lifetime product cost.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** Yocto is a Linux distribution identical for every board.

**Follow-up:** Which artifacts would you preserve to reproduce an image?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Requirements-based comparison and lifecycle tradeoffs. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q162 — What is a Buildroot external tree?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Declarative customization and clean-build evidence.

**Spoken answer:** It keeps product configuration, packages and board customization outside the upstream Buildroot source tree under its supported integration mechanism.

**Deeper explanation/example:** Store defconfig and relevant kernel/rootfs/package inputs, not only a generated output directory. Check the selected release's layout/hooks; moving manual examples are not a pin.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** Copy random files into output/target and call it reproducible.

**Follow-up:** When can an incremental rebuild be misleading?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Declarative customization and clean-build evidence. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q163 — Describe the minimum complete custom application package.

**Tags:** EL/KD; intermediate; coding practical; coding. **Assesses:** Complete source-to-target integration and licensing traceability.

**Spoken answer:** Declare source/version/hash/license, build/install steps and configuration integration, with explicit dependencies.

**Deeper explanation/example:** For local educational sources, record a versioned immutable input and license. Install only required runtime artifacts and include startup policy separately. Build success must be followed by guest/service tests.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** A shell command copying a host binary is a target package.

**Follow-up:** How do you prove the binary uses the target ABI?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Complete source-to-target integration and licensing traceability. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q164 — What is a Yocto layer, recipe, package and image?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Correct metadata/build/runtime boundaries.

**Spoken answer:** A layer organizes metadata; a recipe describes build tasks; packages contain outputs; an image selects/install outputs into a target filesystem.

**Deeper explanation/example:** One recipe can produce multiple packages. Layers are not automatically runtime files, and adding a recipe does not necessarily install its package in an image.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** Every layer becomes a partition on the device.

**Follow-up:** How does a bbappend alter an existing recipe?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct metadata/build/runtime boundaries. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q165 — A recipe builds but the target service cannot start. What inspect?

**Tags:** EL/KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Runtime artifact/dependency diagnosis.

**Spoken answer:** Check installed package content, runtime dependencies, interpreter/loader, service configuration, permissions and selected image inclusion.

**Deeper explanation/example:** DEPENDS and runtime dependency declarations solve different edges. Inspect actual rootfs/package metadata and service logs rather than adding host packages.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** BitBake success proves runtime completeness.

**Follow-up:** What if a script needs an undeclared interpreter?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Runtime artifact/dependency diagnosis. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q166 — What is the SDK used for?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Coherent compiler/sysroot/image relationship.

**Spoken answer:** It supplies a compatible target toolchain/sysroot and environment for application development against the selected image context.

**Deeper explanation/example:** Record SDK/image lineage. An arbitrary compiler with a matching CPU name may still use incompatible libc/ABI or libraries. Validate an SDK-built client on the target.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** Any AArch64 compiler is equivalent.

**Follow-up:** How do you distribute updated headers/libraries to application developers?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Coherent compiler/sysroot/image relationship. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q167 — An image changes despite unchanged application source. Why?

**Tags:** EL/KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Complete input model and measured comparison.

**Spoken answer:** Inputs include layers/revisions, configs, downloaded sources, tools and nondeterministic metadata; caches can also hide undeclared dependencies.

**Deeper explanation/example:** Preserve manifests and compare artifacts with a controlled clean rebuild. A reproducible configuration is a prerequisite, not proof of byte-for-byte reproducible output.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** The source commit alone completely defines every image.

**Follow-up:** How do timestamps/build paths affect reproducibility?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Complete input model and measured comparison. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q168 — What does sstate or a build cache guarantee?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Cache model versus independent verification.

**Spoken answer:** It can reuse matching task outputs under the tool's dependency model, accelerating builds; it is not itself proof of reproducibility or correctness.

**Deeper explanation/example:** Trust boundaries, undeclared inputs and cache corruption still matter. Rebuild a small controlled comparison when investigating differences; do not routinely erase all caches without a hypothesis.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** A cache hit proves the output matches an independent clean build.

**Follow-up:** How would you test a suspected undeclared dependency?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Cache model versus independent verification. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q169 — What belongs in license and SBOM evidence?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Artifact-linked inventory and accurate limits.

**Spoken answer:** Actual shipped components/versions and license/dependency metadata, with source/notice obligations reviewed for the distribution context.

**Deeper explanation/example:** An SBOM helps inventory and vulnerability analysis but does not prove a product is secure or legally compliant. Keep generated records tied to the shipped image hash.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** A license scanner or SPDX file settles every obligation.

**Follow-up:** How do local patches and bundled dependencies affect records?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Artifact-linked inventory and accurate limits. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.

## Q170 — A clean image build runs out of memory. What change first?

**Tags:** EL/KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Measured resource diagnosis and controlled build settings.

**Spoken answer:** Confirm OOM evidence, host requirements, free memory/swap and parallelism; reduce concurrent tasks rather than changing application logic.

**Deeper explanation/example:** Record build configuration and resource conditions. Disk exhaustion and compiler errors can look similar in a truncated log; inspect the first real failure.

**Assumptions/version:** Buildroot and Yocto are separate pinned lineages; future image builds unverified.

**Common incorrect answer:** Retry with maximum parallelism for speed.

**Follow-up:** How do you estimate disk/cache needs before Yocto?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Measured resource diagnosis and controlled build settings. [Learning: M10](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m10). References: R02; R04; R25; R34.
