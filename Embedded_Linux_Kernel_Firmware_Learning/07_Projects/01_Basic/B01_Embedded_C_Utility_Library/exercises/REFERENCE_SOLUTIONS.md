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
