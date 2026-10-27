# POSIX I/O, IPC and readiness

## Q051 — Implement write-all with partial progress and a deadline.

**Tags:** EL; foundation; coding practical; coding. **Assesses:** Correct accounting, bounded wait and explicit partial-completion contract.

**Spoken answer:** Keep an offset, advance only after positive writes, retry EINTR and wait for readiness after EAGAIN without resetting the total deadline.

**Deeper explanation/example:** For nonblocking output recompute remaining time from a monotonic deadline. Define zero-progress and peer-close handling. A timeout may occur after partial output, so report bytes sent.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** Retry the whole original buffer after every short write.

**Follow-up:** Can the caller safely retry a partly sent command?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct accounting, bounded wait and explicit partial-completion contract. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q052 — What can a read result mean?

**Tags:** EL; foundation; technical screen; conceptual. **Assesses:** Object-specific return interpretation and no unsigned error conversion.

**Spoken answer:** Positive means that many bytes, zero has object-specific end/no-data semantics, and negative requires checking errno.

**Deeper explanation/example:** For a pipe/socket stream, zero commonly means EOF after buffered data is consumed; terminal VMIN/VTIME modes need separate interpretation. Never cast a negative ssize_t to size_t first.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** Zero always means wait and retry forever.

**Follow-up:** What changes with a datagram socket?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Object-specific return interpretation and no unsigned error conversion. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q053 — Design an absolute timeout for an I/O loop.

**Tags:** EL; foundation; coding practical; coding. **Assesses:** End-to-end deadline preserved despite progress/interruption.

**Spoken answer:** Compute one monotonic deadline and recalculate remaining time after interruption or partial progress.

**Deeper explanation/example:** Round remaining units carefully for poll and cap conversions. When deadline expires stop rather than repeatedly polling with zero. Test repeated EINTR and a peer that trickles one byte at a time.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** Restart the full timeout after each byte.

**Follow-up:** What if a wall clock is adjusted?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: End-to-end deadline preserved despite progress/interruption. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q054 — poll reports readable but read returns EAGAIN. Is that impossible?

**Tags:** EL; foundation; debugging/code review; debugging/scenario. **Assesses:** Correct event interpretation and no busy spin or data loss.

**Spoken answer:** No; readiness can change before the operation or another consumer may take the data. Keep nonblocking handling correct.

**Deeper explanation/example:** Inspect ownership and events, then return to bounded waiting. Treat readiness as a hint about current state, not a reservation of bytes.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** poll guarantees the requested byte count is available.

**Follow-up:** What about POLLHUP with buffered data?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct event interpretation and no busy spin or data loss. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q055 — Implement a bounded line reader over a byte stream.

**Tags:** EL; foundation; coding practical; coding. **Assesses:** Bounded storage, record state and progress on malformed input.

**Spoken answer:** Accumulate into a fixed-capacity buffer, handle fragmented delimiters and define oversize-line discard/recovery.

**Deeper explanation/example:** Return complete lines independently of read boundaries. Specify embedded zero policy and EOF with partial line. Test delimiter split, exact limit and overlong input followed by a valid line.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** Use one fgets/read call and assume a complete record.

**Follow-up:** How do you resynchronize after oversize input?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Bounded storage, record state and progress on malformed input. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q056 — Create a pipe-based parent/child exchange without descriptor leaks.

**Tags:** EL; foundation; coding practical; coding. **Assesses:** Correct descriptor graph and EOF/reaping behavior.

**Spoken answer:** Create the pipe, fork, close unused ends in each process and handle partial I/O and child status.

**Deeper explanation/example:** A remaining write end can prevent reader EOF. Use close-on-exec when appropriate and ensure error paths close every inherited descriptor. Test child exec failure and early close.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** EOF arrives when the intended writer exits regardless of other copies.

**Follow-up:** How would you add a shutdown deadline?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct descriptor graph and EOF/reaping behavior. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q057 — When use shared memory instead of a pipe/socket?

**Tags:** EL; foundation; technical screen; conceptual. **Assesses:** Data transport versus synchronization/recovery distinction.

**Spoken answer:** Use it for a justified copying/throughput need, with explicit synchronization and version/lifetime contracts.

**Deeper explanation/example:** Shared memory is only storage. Define ownership, publication, restart/recovery and how processes agree on layout; pointers from one address space are not generally portable shared references.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** mmap automatically makes updates safe and atomic.

**Follow-up:** How does one process crashing affect the shared state?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Data transport versus synchronization/recovery distinction. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q058 — Your epoll edge-triggered receiver stalls despite unread data. Why?

**Tags:** EL; foundation; debugging/code review; debugging/scenario. **Assesses:** Mode-specific state reasoning and a reproducible burst fixture.

**Spoken answer:** It may have failed to drain nonblocking input until EAGAIN, leaving data without a new edge.

**Deeper explanation/example:** Inspect actual epoll mode and owner; drain correctly while bounding fairness across connections. Level-triggered behavior differs. Reproduce with several records arriving before one event.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** Read exactly one message for each edge.

**Follow-up:** How would backpressure and fairness change the loop?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Mode-specific state reasoning and a reproducible burst fixture. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q059 — How do stream and datagram sockets affect protocol design?

**Tags:** EL; foundation; technical screen; conceptual. **Assesses:** Correct transport guarantees and application responsibilities.

**Spoken answer:** Streams preserve byte order, not message boundaries; datagrams preserve message units but can be lost/truncated depending on protocol/API.

**Deeper explanation/example:** Framing and partial I/O belong in a stream design; maximum message size and loss/reordering belong in datagram handling. Neither choice removes versioning or trust checks.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** TCP preserves each application write as a packet.

**Follow-up:** How do you detect a truncated datagram?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct transport guarantees and application responsibilities. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q060 — A writer dies with SIGPIPE when its reader closes. How handle it?

**Tags:** EL; foundation; debugging/code review; debugging/scenario. **Assesses:** Peer-close behavior and scope of chosen mechanism.

**Spoken answer:** Choose an explicit signal/socket policy and handle the corresponding EPIPE error rather than assuming peer availability.

**Deeper explanation/example:** For sockets, supported per-call flags may suppress SIGPIPE; for pipes a process signal policy may be needed. Preserve partial-progress/error semantics and clean up connection state.

**Assumptions/version:** Linux/POSIX; distinguish socket, pipe, regular-file and terminal semantics.

**Common incorrect answer:** Retry writes forever until the reader returns.

**Follow-up:** What if another thread changes the process-wide signal disposition?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Peer-close behavior and scope of chosen mechanism. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.
