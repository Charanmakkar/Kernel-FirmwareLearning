# I01 — Custom Buildroot appliance

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: Intermediate. Estimated effort: 22 hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: br2-external tree, custom package with license/hash, overlay/init script, defconfig, persistence format and boot script. Prerequisites: B02/B03/B05; M06. Role/skills mapping: S10/S11/S19/S21 in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: Buildroot 2026.08.1 qemu_aarch64_virt_defconfig; kernel 6.18.7. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
Pinned source/package → Buildroot image → init-started telemetry → separate persistent configuration
```

State/failure obligations: Validate configuration, keep last good value, bounded logs, recover missing config; avoid writing immutable rootfs. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: br2-external tree, custom package with license/hash, overlay/init script, defconfig, persistence format and boot script. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: Clean build/boot; package startup; first boot; reboot; malformed config; interrupted write; disk full.

Exit criteria: **Clean checkout reproduces accepted image behavior; source inputs/config hashes recorded; valid config survives restart.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: Plan only; upstream target file inspected, image/package implementation and builds pending. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: Which change requires a full rebuild? How do configuration and image state differ?

Extensions after minimum acceptance: Read-only rootfs, reproducibility comparison, legal-info/SBOM artifacts using supported release tools. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
