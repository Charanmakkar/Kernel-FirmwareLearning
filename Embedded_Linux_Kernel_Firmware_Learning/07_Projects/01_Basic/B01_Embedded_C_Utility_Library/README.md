# B01 — Embedded C utility library

**Reference implementation delivered. See evidence/ for actual verification status.** Basic, 12 estimated hours after M01. Shared EL/KD/FW foundation; reference requirements S01–S03 and S05. This project solves bounded byte buffering and packet validation for a small device link. It uses no heap allocation, no OS, and no target MMIO. Hardware, target deployment, and Linux kernel behavior are outside this project's acceptance scope.

## Outcomes and interfaces

Implement a FIFO (first in, first out) ring using caller-owned storage, preserve output on errors, reject malformed frames, update bit fields without disturbing other bits, and guard size multiplication. Explain each invariant and test it independently. Operations push/pop are O(1); CRC and codec are O(n), with n bounded by 72 bytes. The ring uses all capacity slots and stores a count; it deliberately uses no power-of-two restriction or lock-free concurrency claims.

```text
bytes --> [complete frame supplied by caller] --> length/magic/version checks
  --> CRC check --> owned eu_packet --> application

caller-owned storage <--> eu_ring {head, tail, count} <--> bytes
           one execution context or one external lock across all calls
```

Wire contract: `A5 5A 01 TYPE LEN_H LEN_L PAYLOAD CRC_H CRC_L`. Version is 1; type is any byte; length is 0–64 bytes; CRC covers the six-byte header plus payload. CRC-16/IBM-3740 uses polynomial 0x1021, initial state 0xFFFF, no reflection and no final XOR. Check vector ASCII `123456789` is 0x29B1. Network order is explicit. An extra trailing byte is rejected rather than silently consumed. CRC detects accidental corruption; it authenticates nothing. A sender can forge both payload and CRC.

The decoder requires exactly one complete frame. B03 will add stream accumulation, fragmentation, timeouts and bounded resynchronization. Keeping those concerns separate makes the frame parser independently testable. No stream behavior is claimed here.

## Build and run

From this project directory on Windows PowerShell, with Python and Clang on PATH:

```powershell
python scripts/verify.py --cc clang
python scripts/verify.py --cc clang --sanitize
```

On Linux:

```sh
python3 scripts/verify.py --cc cc
python3 scripts/verify.py --cc clang --sanitize
# Optional GNU Make path:
make test
```

Each run records commands, exact compiler version, source hashes, return codes and captured output. A sanitizer runtime may be unavailable on a particular host. A failed sanitizer compile/run is recorded as failed; the normal build passing does not substitute for it. The executable named gcc on the observed Windows host is a Clang alias; testing both names is not independent GCC coverage.

Expected behavior by contract: the test program prints PASS with its actual assertion count, then the demo prints `type=7 payload=3 frame=11`. Do not copy that line into evidence as if run. The runner compares actual demo output and saves actual results. Evidence JSON, not this illustrative expectation, establishes status.

## Guided build/debug sequence

1. Read include/embedded_util.h before implementation. Identify caller and callee ownership for every pointer. Invalid pointer *addresses* cannot be made safe by null checks; valid live backing objects remain preconditions.
2. Draw capacity=3 states for push A, push B, pop A, push C, push D, failed push E. Verify head/tail/count after each transition. A failed push or pop must not change queue state or output.
3. Run the tests. Trace `eu_ring_pop` with a debugger; stop when count=0 and inspect the unchanged output byte.
4. Encode the demo packet and inspect the header. Corrupt a payload byte and observe EU_CRC. Change the declared length and observe EU_LENGTH before any payload copy.
5. Attempt exercises/EXERCISES.md independently before opening its separate solution.

## Acceptance defined before validation

| ID | Criterion | Test evidence |
|---|---|---|
| B01-T1 | Strict warning build succeeds; demo output matches contract | runner compile commands and actual stdout |
| B01-T2 | Correct FIFO order for capacities 1–17, full/empty and wrap transitions | 340,000 operations compared to a simple shifting-array model |
| B01-T3 | All payload sizes 0–64 roundtrip; every truncation and one extra byte rejected | tests/test_util.c packet suite |
| B01-T4 | Each single-bit mutation in each valid frame is rejected | mutation loop over every valid payload size |
| B01-T5 | Decoder leaves full output object unchanged on tested errors | byte snapshot comparison in rejects() |
| B01-T6 | 100,000 seeded arbitrary input frames execute within bounded space | randomized loop plus sanitizers where supported |
| B01-T7 | Checked shift/multiply boundary and CRC vector correct | arithmetic suite |
| B01-T8 | Sanitized suite passes on supported runtime | separate sanitize.json, otherwise pending/failed |
| B01-T9 | Learner can change and defend unseen requirements independently | not assessed; cannot be satisfied by supplied code |

Tests use a fixed PRNG seed for reproducibility, not cryptography. Model tests cover useful cases, not proof of all possible executions. CRC equality is not a security acceptance criterion. No performance benchmark or hardware claim is made.

## Failure handling, ownership and limitations

The ring returns EU_FULL instead of overwriting unread bytes; the application decides whether to drop new data, retry or report overload. EU_EMPTY leaves pop output unchanged. No function allocates. Backing storage and ring metadata must remain alive, initialized and unmodified outside this API. Returned count cannot distinguish an invalid ring from an empty one; use only initialized rings and check operation statuses. This educational public struct could be hidden behind an opaque interface for larger applications.

All ring access requires one execution context or external serialization, including count queries. Declaring fields volatile would not fix races. An ISR/task design needs documented target primitives and timing analysis. Packet output owns its payload, avoiding borrowed-pointer lifetime hazards; copying costs at most 64 bytes. Encoder output and written pointer must name valid, suitably sized distinct objects; never point written into the frame buffer. CRC data must be a live readable array for nonzero length; NULL with zero length is allowed.

## Troubleshooting and cleanup

Missing compiler: choose --cc with a compiler executable path as one argument; do not embed flags in the compiler name. Missing ASan runtime: retain failed evidence and retry on a supported Linux toolchain. A warning-as-error failure should be understood, not disabled blindly. Failed FIFO model comparison: print operation index/capacity/state and reduce the sequence. Incorrect CRC: check every CRC parameter and covered bytes, not just the polynomial.

Generated executables live under build/. To clean on Windows, remove the two known build subdirectories using your file manager after confirming this project path. On Linux `make clean` removes only its two named outputs. Source and evidence files are retained.

## Demonstration and interview defense

Five-minute demo: state the wire/error/ownership contract; run verification; show a wraparound example; explain one rejected frame and the separate evidence status; describe what changes for threads, UART streams and an MCU ISR. Questions: why count instead of a reserved slot; why not cast bytes to a packed struct; why CRC is not authentication; why the parser commits output last; which errors sanitizers miss; where source-controlled invariants end and caller preconditions begin.

Portfolio wording before independent work: “Studied and executed a supplied bounded C reference library.” After an independent extension and documented tests, describe your actual contribution and measured results. Never claim authorship of the supplied implementation.

References: R01 C language draft (object/shift/conversion rules), R05 conceptual ring alternatives, R07/R08 sanitizer capabilities. All implementation code is original educational code in this package, not copied kernel code.
