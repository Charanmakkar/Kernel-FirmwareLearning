# B01 Exercise solutions

A peek should validate the ring and output pointer, return false when count is zero, otherwise copy `data[read_at]` without changing any index or count. A complete implementation is:
```c
bool ring_peek(const struct ring *r, uint8_t *v) {
    if (!r || !v || r->count == 0) return false;
    *v = r->data[r->read_at];
    return true;
}
```
Declare it in the header. Test two peeks before one pop and assert equal values and unchanged count. Each malformed candidate is INVALID with one byte consumed once enough bytes exist to prove the error. A two-byte prefix cannot prove a version error because version has not arrived yet. The separate reference codec is `src/util.c`.

Compare the result with the complete original implementation in `src/`. Passing the supplied tests is one piece of evidence; explain the change without reading this solution before marking the skill demonstrated.
