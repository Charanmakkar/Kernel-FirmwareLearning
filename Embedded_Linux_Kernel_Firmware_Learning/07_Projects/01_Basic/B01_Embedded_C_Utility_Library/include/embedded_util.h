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
