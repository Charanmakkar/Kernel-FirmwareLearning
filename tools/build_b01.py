from build_program import ROOT, write

P = '07_Projects/01_Basic/B01_Embedded_C_Utility_Library/'

write(P+'include/embedded_util.h', r'''
#ifndef EMBEDDED_UTIL_H
#define EMBEDDED_UTIL_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef enum {
    EU_OK = 0, EU_INVALID, EU_FULL, EU_EMPTY,
    EU_LENGTH, EU_MAGIC, EU_VERSION, EU_CRC
} eu_status;

/* Caller owns storage for the entire ring lifetime. No concurrent access.
 * Do not modify these fields after init except through this API. */
typedef struct {
    uint8_t *storage;
    size_t capacity, head, tail, count;
} eu_ring;

eu_status eu_ring_init(eu_ring *r, uint8_t *storage, size_t capacity);
eu_status eu_ring_push(eu_ring *r, uint8_t value);
/* out must not overlap ring metadata or its backing storage. */
eu_status eu_ring_pop(eu_ring *r, uint8_t *out);
size_t eu_ring_count(const eu_ring *r);

uint32_t eu_bits_update32(uint32_t old, uint32_t mask, uint32_t value);
bool eu_bit32(unsigned position, uint32_t *out);
bool eu_size_mul(size_t a, size_t b, size_t *out);

#define EU_PAYLOAD_MAX 64u
#define EU_FRAME_MAX (EU_PAYLOAD_MAX + 8u)
typedef struct {
    uint8_t type;
    uint16_t length;
    uint8_t payload[EU_PAYLOAD_MAX];
} eu_packet;

/* CRC-16/IBM-3740 (also called CCITT-FALSE): init FFFF, poly 1021,
 * non-reflected, xorout 0000. data may be NULL only when length is zero. */
uint16_t eu_crc16(const uint8_t *data, size_t length);
/* Exact one-frame codec, not a stream reassembler. Output remains unchanged
 * on error. Byte layout: A5 5A 01 type len_be16 payload crc_be16.
 * CRC covers header and payload, excluding the two CRC bytes. */
eu_status eu_packet_decode(const uint8_t *wire, size_t length, eu_packet *out);
eu_status eu_packet_encode(const eu_packet *packet, uint8_t *wire,
                           size_t capacity, size_t *written);
#endif
''')

write(P+'src/embedded_util.c', r'''
#include "embedded_util.h"
#include <limits.h>
#include <string.h>

_Static_assert(CHAR_BIT == 8, "protocol requires 8-bit bytes");

static bool ring_valid(const eu_ring *r)
{
    return r != NULL && r->storage != NULL && r->capacity != 0u &&
           r->head < r->capacity && r->tail < r->capacity &&
           r->count <= r->capacity;
}

static size_t advance(size_t i, size_t capacity)
{
    ++i;
    return i == capacity ? 0u : i;
}

eu_status eu_ring_init(eu_ring *r, uint8_t *storage, size_t capacity)
{
    if (r == NULL || storage == NULL || capacity == 0u)
        return EU_INVALID;
    *r = (eu_ring){storage, capacity, 0u, 0u, 0u};
    return EU_OK;
}

eu_status eu_ring_push(eu_ring *r, uint8_t value)
{
    if (!ring_valid(r))
        return EU_INVALID;
    if (r->count == r->capacity)
        return EU_FULL;
    r->storage[r->head] = value;
    r->head = advance(r->head, r->capacity);
    ++r->count;
    return EU_OK;
}

eu_status eu_ring_pop(eu_ring *r, uint8_t *out)
{
    if (!ring_valid(r) || out == NULL)
        return EU_INVALID;
    if (r->count == 0u)
        return EU_EMPTY;
    *out = r->storage[r->tail];
    r->tail = advance(r->tail, r->capacity);
    --r->count;
    return EU_OK;
}

size_t eu_ring_count(const eu_ring *r)
{
    return ring_valid(r) ? r->count : 0u;
}

uint32_t eu_bits_update32(uint32_t old, uint32_t mask, uint32_t value)
{
    return (old & ~mask) | (value & mask);
}

bool eu_bit32(unsigned position, uint32_t *out)
{
    if (out == NULL || position >= 32u)
        return false;
    *out = UINT32_C(1) << position;
    return true;
}

bool eu_size_mul(size_t a, size_t b, size_t *out)
{
    if (out == NULL || (b != 0u && a > SIZE_MAX / b))
        return false;
    *out = a * b;
    return true;
}

uint16_t eu_crc16(const uint8_t *data, size_t length)
{
    uint32_t crc = UINT32_C(0xffff);
    /* Pointer validity is a caller precondition for nonzero length. */
    for (size_t i = 0u; i < length; ++i) {
        crc ^= (uint32_t)data[i] << 8u;
        for (unsigned j = 0u; j < 8u; ++j)
            crc = ((crc & UINT32_C(0x8000)) != 0u)
                ? ((crc << 1u) ^ UINT32_C(0x1021)) & UINT32_C(0xffff)
                : (crc << 1u) & UINT32_C(0xffff);
    }
    return (uint16_t)crc;
}

eu_status eu_packet_decode(const uint8_t *wire, size_t length, eu_packet *out)
{
    if (wire == NULL || out == NULL)
        return EU_INVALID;
    if (length < 8u || length > EU_FRAME_MAX)
        return EU_LENGTH;
    if (wire[0] != 0xa5u || wire[1] != 0x5au)
        return EU_MAGIC;
    if (wire[2] != 1u)
        return EU_VERSION;
    const size_t payload_length = ((size_t)wire[4] << 8u) | wire[5];
    if (payload_length > EU_PAYLOAD_MAX || length != payload_length + 8u)
        return EU_LENGTH;
    const uint16_t received_crc = (uint16_t)(((uint32_t)wire[length - 2u] << 8u)
                                            | wire[length - 1u]);
    if (eu_crc16(wire, length - 2u) != received_crc)
        return EU_CRC;
    eu_packet parsed = {0};
    parsed.type = wire[3];
    parsed.length = (uint16_t)payload_length;
    memcpy(parsed.payload, wire + 6u, payload_length);
    *out = parsed;
    return EU_OK;
}

eu_status eu_packet_encode(const eu_packet *packet, uint8_t *wire,
                           size_t capacity, size_t *written)
{
    if (packet == NULL || wire == NULL || written == NULL)
        return EU_INVALID;
    if (packet->length > EU_PAYLOAD_MAX)
        return EU_LENGTH;
    const size_t total = (size_t)packet->length + 8u;
    if (capacity < total)
        return EU_LENGTH;
    uint8_t temp[EU_FRAME_MAX] = {0xa5u, 0x5au, 1u, 0u, 0u, 0u};
    temp[3] = packet->type;
    temp[4] = (uint8_t)(packet->length >> 8u);
    temp[5] = (uint8_t)(packet->length & 0xffu);
    memcpy(temp + 6u, packet->payload, packet->length);
    const uint16_t crc = eu_crc16(temp, total - 2u);
    temp[total - 2u] = (uint8_t)(crc >> 8u);
    temp[total - 1u] = (uint8_t)(crc & 0xffu);
    memcpy(wire, temp, total);
    *written = total;
    return EU_OK;
}
''')

write(P+'src/demo.c', r'''
#include "embedded_util.h"
#include <stdio.h>

int main(void)
{
    eu_packet original = {.type = 7u, .length = 3u, .payload = {10u, 20u, 30u}};
    eu_packet decoded = {0};
    uint8_t wire[EU_FRAME_MAX];
    size_t length = 0u;
    if (eu_packet_encode(&original, wire, sizeof wire, &length) != EU_OK ||
        eu_packet_decode(wire, length, &decoded) != EU_OK)
        return 1;
    printf("type=%u payload=%u frame=%zu\n", (unsigned)decoded.type,
           (unsigned)decoded.length, length);
    return 0;
}
''')

write(P+'tests/test_util.c', r'''
#include "embedded_util.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static size_t checks;
#define CHECK(x) do { ++checks; if (!(x)) { \
    fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #x); exit(1); \
} } while (0)

static uint32_t rng = UINT32_C(0x12345678);
static uint32_t random32(void)
{
    rng ^= rng << 13u;
    rng ^= rng >> 17u;
    rng ^= rng << 5u;
    return rng;
}

static void rings(void)
{
    uint8_t storage[17];
    eu_ring r = {0};
    CHECK(eu_ring_init(NULL, storage, 1u) == EU_INVALID);
    CHECK(eu_ring_init(&r, NULL, 1u) == EU_INVALID);
    CHECK(eu_ring_init(&r, storage, 0u) == EU_INVALID);
    CHECK(eu_ring_push(&r, 0u) == EU_INVALID);
    CHECK(eu_ring_count(NULL) == 0u);
    for (size_t capacity = 1u; capacity <= sizeof storage; ++capacity) {
        uint8_t model[17] = {0};
        size_t count = 0u;
        CHECK(eu_ring_init(&r, storage, capacity) == EU_OK);
        uint8_t out = 0xedu;
        CHECK(eu_ring_pop(&r, &out) == EU_EMPTY && out == 0xedu);
        CHECK(eu_ring_pop(&r, NULL) == EU_INVALID);
        for (size_t n = 0u; n < 20000u; ++n) {
            const uint32_t choice = random32();
            if ((choice & 1u) != 0u) {
                const uint8_t value = (uint8_t)(choice >> 8u);
                const eu_status status = eu_ring_push(&r, value);
                if (count == capacity) {
                    CHECK(status == EU_FULL);
                } else {
                    CHECK(status == EU_OK);
                    model[count++] = value;
                }
            } else {
                out = 0xedu;
                const eu_status status = eu_ring_pop(&r, &out);
                if (count == 0u) {
                    CHECK(status == EU_EMPTY && out == 0xedu);
                } else {
                    CHECK(status == EU_OK && out == model[0]);
                    --count;
                    memmove(model, model + 1u, count);
                }
            }
            CHECK(eu_ring_count(&r) == count);
            CHECK(r.head < capacity && r.tail < capacity);
        }
        while (count != 0u) {
            CHECK(eu_ring_pop(&r, &out) == EU_OK && out == model[0]);
            --count;
            memmove(model, model + 1u, count);
        }
    }
}

static void arithmetic(void)
{
    uint32_t out = 99u;
    CHECK(eu_bit32(31u, &out) && out == UINT32_C(0x80000000));
    CHECK(!eu_bit32(32u, &out) && out == UINT32_C(0x80000000));
    CHECK(!eu_bit32(0u, NULL));
    CHECK(eu_bits_update32(0xaau, 0x0fu, 0xf5u) == 0xa5u);
    CHECK(eu_bits_update32(UINT32_MAX, 0u, 0u) == UINT32_MAX);
    CHECK(eu_bits_update32(0u, UINT32_MAX, 23u) == 23u);
    size_t bytes = 42u;
    CHECK(eu_size_mul(SIZE_MAX, 1u, &bytes) && bytes == SIZE_MAX);
    CHECK(!eu_size_mul(SIZE_MAX, 2u, &bytes) && bytes == SIZE_MAX);
    CHECK(eu_size_mul(SIZE_MAX, 0u, &bytes) && bytes == 0u);
    CHECK(!eu_size_mul(1u, 1u, NULL));
    CHECK(eu_crc16((const uint8_t *)"123456789", 9u) == 0x29b1u);
    CHECK(eu_crc16(NULL, 0u) == 0xffffu);
}

static void rejects(const uint8_t *wire, size_t length, eu_status expected)
{
    eu_packet out;
    memset(&out, 0xabu, sizeof out);
    unsigned char before[sizeof out];
    memcpy(before, &out, sizeof out);
    CHECK(eu_packet_decode(wire, length, &out) == expected);
    CHECK(memcmp(before, &out, sizeof out) == 0);
}

static void packets(void)
{
    uint8_t wire[EU_FRAME_MAX + 1u] = {0};
    for (size_t length = 0u; length <= EU_PAYLOAD_MAX; ++length) {
        eu_packet in = {.type = 255u, .length = (uint16_t)length};
        for (size_t i = 0u; i < length; ++i)
            in.payload[i] = (uint8_t)i;
        eu_packet out = {0};
        size_t written = 999u;
        CHECK(eu_packet_encode(&in, wire, sizeof wire, &written) == EU_OK);
        CHECK(written == length + 8u);
        CHECK(eu_packet_decode(wire, written, &out) == EU_OK);
        CHECK(out.type == in.type && out.length == in.length);
        CHECK(memcmp(out.payload, in.payload, length) == 0);
        for (size_t n = 0u; n < written; ++n)
            rejects(wire, n, EU_LENGTH);
        rejects(wire, written + 1u, EU_LENGTH);
        /* Every bit flip in this valid frame must fail validation. */
        for (size_t i = 0u; i < written; ++i) {
            for (unsigned bit = 0u; bit < 8u; ++bit) {
                wire[i] ^= (uint8_t)(1u << bit);
                CHECK(eu_packet_decode(wire, written, &out) != EU_OK);
                wire[i] ^= (uint8_t)(1u << bit);
            }
        }
        uint8_t before[sizeof wire];
        memcpy(before, wire, sizeof wire);
        written = 999u;
        CHECK(eu_packet_encode(&in, wire, length + 7u, &written) == EU_LENGTH);
        CHECK(written == 999u && memcmp(before, wire, sizeof wire) == 0);
    }
    eu_packet in = {.type = 1u, .length = 0u};
    size_t written;
    CHECK(eu_packet_encode(&in, wire, sizeof wire, &written) == EU_OK);
    wire[0] = 0u;
    rejects(wire, written, EU_MAGIC);
    wire[0] = 0xa5u;
    wire[2] = 2u;
    rejects(wire, written, EU_VERSION);
    wire[2] = 1u;
    wire[7] ^= 1u;
    rejects(wire, written, EU_CRC);
    rejects(NULL, 0u, EU_INVALID);
    CHECK(eu_packet_decode(wire, written, NULL) == EU_INVALID);
    CHECK(eu_packet_encode(NULL, wire, sizeof wire, &written) == EU_INVALID);
    CHECK(eu_packet_encode(&in, NULL, sizeof wire, &written) == EU_INVALID);
    CHECK(eu_packet_encode(&in, wire, sizeof wire, NULL) == EU_INVALID);
    in.length = 65u;
    CHECK(eu_packet_encode(&in, wire, sizeof wire, &written) == EU_LENGTH);
    /* Arbitrary data across every accepted input length: reject or roundtrip. */
    for (size_t n = 0u; n < 100000u; ++n) {
        const size_t length = (size_t)(random32() % (EU_FRAME_MAX + 1u));
        for (size_t i = 0u; i < length; ++i)
            wire[i] = (uint8_t)random32();
        eu_packet out;
        const eu_status status = eu_packet_decode(wire, length, &out);
        CHECK(status >= EU_OK && status <= EU_CRC);
        if (status == EU_OK) {
            uint8_t again[EU_FRAME_MAX];
            CHECK(eu_packet_encode(&out, again, sizeof again, &written) == EU_OK);
            CHECK(written == length && memcmp(wire, again, length) == 0);
        }
    }
}

int main(void)
{
    rings();
    arithmetic();
    packets();
    printf("PASS: %zu checks; 340000 ring operations; 100000 parser inputs\n", checks);
    return 0;
}
''')

write(P+'scripts/verify.py', r'''
"""Portable compile/test runner. It records actual subprocess results, not estimates."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--cc', default=os.environ.get('CC', 'clang'))
parser.add_argument('--sanitize', action='store_true')
args = parser.parse_args()
build = root / 'build' / ('sanitize' if args.sanitize else 'normal')
build.mkdir(parents=True, exist_ok=True)
record = {'host': platform.platform(), 'python': sys.version, 'sanitizers_requested': args.sanitize,
          'commands': [], 'source_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(root.rglob('*')) if p.is_file() and p.suffix in ['.c', '.h']}}

def run(command):
    proc = subprocess.run(command, cwd=root, capture_output=True, text=True)
    record['commands'].append({'argv': [str(x) for x in command], 'returncode': proc.returncode,
                              'stdout': proc.stdout, 'stderr': proc.stderr})
    if proc.returncode != 0:
        raise RuntimeError('Command failed: ' + ' '.join(str(x) for x in command))
    return proc.stdout

try:
    run([args.cc, '--version'])
    flags = ['-std=c11', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wshadow', '-Werror',
             '-g', '-O1' if args.sanitize else '-O2', '-Iinclude']
    if args.sanitize:
        flags += ['-fsanitize=address,undefined', '-fno-sanitize-recover=all', '-fno-omit-frame-pointer']
    suffix = '.exe' if os.name == 'nt' else ''
    test = build / ('test_util' + suffix)
    demo = build / ('demo' + suffix)
    run([args.cc, *flags, 'src/embedded_util.c', 'tests/test_util.c', '-o', str(test)])
    run([args.cc, *flags, 'src/embedded_util.c', 'src/demo.c', '-o', str(demo)])
    print(run([str(test)]), end='')
    actual = run([str(demo)])
    if actual != 'type=7 payload=3 frame=11\n':
        raise RuntimeError('Demo output differs from contract: ' + repr(actual))
    print(actual, end='')
    record['result'] = 'passed'
except (OSError, RuntimeError) as error:
    record['result'] = 'failed'
    record['error'] = str(error)
finally:
    evidence = root / 'evidence' / ('sanitize.json' if args.sanitize else 'host.json')
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print('Evidence:', evidence)
if record['result'] != 'passed':
    sys.exit(1)
''')

write(P+'Makefile', r'''
CC ?= cc
CFLAGS ?= -std=c11 -O2 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror
CPPFLAGS += -Iinclude
.PHONY: all test clean
all: build/test_util build/demo
build:
	mkdir -p build
build/test_util: src/embedded_util.c tests/test_util.c include/embedded_util.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) src/embedded_util.c tests/test_util.c -o $@
build/demo: src/embedded_util.c src/demo.c include/embedded_util.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) src/embedded_util.c src/demo.c -o $@
test: all
	./build/test_util
	./build/demo
clean:
	rm -f build/test_util build/demo
''')

write(P+'README.md', r'''
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
''')

write(P+'VERSIONS.md', r'''
# B01 versions

Source contract: ISO C11 with CHAR_BIT=8, uint8_t/uint16_t/uint32_t and size_t. Host-independent logic; x86-64 Windows is the only initially observed execution host. Python runner requires Python 3.9+; executed host version recorded in evidence. Observed compiler: LLVM-MinGW Clang 22.1.0-rc3, target x86_64-w64-windows-gnu, toolchain path recorded in JSON. GCC coverage, Linux execution, emulator and MCU execution remain separate pending checks unless later evidence is added.

No kernel, linker script, board wiring, peripheral or external package dependency applies. include/, src/, tests/, scripts/, docs/, exercises/ and evidence/ are present. config/ and hardware/ are omitted because B01 has neither OS configuration nor physical hardware. build/ is generated output and excluded from the distributable ZIP.
''')

write(P+'docs/REVIEW.md', r'''
# Design review

Storage duration belongs to the caller; the ring never frees memory. The metadata count distinguishes head==tail empty from head==tail full. Index advance uses increment and comparison, avoiding a division and accepting arbitrary positive capacities. Although structural validation catches null/obvious range errors, it cannot detect dangling pointers, a false backing size or all forged metadata. Those are caller preconditions, not solved by defensive checks.

Each parser check precedes the access it justifies. The fixed maximum means adding eight to a validated payload length cannot overflow size_t on supported hosts. Byte assembly avoids alignment and effective-type violations; no struct layout is part of the wire ABI. Decoder output changes exactly once after validation, making rollback on errors unnecessary. Encoding through a temporary byte array avoids reading packet fields after output writes begin. CRC calculations use bounded unsigned arithmetic with an explicitly masked 16-bit state.

The test model uses a shifting array rather than copying the ring algorithm. The mutation suite tests the integrity boundary. Arbitrary-input stress exercises invalid headers/lengths; it is complemented by valid-frame mutations because random bytes rarely form valid frames. No input test proves absence of concurrency defects: concurrency is explicitly excluded.
''')

write(P+'exercises/EXERCISES.md', r'''
# B01 independent exercises — answers separate

Prerequisites M01 and a normal verification pass. Allow 60 minutes, editor/compiler/debugger and API header; no AI or reference implementation. Work in a copy/branch. Deliver source diff, tests and a short invariant explanation. Score behavior 40, boundary tests 25, resource/alias reasoning 20, communication 15; pass >=80 and no unsafe access.

E01: add `eu_ring_peek(const eu_ring *r, uint8_t *out)` that returns the oldest byte without removing it. Invalid arguments yield EU_INVALID; empty yields EU_EMPTY; out and ring remain unchanged on failure. Test capacity one, wrapped state and empty. Do not solve by popping then pushing.

E02: add `eu_packet_payload_sum(const eu_packet *packet, uint32_t *out)` with explicit length checking and unchanged output on failure. Payload bytes sum as unsigned values; no CRC recomputation. Test zero bytes, all 64 bytes equal 255, length 65, and null parameters.

E03 debugging: change the ring full test to `count == capacity - 1`. Predict the affected capacity-one behavior before execution, reproduce a minimal failure, fix it, and explain why the original model test detects it.

Then retest one week later with a different API: peek the newest byte without removal. Independent retention matters more than remembering this solution.
''')

write(P+'exercises/REFERENCE_SOLUTIONS.md', r'''
# B01 exercise reference solutions — open after attempting

E01 may live in src/embedded_util.c so it can use ring_valid. Add declarations to the public header. The same non-aliasing output precondition as pop applies.

```c
eu_status eu_ring_peek(const eu_ring *r, uint8_t *out)
{
    if (!ring_valid(r) || out == NULL)
        return EU_INVALID;
    if (r->count == 0u)
        return EU_EMPTY;
    *out = r->storage[r->tail];
    return EU_OK;
}

eu_status eu_packet_payload_sum(const eu_packet *packet, uint32_t *out)
{
    if (packet == NULL || out == NULL)
        return EU_INVALID;
    if (packet->length > EU_PAYLOAD_MAX)
        return EU_LENGTH;
    uint32_t sum = 0u;
    for (size_t i = 0u; i < packet->length; ++i)
        sum += packet->payload[i];
    *out = sum;
    return EU_OK;
}
```

E01 checks: initialize capacity=1; peek(empty) leaves sentinel unchanged; push 9; peek returns 9 twice and count stays 1; pop returns 9; peek empty. For capacity=3 push 1,2,3; pop 1,2; push 4,5; peek returns 3 with identical metadata before/after. Null output yields invalid without mutation.

E02 maximum is 64*255=16320, within uint32_t. Test length 0 returns 0; length 64 all 255 returns 16320; invalid length/null leaves sentinel unchanged. The packet contract, not the numeric type alone, establishes the bound.

E03 faulty capacity-one ring reports full immediately when count=0. A one-byte queue must accept one byte. The implementation counts occupied slots; applying a reserved-slot condition from a different ring representation changes its contract. The shifting-array model is representation independent, so the first successful push expected by the model disagrees.

These small exercise solutions are explanatory reference code. Their integration and new tests have not been executed as part of B01's base suite; learner assessment remains not assessed.
''')

if __name__ == '__main__':
    print('Authored B01 reference implementation and tests')
