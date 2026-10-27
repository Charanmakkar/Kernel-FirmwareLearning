# Phase exit tests

Pass each gate before relying on its topics in a capstone. These are independent assessments with no AI or answer keys. Local official documentation is allowed, except the oral explanation must be given without notes. Score with the 100-point practical rubric; pass at 75 with every stated critical gate satisfied. Use the actual project versions and preserve evidence.

## G01 Foundations

**Prerequisites:** M01–M04; B01 and compiler/shell basics. **Time:** 75 minutes.

**Task:** Implement Q021 and Q024; explain Q006 and Q016; inspect one ELF with readelf and show a clean Git diff.

**Test data and conditions:** Inputs: multiplication boundaries; hex 00af, odd length, invalid G, insufficient capacity; structure with char then uint32_t.

**Deliverables:** C source/tests, ELF inspection transcript, explanation of UB and padding.

**Critical gate:** Bounds and unchanged-failure behavior are mandatory.

**Remediation:** Repeat M02 integer/lifetime exercises and B01 with changed capacities.

## G02 Linux systems

**Prerequisites:** M05–M07; B02–B04. **Time:** 100 minutes.

**Task:** Implement a bounded line reader and drain-on-shutdown queue. Diagnose spin.trace and explain a descriptor reuse race.

**Test data and conditions:** Chunks ab then c\nx\n; overlong 65-byte line for a 64-byte limit; shutdown while empty and full.

**Deliverables:** Source, PTY/pipe or injected-read tests, thread shutdown transcript, failure table.

**Critical gate:** No silent truncation, data race or indefinite required shutdown.

**Remediation:** Repeat partial-I/O lab and condition-variable exercise before retesting.

## G03 Images and drivers

**Prerequisites:** M08–M11 and M14; B05 and at least one image/driver project. **Time:** 120 minutes.

**Task:** Show target build metadata and a boot log if available; review a driver user-copy path and device removal; explain a DT supplier failure.

**Test data and conditions:** A short user buffer, concurrent readers, remove during blocked read, wrong compatible string.

**Deliverables:** Build evidence, source review, matching kernel config and an explicitly pending hardware matrix.

**Critical gate:** No unsafe user pointer or asynchronous use-after-free; never invent a boot log.

**Remediation:** Repeat I02/I03 lifecycle tests in a disposable VM and verify target headers.

## G04 Firmware and RTOS

**Prerequisites:** M12–M13; I05 or a host-tested firmware logic core. **Time:** 100 minutes.

**Task:** Implement Q163–Q165; draw ISR-to-task buffer ownership; explain startup/linker agreement and priority inversion.

**Test data and conditions:** Heartbeat unseen/stale/current; FAULT then ARM; stale plausible sensor; wraparound ticks.

**Deliverables:** Portable tests, state table, stack/timing measurement plan and pending board checks.

**Critical gate:** Stale command disables permission and fault never clears implicitly.

**Remediation:** Repeat explicit state machine, watchdog and RTOS ownership lessons.

## G05 Production and diagnosis

**Prerequisites:** M15–M17; A02/A03 concepts and fault tests. **Time:** 100 minutes.

**Task:** Analyze a latency claim, review an update transition matrix, and implement or demonstrate atomic configuration replacement in a disposable directory.

**Test data and conditions:** Storage full, interrupted temporary write, invalid signature, candidate health timeout, rollback data mismatch.

**Deliverables:** Failure matrix, raw available measurements, update/configuration evidence, limitations.

**Critical gate:** No forged benchmark, unauthorized update acceptance or destruction of the only recovery path.

**Remediation:** Revisit measured-versus-proven timing, persistence sequencing and A03 recovery.

## G06 Capstone integration

**Prerequisites:** M01–M18 relevant track coverage; One capstone at minimum complete scope. **Time:** 180 minutes plus 45-minute defense.

**Task:** Run the chosen capstone from its documented setup; inject disconnect, malformed input, consumer overload and peer restart; explain one independent change.

**Test data and conditions:** Use fixed seed 2710 and record exact injected event times. For C02 include stale command and re-arm behavior.

**Deliverables:** Reproducible demo, requirement-to-test table, results, evidence gaps and 5-minute architecture explanation.

**Critical gate:** No undocumented control continuation, fabricated pass, unbounded queue or unexplained lifecycle fault.

**Remediation:** Repair the failing requirement, add regression, then retake with changed event order.
