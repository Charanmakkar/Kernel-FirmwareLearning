# C01 — Industrial monitoring and edge gateway

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: Capstone. Estimated effort: 50 hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: Integrated image, serial service, MCU/sim endpoint, config schema/store, health CLI, CI fixtures and acceptance report. Prerequisites: B03/I01/I05/A03; G2/G3/G5. Role/skills mapping: S07/S08/S11/S18/S19/S21/S22 in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: Linux QEMU appliance + MCU simulator first; chosen Linux/Nucleo boards later. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
One serial path → validated telemetry → bounded log + health snapshot; persistent config and signed image update
```

State/failure obligations: Monotonic freshness, bounded storage, validated atomic config replacement, reconnect with epoch, health-gated rollback. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: Integrated image, serial service, MCU/sim endpoint, config schema/store, health CLI, CI fixtures and acceptance report. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: Nominal sample; bad CRC/version; link loss; duplicate/old frame; worker stall; disk full; corrupt config; interrupted/rejected update.

Exit criteria: **All C01-R requirements in CAPSTONE_REQUIREMENTS.md have reproducible evidence and independent architecture defense.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: Plan only; dependency integrations, complete source/config, fixtures and capstone execution pending. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: What is the primary failure boundary? Which evidence distinguishes a transport fault from a sensor fault?

Extensions after minimum acceptance: Add MQTT/SocketCAN only if target JD needs it; optional anomaly score remains outside health-critical acquisition. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
