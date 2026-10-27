# D01 key and remediation

Keep closed during the diagnostic. Do not assign the learner scores before reviewing their artifacts.

C25: 8 for valid endian decode without alignment assumptions, 8 for null/offset/remaining-space checks and unchanged output, 4 for useful tests, 3 for correctly identifying unsequenced modifications of i as undefined behavior under C11, 2 for parameter array adjustment. Unsafe accesses block G0 regardless of total. Remediate M01 and E-M01, then retest with a 32-bit field.

Linux20: 4 each for correct isolated file/symlink creation, permission verification, correct owned PID discovery, proc inspection with process-disappearance handling, and SIGTERM/exit confirmation. `/proc` results are dynamic; process identity can also be complicated by PID reuse. A proc path missing after enumeration is a normal race, not proof of corruption. On Linux a suitable scratch sequence is `mkdir scratch`, `cd scratch`, `touch one two`, `ln -s one alias`, `chmod 600 one`, `ls -l`, `sleep 120 &`, `pid=$!`, `cat /proc/$pid/status`, `kill -TERM "$pid"`, `wait "$pid"`; expected signal termination is handled as such, not a command-success requirement. Shell job-control output varies. This sequence is illustrative, not executed evidence. Missing environment means unassessed, not zero competence. Remediate basic shell/process labs before B02.

Concurrency15: 5 for volatile not providing atomicity/order and count++ being read-modify-write; 5 for mutex-protected state plus while-loop predicate and wake/recheck; 5 for shutdown flag/broadcast/join with declared drain/discard policy. Blocking a producer on a full queue forever after consumer shutdown is incorrect. Remediate single-owner queue plus one-mutex implementation; use a race tool where supported, then explain correctness without relying on the tool.

Architecture10: 2.5 each for distinct processor roles, MMU page translation versus MPU region protection (target-dependent), device DMA address not assumed equal to CPU pointer/physical address, and context-dependent sleep/interrupt rules. Remediate with the target memory map and callback-context table.

Debugging20: 5 for identifying partial-frame accumulation as a hypothesis, 5 for absolute deadline/recomputed remaining time and EAGAIN readiness races, 5 for bounded PTY fixture with fragmented input, 5 for measured observation and alternative explanations. Readiness does not guarantee that a later operation cannot return EAGAIN; the trace alone does not establish every cause of the CPU spin. Remediate B03 I/O state transitions and a timeout fixture.

Communication10: 4 accurate contribution, 3 evidence/limits, 3 clear next experiment. No experience is an acceptable honest starting point. Remediate by describing B01's supplied versus independent work.

Record scores, evidence, critical blockers and next task in skills_tracker.csv. Retake failed sections after at least a focused remediation cycle; use different input and state transitions. Do not average away critical failures.
