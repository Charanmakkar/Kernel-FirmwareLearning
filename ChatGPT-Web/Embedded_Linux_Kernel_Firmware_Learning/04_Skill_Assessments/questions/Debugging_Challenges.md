# Debugging and review challenges

All supplied traces are synthetic teaching inputs. Do not describe them as measurements from the projects. Allowed tools: editor, compiler, local documentation, debugger, and static/sanitizer tools in a disposable host environment. No AI for independent attempts. For each challenge submit a hypothesis table with supporting and contradicting evidence, a minimal repair, a regression test, and remaining uncertainties. Score each out of 100 using the common rubric; pass at 75 with no critical gate failure.

## DBG01 Packet length review

Prerequisites M02–M03. Time 30 minutes. Review `fixtures/broken_parser.c` without initially running it. Inputs: empty input; one-byte input `04`; `02 41 42`; `11` followed by 17 data bytes; and `03 41`. Identify each access that requires a precondition, repair the contract so output changes only on success, and add tests. Expected deliverable is a complete C function and executed tests. Critical gate: no out-of-bounds access on any supplied case. Remediation: checked lengths and transactional parsing.

## DBG02 Queue wakeup review

Prerequisites M07. Time 35 minutes. Review `fixtures/broken_queue.c`. Assume two consumers, one queued byte, spurious wakeups, and shutdown while empty. Explain at least three failing interleavings and repair the predicate. Submit a state-based test design and the corrected function. Critical gate: no empty-queue access and no indefinite required shutdown. Remediation: Q071, Q092 and C90.

## DBG03 Busy-loop trace

Prerequisites M06. Time 20 minutes. Read spin.trace. State the supported fault, the minimum control-flow repair, and tests for hangup with and without buffered data. List one electrical hypothesis the trace does not prove. Deliver a trace annotation and a small event-loop decision table. Critical gate: no endless immediate retry on EOF. Remediation: poll readiness and connection state transitions.

## DBG04 Kernel lifetime report

Prerequisites M09–M10. Time 35 minutes. Read kernel_oops.txt. Explain a possible remove-versus-work race. State the additional exact-source and build evidence needed before claiming root cause. Design teardown ordering that stops requeue, waits for work, and frees only after users quiesce. Include the lock-deadlock risk of synchronous cancellation. Critical gate: no callback can access freed state. Remediation: devres scope, workqueue cancellation and reference ownership.

## DBG05 Firmware watchdog record

Prerequisites M12–M13. Time 30 minutes. Read fault_summary.txt. Draw the supported blocking dependency in prose, calculate which recorded heartbeats are stale at 1400 ms using the stated 100 ms control timeout, and propose an isolation design. Do not infer absent fault-register values. Include how to validate the watchdog's actual hardware behavior later. Critical gate: do not feed solely because the logger still executes. Remediation: bounded queues, useful-progress supervision and priority inversion.

## DBG06 Driver API review

Prerequisites M10–M11. Time 40 minutes. Review this proposed design: hard IRQ handler takes a mutex, reads an I2C register, appends to an unbounded list, calls copy_to_user on a stored user pointer, and schedules work holding a devm pointer; removal only returns. Identify context, trust-boundary, allocation, ownership and teardown defects. Redesign with a threaded or deferred bus read, bounded queue, ordinary read/poll interface, and explicit disconnect state. Deliver a context table and removal sequence. Critical gate: user access and asynchronous state cannot outlive valid ownership. Remediation: Q095 and Q121–Q130.

## DBG07 Performance evidence review

Prerequisites M15. Time 25 minutes. A report claims 99.9th-percentile latency of 2 ms from 100 samples and calls this a hard real-time guarantee. State what the sample supports, what it does not, and a better measurement plan. Include intended/actual wake times, workload, clock, raw samples, distribution, outliers and host interference. Critical gate: do not relabel an observed maximum as a proven bound. Remediation: Q088, Q159 and Q198.

## DBG08 Update failure review

Prerequisites M16. Time 40 minutes. An updater writes the active slot, accepts any file with a matching CRC, changes boot flags before syncing data, and marks healthy when PID 1 starts. Identify four independent defects and propose an interruption matrix. Include shared-data rollback compatibility. Critical gate: reject unauthorized images and preserve a documented recovery path. Remediation: Q100, Q176–Q177 and A03.
