# I04 — Custom Yocto telemetry image

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: Intermediate. Estimated effort: 32 hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: Layer.conf, application recipe, image recipe/config, service unit and enablement, build configuration and SDK instructions. Prerequisites: I01; M10; sufficient Linux disk/RAM. Role/skills mapping: S10/S11/S19/S21 in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: Poky yocto-5.0.14; MACHINE=qemuarm64; separate lineage from Buildroot. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
Own layer/recipe → package + image → service → SDK-built client
```

State/failure obligations: Explicit dependencies and license checks; immutable metadata inputs; avoid downloads from arbitrary moving branches. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: Layer.conf, application recipe, image recipe/config, service unit and enablement, build configuration and SDK instructions. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: Parse/build; boot/service status; runtime dependency missing fixture; SDK compile; clean configuration replay; license manifest.

Exit criteria: **Image starts intended service; client from generated SDK runs; layers/revisions/config and actual versions archived.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: Plan only; tag/build environment, recipe implementation and boot/SDK checks pending. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: How do build-time DEPENDS and runtime RDEPENDS differ? What is a layer versus an image?

Extensions after minimum acceptance: Compare sstate cache versus reproducibility; add application package feed only with a maintenance policy. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
