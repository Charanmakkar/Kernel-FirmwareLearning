# Interview questions only

Attempt without opening Answers.md. Record reasoning, uncertainties, test cases, and time used. A module link is a remediation route, not permission to consult answers during an independent timed attempt.

## C objects and behavior

### Q001 How are an array and a pointer different when passed to a function?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Object representation, parameter adjustment, and bounded API design.

**Extension prompt:** How would you express read-only access and document whether null is valid at length zero?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q002 Explain storage duration, scope, and linkage using a static local variable.

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Separating three language concepts that affect firmware state.

**Extension prompt:** How would you refactor this into an explicit per-instance context with a reset operation?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q003 What do const placement and volatile placement actually promise?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Type qualifiers and the boundary between language semantics and hardware access.

**Extension prompt:** Why might reading a status register twice be incorrect even when both reads are volatile?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q004 Classify signed overflow and unsigned wraparound.

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Integer contracts and avoiding optimization-sensitive bugs.

**Extension prompt:** How would you safely check `count * element_size` before allocating?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q005 Why can comparing a negative int with an unsigned length surprise you?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Usual arithmetic conversions and length validation.

**Extension prompt:** How do you handle `read()` returning -1 before comparing its result with a buffer size?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q006 Is `printf("%d %d", i++, i++)` guaranteed to print a particular pair?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Recognizing undefined behavior instead of guessing evaluation order.

**Extension prompt:** Give an expression with unspecified evaluation order that does not have undefined behavior.

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q007 What makes returning a pointer to a local array unsafe?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Object lifetime and ownership at function boundaries.

**Extension prompt:** How would the API report required size when the supplied buffer is too small?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q008 Why is memcpy not a safe replacement for memmove on overlapping regions?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Library preconditions and reasoning about aliasing.

**Extension prompt:** Does using memmove also solve a destination buffer overflow?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q009 Can a received byte buffer be cast directly to a C packet structure?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Alignment, object representation, endianness, and defensive decoding.

**Extension prompt:** How would you validate a length field without overflowing `header_size + payload_size`?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q010 Why is bit-field layout unsuitable for a portable wire protocol?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Distinguishing convenient source notation from an interchange representation.

**Extension prompt:** What additional precautions apply when the destination is a hardware status register?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q011 When is a shift expression undefined or implementation-defined?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Boundary conditions in bit operations.

**Extension prompt:** How would you construct a full-width mask without evaluating `1u << width`?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q012 Explain strict aliasing and a safe way to inspect a float's bytes.

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Access type rules and representation inspection.

**Extension prompt:** How would you serialize a floating measurement for heterogeneous machines?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q013 What is the difference between a null pointer and an uninitialized pointer?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Initialization and error-resistant API contracts.

**Extension prompt:** Why is `memset(&p, 0, sizeof p)` a weaker portable initialization than `p = NULL`?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q014 How should realloc failure be handled without losing the original allocation?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Ownership-preserving allocation and size contracts.

**Extension prompt:** What happens to a pointer into the old allocation after a successful relocation?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q015 What can a function pointer safely represent in a driver-like C interface?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Typed callbacks, context ownership, and dispatch.

**Extension prompt:** How would cancellation work when a callback may already be running?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q016 How do alignment and structure padding affect an embedded ABI?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Memory layout versus source-field intuition.

**Extension prompt:** Which problems can appear when a packed member is passed to a function expecting aligned storage?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q017 What makes a C API reentrant, and how is that different from thread safe?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** State isolation and nested-call reasoning.

**Extension prompt:** Can a function with only local variables still be non-reentrant because of a callee?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q018 Why does volatile not fix a shared-counter data race?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** The C memory model and atomic read-modify-write.

**Extension prompt:** When would acquire-release ordering be needed instead of a relaxed counter increment?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q019 What does undefined behavior imply for a code-output interview question?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Disciplined reasoning under missing language guarantees.

**Extension prompt:** How would you explain an optimization-sensitive crash to a colleague without blaming the compiler prematurely?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

### Q020 How do you choose between fixed allocation, a pool, and general heap allocation?

**Track:** Shared | **Difficulty:** Foundation | **Round:** Technical screen | **Tags:** conceptual;code-analysis

**What is assessed:** Resource budgeting and failure behavior in embedded software.

**Extension prompt:** How will the system behave when the pool is empty, and how will that be observed?

**Remediation:** [Module M02](../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

## C coding exercises

### Q021 Implement checked multiplication for two size_t values before allocation.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Overflow prevention without evaluating an already-overflowed result.

**Extension prompt:** How would you add a header size to the multiplication result safely?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q022 Write a bounds-checked big-endian 16-bit decoder from bytes.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Portable byte decoding and a clear error interface.

**Extension prompt:** How would the interface advance a cursor only when decoding succeeds?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q023 Implement an eight-byte ring buffer with explicit full and empty states.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Capacity invariants, wraparound, and overload policy.

**Extension prompt:** How would a single-producer single-consumer atomic implementation publish an element safely?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q024 Convert an even-length ASCII hexadecimal string into a bounded byte buffer.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Validation, capacity checks, and transactional parsing.

**Extension prompt:** When would a streaming decoder with partial progress be a better contract?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q025 Reverse a byte array in place without accessing beyond either end.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Index invariants and zero-length handling.

**Extension prompt:** How would reversing UTF-8 bytes differ from reversing user-visible characters?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q026 Set or clear a selected bit in a uint32_t without undefined shifts.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Bit-width validation and preserving unrelated bits.

**Extension prompt:** How would an atomic shared flags word change the implementation?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q027 Implement CRC-16/CCITT-FALSE and verify a known check value.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Protocol interoperability and complete CRC parameterization.

**Extension prompt:** What wire byte order will you choose for the two CRC bytes, and why specify it separately?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q028 Parse a decimal uint32_t with no trailing characters or overflow.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Defensive conversion of external text.

**Extension prompt:** How would you support optional base prefixes without silently accepting octal unexpectedly?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q029 Write a bounded string copy that reports truncation explicitly.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** C string termination and useful caller-visible status.

**Extension prompt:** When would rejecting the entire operation be preferable to writing a truncated prefix?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q030 Implement a saturating addition of two uint32_t values.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Deliberate arithmetic policy instead of accidental wraparound.

**Extension prompt:** How would you extend the interface to return a separate overflow flag?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q031 Implement a debounced boolean input state machine using sample counts.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** State transitions, noisy input handling, and bounded state.

**Extension prompt:** How would the design change to debounce by monotonic timestamps instead of sample count?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q032 Implement an integer moving average over the most recent four samples.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Window maintenance, startup behavior, and accumulator range.

**Extension prompt:** How would you detect the maximum required accumulator width for a configurable window?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q033 Insert a uint32_t into a sorted fixed-capacity array.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Bounds, shifting, and a precise duplicate policy.

**Extension prompt:** When would a heap or bitmap be a better data structure than a sorted array?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q034 Compare a wrapping 32-bit tick counter against a deadline safely.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Modular-time assumptions and half-range ambiguity.

**Extension prompt:** How would you handle a timer that may be suspended longer than half a counter cycle?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q035 Detect a cycle in a singly linked list using constant extra space.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Pointer traversal invariants and algorithmic reasoning.

**Extension prompt:** How would you find the entry point of the cycle after detecting a meeting?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q036 Count the set bits in a uint32_t without a 32-iteration loop.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Bit identities and complexity that depends on input.

**Extension prompt:** When would a table, intrinsic, or constant-step method be preferable?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q037 Round a size_t up to a power-of-two alignment without overflow.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Alignment preconditions and checked arithmetic.

**Extension prompt:** How would you round up to a non-power-of-two block size safely?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q038 Validate a sequence of one-byte-type one-byte-length TLV records.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Length-driven parsing and progress guarantees.

**Extension prompt:** How would you cap nesting depth if a type contains another TLV sequence?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q039 Implement hysteresis for a high-temperature alarm.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Stateful threshold behavior and boundary precision.

**Extension prompt:** What should happen when the sensor reading is invalid or stale?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

### Q040 Replace a bounded bit field in a uint32_t while preserving other bits.

**Track:** Shared | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Bit-range validation, mask construction, and overflow-free shifts.

**Extension prompt:** How would you adapt the interface to extract the same field and verify encode-decode vectors?

**Remediation:** [Module M03](../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

## Tools linking and C++

### Q041 Explain preprocessing, compilation, assembly, and linking using one missing-symbol error.

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Locating a build failure at the correct stage.

**Extension prompt:** How would C++ name mangling affect linking a C library?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q042 What information can readelf and a linker map reveal that source code cannot?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Binary-level verification of a firmware build.

**Extension prompt:** Why might `.bss` consume RAM while contributing little payload to the image file?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q043 What is the difference between an ABI and an API?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Compatibility across compilation and runtime boundaries.

**Extension prompt:** Which ABI evidence would you collect when a cross-compiled program crashes immediately?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q044 How does RAII improve resource handling in C++ system code?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Lifetime-bound cleanup and ownership transfer.

**Extension prompt:** How would you expose an explicit finalize operation for a resource whose release can fail?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q045 When would you use unique_ptr, shared_ptr, or a nonowning pointer?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Ownership communication and avoiding unnecessary shared lifetime.

**Extension prompt:** How do you prevent a callback from using a borrowed object after shutdown?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q046 How would you make a Make or CMake build reproducible enough to investigate a regression?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Controlled inputs and traceable build configuration.

**Extension prompt:** How would you identify why two nominally identical ELF files differ?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q047 Why can a static library link fail depending on command-line order?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Archive extraction and dependency direction.

**Extension prompt:** What do archive groups change, and why can excessive circular dependencies signal a design problem?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q048 What should a useful embedded code review examine beyond formatting?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Risk-focused review of interfaces and failure paths.

**Extension prompt:** What evidence would justify accepting a known limitation in a learning demonstrator?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q049 How do you use git bisect without misdiagnosing an intermittent fault?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Controlled experimentation over source history.

**Extension prompt:** How would you handle a bisect step that cannot build with the current host toolchain?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

### Q050 What do compiler warnings, static analysis, and sanitizers each contribute?

**Track:** Shared | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Understanding complementary verification tools and their limits.

**Extension prompt:** How would you design input generation to exercise a parser beyond its normal examples?

**Remediation:** [Module M04](../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

## Linux process and I O fundamentals

### Q051 How do a process, a thread, and a file descriptor differ?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Basic Linux resource and execution models.

**Extension prompt:** How can close followed by open in another thread create a subtle reuse bug?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q052 Why must a read or write loop handle partial progress?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Correct byte-stream I/O and error semantics.

**Extension prompt:** What timeout should cover the whole operation instead of restarting after every short transfer?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q053 What is the difference between blocking mode and readiness notification?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Avoiding event-loop stalls and race assumptions.

**Extension prompt:** How should the loop handle a socket that is readable because its peer closed cleanly?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q054 When should you choose poll instead of epoll, or epoll instead of poll?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Scale-sensitive design without premature complexity.

**Extension prompt:** What would you measure to justify migrating a 12-descriptor daemon from poll?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q055 How should a daemon shut down cleanly after SIGTERM?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Signal safety and coordinated resource lifetime.

**Extension prompt:** How would you guarantee that a worker blocked on a condition variable notices shutdown?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q056 What are /proc, /sys, and /dev used for?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Kernel interfaces and choosing a stable observation method.

**Extension prompt:** Why is parsing `/proc/PID/stat` by simply splitting on spaces unsafe for the command field?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q057 How do fork and exec interact with descriptors and memory?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Process creation and deliberate inheritance.

**Extension prompt:** Why can logging with a library mutex in the post-fork child deadlock?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q058 What does fsync add beyond a successful write?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Durability and failure-aware persistence.

**Extension prompt:** How would you test interrupted configuration updates without damaging real user data?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q059 Why should timeouts normally use a monotonic clock?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Deadline correctness under wall-clock adjustments.

**Extension prompt:** How would you define whether a command timeout should elapse while a laptop is suspended?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q060 What does least privilege mean for an embedded Linux service?

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Technical screen | **Tags:** conceptual

**What is assessed:** Reducing the consequences of parser or network failures.

**Extension prompt:** How would you verify that an update helper has narrowly scoped authority?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

## Linux coding exercises

### Q061 Write a complete-write helper for a blocking descriptor with EINTR handling.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Progress tracking and syscall error handling.

**Extension prompt:** How would you add cancellation and an absolute deadline for a nonblocking socket?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q062 Read a text file whose length is unknown without trusting stat size.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Dynamic input handling and growth limits.

**Extension prompt:** How would you distinguish allocation failure from exceeding the configured maximum?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q063 Build a poll loop that reads a pipe and exits when a control pipe signals shutdown.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Multiplexing, readiness, and shutdown ownership.

**Extension prompt:** What if the control pipe fills before a shutdown request is written?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q064 Implement a bounded newline decoder for fragmented stream input.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Streaming parser state and overflow recovery.

**Extension prompt:** How would binary framing differ when the payload may legitimately contain newline?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q065 Implement a monotonic deadline helper returning milliseconds remaining.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Time arithmetic, rounding, and poll integration.

**Extension prompt:** How would you expose an infinite timeout distinctly from an expired timeout?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q066 Write a subprocess launcher that captures exit status without leaking descriptors.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Process lifecycle and error-channel design.

**Extension prompt:** How would you enforce a subprocess timeout and avoid orphaning grandchildren?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q067 Write a TCP request parser that accepts a 16-bit length followed by payload.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Message framing over a stream and memory limits.

**Extension prompt:** How do you prevent queued complete messages from exhausting memory when the consumer is slow?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q068 Implement atomic replacement of a small configuration file with error checking.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Persistence sequencing and recovery from partial failure.

**Extension prompt:** How would you handle concurrent writers so a stale update does not overwrite a newer configuration?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q069 Implement a bounded producer-consumer queue with clean shutdown.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Condition-variable predicates and lifetime-safe concurrency.

**Extension prompt:** How would you report that a producer's item was rejected because shutdown began?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

### Q070 Parse a /proc PID stat record robustly enough to extract state and PID.

**Track:** Embedded Linux | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Parsing a kernel text interface with nontrivial delimiters.

**Extension prompt:** How would you avoid accidentally associating observations from a reused PID with the old process?

**Remediation:** [Module M06](../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

## Concurrency and IPC

### Q071 Why must a condition variable be paired with a predicate and mutex?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Lost-wakeup prevention and state-based waiting.

**Extension prompt:** When should shutdown broadcast rather than signal one waiter?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q072 How does deadlock differ from starvation and livelock?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Classifying lack of progress and selecting evidence.

**Extension prompt:** How would a global lock ordering prevent the two-lock example?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q073 When is an atomic counter insufficient to protect a data structure?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Atomicity versus compound invariants.

**Extension prompt:** What linearization point would you choose for a successful queue push?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q074 What is priority inversion, and what does priority inheritance solve?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Scheduling interactions through shared resources.

**Extension prompt:** What would you measure to separate inversion from an intrinsically long critical section?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q075 How should shared memory between processes be synchronized?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Cross-process lifetime, initialization, and publication.

**Extension prompt:** How would you recover if a writer dies halfway through updating a multi-field record?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q076 What is backpressure, and where should it appear in telemetry systems?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Bounded resource usage under overload.

**Extension prompt:** How would you expose overload in health metrics without producing even more unbounded logs?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q077 Why is cancellation harder than adding a stop flag?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Interrupting waits and coordinating object lifetime.

**Extension prompt:** How would you guarantee exactly one completion callback for a request canceled at the same time it succeeds?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q078 What is false sharing, and how would you establish that it matters?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Cache effects versus correctness failures.

**Extension prompt:** How would you compare padded and unpadded layouts without changing unrelated benchmark conditions?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q079 What does lock-free mean, and what does it not guarantee?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Progress guarantees and realistic use of atomics.

**Extension prompt:** How would you reclaim a node while another thread may still hold its address?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

### Q080 When would you choose a pipe, Unix socket, shared memory, or message queue?

**Track:** Embedded Linux and Kernel | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Selecting IPC from semantics instead of preference.

**Extension prompt:** How would you version messages so independently updated peers can reject incompatible requests safely?

**Remediation:** [Module M07](../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

## Linux debugging scenarios

### Q081 A daemon uses 100 percent CPU after its serial peer disconnects. What do you inspect?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Evidence-led diagnosis of an event-loop spin.

**Extension prompt:** How would you avoid a new busy loop if reconnect itself fails immediately?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q082 A parser passes whole-frame tests but fails on real UART traffic. What is likely missing?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Transport-independent framing and fragmentation tests.

**Extension prompt:** How would a partial frame time out without discarding a valid following frame?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q083 A process reports ENOENT when executing a file that visibly exists. How can that happen?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** ELF interpreter and script-launch dependencies.

**Extension prompt:** How would a static binary change the deployment requirements, and what would it not solve?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q084 A service works as root but fails under its intended account. How do you fix it?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Permission analysis without weakening the entire system.

**Extension prompt:** How would a udev rule make the device permission persistent across reboot and reconnect?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q085 Memory usage grows slowly while the process stays responsive. How do you separate a leak from caching?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Resource accounting and experiment design.

**Extension prompt:** What evidence would show that cancellation paths leak request objects?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q086 A multithreaded application hangs only during shutdown. What is your first investigation?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Wait dependencies and destruction ordering.

**Extension prompt:** How would you make a shutdown test deterministic instead of using arbitrary sleeps?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q087 A network request sometimes contains duplicated bytes. What write-loop bug would you check?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Partial-write bookkeeping and reproducible transport tests.

**Extension prompt:** How would you safely retry a command when the connection drops after the server may have applied it?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q088 A periodic task drifts farther behind each minute. What timing pattern is suspect?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Periodic scheduling with absolute versus relative deadlines.

**Extension prompt:** What policy would you choose if one cycle takes three times the nominal period?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q089 A cross-compiled program crashes on one board but passes on the host. What do you compare?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Architecture-sensitive faults and environment differences.

**Extension prompt:** How would you verify that gdbserver and the debugger agree on the target's symbols and architecture?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q090 A configuration file becomes empty after power loss. What is wrong with a direct overwrite?

**Track:** Embedded Linux | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Crash-consistent updates and evidence-based persistence.

**Extension prompt:** How would the application choose between two versioned configuration records after a torn write?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

## Concurrency and fault analysis scenarios

### Q091 A counter occasionally loses increments despite being volatile. How do you demonstrate the defect?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Data-race diagnosis and independent verification.

**Extension prompt:** What if the counter also indicates that a corresponding data buffer is ready?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q092 A consumer sleeps although the queue contains data. What lost-wakeup pattern do you inspect?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Atomic relationship between predicate checks and sleeping.

**Extension prompt:** How can multiple consumers turn a single if check into an empty-queue access after wakeup?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q093 A two-thread program locks up after each thread takes a different mutex. What is the repair?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Lock-order deadlock and design-level prevention.

**Extension prompt:** How would lockdep or an application lock-order assertion help catch future inversions?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q094 A timer callback accesses freed state after device removal. What lifetime ordering is missing?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Asynchronous activity teardown and use-after-free prevention.

**Extension prompt:** How can calling a synchronous cancellation routine while holding a callback-needed lock deadlock?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q095 A driver fails with a sleeping-in-atomic-context warning. What do you inspect?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Execution context and API preconditions.

**Extension prompt:** How would you divide a hardware interrupt handler from deferred processing?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q096 A low-priority logger causes a high-priority control task to miss deadlines. How can this occur?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Priority inversion through a shared resource.

**Extension prompt:** What information must be logged to separate inversion from CPU overload?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q097 A device works until runtime suspend is enabled. Where do you start?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Power-state-dependent resources and access lifetimes.

**Extension prompt:** What state must be replayed after a power domain loses register contents?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q098 A DMA buffer contains stale data on one architecture. What could host testing have missed?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** DMA ownership, cache coherency, and address domains.

**Extension prompt:** How would an IOMMU make a physical-address assumption fail?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q099 A firmware task resets under heavy logging but never in the debugger. What hypotheses fit?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** Timing perturbation, stack usage, and watchdog diagnosis.

**Extension prompt:** How would you distinguish stack overflow from a watchdog timeout that occurs while interrupts are disabled?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

### Q100 An update passes in normal testing but bricks the device after power interruption. What was missing?

**Track:** Shared | **Difficulty:** Intermediate | **Round:** Debugging round | **Tags:** debugging;scenario

**What is assessed:** State-transition fault injection and recovery guarantees.

**Extension prompt:** How should persistent application data remain compatible with rollback to the previous software?

**Remediation:** [Module M15](../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

## Architecture boot and device tree

### Q101 How is a Linux application processor different from a typical microcontroller target?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Platform assumptions and selecting the correct software model.

**Extension prompt:** Which portions of a packet parser could be shared unchanged across both targets?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q102 What do an MMU and an MPU each provide?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Memory protection and address-translation concepts.

**Extension prompt:** How would a DMA engine's access differ from CPU accesses checked by an MPU?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q103 Describe a representative embedded Linux boot path without assuming every board uses U-Boot.

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Boot-stage responsibilities and platform-specific qualification.

**Extension prompt:** What evidence distinguishes a kernel decompression failure from a missing root filesystem?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q104 How do initramfs and a persistent root filesystem differ?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Early userspace and root transition.

**Extension prompt:** Why might a storage driver need to be built into the kernel rather than available only as a module?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q105 What belongs in device tree, and what belongs in a driver?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Hardware description versus implementation policy.

**Extension prompt:** Why is a binding a compatibility interface that deserves review beyond one driver revision?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q106 What are pin control and GPIO control responsible for?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Avoiding confusion between pad configuration and logical line access.

**Extension prompt:** What happens if a pin is still muxed to UART while a GPIO consumer toggles it?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q107 Why are clocks and regulators explicit driver resources?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Dependency management and power-aware initialization.

**Extension prompt:** How would you distinguish an absent regulator driver from a wrong voltage or enable pin in the board description?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q108 What does a cross-compilation sysroot contain, and why is it important?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Target headers and libraries versus host contamination.

**Extension prompt:** How can pkg-config accidentally supply host include paths during a cross build?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q109 How does an interrupt differ from polling, and when can polling be reasonable?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Latency, load, and execution-context tradeoffs.

**Extension prompt:** How would you prevent a level-triggered interrupt storm caused by an uncleared source?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

### Q110 What is memory ordering, and why can it matter even with coherent caches?

**Track:** Kernel BSP and Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Visibility order across cores or devices.

**Extension prompt:** Why does a cache flush not by itself establish a complete concurrent object-lifetime protocol?

**Remediation:** [Module M08](../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

## Kernel internals and lifetime

### Q111 Why should most application logic remain in user space?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Privilege boundaries and choosing the narrowest kernel responsibility.

**Extension prompt:** What evidence would justify moving part of a data path closer to the kernel?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q112 What are process context and interrupt context in kernel code?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Allowed operations and who may sleep.

**Extension prompt:** Which context would you choose for an I2C transaction triggered by a GPIO interrupt?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q113 How do kmalloc, vmalloc, and DMA allocation serve different needs?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Address-space, contiguity, and device access requirements.

**Extension prompt:** How would a scatter-gather-capable device change the buffer design?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q114 How do a mutex and a spinlock differ in the kernel?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Lock selection based on context and critical-section behavior.

**Extension prompt:** Why might holding a spinlock across copy_to_user be invalid?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q115 What does a wait queue solve in a blocking character driver?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** State-based blocking and wakeup races.

**Extension prompt:** What should a blocked read return if the device is disconnected?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q116 Why does devm allocation not eliminate the need for a removal design?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Managed resource scope versus asynchronous lifetime.

**Extension prompt:** How would you handle a user process keeping a character device open during unbind?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q117 What is the core idea of Read Copy Update?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Read-mostly synchronization and delayed reclamation.

**Extension prompt:** When would a reference count be needed in addition to an RCU read-side critical section?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q118 How do workqueues differ from doing everything in an interrupt handler?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Deferred processing and cancellation.

**Extension prompt:** How would you preserve ten rapid events when one work item is already pending?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q119 What is a kernel oops, and how should its evidence be preserved?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Crash interpretation without inventing a root cause.

**Extension prompt:** How would you distinguish a use-after-free from a simple null dereference using additional evidence?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

### Q120 Why must an out-of-tree module match the target kernel build?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Internal API and configuration compatibility.

**Extension prompt:** What evidence would you collect for an unknown-symbol error at insertion time?

**Remediation:** [Module M09](../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

## Driver review scenarios

### Q121 A platform driver's probe never runs. What matching evidence do you inspect?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Enumeration, binding, and build configuration.

**Extension prompt:** How would you verify the compatible string in the live device tree?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q122 Probe returns EPROBE_DEFER repeatedly. Is this always a bug in the driver?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Supplier dependencies and correct deferral.

**Extension prompt:** What happens when the supplier's driver is built as a module but never packaged in the image?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q123 A read method directly dereferences the user's buffer pointer. What is wrong?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** User/kernel trust boundary and fault handling.

**Extension prompt:** How would you avoid consuming an entire FIFO item when copying it to userspace fails partway?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q124 A blocking read never wakes when a writer adds data. Where can the bug be?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Consistency of wait predicates and notification.

**Extension prompt:** How should two readers behave when only one byte becomes available?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q125 Poll reports readable but the next read blocks. Is the driver necessarily wrong?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Readiness races and API consistency.

**Extension prompt:** What ordering avoids missing a state change between checking readiness and registering a waiter?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q126 A driver leaks memory whenever the second initialization step fails. How do you repair it?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Error-path ownership and acquisition order.

**Extension prompt:** Why might unregistering a visible interface need synchronization before freeing its backing object?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q127 A driver's ioctl works for 64-bit applications but fails for 32-bit userspace. What do you inspect?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Stable UAPI layout and compatibility handling.

**Extension prompt:** How would you verify structure offsets in both a 32-bit and 64-bit test build?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q128 A GPIO interrupt handler triggers continuously after the first event. What evidence matters?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Interrupt polarity, triggering, and source acknowledgment.

**Extension prompt:** How do you prevent repeated handling while a threaded handler services a level-triggered source?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q129 A device is removed while a process is blocked in read. What behavior must the driver define?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Disconnect semantics and object lifetime beyond unbind.

**Extension prompt:** How would you make close safe after the underlying hardware has disappeared?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

### Q130 A custom character driver duplicates a standard sensor interface. When should it be redesigned?

**Track:** Kernel BSP | **Difficulty:** Intermediate | **Round:** Driver review | **Tags:** debugging;scenario

**What is assessed:** Subsystem selection and long-term interface cost.

**Extension prompt:** Which sensor features would you map to IIO channels, events, and buffered acquisition?

**Remediation:** [Module M10](../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

## Buses sensors DMA and power

### Q131 Compare UART, I2C, and SPI from an integration perspective.

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Bus semantics and electrical/software responsibilities.

**Extension prompt:** Which measurements would you collect when a peripheral occasionally returns all 0xff bytes?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q132 What does an I2C register read typically require, and what must be checked?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Transactions, repeated starts, and device-specific behavior.

**Extension prompt:** How would you handle an address conflict between two identical fixed-address sensors?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q133 What SPI parameters must agree between controller configuration and peripheral expectations?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Clocking, framing, and transaction boundaries.

**Extension prompt:** How would you detect a one-bit sampling shift in a known device-ID response?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q134 Why does IIO expose raw values and scale rather than only a floating-point value?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Measurement representation and subsystem conventions.

**Extension prompt:** How would you validate a signed 12-bit sample stored in a 16-bit scan element?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q135 How do direct reads and buffered acquisition differ for a sensor driver?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Sampling architecture and throughput requirements.

**Extension prompt:** Where should a timestamp be taken if acquisition time matters more than delivery time?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q136 What problem does regmap solve, and what does it not know automatically?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Register-access abstraction and device-specific semantics.

**Extension prompt:** How would you handle a register whose contents change without software writing it?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q137 Why is a DMA address different from a CPU virtual or physical address?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Address domains and portable device programming.

**Extension prompt:** How would you test a driver on a system with an IOMMU to expose hidden address assumptions?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q138 What is the difference between coherent and streaming DMA mappings?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Ownership and cache-synchronization contracts.

**Extension prompt:** What can happen if CPU cache lines overlap a DMA buffer and unrelated writable data?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q139 How do system suspend and runtime suspend differ?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Power-management scope and state coordination.

**Extension prompt:** Which information is lost when a sensor's power rail is removed rather than merely clock-gated?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

### Q140 What does SocketCAN provide beyond sending raw CAN-controller registers?

**Track:** Kernel BSP and Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Using the Linux networking abstraction for a fieldbus.

**Extension prompt:** How would you detect stale or missing application messages independently of CAN frame checks?

**Remediation:** [Module M11](../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

## Bare metal firmware

### Q141 What must startup code establish before calling main on a microcontroller?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Reset-state assumptions and C runtime initialization.

**Extension prompt:** How would you diagnose a fault before main using the reset handler and linker map?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q142 How does a linker script affect firmware correctness?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Memory placement and load/run relationships.

**Extension prompt:** What would happen if initialized data's load address and run address were confused?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q143 How should an interrupt service routine be structured?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Bounded urgent work and safe deferred processing.

**Extension prompt:** How would you handle a burst larger than the ISR-to-task queue capacity?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q144 What is the difference between a hardware timer, a software timer, and a busy wait?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Timing mechanisms and interference.

**Extension prompt:** Which mechanism would you use to measure pulse width, and where would software latency enter?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q145 How do you choose PWM frequency and resolution?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Timer arithmetic and application constraints.

**Extension prompt:** How would center-aligned mode change the frequency calculation and switching behavior?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q146 What should be considered before trusting an ADC measurement?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** The analog path and digital representation.

**Extension prompt:** How would you separate reference drift from sensor noise in a repeatable experiment?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q147 How should a watchdog be integrated into a multitask firmware system?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Detecting loss of useful progress rather than merely CPU activity.

**Extension prompt:** What failures cannot a software-supervised watchdog detect if all tasks keep sending stale heartbeats?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q148 What information should a Cortex-M fault handler preserve?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Postmortem evidence with minimal additional failure risk.

**Extension prompt:** How would you ensure a fault record corresponds to the firmware binary used for symbolication?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q149 How should flash writes be designed when erase granularity exceeds record size?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Persistence under erase/program restrictions.

**Extension prompt:** How would you recover when both records are invalid, and what configuration is safe to use?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

### Q150 What belongs in a firmware bootloader versus the application?

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Update and recovery boundaries.

**Extension prompt:** How would the bootloader decide that a newly installed image failed health confirmation?

**Remediation:** [Module M12](../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

## RTOS scheduling and communication

### Q151 How do task priority and execution time interact in a preemptive RTOS?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Schedulability rather than priority folklore.

**Extension prompt:** How would you choose priorities for acquisition, control, logging, and background diagnostics?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q152 When should you use a queue rather than a task notification?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Communication semantics and ownership.

**Extension prompt:** How would you transfer a DMA buffer between producer and consumer without copying its contents?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q153 Why can a mutex be unsuitable in an interrupt handler?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Ownership, blocking, and priority inheritance context.

**Extension prompt:** What does a higher-priority-task-woken flag mean for the return-from-interrupt path?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q154 What are the limits of FreeRTOS priority inheritance?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Avoiding overclaims about a simplified mechanism.

**Extension prompt:** How would a message-passing design remove a problematic shared peripheral lock?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q155 How do you size and validate RTOS task stacks?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Worst-case stack demand and meaningful evidence.

**Extension prompt:** Which rarely executed failure path could consume more stack than steady-state operation?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q156 How should a periodic RTOS task avoid cumulative drift?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Release-time scheduling and overrun policy.

**Extension prompt:** How would a task whose execution sometimes exceeds its period report and recover from overruns?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q157 What must a Linux to MCU protocol specify beyond a payload structure?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Interoperability and failure recovery.

**Extension prompt:** How would each peer recover when the other reboots and its sequence counter restarts?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q158 How do you make a command timeout meaningful for a robot demonstrator?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Freshness, authority, and local control boundaries.

**Extension prompt:** Should a recovered link automatically re-arm motion, or require an explicit operator action?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q159 What does deterministic execution mean in an RTOS discussion?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Bounded behavior and precise claims.

**Extension prompt:** What evidence would you present for a 2 ms response requirement after only host simulation?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q160 How do you recover from a stalled I2C transaction in firmware without wedging every task?

**Track:** MCU Firmware | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual;scenario

**What is assessed:** Timeout boundaries, peripheral recovery, and system isolation.

**Extension prompt:** What should happen if the bus remains physically stuck after the retry budget expires?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

## Firmware and protocol coding

### Q161 Implement comparison of wrapping 16-bit sequence numbers.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Freshness semantics and half-range limits.

**Extension prompt:** How would you reject a replay from a previous boot after the sequence counter resets?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q162 Encode payload bytes with delimiter 0x7e and escape 0x7d.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Framing expansion and bounded output.

**Extension prompt:** How would you recover when a stream ends immediately after an escape byte?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q163 Implement a watchdog supervisor for three required task heartbeats.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Progress windows and stale-health rejection.

**Extension prompt:** How would you supervise a task that legitimately performs a long firmware update operation?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q164 Implement a robot command state machine with DISARMED ARMED and FAULT states.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Explicit authority and fault transitions.

**Extension prompt:** How would you verify that an MCU reset starts with outputs disabled before application initialization?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q165 Implement sensor validity classification using range and maximum age.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Separating measurement value from trust in that value.

**Extension prompt:** When would a rate-of-change plausibility check add useful evidence, and when could it reject real events?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q166 Implement bounded exponential retry delays with a maximum delay.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Recovery behavior without overflow or retry storms.

**Extension prompt:** How would you reset the retry state after a connection briefly succeeds then immediately fails?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q167 Write a median-of-three filter for signed 32-bit samples without addition.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Small bounded filtering and overflow avoidance.

**Extension prompt:** How would you define output during the first two samples of a streaming implementation?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q168 Scale a signed sensor code by an integer ratio with checked output range.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Fixed-point arithmetic and explicit rounding.

**Extension prompt:** How would round-to-nearest be defined at exact half steps for negative values?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q169 Decode a signed 12-bit two's-complement value from a 16-bit container.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Bit-width-specific signed interpretation without accidental promotions.

**Extension prompt:** How would the code change for a left-aligned 12-bit field with four low padding bits?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

### Q170 Implement a token bucket that limits diagnostic events per time window.

**Track:** MCU Firmware | **Difficulty:** Practical | **Round:** Coding round | **Tags:** coding

**What is assessed:** Rate limiting with bounded arithmetic and observability.

**Extension prompt:** How would you reserve capacity for critical alarms separately from verbose diagnostics?

**Remediation:** [Module M13](../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

## Images updates and reliability

### Q171 How would you choose between Buildroot and Yocto for a learning or product image?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Build-system scope and maintenance tradeoffs.

**Extension prompt:** Which evidence would justify switching build systems after an initial prototype?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q172 What do a Yocto layer, recipe, and image each represent?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Metadata organization and build artifacts.

**Extension prompt:** How would you package one telemetry service in your own layer without editing upstream recipes?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q173 What belongs in a Buildroot external tree for a custom appliance?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Keeping product changes separate and reproducible.

**Extension prompt:** How would you prove a clean build includes your application without manual post-build copying?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q174 What is the difference between a rebuildable and a bit-reproducible image?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Precise reproducibility claims.

**Extension prompt:** How can signature timestamps or generated filesystem UUIDs complicate bitwise comparison?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q175 What should an SBOM contribute to an embedded product workflow?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Dependency traceability and its limits.

**Extension prompt:** How would you determine whether a reported vulnerability affects a feature disabled in your image?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q176 How do signed updates differ from secure or verified boot?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Integrity boundaries across installation and startup.

**Extension prompt:** How would you rotate an update signing key without stranding deployed devices?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q177 What must an A/B updater do before marking a new slot good?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Health confirmation and rollback semantics.

**Extension prompt:** What health tests should run locally when the network is unavailable?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q178 How should a CI pipeline validate an embedded change at several levels?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Test layering and honest coverage.

**Extension prompt:** Which smallest regression test would you add for a malformed length-field crash?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q179 How do you investigate boot time without optimizing the wrong stage?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Measurement boundaries and causal experiments.

**Extension prompt:** How would you measure a service that must initialize a sensor before it is operational?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

### Q180 What makes a reliability test more useful than leaving a device running overnight?

**Track:** Embedded Linux and Kernel | **Difficulty:** Intermediate | **Round:** Technical interview | **Tags:** conceptual

**What is assessed:** Targeted failure coverage and measurable acceptance.

**Extension prompt:** How would you make a storage-full failure test verify both diagnosis and recovery?

**Remediation:** [Module M14](../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

## System design exercises

### Q181 Design a bounded industrial sensor gateway using one MCU and one Linux computer.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Requirements decomposition, interfaces, and failure containment.

**Extension prompt:** How would you demonstrate that disconnecting the network cannot block MCU acquisition indefinitely?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q182 Design a Linux to MCU robot control demonstrator with stale-command protection.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Control authority, simulation, and explicit safety scope.

**Extension prompt:** What evidence would justify moving from simulation to wheels-off-ground hardware testing?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q183 Design a character-device interface for a bounded event queue.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** ABI semantics, concurrency, and removal.

**Extension prompt:** How would userspace detect that records were dropped due to queue overflow?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q184 Design a sensor acquisition path using Linux IIO and a user-space logger.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Subsystem reuse, units, timestamps, and data integrity.

**Extension prompt:** How would you correlate MCU and Linux timestamps if measurements come from both domains?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q185 Design a signed A/B update workflow for a small appliance.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Trust, persistent state, and recovery transitions.

**Extension prompt:** How would you prevent installation of an image for the wrong board revision?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q186 Design a reliable serial protocol for commands and telemetry with 128-byte payloads.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Complete protocol specification and resynchronization.

**Extension prompt:** How would a firmware update preserve compatibility with an older Linux peer?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q187 Design a real-time acquisition task plus best-effort logging under overload.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Scheduling and queue policy under conflicting priorities.

**Extension prompt:** How much storage is required to survive a 30-second downstream outage at the stated sample rate?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q188 Design a diagnostic subsystem that remains useful during failure.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Observability with bounded resource and privacy costs.

**Extension prompt:** Which five fields would you preserve for a communication timeout after a reboot?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q189 Design a small optional anomaly detector without giving it control authority.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Data methodology and safe integration boundaries.

**Extension prompt:** How would you detect that a new sensor revision invalidates the model's input distribution?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

### Q190 Design a test strategy for a driver and firmware pair before boards arrive.

**Track:** All three tracks | **Difficulty:** Advanced | **Round:** System design | **Tags:** system-design

**What is assessed:** Maximizing useful evidence without overstating emulation.

**Extension prompt:** Which failure would you expect a PTY test to reveal, and which requires a logic analyzer?

**Remediation:** [Module M17](../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

## Project defense behavioral and AI judgment

### Q191 How would you explain a project you built with AI assistance honestly?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Ownership, understanding, and evidence.

**Extension prompt:** Which AI suggestion did you reject, and what evidence led you to reject it?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q192 What should you say when you do not know an API or answer?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Intellectual honesty and a useful investigation method.

**Extension prompt:** How would you test whether a helper cancels in-flight work synchronously?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q193 How do you turn a learning project into a credible resume bullet?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Evidence-based claims and personal contribution.

**Extension prompt:** How would you phrase a kernel module that compiles but has not yet been loaded on its target?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q194 How should you defend a design decision that has a clear drawback?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Tradeoff reasoning and willingness to revise.

**Extension prompt:** What specific requirement change would make your current queue policy unacceptable?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q195 How do you answer a behavioral question about a failure without inventing experience?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Reflection, accountability, and truthful scope.

**Extension prompt:** What permanent change in your test or review process resulted from that experience?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q196 An AI suggests a kernel helper that is absent from your headers. What is your workflow?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Version-aware verification and resisting plausible inventions.

**Extension prompt:** How would you distinguish a missing Kconfig dependency from a completely invented API?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q197 How can AI-generated tests give false confidence?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Independent oracles and adversarial test design.

**Extension prompt:** Which single mutation would reveal whether your overflow test actually exercises the overflow branch?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q198 How would you present benchmark results from an emulator or shared host?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Measurement honesty and practical limits.

**Extension prompt:** What measurements would you repeat first when the selected board becomes available?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q199 How should you prioritize preparation when a JD contains far more topics than you can master soon?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Requirement extraction and evidence-based gap closure.

**Extension prompt:** Which missing evidence would most change your confidence in readiness for this specific role?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

### Q200 What demonstrates interview readiness beyond knowing 200 answers?

**Track:** All three tracks | **Difficulty:** Practical | **Round:** Project defense | **Tags:** project-defense;behavioral

**What is assessed:** Transfer of knowledge into implementation and explanation.

**Extension prompt:** Can you change one protocol requirement live, update tests, and explain the new failure modes?

**Remediation:** [Module M18](../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

