# M13 RTOS scheduling and Linux to MCU communication

## Objectives and prerequisites

Prerequisites: M07 M12.

Use tasks and queues, analyze timing and priority inversion, and make an MCU communication boundary recoverable.

## Lesson


An RTOS task is an independently scheduled execution context. Its priority matters only when it is ready to run and no higher-priority or interrupt work prevents progress. Blocking on a queue is usually preferable to polling because it states the wait condition and yields CPU time. Periodic work should use an absolute cadence or the RTOS's appropriate delay-until API to avoid accumulating processing time into the period.

A queue transfers fixed-size items or references according to its API. If you queue a pointer to a stack buffer and return, the consumer can use invalid data. If a buffer pool owns payloads, specify how ownership returns on normal receive, timeout, cancellation and shutdown. A queue's maximum depth is also a timing choice: large queues can hide stale data. Decide whether to block, drop oldest, drop newest or enter a fault state under overload.

Priority inversion occurs when a high-priority task waits on a resource held by a lower-priority task that is itself delayed by other work. FreeRTOS mutexes provide a simplified priority inheritance mechanism, and their behavior with multiple held mutexes is deliberately limited. Mutexes are task-context objects, not objects an ISR can wait on. Use the port's appropriate FromISR APIs and obey its interrupt-priority rules. [FREERTOS-MUTEX]

A schedulability argument needs execution times, periods/deadlines, blocking and interrupt costs. Utilization alone is not a proof for arbitrary tasks. Begin by measuring task execution and queue waiting under load on the MCU. Host-port FreeRTOS execution is useful for task/queue behavior but includes host scheduling and cannot establish the chip's worst-case timing.

The Linux-MCU link should carry a bounded framed protocol with version, sequence and integrity checking. Define boot handshakes, capability negotiation, heartbeats, retries and reboot detection. After either endpoint restarts, stale buffered commands must not be mistaken for current intent. Use a session or explicit reset rule and require a current valid command before enabling actuation. A stop or limit on the MCU must remain effective when Linux is stalled.

Keep firmware updates distinct from normal application messages. Validate compatibility and image integrity, preserve a recovery path and handle interruption. A CRC checks corruption; a signature verifies an authorized signer under a trust model. An update format, bootloader state and reset-vector handoff must agree on the actual MCU.


## Worked lab and expected behavior


Run I05's real FreeRTOS POSIX-port application and host integration tests using its setup instructions. Inspect queue producer/consumer behavior, protocol handling and shutdown. Record RTOS source tag and host compiler. Then change task rates or inject a communication timeout and explain the observed queue policy.

For the physical path, use the selected Nucleo port notes and a logic analyzer to measure ISR-to-task latency and serial timing. These measurements are separate from host tests. If the firmware blocks, inspect task states and queue ownership; increasing every queue size does not diagnose the root cause.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Can an ISR take a mutex? Does priority inheritance prevent deadlock? What happens to stale commands on reboot? Interview bank: RTOS and protocol scenarios.

## Mastery checklist

- State task and queue ownership.
- Explain priority and ISR constraints.
- Bound command age and recovery.
- Separate host logic from MCU timing proof.

## Primary references

[FREERTOS-MUTEX] FreeRTOS mutex documentation. [NVIC] Arm interrupt rules. I05 includes its exact RTOS source and port references.
