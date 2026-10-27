# M15 reference solution and reasoning

Correlate application timestamps with scheduling/wakeup events, I/O syscall durations, lock waiting and queue depth. A blocked fsync suggests storage-related delay; runnable-but-not-scheduled suggests contention; long mutex hold time suggests serialization; periodic queue release suggests batching. Repeat with the same workload and compare tail distributions and correctness. A single improved average cannot justify a deadline claim.
