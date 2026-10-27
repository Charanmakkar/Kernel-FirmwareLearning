# C02 — Linux–MCU robot control and diagnostics platform

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: Capstone. Estimated effort: 54 hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: Linux supervisory app, firmware control core, simulated plant, deterministic clock/fault runner, diagnostic UI/CLI and acceptance tests. Prerequisites: B03/I05/A02; C01 integration methods; M16. Role/skills mapping: S08/S16/S17/S18/S20/S22 in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: Deterministic simulated differential-drive plant first; no connected actuators. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
Linux goal/planner → leased bounded command → MCU control/state → simulated plant → diagnostic telemetry
```

State/failure obligations: MCU owns control cadence and lease/safety state; Linux loss triggers safe output; reject stale sequence/epoch; inference never blocks control. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: Linux supervisory app, firmware control core, simulated plant, deterministic clock/fault runner, diagnostic UI/CLI and acceptance tests. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: Nominal trajectory; dropped/reordered/stale commands; Linux exit; sensor freeze; control overrun; reset epoch; malformed packet.

Exit criteria: **All C02-R criteria pass in simulation; independent defense; hardware gaps documented without production safety claims.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: Plan only; complete simulation/control/firmware reference implementations and execution pending. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: What stops motion if Linux hangs? Which simulated timing results cannot establish physical safety?

Extensions after minimum acceptance: After explicit hardware integration design: current-limited test rig, documented driver/encoder, emergency-stop and independent safety review. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
