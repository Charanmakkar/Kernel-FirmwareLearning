# A01 — Sensor driver using the IIO subsystem

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: Advanced. Estimated effort: 28 hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: Read existing ADXL345 driver; implement isolated educational IIO variant or a justified tested patch; register fixture tests and client. Prerequisites: I03; M13; ADXL345 datasheet. Role/skills mapping: S09/S14/S15 in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: ADXL345 I2C on BeagleBone Black Rev C; exact board kernel/image pin pending. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
Bus register reads → IIO channels/raw/scale → userspace acquisition → fault report
```

State/failure obligations: Check identity and supported config; propagate bus failures; serialize mode changes; release active work before teardown. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: Read existing ADXL345 driver; implement isolated educational IIO variant or a justified tested patch; register fixture tests and client. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: Known signed sample fixtures; wrong identity; bus NACK/timeout; invalid config; unbind; orientation sanity and reported scale.

Exit criteria: **Use documented IIO ABI; known raw-to-unit conversions correct; physical orientation agrees within stated device/test tolerances.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: Plan only; no invented wiring; exact breakout, pinmux, driver implementation and physical readings pending. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: Why IIO rather than a custom ioctl? How do raw value, scale and physical units relate?

Extensions after minimum acceptance: Add triggered buffer/interrupt and runtime PM only after raw acquisition/lifetimes pass. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
