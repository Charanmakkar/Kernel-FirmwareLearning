# Design review

Storage duration belongs to the caller; the ring never frees memory. The metadata count distinguishes head==tail empty from head==tail full. Index advance uses increment and comparison, avoiding a division and accepting arbitrary positive capacities. Although structural validation catches null/obvious range errors, it cannot detect dangling pointers, a false backing size or all forged metadata. Those are caller preconditions, not solved by defensive checks.

Each parser check precedes the access it justifies. The fixed maximum means adding eight to a validated payload length cannot overflow size_t on supported hosts. Byte assembly avoids alignment and effective-type violations; no struct layout is part of the wire ABI. Decoder output changes exactly once after validation, making rollback on errors unnecessary. Encoding through a temporary byte array avoids reading packet fields after output writes begin. CRC calculations use bounded unsigned arithmetic with an explicitly masked 16-bit state.

The test model uses a shifting array rather than copying the ring algorithm. The mutation suite tests the integrity boundary. Arbitrary-input stress exercises invalid headers/lengths; it is complemented by valid-frame mutations because random bytes rarely form valid frames. No input test proves absence of concurrency defects: concurrency is explicitly excluded.
