# Interview question bank

This bank contains 200 distinct questions for shared foundations, Embedded Linux, kernel and BSP development, and MCU firmware. Questions are original teaching and assessment material. Primary references are supplied for verification; no company-specific interview claims are made.

Use Questions_Only.md for a closed-book attempt before opening the answers. Each question has four one-point scoring criteria. A score of 3/4 is a useful retrieval-practice target, but a dangerous incorrect claim about bounds, concurrency, lifetime, update trust, or control authority fails that question regardless of fluent delivery. Complete the practical assessments separately; oral scores do not demonstrate implementation competence.

Assumptions are C11 for C questions, C++17 where stated, Linux/POSIX for system programming, and Linux 6.12 documentation for kernel concepts. Project VERSIONS.md controls actual build targets. Conceptual references to current project documentation do not silently upgrade a project's pinned toolchain. All source access dates are 27 October 2026.

Coding tasks Q021–Q040 and Q161–Q170 have executable reference routines in `../04_Skill_Assessments/answers/coding_reference.c`; Q061 has a complete POSIX helper in `../04_Skill_Assessments/answers/posix_reference.c`. Other Linux coding tasks include precise solution contracts and can be developed against the associated system-programming projects. Full project implementations remain in 07_Projects.

## C objects and behavior

### Q001 How are an array and a pointer different when passed to a function?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Object representation, parameter adjustment, and bounded API design.

**Spoken answer:** An array owns a sequence of elements; a pointer holds an address. An array parameter is adjusted to a pointer, so pass its length separately.

**Deeper explanation:** For `int a[8]`, `sizeof a` in its declaring scope measures the array. In `void f(int a[8])`, `sizeof a` measures a pointer. An interface such as `f(int *a, size_t n)` must still validate `n` against the caller's actual storage contract. A one-past pointer may be formed, but dereferencing it is invalid.

**Assumptions:** Assume ISO C11 and a real array, not a flexible array member.

**Common incorrect answer:** Claiming the callee recovers element count from the pointer or bracket annotation.

**Follow-up:** How would you express read-only access and document whether null is valid at length zero?

**Scoring out of 4:** 1 point each: object distinction; parameter adjustment; length contract; correct one-past rule.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q002 Explain storage duration, scope, and linkage using a static local variable.

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Separating three language concepts that affect firmware state.

**Spoken answer:** Scope controls where a name is visible, storage duration controls lifetime, and linkage connects declarations. A static local persists across calls with block scope.

**Deeper explanation:** In `int next(void) { static unsigned n; return ++n; }`, `n` has static storage duration and no linkage. It is initialized once, before normal execution, and retains state. This is not automatically reentrant or thread safe. A file-scope `static` object instead has internal linkage. Hidden persistent state complicates reset, unit testing, and multiple device instances.

**Assumptions:** Assume C11; integer conversion of the returned unsigned counter needs a separate contract.

**Common incorrect answer:** Saying `static` always means global visibility or a thread-safe singleton.

**Follow-up:** How would you refactor this into an explicit per-instance context with a reset operation?

**Scoring out of 4:** 1 point each: scope; duration; linkage; reentrancy and explicit-state consequence.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q003 What do const placement and volatile placement actually promise?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Type qualifiers and the boundary between language semantics and hardware access.

**Spoken answer:** `const int *p` prevents modification through `p`; `int *const p` fixes the pointer. `volatile` preserves required accesses to a volatile object under implementation rules.

**Deeper explanation:** A const view does not prove the underlying object never changes through another legal alias. Conversely, casting away const and modifying an originally const-defined object is invalid. `volatile` is useful for implementation-defined hardware access patterns, but it supplies neither mutual exclusion nor inter-thread ordering. For Linux MMIO, use the kernel's accessor APIs instead of substituting a volatile pointer.

**Assumptions:** Assume C11; device access width and ordering require target documentation.

**Common incorrect answer:** Treating volatile as atomic, or assuming const universally puts data in ROM.

**Follow-up:** Why might reading a status register twice be incorrect even when both reads are volatile?

**Scoring out of 4:** 1 point each: qualifier placement; alias caveat; volatile limits; hardware API distinction.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q004 Classify signed overflow and unsigned wraparound.

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Integer contracts and avoiding optimization-sensitive bugs.

**Spoken answer:** Unsigned arithmetic wraps modulo its type's range. Signed overflow is undefined behavior; a compiler may optimize on the assumption that it does not happen.

**Deeper explanation:** `int x = INT_MAX; x + 1` has no portable numeric result. Check before the addition, for example positive `b` requires `a <= INT_MAX-b`; handle negative `b` symmetrically. Unsigned wrap can implement a deliberate counter, but it is a bug when it defeats a bounds or allocation check. Sanitizers help expose exercised violations and do not prove absence.

**Assumptions:** Assume standard integer arithmetic without compiler flags defining alternate overflow behavior.

**Common incorrect answer:** Reporting signed overflow always wraps because one observed processor does so.

**Follow-up:** How would you safely check `count * element_size` before allocating?

**Scoring out of 4:** 1 point each: both classifications; precondition check; optimization implication; allocation connection.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q005 Why can comparing a negative int with an unsigned length surprise you?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Usual arithmetic conversions and length validation.

**Spoken answer:** The operands may be converted to an unsigned type, making a negative value a large positive number. Validate signs before crossing signed and unsigned domains.

**Deeper explanation:** For typical equal-rank `int` and `unsigned int`, `-1 < 1u` is false after conversion. The exact conversion path depends on ranks and representable ranges, so avoid memorizing one result for every type combination. Store object sizes as `size_t`, keep negative error codes separate, and only convert a validated nonnegative count. Review mixed comparisons in parsers and syscall result handling.

**Assumptions:** Assume the stated type ranks; `ssize_t` is a POSIX signed result type.

**Common incorrect answer:** Casting every value to unsigned to silence warnings without validating its meaning.

**Follow-up:** How do you handle `read()` returning -1 before comparing its result with a buffer size?

**Scoring out of 4:** 1 point each: conversion mechanism; rank qualification; validated conversion; syscall example.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q006 Is `printf("%d %d", i++, i++)` guaranteed to print a particular pair?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Recognizing undefined behavior instead of guessing evaluation order.

**Spoken answer:** No. The two modifications of the same scalar are unsequenced in C11, so the expression has undefined behavior and no valid universal output.

**Deeper explanation:** Changing optimization level or compiler may change the observation without making either result authoritative. Rewrite as separate full expressions when an order matters: save the first value, increment, save the second, increment, then print the saved values. Distinguish this from unspecified argument order when independent arguments do not create a conflicting access. A code-output interview answer should name the violated rule first.

**Assumptions:** Assume ISO C11; do not transfer C++ sequencing rules without specifying its version.

**Common incorrect answer:** Calling the result merely compiler-dependent or selecting a likely left-to-right order.

**Follow-up:** Give an expression with unspecified evaluation order that does not have undefined behavior.

**Scoring out of 4:** 1 point each: UB classification; unsequenced conflict; valid rewrite; distinction from unspecified order.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q007 What makes returning a pointer to a local array unsafe?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Object lifetime and ownership at function boundaries.

**Spoken answer:** The automatic array's lifetime ends when the function returns. A returned pointer does not extend that lifetime, and dereferencing it is invalid.

**Deeper explanation:** Choose an explicit ownership model: the caller supplies a buffer and capacity; the function allocates and transfers ownership; or it returns a documented immutable static object. Static storage avoids the lifetime bug but may introduce shared-state races and overwrite earlier results. A caller-owned buffer often suits firmware because memory and concurrency are visible. Return a status and written length to distinguish truncation from success.

**Assumptions:** Assume ordinary automatic storage, not an object intentionally allocated on the heap.

**Common incorrect answer:** Believing the pointer is safe until another function happens to reuse the stack.

**Follow-up:** How would the API report required size when the supplied buffer is too small?

**Scoring out of 4:** 1 point each: lifetime; caller-buffer alternative; ownership transfer; static-state tradeoff.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q008 Why is memcpy not a safe replacement for memmove on overlapping regions?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Library preconditions and reasoning about aliasing.

**Spoken answer:** `memcpy` requires nonoverlapping source and destination regions; violating that precondition is undefined behavior. `memmove` supports overlap with an as-if temporary copy.

**Deeper explanation:** Consider shifting a byte buffer one position right: `memmove(buf+1, buf, n)` preserves the original bytes. A naive forward loop overwrites future input; a naive backward loop fails for the opposite overlap direction. Do not compare unrelated object pointers to invent portable overlap detection. Choose the correct contract at the call site and independently verify destination capacity.

**Assumptions:** Assume both source and destination designate valid regions of the requested length.

**Common incorrect answer:** Assuming a particular libc implementation happens to handle overlap, so the code is portable.

**Follow-up:** Does using memmove also solve a destination buffer overflow?

**Scoring out of 4:** 1 point each: overlap precondition; direction example; capacity independence; portable contract.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q009 Can a received byte buffer be cast directly to a C packet structure?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Alignment, object representation, endianness, and defensive decoding.

**Spoken answer:** Usually that is not a portable parser. Structure layout, alignment, padding, byte order, and available input length need explicit handling.

**Deeper explanation:** Decode fixed-width fields from bytes after checking the complete field is present. For a big-endian 16-bit field, combine `((uint16_t)p[0] << 8) | p[1]`. A packed structure may remove padding for a particular compiler, but it can create unaligned accesses and does not resolve endian or lifetime assumptions. Validate lengths before constructing views and avoid trusting a packet's declared size.

**Assumptions:** Assume an octet-based wire format and available `uint16_t`.

**Common incorrect answer:** Using a packed attribute as a complete cross-platform serialization strategy.

**Follow-up:** How would you validate a length field without overflowing `header_size + payload_size`?

**Scoring out of 4:** 1 point each: layout; alignment; explicit decoding; checked bounds.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q010 Why is bit-field layout unsuitable for a portable wire protocol?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Distinguishing convenient source notation from an interchange representation.

**Spoken answer:** C bit-field allocation and ordering are implementation-defined in important respects. Use explicit masks and shifts over well-defined integer or byte representations for a wire format.

**Deeper explanation:** Define bit positions in the protocol specification, for example bit 0 means sensor-valid and bits 1–3 contain a mode. Validate the field value before shifting and preserve reserved bits according to the contract. A register description may also require write-one-to-clear behavior, making a read-modify-write unsafe. Test encoding against fixed vectors instead of comparing only an encoder to its own decoder.

**Assumptions:** Assume the protocol specifies byte order and bit numbering independently of compiler layout.

**Common incorrect answer:** Expecting a bit-field structure to have identical layout across compilers and endian targets.

**Follow-up:** What additional precautions apply when the destination is a hardware status register?

**Scoring out of 4:** 1 point each: implementation dependence; explicit masks; reserved-bit rule; register side effects.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q011 When is a shift expression undefined or implementation-defined?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Boundary conditions in bit operations.

**Spoken answer:** A negative shift count or a count at least the promoted left operand width is undefined. Signed shifts have additional restrictions; prefer unsigned operands for bit masks.

**Deeper explanation:** For `1u << n`, validate `n` against the width of `unsigned`, not an assumed 32. In C11, right shifting a negative signed value is implementation-defined. Left shifting signed values is not a general multiplication substitute because representability restrictions apply. Integer promotions also mean a `uint8_t` operand may be promoted before shifting. Use width-specific constants and document the supported width.

**Assumptions:** Assume C11 and no implementation extension that changes these semantics.

**Common incorrect answer:** Claiming the processor masks the count, so shifting by the width is valid C.

**Follow-up:** How would you construct a full-width mask without evaluating `1u << width`?

**Scoring out of 4:** 1 point each: count limits; unsigned choice; negative-right-shift qualification; promotions.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q012 Explain strict aliasing and a safe way to inspect a float's bytes.

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Access type rules and representation inspection.

**Spoken answer:** Accessing an object through an incompatible lvalue type can violate C's effective-type rules. Character-type access may inspect its representation; memcpy also avoids an incompatible pointer dereference.

**Deeper explanation:** Copy a float into an unsigned-character array with `memcpy(bytes, &f, sizeof f)` and inspect the bytes as representation, not as a promised IEEE-754 encoding. Copying into an equal-sized integer can be useful only with an explicit size and representation assumption. Pointer-casting a float to `uint32_t *` risks both aliasing and alignment problems. Compiler optimization can expose bugs hidden in debug builds.

**Assumptions:** Assume ISO C11; floating representation and byte order are target properties.

**Common incorrect answer:** Saying equal object sizes make all pointer casts legal.

**Follow-up:** How would you serialize a floating measurement for heterogeneous machines?

**Scoring out of 4:** 1 point each: incompatible access; character exception; memcpy pattern; representation caveat.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q013 What is the difference between a null pointer and an uninitialized pointer?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Initialization and error-resistant API contracts.

**Spoken answer:** A null pointer is a defined value that designates no object or function. An uninitialized automatic pointer has an indeterminate value and is not a valid substitute.

**Deeper explanation:** Initializing an owner to null makes cleanup paths simpler because `free(NULL)` is defined. It does not make every null dereference or every function call with null acceptable. Document whether an API accepts null with zero length. After freeing, clear the owner when useful, but other aliases remain dangling; clearing one variable does not resolve shared ownership or use-after-free elsewhere.

**Assumptions:** Assume a hosted C implementation; an all-zero byte pattern is not a universal pointer representation.

**Common incorrect answer:** Treating an uninitialized pointer as probably null or clearing one alias as a lifetime solution.

**Follow-up:** Why is `memset(&p, 0, sizeof p)` a weaker portable initialization than `p = NULL`?

**Scoring out of 4:** 1 point each: defined null; indeterminate pointer; API contract; dangling aliases.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q014 How should realloc failure be handled without losing the original allocation?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Ownership-preserving allocation and size contracts.

**Spoken answer:** Assign the result to a temporary pointer. On failure for a nonzero requested size, retain the original allocation and decide whether to continue or free it.

**Deeper explanation:** Use `void *tmp = realloc(p, new_size); if (!tmp) { /* preserve p */ } else p = tmp;`. Validate multiplication before calculating `new_size`; define zero-size behavior explicitly rather than relying on version-sensitive rules. A successful move invalidates the old pointer and interior aliases. Embedded software may instead use fixed-capacity buffers when bounded memory usage and deterministic failure behavior matter.

**Assumptions:** Assume nonzero size and a standard hosted allocator; ISR allocation is a separate policy question.

**Common incorrect answer:** Overwriting the sole owning pointer directly and then being unable to free on failure.

**Follow-up:** What happens to a pointer into the old allocation after a successful relocation?

**Scoring out of 4:** 1 point each: temporary owner; size validation; aliases; zero-size qualification.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q015 What can a function pointer safely represent in a driver-like C interface?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Typed callbacks, context ownership, and dispatch.

**Spoken answer:** A function pointer can select behavior through a compatible function type. Pair it with explicit context and a lifetime contract for callback registration and removal.

**Deeper explanation:** For example, `struct sink { int (*write)(void *, const unsigned char *, size_t); void *ctx; };` makes state ownership visible. Define whether callbacks may block, whether they can be called concurrently, and who owns the input during the call. Calling through an incompatible function-pointer type is not repaired by a cast. Unregistering requires preventing new calls and waiting for in-flight calls before freeing context.

**Assumptions:** Assume C11; converting object pointers to function pointers is not generally portable ISO C.

**Common incorrect answer:** Casting any callback signature to the expected type and trusting matching register usage.

**Follow-up:** How would cancellation work when a callback may already be running?

**Scoring out of 4:** 1 point each: compatible type; explicit context; execution contract; unregister lifetime.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q016 How do alignment and structure padding affect an embedded ABI?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Memory layout versus source-field intuition.

**Spoken answer:** Compilers may insert padding to satisfy alignment, so a structure's size is not necessarily the sum of its member sizes. ABI rules determine the concrete layout.

**Deeper explanation:** Reordering private members can reduce padding, but changing a public structure may break binary compatibility. Use `sizeof`, `_Alignof`, `offsetof`, and compile-time assertions for an explicitly supported target. Do not compare whole structures with `memcmp` to test semantic equality because padding may differ. DMA buffers, shared memory, and wire data each have distinct layout and alignment contracts that should be specified separately.

**Assumptions:** Assume C11 and the selected compiler ABI; exact offsets must be measured or documented.

**Common incorrect answer:** Assuming packing is a cost-free way to save memory on every architecture.

**Follow-up:** Which problems can appear when a packed member is passed to a function expecting aligned storage?

**Scoring out of 4:** 1 point each: padding; ABI contract; semantic comparison; packed-access consequence.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q017 What makes a C API reentrant, and how is that different from thread safe?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** State isolation and nested-call reasoning.

**Spoken answer:** A reentrant function can be entered again before an earlier invocation finishes without corrupting state. Thread safety concerns concurrent calls under a specified threading model.

**Deeper explanation:** A function protected by a nonrecursive mutex may be thread safe yet unsafe to call recursively from a signal path or callback that interrupts its execution. Per-call local state and caller-owned contexts improve reentrancy, but callees and allocator behavior still matter. An interrupt handler has stricter allowed-operation rules than ordinary threads. State precisely which callers, contexts, and shared resources an API supports.

**Assumptions:** Assume the terms are evaluated against an explicit execution model rather than as unconditional labels.

**Common incorrect answer:** Treating a mutex as proof that an API is safe in a signal handler or ISR.

**Follow-up:** Can a function with only local variables still be non-reentrant because of a callee?

**Scoring out of 4:** 1 point each: nested entry; thread distinction; callee effects; context restrictions.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q018 Why does volatile not fix a shared-counter data race?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** The C memory model and atomic read-modify-write.

**Spoken answer:** Volatile does not make an increment atomic or establish synchronization between threads. Use a mutex or a suitable C atomic operation, depending on the required invariant.

**Deeper explanation:** `counter++` includes a read and write that can overlap another increment. Even when machine word accesses are naturally atomic, unsynchronized conflicting C accesses can be undefined behavior. `_Atomic unsigned` with `atomic_fetch_add` makes the update atomic; relaxed ordering is enough only when the counter does not publish other state. A multi-field invariant usually needs a larger synchronization design.

**Assumptions:** Assume C11 threads and objects shared by threads; MMIO is a different problem.

**Common incorrect answer:** Arguing that a single-core CPU or optimization level makes the data race acceptable.

**Follow-up:** When would acquire-release ordering be needed instead of a relaxed counter increment?

**Scoring out of 4:** 1 point each: race; atomic RMW; relaxed limit; multi-field invariant.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q019 What does undefined behavior imply for a code-output interview question?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Disciplined reasoning under missing language guarantees.

**Spoken answer:** State that the standard gives no guaranteed behavior, identify the first violated precondition, and propose a valid rewrite. Do not manufacture one universal output.

**Deeper explanation:** Examples include using a freed object, out-of-bounds access, signed overflow, and conflicting unsequenced accesses. An experiment can show one implementation's observation but cannot define all valid implementations. Separate undefined behavior from unspecified choices and implementation-defined behavior that must be documented. Ask for the language version, data model, and compiler extensions only when those can legitimately resolve the question.

**Assumptions:** Assume ISO C semantics unless the interviewer explicitly requests a documented extension.

**Common incorrect answer:** Calling every surprising result undefined or every observed result implementation-defined.

**Follow-up:** How would you explain an optimization-sensitive crash to a colleague without blaming the compiler prematurely?

**Scoring out of 4:** 1 point each: precise classification; first violation; valid rewrite; experiment limitation.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q020 How do you choose between fixed allocation, a pool, and general heap allocation?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**Assesses:** Resource budgeting and failure behavior in embedded software.

**Spoken answer:** Choose from measured lifetime patterns and timing requirements. Fixed storage is simple and bounded; pools bound object counts; a general allocator supports flexibility with more failure modes.

**Deeper explanation:** A telemetry queue can use a fixed ring when overload policy is explicit. A pool can serve equal-sized request objects without general external fragmentation. Heap use may be reasonable during initialization or noncritical work, but handle exhaustion and document ownership. Avoid claiming all heaps are nondeterministic or all static allocation is safe: static sizing can still overflow or silently drop important work.

**Assumptions:** Assume the target's allocator, memory budget, and scheduling constraints are known before final selection.

**Common incorrect answer:** Banning all dynamic allocation without explaining the actual lifetime or timing requirement.

**Follow-up:** How will the system behave when the pool is empty, and how will that be observed?

**Scoring out of 4:** 1 point each: lifetime analysis; bounded capacity; failure policy; measured tradeoff.

**Learning connection:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

## C coding exercises

### Q021 Implement checked multiplication for two size_t values before allocation.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Overflow prevention without evaluating an already-overflowed result.

**Spoken answer:** Reject multiplication when the second operand is nonzero and the first exceeds `SIZE_MAX / second`. Otherwise store the product through a valid output pointer.

**Deeper explanation:** The reference function `checked_mul` returns false on overflow and leaves the output unchanged. Cases include `(0, SIZE_MAX)`, `(SIZE_MAX, 1)`, and `(SIZE_MAX, 2)`. Do not check the wrapped product afterward. Also distinguish representability from an application's smaller memory limit: a mathematically valid allocation can still fail or be unacceptable for the target.

**Assumptions:** Assume a nonnull output pointer; the API explicitly rejects null in the reference implementation.

**Common incorrect answer:** Testing only `a*b < a`, which misses some overflow combinations and obscures the contract.

**Follow-up:** How would you add a header size to the multiplication result safely?

**Scoring out of 4:** 1 point each: division precheck; zero handling; unchanged failure output; boundary tests.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q022 Write a bounds-checked big-endian 16-bit decoder from bytes.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Portable byte decoding and a clear error interface.

**Spoken answer:** Require at least two bytes, widen each byte before shifting, combine them, and return status separately from the decoded value.

**Deeper explanation:** `decode_be16` accepts a byte pointer, length, and output pointer; invalid pointers or short input fail without modifying output. Vectors `00 00`, `12 34`, and `ff ff` must yield 0, 4660, and 65535. Casting the input to `uint16_t *` is unnecessary and can introduce alignment, endian, and aliasing assumptions. Larger parsers must retain a cursor and remaining-length invariant.

**Assumptions:** Assume 8-bit bytes and availability of `uint16_t`; the wire format is big-endian.

**Common incorrect answer:** Returning zero on error, making an invalid packet indistinguishable from a valid zero reading.

**Follow-up:** How would the interface advance a cursor only when decoding succeeds?

**Scoring out of 4:** 1 point each: length check; explicit endian conversion; status separation; unmodified failure state.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q023 Implement an eight-byte ring buffer with explicit full and empty states.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Capacity invariants, wraparound, and overload policy.

**Spoken answer:** Track head, tail, and count. Push only when count is below capacity; pop only when count is nonzero. Advance indices modulo the fixed capacity.

**Deeper explanation:** The reference `ring_push` and `ring_pop` reject full and empty operations without altering state. Test filling all eight slots, a ninth push, partial draining, wraparound writes, then FIFO order. Maintaining count allows all eight elements to be usable. This simple implementation is single-threaded; synchronization cannot be added by merely qualifying fields volatile. Define whether a future application drops, blocks, or replaces data when full.

**Assumptions:** Assume a caller-initialized zeroed ring and no concurrent access.

**Common incorrect answer:** Allowing head equal to tail to ambiguously mean both full and empty.

**Follow-up:** How would a single-producer single-consumer atomic implementation publish an element safely?

**Scoring out of 4:** 1 point each: invariant; wraparound; no mutation on failure; concurrency qualification.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q024 Convert an even-length ASCII hexadecimal string into a bounded byte buffer.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Validation, capacity checks, and transactional parsing.

**Spoken answer:** Reject odd length, invalid digits, and insufficient output capacity. Validate all characters before modifying output if the API promises failure leaves output unchanged.

**Deeper explanation:** `hex_decode` accepts upper- and lowercase hex without separators. `"00aF"` becomes two bytes; `"0"`, `"0G"`, and a two-byte result with capacity one fail. The reference uses explicit digit classification rather than a locale-sensitive permissive parser. Record output length only on success. Two-pass validation costs another linear scan but makes the failure contract simple for callers.

**Assumptions:** Assume a NUL-terminated input and output storage that does not overlap it.

**Common incorrect answer:** Using a conversion routine that silently stops at the first invalid character.

**Follow-up:** When would a streaming decoder with partial progress be a better contract?

**Scoring out of 4:** 1 point each: all validation; bounded output; transactional failure; case and malformed tests.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q025 Reverse a byte array in place without accessing beyond either end.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Index invariants and zero-length handling.

**Spoken answer:** Swap symmetric elements while the left index is below half the length. Compute the matching index as `n-1-i` only inside that loop.

**Deeper explanation:** `reverse_bytes` treats null with zero length as valid but rejects null with positive length. The half-length loop avoids computing `n-1` for an empty array, so there is no unsigned underflow before a guard. Test lengths zero, one, two, and five, plus applying reverse twice. This is linear time and constant extra space; the contract does not promise safe concurrent mutation.

**Assumptions:** Assume ordinary writable byte storage for every index in the stated length.

**Common incorrect answer:** Starting an unsigned right index at `n-1` before checking `n == 0`.

**Follow-up:** How would reversing UTF-8 bytes differ from reversing user-visible characters?

**Scoring out of 4:** 1 point each: empty input; valid indices; odd middle element; stated byte-level scope.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q026 Set or clear a selected bit in a uint32_t without undefined shifts.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Bit-width validation and preserving unrelated bits.

**Spoken answer:** Reject bit indices 32 or above. Build a `UINT32_C(1)` mask, then OR it to set or AND its complement to clear.

**Deeper explanation:** `bit_assign` receives an output pointer, index, and boolean value. Tests must preserve all other bits, exercise indices zero and 31, and reject 32. A zero initial value helps test set operations; all-ones tests clear operations. This function operates on an ordinary in-memory object. Applying an equivalent read-modify-write to a hardware register may be wrong when bits are write-one-to-clear or concurrently updated.

**Assumptions:** Assume `uint32_t` exists and the object is not concurrently modified.

**Common incorrect answer:** Using signed `1 << 31` or accepting an unchecked shift count.

**Follow-up:** How would an atomic shared flags word change the implementation?

**Scoring out of 4:** 1 point each: index bound; unsigned mask; preservation; MMIO and concurrency caveat.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q027 Implement CRC-16/CCITT-FALSE and verify a known check value.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Protocol interoperability and complete CRC parameterization.

**Spoken answer:** Use polynomial 0x1021, initial value 0xffff, no input/output reflection, and final XOR zero. The ASCII bytes of `123456789` produce 0x29b1.

**Deeper explanation:** `crc16_ccitt` processes each byte into the high end of the register and advances eight polynomial steps. CRC names alone can be ambiguous, so put all parameters and byte order in the protocol document. The function returns 0xffff for empty input. CRC detects many accidental transmission errors but supplies no authentication; an attacker can recompute it after modifying a message.

**Assumptions:** Assume eight-bit bytes; null is allowed only with zero input length.

**Common incorrect answer:** Using another CRC-16 variant and assuming all peers will agree because the width matches.

**Follow-up:** What wire byte order will you choose for the two CRC bytes, and why specify it separately?

**Scoring out of 4:** 1 point each: parameters; check vector; empty input; integrity versus authenticity.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q028 Parse a decimal uint32_t with no trailing characters or overflow.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Defensive conversion of external text.

**Spoken answer:** Require at least one decimal digit and reject signs, whitespace, and trailing characters under the stated grammar. Before each step, ensure the next multiply-add fits.

**Deeper explanation:** `parse_u32` checks `value > (UINT32_MAX-digit)/10` before updating. Test zero, 4294967295, 4294967296, empty input, `12x`, and `-1`. The output stays unchanged on failure. This narrow grammar suits machine configuration; a command-line UI may choose a more permissive grammar, but should do so explicitly. Avoid conflating parse failure with numeric zero.

**Assumptions:** Assume NUL-terminated ASCII input and a nonnull output pointer.

**Common incorrect answer:** Using atoi, which cannot express the necessary error and range distinctions.

**Follow-up:** How would you support optional base prefixes without silently accepting octal unexpectedly?

**Scoring out of 4:** 1 point each: grammar; precheck; status contract; maximum and malformed cases.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q029 Write a bounded string copy that reports truncation explicitly.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** C string termination and useful caller-visible status.

**Spoken answer:** If capacity is positive, copy at most capacity minus one characters and terminate. Return success only when the complete source fits; report the needed length separately.

**Deeper explanation:** `copy_text` computes the source length and handles zero capacity without writing. Test an exact fit including the terminator, one-byte destination, empty source, and insufficient space. A terminated partial string is still truncated, so callers must not treat termination as complete success. Document that the source and destination cannot overlap. Avoid using a silent truncation helper for security-sensitive identifiers.

**Assumptions:** Assume a valid NUL-terminated source; source length excludes its terminator.

**Common incorrect answer:** Claiming strncpy always terminates or that a truncated pathname is an acceptable success.

**Follow-up:** When would rejecting the entire operation be preferable to writing a truncated prefix?

**Scoring out of 4:** 1 point each: terminator; zero capacity; explicit truncation; overlap and semantic contract.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q030 Implement a saturating addition of two uint32_t values.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Deliberate arithmetic policy instead of accidental wraparound.

**Spoken answer:** Return `UINT32_MAX` when `a > UINT32_MAX-b`; otherwise return `a+b`. Saturation is an explicit application policy, distinct from modular arithmetic.

**Deeper explanation:** `saturating_add` is useful for cumulative diagnostics where wraparound would hide repeated errors. Test zero, values adding exactly to the maximum, and an overflowing pair. The operation sacrifices information once saturated, so expose a saturation indicator if the application needs to distinguish a true maximum from overflow. Do not transfer this unsigned check to signed arithmetic without considering both overflow directions.

**Assumptions:** Assume a 32-bit unsigned result and no requirement to count beyond saturation.

**Common incorrect answer:** Computing the sum first and casting it to a larger type afterward.

**Follow-up:** How would you extend the interface to return a separate overflow flag?

**Scoring out of 4:** 1 point each: precondition; exact boundary; policy explanation; loss-of-information consequence.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q031 Implement a debounced boolean input state machine using sample counts.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** State transitions, noisy input handling, and bounded state.

**Spoken answer:** Keep the stable value, a candidate value, and consecutive candidate count. Commit a change only after the candidate persists for the configured number of samples.

**Deeper explanation:** `debounce_step` resets the candidate count when a sample disagrees with the pending candidate. Use threshold three and the trace `0,1,0,1,1,1` from stable zero: only the last sample changes the stable output. Saturate the count rather than allowing it to wrap. Sample-count debounce depends on sample cadence; missed samples alter wall-clock behavior and must be considered when specifying latency.

**Assumptions:** Assume periodic sampling and a threshold of at least one.

**Common incorrect answer:** Delaying in an ISR for the whole debounce interval or counting nonconsecutive samples as stable.

**Follow-up:** How would the design change to debounce by monotonic timestamps instead of sample count?

**Scoring out of 4:** 1 point each: candidate state; consecutive rule; bounded counter; timing interpretation.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q032 Implement an integer moving average over the most recent four samples.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Window maintenance, startup behavior, and accumulator range.

**Spoken answer:** Keep a four-element ring, running sum, current count, and next replacement index. Subtract the outgoing sample only after the window fills, then add the new sample.

**Deeper explanation:** `average_push` uses a 64-bit sum for 32-bit samples and divides by the current count during startup. For inputs 4, 8, 12, 16, 20, outputs are 4, 6, 8, 10, 14 with integer truncation. A running sum gives constant work per sample. Define rounding, signedness, and missing-sample behavior rather than assuming every averaging application shares one interpretation.

**Assumptions:** Assume unsigned 32-bit samples and a four-sample count-based window.

**Common incorrect answer:** Dividing by four before four samples exist without stating that zero-padding is intended.

**Follow-up:** How would you detect the maximum required accumulator width for a configurable window?

**Scoring out of 4:** 1 point each: replace/subtract rule; startup count; wide accumulator; known sequence.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q033 Insert a uint32_t into a sorted fixed-capacity array.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Bounds, shifting, and a precise duplicate policy.

**Spoken answer:** Reject a full array, find the insertion position, shift larger elements right, insert the value, and increment count only after success.

**Deeper explanation:** `sorted_insert` places a duplicate after existing equal values. Test insertion at the beginning, middle, and end; duplicates; empty storage; and full capacity with unchanged contents. Moving elements backward prevents overwriting values that still need to move. The operation is linear time, which is reasonable for small bounded embedded collections but different from a logarithmic lookup requirement.

**Assumptions:** Assume the first count elements are already sorted and count does not exceed capacity.

**Common incorrect answer:** Shifting forward into the destination or updating count before validating capacity.

**Follow-up:** When would a heap or bitmap be a better data structure than a sorted array?

**Scoring out of 4:** 1 point each: capacity; backward shift; duplicate contract; boundary and complexity analysis.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q034 Compare a wrapping 32-bit tick counter against a deadline safely.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Modular-time assumptions and half-range ambiguity.

**Spoken answer:** Use unsigned subtraction and a documented half-range rule. A deadline is reached when `(uint32_t)(now-deadline) < 0x80000000u`, provided relevant distances stay below half the range.

**Deeper explanation:** `tick_due` is portable unsigned arithmetic and avoids relying on out-of-range unsigned-to-signed conversion. Test a deadline of 0xfffffff0 against times just before it, equal to it, and 0x00000010 after wrap. Exactly half a cycle is ambiguous and excluded by the contract. Expired deadlines must be consumed or refreshed before a full ambiguity window passes.

**Assumptions:** Assume no scheduled interval or observation gap reaches 2^31 ticks.

**Common incorrect answer:** Comparing `now >= deadline` or claiming wrap-safe arithmetic works for arbitrarily long intervals.

**Follow-up:** How would you handle a timer that may be suspended longer than half a counter cycle?

**Scoring out of 4:** 1 point each: unsigned difference; half-range condition; wrap example; observation-gap limit.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q035 Detect a cycle in a singly linked list using constant extra space.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Pointer traversal invariants and algorithmic reasoning.

**Spoken answer:** Advance a slow pointer one link and a fast pointer two links, checking fast and its next pointer before advancing. A meeting indicates a cycle.

**Deeper explanation:** `list_has_cycle` covers an empty list, a one-node noncycle, a self-loop, and a cycle starting after a prefix. The method is linear in the reachable nodes before detection and constant in additional storage. It presumes every traversed link points to a live node or null; it cannot safely validate arbitrary corrupted addresses. Concurrency would require a separate lifetime strategy.

**Assumptions:** Assume an immutable list during the check and valid node storage.

**Common incorrect answer:** Dereferencing `fast->next->next` before verifying the necessary pointers.

**Follow-up:** How would you find the entry point of the cycle after detecting a meeting?

**Scoring out of 4:** 1 point each: two speeds; null guards; cycle cases; valid-memory assumption.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q036 Count the set bits in a uint32_t without a 32-iteration loop.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Bit identities and complexity that depends on input.

**Spoken answer:** Repeatedly clear the lowest set bit with `x &= x-1` and increment a counter until x becomes zero. Each iteration removes exactly one set bit.

**Deeper explanation:** `popcount32` returns zero for zero and 32 for all ones. Explain why subtraction flips the lowest one and lower zero bits, making the AND clear only that one. The algorithm executes as many iterations as set bits; it is not constant-time with respect to the value. A compiler intrinsic may map to an efficient instruction but requires a documented portability fallback.

**Assumptions:** Assume unsigned arithmetic; timing-sensitive cryptographic code needs separate analysis.

**Common incorrect answer:** Claiming the algorithm always executes exactly 32 steps or using signed overflow-prone intermediates.

**Follow-up:** When would a table, intrinsic, or constant-step method be preferable?

**Scoring out of 4:** 1 point each: identity; zero/all-ones cases; input-dependent work; portability/timing tradeoff.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q037 Round a size_t up to a power-of-two alignment without overflow.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Alignment preconditions and checked arithmetic.

**Spoken answer:** Reject zero or non-power-of-two alignment. Check `size <= SIZE_MAX-(alignment-1)` before computing `(size+alignment-1) & ~(alignment-1)`.

**Deeper explanation:** `round_up` keeps the output unchanged on failure. Test already aligned sizes, zero, one below a boundary, alignment one, invalid alignment three, and overflow near `SIZE_MAX`. The result describes a numeric size; it does not itself allocate memory with that alignment. Also respect a target allocator's supported alignment values and minimum requirements.

**Assumptions:** Assume alignment fits size_t and only power-of-two alignment is supported by this API.

**Common incorrect answer:** Using the mask formula for arbitrary alignment or ignoring the addition overflow.

**Follow-up:** How would you round up to a non-power-of-two block size safely?

**Scoring out of 4:** 1 point each: power-of-two check; overflow check; exact mask; allocation distinction.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q038 Validate a sequence of one-byte-type one-byte-length TLV records.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Length-driven parsing and progress guarantees.

**Spoken answer:** Require a complete two-byte header, then ensure the declared value length fits the remaining input. Advance by header plus value and require exact exhaustion.

**Deeper explanation:** `validate_tlvs` accepts unknown types structurally and counts records; semantic policy is separate. Test empty input, a zero-length value, multiple records, a truncated header, and an oversized final value. Comparing length with remaining bytes avoids overflow-prone absolute-end calculations. Every successful iteration consumes at least the two-byte header, so zero-length values cannot cause an infinite loop.

**Assumptions:** Assume the outer buffer length is trusted and values contain arbitrary bytes.

**Common incorrect answer:** Advancing by value length alone or accepting a trailing orphan byte as harmless padding.

**Follow-up:** How would you cap nesting depth if a type contains another TLV sequence?

**Scoring out of 4:** 1 point each: header bound; value bound; forward progress; semantic/structural separation.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q039 Implement hysteresis for a high-temperature alarm.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Stateful threshold behavior and boundary precision.

**Spoken answer:** Turn the alarm on at or above the high threshold and off at or below the low threshold. Between thresholds, preserve the prior alarm state.

**Deeper explanation:** `alarm_step` rejects invalid threshold ordering and returns the next state through an output pointer. With low 60 and high 70, the trace 65, 71, 68, 60 yields off, on, on, off from an initially off state. Hysteresis limits chatter but does not filter measurement noise in every circumstance; sampling, debounce, and sensor validity may still need separate policies.

**Assumptions:** Assume integer temperatures in one documented unit and low strictly below high.

**Common incorrect answer:** Recomputing alarm as `temperature >= high` on every sample and losing the hold state.

**Follow-up:** What should happen when the sensor reading is invalid or stale?

**Scoring out of 4:** 1 point each: two transitions; hold band; boundary tests; invalid/stale-data policy.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

### Q040 Replace a bounded bit field in a uint32_t while preserving other bits.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Bit-range validation, mask construction, and overflow-free shifts.

**Spoken answer:** Validate width and offset, ensure the field fits within 32 bits, and reject a value too large for the field. Clear the field mask then insert the shifted value.

**Deeper explanation:** `field_replace` handles a full-width field separately so it never computes `1u << 32`. Test a four-bit field at offset eight, a one-bit field at bit 31, a full-width replacement, and out-of-range values. Width zero is rejected by this contract. This routine updates ordinary memory; hardware registers may require different write semantics or atomic access.

**Assumptions:** Assume nonconcurrent uint32_t storage and explicitly numbered least-significant-bit offsets.

**Common incorrect answer:** Allowing the value to spill into adjacent bits or constructing a full-width mask with an invalid shift.

**Follow-up:** How would you adapt the interface to extract the same field and verify encode-decode vectors?

**Scoring out of 4:** 1 point each: range; value bound; full-width case; unrelated-bit preservation.

**Learning connection:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

## Tools linking and C++

### Q041 Explain preprocessing, compilation, assembly, and linking using one missing-symbol error.

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Locating a build failure at the correct stage.

**Spoken answer:** Preprocessing expands includes and macros, compilation produces assembly, assembly produces objects, and linking resolves references and creates an executable or library.

**Deeper explanation:** An undefined reference at link time can mean the implementation was not compiled, the object or library was omitted, the archive order is wrong, or symbol naming differs. Inspect commands with verbose builds, then use `nm` and `readelf` on the actual objects. A header declaration alone does not provide an implementation. Avoid changing source randomly when the failing stage is the link command.

**Assumptions:** Assume GCC-style ELF tooling; exact options and link-order behavior depend on the linker.

**Common incorrect answer:** Adding more include directories to fix an omitted function definition at link time.

**Follow-up:** How would C++ name mangling affect linking a C library?

**Scoring out of 4:** 1 point each: stages; plausible symbol causes; object inspection; declaration/definition distinction.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q042 What information can readelf and a linker map reveal that source code cannot?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Binary-level verification of a firmware build.

**Spoken answer:** They reveal section placement, symbols, relocations, entry points, and loadable segments. A map connects memory usage to input objects and linker decisions.

**Deeper explanation:** For a microcontroller image, check vector placement, flash and RAM regions, data load versus run addresses, and stack/heap reservations. For an ELF Linux binary, inspect interpreter path and required architecture. Source may look correct while the linker places a buffer in the wrong memory region. Compare actual section sizes against the linker script's limits and preserve the map with the build evidence.

**Assumptions:** Assume the selected ELF toolchain; some bare-metal artifacts are later converted to binary or Intel HEX.

**Common incorrect answer:** Equating the executable file size with runtime RAM usage.

**Follow-up:** Why might `.bss` consume RAM while contributing little payload to the image file?

**Scoring out of 4:** 1 point each: sections/segments; symbol ownership; memory budgeting; load/run distinction.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q043 What is the difference between an ABI and an API?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Compatibility across compilation and runtime boundaries.

**Spoken answer:** An API defines source-level interfaces and behavior. An ABI defines binary conventions such as calling convention, data layout, symbol naming, and object format.

**Deeper explanation:** Two builds may expose the same C function declaration but disagree on floating-point calling convention, structure packing, or architecture. That can cause runtime corruption even when names link. Pin compiler target options and compatible libraries, and rebuild dependent components when ABI changes. Linux user-space interfaces and internal kernel interfaces have different stability expectations; out-of-tree modules must match their target build.

**Assumptions:** Assume the same source language does not imply the same target ABI.

**Common incorrect answer:** Saying recompilation is never necessary because the header text is unchanged.

**Follow-up:** Which ABI evidence would you collect when a cross-compiled program crashes immediately?

**Scoring out of 4:** 1 point each: API/ABI distinction; concrete conventions; compatibility checks; kernel qualification.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q044 How does RAII improve resource handling in C++ system code?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Lifetime-bound cleanup and ownership transfer.

**Spoken answer:** Resource Acquisition Is Initialization ties resource ownership to an object's lifetime so destructors release resources on every normal scope-exit path, including exceptions.

**Deeper explanation:** Wrap a file descriptor in a move-only type that closes only when it owns a valid descriptor. Delete copying, transfer ownership during move, and make destruction nonthrowing. RAII applies to locks, mappings, and transactions, not just heap memory. It does not by itself prevent deadlocks, ambiguous shared ownership, or failure during a close-like operation that needs explicit reporting.

**Assumptions:** Assume C++17 or later for examples; exception policy depends on the embedded project.

**Common incorrect answer:** Treating a raw pointer member as ownership without implementing safe copy/move behavior.

**Follow-up:** How would you expose an explicit finalize operation for a resource whose release can fail?

**Scoring out of 4:** 1 point each: lifetime cleanup; move-only ownership; nonthrowing destructor; explicit error tradeoff.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q045 When would you use unique_ptr, shared_ptr, or a nonowning pointer?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Ownership communication and avoiding unnecessary shared lifetime.

**Spoken answer:** Use unique ownership by default when one component controls lifetime. Use shared ownership only for genuinely shared lifetime; use nonowning references or pointers with a clear validity contract.

**Deeper explanation:** `shared_ptr` reference counting has overhead and does not make the pointed-to object thread safe. Cycles require redesign or weak references. In a driver-like application, a manager can own a device object while short-lived operations borrow it under an explicit shutdown protocol. Ownership type and concurrency control solve different problems. Firmware may impose allocation policies that constrain standard-library use.

**Assumptions:** Assume C++17 and a toolchain/runtime supporting the selected library features.

**Common incorrect answer:** Choosing shared_ptr everywhere to avoid designing ownership or assuming it prevents data races.

**Follow-up:** How do you prevent a callback from using a borrowed object after shutdown?

**Scoring out of 4:** 1 point each: ownership choices; shared cost/cycles; data race distinction; borrower lifetime.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q046 How would you make a Make or CMake build reproducible enough to investigate a regression?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Controlled inputs and traceable build configuration.

**Spoken answer:** Record source revision, toolchain, options, dependency versions, configuration, and build environment. Rebuild from a clean or well-defined incremental state and compare artifacts appropriately.

**Deeper explanation:** Avoid embedding uncontrolled timestamps and host-specific absolute paths when bit-identical output matters. A successful rebuild is weaker than a reproducible binary. Keep generated files deterministic and include their generators. When a regression appears, compare the actual compile/link commands before assuming the source change alone caused it. A container helps capture environment but does not pin external downloads by itself.

**Assumptions:** Assume reproducibility goals are stated as repeatable behavior or byte-identical artifacts.

**Common incorrect answer:** Claiming a container tag or a committed Makefile proves every dependency is fixed.

**Follow-up:** How would you identify why two nominally identical ELF files differ?

**Scoring out of 4:** 1 point each: input manifest; environment control; goal distinction; artifact comparison.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q047 Why can a static library link fail depending on command-line order?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Archive extraction and dependency direction.

**Spoken answer:** Many traditional linkers scan archives to satisfy unresolved symbols known at that point, so objects that require symbols commonly precede their providing archives.

**Deeper explanation:** For an object using a utility library that itself uses a math library, an order such as `app.o -lutil -lm` may be required. Circular archive dependencies may need grouping or architectural cleanup. Shared-library behavior and linker options can alter details, so inspect the selected linker rather than applying a universal slogan. The useful debugging question is which unresolved symbol existed when an archive was scanned.

**Assumptions:** Assume a conventional GNU-style archive-linking model; confirm the active linker and flags.

**Common incorrect answer:** Rearranging include directives or adding the same library repeatedly without understanding the dependency graph.

**Follow-up:** What do archive groups change, and why can excessive circular dependencies signal a design problem?

**Scoring out of 4:** 1 point each: unresolved-symbol scan; example order; linker qualification; dependency reasoning.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q048 What should a useful embedded code review examine beyond formatting?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Risk-focused review of interfaces and failure paths.

**Spoken answer:** Review ownership, bounds, execution context, concurrency, timeout behavior, error recovery, tests, and observability against requirements. Style is useful but does not establish correctness.

**Deeper explanation:** Trace a resource from acquisition through normal completion, error unwinding, cancellation, and shutdown. For a parser, inspect invalid inputs and arithmetic before accepting a happy-path demo. For an ISR, inspect bounded work and the allowed API context. Ask for a test that would fail before the fix. Separate blocking correctness issues from optional preferences so reviews remain actionable.

**Assumptions:** Assume the reviewer has the relevant requirements and pinned target API documentation.

**Common incorrect answer:** Approving code because it compiles or because an AI review found no issues.

**Follow-up:** What evidence would justify accepting a known limitation in a learning demonstrator?

**Scoring out of 4:** 1 point each: risk categories; lifecycle trace; regression test; actionable prioritization.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q049 How do you use git bisect without misdiagnosing an intermittent fault?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Controlled experimentation over source history.

**Spoken answer:** Define a reliable good/bad test, identify known boundary revisions, and bisect while controlling environment. Mark untestable commits explicitly rather than labeling them good.

**Deeper explanation:** An intermittent failure needs repeated trials or a statistically justified classification rule; one clean run is insufficient. Preserve failing seeds, configuration, and logs. A commit may expose an older latent bug, so the first bad revision is evidence about behavior, not automatically proof of root cause. Build failures can require a skip or a separately documented compatibility fix.

**Assumptions:** Assume the regression is reproducible enough to classify revisions under the chosen test.

**Common incorrect answer:** Treating the first revision found as proof that every line in its patch is wrong.

**Follow-up:** How would you handle a bisect step that cannot build with the current host toolchain?

**Scoring out of 4:** 1 point each: classifier; environment; intermittent handling; exposure versus root cause.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

### Q050 What do compiler warnings, static analysis, and sanitizers each contribute?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Understanding complementary verification tools and their limits.

**Spoken answer:** Warnings catch many suspicious constructs, static analysis reasons about paths without normal execution, and sanitizers instrument executed paths to detect selected runtime violations.

**Deeper explanation:** Use strict warnings for code you own, inspect static findings rather than suppressing them wholesale, and run meaningful tests under supported sanitizers. AddressSanitizer and ThreadSanitizer are normally separate builds; target/runtime support matters. A clean run does not prove all paths or all races are safe. Record exact compiler, flags, test inputs, and exclusions so the evidence is reproducible.

**Assumptions:** Assume tool support is confirmed for the selected host and target; do not infer MCU support from host success.

**Common incorrect answer:** Claiming a sanitizer proves a program memory-safe or treating every analyzer warning as a confirmed bug.

**Follow-up:** How would you design input generation to exercise a parser beyond its normal examples?

**Scoring out of 4:** 1 point each: tool roles; separate builds/support; coverage limitation; recorded evidence.

**Learning connection:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [LLVM](https://clang.llvm.org/docs/AddressSanitizer.html).

## Linux process and I O fundamentals

### Q051 How do a process, a thread, and a file descriptor differ?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Basic Linux resource and execution models.

**Spoken answer:** A process provides a resource context and address space; threads execute within it and share many resources. A file descriptor is a per-process integer handle to an open file description.

**Deeper explanation:** Duplicated descriptors can refer to the same open file description and therefore share offset or status flags. Threads generally share the descriptor table, so one thread closing a descriptor can affect another and lead to descriptor reuse races. A process boundary can isolate memory faults but introduces IPC and lifecycle complexity. Do not equate a descriptor number with permanent object identity.

**Assumptions:** Assume conventional Linux processes and POSIX threads; clone flags can construct other sharing arrangements.

**Common incorrect answer:** Thinking every thread has an independent descriptor table or that descriptor 5 always names one device.

**Follow-up:** How can close followed by open in another thread create a subtle reuse bug?

**Scoring out of 4:** 1 point each: process; thread sharing; open description; descriptor reuse consequence.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q052 Why must a read or write loop handle partial progress?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Correct byte-stream I/O and error semantics.

**Spoken answer:** A successful read or write may transfer fewer bytes than requested. Track progress, handle interruptions and nonblocking conditions, and treat EOF according to the operation's contract.

**Deeper explanation:** For writes, advance the pointer only by the positive byte count returned. Retry EINTR according to documented semantics, wait for readiness on EAGAIN when appropriate, and do not spin forever on no progress. Reads may split one protocol frame across calls or combine multiple frames. A negative return must be checked before converting to an unsigned length.

**Assumptions:** Assume POSIX byte-stream descriptors; datagram semantics and special devices need separate treatment.

**Common incorrect answer:** Assuming one write corresponds to one read or discarding the unwritten suffix.

**Follow-up:** What timeout should cover the whole operation instead of restarting after every short transfer?

**Scoring out of 4:** 1 point each: partial progress; errors; stream framing; absolute deadline.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q053 What is the difference between blocking mode and readiness notification?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Avoiding event-loop stalls and race assumptions.

**Spoken answer:** Blocking mode controls what an I/O operation does when it cannot progress. Readiness notification reports that an operation may progress; it does not reserve data for your thread.

**Deeper explanation:** Another consumer can drain a descriptor after poll reports it ready. Use nonblocking descriptors in multiplexed loops and handle EAGAIN even after readiness. A readable stream can signal EOF, not just payload. Error and hangup flags may coexist with readable buffered data, so drain according to the device contract before final closure. Readiness is not equivalent to a complete application message.

**Assumptions:** Assume POSIX poll-style readiness on Linux and potentially concurrent consumers.

**Common incorrect answer:** Calling a blocking read for a full expected message after one readiness event.

**Follow-up:** How should the loop handle a socket that is readable because its peer closed cleanly?

**Scoring out of 4:** 1 point each: mode versus event; race; EOF; message-boundary distinction.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q054 When should you choose poll instead of epoll, or epoll instead of poll?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Scale-sensitive design without premature complexity.

**Spoken answer:** Poll is straightforward for a small descriptor set. Epoll maintains an interest set and scales differently for many mostly idle descriptors, but introduces registration and event-lifecycle details.

**Deeper explanation:** Choose from measured workload, portability, and complexity. Level-triggered epoll is easier to reason about initially; edge-triggered mode normally requires nonblocking I/O and draining until EAGAIN. A large number of events still requires work regardless of the API. Handle descriptor closure and object lifetime carefully, because an event can outlive application metadata if teardown is poorly designed.

**Assumptions:** Assume Linux for epoll; regular files and device implementations have readiness-specific limitations.

**Common incorrect answer:** Saying epoll is always faster or edge-triggered mode automatically provides one event per message.

**Follow-up:** What would you measure to justify migrating a 12-descriptor daemon from poll?

**Scoring out of 4:** 1 point each: tradeoff; workload; edge-trigger drain; lifecycle risk.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q055 How should a daemon shut down cleanly after SIGTERM?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Signal safety and coordinated resource lifetime.

**Spoken answer:** Convert the signal into normal control flow, stop accepting work, notify blocked workers, drain or discard by policy, join them, then release shared resources.

**Deeper explanation:** A minimal signal handler can set a `volatile sig_atomic_t` flag or write to a suitable self-pipe using permitted operations. Linux signalfd with a correctly managed signal mask is another design. Avoid printf, mutex locking, or general allocator calls in a handler. A shutdown deadline prevents a stuck worker from hanging service termination forever, but forced termination must acknowledge possible data loss.

**Assumptions:** Assume documented POSIX async-signal-safety rules; the flag alone may not wake a blocked poll.

**Common incorrect answer:** Calling complex cleanup directly inside the signal handler or freeing state before workers exit.

**Follow-up:** How would you guarantee that a worker blocked on a condition variable notices shutdown?

**Scoring out of 4:** 1 point each: safe notification; blocked-worker wake; join-before-free; deadline policy.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q056 What are /proc, /sys, and /dev used for?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Kernel interfaces and choosing a stable observation method.

**Spoken answer:** Procfs exposes process and other kernel information, sysfs exposes device-model attributes, and device nodes under /dev provide entry points to device operations.

**Deeper explanation:** Treat each file as an interface with its own documented format rather than a normal disk file. A process can exit while its `/proc/PID` data is read, and files can change between reads. A sysfs attribute generally has a narrow representation; a character device can support a stream or control ABI. Prefer an established interface and document which fields your tool consumes.

**Assumptions:** Assume Linux and mounted virtual filesystems; permissions and namespaces affect visible data.

**Common incorrect answer:** Treating every virtual file as seekable, static, or safe to parse with fixed column assumptions.

**Follow-up:** Why is parsing `/proc/PID/stat` by simply splitting on spaces unsafe for the command field?

**Scoring out of 4:** 1 point each: three roles; dynamic data; per-interface contract; robust parsing example.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q057 How do fork and exec interact with descriptors and memory?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Process creation and deliberate inheritance.

**Spoken answer:** Fork creates a child with logically copied process state, commonly using copy-on-write memory. Exec replaces the process image while preserving selected state, including descriptors not marked close-on-exec.

**Deeper explanation:** Set close-on-exec atomically during descriptor creation where supported to avoid races in multithreaded programs. After fork in a multithreaded process, only the calling thread remains in the child, while copied locks may reflect vanished owners; follow restricted operations until exec. Use `waitpid` or another deliberate reaping strategy so child exits do not accumulate zombies.

**Assumptions:** Assume POSIX/Linux semantics; posix_spawn may simplify some launch cases.

**Common incorrect answer:** Believing exec creates a second process or assuming all descriptors close automatically.

**Follow-up:** Why can logging with a library mutex in the post-fork child deadlock?

**Scoring out of 4:** 1 point each: fork/exec distinction; inheritance; multithreaded caveat; reaping.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q058 What does fsync add beyond a successful write?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Durability and failure-aware persistence.

**Spoken answer:** A successful write usually means data was accepted by the kernel, not necessarily made durable. Fsync requests persistence for the file under the filesystem and device's guarantees.

**Deeper explanation:** For replacement of a configuration file, write a temporary file in the same filesystem, check writes, fsync the file, rename it into place, then fsync the containing directory when durability of the name change matters. Atomic rename and power-loss durability are different properties. Validate behavior on the actual filesystem and storage stack; hardware caches and failures can affect the guarantee.

**Assumptions:** Assume a filesystem supporting the operations; exact crash guarantees are target-specific.

**Common incorrect answer:** Calling rename alone a universal power-loss-safe transaction or ignoring writeback errors.

**Follow-up:** How would you test interrupted configuration updates without damaging real user data?

**Scoring out of 4:** 1 point each: acceptance versus durability; file sync; rename/directory; target validation.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q059 Why should timeouts normally use a monotonic clock?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Deadline correctness under wall-clock adjustments.

**Spoken answer:** A monotonic clock is intended for measuring elapsed time without civil-time jumps. Use a single deadline and recompute remaining time after interruptions or partial progress.

**Deeper explanation:** A wall clock may step when synchronized or manually adjusted, causing a timeout to expire early or late. Clock choice also determines whether suspend time is counted; Linux CLOCK_BOOTTIME and CLOCK_MONOTONIC differ in that respect. Convert units carefully and clamp expired deadlines to zero. Repeated relative sleeps accumulate work and scheduling delays, so periodic tasks benefit from absolute deadlines.

**Assumptions:** Assume the selected API supports the chosen clock; verify condition-variable clock configuration separately.

**Common incorrect answer:** Restarting a full timeout after every EINTR or assuming all monotonic-like clocks include suspend.

**Follow-up:** How would you define whether a command timeout should elapse while a laptop is suspended?

**Scoring out of 4:** 1 point each: elapsed-time clock; absolute deadline; suspend semantics; conversion/expiry.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

### Q060 What does least privilege mean for an embedded Linux service?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**Assesses:** Reducing the consequences of parser or network failures.

**Spoken answer:** Run with only the identity, device access, filesystem access, and capabilities required for the service's job. Separate privileged setup from ongoing processing when practical.

**Deeper explanation:** A serial telemetry service may need a specific device group and writable state directory, not unrestricted root. Service-manager restrictions and namespaces can reduce exposure, but must be tested against actual I/O and recovery behavior. Opening access by chmod 777 or globally disabling protections hides the permission model. Log actionable denial errors without exposing credentials or secret payloads.

**Assumptions:** Assume a defined deployment environment; capabilities and sandbox settings are Linux-specific and version-sensitive.

**Common incorrect answer:** Using root as a permanent fix for any device-permission failure.

**Follow-up:** How would you verify that an update helper has narrowly scoped authority?

**Scoring out of 4:** 1 point each: required privileges; concrete reduction; tested restrictions; operational diagnostics.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [EPOLL](https://man7.org/linux/man-pages/man7/epoll.7.html), [SIGNAL](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html).

## Linux coding exercises

### Q061 Write a complete-write helper for a blocking descriptor with EINTR handling.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Progress tracking and syscall error handling.

**Spoken answer:** Loop until all bytes are written, advancing by each positive result. Retry EINTR, return a clear error for other failures, and reject a zero-progress write to prevent an infinite loop.

**Deeper explanation:** The reference `write_all_blocking` returns zero on success and -1 with errno on failure. Its contract excludes nonblocking descriptors and leaves timeout/cancellation to a higher layer. Test through a pipe with a reading peer; a large payload may produce partial progress. Preserve the original buffer and requested length for diagnostics rather than overwriting them with a syscall result.

**Assumptions:** Assume length is representable for each write call and the caller handles SIGPIPE policy.

**Common incorrect answer:** Retrying from the original buffer after a short write and duplicating the prefix.

**Follow-up:** How would you add cancellation and an absolute deadline for a nonblocking socket?

**Scoring out of 4:** 1 point each: suffix progress; EINTR; zero-progress/error; explicit blocking contract.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q062 Read a text file whose length is unknown without trusting stat size.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Dynamic input handling and growth limits.

**Spoken answer:** Read chunks until EOF, grow a buffer with overflow checks, and impose a maximum accepted size. Reserve space for a terminator only if the result is intended as text.

**Deeper explanation:** Procfs files may report an unhelpful size, so their contents must be read rather than allocated solely from stat. Handle EINTR and preserve the original allocation if growth fails. The exercise contract caps input at 64 KiB and rejects embedded NUL when parsing text. Tests should include empty input, exact cap, over-cap, and short reads through a pipe.

**Assumptions:** Assume a blocking descriptor and a caller-selected maximum; binary input requires a different parsing policy.

**Common incorrect answer:** Using one read sized from stat and assuming the returned data is complete and NUL-terminated.

**Follow-up:** How would you distinguish allocation failure from exceeding the configured maximum?

**Scoring out of 4:** 1 point each: EOF loop; bounded growth; realloc safety; dynamic-file cases.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q063 Build a poll loop that reads a pipe and exits when a control pipe signals shutdown.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Multiplexing, readiness, and shutdown ownership.

**Spoken answer:** Register both descriptors, process all returned flags, read available bytes, and leave the loop when the control channel requests shutdown or closes by policy.

**Deeper explanation:** Use nonblocking descriptors to avoid races after readiness. Handle EINTR by retrying with the remaining deadline, and handle data-descriptor hangup after draining buffered bytes. Keep shutdown notification separate from payload framing. Tests write payload in fragments, then send one control byte; another test closes the payload writer. Ensure descriptors are closed exactly once by their owner after the loop exits.

**Assumptions:** Assume a single loop owns these descriptors and the control byte protocol is local.

**Common incorrect answer:** Checking only POLLIN and spinning forever after POLLHUP or POLLERR.

**Follow-up:** What if the control pipe fills before a shutdown request is written?

**Scoring out of 4:** 1 point each: both sources; flag handling; nonblocking reads; ownership and wake failure.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q064 Implement a bounded newline decoder for fragmented stream input.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Streaming parser state and overflow recovery.

**Spoken answer:** Append bytes until newline, emit a complete line, and retain a partial line across reads. When capacity is exceeded, enter discard-until-newline mode and report one overlong record.

**Deeper explanation:** The decoder must handle `"ab"` then `"c\nx\n"` as two lines, `abc` and `x`. Define whether CRLF is normalized and whether empty lines are allowed. Do not assume each read contains a whole line. Once overflow occurs, consuming to a delimiter restores framing; resetting immediately on every byte can accidentally accept the tail of a malformed command.

**Assumptions:** Assume a byte-oriented newline protocol with a 64-byte maximum excluding the delimiter.

**Common incorrect answer:** NUL-terminating each read and treating it as one complete command.

**Follow-up:** How would binary framing differ when the payload may legitimately contain newline?

**Scoring out of 4:** 1 point each: retained partial state; multiple lines; overlong recovery; explicit grammar.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q065 Implement a monotonic deadline helper returning milliseconds remaining.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Time arithmetic, rounding, and poll integration.

**Spoken answer:** Subtract current monotonic time from an absolute deadline, return zero if expired, and round a positive fractional millisecond upward without overflowing the API's int limit.

**Deeper explanation:** Rounding down can create an immediate busy loop just before expiry; rounding up avoids declaring time remains while repeatedly polling with zero. Clamp very distant deadlines to INT_MAX and recompute after wakeup. Store nanoseconds in a sufficiently wide representation or normalize seconds/nanoseconds carefully. Unit tests should use injected timestamps rather than sleeping, so boundary behavior is deterministic.

**Assumptions:** Assume CLOCK_MONOTONIC semantics and poll's millisecond integer timeout.

**Common incorrect answer:** Subtracting timespec fields independently without borrowing or restarting the deadline after every event.

**Follow-up:** How would you expose an infinite timeout distinctly from an expired timeout?

**Scoring out of 4:** 1 point each: absolute subtraction; upward rounding; clamping; deterministic tests.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q066 Write a subprocess launcher that captures exit status without leaking descriptors.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Process lifecycle and error-channel design.

**Spoken answer:** Create needed pipes with close-on-exec, fork or use posix_spawn, close unused ends in each process, execute the child, and reap it with EINTR-aware waitpid handling.

**Deeper explanation:** Distinguish normal exit from signal termination with the wait-status macros. An exec failure should be communicated separately from the child's eventual application exit code, for example through a close-on-exec error pipe. For multithreaded parents, restrict child-side operations before exec or prefer posix_spawn. Test missing executable, exit zero, exit seven, and signal termination using controlled local commands.

**Assumptions:** Assume trusted executable paths and arguments passed as an argv vector, not concatenated shell text.

**Common incorrect answer:** Passing untrusted arguments through a shell or interpreting raw wait status as the exit code.

**Follow-up:** How would you enforce a subprocess timeout and avoid orphaning grandchildren?

**Scoring out of 4:** 1 point each: descriptor ends; exec failure; status macros; reaping and trusted arguments.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q067 Write a TCP request parser that accepts a 16-bit length followed by payload.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Message framing over a stream and memory limits.

**Spoken answer:** Maintain header and payload states, accumulate partial input, reject lengths above the configured maximum, and emit only after the exact declared payload has arrived.

**Deeper explanation:** Zero-length messages need a deliberate policy. One recv may contain part of a header, a whole message, or several messages, so return consumed-byte counts and continue decoding. A disconnect mid-payload is a truncated-message error. Pair a total frame deadline with a maximum size to prevent a peer from holding memory indefinitely by sending slowly. Exercise every possible split of a small valid frame.

**Assumptions:** Assume network-order length, maximum payload 1024 bytes, and a byte-stream socket.

**Common incorrect answer:** Allocating directly from an unchecked length or equating a recv call with one request.

**Follow-up:** How do you prevent queued complete messages from exhausting memory when the consumer is slow?

**Scoring out of 4:** 1 point each: parser states; size cap; split/coalesced frames; deadline/backpressure.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q068 Implement atomic replacement of a small configuration file with error checking.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Persistence sequencing and recovery from partial failure.

**Spoken answer:** Create a unique temporary file in the destination directory, write the complete validated content, sync it, rename it over the destination, and sync the directory when required.

**Deeper explanation:** Check every operation and clean up the temporary path on pre-rename failures. Preserve the old configuration until replacement succeeds. Set ownership and permissions deliberately; avoid predictable temporary names and symlink races. Failure after rename may mean the new version is visible but durability is uncertain, so report that state rather than pretending nothing changed. Test with injected failure at each stage in a disposable directory.

**Assumptions:** Assume local filesystem support for the chosen operations and a defined crash-consistency contract.

**Common incorrect answer:** Writing directly into the live file or treating an unchecked fflush as durable storage.

**Follow-up:** How would you handle concurrent writers so a stale update does not overwrite a newer configuration?

**Scoring out of 4:** 1 point each: sequence; secure temp; failure states; concurrency/version consideration.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q069 Implement a bounded producer-consumer queue with clean shutdown.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Condition-variable predicates and lifetime-safe concurrency.

**Spoken answer:** Protect queue state with a mutex; wait in predicate loops for space or data; publish state before notification; and include a shutdown flag in every blocking predicate.

**Deeper explanation:** Define whether shutdown drains queued items or discards them. Broadcast to wake both producer and consumer waiters, then join all threads before destroying synchronization objects. Spurious wakeups require rechecking conditions. A test should stop while empty, stop while full, run multiple producers, and verify each accepted item is consumed once under the chosen drain policy.

**Assumptions:** Assume POSIX threads and a fixed-capacity queue; cancellation behavior is explicitly out of scope unless implemented.

**Common incorrect answer:** Using if instead of while around condition waits or destroying a mutex while a worker can still access it.

**Follow-up:** How would you report that a producer's item was rejected because shutdown began?

**Scoring out of 4:** 1 point each: protected predicates; loops; shutdown policy; join-before-destroy.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q070 Parse a /proc PID stat record robustly enough to extract state and PID.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Parsing a kernel text interface with nontrivial delimiters.

**Spoken answer:** Parse the numeric PID before the opening parenthesis, locate the command field's closing delimiter under the documented format, then parse the following state field with bounds checks.

**Deeper explanation:** The command field may contain spaces and parentheses, so a naive whitespace split is invalid. For this exercise, validate the trailing `) state ` layout and reject malformed records. Include fixtures with `worker name`, a command containing `)`, truncated data, and PID overflow. Reading `/proc` is racy: a missing process is an expected operational outcome, not necessarily a program defect.

**Assumptions:** Assume Linux proc_pid_stat format; extraction requirements are deliberately limited to PID and state.

**Common incorrect answer:** Assuming the command is always a single token or assigning a failure to PID zero silently.

**Follow-up:** How would you avoid accidentally associating observations from a reused PID with the old process?

**Scoring out of 4:** 1 point each: delimiter awareness; numeric bounds; malformed cases; process-lifetime race.

**Learning connection:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

## Concurrency and IPC

### Q071 Why must a condition variable be paired with a predicate and mutex?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Lost-wakeup prevention and state-based waiting.

**Spoken answer:** The condition variable is a notification mechanism; shared state is the truth. Protect the predicate with a mutex and wait in a loop that rechecks it after waking.

**Deeper explanation:** The wait operation releases the mutex and blocks as one coordinated operation, then reacquires it before returning. This avoids a gap in which a producer changes state and sends a notification just before the consumer actually sleeps. Spurious wakeups and competing consumers still require a loop. Update the predicate while holding its lock, then signal or broadcast according to who may now proceed.

**Assumptions:** Assume POSIX condition variables and consistent use of the same mutex for the predicate.

**Common incorrect answer:** Treating a signal as a stored event token that a later waiter is guaranteed to consume.

**Follow-up:** When should shutdown broadcast rather than signal one waiter?

**Scoring out of 4:** 1 point each: predicate; atomic wait transition; while loop; correct notification scope.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q072 How does deadlock differ from starvation and livelock?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Classifying lack of progress and selecting evidence.

**Spoken answer:** Deadlock is a cycle of waits that cannot resolve internally. Starvation denies one participant progress while others run. Livelock performs activity without useful completion.

**Deeper explanation:** Two threads acquiring A then B and B then A can deadlock. A low-priority task may starve under continuous higher-priority work. Two peers repeatedly backing off in synchrony can livelock. Capture stacks, ownership, scheduling traces, and progress counters to distinguish them. A timeout may restore service but does not automatically eliminate the underlying resource-order or fairness defect.

**Assumptions:** Assume a defined notion of useful progress and observable task state.

**Common incorrect answer:** Calling every hung application a deadlock or using sleep calls as a permanent locking fix.

**Follow-up:** How would a global lock ordering prevent the two-lock example?

**Scoring out of 4:** 1 point each: three distinctions; concrete examples; diagnostic evidence; structural remedy.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q073 When is an atomic counter insufficient to protect a data structure?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Atomicity versus compound invariants.

**Spoken answer:** An atomic counter protects that counter's operations, not an invariant involving several fields or an object's lifetime. Choose synchronization covering the complete state transition.

**Deeper explanation:** A queue's head, tail, slot contents, and storage lifetime must agree. Publishing a new head before the item is visible can let a consumer read uninitialized data. Acquire-release may support a carefully designed single-producer single-consumer queue, but does not make an arbitrary multi-producer design correct. A mutex is often simpler when the operation spans several related fields.

**Assumptions:** Assume the C memory model for user space; Linux kernel atomics have their own documented model.

**Common incorrect answer:** Replacing every shared integer with an atomic and declaring the whole algorithm lock-free and correct.

**Follow-up:** What linearization point would you choose for a successful queue push?

**Scoring out of 4:** 1 point each: invariant scope; publication; producer assumptions; simpler alternative.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q074 What is priority inversion, and what does priority inheritance solve?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Scheduling interactions through shared resources.

**Spoken answer:** A high-priority task can wait for a lower-priority lock owner while unrelated medium-priority work delays that owner. Priority inheritance temporarily raises the owner's effective priority.

**Deeper explanation:** Inheritance reduces this specific scheduling interference; it does not shorten the critical section, prevent deadlock, or bound arbitrary I/O performed while holding the lock. Multiple locks and nested dependencies need careful analysis. On Linux, use documented priority-inheritance primitives when required; on an RTOS, inspect its actual implementation and restrictions. Keep shared critical sections short and avoid blocking operations inside them when deadlines matter.

**Assumptions:** Assume fixed-priority scheduling for the illustrative high/medium/low example.

**Common incorrect answer:** Claiming priority inheritance guarantees no blocking or makes a poor lock hierarchy safe.

**Follow-up:** What would you measure to separate inversion from an intrinsically long critical section?

**Scoring out of 4:** 1 point each: three-task mechanism; temporary boost; limits; measurement.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q075 How should shared memory between processes be synchronized?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Cross-process lifetime, initialization, and publication.

**Spoken answer:** Define a binary layout, initialize it exactly once, and use synchronization explicitly supported for interprocess sharing. Ordinary in-process assumptions do not automatically apply.

**Deeper explanation:** POSIX process-shared mutexes require appropriate attributes and placement in shared storage. Robust mutexes can report owner death, but the next owner must repair or reject inconsistent data before declaring the state usable. Include version, size, and initialization state in the shared ABI. A process crash can leave a half-updated record even though shared memory itself persists.

**Assumptions:** Assume a Linux/POSIX implementation supporting the selected process-shared or robust primitive.

**Common incorrect answer:** Placing a default mutex in shared memory and assuming it works correctly across processes.

**Follow-up:** How would you recover if a writer dies halfway through updating a multi-field record?

**Scoring out of 4:** 1 point each: shared attributes; initialization; owner-death recovery; versioned layout.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q076 What is backpressure, and where should it appear in telemetry systems?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Bounded resource usage under overload.

**Spoken answer:** Backpressure makes producers slow, reject, or adapt when consumers cannot keep up. Every queue needs an explicit bound and overload policy.

**Deeper explanation:** For critical alarms, dropping silently may be unacceptable; for high-rate trend samples, coalescing or dropping oldest data may be appropriate. A serial input cannot always be paused, so count losses and reserve capacity for important events. Applying backpressure only at the final network queue can still let earlier queues grow without bound. Test sustained overload, not just short bursts.

**Assumptions:** Assume requirements distinguish command, alarm, and best-effort telemetry semantics.

**Common incorrect answer:** Using an unbounded queue as the solution to a slow consumer.

**Follow-up:** How would you expose overload in health metrics without producing even more unbounded logs?

**Scoring out of 4:** 1 point each: bounded queues; chosen policy; end-to-end path; observable loss.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q077 Why is cancellation harder than adding a stop flag?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Interrupting waits and coordinating object lifetime.

**Spoken answer:** A flag expresses intent but does not wake blocked I/O, condition waits, or sleeping threads. Cancellation must reach each blocking point and define ownership of unfinished work.

**Deeper explanation:** Use a wake descriptor, condition broadcast, timeout, or API-specific cancellation mechanism. Define who completes a request when stop races with normal completion. Join or otherwise establish quiescence before freeing shared context. A stop flag must itself be synchronized in a multithreaded C program. Tests should trigger shutdown while empty, full, reconnecting, and processing a partial message.

**Assumptions:** Assume cooperative cancellation; asynchronous thread cancellation has additional cleanup hazards.

**Common incorrect answer:** Setting a volatile boolean and immediately freeing the worker's context.

**Follow-up:** How would you guarantee exactly one completion callback for a request canceled at the same time it succeeds?

**Scoring out of 4:** 1 point each: wake paths; synchronized state; completion race; lifetime barrier.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q078 What is false sharing, and how would you establish that it matters?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Cache effects versus correctness failures.

**Spoken answer:** False sharing occurs when independent writable objects occupy a cache line that moves between cores. It can reduce performance despite logically independent accesses.

**Deeper explanation:** Separate per-thread hot counters or redesign aggregation after measuring cache-coherence behavior and throughput under controlled CPU placement. Padding may help but increases memory footprint and depends on target cache-line size. Do not confuse false sharing with a data race: each thread may own its own variable correctly. A benchmark in a noisy virtual machine may not represent the embedded target's memory hierarchy.

**Assumptions:** Assume a coherent multicore system and a workload with frequent writes.

**Common incorrect answer:** Adding arbitrary padding everywhere before measuring or calling false sharing undefined behavior.

**Follow-up:** How would you compare padded and unpadded layouts without changing unrelated benchmark conditions?

**Scoring out of 4:** 1 point each: cache-line mechanism; correctness distinction; measurement; target-aware remedy.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q079 What does lock-free mean, and what does it not guarantee?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Progress guarantees and realistic use of atomics.

**Spoken answer:** Lock-free algorithms guarantee system-wide progress under their formal assumptions; they do not guarantee every thread completes promptly. Wait-free is a stronger per-operation progress property.

**Deeper explanation:** An atomic variable alone does not establish an algorithm's progress guarantee. Compare-and-swap loops may starve one participant, and memory reclamation can be the hardest part. On a platform, a language atomic type may internally use a lock unless lock-free support is confirmed. For small embedded queues, a clear mutex design may outperform a complicated atomic design in maintainability and predictable behavior.

**Assumptions:** Assume formal progress terms are used with the required scheduler and atomic-operation assumptions.

**Common incorrect answer:** Equating lock-free with faster, bounded latency, or simply no explicit mutex in the source.

**Follow-up:** How would you reclaim a node while another thread may still hold its address?

**Scoring out of 4:** 1 point each: system progress; starvation distinction; implementation support; reclamation concern.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

### Q080 When would you choose a pipe, Unix socket, shared memory, or message queue?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Selecting IPC from semantics instead of preference.

**Spoken answer:** Choose by message boundaries, transfer volume, topology, permissions, failure handling, and lifecycle. Pipes suit simple streams; Unix sockets support richer local communication; shared memory needs explicit coordination.

**Deeper explanation:** A local command service can use a Unix-domain socket with bounded framed messages and peer credentials. A high-volume shared-memory ring can reduce copying but adds initialization, synchronization, and crash-recovery complexity. Message queues may preserve records but impose size and capacity constraints. Measure before optimizing copies, and define behavior when a peer exits or restarts.

**Assumptions:** Assume local Linux processes; portability requirements may narrow the available APIs.

**Common incorrect answer:** Selecting shared memory automatically because it is presumed fastest without considering recovery and ownership.

**Follow-up:** How would you version messages so independently updated peers can reject incompatible requests safely?

**Scoring out of 4:** 1 point each: selection factors; concrete choice; failure/restart; versioning.

**Learning connection:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [FUTEX](https://man7.org/linux/man-pages/man7/futex.7.html), [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).

## Linux debugging scenarios

### Q081 A daemon uses 100 percent CPU after its serial peer disconnects. What do you inspect?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Evidence-led diagnosis of an event-loop spin.

**Spoken answer:** Capture a short syscall trace and loop counters. Look for repeated readiness or hangup returns followed by zero-byte reads, unhandled errors, or a retry path with no wait.

**Deeper explanation:** The provided `spin.trace` fixture repeatedly shows poll returning POLLHUP and read returning zero. That points to EOF/hangup handling, not an expensive computation. Close or transition the connection into a bounded reconnect state after draining any valid buffered data. Verify the fix with disconnect, reconnect, and a silent peer, while measuring CPU over an agreed interval.

**Assumptions:** Assume the fixture is illustrative teaching data; actual devices may report different error combinations.

**Common incorrect answer:** Adding an arbitrary sleep without explaining why the loop remains active.

**Follow-up:** How would you avoid a new busy loop if reconnect itself fails immediately?

**Scoring out of 4:** 1 point each: trace hypothesis; EOF interpretation; state transition; regression/CPU check.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q082 A parser passes whole-frame tests but fails on real UART traffic. What is likely missing?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Transport-independent framing and fragmentation tests.

**Spoken answer:** UART supplies a byte stream, so frames may be split or combined across reads. Inspect retained parser state, length checks, and recovery after malformed bytes.

**Deeper explanation:** Replay a known frame through every split point, then concatenate two frames and inject junk between them. The provided `fragments.json` includes a header split across reads and a truncated declared payload. Ensure the parser consumes bytes monotonically and has a bounded resynchronization strategy. Real electrical errors remain a separate validation concern even after host fragmentation tests pass.

**Assumptions:** Assume baud rate and framing configuration are otherwise correct; verify those rather than presuming them.

**Common incorrect answer:** Increasing the read buffer until one read usually contains a frame.

**Follow-up:** How would a partial frame time out without discarding a valid following frame?

**Scoring out of 4:** 1 point each: stream model; exhaustive splits; malformed recovery; timeout/electrical separation.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q083 A process reports ENOENT when executing a file that visibly exists. How can that happen?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** ELF interpreter and script-launch dependencies.

**Spoken answer:** The missing object may be the executable's interpreter rather than the file itself. Inspect the ELF program headers or script shebang and the target filesystem.

**Deeper explanation:** A dynamically linked ELF can name a loader absent from a minimal root filesystem. A script can reference an unavailable interpreter or contain a malformed shebang with an unintended carriage return. Compare `file`, `readelf -l`, architecture, and interpreter path using the exact deployed binary. Do not treat chmod as the universal fix; permission failures have different evidence.

**Assumptions:** Assume Linux exec behavior and a trusted local binary under inspection.

**Common incorrect answer:** Recreating the file repeatedly or claiming ENOENT proves the pathname lookup alone failed.

**Follow-up:** How would a static binary change the deployment requirements, and what would it not solve?

**Scoring out of 4:** 1 point each: interpreter cause; inspection commands; architecture/rootfs; error distinction.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q084 A service works as root but fails under its intended account. How do you fix it?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Permission analysis without weakening the entire system.

**Spoken answer:** Identify the exact failing operation and errno, then compare identity, groups, device-node permissions, directory traversal rights, and service sandbox settings.

**Deeper explanation:** Use a controlled trace or structured error log to distinguish opening `/dev/ttyX` from writing the state directory. Grant the narrow device or directory access actually required and ensure the service sees supplementary-group changes. If a systemd restriction blocks an operation, modify only the relevant policy and retest. Preserve the intended account and record why each privilege is needed.

**Assumptions:** Assume the target uses documented Linux permissions and possibly a service manager.

**Common incorrect answer:** Running permanently as root or setting device nodes world-writable to make the test pass.

**Follow-up:** How would a udev rule make the device permission persistent across reboot and reconnect?

**Scoring out of 4:** 1 point each: failing syscall; identity/path checks; narrow fix; persistence test.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q085 Memory usage grows slowly while the process stays responsive. How do you separate a leak from caching?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Resource accounting and experiment design.

**Spoken answer:** Measure memory over a repeatable workload, distinguish live allocations from retained allocator arenas or intentional caches, and track object counts and ownership paths.

**Deeper explanation:** Run repeated connect-disconnect or request cycles, then observe whether live application objects return to baseline. A heap profiler or sanitizer can identify leaks in exercised paths, while RSS alone cannot prove them. Check unbounded queues and log buffers as well as missing free calls. Set explicit cache limits and eviction policies; a designed cache can still violate a memory budget.

**Assumptions:** Assume host tooling is supported and the workload can be replayed with stable input volume.

**Common incorrect answer:** Declaring a leak from one rising RSS sample or calling all retained memory harmless caching.

**Follow-up:** What evidence would show that cancellation paths leak request objects?

**Scoring out of 4:** 1 point each: repeatable workload; live-versus-resident distinction; ownership counts; bounded policy.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q086 A multithreaded application hangs only during shutdown. What is your first investigation?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Wait dependencies and destruction ordering.

**Spoken answer:** Capture all thread stacks and the shared shutdown state. Look for a worker blocked on a predicate that never includes shutdown, an unwoken wait, or a join holding a needed lock.

**Deeper explanation:** A common failure is the main thread holding the queue mutex while joining a worker that needs that mutex to exit. Another is signaling one waiter while several remain asleep. Draw a wait-for relationship from evidence, then repair wakeup and ownership order. Test shutdown from empty, full, processing, and error states rather than relying on a normal-exit demo.

**Assumptions:** Assume cooperative shutdown and a reproducible or captured hang.

**Common incorrect answer:** Detaching all threads to hide the hang while their shared memory is freed.

**Follow-up:** How would you make a shutdown test deterministic instead of using arbitrary sleeps?

**Scoring out of 4:** 1 point each: thread stacks; wait graph; join/lock ordering; state-based regression.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q087 A network request sometimes contains duplicated bytes. What write-loop bug would you check?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Partial-write bookkeeping and reproducible transport tests.

**Spoken answer:** Check whether the loop advances its pointer and remaining count after each positive write. Retrying the entire buffer after a short write duplicates the already accepted prefix.

**Deeper explanation:** Instrument requested length, returned count, and cumulative offset without logging sensitive payloads. Use an injected writer that deliberately returns small counts and EINTR to make the bug deterministic. Distinguish this from application-level retries after an uncertain acknowledgment, which require request IDs and idempotency. One is byte-stream bookkeeping; the other is delivery semantics across a reconnect.

**Assumptions:** Assume the receiver's parser is independently tested and transport ordering is preserved.

**Common incorrect answer:** Blaming TCP retransmissions for duplicate bytes delivered to one reliable stream.

**Follow-up:** How would you safely retry a command when the connection drops after the server may have applied it?

**Scoring out of 4:** 1 point each: partial offset; injected writes; transport distinction; idempotency.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q088 A periodic task drifts farther behind each minute. What timing pattern is suspect?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Periodic scheduling with absolute versus relative deadlines.

**Spoken answer:** A loop that does work and then sleeps a fixed period adds its work and scheduling delay to every cycle. Schedule against successive absolute deadlines instead.

**Deeper explanation:** Record intended wake time, actual wake time, execution duration, and missed-deadline count separately. Decide whether an overrun skips missed releases, catches up, or enters a degraded state; blindly executing many overdue cycles can worsen overload. Use a monotonic clock and appropriate absolute-sleep APIs. Averages alone can hide rare deadline misses that matter more than small steady drift.

**Assumptions:** Assume the period is an application requirement and clock suspend semantics are defined.

**Common incorrect answer:** Reducing the sleep duration by one observed average work time and assuming drift is solved.

**Follow-up:** What policy would you choose if one cycle takes three times the nominal period?

**Scoring out of 4:** 1 point each: relative-drift mechanism; absolute schedule; overrun policy; latency measurements.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q089 A cross-compiled program crashes on one board but passes on the host. What do you compare?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Architecture-sensitive faults and environment differences.

**Spoken answer:** Compare architecture, ABI, endianness, alignment assumptions, integer widths, libraries, and inputs. Reproduce with the exact target binary and capture a backtrace or core when possible.

**Deeper explanation:** A parser that casts bytes to a structure may tolerate unaligned access on one host and fault or behave differently elsewhere. A missing synchronization barrier may appear only under a different memory model. Use compiler warnings, sanitizers where supported, and portable byte decoding to isolate assumptions. Host success validates host behavior, not board timing or peripheral correctness.

**Assumptions:** Assume the target executable and debug symbols correspond to the same build.

**Common incorrect answer:** Rebuilding with optimization disabled and calling the problem fixed without understanding the cause.

**Follow-up:** How would you verify that gdbserver and the debugger agree on the target's symbols and architecture?

**Scoring out of 4:** 1 point each: environment comparison; concrete portability bug; matching symbols; validation limits.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

### Q090 A configuration file becomes empty after power loss. What is wrong with a direct overwrite?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Crash-consistent updates and evidence-based persistence.

**Spoken answer:** Truncating the live file before writing exposes an empty or partial version if power fails. Use a validated temporary file, syncing and atomic replacement under a tested filesystem contract.

**Deeper explanation:** The fix must handle data and directory durability, writeback errors, and permissions. Keep a known-good fallback or versioned copy if the product requires recovery from corruption. Inject failures at each operation in a disposable image, then power-cut test the actual storage stack when available. Passing a host rename test is not evidence of board-level power-failure robustness.

**Assumptions:** Assume the filesystem offers the required rename and sync semantics; verify rather than generalize.

**Common incorrect answer:** Adding fflush alone or claiming atomic visibility guarantees durable persistence.

**Follow-up:** How would the application choose between two versioned configuration records after a torn write?

**Scoring out of 4:** 1 point each: truncate window; safe sequence; recovery selection; target power-cut evidence.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [READ](https://man7.org/linux/man-pages/man2/read.2.html), [WRITE](https://man7.org/linux/man-pages/man2/write.2.html), [POLL](https://man7.org/linux/man-pages/man2/poll.2.html), [FSYNC](https://man7.org/linux/man-pages/man2/fsync.2.html), [CLOCK](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), [PROC](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html).

## Concurrency and fault analysis scenarios

### Q091 A counter occasionally loses increments despite being volatile. How do you demonstrate the defect?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Data-race diagnosis and independent verification.

**Spoken answer:** Identify concurrent read-modify-write operations without synchronization. Replace the mechanism with an atomic operation or mutex, then test the required invariant under concurrent load.

**Deeper explanation:** A stress test can compare the final count with known accepted work, and ThreadSanitizer may report exercised races on a supported host. Neither a failed run nor a clean run alone defines the language semantics: the unsynchronized C accesses are already invalid. Choose relaxed atomics only if the counter is independent of other published state. Record sanitizer support and actual flags.

**Assumptions:** Assume user-space C11 threads; volatile MMIO is not the object under test.

**Common incorrect answer:** Claiming the fix is to force optimization off or make the variable wider.

**Follow-up:** What if the counter also indicates that a corresponding data buffer is ready?

**Scoring out of 4:** 1 point each: RMW race; proper primitive; invariant test; ordering qualification.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q092 A consumer sleeps although the queue contains data. What lost-wakeup pattern do you inspect?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Atomic relationship between predicate checks and sleeping.

**Spoken answer:** Check whether the consumer tests the predicate outside its mutex or releases the mutex before starting a separate wait. The state check and wait transition must use the correct condition-variable pattern.

**Deeper explanation:** A producer can enqueue and signal during the gap, leaving no later notification to wake the consumer. The fix is a mutex-protected predicate loop around pthread_cond_wait, not an extra signal placed randomly. Also inspect whether producer and consumer use different mutexes or inconsistent predicates. Build a test barrier that forces the suspect interleaving instead of hoping stress reproduces it.

**Assumptions:** Assume POSIX condition variables and shared in-process queue state.

**Common incorrect answer:** Treating condition notifications as a durable count of pending items.

**Follow-up:** How can multiple consumers turn a single if check into an empty-queue access after wakeup?

**Scoring out of 4:** 1 point each: gap identification; correct wait loop; same-lock predicate; forced interleaving.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q093 A two-thread program locks up after each thread takes a different mutex. What is the repair?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Lock-order deadlock and design-level prevention.

**Spoken answer:** Confirm the circular wait with thread stacks and lock ownership. Establish a consistent global lock order or redesign the operation so both locks are unnecessary.

**Deeper explanation:** If one path takes A then B and another B then A, both can wait forever. A try-lock-and-backoff approach needs a progress analysis and can livelock; it is not automatically better. Document the order near interfaces and test opposing operations concurrently. Avoid joining a thread or calling an unknown callback while holding a lock the other path may need.

**Assumptions:** Assume nonrecursive mutexes and no external mechanism deliberately breaking the wait.

**Common incorrect answer:** Using recursive mutexes as a cure for a cycle involving two different threads.

**Follow-up:** How would lockdep or an application lock-order assertion help catch future inversions?

**Scoring out of 4:** 1 point each: wait cycle; consistent order; callback/join risk; regression prevention.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q094 A timer callback accesses freed state after device removal. What lifetime ordering is missing?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Asynchronous activity teardown and use-after-free prevention.

**Spoken answer:** Removal must prevent new scheduling, stop or cancel the timer synchronously as appropriate, and wait for in-flight callbacks before releasing state they can access.

**Deeper explanation:** A flag alone is insufficient if the callback reads freed memory before checking it. A callback may also rearm itself, so close that path before synchronization. The exact kernel timer/work APIs and allowed calling context matter. Exercise repeated load-use-unload or bind-unbind cycles in a disposable VM with supported memory debugging, then inspect retained evidence rather than assuming devm allocation handles asynchronous activity.

**Assumptions:** Assume a Linux driver and the selected kernel's timer API contract.

**Common incorrect answer:** Freeing memory first and hoping the callback sees a stop flag.

**Follow-up:** How can calling a synchronous cancellation routine while holding a callback-needed lock deadlock?

**Scoring out of 4:** 1 point each: prevent rearm; synchronous quiescence; free-last; lock/context caveat.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q095 A driver fails with a sleeping-in-atomic-context warning. What do you inspect?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Execution context and API preconditions.

**Spoken answer:** Identify the current context and held locks, then inspect the call chain for sleeping operations such as mutex acquisition, GFP_KERNEL allocation, or faulting user copies.

**Deeper explanation:** On a conventional non-RT kernel, spinlocked and hard-IRQ paths cannot sleep. Move substantial work into an appropriate threaded context or redesign resource acquisition before the atomic section. Do not blindly substitute GFP_ATOMIC everywhere: allocation can fail and may still be unsuitable. PREEMPT_RT changes some lock semantics, so reason from the pinned configuration and API rules rather than a slogan.

**Assumptions:** Assume the warning trace is available and kernel version/configuration are known.

**Common incorrect answer:** Disabling the warning or changing one allocator flag without addressing the execution-context design.

**Follow-up:** How would you divide a hardware interrupt handler from deferred processing?

**Scoring out of 4:** 1 point each: context; sleeping call; structural move; version/config caveat.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q096 A low-priority logger causes a high-priority control task to miss deadlines. How can this occur?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Priority inversion through a shared resource.

**Spoken answer:** The control task may wait for a mutex held by the logger while medium-priority tasks prevent the logger from running. Capture ownership and scheduling history to test that hypothesis.

**Deeper explanation:** Shorten the shared critical section, avoid slow I/O under the lock, and use appropriate priority inheritance where supported. Consider transferring log records through a bounded queue so control never waits for storage. Inheritance does not fix a filesystem write that itself stalls for a long time. Measure worst observed blocking under representative interference, and state that observed maxima are not formal worst-case bounds.

**Assumptions:** Assume fixed-priority tasks and a shared lock identified in the trace.

**Common incorrect answer:** Simply raising every task to the highest priority or calling average latency a deadline guarantee.

**Follow-up:** What information must be logged to separate inversion from CPU overload?

**Scoring out of 4:** 1 point each: ownership chain; scheduling evidence; bounded redesign; measured-versus-proven bound.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q097 A device works until runtime suspend is enabled. Where do you start?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Power-state-dependent resources and access lifetimes.

**Spoken answer:** Correlate failures with suspend/resume events and inspect whether each access holds the required runtime-PM reference and whether registers, clocks, regulators, and interrupts are restored correctly.

**Deeper explanation:** A cached software state can disagree with reset hardware after resume. Ensure deferred work cannot access a powered-down device, and balance references on error paths. Test repeated idle-resume cycles, requests racing with suspend, and removal during suspended state. Disable autosuspend only as a diagnostic experiment; it does not establish the final fix. Use the selected subsystem's PM conventions.

**Assumptions:** Assume the hardware and driver advertise runtime power management support.

**Common incorrect answer:** Adding a long delay after every request without checking the device power state.

**Follow-up:** What state must be replayed after a power domain loses register contents?

**Scoring out of 4:** 1 point each: correlation; PM references; restore/quiesce; race tests.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q098 A DMA buffer contains stale data on one architecture. What could host testing have missed?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** DMA ownership, cache coherency, and address domains.

**Spoken answer:** Inspect use of the DMA API, transfer direction, map/unmap or sync transitions, and ownership between CPU and device. CPU virtual addresses are not interchangeable with DMA addresses.

**Deeper explanation:** A coherent x86 host can hide cache-maintenance bugs that appear on another target. Even coherent allocations do not remove every ordering requirement. Do not access a streaming DMA buffer from the CPU while the device owns it unless the documented synchronization protocol permits it. Check mapping errors and alignment restrictions, then validate on the actual bus/SoC with known patterns.

**Assumptions:** Assume a Linux driver using a real DMA-capable device and the selected DMA API contract.

**Common incorrect answer:** Calling cache flush functions ad hoc or passing a kmalloc pointer directly to hardware as an address.

**Follow-up:** How would an IOMMU make a physical-address assumption fail?

**Scoring out of 4:** 1 point each: ownership; API mapping; address domains; target coherency test.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q099 A firmware task resets under heavy logging but never in the debugger. What hypotheses fit?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** Timing perturbation, stack usage, and watchdog diagnosis.

**Spoken answer:** Collect reset cause, fault registers, stack high-water evidence, and watchdog timing. Heavy logging can increase stack use, block critical work, or change interrupt timing.

**Deeper explanation:** A debugger can halt watchdogs or slow execution, so its absence of failure is not decisive. Use bounded, low-overhead event records and reproduce at full speed. Inspect formatting functions, queue capacity, interrupt priorities, and whether the watchdog is fed from a path that masks system failure. Preserve fault data in a mechanism that survives the relevant reset without relying on unsafe fault-time printing.

**Assumptions:** Assume MCU-specific reset and fault information is available from its reference manual.

**Common incorrect answer:** Increasing every task's stack or watchdog period without identifying the violated budget.

**Follow-up:** How would you distinguish stack overflow from a watchdog timeout that occurs while interrupts are disabled?

**Scoring out of 4:** 1 point each: reset evidence; timing perturbation; resource budgets; targeted reproduction.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

### Q100 An update passes in normal testing but bricks the device after power interruption. What was missing?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**Assesses:** State-transition fault injection and recovery guarantees.

**Spoken answer:** Test interruption at every persistent transition: download, verification, inactive-slot write, boot-selection update, first boot, health confirmation, and rollback. Validate an always-available recovery path.

**Deeper explanation:** A/B storage alone is insufficient if metadata updates are not crash safe or if both slots depend on a shared incompatible data schema. Signed payload verification must precede activation, while health confirmation must reflect useful operation. Simulate interruption in disposable images, then test the actual bootloader and storage. Record exact boot attempts and slot states; do not invent successful power-cut coverage.

**Assumptions:** Assume a defined bootloader/update framework and a documented partition layout.

**Common incorrect answer:** Declaring rollback works because a manual reboot successfully starts the new image once.

**Follow-up:** How should persistent application data remain compatible with rollback to the previous software?

**Scoring out of 4:** 1 point each: transition matrix; metadata safety; health/rollback; shared-data compatibility.

**Learning connection:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md). **Verification references:** [PTHREAD](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html), [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html).

## Architecture boot and device tree

### Q101 How is a Linux application processor different from a typical microcontroller target?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Platform assumptions and selecting the correct software model.

**Spoken answer:** An application processor commonly runs a rich OS with virtual memory and external memory; a microcontroller commonly emphasizes integrated peripherals, bounded resources, and direct or RTOS-controlled execution.

**Deeper explanation:** These are practical categories, not absolute definitions. Check the actual core, MMU or MPU, memory map, boot chain, and board support. A Cortex-M firmware example cannot simply be compiled as a Linux driver, and a Linux userspace program relies on services absent from bare metal. Shared C modules can still be portable if hardware, time, and concurrency are abstracted behind explicit interfaces.

**Assumptions:** Assume representative ARM platforms; exact capabilities come from the selected part documentation.

**Common incorrect answer:** Equating every ARM device with Raspberry Pi or expecting POSIX processes on any MCU.

**Follow-up:** Which portions of a packet parser could be shared unchanged across both targets?

**Scoring out of 4:** 1 point each: practical distinction; hardware verification; software services; portable boundary.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q102 What do an MMU and an MPU each provide?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Memory protection and address-translation concepts.

**Spoken answer:** An MMU can translate virtual addresses and enforce permissions through mappings. An MPU typically applies access permissions and attributes to regions without providing the same general virtual-memory model.

**Deeper explanation:** The exact features depend on architecture. Linux processes normally rely on virtual-memory isolation and page tables on supported MMU platforms, while MCU firmware can use an MPU to separate task stacks or protect code and peripheral regions. Neither unit automatically fixes a buffer overflow in permitted memory. Region alignment, count, and cache attributes constrain an MPU design.

**Assumptions:** Assume a documented architecture; Linux also has specialized no-MMU configurations that need separate treatment.

**Common incorrect answer:** Claiming an MPU is just a smaller page table or that memory protection eliminates all memory corruption.

**Follow-up:** How would a DMA engine's access differ from CPU accesses checked by an MPU?

**Scoring out of 4:** 1 point each: translation; region protection; limitations; non-CPU access caveat.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q103 Describe a representative embedded Linux boot path without assuming every board uses U-Boot.

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Boot-stage responsibilities and platform-specific qualification.

**Spoken answer:** A platform may execute immutable ROM, early firmware, a bootloader, the kernel, and init or a service manager. Each stage initializes enough state and verifies or loads the next as configured.

**Deeper explanation:** Some boards use U-Boot SPL and U-Boot proper; others use different firmware or direct kernel loading. Record the board's actual chain, console, image formats, device tree, and root filesystem source. A kernel boot message does not prove userspace started. Debug by finding the last known-good stage and the expected handoff inputs, rather than reflashing unrelated components.

**Assumptions:** Assume a chosen board or QEMU machine; the sequence is a representative model, not a universal prescription.

**Common incorrect answer:** Stating all ARM boards use the identical ROM-to-U-Boot sequence.

**Follow-up:** What evidence distinguishes a kernel decompression failure from a missing root filesystem?

**Scoring out of 4:** 1 point each: stages; responsibilities; board qualification; stage-specific evidence.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q104 How do initramfs and a persistent root filesystem differ?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Early userspace and root transition.

**Spoken answer:** An initramfs is an early in-memory filesystem that can provide initial userspace and prepare access to the final root. A persistent root filesystem resides on a storage or network source.

**Deeper explanation:** A minimal appliance can run entirely from initramfs, while another uses it to unlock storage, load drivers, or select a root slot before switching. Its contents and init program must match the target architecture. A kernel configured without the needed storage driver available at the required stage cannot mount the final root merely because the driver exists somewhere on that inaccessible filesystem.

**Assumptions:** Assume Linux boot configuration explicitly identifies the root and initial userspace behavior.

**Common incorrect answer:** Treating initramfs as just a compressed disk partition or assuming it is mandatory for every system.

**Follow-up:** Why might a storage driver need to be built into the kernel rather than available only as a module?

**Scoring out of 4:** 1 point each: early-memory role; persistent-root role; transition; driver availability.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q105 What belongs in device tree, and what belongs in a driver?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Hardware description versus implementation policy.

**Spoken answer:** Device tree describes hardware connections and properties according to bindings; the driver implements the device's behavior using those resources and subsystem interfaces.

**Deeper explanation:** A sensor node can specify compatibility, bus address, interrupt, supply, and clock references. Do not place arbitrary Linux implementation details into bindings when they are not hardware properties. Matching can succeed while probe still fails because a referenced supplier is unavailable. Validate the tree against binding schemas and inspect the live tree and logs on the running target.

**Assumptions:** Assume a platform using device tree; ACPI or other enumeration paths may apply elsewhere.

**Common incorrect answer:** Treating a device-tree node as executable driver code or adding undocumented properties until probe works.

**Follow-up:** Why is a binding a compatibility interface that deserves review beyond one driver revision?

**Scoring out of 4:** 1 point each: description; binding contract; resource dependencies; validation.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q106 What are pin control and GPIO control responsible for?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Avoiding confusion between pad configuration and logical line access.

**Spoken answer:** Pin control configures pin multiplexing and electrical attributes such as pull or drive settings. GPIO APIs acquire and operate logical GPIO lines with polarity and ownership rules.

**Deeper explanation:** A pin may need the correct mux before a GPIO function reaches the physical pad. The GPIO descriptor's active-low property lets a driver use logical asserted/deasserted values. Some GPIO controllers are reached through sleeping buses, so choose APIs and context accordingly. The schematic, SoC pin map, and board device tree must agree; a Linux line number alone is not a wiring specification.

**Assumptions:** Assume a selected board and descriptor-based Linux GPIO APIs.

**Common incorrect answer:** Hard-coding a legacy global GPIO number or treating physical header pin numbers as GPIO offsets.

**Follow-up:** What happens if a pin is still muxed to UART while a GPIO consumer toggles it?

**Scoring out of 4:** 1 point each: mux/electrical; logical GPIO; polarity/context; board mapping.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q107 Why are clocks and regulators explicit driver resources?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Dependency management and power-aware initialization.

**Spoken answer:** Devices need correct clocks and supplies before register access. Drivers obtain and sequence these resources through their frameworks so ownership, sharing, and power transitions are coordinated.

**Deeper explanation:** A regulator may be shared by several consumers, and a clock may require a rate suitable for the bus or peripheral. Probe failures must unwind acquired state, while suspend and runtime idle need a compatible sequence. A missing supplier can require deferred probing rather than permanent failure. Always follow the hardware's timing and sequencing requirements and the subsystem's resource conventions.

**Assumptions:** Assume the board bindings describe the relevant supplies and clocks correctly.

**Common incorrect answer:** Accessing registers first and adding arbitrary delays when reads return all ones.

**Follow-up:** How would you distinguish an absent regulator driver from a wrong voltage or enable pin in the board description?

**Scoring out of 4:** 1 point each: prerequisites; shared frameworks; sequencing/unwind; supplier diagnosis.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q108 What does a cross-compilation sysroot contain, and why is it important?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Target headers and libraries versus host contamination.

**Spoken answer:** A sysroot provides the target-facing headers and libraries used by a cross toolchain. It prevents accidental use of incompatible host interfaces when building target applications.

**Deeper explanation:** The compiler target triple, libc, ABI, dynamic loader, and linked libraries must agree with the deployed root filesystem. A successful compile can still produce a binary requesting a loader absent on the board. Use the SDK's environment and inspect verbose commands and ELF metadata. Do not copy random host shared libraries into the target image to resolve one error.

**Assumptions:** Assume a toolchain and SDK intended for the selected target distribution or image.

**Common incorrect answer:** Believing setting CC alone ensures every dependency is built for the target.

**Follow-up:** How can pkg-config accidentally supply host include paths during a cross build?

**Scoring out of 4:** 1 point each: sysroot role; ABI/libc match; ELF check; dependency isolation.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q109 How does an interrupt differ from polling, and when can polling be reasonable?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Latency, load, and execution-context tradeoffs.

**Spoken answer:** An interrupt notifies software of an event asynchronously; polling checks state at chosen intervals. Choose from event rate, latency, CPU budget, power, and hardware behavior.

**Deeper explanation:** For a low-rate sensor, interrupts can avoid repeated checks. Under very high sustained load, bounded polling can reduce interrupt overhead; some subsystems combine both approaches. An interrupt handler still needs to acknowledge the correct condition and defer inappropriate work. A polling period bounds observation delay only under the assumed scheduling behavior, not merely because a sleep duration was configured.

**Assumptions:** Assume the hardware documents event-latching and acknowledge semantics.

**Common incorrect answer:** Claiming interrupts are always faster or polling inherently guarantees deterministic latency.

**Follow-up:** How would you prevent a level-triggered interrupt storm caused by an uncleared source?

**Scoring out of 4:** 1 point each: mechanism; workload tradeoff; acknowledgment; scheduling qualification.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q110 What is memory ordering, and why can it matter even with coherent caches?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Visibility order across cores or devices.

**Spoken answer:** Coherency concerns agreement about a location's value; ordering concerns when accesses to different locations become observable. Use the relevant synchronization or I/O primitives to establish required order.

**Deeper explanation:** A producer must initialize data before publishing a ready flag in the chosen memory model. A DMA descriptor may need its fields visible before a valid bit is exposed, even with coherent DMA memory. User-space C atomics, kernel barriers, and MMIO accessors serve different domains and are not interchangeable incantations. Start from the ownership and publication protocol, then choose documented primitives.

**Assumptions:** Assume a specified CPU, device, and software memory model; barriers are not substitutes for all synchronization.

**Common incorrect answer:** Using volatile or one generic barrier everywhere without identifying the ordering relation.

**Follow-up:** Why does a cache flush not by itself establish a complete concurrent object-lifetime protocol?

**Scoring out of 4:** 1 point each: coherence/order distinction; publication example; domains; ownership-first design.

**Learning connection:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md). **Verification references:** [DT](https://docs.kernel.org/6.12/devicetree/usage-model.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [UBOOT](https://docs.u-boot.org/en/v2025.01/), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [QEMU](https://www.qemu.org/docs/master/system/index.html).

## Kernel internals and lifetime

### Q111 Why should most application logic remain in user space?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Privilege boundaries and choosing the narrowest kernel responsibility.

**Spoken answer:** User space provides isolation, mature libraries, easier deployment, and safer debugging. Kernel code is appropriate when hardware or core subsystem integration requires that privilege and execution model.

**Deeper explanation:** A sensor driver can expose measurements through IIO while filtering, storage, networking, and inference run in user space. Moving a daemon into a module does not automatically reduce latency meaningfully, and it enlarges the failure impact of bugs. Measure the actual bottleneck and use existing interfaces before designing a new kernel ABI. Keep a clear boundary between mechanism and product policy.

**Assumptions:** Assume the required device functionality can be represented by a suitable subsystem interface.

**Common incorrect answer:** Writing a kernel module merely because a product is embedded or needs a service to start at boot.

**Follow-up:** What evidence would justify moving part of a data path closer to the kernel?

**Scoring out of 4:** 1 point each: isolation; legitimate kernel role; subsystem boundary; measured justification.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q112 What are process context and interrupt context in kernel code?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Allowed operations and who may sleep.

**Spoken answer:** Process context runs on behalf of a schedulable task, although held locks or disabled preemption can restrict it. Hard interrupt context cannot perform operations that may sleep.

**Deeper explanation:** A file operation is generally in task context but may enter atomic sections internally. A hard IRQ handler should do bounded urgent work and arrange suitable deferred processing. Threaded IRQ handlers and workqueues provide different contexts with their own rules. Never infer permission to sleep from the function name alone; inspect call paths, locks, and the selected kernel configuration.

**Assumptions:** Assume Linux 6.12 documentation; PREEMPT_RT affects some locking and interrupt behavior.

**Common incorrect answer:** Saying all code called by a process may sleep or all deferred work has identical restrictions.

**Follow-up:** Which context would you choose for an I2C transaction triggered by a GPIO interrupt?

**Scoring out of 4:** 1 point each: task context; IRQ restriction; held-lock caveat; deferred-context selection.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q113 How do kmalloc, vmalloc, and DMA allocation serve different needs?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Address-space, contiguity, and device access requirements.

**Spoken answer:** Kmalloc provides physically contiguous kernel allocations subject to allocator limits; vmalloc provides virtually contiguous mappings; DMA allocations or mappings meet a device's DMA contract.

**Deeper explanation:** Do not choose a buffer merely by whether the CPU can dereference it. A large vmalloc area is not a single physically contiguous block suitable for an arbitrary device. DMA APIs handle device-visible addresses, masks, and coherency requirements. Allocation flags must match context, and every allocation can fail. Bound buffers and avoid large allocations in hot or atomic paths.

**Assumptions:** Assume ordinary Linux allocation APIs; precise sizes and architecture constraints depend on the target.

**Common incorrect answer:** Passing a virtual pointer to a device or expecting GFP_ATOMIC to make unlimited memory available.

**Follow-up:** How would a scatter-gather-capable device change the buffer design?

**Scoring out of 4:** 1 point each: allocation distinction; DMA domain; context/failure; device capability.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q114 How do a mutex and a spinlock differ in the kernel?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Lock selection based on context and critical-section behavior.

**Spoken answer:** A mutex is a sleeping lock for eligible task contexts. A conventional spinlock protects short non-sleeping sections; PREEMPT_RT changes spinlock_t semantics, so configuration matters.

**Deeper explanation:** On a non-RT kernel, do not call sleeping functions while holding a spinlock. Shared state accessed from an interrupt may require interrupt-safe locking to avoid local deadlock, but the choice depends on all access paths. Raw spinlocks retain stricter behavior and are not a general optimization substitute. Document lock ownership, ordering, and which fields each lock protects.

**Assumptions:** Assume Linux 6.12 and explicitly distinguish non-RT from PREEMPT_RT behavior.

**Common incorrect answer:** Saying a spinlock is always faster or that disabling local interrupts serializes other CPUs.

**Follow-up:** Why might holding a spinlock across copy_to_user be invalid?

**Scoring out of 4:** 1 point each: sleeping distinction; context; RT qualification; per-state locking contract.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q115 What does a wait queue solve in a blocking character driver?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** State-based blocking and wakeup races.

**Spoken answer:** A wait queue lets a task sleep until a device-specific predicate becomes true, such as data available or device removed. The predicate and state synchronization remain the driver's responsibility.

**Deeper explanation:** A read path must handle interruption, nonblocking mode, removal, and competition with other readers. Wake after changing state so a woken task can observe progress. Recheck the condition because another reader may consume data first. Poll support must register the same wait relationship and report readiness from the same protected state. A wakeup is not a data item.

**Assumptions:** Assume the selected wait-event APIs and file-operation error conventions for Linux 6.12.

**Common incorrect answer:** Sleeping after a separate unprotected empty check or assuming each wake guarantees a readable byte.

**Follow-up:** What should a blocked read return if the device is disconnected?

**Scoring out of 4:** 1 point each: predicate; races; interruption/nonblocking; removal/poll consistency.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q116 Why does devm allocation not eliminate the need for a removal design?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Managed resource scope versus asynchronous lifetime.

**Spoken answer:** Managed resources simplify release when a device detaches or probe fails. They do not automatically stop work, timers, open-file users, or callbacks that still reference those resources.

**Deeper explanation:** Before detach completes, prevent new activity, quiesce hardware, and synchronize outstanding users using appropriate subsystem mechanisms. Registering cleanup actions in a deliberate order can help, but only if each action satisfies its context and lifetime contract. Open descriptors may outlive unbind, requiring separate state ownership or a disconnected state. A devm pointer is not a universal reference-counted object.

**Assumptions:** Assume Linux managed-device resources for the selected driver model.

**Common incorrect answer:** Removing manual cleanup blindly and allowing a workqueue callback to run after managed memory is released.

**Follow-up:** How would you handle a user process keeping a character device open during unbind?

**Scoring out of 4:** 1 point each: managed scope; asynchronous users; teardown order; open-file lifetime.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q117 What is the core idea of Read Copy Update?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Read-mostly synchronization and delayed reclamation.

**Spoken answer:** RCU lets readers access appropriately published objects while updates replace or unlink them. Old objects are reclaimed only after a suitable grace period ensures relevant preexisting readers are done.

**Deeper explanation:** RCU separates removal from reclamation and does not make arbitrary in-place updates safe. Writers still need a coordination strategy, and pointers must use the documented publish/dereference operations. The reader's allowed operations depend on the RCU flavor. A grace period is a lifetime guarantee for the specified readers, not a generic delay chosen in milliseconds.

**Assumptions:** Assume Linux 6.12 RCU APIs; SRCU and other flavors have distinct constraints.

**Common incorrect answer:** Calling sleep for a fixed time before freeing or claiming RCU removes every writer lock.

**Follow-up:** When would a reference count be needed in addition to an RCU read-side critical section?

**Scoring out of 4:** 1 point each: replace/unlink; grace-period reclamation; writer coordination; flavor/lifetime limits.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q118 How do workqueues differ from doing everything in an interrupt handler?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Deferred processing and cancellation.

**Spoken answer:** Workqueues run deferred callbacks in worker-thread context, allowing eligible sleeping operations. The interrupt path can acknowledge the event and schedule bounded follow-up work.

**Deeper explanation:** Coalescing behavior matters: queuing the same work item is not necessarily a count of every hardware event, so retain event data or counters separately. Protect shared state and choose ordering when multiple devices or events interact. During removal, prevent new queuing and use the correct cancellation or flushing protocol before releasing context. Do not hold a lock needed by the worker while waiting for it.

**Assumptions:** Assume ordinary workqueues in the selected Linux release; specialized queues have additional properties.

**Common incorrect answer:** Expecting one callback invocation for every attempted queue operation without checking the API semantics.

**Follow-up:** How would you preserve ten rapid events when one work item is already pending?

**Scoring out of 4:** 1 point each: worker context; event accounting; shared state; teardown/lock ordering.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q119 What is a kernel oops, and how should its evidence be preserved?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Crash interpretation without inventing a root cause.

**Spoken answer:** An oops reports a serious kernel fault with context such as instruction location and stack trace; it may or may not escalate to panic under configuration. Preserve the complete report and matching build identity.

**Deeper explanation:** Record kernel version, configuration, taint state, loaded modules, symbols, and reproduction steps. Decode addresses against the exact binary and inspect the first fault, because later failures may be consequences. A null-looking fault address suggests a class of access but does not prove the original source-level cause. Use a disposable VM for intentional fault experiments.

**Assumptions:** Assume access to matching unstripped symbols and a logging path that survives the failure where possible.

**Common incorrect answer:** Decoding against a different build or treating one stack frame as definitive proof of blame.

**Follow-up:** How would you distinguish a use-after-free from a simple null dereference using additional evidence?

**Scoring out of 4:** 1 point each: report preservation; exact symbols; first-fault reasoning; qualified hypothesis.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

### Q120 Why must an out-of-tree module match the target kernel build?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Internal API and configuration compatibility.

**Spoken answer:** Kernel internal interfaces and structure layouts are not a stable external ABI. Build the module against the exact target kernel's prepared build configuration and exported interfaces.

**Deeper explanation:** Version strings alone may be insufficient when configuration, symbol versions, compiler assumptions, or vendor patches differ. Inspect module metadata and load errors; do not force-load incompatible modules to make a demonstration pass. A module building successfully proves compiler acceptance for that build, not correct runtime behavior or safe teardown. Keep source, config, build logs, and runtime evidence together.

**Assumptions:** Assume Linux loadable modules; distribution signing and policy may impose additional requirements.

**Common incorrect answer:** Copying a random headers directory with the same major version or treating force-load as a compatibility fix.

**Follow-up:** What evidence would you collect for an unknown-symbol error at insertion time?

**Scoring out of 4:** 1 point each: unstable internals; exact build; load diagnostics; build/runtime distinction.

**Learning connection:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md). **Verification references:** [LOCKS](https://docs.kernel.org/6.12/locking/locktypes.html), [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [RCU](https://docs.kernel.org/6.12/RCU/whatisRCU.html), [WORKQUEUE](https://docs.kernel.org/6.12/core-api/workqueue.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html).

## Driver review scenarios

### Q121 A platform driver's probe never runs. What matching evidence do you inspect?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Enumeration, binding, and build configuration.

**Spoken answer:** Check that the device exists, the driver is built or loaded, the compatible or ID table matches, and the bus can bind them. Inspect the live description and logs.

**Deeper explanation:** A correct source DTS is not enough if a different DTB was deployed. A module may need a device table for alias-based autoloading. A disabled node, missing parent bus, absent Kconfig selection, or earlier resource dependency can prevent expected behavior. Distinguish no matching attempt from probe returning an error by adding appropriate diagnostic evidence rather than unconditional noisy prints.

**Assumptions:** Assume a device-tree-backed platform device and the selected Linux driver model.

**Common incorrect answer:** Renaming probe repeatedly or assuming source-code presence means the module is in the running image.

**Follow-up:** How would you verify the compatible string in the live device tree?

**Scoring out of 4:** 1 point each: enumeration; build/load; match table; deployed/live evidence.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q122 Probe returns EPROBE_DEFER repeatedly. Is this always a bug in the driver?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Supplier dependencies and correct deferral.

**Spoken answer:** Not necessarily. A required supplier such as a regulator, clock, GPIO controller, or interrupt domain may not yet be available. Trace the unresolved dependency and its eventual availability.

**Deeper explanation:** Deferral is useful when a supplier will appear later, but a misspelled reference or absent provider can make it permanent. Use framework error helpers and deferred-probe diagnostics appropriate to the pinned kernel. Do not convert every acquisition error into deferral; a malformed property or unsupported device should remain distinguishable. Confirm that successful reprobe does not leak resources from prior attempts.

**Assumptions:** Assume APIs report deferral through documented error codes and resource-acquisition patterns.

**Common incorrect answer:** Replacing EPROBE_DEFER with success while leaving essential resources uninitialized.

**Follow-up:** What happens when the supplier's driver is built as a module but never packaged in the image?

**Scoring out of 4:** 1 point each: supplier cause; permanent versus temporary; error distinctions; retry cleanup.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q123 A read method directly dereferences the user's buffer pointer. What is wrong?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** User/kernel trust boundary and fault handling.

**Spoken answer:** A user pointer must be accessed through the appropriate user-copy APIs, with validated sizes and error handling. Direct dereference can fault or violate the kernel's access rules.

**Deeper explanation:** `copy_to_user` and `copy_from_user` report bytes not copied rather than a conventional negative errno. Define how partial transfer affects device state and the read return value. Copying can fault and sleep in ordinary contexts, so do not place it blindly under a spinlock. Validate lengths and initialize any returned padding to avoid disclosing uninitialized kernel data.

**Assumptions:** Assume Linux 6.12 user-copy interfaces and a normal character-device file operation.

**Common incorrect answer:** Treating copy_to_user's nonzero return as a successful byte count or ignoring partial failure.

**Follow-up:** How would you avoid consuming an entire FIFO item when copying it to userspace fails partway?

**Scoring out of 4:** 1 point each: user-copy boundary; return semantics; context; state/initialization policy.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q124 A blocking read never wakes when a writer adds data. Where can the bug be?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Consistency of wait predicates and notification.

**Spoken answer:** Check that writer and reader use the same device instance, protected state, and wait queue, and that the writer updates the predicate before waking relevant waiters.

**Deeper explanation:** The reader must recheck after wake and handle interruption or removal. A predicate based on an unsynchronized cached count can remain false even though data exists. Poll and read should agree on what available data means. Use a deterministic test with a reader already blocked, then one write, and verify bounded completion without arbitrary polling sleeps.

**Assumptions:** Assume a stream-like character device with blocking and nonblocking contracts defined.

**Common incorrect answer:** Adding wakeups everywhere without identifying the predicate's owner and synchronization.

**Follow-up:** How should two readers behave when only one byte becomes available?

**Scoring out of 4:** 1 point each: shared instance/predicate; update-before-wake; competition; deterministic test.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q125 Poll reports readable but the next read blocks. Is the driver necessarily wrong?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Readiness races and API consistency.

**Spoken answer:** Not necessarily: another consumer may have consumed the data. Readiness is not a reservation. A nonblocking read should then return EAGAIN under the documented contract.

**Deeper explanation:** With only one consumer and no intervening state change, persistent disagreement suggests the driver's readiness predicate is wrong. Its poll implementation should register the wait queue and inspect the same state as read under compatible synchronization. Include removal and error readiness where appropriate. Test both single-consumer consistency and multi-consumer races rather than assuming one observation proves a defect.

**Assumptions:** Assume Linux poll semantics and a descriptor that supports nonblocking operation.

**Common incorrect answer:** Guaranteeing that readiness reserves bytes for the caller or returning readable unconditionally.

**Follow-up:** What ordering avoids missing a state change between checking readiness and registering a waiter?

**Scoring out of 4:** 1 point each: race distinction; nonblocking outcome; shared predicate; wait registration.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q126 A driver leaks memory whenever the second initialization step fails. How do you repair it?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Error-path ownership and acquisition order.

**Spoken answer:** List resources in acquisition order and unwind every successfully acquired resource in reverse dependency order. Use managed resources where their lifetime matches, without mixing incompatible cleanup models.

**Deeper explanation:** A failure test should inject an error after each acquisition, not only allocation failure at the first line. Set pointers or state so cleanup cannot double-release resources. If an interface becomes externally visible before initialization completes, a concurrent user can observe half-initialized state; delay publication until the object is ready. Review module init and per-device probe separately.

**Assumptions:** Assume each acquisition's release contract is known for the selected kernel APIs.

**Common incorrect answer:** Jumping to one generic cleanup label that releases resources never acquired.

**Follow-up:** Why might unregistering a visible interface need synchronization before freeing its backing object?

**Scoring out of 4:** 1 point each: resource inventory; reverse unwind; publish-last; failure injection.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q127 A driver's ioctl works for 64-bit applications but fails for 32-bit userspace. What do you inspect?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Stable UAPI layout and compatibility handling.

**Spoken answer:** Inspect argument structure sizes, alignment, pointer and long fields, command encoding, and the compat ioctl path. Use fixed-width UAPI types and explicit layout rules.

**Deeper explanation:** A structure containing a 32-bit field followed by a 64-bit field can have different padding across ABIs. Avoid native pointers and long in portable structures; validate reserved fields and initialize returned storage. Compatibility helpers apply only when the argument representation actually matches their assumptions. Preserve old command semantics when extending the interface, or add a new versioned command.

**Assumptions:** Assume a 64-bit kernel supporting 32-bit compatibility and Linux UAPI conventions.

**Common incorrect answer:** Adding a cast in the handler while leaving the userspace layout different.

**Follow-up:** How would you verify structure offsets in both a 32-bit and 64-bit test build?

**Scoring out of 4:** 1 point each: layout; fixed types; compat handler; ABI test/version strategy.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q128 A GPIO interrupt handler triggers continuously after the first event. What evidence matters?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Interrupt polarity, triggering, and source acknowledgment.

**Spoken answer:** Check electrical level, configured trigger type, polarity, and whether the device's interrupt condition is actually cleared. A level source stays asserted until its cause is removed.

**Deeper explanation:** Use the schematic and datasheet, inspect interrupt counters, and capture the line with suitable hardware tools when available. If clearing the condition requires a sleeping I2C transaction, a threaded handler may be appropriate. Masking the interrupt permanently hides the issue and loses future events. Contact bounce is a separate possibility with mechanical inputs and should be measured rather than assumed.

**Assumptions:** Assume the selected board's voltage and wiring are already verified and the interrupt source is known.

**Common incorrect answer:** Changing edge polarity randomly or adding long busy waits in a hard IRQ handler.

**Follow-up:** How do you prevent repeated handling while a threaded handler services a level-triggered source?

**Scoring out of 4:** 1 point each: trigger/electrical; acknowledgment; context; measured test.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q129 A device is removed while a process is blocked in read. What behavior must the driver define?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Disconnect semantics and object lifetime beyond unbind.

**Spoken answer:** Mark the device disconnected, prevent new hardware operations, wake blocked users, and return the documented EOF or error behavior. Keep backing state alive until existing references are released.

**Deeper explanation:** Unregistering a device node prevents new opens but does not necessarily eliminate existing file descriptions. A per-open or reference-counted state can distinguish dead hardware from still-valid bookkeeping. Stop interrupts, timers, and work before their resources vanish. Test removal during blocked read, active write, poll, and close, including repeated cycles in a disposable VM.

**Assumptions:** Assume a removable or unbindable device and a documented userspace ABI.

**Common incorrect answer:** Freeing all state in remove because the node no longer appears under /dev.

**Follow-up:** How would you make close safe after the underlying hardware has disappeared?

**Scoring out of 4:** 1 point each: disconnected state; wake behavior; references; teardown tests.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

### Q130 A custom character driver duplicates a standard sensor interface. When should it be redesigned?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**Assesses:** Subsystem selection and long-term interface cost.

**Spoken answer:** If the device fits an established subsystem such as IIO, input, hwmon, tty, or networking, use that subsystem's model unless a documented requirement cannot be represented.

**Deeper explanation:** A custom device node may be useful for teaching read/write and poll, but production integration benefits from established units, discovery, buffering, power management, and userspace tools. Evaluate the actual device class and required data rate before choosing. Replacing a public ABI later can be expensive, so document educational shortcuts and a migration path rather than presenting every toy driver as deployment-ready.

**Assumptions:** Assume the subsystem supports the device's essential semantics in the pinned kernel.

**Common incorrect answer:** Choosing a custom ioctl for every property because a character driver is familiar.

**Follow-up:** Which sensor features would you map to IIO channels, events, and buffered acquisition?

**Scoring out of 4:** 1 point each: subsystem fit; existing conventions; ABI cost; justified exception.

**Learning connection:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md). **Verification references:** [DEVRES](https://docs.kernel.org/6.12/driver-api/driver-model/devres.html), [IOCTL](https://docs.kernel.org/6.12/driver-api/ioctl.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html).

## Buses sensors DMA and power

### Q131 Compare UART, I2C, and SPI from an integration perspective.

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Bus semantics and electrical/software responsibilities.

**Spoken answer:** UART is asynchronous serial communication, I2C is addressed shared-bus communication, and SPI commonly uses synchronous clocked transfers with chip selection. Each has distinct wiring, timing, and framing responsibilities.

**Deeper explanation:** Do not infer voltage compatibility from protocol names. UART needs baud and framing agreement; I2C needs suitable pull-ups and address handling; SPI needs clock mode, chip-select behavior, and device-specific transaction structure. Throughput and reliability depend on the selected controllers, board layout, and protocol overhead. Linux bus drivers and MCU peripheral drivers expose different APIs despite sharing electrical protocols.

**Assumptions:** Assume specific board schematics and component datasheets are available before hardware wiring.

**Common incorrect answer:** Calling I2C universally slower or SPI universally reliable without considering the actual configuration.

**Follow-up:** Which measurements would you collect when a peripheral occasionally returns all 0xff bytes?

**Scoring out of 4:** 1 point each: semantics; electrical compatibility; configuration; evidence-led diagnosis.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q132 What does an I2C register read typically require, and what must be checked?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Transactions, repeated starts, and device-specific behavior.

**Spoken answer:** Many devices require writing a register address then reading data, sometimes within one combined transaction with a repeated start. The datasheet determines the exact sequence.

**Deeper explanation:** Check adapter functionality, address width, register width, endianness, auto-increment, and transfer return values. An API returning fewer messages than requested is not complete success. Some devices have read-to-clear registers or require conversion delays, so a generic byte read is insufficient. Avoid using bus probing tools indiscriminately on devices whose writes or reads have side effects.

**Assumptions:** Assume the chosen sensor's transaction protocol, not a universal I2C register model.

**Common incorrect answer:** Using two unrelated transfers when the device requires a combined transaction or ignoring short-transfer results.

**Follow-up:** How would you handle an address conflict between two identical fixed-address sensors?

**Scoring out of 4:** 1 point each: sequence; adapter/device capabilities; result checking; side effects.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q133 What SPI parameters must agree between controller configuration and peripheral expectations?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Clocking, framing, and transaction boundaries.

**Spoken answer:** Clock polarity and phase, maximum frequency, word width, bit order where configurable, chip-select polarity, and chip-select timing must match the device's requirements.

**Deeper explanation:** A command and its response may need chip select held across multiple transfer segments. Some devices insert dummy cycles or return data one transaction later. Verify the controller actually supports the requested pattern. Use a logic analyzer to compare clock, select, and data to the datasheet, and keep a software loopback test separate from proof that the real peripheral interprets commands correctly.

**Assumptions:** Assume a specific peripheral and controller; supported transfer features vary.

**Common incorrect answer:** Trying all modes until output looks plausible without verifying timing or device identity.

**Follow-up:** How would you detect a one-bit sampling shift in a known device-ID response?

**Scoring out of 4:** 1 point each: mode; frequency/width; transaction CS; waveform evidence.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q134 Why does IIO expose raw values and scale rather than only a floating-point value?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Measurement representation and subsystem conventions.

**Spoken answer:** IIO commonly separates raw readings and conversion attributes so userspace can interpret samples consistently without requiring floating-point work in the kernel.

**Deeper explanation:** The conversion depends on the channel's documented scale, offset, units, and representation. A raw ADC code is not automatically volts or degrees. Buffered scans also define channel ordering, signedness, storage width, real bit width, shift, and endianness. Read the channel metadata and test against known input points; a plausible-looking number can still have the wrong scale or sign extension.

**Assumptions:** Assume Linux IIO and the selected device's documented channel attributes.

**Common incorrect answer:** Hard-coding one sensor's scaling formula for every IIO device or ignoring scan layout metadata.

**Follow-up:** How would you validate a signed 12-bit sample stored in a 16-bit scan element?

**Scoring out of 4:** 1 point each: raw/scale; units/offset; buffer layout; calibration test.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q135 How do direct reads and buffered acquisition differ for a sensor driver?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Sampling architecture and throughput requirements.

**Spoken answer:** Direct reads suit occasional measurements; buffered acquisition collects sequences using triggers or hardware FIFOs with defined timestamps and scan layouts. Choose based on rate and timing needs.

**Deeper explanation:** A high-rate sensor can lose samples if userspace repeatedly requests one value with uncontrolled scheduling delays. A buffer needs capacity, overrun policy, trigger lifecycle, and timestamp interpretation. Hardware timestamps and host receipt timestamps mean different things. Switching between modes may require mutual exclusion or configuration restrictions enforced by the subsystem. Test overrun and start-stop transitions, not just steady-state samples.

**Assumptions:** Assume the sensor and IIO driver support the chosen acquisition mode.

**Common incorrect answer:** Calling a polling loop a precise sampling system because its average sleep interval is correct.

**Follow-up:** Where should a timestamp be taken if acquisition time matters more than delivery time?

**Scoring out of 4:** 1 point each: mode tradeoff; buffering/overrun; timestamps; transition constraints.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q136 What problem does regmap solve, and what does it not know automatically?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Register-access abstraction and device-specific semantics.

**Spoken answer:** Regmap can centralize register formatting, bus access, caching, and common update patterns. It still needs accurate configuration of register widths, readable/writable ranges, volatility, and side effects.

**Deeper explanation:** A cached status register can be wrong if the device changes it asynchronously. Write-one-to-clear or read-to-clear registers need careful treatment; a generic update-bits operation may not be appropriate. Power loss can invalidate hardware state and require cache synchronization in a defined sequence. Use the device datasheet to classify registers, then test both ordinary access and suspend/resume behavior.

**Assumptions:** Assume a Linux regmap-backed device on a supported bus.

**Common incorrect answer:** Enabling caching for every register or assuming regmap removes the need to understand register behavior.

**Follow-up:** How would you handle a register whose contents change without software writing it?

**Scoring out of 4:** 1 point each: abstraction; configuration; side effects; cache/power coherence.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q137 Why is a DMA address different from a CPU virtual or physical address?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Address domains and portable device programming.

**Spoken answer:** A DMA address is the address the device uses after the platform's mapping rules, potentially including an IOMMU. It is not generally a cast of the CPU pointer.

**Deeper explanation:** Use dma_addr_t for device-visible addresses and the DMA API for mapping and ownership transitions. Set the supported DMA mask and check relevant failures. A 32-bit device may not address every buffer the CPU can access. Scatter-gather mapping can merge or transform segments, so use returned mapping information rather than assuming the original list directly matches hardware descriptors.

**Assumptions:** Assume Linux DMA APIs and a device with documented addressing limits.

**Common incorrect answer:** Programming hardware with virt_to_phys as a universal substitute for DMA mapping.

**Follow-up:** How would you test a driver on a system with an IOMMU to expose hidden address assumptions?

**Scoring out of 4:** 1 point each: domains; DMA API/type; mask; mapped-segment semantics.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q138 What is the difference between coherent and streaming DMA mappings?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Ownership and cache-synchronization contracts.

**Spoken answer:** Coherent mappings support shared visibility under the architecture's DMA contract; streaming mappings support explicit transfer ownership and synchronization. Neither choice removes the need for correct device protocol ordering.

**Deeper explanation:** Descriptor rings often use coherent memory while data buffers may use streaming mappings. For streaming access, map or sync in the correct direction before handing ownership to the other side, and do not let CPU and device race over the same bytes. A coherent descriptor still needs fields published in the documented order before its valid flag or doorbell exposes it.

**Assumptions:** Assume Linux's documented mapping model and the target's DMA capabilities.

**Common incorrect answer:** Calling coherent memory automatically race-free or skipping ownership transitions because host tests pass.

**Follow-up:** What can happen if CPU cache lines overlap a DMA buffer and unrelated writable data?

**Scoring out of 4:** 1 point each: mapping distinction; ownership; direction/sync; ordering/cache-line risk.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q139 How do system suspend and runtime suspend differ?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Power-management scope and state coordination.

**Spoken answer:** System suspend coordinates a broader system sleep transition. Runtime suspend idles an individual device while the system remains active, subject to dependencies and usage references.

**Deeper explanation:** A driver must stop or account for active work, preserve needed state, manage wake sources, and restore hardware correctly. Runtime-PM reference imbalance can keep a device awake forever or let it suspend during access. Error paths are as important as success paths. Tests should cover repeated cycles, ongoing requests, supplier dependencies, and removal in each state.

**Assumptions:** Assume Linux PM frameworks and a device with documented power-state behavior.

**Common incorrect answer:** Treating both callbacks as identical boilerplate or disabling power management to hide every race.

**Follow-up:** Which information is lost when a sensor's power rail is removed rather than merely clock-gated?

**Scoring out of 4:** 1 point each: scope; usage/dependencies; state restoration; transition tests.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

### Q140 What does SocketCAN provide beyond sending raw CAN-controller registers?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Using the Linux networking abstraction for a fieldbus.

**Spoken answer:** SocketCAN presents CAN communication through Linux networking interfaces and sockets, enabling established filtering, interface management, and integration with network tooling.

**Deeper explanation:** Distinguish Classic CAN from CAN FD frame limits and configuration. A DBC describes application signal interpretation; it is not the bus transport itself. Bit timing, termination, transceiver state, bus-off recovery, and message freshness remain system concerns. A virtual CAN interface tests software paths without proving physical arbitration, error confinement, or electrical compatibility on the target bus.

**Assumptions:** Assume a supported Linux CAN interface and explicitly selected Classic CAN or CAN FD mode.

**Common incorrect answer:** Claiming virtual CAN success validates transceiver wiring or interpreting every frame payload as a universal signal layout.

**Follow-up:** How would you detect stale or missing application messages independently of CAN frame checks?

**Scoring out of 4:** 1 point each: networking API; transport/DBC; physical limits; freshness policy.

**Learning connection:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [GPIO](https://www.kernel.org/doc/html/v6.12/driver-api/gpio/consumer.html), [DMA](https://docs.kernel.org/6.12/core-api/dma-api-howto.html), [PM](https://docs.kernel.org/6.12/power/runtime_pm.html), [I2C](https://docs.kernel.org/6.12/i2c/writing-clients.html), [SPI](https://docs.kernel.org/6.12/spi/spi-summary.html), [REGMAP](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/regmap.h), [CAN](https://www.kernel.org/doc/html/v6.12/networking/can.html).

## Bare metal firmware

### Q141 What must startup code establish before calling main on a microcontroller?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Reset-state assumptions and C runtime initialization.

**Spoken answer:** Startup establishes the stack and vector handling as required by the architecture, initializes writable data, clears zero-initialized storage, and performs necessary runtime setup before main.

**Deeper explanation:** Initialized data often has a load image in flash and a run address in RAM, while `.bss` needs zeroing rather than stored payload bytes. Clock setup, constructors for C++, and platform hooks depend on the toolchain and startup design. Verify the linker symbols and memory map; copying the wrong region can corrupt memory before source-level debugging reaches main.

**Assumptions:** Assume a chosen Cortex-M-style example; reset behavior and vector details are architecture-specific.

**Common incorrect answer:** Assuming main is the first instruction after reset or that RAM automatically starts at zero.

**Follow-up:** How would you diagnose a fault before main using the reset handler and linker map?

**Scoring out of 4:** 1 point each: stack/vector; data copy; bss clear; toolchain/platform qualification.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q142 How does a linker script affect firmware correctness?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Memory placement and load/run relationships.

**Spoken answer:** It maps sections to physical memory regions, defines entry and boundary symbols, and reserves resources such as stack, heap, and retained data according to the platform.

**Deeper explanation:** A DMA buffer may need a particular accessible RAM region; a vector table may need alignment and placement rules. Code executing while flash is being programmed may require RAM placement on some MCUs. Linker overflow checks should reject oversized images rather than allowing silent overlap. Preserve the map file and verify that startup uses the same symbols and section assumptions.

**Assumptions:** Assume the selected linker syntax and MCU memory map, not a universal flash/RAM layout.

**Common incorrect answer:** Treating the script as cosmetic or moving sections without updating startup and peripheral-access assumptions.

**Follow-up:** What would happen if initialized data's load address and run address were confused?

**Scoring out of 4:** 1 point each: placement; boundary symbols; special-region needs; startup/map consistency.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q143 How should an interrupt service routine be structured?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Bounded urgent work and safe deferred processing.

**Spoken answer:** Identify and acknowledge the event as required, capture minimal necessary data, and notify deferred processing through an ISR-safe mechanism. Keep execution bounded and respect interrupt-priority rules.

**Deeper explanation:** Some peripherals require reading status before data or clearing specific flags in a defined order. A long printf, blocking wait, general allocation, or mutex acquisition can violate latency and API constraints. Preserve overrun/error information instead of discarding it. Measure ISR duration and nesting behavior on hardware; host unit tests can validate state logic but not real interrupt timing.

**Assumptions:** Assume the MCU reference manual and RTOS port define acknowledgment and allowed API behavior.

**Common incorrect answer:** Doing all parsing and storage inside the ISR because it seems fastest to access data there.

**Follow-up:** How would you handle a burst larger than the ISR-to-task queue capacity?

**Scoring out of 4:** 1 point each: acknowledge; bounded capture; ISR-safe notification; measured overload behavior.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q144 What is the difference between a hardware timer, a software timer, and a busy wait?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Timing mechanisms and interference.

**Spoken answer:** A hardware timer counts independently according to its clock; a software timer schedules callbacks through an OS or scheduler; a busy wait occupies the CPU while checking progress.

**Deeper explanation:** Hardware compare or capture can provide timing behavior unavailable from a task sleep. Software timer callbacks may share a service task, so blocking one callback can delay others. Busy waits may be appropriate for tiny documented hardware sequences but can disrupt scheduling and power usage. Clock source, prescalers, interrupt latency, and rollover must be included in the timing calculation.

**Assumptions:** Assume specific timer hardware and scheduler behavior are known before setting accuracy claims.

**Common incorrect answer:** Equating a requested delay with guaranteed execution at exactly that wall-clock instant.

**Follow-up:** Which mechanism would you use to measure pulse width, and where would software latency enter?

**Scoring out of 4:** 1 point each: mechanism distinction; service context; clock/rollover; suitable application.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q145 How do you choose PWM frequency and resolution?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Timer arithmetic and application constraints.

**Spoken answer:** Choose a timer clock, prescaler, and period that meet the load's frequency requirement while providing enough duty-cycle steps. Frequency and resolution trade off for a fixed timer clock.

**Deeper explanation:** For a simple up-counter, the common relation is timer clock divided by prescaler factor and period count, but exact register conventions vary. A period of N counts gives roughly N duty positions, subject to output mode. Motors, LEDs, and power converters have different constraints; a learning LED demo is not evidence that a motor power stage is safe or controlled correctly.

**Assumptions:** Assume a documented timer mode and electrical load; verify register off-by-one conventions.

**Common incorrect answer:** Changing compare values without considering frequency, polarity, dead time, or load requirements.

**Follow-up:** How would center-aligned mode change the frequency calculation and switching behavior?

**Scoring out of 4:** 1 point each: arithmetic; tradeoff; register convention; application constraints.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q146 What should be considered before trusting an ADC measurement?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** The analog path and digital representation.

**Spoken answer:** Check reference voltage, input range, source impedance, sampling time, resolution, calibration, noise, and conversion format. The numeric code alone is not the physical quantity.

**Deeper explanation:** A high-impedance source may need more acquisition time or buffering to charge the sampling capacitor. Multiplexed channels can interact if settling is inadequate. Convert using the device's documented transfer behavior and calibration data, then verify with known inputs across the relevant range. DMA can move samples efficiently but does not fix analog settling or reference instability.

**Assumptions:** Assume the selected MCU or external ADC datasheet and board analog circuit are available.

**Common incorrect answer:** Converting code to voltage with a nominal supply constant and claiming calibrated accuracy.

**Follow-up:** How would you separate reference drift from sensor noise in a repeatable experiment?

**Scoring out of 4:** 1 point each: analog conditions; transfer/calibration; known-input test; DMA limitation.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q147 How should a watchdog be integrated into a multitask firmware system?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Detecting loss of useful progress rather than merely CPU activity.

**Spoken answer:** Feed the watchdog only when required subsystems demonstrate timely health under a defined policy. A dedicated feeder that runs regardless of failures can mask a dead system.

**Deeper explanation:** Use task heartbeats or supervised state transitions with bounded deadlines, and distinguish transient overload from an unrecoverable fault. Record reset reason and enough diagnostic state for post-reset analysis. Windowed watchdogs may also reject feeds that are too early. Verify behavior during debugger attachment, firmware update, and low-power states, because hardware may handle each differently.

**Assumptions:** Assume the selected watchdog's clock, window, and reset-domain behavior are documented.

**Common incorrect answer:** Feeding unconditionally from a high-priority timer interrupt even when application tasks are stuck.

**Follow-up:** What failures cannot a software-supervised watchdog detect if all tasks keep sending stale heartbeats?

**Scoring out of 4:** 1 point each: useful progress; supervision; reset evidence; special-state behavior.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q148 What information should a Cortex-M fault handler preserve?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Postmortem evidence with minimal additional failure risk.

**Spoken answer:** Preserve the relevant fault-status registers, stacked execution context, active stack selection, reset cause, and build identity using a bounded method appropriate to the target.

**Deeper explanation:** Do not assume printf or the normal allocator is safe after a memory fault. Validate stack addresses before dereferencing a possibly corrupted frame. A fault record can be stored in retained RAM or another target-specific mechanism, then reported after reboot. Exact register availability varies by Cortex-M generation; distinguish hard fault escalation from configurable fault sources using the reference manual.

**Assumptions:** Assume a selected Cortex-M part and verified retained-storage mechanism; no universal register set is promised.

**Common incorrect answer:** Blindly dumping a corrupted stack through an unbounded serial print loop.

**Follow-up:** How would you ensure a fault record corresponds to the firmware binary used for symbolication?

**Scoring out of 4:** 1 point each: context/status; bounded capture; stack validation; build matching.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q149 How should flash writes be designed when erase granularity exceeds record size?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Persistence under erase/program restrictions.

**Spoken answer:** Respect erase-block and program-unit rules, write new records with version and integrity metadata, and choose the newest valid committed record after restart.

**Deeper explanation:** A log or dual-record scheme can preserve the previous valid value until the new one is complete. Power can fail between data and commit marker, so recovery must reject incomplete records. Flash endurance requires write-rate budgeting and wear distribution. CRC can identify accidental corruption but does not authenticate a malicious change. Test interrupted operations on the actual device after modeling the state machine.

**Assumptions:** Assume the MCU datasheet specifies allowed programming sequences and endurance limits.

**Common incorrect answer:** Overwriting a few bytes in place as though flash were RAM or claiming a checksum prevents torn writes.

**Follow-up:** How would you recover when both records are invalid, and what configuration is safe to use?

**Scoring out of 4:** 1 point each: granularity; commit/recovery; endurance; fault tests.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q150 What belongs in a firmware bootloader versus the application?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Update and recovery boundaries.

**Spoken answer:** A bootloader establishes a trusted or validated launch decision and a recovery/update path according to the product's design. The application provides normal device behavior and health confirmation.

**Deeper explanation:** Keep image format, compatibility, signature verification where used, version policy, and failure recovery explicit. An application crash must not necessarily destroy the ability to recover. Bootloader update itself has different risk because it can affect the recovery mechanism. Partition layout, key storage, and reset behavior are target-specific; a host simulation validates decision logic without proving secure boot or power-failure behavior.

**Assumptions:** Assume an identified bootloader framework or carefully scoped learning implementation.

**Common incorrect answer:** Treating checksum verification as signature authentication or overwriting the sole recovery image without a recovery plan.

**Follow-up:** How would the bootloader decide that a newly installed image failed health confirmation?

**Scoring out of 4:** 1 point each: launch/recovery; image policy; bootloader-update risk; validation boundary.

**Learning connection:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md). **Verification references:** [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [MCUBOOT](https://docs.mcuboot.com/design.html).

## RTOS scheduling and communication

### Q151 How do task priority and execution time interact in a preemptive RTOS?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Schedulability rather than priority folklore.

**Spoken answer:** Priority determines which ready task runs under the selected policy; execution time and blocking determine whether deadlines can actually be met. High priority does not create additional CPU capacity.

**Deeper explanation:** Budget worst-case execution, release rates, interrupt load, and shared-resource blocking. A task that never blocks can starve lower priorities under fixed-priority scheduling. Equal-priority time slicing depends on configuration. Assign priorities from timing and dependency requirements, then measure representative behavior and identify where formal analysis or stronger bounds are still needed.

**Assumptions:** Assume a stated FreeRTOS scheduling configuration; SMP and cooperative modes need additional analysis.

**Common incorrect answer:** Giving every task the maximum priority or using observed average execution time as a worst-case guarantee.

**Follow-up:** How would you choose priorities for acquisition, control, logging, and background diagnostics?

**Scoring out of 4:** 1 point each: policy; workload budget; blocking/starvation; evidence limits.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q152 When should you use a queue rather than a task notification?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Communication semantics and ownership.

**Spoken answer:** Use a queue when distinct data items or multiple producers need buffered transfer. A task notification can be a lightweight signal or count for a specific task under its documented semantics.

**Deeper explanation:** Notifications are not a universal replacement for message storage: coalescing, overwrite, and counting modes mean different things. If an ISR signals that DMA data is ready, ownership of the buffer must remain valid until the consumer finishes. Queue item copying versus pointer transfer changes lifetime responsibilities. Define what happens when the receiver is late or a queue is full.

**Assumptions:** Assume the selected FreeRTOS release and configured notification-index support.

**Common incorrect answer:** Sending pointers to temporary buffers or assuming every notification preserves a separate payload.

**Follow-up:** How would you transfer a DMA buffer between producer and consumer without copying its contents?

**Scoring out of 4:** 1 point each: data/signal distinction; notification semantics; ownership; overload.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q153 Why can a mutex be unsuitable in an interrupt handler?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Ownership, blocking, and priority inheritance context.

**Spoken answer:** An interrupt cannot block waiting for a task-owned resource, and ordinary mutex ownership/priority-inheritance semantics are designed for tasks. Use an appropriate ISR-safe signaling or data-transfer mechanism.

**Deeper explanation:** In FreeRTOS, choose documented FromISR APIs and comply with the port's interrupt-priority restrictions. A binary semaphore or notification can wake a task, but does not by itself protect shared multi-field data. If the ISR and task share a buffer, define a bounded critical section or ownership handoff. Never assume an API is ISR-safe merely because it usually returns immediately.

**Assumptions:** Assume the FreeRTOS port documentation for the selected MCU and priority configuration.

**Common incorrect answer:** Calling a normal mutex API with zero timeout from an ISR and assuming that makes it valid.

**Follow-up:** What does a higher-priority-task-woken flag mean for the return-from-interrupt path?

**Scoring out of 4:** 1 point each: no blocking/ownership; FromISR; priority restrictions; data ownership.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q154 What are the limits of FreeRTOS priority inheritance?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Avoiding overclaims about a simplified mechanism.

**Spoken answer:** FreeRTOS mutexes provide a simplified inheritance mechanism to reduce inversion. It is not a complete solution to arbitrary nested-lock timing, deadlocks, or long critical sections.

**Deeper explanation:** The behavior while a task holds multiple mutexes depends on the kernel's implementation and release. Keep lock graphs simple, bound hold times, and avoid slow I/O under locks. A binary semaphore used for signaling does not provide the same ownership-based inheritance semantics as a mutex. Review the selected release's documentation and test the actual nesting scenario relevant to the system.

**Assumptions:** Assume a pinned FreeRTOS kernel version and documented mutex configuration.

**Common incorrect answer:** Claiming every semaphore has priority inheritance or that inheritance guarantees a deadline.

**Follow-up:** How would a message-passing design remove a problematic shared peripheral lock?

**Scoring out of 4:** 1 point each: simplified PI; mutex/semaphore distinction; nested/long-hold limits; redesign.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q155 How do you size and validate RTOS task stacks?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Worst-case stack demand and meaningful evidence.

**Spoken answer:** Estimate call depth, local objects, interrupt/exception behavior, library use, and context overhead, then measure high-water behavior under demanding paths with margin and overflow detection.

**Deeper explanation:** A clean short run does not exercise every branch, recursion depth, error path, or printf formatting case. Stack units differ across APIs, so distinguish bytes from StackType_t elements. Interrupt stacks may be separate or share resources depending on the port. Large local arrays can be moved into explicit owned storage when justified, but shared static buffers introduce concurrency issues.

**Assumptions:** Assume the chosen RTOS port documents stack units and exception-stack behavior.

**Common incorrect answer:** Treating one high-water measurement as a proof of a safe worst-case stack size.

**Follow-up:** Which rarely executed failure path could consume more stack than steady-state operation?

**Scoring out of 4:** 1 point each: estimate; units; stressful measurement; margin and coverage limits.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q156 How should a periodic RTOS task avoid cumulative drift?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Release-time scheduling and overrun policy.

**Spoken answer:** Use the RTOS's absolute or previous-wake-time periodic-delay facility where appropriate, and track overruns separately from the nominal period.

**Deeper explanation:** A delay after work includes the work duration in each cycle. A delay-until pattern targets successive release times but does not guarantee the task will actually run exactly then; higher-priority work and interrupts can delay it. Define how missed releases affect processing, especially for control or sampling. Tick resolution and tickless idle behavior influence what can be represented and measured.

**Assumptions:** Assume the selected FreeRTOS API/version and a valid tick-period conversion.

**Common incorrect answer:** Equating a one-tick delay with one millisecond on every configuration.

**Follow-up:** How would a task whose execution sometimes exceeds its period report and recover from overruns?

**Scoring out of 4:** 1 point each: periodic schedule; scheduler delay; tick conversion; overrun policy.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q157 What must a Linux to MCU protocol specify beyond a payload structure?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Interoperability and failure recovery.

**Spoken answer:** Specify framing, length bounds, byte order, version, message type, sequence or request ID, integrity check, timeouts, and recovery behavior. Define ownership and state transitions on both sides.

**Deeper explanation:** A command acknowledgment should distinguish received, accepted, and completed if those events matter. Duplicate requests need idempotency or a documented replay policy. A CRC detects accidental corruption but is not authentication. Test resets, truncation, corrupt length, stale commands, and incompatible versions. Keep transport-specific behavior separate so the same parser can be exercised through a PTY before hardware testing.

**Assumptions:** Assume a bounded point-to-point learning protocol with explicitly documented trust assumptions.

**Common incorrect answer:** Sending a packed C structure and calling it a complete protocol specification.

**Follow-up:** How would each peer recover when the other reboots and its sequence counter restarts?

**Scoring out of 4:** 1 point each: wire contract; command semantics; reset/replay; fault tests.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q158 How do you make a command timeout meaningful for a robot demonstrator?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Freshness, authority, and local control boundaries.

**Spoken answer:** The MCU should enforce a local deadline for motion commands and transition to a defined stopped or disabled state when commands become stale, independent of Linux remaining alive.

**Deeper explanation:** Use monotonic local timing, explicit arm/disarm state, bounded command values, and clear recovery rules. A network heartbeat is not proof that a current control command is safe. Test dropped packets, Linux stalls, repeated old frames, MCU reset, and reconnect. This establishes a learning demonstrator behavior, not a certified emergency-stop or functional-safety system.

**Assumptions:** Assume simulated motion first; physical hardware requires separate electrical and hazard controls.

**Common incorrect answer:** Continuing the last motor command indefinitely or calling a software timeout a certified safety function.

**Follow-up:** Should a recovered link automatically re-arm motion, or require an explicit operator action?

**Scoring out of 4:** 1 point each: MCU-local deadline; state transition; stale/replay tests; safety scope.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q159 What does deterministic execution mean in an RTOS discussion?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Bounded behavior and precise claims.

**Spoken answer:** State which quantity is bounded under which assumptions: execution time, interrupt latency, response time, or memory use. A repeatable average is not a deterministic worst-case guarantee.

**Deeper explanation:** Bounded loops, fixed-capacity storage, controlled blocking, and documented interrupt load make analysis possible. Cache effects, DMA contention, flash wait states, and other tasks can affect timing. A measurement campaign can establish observed distributions for its conditions; formal worst-case claims require stronger assumptions and analysis. Explain the required deadline and acceptable failure behavior before choosing an RTOS or priority scheme.

**Assumptions:** Assume a documented workload and hardware configuration; no universal zero-jitter guarantee exists.

**Common incorrect answer:** Saying an RTOS makes every task execute at its requested instant.

**Follow-up:** What evidence would you present for a 2 ms response requirement after only host simulation?

**Scoring out of 4:** 1 point each: precise quantity; assumptions; bounded design; measurement-versus-proof.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

### Q160 How do you recover from a stalled I2C transaction in firmware without wedging every task?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**Assesses:** Timeout boundaries, peripheral recovery, and system isolation.

**Spoken answer:** Apply bounded waits, classify controller and bus state, and use the MCU and device's documented recovery sequence. Keep one failed peripheral from blocking unrelated work indefinitely.

**Deeper explanation:** Recovery may involve aborting DMA, resetting the peripheral, inspecting stuck lines, or a documented bus-clear sequence. Electrical faults and devices holding a line require hardware-aware diagnosis; blindly toggling pins can be inappropriate. After recovery, reset protocol state and reinitialize affected devices as needed. Count failures and enter degraded operation after a defined retry budget.

**Assumptions:** Assume a selected MCU and sensor with documented recovery behavior; no universal sequence is prescribed.

**Common incorrect answer:** Looping forever on a ready flag or retrying immediately without a bound or state reset.

**Follow-up:** What should happen if the bus remains physically stuck after the retry budget expires?

**Scoring out of 4:** 1 point each: bounded wait; documented recovery; isolation/degraded mode; observable retries.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [ARM](https://arm-software.github.io/CMSIS_6/latest/Core/index.html), [MCUBOOT](https://docs.mcuboot.com/design.html).

## Firmware and protocol coding

### Q161 Implement comparison of wrapping 16-bit sequence numbers.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Freshness semantics and half-range limits.

**Spoken answer:** A candidate is newer when the unsigned 16-bit difference from the previous value is nonzero and below 0x8000. Treat equality as duplicate and half-range distance as ambiguous.

**Deeper explanation:** `seq_newer` accepts 0 after 65535 and rejects 65535 after 0 under the bounded-distance contract. Sequence comparison alone cannot distinguish a restarted sender from a very old session, so include a session identifier or explicit handshake. Test equality, adjacent values, wraparound, and exactly half the range. Do not silently assign meaning to an excluded ambiguous case.

**Assumptions:** Assume no legitimate forward jump or observation gap reaches half the sequence space.

**Common incorrect answer:** Using ordinary greater-than or claiming modular comparison solves reboot identity.

**Follow-up:** How would you reject a replay from a previous boot after the sequence counter resets?

**Scoring out of 4:** 1 point each: difference rule; duplicate; half-range condition; session boundary.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q162 Encode payload bytes with delimiter 0x7e and escape 0x7d.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Framing expansion and bounded output.

**Spoken answer:** Emit a delimiter, escape each delimiter or escape byte by prefixing 0x7d and XORing the byte with 0x20, then emit a closing delimiter. Check worst-case output size first.

**Deeper explanation:** `escape_frame` needs at most twice the payload length plus two bytes and rejects insufficient capacity without writing. Payload `7e 7d 01` becomes `7e 7d 5e 7d 5d 01 7e`. This framing exercise does not itself add length, CRC, authentication, or a timeout; those are separate protocol layers. The decoder must reject a dangling escape at a boundary under a defined policy.

**Assumptions:** Assume a nonoverlapping output buffer and the exact stated escaping convention.

**Common incorrect answer:** Allocating only payload length plus two or escaping only the delimiter but not the escape byte.

**Follow-up:** How would you recover when a stream ends immediately after an escape byte?

**Scoring out of 4:** 1 point each: encoding; expansion bound; transactional capacity failure; malformed recovery.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q163 Implement a watchdog supervisor for three required task heartbeats.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Progress windows and stale-health rejection.

**Spoken answer:** Track the last observed progress time for each required task. Report healthy only when every task has progressed within its configured timeout and initialization has completed.

**Deeper explanation:** `supervisor_ok` accepts injected monotonic timestamps and rejects a task that has never reported. Use unsigned wrap-aware elapsed arithmetic under a bounded interval contract. A heartbeat should advance only after useful work or an accepted idle-state check, not from an unrelated timer. Unit tests can validate time-window logic; hardware testing must still verify watchdog clocks and reset behavior.

**Assumptions:** Assume timestamps and limits stay within the supported modular interval and task progress reports are trustworthy.

**Common incorrect answer:** Feeding the watchdog because any one task is alive or treating an old stored heartbeat as current.

**Follow-up:** How would you supervise a task that legitimately performs a long firmware update operation?

**Scoring out of 4:** 1 point each: all-task policy; initialization; stale timeout; useful-progress qualification.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q164 Implement a robot command state machine with DISARMED ARMED and FAULT states.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Explicit authority and fault transitions.

**Spoken answer:** Accept motion only while armed, disarm on command timeout, and latch a fault on a defined fault event. Require an explicit clear and re-arm sequence rather than resuming automatically.

**Deeper explanation:** `control_step` models events without touching hardware. The test trace arms, accepts a command, times out to DISARMED, enters FAULT, rejects arm, clears to DISARMED, then arms again. Outputs include whether motion is permitted, so state and actuator policy cannot diverge silently. Integration must independently ensure the hardware output changes on each disabling transition.

**Assumptions:** Assume a learning demonstrator; the state machine is not a certified safety function.

**Common incorrect answer:** Automatically restoring motion when communications return or clearing a fault on any incoming packet.

**Follow-up:** How would you verify that an MCU reset starts with outputs disabled before application initialization?

**Scoring out of 4:** 1 point each: guarded motion; timeout; latched fault/re-arm; output integration boundary.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q165 Implement sensor validity classification using range and maximum age.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Separating measurement value from trust in that value.

**Spoken answer:** A sample is valid only if its status is good, value lies within the configured range, and its monotonic age is no greater than the allowed maximum.

**Deeper explanation:** `sensor_valid` uses explicit minimum, maximum, and age limit inputs. Test exact range boundaries, out-of-range values, stale timestamps, and an invalid status carrying an otherwise plausible number. Do not replace invalid data with zero without a validity marker, because zero may be a legitimate reading. The policy should tell downstream control or logging how to handle missing data.

**Assumptions:** Assume a bounded unsigned timestamp interval and configured range in the same units as the sample.

**Common incorrect answer:** Checking only the numeric range and ignoring that an old value can remain plausible indefinitely.

**Follow-up:** When would a rate-of-change plausibility check add useful evidence, and when could it reject real events?

**Scoring out of 4:** 1 point each: range; age; status; downstream missing-data contract.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q166 Implement bounded exponential retry delays with a maximum delay.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Recovery behavior without overflow or retry storms.

**Spoken answer:** Double the delay while below the cap, saturating before multiplication would overflow or exceed the cap. Track a retry budget separately from the delay calculation.

**Deeper explanation:** `retry_delay` returns min(initial times 2 to the attempt, cap) using guarded steps, not an unchecked shift. Test zero attempts, the cap transition, large attempts, and initial greater than cap. Deterministic tests omit jitter; a deployed multi-device system may add bounded randomization to avoid synchronized reconnect storms. Permanent configuration errors should not be retried endlessly as transient failures.

**Assumptions:** Assume positive cap and a documented zero-initial-delay policy.

**Common incorrect answer:** Using `initial << attempt` with an unchecked shift count or confusing capped delay with capped retry count.

**Follow-up:** How would you reset the retry state after a connection briefly succeeds then immediately fails?

**Scoring out of 4:** 1 point each: saturation; shift avoidance; budget distinction; recovery policy.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q167 Write a median-of-three filter for signed 32-bit samples without addition.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Small bounded filtering and overflow avoidance.

**Spoken answer:** Use comparisons and swaps to order three values, then return the middle. Avoid summing all three and subtracting extremes because the intermediate sum can overflow.

**Deeper explanation:** `median3` is constant in storage and has a fixed small comparison bound. Test already sorted, reversed, equal, and extreme values including INT32_MIN and INT32_MAX. A median suppresses an isolated impulse among three samples but changes signal behavior and adds a window interpretation. It is not a substitute for checking sensor validity or measuring control-loop delay.

**Assumptions:** Assume signed 32-bit samples and a three-sample count-based window.

**Common incorrect answer:** Using arithmetic averaging as a median or ignoring overflow in a sum-based shortcut.

**Follow-up:** How would you define output during the first two samples of a streaming implementation?

**Scoring out of 4:** 1 point each: comparison algorithm; extremes; ties; filtering/startup limitations.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q168 Scale a signed sensor code by an integer ratio with checked output range.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Fixed-point arithmetic and explicit rounding.

**Spoken answer:** Promote the product to int64_t before multiplication, reject a zero denominator, divide under the stated rounding policy, and check the quotient fits int32_t before storing.

**Deeper explanation:** `scale_i32` uses an int32_t numerator and a positive int32_t denominator; their product fits int64_t. C integer division truncates toward zero, so negative values need a different formula if floor rounding is required. Test negative input, fractional output, zero denominator, and an out-of-range result. Units and calibration constants belong in the interface contract.

**Assumptions:** Assume the specified operand ranges; extending to int64_t operands needs additional multiplication checks.

**Common incorrect answer:** Casting only after the 32-bit multiplication has already overflowed.

**Follow-up:** How would round-to-nearest be defined at exact half steps for negative values?

**Scoring out of 4:** 1 point each: promote-before-multiply; denominator; output bounds; rounding/units.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q169 Decode a signed 12-bit two's-complement value from a 16-bit container.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Bit-width-specific signed interpretation without accidental promotions.

**Spoken answer:** Mask to 12 bits, then if bit 11 is set subtract 4096 in a sufficiently wide signed type. Otherwise return the masked value.

**Deeper explanation:** `decode_s12` yields 2047 for 0x07ff, -2048 for 0x0800, and -1 for 0x0fff. This avoids relying on arithmetic right shift of a negative value or implementation-defined out-of-range conversion. Container byte order and any bit shift must be handled before this function. Reserved upper bits may need validation rather than masking in a stricter protocol.

**Assumptions:** Assume the wire field is explicitly 12-bit two's complement, not a sign-magnitude or offset-binary ADC.

**Common incorrect answer:** Casting the whole 16-bit container to int16_t and expecting bit 11 to become the sign bit.

**Follow-up:** How would the code change for a left-aligned 12-bit field with four low padding bits?

**Scoring out of 4:** 1 point each: mask; sign threshold; subtraction; representation boundary tests.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

### Q170 Implement a token bucket that limits diagnostic events per time window.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**Assesses:** Rate limiting with bounded arithmetic and observability.

**Spoken answer:** Store available tokens and last refill time, add whole refill intervals up to capacity, and consume one token only when available. Define whether partial intervals are retained.

**Deeper explanation:** `bucket_take` uses integer millisecond timestamps and retains the unconsumed time remainder by advancing last refill only by complete intervals. Saturate before adding a large refill count. Test initial burst capacity, rejection when empty, one refill, long idle time, and timestamp wrap under the documented interval limit. Count suppressed events so rate limiting does not hide repeated failures completely.

**Assumptions:** Assume single-threaded access and a nonzero refill interval; concurrency requires synchronization.

**Common incorrect answer:** Resetting the bucket to full on every call or overflowing tokens after a long idle period.

**Follow-up:** How would you reserve capacity for critical alarms separately from verbose diagnostics?

**Scoring out of 4:** 1 point each: token/refill invariant; retained remainder; saturation; suppressed-count policy.

**Learning connection:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md). **Verification references:** [C11](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).

## Images updates and reliability

### Q171 How would you choose between Buildroot and Yocto for a learning or product image?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Build-system scope and maintenance tradeoffs.

**Spoken answer:** Choose from required customization, package workflow, reusable metadata, team familiarity, supported BSPs, and maintenance needs. Buildroot and Yocto can both produce embedded Linux systems through different models.

**Deeper explanation:** A small appliance can make Buildroot's configuration and package model approachable. A product family may benefit from Yocto layers, recipes, SDK generation, and policy separation, at the cost of more concepts and build resources. Neither choice automatically proves reproducibility, security, or support for a board. Pin releases and external inputs, then demonstrate the actual image and update path.

**Assumptions:** Assume the exact target BSP and team requirements are evaluated; this is not an employer requirement claim.

**Common incorrect answer:** Calling one universally professional and the other only for toys without examining the use case.

**Follow-up:** Which evidence would justify switching build systems after an initial prototype?

**Scoring out of 4:** 1 point each: requirements; models; maintenance/resource tradeoff; validated target support.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q172 What do a Yocto layer, recipe, and image each represent?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Metadata organization and build artifacts.

**Spoken answer:** A layer groups related metadata; a recipe describes how to obtain, configure, build, install, and package a component; an image selects a filesystem composition and related outputs.

**Deeper explanation:** Keep product policy, board support, and application metadata organized so upgrades remain reviewable. A bbappend modifies a matching recipe without copying its entire implementation, but version matching must be intentional. BitBake task signatures and shared state affect rebuild behavior. Inspect the actual task logs and environment when a variable appears ineffective instead of changing random global configuration.

**Assumptions:** Assume the pinned Yocto 5.0-family documentation and matching layer branches.

**Common incorrect answer:** Putting every customization in local.conf or treating an image recipe as the implementation of every package.

**Follow-up:** How would you package one telemetry service in your own layer without editing upstream recipes?

**Scoring out of 4:** 1 point each: three roles; layer separation; append/version; task diagnostics.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q173 What belongs in a Buildroot external tree for a custom appliance?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Keeping product changes separate and reproducible.

**Spoken answer:** Store the product's board configuration, custom package definitions, overlays or post-build steps, and documented external-tree metadata so the build can be reproduced from versioned inputs.

**Deeper explanation:** Avoid making unrecorded changes directly inside an output root filesystem and calling that the product source. A package should install files through its build rules; an overlay can supply static configuration but should not hide architecture-specific binaries. Track defconfig, source revisions, hashes, and build logs. Test startup and persistence behavior in the generated image rather than only compiling the application on the host.

**Assumptions:** Assume a pinned Buildroot release and its documented BR2_EXTERNAL layout.

**Common incorrect answer:** Copying the entire output directory into version control as the sole recipe for rebuilding.

**Follow-up:** How would you prove a clean build includes your application without manual post-build copying?

**Scoring out of 4:** 1 point each: external organization; versioned inputs; package/overlay boundary; image test.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q174 What is the difference between a rebuildable and a bit-reproducible image?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Precise reproducibility claims.

**Spoken answer:** Rebuildable means documented inputs can produce a functioning artifact again. Bit-reproducible means independent builds with the specified inputs yield identical bytes under the defined conditions.

**Deeper explanation:** Timestamps, source paths, locale, toolchain revisions, archive ordering, and external downloads can change output. Pin inputs and compare hashes, then use structured binary comparison to investigate differences. Functional equivalence is useful but weaker than byte identity. Record which artifact was compared: a root filesystem, signed bundle, compressed image, and full disk image can have different nondeterminism sources.

**Assumptions:** Assume reproducibility is evaluated against an explicit input and environment specification.

**Common incorrect answer:** Claiming reproducibility because two builds both boot or because a Docker tag was reused.

**Follow-up:** How can signature timestamps or generated filesystem UUIDs complicate bitwise comparison?

**Scoring out of 4:** 1 point each: claim distinction; input control; artifact scope; nondeterminism diagnosis.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q175 What should an SBOM contribute to an embedded product workflow?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Dependency traceability and its limits.

**Spoken answer:** A software bill of materials records components and relevant versions, identities, and relationships so maintenance, licensing, and vulnerability review have a traceable starting point.

**Deeper explanation:** Generate it from the actual build where possible and retain it with artifact hashes and configuration. An SBOM is not a vulnerability scan result or proof that all vulnerabilities are exploitable. Version strings alone may miss backported fixes, so preserve source revisions and patch context. Link component findings to deployed products and update decisions rather than producing a file no one can interpret.

**Assumptions:** Assume the selected build system and SBOM format are documented and verified for the artifact.

**Common incorrect answer:** Treating a generated SBOM as proof of security or license compliance without review.

**Follow-up:** How would you determine whether a reported vulnerability affects a feature disabled in your image?

**Scoring out of 4:** 1 point each: inventory; build linkage; backport/config context; triage limits.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q176 How do signed updates differ from secure or verified boot?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Integrity boundaries across installation and startup.

**Spoken answer:** Signed update verification authenticates an update package before accepting it under the update policy. Verified boot checks the boot chain or loaded components according to a trust model at startup.

**Deeper explanation:** One does not automatically provide the other. An accepted image could later be modified on writable storage unless boot/runtime protections address that risk. Key storage, revocation, rollback policy, and recovery paths matter in both designs. CRCs and hashes without an authenticated trust anchor detect corruption but do not prove authorization. State exactly which components and transitions are covered.

**Assumptions:** Assume a chosen update and boot framework; hardware root-of-trust claims require target evidence.

**Common incorrect answer:** Calling a checksum-secured download secure boot or assuming HTTPS alone authorizes every image.

**Follow-up:** How would you rotate an update signing key without stranding deployed devices?

**Scoring out of 4:** 1 point each: two boundaries; trust anchor; uncovered modification; key/recovery plan.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q177 What must an A/B updater do before marking a new slot good?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Health confirmation and rollback semantics.

**Spoken answer:** Boot the candidate slot, run meaningful bounded health checks, and confirm only when required functions and persistent-state compatibility meet the defined policy. Retain rollback until that decision.

**Deeper explanation:** A process merely starting may not prove its sensor path, storage, or network configuration works. Use a boot-attempt counter or framework-supported status so repeated failed boots revert. The updater should not overwrite the currently known-good slot during installation. Shared application data needs a migration strategy compatible with rollback, or rollback can boot old software against unusable new data.

**Assumptions:** Assume the bootloader and updater share a validated slot-selection protocol.

**Common incorrect answer:** Marking good immediately at the start of boot or equating two partitions with guaranteed recovery.

**Follow-up:** What health tests should run locally when the network is unavailable?

**Scoring out of 4:** 1 point each: bounded meaningful health; attempt/rollback; inactive-slot write; data compatibility.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q178 How should a CI pipeline validate an embedded change at several levels?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Test layering and honest coverage.

**Spoken answer:** Run fast host unit and parser tests, static checks, target builds, emulator integration where supported, and hardware tests for behavior that depends on the real board.

**Deeper explanation:** A change touching an I2C driver needs more than a host lint pass; a pure parser change may not require every expensive hardware test on every edit. Preserve exact inputs, artifacts, logs, and failure seeds. Separate authored, compiled, host-tested, emulator-tested, and hardware-tested evidence. Flaky tests should be investigated, not rerun silently until green.

**Assumptions:** Assume available runners and targets are explicitly listed; missing hardware gates remain pending.

**Common incorrect answer:** Reporting full validation from compile success or treating an emulator as an electrical test bench.

**Follow-up:** Which smallest regression test would you add for a malformed length-field crash?

**Scoring out of 4:** 1 point each: layers; risk-based scope; evidence labels; meaningful regression.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q179 How do you investigate boot time without optimizing the wrong stage?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Measurement boundaries and causal experiments.

**Spoken answer:** Define start and ready endpoints, measure stage durations, and identify the dominant delay before changing configuration. Bootloader, kernel, device probing, and userspace readiness are separate intervals.

**Deeper explanation:** A serial console can itself add delay, and a service manager's active state may precede useful application readiness. Record power/reset conditions, storage state, and network availability. Change one cause at a time and compare multiple runs, including outliers. Removing a timeout can improve a benchmark while damaging recovery, so retain required failure behavior in the acceptance criteria.

**Assumptions:** Assume an observable hardware or emulator start event and a product-specific readiness definition.

**Common incorrect answer:** Using only kernel timestamps as total power-on-to-service-ready time.

**Follow-up:** How would you measure a service that must initialize a sensor before it is operational?

**Scoring out of 4:** 1 point each: endpoints; stage breakdown; controlled trials; recovery tradeoff.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

### Q180 What makes a reliability test more useful than leaving a device running overnight?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**Assesses:** Targeted failure coverage and measurable acceptance.

**Spoken answer:** Define workload, faults, metrics, duration, and pass conditions, then preserve evidence. Long duration is useful only when it exercises relevant states and detects failure meaningfully.

**Deeper explanation:** A soak test can track memory, descriptor counts, reconnects, missed deadlines, and data loss. Add targeted disconnects, malformed packets, storage-full conditions, process restarts, and update interruptions according to scope. Record whether the system recovers and whether data integrity survives. A clean overnight run does not cover rare transitions that never occurred during it.

**Assumptions:** Assume a disposable test environment and explicit limits for disruptive fault injection.

**Common incorrect answer:** Calling lack of visible crashes proof of reliability while ignoring silent data loss or unbounded growth.

**Follow-up:** How would you make a storage-full failure test verify both diagnosis and recovery?

**Scoring out of 4:** 1 point each: specified workload; metrics; targeted faults; recovery/integrity criteria.

**Learning connection:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md). **Verification references:** [BUILDROOT](https://buildroot.org/downloads/manual/manual.html), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [REPRO](https://docs.yoctoproject.org/5.0.12/test-manual/reproducible-builds.html), [SBOM](https://docs.yoctoproject.org/5.0.12/dev-manual/sbom.html).

## System design exercises

### Q181 Design a bounded industrial sensor gateway using one MCU and one Linux computer.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Requirements decomposition, interfaces, and failure containment.

**Spoken answer:** Keep acquisition and local timing on the MCU, transfer versioned framed telemetry over one primary link, and let Linux validate, persist, expose health, and manage remote integration.

**Deeper explanation:** Specify sampling rate, payload bounds, queue capacity, freshness deadlines, configuration ownership, and recovery after either side resets. Start with a PTY simulator and deterministic fault injection, then add the selected board path. Use a known-good configuration and observable degraded states. Acceptance should include corrupted frames, slow consumers, storage full, restart, and incompatible versions, with separate host and hardware evidence.

**Assumptions:** Assume a learning gateway with modest telemetry volume, not an unspecified safety-critical product.

**Common incorrect answer:** Adding multiple clouds and buses before proving the primary path and recovery behavior.

**Follow-up:** How would you demonstrate that disconnecting the network cannot block MCU acquisition indefinitely?

**Scoring out of 4:** 1 point each: boundary architecture; bounded interface; recovery; measurable acceptance.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q182 Design a Linux to MCU robot control demonstrator with stale-command protection.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Control authority, simulation, and explicit safety scope.

**Spoken answer:** Linux handles planning or user commands and diagnostics; the MCU handles bounded local control, command validation, freshness, and output disable. Begin with simulated actuators and an explicit arming state.

**Deeper explanation:** Define command units, ranges, sequence/session behavior, timeout, fault latch, and recovery. Separate telemetry from control authority so a live dashboard cannot keep an old command valid. Test Linux pause, dropped frames, replay, MCU reset, and reconnect. Physical deployment needs independent hazard analysis, electrical protection, and verified stopping behavior beyond this learning design. C02’s minimum simulation resumes on a fresh valid command after ordinary command expiry; a separate arming/session handshake is an extension. Its local stop latch requires deliberate rearming.

**Assumptions:** Assume differential-drive simulation as a teaching target; no certified safety claim is made.

**Common incorrect answer:** Putting the only motion timeout in a Linux UI, or resuming motion without an explicit, justified recovery policy or while a fault remains latched.

**Follow-up:** What evidence would justify moving from simulation to wheels-off-ground hardware testing?

**Scoring out of 4:** 1 point each: responsibilities; local freshness; fault tests; staged hardware boundary.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q183 Design a character-device interface for a bounded event queue.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** ABI semantics, concurrency, and removal.

**Spoken answer:** Define record format, maximum queue size, read semantics, nonblocking behavior, poll readiness, overflow policy, and disconnection behavior before writing file operations.

**Deeper explanation:** Choose whether reads return whole records or byte streams and how too-small user buffers behave. Synchronize producers and readers, avoid sleeping under incompatible locks, and preserve state on failed user copies according to the contract. Existing opens must remain safe after device removal. Acceptance includes concurrent readers, full queue, signals, invalid user buffers, blocked read during removal, and repeated bind/unbind.

**Assumptions:** Assume an educational device; use an existing subsystem instead if it fits the real hardware.

**Common incorrect answer:** Returning inconsistent readiness and read behavior or freeing state when the node is unregistered.

**Follow-up:** How would userspace detect that records were dropped due to queue overflow?

**Scoring out of 4:** 1 point each: precise ABI; synchronization; lifetime; adversarial acceptance.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q184 Design a sensor acquisition path using Linux IIO and a user-space logger.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Subsystem reuse, units, timestamps, and data integrity.

**Spoken answer:** Expose the sensor through IIO channels and the suitable direct or buffered interface, then let a bounded userspace service decode scan metadata, validate samples, and persist records.

**Deeper explanation:** Specify rate, timestamp meaning, scaling, channel order, and overrun behavior. Keep hardware reset and register recovery in the driver while storage policy remains in userspace. Test known sensor inputs, bus errors, suspend/resume, buffer overrun, logger restart, and storage failure. A synthetic IIO or parser test validates software interpretation but does not establish analog accuracy or real interrupt timing.

**Assumptions:** Assume the selected sensor supports the required acquisition mode and a documented datasheet.

**Common incorrect answer:** Inventing a private ioctl for every channel or hard-coding raw sample bytes without metadata.

**Follow-up:** How would you correlate MCU and Linux timestamps if measurements come from both domains?

**Scoring out of 4:** 1 point each: subsystem mapping; representation/time; failure boundaries; layered validation.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q185 Design a signed A/B update workflow for a small appliance.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Trust, persistent state, and recovery transitions.

**Spoken answer:** Verify an authorized bundle, write only the inactive slot, update boot-selection metadata through the supported mechanism, boot the candidate, and confirm it after bounded health checks.

**Deeper explanation:** Define failure handling before download, during writing, during metadata changes, and after first boot. Preserve a recovery image or path and plan signing-key rotation and rollback policy. Application data migrations must not make the previous slot unusable without an explicit strategy. Test interruption points in disposable images and later on actual bootloader/storage hardware, recording each transition outcome.

**Assumptions:** Assume a selected framework such as RAUC with a compatible bootloader integration; host simulation is not deployment proof.

**Common incorrect answer:** Calling two copied directories a complete secure updater or marking good before the application works.

**Follow-up:** How would you prevent installation of an image for the wrong board revision?

**Scoring out of 4:** 1 point each: signed inactive-slot flow; boot/health; compatibility/data; interruption matrix.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q186 Design a reliable serial protocol for commands and telemetry with 128-byte payloads.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Complete protocol specification and resynchronization.

**Spoken answer:** Choose a bounded frame with version, type, length, session/request identity, payload, and CRC, plus escaping or another unambiguous framing method and explicit deadlines.

**Deeper explanation:** Specify byte order, CRC parameters, maximum encoded length, duplicate handling, and which messages require acknowledgment. A command should distinguish accepted from completed if execution is asynchronous. Recovery must handle truncation, bad length, bad CRC, unknown version, and peer restart without unbounded buffering. Provide fixed vectors and tests at every fragmentation boundary; electrical validation remains separate.

**Assumptions:** Assume an accidental-error model unless authentication is explicitly added; CRC is not a security mechanism.

**Common incorrect answer:** Using a magic prefix alone with no escape, length, or bounded resynchronization policy.

**Follow-up:** How would a firmware update preserve compatibility with an older Linux peer?

**Scoring out of 4:** 1 point each: full wire contract; semantics; bounded recovery; vectors/compatibility.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q187 Design a real-time acquisition task plus best-effort logging under overload.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Scheduling and queue policy under conflicting priorities.

**Spoken answer:** Keep acquisition bounded and independent of slow storage. Transfer samples through a fixed-capacity queue with a stated drop or backpressure policy and expose overrun counters.

**Deeper explanation:** Prioritize from deadlines and execution budgets, not component importance alone. Avoid storage calls or unbounded allocation in the acquisition path. If losing any sample is unacceptable, prove the required throughput and buffering under the specified outage duration or reduce acquisition rate by policy. Test sustained overload, not only bursts, and distinguish measured worst observed latency from a guaranteed bound.

**Assumptions:** Assume requirements state which data loss is acceptable and what local control must continue.

**Common incorrect answer:** Using an unbounded queue or blocking the acquisition ISR until a flash write finishes.

**Follow-up:** How much storage is required to survive a 30-second downstream outage at the stated sample rate?

**Scoring out of 4:** 1 point each: timing boundary; capacity arithmetic; overload policy; evidence limits.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q188 Design a diagnostic subsystem that remains useful during failure.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Observability with bounded resource and privacy costs.

**Spoken answer:** Use structured event IDs, monotonic timing, severity, bounded buffers, rate limiting, and persistent reset/fault summaries where supported. Separate high-value fault evidence from verbose tracing.

**Deeper explanation:** A log path must not block a critical control path or recursively fail while reporting its own failure. Include build identity, configuration revision, counters, and state transitions, while redacting credentials and unnecessary payloads. Define behavior when storage is full and when clocks are unsynchronized. Verify that injected failures produce actionable evidence and that excessive logging cannot exhaust memory.

**Assumptions:** Assume a learning system with a defined retention budget and no invented hardware persistence guarantees.

**Common incorrect answer:** Logging every byte synchronously in an ISR or assuming more logs always improve diagnosis.

**Follow-up:** Which five fields would you preserve for a communication timeout after a reboot?

**Scoring out of 4:** 1 point each: structured evidence; bounded path; failure/retention; useful diagnostic test.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q189 Design a small optional anomaly detector without giving it control authority.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Data methodology and safe integration boundaries.

**Spoken answer:** Collect timestamped sensor data with operating context, define a simple non-AI baseline, separate training/validation/test by run or time, and evaluate a small model in userspace.

**Deeper explanation:** Measure false alarms, missed anomalies, inference latency, memory, CPU, and model size using actual execution. Prevent leakage from near-duplicate windows across splits. Keep existing deterministic checks and a clear fallback if inference fails or data is out of distribution. The model may annotate diagnostics; it should not replace MCU timing or motion limits in this learning system.

**Assumptions:** Assume labeled or carefully characterized data exists; synthetic results must be labeled and not presented as field accuracy.

**Common incorrect answer:** Reporting training accuracy as deployed performance or running inference in a kernel interrupt handler.

**Follow-up:** How would you detect that a new sensor revision invalidates the model's input distribution?

**Scoring out of 4:** 1 point each: baseline/data split; measured evaluation; application boundary; fallback/drift.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

### Q190 Design a test strategy for a driver and firmware pair before boards arrive.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**Assesses:** Maximizing useful evidence without overstating emulation.

**Spoken answer:** Extract pure parsing and state logic for host tests, compile target code against pinned interfaces, simulate the communication peer, and use supported QEMU targets for integration where meaningful.

**Deeper explanation:** Create a hardware-validation matrix for remaining electrical, timing, DMA, interrupt, power, and peripheral behaviors. Use synthetic logs and faults with explicit labels. Test malformed packets, restart ordering, queue overflow, and teardown now, preserving command lines and outputs. When boards arrive, prioritize the highest-risk assumptions rather than repeating only happy-path software tests.

**Assumptions:** Assume emulator device models do not reproduce every selected physical peripheral.

**Common incorrect answer:** Calling host compilation hardware validation or delaying all testing until every board is available.

**Follow-up:** Which failure would you expect a PTY test to reveal, and which requires a logic analyzer?

**Scoring out of 4:** 1 point each: portable logic; target build/simulation; explicit gaps; risk-based hardware plan.

**Learning connection:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md). **Verification references:** [IIO](https://docs.kernel.org/6.12/driver-api/iio/intro.html), [RAUC](https://rauc.readthedocs.io/en/latest/basic.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [QEMU](https://www.qemu.org/docs/master/system/index.html).

## Project defense behavioral and AI judgment

### Q191 How would you explain a project you built with AI assistance honestly?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Ownership, understanding, and evidence.

**Spoken answer:** Describe the problem, your decisions and implementation work, where AI assisted, how you verified suggestions, and which results you personally reproduced. Separate generated code from demonstrated competence.

**Deeper explanation:** A credible explanation can say that AI proposed parser edge cases while you defined the protocol, reviewed code, wrote tests, and diagnosed a failing case. Do not invent percentages or claim independent authorship of work you cannot explain. Prepare to modify one requirement live and predict which tests change. Keep provenance and validation notes with the project.

**Assumptions:** Assume the interview permits discussion of AI-assisted personal projects; obey its stated tool rules.

**Common incorrect answer:** Hiding material assistance or claiming all generated code is correct because it compiled once.

**Follow-up:** Which AI suggestion did you reject, and what evidence led you to reject it?

**Scoring out of 4:** 1 point each: truthful role; decisions; independent verification; live understanding.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q192 What should you say when you do not know an API or answer?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Intellectual honesty and a useful investigation method.

**Spoken answer:** State the boundary of your knowledge, explain the relevant principles you do know, and outline how you would verify the missing detail from the selected version's documentation or source.

**Deeper explanation:** For example, distinguish confidence in a lifetime requirement from uncertainty about one helper's exact signature. Ask permission to consult documentation when the interview format allows it. Avoid inventing a plausible function name or presenting a guess as fact. A structured hypothesis with a proposed check is stronger than a memorized but unsupported claim.

**Assumptions:** Assume the interviewer has specified whether documentation or coding tools are allowed.

**Common incorrect answer:** Bluffing an API or answering only that you do not know without showing any reasoning.

**Follow-up:** How would you test whether a helper cancels in-flight work synchronously?

**Scoring out of 4:** 1 point each: knowledge boundary; valid principle; verification plan; honest uncertainty.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q193 How do you turn a learning project into a credible resume bullet?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Evidence-based claims and personal contribution.

**Spoken answer:** State what you built, the relevant technical responsibility, and a measured result or verified capability with its test scope. Use numbers only when recorded evidence supports them.

**Deeper explanation:** A template is: built a bounded serial telemetry parser in C; added fragmentation and malformed-frame tests; verified the listed host cases and documented hardware checks still pending. Replace template fields only after completion. Avoid calling a simulator production deployment or inventing latency improvements. Link the repository, reproducible command, and a short demonstration when appropriate.

**Assumptions:** Assume no employer or production experience beyond what the candidate actually has.

**Common incorrect answer:** Writing improved reliability by 80 percent without a baseline, metric, workload, and recorded result.

**Follow-up:** How would you phrase a kernel module that compiles but has not yet been loaded on its target?

**Scoring out of 4:** 1 point each: concrete artifact; personal work; scoped evidence; truthful limitations.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q194 How should you defend a design decision that has a clear drawback?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Tradeoff reasoning and willingness to revise.

**Spoken answer:** State the requirement that drove the choice, alternatives considered, its cost, and the evidence that made the tradeoff acceptable. Explain what change would cause you to revisit it.

**Deeper explanation:** For a fixed-size queue, bounded memory may outweigh occasional telemetry loss if loss is counted and the product permits it. That defense fails if every sample is required. Use actual constraints rather than personal preference, and distinguish a deliberate learning shortcut from a production recommendation. Acknowledge evidence that weakens the decision instead of defending it reflexively.

**Assumptions:** Assume requirements and test evidence are available for the project being discussed.

**Common incorrect answer:** Saying the chosen tool is always best or pretending there were no disadvantages.

**Follow-up:** What specific requirement change would make your current queue policy unacceptable?

**Scoring out of 4:** 1 point each: requirement; alternatives/cost; evidence; revision trigger.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q195 How do you answer a behavioral question about a failure without inventing experience?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Reflection, accountability, and truthful scope.

**Spoken answer:** Use a real work, study, or personal-project example. Explain the situation, your responsibility, the action you took, the observed outcome, and what you changed afterward.

**Deeper explanation:** A small debugging mistake can demonstrate sound judgment if you identify its consequence and prevention. Do not inflate a class project into a production incident or attribute a team's work solely to yourself. If you have no relevant example, say so and discuss a related genuine situation, clearly labeling hypothetical approaches as hypothetical.

**Assumptions:** Assume the candidate's actual history has not been supplied; all answer structures are templates.

**Common incorrect answer:** Memorizing a fabricated rescue story or removing every sign of personal responsibility.

**Follow-up:** What permanent change in your test or review process resulted from that experience?

**Scoring out of 4:** 1 point each: real context; personal responsibility; observable outcome; learning action.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q196 An AI suggests a kernel helper that is absent from your headers. What is your workflow?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Version-aware verification and resisting plausible inventions.

**Spoken answer:** Check the exact target source and documentation, determine whether the helper exists in another version or subsystem, and redesign against supported APIs rather than forcing an undeclared symbol.

**Deeper explanation:** Provide the model with kernel version, configuration, relevant declarations, and the actual build error. Ask it to identify evidence for every proposed API. Compile a focused change and run the tests relevant to lifetime and failure behavior. A function with a similar name may have different context or ownership semantics, so replacing names mechanically is unsafe.

**Assumptions:** Assume access to the pinned kernel tree and permission to share the code context being used.

**Common incorrect answer:** Adding a hand-written prototype for an unavailable function or trusting a confident generated explanation.

**Follow-up:** How would you distinguish a missing Kconfig dependency from a completely invented API?

**Scoring out of 4:** 1 point each: source check; version/context; supported redesign; focused validation.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q197 How can AI-generated tests give false confidence?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Independent oracles and adversarial test design.

**Spoken answer:** A model may repeat the implementation's assumptions, test only happy paths, or assert the same incorrect formula. Use independently specified behavior and fixed external vectors where appropriate.

**Deeper explanation:** For CRC, test a known check value rather than only encode-decode round trips. For a parser, include every fragmentation boundary, malformed lengths, and bounded recovery. Mutation testing can show whether tests detect intentional defects, but does not prove completeness. Review expected outputs before running them and keep at least one assessment independent of AI assistance.

**Assumptions:** Assume tests are used as engineering evidence, not as proof of exhaustive correctness.

**Common incorrect answer:** Counting many generated test functions as coverage without examining their assertions.

**Follow-up:** Which single mutation would reveal whether your overflow test actually exercises the overflow branch?

**Scoring out of 4:** 1 point each: independent oracle; edge cases; mutation limit; independent competence.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q198 How would you present benchmark results from an emulator or shared host?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Measurement honesty and practical limits.

**Spoken answer:** State platform, configuration, workload, sample count, clock, measurement method, and interference conditions. Report observed distributions and avoid treating them as target hardware guarantees.

**Deeper explanation:** Compare changes under the same conditions and preserve raw data. A noisy shared host can still reveal a large algorithmic regression, but tail latency may reflect host scheduling. Do not invent before/after numbers or call one fast run an improvement. Hardware timing, cache behavior, bus delays, and physical control performance remain separate measurements.

**Assumptions:** Assume the benchmark was actually executed; otherwise label the metric as a proposed acceptance target.

**Common incorrect answer:** Reporting an emulator's best latency as the robot's worst-case response time.

**Follow-up:** What measurements would you repeat first when the selected board becomes available?

**Scoring out of 4:** 1 point each: method metadata; distributions; comparison control; scope limits.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q199 How should you prioritize preparation when a JD contains far more topics than you can master soon?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Requirement extraction and evidence-based gap closure.

**Spoken answer:** Separate explicit must-haves from nice-to-haves and inferred suggestions, map each to evidence, and prioritize shared foundations plus the target track's essential practical tasks.

**Deeper explanation:** Mark unassessed skills as unassessed rather than assigning optimistic scores. For a driver role, strengthen C, context/locking, resource lifetime, bus/subsystem knowledge, and one defensible driver project before optional cloud breadth. A firmware role may instead prioritize startup, interrupts, RTOS timing, and hardware debugging. Reassess after a timed mock and use failures to choose remediation.

**Assumptions:** Assume an actual JD is supplied; otherwise call the matrix a reference framework.

**Common incorrect answer:** Treating one employer's stack as universal or learning every keyword to the same depth.

**Follow-up:** Which missing evidence would most change your confidence in readiness for this specific role?

**Scoring out of 4:** 1 point each: explicit/inferred split; evidence; role priority; reassessment.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

### Q200 What demonstrates interview readiness beyond knowing 200 answers?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**Assesses:** Transfer of knowledge into implementation and explanation.

**Spoken answer:** Solve representative tasks independently, debug unfamiliar failures methodically, explain tradeoffs and limitations, and defend a reproducible project with actual evidence under time constraints.

**Deeper explanation:** Use the bank for retrieval practice, then change inputs, requirements, and failure modes so memorized wording is insufficient. A readiness gate should include no critical correctness failures, a passing practical task, a role-specific mock, and an honest project demonstration. Selection also depends on role fit and interview conditions, so preparation cannot guarantee an offer.

**Assumptions:** Assume the candidate has completed foundations and the relevant track projects, not merely read the answer file.

**Common incorrect answer:** Equating a high multiple-choice score or an AI-produced repository with independent engineering competence.

**Follow-up:** Can you change one protocol requirement live, update tests, and explain the new failure modes?

**Scoring out of 4:** 1 point each: independent task; debugging; project evidence; realistic readiness limits.

**Learning connection:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md). **Verification references:** [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [KERNEL](https://docs.kernel.org/6.12/driver-api/driver-model/index.html), [FREERTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), [YOCTO](https://docs.yoctoproject.org/5.0.12/dev-manual/layers.html).

