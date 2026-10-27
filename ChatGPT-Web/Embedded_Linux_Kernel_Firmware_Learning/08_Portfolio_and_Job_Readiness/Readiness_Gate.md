# Readiness gate

Apply this gate to one target role and actual JD where available. It is a preparation decision, not a prediction of selection. Use unfamiliar inputs and keep the first attempt independent.

| Dimension | Evidence | Points |
|---|---|---|
| Correctness and contracts | Working coding task with boundary/error cases | 25 |
| Reasoning and debugging | Competing hypotheses, discriminating evidence and regression | 20 |
| Ownership and concurrency | Accurate lifetime, synchronization and shutdown explanation | 20 |
| Role depth | Defensible kernel, Linux-system or MCU task relevant to the JD | 20 |
| Communication and honesty | Clear contribution, assumptions, limits and source attribution | 15 |

Use 80/100 as a local preparation threshold, require at least half the points in every dimension, and retain the assessor's reasons. Any uncorrected out-of-bounds access, dangling lifetime, deadlock, unsafe command-authority behavior or fabricated evidence fails the gate regardless of average score.

Also require one clean-build demonstration, one failed-input recovery, one project defense and one modest change made without copying the reference. A strong oral score cannot replace these practical checks. Hardware-dependent JD requirements remain gaps until the corresponding evidence exists.

After a failure, record the defect and linked module, implement a focused correction, and retest with changed data in a later session. Mark outcomes as ready for the tested scope, needs remediation, or not assessed. Reassess when the target JD or project environment changes.
