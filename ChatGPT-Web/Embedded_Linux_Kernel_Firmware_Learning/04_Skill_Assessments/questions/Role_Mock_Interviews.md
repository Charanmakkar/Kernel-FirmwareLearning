# Role mock interviews

Run one role mock per week during revision. Each lasts 75 minutes and is independent: no AI, hidden assistance, or answer key. Local compiler and official documentation are allowed only during the practical section if the interviewer states so before starting. Use a partner or record yourself; a self-review is still labeled self-review. Submit recording or notes, source/test output, scores, and three concrete weaknesses. Pass at 75/100 with all critical gates and at least half the points in every section. Retake with different bank questions after remediation.

## MOCK L Embedded Linux developer

Prerequisites G01–G02 and a system-programming project. First 5 minutes: clarify a telemetry daemon's input rate, maximum record, shutdown and persistence requirements. Next 15 minutes: Q052 partial I/O, Q059 deadlines, Q071 condition predicates. Next 25 minutes: implement strict numeric parsing and a blocking complete-write helper, using inputs from C15 and a pipe. Next 20 minutes: diagnose spin.trace, explain a lost-wakeup scenario and define regression tests. Final 10 minutes: defend B03 or B04 and accurately label host versus hardware evidence.

Score requirements/communication 10, concepts 20, coding 30, debugging 25, project defense 15. Critical gates: no unchecked length/overflow, unsynchronized shared access, endless EOF loop or invented test result. Remediation: M03, M06, M07 and M15 according to the failed section.

## MOCK K Kernel driver and BSP developer

Prerequisites G01–G03 and I02 or I03. First 5 minutes: establish kernel version/configuration, target and hardware enumeration. Next 15 minutes: Q105 bindings, Q114 locking and Q116 managed lifetimes. Next 25 minutes: review a proposed read path that copies to userspace under a spinlock and consumes a FIFO before checking copy result; write a corrected design with blocking/nonblocking and removal behavior. Next 20 minutes: diagnose kernel_oops.txt and a deferred-probe dependency. Final 10 minutes: defend the actual driver build and runtime evidence, including pending target tests.

Score requirements/communication 10, concepts 20, driver review 30, debugging 25, defense 15. Critical gates: no direct user-pointer dereference, sleeping in an incompatible context, callback-after-free or false target validation. Remediation: M08–M11; rerun lifecycle tests in a disposable VM.

## MOCK F MCU firmware and RTOS developer

Prerequisites G01, G04 and I05. First 5 minutes: clarify MCU, clocks, rates, deadlines and reset behavior. Next 15 minutes: Q141 startup, Q153 ISR APIs and Q155 stack evidence. Next 25 minutes: implement Q164 state transitions and Q161 sequence comparison, with wraparound, FAULT then ARM, and explicit clear tests. Next 20 minutes: analyze fault_summary.txt and ISR-to-task buffer ownership. Final 10 minutes: defend firmware architecture, watchdog policy and the difference between host logic tests and board timing evidence.

Score requirements/communication 10, concepts 20, coding 30, debugging 25, defense 15. Critical gates: stale/FAULT state cannot permit motion, ISR cannot block on task mutex, shared buffer ownership cannot overlap, no fabricated hardware results. Remediation: M12–M13 and the matching I05 test.

## AI assisted comparison mock

After one independent mock, repeat a changed problem with AI explicitly permitted. Keep prompts, edits, rejected advice and verification. Score engineering quality using the same rubric but label it assisted. Within 48 hours, explain the result and repair one injected defect without AI. The assisted score must not replace the independent score in the tracker.
