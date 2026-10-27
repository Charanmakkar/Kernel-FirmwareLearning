# Diagnostic answer key

D01: the array's automatic lifetime ends on return. A caller-owned buffer with capacity or explicit heap ownership is valid; immutable static storage has shared lifetime and reentrancy limitations. Award 3 lifetime, 3 alternatives, 2 tradeoffs.

D02: under C11, signed overflow is undefined; unsigned addition wraps modulo the range; conflicting unsequenced increments are undefined. No universal output exists for UB. Award 2 each classification and 2 explicit version/assumption.

D03: reject null; if `b != 0 && a > SIZE_MAX/b`, fail before multiplication; otherwise store the product. The first two pairs succeed, the third fails, null fails. Award 5 precheck, 2 zero, 2 unchanged failure, 3 tests. See `coding_reference.c` checked_mul. Out-of-bounds or overflow-based validation fails the critical gate.

D04: one valid sequence is `mktemp -d`, create files under that path, `ls -l`, `command 2>errors.txt`, `rg 'ERROR' file`, then initialize and commit in that disposable directory. Verify actual output; do not award execution points for a copied transcript. Award 2 permissions, 2 redirection, 2 search, 2 Git evidence. Configure a local temporary Git identity only as needed, without modifying global settings.

D05: streams lack application message boundaries. Positive write results advance offset; EINTR retries under API semantics; EAGAIN waits for readiness in nonblocking mode; read zero indicates EOF for ordinary streams. Award 3 stream model, 3 progress, 2 errors.

D06: hold the mutex; loop while empty and not stopping; wait atomically releases/reacquires; on stop follow drain/discard policy; otherwise consume under the lock. Wake all necessary waiters on shutdown and join before destruction. Award 3 loop, 3 predicate/lock, 2 shutdown, 2 lifetime.

D07: ROM/firmware/bootloader/kernel/init is representative, not universal. MCU startup initializes a bare-metal or RTOS runtime; an application processor commonly provides MMU and Linux support. Award 3 stages, 3 platform distinction, 2 board qualification.

D08: these potentially sleeping operations are inappropriate in a conventional hard-IRQ context. Capture/acknowledge bounded state and use a documented threaded handler or workqueue where appropriate. PREEMPT_RT requires configuration-aware reasoning. Award 3 context, 3 deferred design, 2 caveat.

D09: define buffer states FREE, FILLING, READY, CONSUMING, with a single owner at each transition; use an ISR-safe notification and queue or descriptor ring, and do not rearm a consumed buffer until returned. DMA cache synchronization and interrupt priority restrictions remain target-specific. Award 4 ownership, 2 notification, 2 hardware qualification.

D10: repeated POLLHUP and read zero support an unhandled EOF/hangup spin. They do not prove the remote electrical cause. Transition out of the active read loop, drain correctly, and reconnect with a bounded policy. Award 3 evidence, 2 restraint, 3 test/fix.

D11: CRC is accidental-error detection, signatures authenticate under a trust policy, verified boot checks startup components in a trust chain. None alone guarantees availability, physical safety, or every runtime state. Award 4 distinctions, 3 limits.

D12: award 2 concrete requirement and role, 2 supported result, 2 failure/lesson, 1 limitation. Fabrication fails the truthfulness gate. A small truthful practice example can receive full credit.
