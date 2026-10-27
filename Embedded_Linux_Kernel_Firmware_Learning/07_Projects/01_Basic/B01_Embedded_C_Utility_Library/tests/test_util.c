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
