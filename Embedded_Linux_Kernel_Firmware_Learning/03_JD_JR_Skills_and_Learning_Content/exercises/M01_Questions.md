# M01 independent exercise and exit test

Prerequisites: M01 guided lab. Duration 60 minutes. Allowed: editor, compiler, local C documentation, debugger; no AI and no reference solution. Deliver a .c/.h pair, tests, actual compiler output and a 200-word explanation. Test data is below; add your own edge cases.

E-M01: implement `bool read_be16(const uint8_t *data, size_t size, size_t offset, uint16_t *out)` with an unchanged output on failure. A valid live data array and distinct live output object are caller preconditions. Null, insufficient bytes and huge offsets must return false; avoid `offset+2` overflow. Data `{0x12,0x34,0xab,0xcd}` at offsets 0 and 2 yields 0x1234 and 0xabcd. Offsets 3, 4 and SIZE_MAX fail; size 0 fails; null arguments fail. No unaligned casts or host-endian assumptions.

Explain: why `if (offset + 2 <= size)` can fail; why the out pointer cannot be “validated” by a null test alone; why no malloc is necessary; why a volatile output pointer would not add synchronization.

Score: correct byte result 25, all boundary/error semantics 25, portable types and lifetime reasoning 20, meaningful tests/evidence 20, explanation 10. Pass >=80 with no invalid access, overflow-based bounds defect or fabricated result. Failure remediation: draw the valid index interval, rewrite using subtraction after offset validation, add a regression for SIZE_MAX and retake on a 32-bit-byte-field decoder with a different input.
