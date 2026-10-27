# A03 — Signed A/B update and rollback system

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: Advanced. Estimated effort: 28 hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: Disk layout, RAUC config/bundle manifest, development signing script, boot-state integration, health gate, interruption harness. Prerequisites: I01; M15; boot/persistence understanding. Role/skills mapping: S11/S19/S21 in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: RAUC 1.13; disposable QEMU disk; bootloader/version integration still to be selected and locked. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
Signed compatible bundle → inactive slot → candidate boot attempts → health → commit or rollback
```

State/failure obligations: Never overwrite active known-good slot; verification before activation; bounded attempts; durable metadata; key kept out of image. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: Disk layout, RAUC config/bundle manifest, development signing script, boot-state integration, health gate, interruption harness. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: Bad signature; wrong target; full disk; partial install; reset before/after activation; failed health; attempt exhaustion; successful commit.

Exit criteria: **Every defined interrupted transition yields old or candidate bootable state; unsigned/wrong-target rejected; unhealthy candidate rolls back.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: Plan only; no complete updater/boot integration or disk fault tests delivered. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: What durable state allows rollback after power loss? Which component consumes the attempt counter?

Extensions after minimum acceptance: Separate production key custody/rotation, anti-rollback requirements and secure boot chain; do not confuse these with bundle signing. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
