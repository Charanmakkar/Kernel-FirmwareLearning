# M03 Data structures and defensive protocols

## Objectives and prerequisites

Prerequisites: M02.

Implement a bounded ring buffer and state machine, define a binary wire format and recover from corrupted or incomplete input.

## Lesson


A ring buffer reuses a fixed storage array. Choose an invariant before coding: either store a count, reserve one slot, or use monotonic counters whose wrap arithmetic is explicitly bounded. A count-based single-threaded design maintains 0 <= count <= capacity. Push writes at the tail only when count < capacity; pop reads at the head only when count > 0. Each operation is constant time. A concurrent ring needs an additional synchronization design; the data structure alone is not thread-safe.

Prefer a small state machine when input arrives over time. A parser can search for a prefix, collect a header, validate a length, collect a payload, and verify integrity. State transitions must define what happens on an invalid byte, a timeout and reset. The receiving transport may split one frame across many reads or combine many frames into one read. A packet boundary in your application is not a UART or TCP read boundary.

Specify the protocol before implementing it: framing, version, message type, sequence, bounded payload length, byte order, integrity algorithm and the exact bytes covered by the integrity check. A cyclic redundancy check detects accidental corruption; it does not authenticate the sender. If replay or malicious commands matter, add an appropriate authenticated channel or message authentication and a key-management design.

An API should distinguish incomplete input from invalid input. Both may consume bytes, but their recovery rules differ. Reject a length before allocating or indexing. Resynchronize deliberately after a bad checksum so the next valid frame can be found. Counters for invalid length, integrity failure, unsupported version and timeout turn field failures into observable behavior.

For a command such as set-speed, make retries idempotent or include a sequence/transaction identifier. An acknowledgement states what was accepted, not necessarily what was physically achieved. Add a timestamp or age limit where stale commands are unsafe. Receiver-side limits remain active when the upstream process stalls. These are original protocol design choices for the exercises; they must be validated against the actual product requirements.


## Worked lab and expected behavior


Build and test B01 and B03. Inspect the protocol specification in B03 rather than assuming its field order from this lesson. Use its pseudo-terminal test to send a valid frame one byte at a time, then a corrupt frame followed by a valid frame. Acceptance requires the valid frame to survive fragmentation, corruption to be rejected and synchronization to recover without a process restart.

For a count-based ring with capacity 3, push 10, 20, 30; reject 40; pop 10 and 20; push 40 and 50; then pop 30, 40, 50. This concrete sequence exercises wraparound and a full/empty distinction. If the final order differs, inspect the update order of head, tail and count. If a parser hangs after corrupt input, log state transitions and consumed-byte counts, not only the final error.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Why is a checksum insufficient for security? How do you distinguish duplicate commands from retransmissions? What makes your ring full? Interview bank: coding, protocol debugging and system design.

## Mastery checklist

- State ring invariants before implementation.
- Test every split position of a frame.
- Recover after corruption.
- Bound memory, retries and waiting.

## Primary references

[READ] Linux read semantics. [WRITE] Linux write semantics. B01 and B03 contain original protocol contracts and tests.
