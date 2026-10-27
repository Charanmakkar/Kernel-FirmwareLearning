# Framed transaction specification

| Offset | Field | Encoding |
|---|---|---|
| 0 | Sync | 0xA5 |
| 1 | Sync | 0x5A |
| 2 | Version | 1 |
| 3 | Type | 1 request and 2 response |
| 4 to 5 | Payload length | Big-endian unsigned 16-bit value 0 through 128 |
| 6 to 7 | Sequence | Big-endian unsigned 16-bit; minimum client uses 1 |
| 8 onward | Payload | Length bytes; binary codec, command-line frontend accepts text |
| 8 plus length | CRC high byte then low byte | CRC-16 polynomial 0x1021 initial 0xFFFF non-reflected no final XOR |

CRC coverage starts at version and ends after the final payload byte. Total frame length is payload length plus ten. A corrupted header is handled by scanning one byte forward. A maximum-size false header can delay resynchronization until its bounded candidate is complete or the absolute transaction deadline expires; it cannot allocate unbounded memory. Complete responses with a different sequence are consumed and ignored. This one-shot reference uses sequence 1 again on each invocation, so an old response with sequence 1 arriving during a later invocation cannot be distinguished from a new reply. The minimum protocol does not claim cross-invocation freshness. A production protocol needs an explicit session/nonce or equivalent freshness contract; a persistent client must also manage wraparound and stale replay.

State transitions: open and configure; write all request bytes before deadline; accumulate response; reject corrupt or unmatched frames; accept matching frame; restore settings and close. Every error takes the same cleanup path. Tests use an independently implemented Python codec so encoder and decoder errors are less likely to cancel each other silently.
