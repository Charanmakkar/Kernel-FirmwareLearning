# Phase exit marking guidance

Use the rubric in Scoring_and_Evidence.md and the specific criteria below. A missing board can leave a hardware check pending, but it cannot be converted into a passed execution criterion. Grade the available host/emulator scope explicitly.

## G01 Foundations

Award correctness only when the stated test conditions are demonstrated or accurately analyzed. Required evidence: C source/tests, ELF inspection transcript, explanation of UB and padding. Reject a pass if this gate fails: Bounds and unchanged-failure behavior are mandatory. Compare mechanisms to the relevant interview answers and project acceptance tests; do not award points merely for matching wording. For retest, use different input sizes or fault order and require the learner to explain why the correction generalizes. Remediation: Repeat M02 integer/lifetime exercises and B01 with changed capacities.

## G02 Linux systems

Award correctness only when the stated test conditions are demonstrated or accurately analyzed. Required evidence: Source, PTY/pipe or injected-read tests, thread shutdown transcript, failure table. Reject a pass if this gate fails: No silent truncation, data race or indefinite required shutdown. Compare mechanisms to the relevant interview answers and project acceptance tests; do not award points merely for matching wording. For retest, use different input sizes or fault order and require the learner to explain why the correction generalizes. Remediation: Repeat partial-I/O lab and condition-variable exercise before retesting.

## G03 Images and drivers

Award correctness only when the stated test conditions are demonstrated or accurately analyzed. Required evidence: Build evidence, source review, matching kernel config and an explicitly pending hardware matrix. Reject a pass if this gate fails: No unsafe user pointer or asynchronous use-after-free; never invent a boot log. Compare mechanisms to the relevant interview answers and project acceptance tests; do not award points merely for matching wording. For retest, use different input sizes or fault order and require the learner to explain why the correction generalizes. Remediation: Repeat I02/I03 lifecycle tests in a disposable VM and verify target headers.

## G04 Firmware and RTOS

Award correctness only when the stated test conditions are demonstrated or accurately analyzed. Required evidence: Portable tests, state table, stack/timing measurement plan and pending board checks. Reject a pass if this gate fails: Stale command disables permission and fault never clears implicitly. Compare mechanisms to the relevant interview answers and project acceptance tests; do not award points merely for matching wording. For retest, use different input sizes or fault order and require the learner to explain why the correction generalizes. Remediation: Repeat explicit state machine, watchdog and RTOS ownership lessons.

## G05 Production and diagnosis

Award correctness only when the stated test conditions are demonstrated or accurately analyzed. Required evidence: Failure matrix, raw available measurements, update/configuration evidence, limitations. Reject a pass if this gate fails: No forged benchmark, unauthorized update acceptance or destruction of the only recovery path. Compare mechanisms to the relevant interview answers and project acceptance tests; do not award points merely for matching wording. For retest, use different input sizes or fault order and require the learner to explain why the correction generalizes. Remediation: Revisit measured-versus-proven timing, persistence sequencing and A03 recovery.

## G06 Capstone integration

Award correctness only when the stated test conditions are demonstrated or accurately analyzed. Required evidence: Reproducible demo, requirement-to-test table, results, evidence gaps and 5-minute architecture explanation. Reject a pass if this gate fails: No undocumented control continuation, fabricated pass, unbounded queue or unexplained lifecycle fault. Compare mechanisms to the relevant interview answers and project acceptance tests; do not award points merely for matching wording. For retest, use different input sizes or fault order and require the learner to explain why the correction generalizes. Remediation: Repair the failing requirement, add regression, then retake with changed event order.
