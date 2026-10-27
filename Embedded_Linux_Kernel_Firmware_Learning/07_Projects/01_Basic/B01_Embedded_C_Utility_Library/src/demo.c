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
