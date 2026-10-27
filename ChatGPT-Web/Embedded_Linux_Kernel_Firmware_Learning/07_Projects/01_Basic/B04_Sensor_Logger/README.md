# B04 Multithreaded sensor simulator and logger

Build two simulated sensor producers and a CSV consumer with a bounded queue. The system runs for a selected sample count, drains on a normal termination request, joins every created thread, and exits on an output failure. Plan 12–16 hours after M07. This is evidence for POSIX threads, ownership, condition predicates, resource cleanup, and concurrency debugging.

## Learning outcomes and acceptance

Prove that shared queue fields are accessed under one mutex, that every condition wait rechecks its predicate, and that the finite run writes every produced sample exactly once. Show zero-work behavior, a full queue, normal termination during production, and a failing output stream. Race-tool success is useful evidence and does not prove the absence of every possible race.

## Architecture

Two producers generate `(sensor, sequence, value)` records. The queue holds eight records and applies backpressure when full. The main thread removes records and performs file I/O outside the queue lock, allowing producers to continue until capacity is reached. Per-sensor sequence is deterministic; global interleaving depends on scheduling and is deliberately not specified.

SIGINT, SIGTERM, and a private shutdown signal are blocked before any worker starts. A dedicated `sigwait` thread synchronously receives them. It sets the stop flag while holding the queue mutex and broadcasts to waiting producers. This avoids calling condition-variable functions from an asynchronous signal handler and avoids pretending that `volatile` provides thread synchronization. Producers decrement the active count before exit. The consumer stops when the queue is empty and no producer remains, then joins workers and the signal monitor.

If writing fails, the main thread marks failure, asks producers to stop, and drains remaining queue entries without claiming they reached disk. It returns nonzero. Flush on each record makes the teaching fault test deterministic; it is a throughput tradeoff, not a recommended high-rate logging policy.

## Environment and source navigation

Use Linux, GCC, pthreads, Make, and Python 3. `src/logger.c` contains the complete implementation; `tests/test_logger.py` checks ordering, output shape, early termination, and output failure. No hardware or external services are involved. Measured host tests do not establish real sensor sampling precision or hard deadlines. See `VERSIONS.md` and `evidence/VALIDATION.md`.

## Guided lab

```sh
make test
./build/logger build/samples.csv 100 1000
make tsan
gdb --args ./build/logger build/debug.csv 1000 1000
```

Arguments are output file, samples per producer, and a delay in microseconds. The delay is an approximate pacing interval and accumulates scheduling and work time; this is not a periodic real-time scheduler. In GDB use `info threads`, interrupt while running, and inspect a producer waiting at the full queue. Confirm that a thread waiting on a condition does not keep the mutex locked while asleep.

Run a long count from a shell and send SIGTERM from another terminal. Verify that the process returns promptly and each sensor's sequences remain contiguous. The automated test also writes to `/dev/full` to force a real operating-system I/O error. `make clean` removes binaries and generated CSV files beneath `build/`.

## Validation and practical limits

Recorded host tests passed for 1,000 total samples, zero work, early SIGTERM, and failed output. A GCC ThreadSanitizer run passed with 2,000 total samples; retain the exact command and log. Re-run on your environment because sanitizer support can differ. The queue is bounded, but lossless logging still requires either sustainable consumer throughput or a declared policy for dropping data. Blocking sensor acquisition threads may be inappropriate for an actual sensor FIFO; redesign with explicit overrun accounting when hardware is added.

## Troubleshooting and defense

A hang after production ends usually means the active-producer count or wakeup is wrong. Missing records require distinguishing data never produced from data queued but not written. Excess CPU usage suggests polling instead of predicate waits. A benchmark should state storage type, flush policy, sample size, scheduling policy, and queue depth.

Demonstrate a normal run, termination, and `/dev/full`. Explain the predicate for both waits, why wakeups are advisory, how failed thread creation is unwound, and which thread owns the output stream. A useful extension is monotonic timestamping with absolute periodic deadlines and an explicit deadline-miss metric.

## Primary references

- [POSIX condition wait specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_wait.html)
- [Linux pthread condition documentation](https://man7.org/linux/man-pages/man3/pthread_cond_init.3.html)
- [GCC sanitizer options](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)

Access date: 27 October 2026. The POSIX web endpoint returned 403 during retrieval; Linux documentation and executed behavior provide the accessible supporting references.
