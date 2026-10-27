# Concise revision sheets

Use these prompts for retrieval, then check the linked module and source references. Explain an example aloud; merely recognizing the words is insufficient.

## C and ownership

Name the owner, capacity, valid length and lifetime of each pointer. Array-to-pointer conversion loses size information. Check allocation multiplication before allocating. Unsigned wrap can violate an application contract; signed overflow can invalidate language-level reasoning. `const` restricts modification through a particular access path; `volatile` supplies neither thread synchronization nor general atomicity. See [M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md) and Q001–Q040.

## Linux I/O and concurrency

Separate progress, EOF, timeout, interruption and failure. A readiness event is not a message boundary. Use a monotonic deadline and recompute remaining time after interruption. Trace every descriptor through creation, duplication, exec and cleanup. Protect queue invariants with the same synchronization; wait in a predicate loop, publish shutdown and wake relevant waiters. A notification does not own the data. See M06–M07 and Q051–Q100.

## Kernel and platform

Before choosing a helper, identify context, sleepability, lock rules and lifetime. User-copy helpers can fault and report residual bytes; their wrapper's return contract may differ. Managed resources do not automatically preserve state referenced by open files. Device tree describes hardware under binding rules. A matching object build does not prove loadability, correct teardown or physical behavior. See M08–M11 and Q101–Q140.

## Firmware and RTOS

Explain reset vectors, stack placement, initialized-data copying and zeroing. Know the actual device's interrupt-priority convention. Bound ISR work and use the correct ISR-safe API. Queueing a pointer requires a payload ownership rule. Priority inheritance does not prevent deadlock. Feed a watchdog on meaningful application progress. Distinguish measured latency from a proven bound. See M12–M13 and Q141–Q170.

## Images updates and evidence

Separate recipe, layer, image, machine and distribution policy. Pin source inputs and preserve configuration. Atomic replacement and durable persistence need an explicit storage failure model. Signing, secure boot, health acceptance and downgrade protection solve different parts of the trust/recovery problem. Report authored, compiled, host-tested, emulated and hardware-tested separately. See M14–M17 and Q171–Q200.
