# B01 Embedded C utility library

Build a small library that can be reused by a serial tool and MCU application. Its minimum implementation contains a bounded byte ring, checked bit updates, a CRC function, and a binary frame encoder/decoder. All storage is caller owned; there are no hidden heap allocations. Plan 8–12 hours after modules M02 and M03. This project supports the common C foundation of all three career tracks.

## Outcomes and acceptance

Explain the invariant `0 <= count <= capacity`, preserve FIFO order across wraparound, reject bit positions outside 0–31, and parse a stream fragment without reading beyond its length. Demonstrate every payload size from zero to 128 bytes, every truncation point of each valid packet, bad CRCs, oversized declarations, and at least one known CRC test vector. Pass `make test` and the supported sanitizer configuration. A correct return value alone is insufficient if an invalid input changes memory outside the output object.

## Environment and files

Use a Linux host, GCC with C11 support, Make, and a terminal. The recorded build uses GCC 13.3.0 on x86_64. No board or wiring is required. The source also avoids Linux-specific interfaces, making it suitable for later MCU reuse after target compilation and timing checks. [VERSIONS.md](VERSIONS.md) records the actual environment.

`include/util.h` is the API contract; `src/util.c` is the complete reference implementation; `tests/test_util.c` exercises boundaries and malformed input. Read [exercises/EXERCISES.md](exercises/EXERCISES.md) before [solutions/SOLUTIONS.md](solutions/SOLUTIONS.md). `evidence/` contains validation records. There is no hardware directory because this is a portable library.

## Design and protocol

The ring stores a separate count so all allocated slots can be used. Both indices wrap modulo capacity. Full insertion and empty removal return false without changing state. Objects must be initialized successfully before other ring functions; callers must not modify their fields independently. A ring instance has one owner or requires an external lock.

The wire format is `A5 5A | version u8 | type u8 | length be16 | sequence be16 | payload | CRC be16`. Version is 1; length is payload length, at most 128. The CRC uses polynomial 0x1021, initial value 0xFFFF, no reflection, no final XOR, and covers bytes beginning with version through the payload. For `123456789`, it yields 0x29B1. This is a teaching protocol specification, not a claim of compatibility with an existing industrial protocol.

The decoder returns MORE for an incomplete candidate, INVALID with one byte consumed for resynchronization, or OK with the full frame length. It writes a completed output only after structural and CRC checks. Network order is decoded byte by byte; the implementation never casts unaligned packet memory to a C structure. CRC detects accidental errors and provides no authentication.

## Guided build and debugging lab

Run from this project directory:

```sh
make test
make sanitize
gdb ./build/test_util
```

In GDB, set `break ring_push`, run, inspect `r->count`, and step through the full-buffer rejection. Set a conditional breakpoint at `frame_decode` when `n == 8` and follow the oversized-length test. Expected test output begins with `PASS` and names the checked cases; the exact executed output is preserved in `evidence/host_tests.log`.

If LeakSanitizer cannot inspect processes in a restricted container, use `ASAN_OPTIONS=detect_leaks=0 make sanitize` and record that leak detection was disabled. That command was the successful recorded configuration here. Address and undefined-behavior instrumentation remained enabled. The code allocates no heap memory, but this does not make leak detection generally unnecessary in later projects.

Before adding features, explain why replacing the count with `write_at == read_at` creates ambiguity between empty and full. Change one loop boundary locally, show the failing test, and restore it. `make clean` removes only this project's build directory.

## Troubleshooting and limitations

A CRC mismatch often comes from including sync bytes, using little-endian CRC storage, or applying reflection accidentally. An off-by-one bug at length 128 should be investigated with the byte count `8 + payload + 2`. Sanitizers cannot prove correct synchronization or correct hardware register behavior. This library deliberately supplies no lock-free guarantee, allocator, retransmission, or cryptographic protection.

## Demonstration and interview defense

Demonstrate a passing boundary test, a rejected corrupted frame, and successful recovery by the B03 stream receiver. Explain why unsigned shifts need range checks, why C structure padding is unsuitable for a wire format, and who owns each buffer. A truthful portfolio statement is: “Implemented and host-tested a bounded C codec and ring buffer with malformed-input and sanitizer checks.” Add specific counts only from retained evidence.

## Primary references

- [GCC warning options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html)
- [GCC instrumentation options](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)

Access date: 27 October 2026. The protocol layout and acceptance tests are original teaching design choices.
