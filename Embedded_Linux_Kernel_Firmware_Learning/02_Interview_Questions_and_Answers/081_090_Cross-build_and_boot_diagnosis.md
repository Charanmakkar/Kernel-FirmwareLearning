# Cross-build and boot diagnosis

## Q081 — What is a cross toolchain and sysroot?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Toolchain/ABI/loader consistency with inspected artifacts.

**Spoken answer:** The toolchain emits code for another target; the sysroot supplies target headers/libraries and related link context.

**Deeper explanation/example:** Compiler target, ABI, libc and loader must agree with the image. Host headers/libraries accidentally found during a build can create a plausible but wrong binary.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** A sysroot simulates the target CPU.

**Follow-up:** How would you prove which libraries were linked?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Toolchain/ABI/loader consistency with inspected artifacts. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q082 — An AArch64 binary exists but cannot execute. What check?

**Tags:** EL/KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Differentiate architecture, interpreter and permissions failures.

**Spoken answer:** Inspect ELF machine, interpreter, ABI and target libraries, plus execute permissions and mount policy.

**Deeper explanation/example:** Exec-format error differs from a missing dynamic loader, which can produce a missing-file symptom. Use file/readelf and actual target logs rather than recompiling blindly.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** Copy the host libc onto the target.

**Follow-up:** How do static linking and QEMU user mode affect diagnosis?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Differentiate architecture, interpreter and permissions failures. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q083 — Write a cross-build configuration that avoids host leakage.

**Tags:** EL/KD; intermediate; coding practical; coding. **Assesses:** Correct separation of build tools and target artifacts.

**Spoken answer:** Select the target compiler, sysroot and find-root policy explicitly; use target pkg-config metadata or a controlled wrapper.

**Deeper explanation/example:** Record the actual toolchain file, link line and ELF interpreter. A successful compile is not execution proof. Test one intentionally missing target dependency.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** Add host /usr/include until headers resolve.

**Follow-up:** Which CMake searches should run on the host?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct separation of build tools and target artifacts. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q084 — How do QEMU user mode and system mode differ?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Scope and limitations tied to the intended test.

**Spoken answer:** User mode translates target application execution against a host syscall environment; system mode emulates a machine with a guest kernel.

**Deeper explanation/example:** Use system mode for driver/kernel/boot learning. Neither mode automatically verifies physical timing, wiring, DMA controller behavior or real peripheral quirks.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** Running a target ELF in user mode tests its kernel module.

**Follow-up:** When can user mode still be useful?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Scope and limitations tied to the intended test. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q085 — Remote debugging shows wrong source lines. What inspect?

**Tags:** EL/KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Matching artifact identity and address/source mapping.

**Spoken answer:** Check binary/debug-symbol build identity, load addresses, source paths, optimization and architecture settings.

**Deeper explanation/example:** Use symbols from the exact deployed image. Source checkout resemblance is insufficient. Break at a known function and verify disassembly before trusting variables optimized away.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** The debugger is unreliable; ignore its output.

**Follow-up:** How do separate debug files or ASLR affect setup?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Matching artifact identity and address/source mapping. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q086 — Explain a platform boot chain without assuming U-Boot everywhere.

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Platform-specific sequence and diagnostic boundaries.

**Spoken answer:** Identify actual ROM/firmware stages, optional bootloader, kernel handoff, rootfs and init for the selected platform.

**Deeper explanation/example:** A QEMU direct-kernel boot can bypass a bootloader; MCU reset/vector startup is a different chain. Verify each board's trusted/loaded image and handoff data.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** Every Linux system boots through U-Boot.

**Follow-up:** Where does device tree enter the chain?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Platform-specific sequence and diagnostic boundaries. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q087 — Kernel boots but cannot mount root filesystem. What check?

**Tags:** EL/KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Stage-localized diagnosis and required early drivers.

**Spoken answer:** Check root device naming, driver built-in availability, filesystem support, image attachment and command line.

**Deeper explanation/example:** A driver built only as a module may not exist before root is mounted unless an initramfs provides it. Separate storage discovery from filesystem integrity.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** Rebuild userspace application first.

**Follow-up:** How would an initramfs help identify the failure?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Stage-localized diagnosis and required early drivers. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q088 — Kernel finds rootfs but reports no working init. What next?

**Tags:** EL/KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Distinguish mounting root from executing userspace.

**Spoken answer:** Inspect init path, executable format, loader/libraries, permissions and the configured init argument.

**Deeper explanation/example:** An existing /sbin/init can fail because its interpreter is missing. Compare the rootfs contents and kernel log return codes; do not treat all boot failures as root-device errors.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** Any shell script named init always works.

**Follow-up:** Which device mounts are needed for a minimal init environment?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Distinguish mounting root from executing userspace. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q089 — What is an initramfs compared with persistent rootfs?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Early userspace role and persistence boundary.

**Spoken answer:** An initramfs is an early RAM-backed filesystem populated from an archive; it can perform discovery and handoff before another root.

**Deeper explanation/example:** It is not necessarily a compressed disk partition, and changes vanish unless explicitly persisted. Define switch/root handoff and tool availability for the chosen setup.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** initramfs writes automatically survive reboot.

**Follow-up:** Why might it contain storage or decryption tools?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Early userspace role and persistence boundary. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.

## Q090 — What belongs in a BSP?

**Tags:** EL/KD; intermediate; technical screen; conceptual. **Assesses:** Hardware enablement and lifecycle/maintenance understanding.

**Spoken answer:** Board/platform enablement such as boot configuration, kernel/device-tree settings, drivers and integration metadata for the chosen hardware.

**Deeper explanation/example:** The exact scope varies by vendor. Treat board revision, pinmux, regulators, clocks and maintenance patches as traceable inputs, not a generic tarball that works on every board.

**Assumptions/version:** Buildroot 2026.08.1 planned virt lane; no executed guest in this release.

**Common incorrect answer:** A BSP is only a cross compiler.

**Follow-up:** What would you upstream versus keep product-specific?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Hardware enablement and lifecycle/maintenance understanding. [Learning: M05/M06](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m05). References: R02; R03; R18.
