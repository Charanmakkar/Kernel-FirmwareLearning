# Role mock marking guide

For MOCK L use Q052, Q059 and Q071 criteria, coding_reference.c parse_u32, posix_reference.c and DBG03/DBG02 keys. Expect explicit blocking-helper limits, signed syscall checking, suffix progress, shutdown wakeups and a current-evidence boundary. Ask a follow-up that changes the descriptor to nonblocking; a candidate must not retain the same retry loop without a readiness/deadline design.

For MOCK K expect a short protected state transfer or a suitable mutex strategy, user copies in an allowed context, defined partial-copy/consumption semantics, and state lifetime beyond unbind. There is no universal single implementation for the proposed FIFO, so require consistency between its contract and code. Probe deferral must be tied to a supplier rather than every error. The synthetic KASAN report supports a lifetime hypothesis, not a proven line-number root cause. Use Q123, Q125, Q129 and DBG04.

For MOCK F use control_step, seq_newer and DBG05 keys. Sequence freshness needs a half-range and session/reboot contract. ARM does not clear FAULT; CLEAR returns to DISARMED. A heartbeat is useful progress, not merely periodic execution. Stack estimates and host tests do not establish target worst-case timing. Ask what happens if the MCU resets while Linux keeps transmitting an old session.

Across roles, award communication for stating assumptions, defining interfaces and explaining tradeoffs. Do not reward unnecessary jargon. A candidate may consult permitted documentation and still earn full points if the reasoning and validation are their own. Apply the critical gates even when the total would otherwise pass. Retain the original score, remediation and retake evidence separately.
