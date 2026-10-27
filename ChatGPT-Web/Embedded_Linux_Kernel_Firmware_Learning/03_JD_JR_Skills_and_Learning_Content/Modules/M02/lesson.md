# M02 C memory ownership and defined behavior

## Objectives and prerequisites

Prerequisites: M01.

Track object lifetime and bounds, explain pointer declarations, distinguish language behavior categories and choose qualifiers correctly.

## Lesson


A C pointer carries an address-like value and a type; it does not carry the allocation length or proof that an object is still alive. Define an ownership rule at each API: the caller borrows a buffer for the call, transfers it, or receives a new allocation to release. A pointer to an automatic local object becomes invalid when that object's lifetime ends. Copying the pointer does not extend the lifetime. Null checks cannot detect a dangling non-null pointer.

Arrays and pointers interact but are not the same object. In most expressions an array converts to a pointer to its first element, which loses its size. A parameter declared `int a[]` is adjusted to a pointer parameter. Pass the element count explicitly, and calculate allocation sizes with a checked multiplication before calling `malloc`. For an element size s, reject count greater than SIZE_MAX / s. Use `sizeof *p` so the allocation stays aligned with the pointed-to type.

`const int *p` prevents modification through p; `int *const p` fixes the pointer variable. Neither implies a particular memory region. `volatile` concerns accesses observable to the implementation and is often relevant to vendor-defined MMIO. It does not make a read-modify-write atomic or establish ordering of ordinary shared objects. Use C atomics or a mutex for inter-thread communication. In Linux kernel code use the kernel's accessors and synchronization contracts. [GCC-VOL] [K-VOL]

Unsigned arithmetic wraps modulo its range, which can still be a security or logic defect. Signed overflow has undefined behavior. Integer promotions can surprise bit manipulation: use an unsigned type of known width, validate shift counts and apply a mask deliberately. Do not cast a received byte buffer to a packed structure and assume correct alignment, endianness or ABI layout. Decode fields byte by byte or copy into a suitable object with an explicitly specified representation.

Undefined behavior means the language gives no required result. Unspecified behavior permits more than one allowed choice without requiring documentation. Implementation-defined behavior requires the implementation to document its choice. Do not invent one output for an expression with unsequenced modifications, an invalid pointer access or signed overflow. For an interview, name the violated rule first. The public C11 committee draft is a reference for these foundational contracts, not a substitute for checking the selected compiler dialect. [C11]

Memory corruption often appears far from its origin. A write one byte beyond a buffer can damage a neighbor; the resulting crash may occur during a later free. A sanitizer can expose a failing execution, but a clean test covers only the paths exercised. Pair bounds reasoning with boundary tests, static diagnostics and review. [GCC13]


## Worked lab and expected behavior


Use B01's parser and ring-buffer tests as the worked example. Build the normal target first, then use its sanitizer target if available. For a self-contained ownership example:

```c
int read_u16_be(const unsigned char *p, size_t n,
                unsigned *value)
{
    if (!p || !value || n < 2) return -1;
    *value = ((unsigned)p[0] << 8) | p[1];
    return 0;
}
```

The caller owns p and value; the function borrows them only during the call. Inputs `{0x01,0x02}` decode to 258. A one-byte input returns an error without reading past its end. If a sanitizer reports a stack lifetime error, compare where the object is created, returned and accessed. Do not suppress the report before understanding ownership.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain array decay, const placement, padding and storage duration using your code. Classify three invalid-output questions before predicting values. Interview bank: C memory, UB and synchronization.

## Mastery checklist

- State ownership for every pointer.
- Reject invalid lengths before access.
- Explain qualifiers without claiming synchronization.
- Reproduce and fix a memory error independently.

## Primary references

[C11] WG14 N1570 public draft. [GCC13] GCC 13.3 instrumentation. [GCC-VOL] GCC volatile access. [K-VOL] Linux volatile guidance.
