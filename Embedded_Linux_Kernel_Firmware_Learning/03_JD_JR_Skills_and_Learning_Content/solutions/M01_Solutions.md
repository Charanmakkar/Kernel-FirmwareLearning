# M01 reference solution — separate from attempt

```c
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
bool read_be16(const uint8_t *data, size_t size, size_t offset, uint16_t *out)
{
    if (data == NULL || out == NULL || offset > size || size - offset < 2u)
        return false;
    uint16_t value = (uint16_t)(((uint32_t)data[offset] << 8u)
                              | data[offset + 1u]);
    *out = value;
    return true;
}
```

Short-circuiting checks offset<=size before subtracting; then at least two bytes remain. Therefore offset and offset+1 are valid indexes and the addition cannot wrap. Promotion to uint32_t gives a known unsigned operand for the shift. The output changes only on success. These checks establish an index bound relative to the supplied size, not whether the caller lied about the object or supplied a dangling pointer.

Test each failing call with out initially 0xeeee and verify it remains unchanged. Test offset=SIZE_MAX even when size=4. Test byte sequence 0x80,0x00 to catch signed-byte mistakes. Do not assert a numeric stdout result for undefined behavior. This solution has not been separately compiled by the B01 runner; it is an explanatory exercise answer with its integration test still pending.
