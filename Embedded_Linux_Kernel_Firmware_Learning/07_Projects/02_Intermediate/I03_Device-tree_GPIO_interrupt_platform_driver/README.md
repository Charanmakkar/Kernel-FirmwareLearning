# I03 — Device-tree GPIO/interrupt platform driver

**Delivery status: plan/specification only. The minimum complete implementation is pending.** This file defines scope and acceptance before source is authored; it is not a working project claim. Difficulty: Intermediate. Estimated effort: 24 hours, plus prerequisite study and any hardware setup.

## Problem, outcomes and prerequisites

Practical goal: Binding YAML, driver using descriptors/managed resources, board-specific DT change, event test client and unbind test. Prerequisites: I02; M09; electronics and selected board docs. Role/skills mapping: S09/S14 in the reference framework, not an employer JD. Demonstrate correctness, bounded resource use and diagnosis of the listed failure modes, then defend one implementation tradeoff independently.

Planned supported target: QEMU context tests plus BeagleBone Black Rev C physical path; board kernel pin pending. Read [environment setup](../../../00_Start_Here/ENVIRONMENT.md) before target-dependent work. Host package versions, target source hashes, compiler/configuration and generated image hashes must be recorded in VERSIONS.md when implementation is delivered. No unverified compiler/kernel/board combination is asserted to work.

## Architecture and failure contract

```text
Device-tree node/binding → probe GPIO descriptor/IRQ → deferred event → standard observable interface
```

State/failure obligations: Handle deferred resources; avoid sleeping bus operations in hard IRQ; stop IRQ/work before freeing state; bounded debounce. Name the owner and lifetime of each resource before writing callbacks. Define which context can block, who serializes shared state, what shutdown wakes, and how errors become observable. Do not silently retry forever.

Minimum source/configuration deliverables: Binding YAML, driver using descriptors/managed resources, board-specific DT change, event test client and unbind test. Expected project structure when implementation is authored: README.md, VERSIONS.md, docs/, src/, tests/, config/ and scripts/, with include/ and hardware/ only when applicable. A hardware folder must include selected board revision, actual breakout schematic, voltage, pin assignments and shared-pin restrictions before any wiring instructions. Those details are currently pending for physical projects. No guessed pin assignment is supplied.

## Build/run/deployment milestone plan

1. Lock target sources and host tools; capture known-good baseline and recovery path.
2. Author the smallest complete implementation described above, including build files and explicit interfaces.
3. Build on the supported host and run host fixtures where meaningful; preserve actual command and output evidence.
4. Deploy to the named isolated guest/simulator or board; run nominal and failure tests before adding extensions.
5. Debug one intentionally injected failure, clean up owned resources/guest artifacts, and reproduce from a clean checkout.

Exact commands, complete code, executable fixtures and cleanup scripts will be supplied with the implementation release. They are not implied by this milestone plan. Pending build/run steps must never be recorded as passed.

## Acceptance and evidence

Test scope: Wrong compatible; missing GPIO; deferred provider; edge bursts/bounce; work pending during unbind; real input transitions.

Exit criteria: **Binding validates; supported probe/error paths clean; physical IRQ count/timing documented separately from simulated tests.** Each test must name setup/input, expected behavior, actual result, target/build ID and an artifact path. Use normal/boundary/invalid/failure rows; use separate host, emulator and physical result columns. Timing/electrical/real peripheral behavior requires instrumented hardware evidence even if simulated state tests pass.

Current evidence: Plan only; exact board image, pins, wiring, binding and source pending; no physical validation. No test log, screenshot, performance result or hardware behavior is invented. If a test fails, minimize the fixture, inspect ownership/state and add a regression before resuming integration.

## Troubleshooting, demonstration and portfolio

Troubleshoot by boundaries: source/config/toolchain identity → startup/interface discovery → valid input → partial/invalid input → resource failure → teardown. Save the first unexpected return code and the smallest reproducer rather than disabling checks.

Demo plan (5–10 minutes): explain target and architecture; show a nominal path; inject one listed fault; inspect a concrete observable; reproduce the fix/regression; state the remaining target limitations. Defense questions: What does devm clean up automatically, and what asynchronous activity must you stop first?

Extensions after minimum acceptance: Compare gpio-keys/gpio-leds first; implement custom driver only for a justified teaching event protocol. Keep extensions separate from the core acceptance baseline. Resume wording must describe your own implemented and tested contribution; a supplied plan does not establish experience.
