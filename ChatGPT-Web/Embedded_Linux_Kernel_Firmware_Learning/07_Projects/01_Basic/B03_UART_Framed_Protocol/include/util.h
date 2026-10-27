#ifndef LEARN_UTIL_H
#define LEARN_UTIL_H
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#define FRAME_MAX_PAYLOAD 128u
#define FRAME_MAX_SIZE (FRAME_MAX_PAYLOAD + 10u)
/* Caller owns storage for the complete lifetime; no implicit locking. */
struct ring { uint8_t *data; size_t capacity, read_at, write_at, count; };
bool ring_init(struct ring *r, uint8_t *storage, size_t capacity);
bool ring_push(struct ring *r, uint8_t value);
bool ring_pop(struct ring *r, uint8_t *value);
bool bit_assign(uint32_t *value, unsigned bit, bool enabled);
uint16_t crc16_ccitt(const uint8_t *data, size_t count);
struct frame { uint8_t type; uint16_t sequence, length; uint8_t payload[FRAME_MAX_PAYLOAD]; };
enum frame_result { FRAME_INVALID=-1, FRAME_MORE=0, FRAME_OK=1 };
size_t frame_encode(const struct frame *frame, uint8_t *dst, size_t capacity);
enum frame_result frame_decode(const uint8_t *src, size_t length,
                               struct frame *out, size_t *consumed);
#endif
