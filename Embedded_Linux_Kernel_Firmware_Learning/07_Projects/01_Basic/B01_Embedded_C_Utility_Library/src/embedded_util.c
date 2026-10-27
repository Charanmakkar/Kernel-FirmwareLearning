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
