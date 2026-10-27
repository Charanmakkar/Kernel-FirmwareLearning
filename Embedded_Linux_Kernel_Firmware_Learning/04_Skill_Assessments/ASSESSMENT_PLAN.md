# Assessment inventory and execution rules

Delivered questions/keys: D01 initial diagnostic; M01 independent exit test E-M01; B01 E01–E03 exercises and separate solutions. Program-wide G0–G7 criteria are defined in the roadmap. Later phase-exit question sets, timed coding suites, seeded Linux/kernel/firmware broken-code fixtures, crash-analysis fixtures, per-track full mocks and final practical reference solutions remain pending. A plan for those tests is not a delivered assessment.

Standard attempt record: assessment ID; prerequisites satisfied; start/end time; allowed tools and actual AI use; source/config revision; exact task/test data; actual stdout/stderr; expected-versus-observed behavior; rubric score; critical failures; remediation; retention-test date. Independent attempts exclude AI; assisted attempts are clearly labeled and cannot establish independent passage.

## Future timed formats and acceptance definitions

15-minute microtest: decode bounded bytes and explain a supplied edge case; no AI; header/manual allowed; deliver code/test/explanation. 45-minute coding task: handle fragmented pipe input with timeout and cleanup; local compiler/debugger allowed; deliver fixture, resource analysis and command log. 90-minute debugging task: seeded memory/race/hang defect; deliver initial hypotheses, minimal reproducer, fix and regression, not just a patch. These fixtures and separate reference solutions are not delivered yet.

Per-track mock design: 60 minutes, conceptual 10, coding/review 20, debugging 15, project defense 15. EL focuses partial I/O and service lifecycle; KD covers context/locking/lifetime and a probe/unbind scenario; FW covers startup, task/ISR ownership and a watchdog deadline. At least one changed-input task is done without hints. Full scripts/questions are pending.

Final practical plan: four hours after applicable gates, offline docs/compiler/debugger allowed, no AI for the independent grade. Fresh source setup, one unfamiliar failure, one constrained feature, normal/boundary/fault tests, and a 15-minute capstone defense. Proposed data: valid frame, fragmented frame, wrong version, duplicate sequence, worker stall, restart and disk-full fixture; actual runnable fixtures remain pending. Score with the gate rubric; pass >=80 and no critical failure. Retest the failed category using different data. Hardware timing claims require target instrumentation and measured evidence, not a simulation grade.
