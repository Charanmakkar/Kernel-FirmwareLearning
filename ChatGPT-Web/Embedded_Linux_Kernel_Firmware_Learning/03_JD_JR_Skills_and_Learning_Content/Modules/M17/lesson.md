# M17 Integration testing and capstone engineering

## Objectives and prerequisites

Prerequisites: M03 M13 M16.

Turn requirements into acceptance tests, integrate earlier work and present evidence with clearly bounded claims.

## Lesson


A capstone should make a small system work end to end. C01 uses one primary communication path and focuses on acquisition, configuration, health and recovery. C02 separates Linux supervision from MCU control behavior and starts with a deterministic robot simulation. Reusing a parser is useful; merely renaming the parser project is not system integration.

Write requirements as observable behavior with an ID, precondition, stimulus and acceptance condition. For example: when valid telemetry stops, the gateway changes health to stale within the configured deadline without corrupting the last stored configuration. The test should manipulate time and inputs so it can check both just-before and just-after the threshold. Distinguish requirement limits from measured results.

Use unit tests for conversion and parsing, integration tests for process/protocol boundaries and system tests for boot/recovery behavior. Mocks isolate a contract but can faithfully reproduce a wrong assumption. Compare at least one transaction with the real interface later. Hardware-in-the-loop adds board behavior, but its sensors, loads and timing coverage still need to be described.

Fault injection should follow the architecture: drop, delay, duplicate or corrupt a frame; restart either endpoint; fill storage; break configuration; fail a health check; interrupt update; disconnect a sensor; stall a control task. Define the expected bounded response first. A test that never asserts the fault outcome merely proves the harness ran.

Continuous integration, or CI, should start with deterministic host checks that need no devices. Compile warnings, unit tests and protocol integration belong there. Heavier image builds and hardware tests can run separately with versioned artifacts. Never upload a successful status when an important test was skipped; report passed, failed and not run separately. KUnit offers an in-kernel unit testing framework where kernel logic can be isolated appropriately. [KUNIT]

The portfolio should contain a concise architecture, a demo script, requirements-to-test mapping, raw logs, a failure investigation and a limitation statement. Say what you wrote and which dependencies you used. Explain one design you changed after evidence. A credible account of a bug and its fix often demonstrates more depth than a long feature list.


## Worked lab and expected behavior


Run C01 and C02's minimum host demonstrations and test suites. Inspect the acceptance IDs in their documentation. Add one new fault without changing the implementation first; predict the outcome, run it and explain any difference. Use the aggregate validation report only as an index; the project logs contain the evidence.

For a final defense, draw the architecture from memory, explain the wire format, identify every persistent state and walk through one restart during an active transaction. Then modify a small requirement under time pressure and update its test. This demonstrates transfer beyond a memorized demo.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

How do you know the system works? What did your mock not test? What is your own contribution? Interview bank: project defense and systems design.

## Mastery checklist

- Map every capstone requirement to a test.
- Demonstrate recovery under one injected fault.
- Explain scope and untested hardware.
- Modify behavior without breaking existing acceptance.

## Primary references

[KUNIT] Kernel unit testing. C01 and C02 provide original requirements and acceptance tests. Project-specific sources govern actual hardware contracts.
