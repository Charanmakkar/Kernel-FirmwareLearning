from build_program import write

write('03_JD_JR_Skills_and_Learning_Content/M01_C_Objects_Bytes_and_Contracts.md', r'''
# M01 — C objects, bytes and bounded interfaces

**Status: complete first lesson.** Estimated 8–12 hours including B01 practice, depending on prerequisites. Tracks: EL/KD/FW. Prerequisites: attempt D01; know how to edit a file and invoke a compiler. No board or Linux-specific API is required. Open B01's header first; keep its implementation closed during your independent attempt.

## 1. Objectives and the engineering problem

By the exit test you should explain a pointer's lifetime and bounds, decode a byte sequence without alignment assumptions, distinguish defined behavior from undefined behavior, implement a bounded queue, and write tests that challenge its contract. A driver or firmware task often receives bytes from a device that does not obey your program's expectations. The objective is to prevent those bytes, or an error path, from violating ownership or memory bounds.

The key questions at every interface are: who owns this object; how long is it alive; how large is the valid region; who may mutate it; what changes on failure; and which execution contexts can call it? A pointer type alone answers almost none of these.

## 2. Objects, arrays, pointers and lifetime

An object is a region of storage containing a value. `uint8_t bytes[8]` is an eight-element array where this exact-width type exists. `uint8_t *p` is a pointer; it carries neither the array's length nor its ownership. In most expression contexts an array converts to a pointer to its first element. In a function parameter, `uint8_t data[8]` is adjusted to a pointer parameter; the annotation does not create or enforce an eight-byte array. Pass the length separately and document the required valid region.

```c
/* Caller supplies a live readable region of at least n bytes. */
bool first_byte(const uint8_t *data, size_t n, uint8_t *out)
{
    if (data == NULL || out == NULL || n == 0u)
        return false;
    *out = data[0];
    return true;
}
```

The null checks do not validate an arbitrary non-null address. The caller must supply live objects of the promised sizes. `sizeof array` measures an actual array at its declaration site; `sizeof data` inside this function measures a pointer. `strlen` finds a zero byte in a valid string; it cannot safely discover the size of arbitrary incoming storage.

Automatic local objects usually live until their block exits. Dynamically allocated storage persists until freed; ownership describes which part of the program must free it. Static-duration objects last for the program lifetime. Stack and heap are common implementation arrangements, not complete definitions of C storage duration. Returning the address of an automatic local object creates a dangling pointer after return. A successful test run does not repair that error. A pointer one past an array may be formed for iteration but not dereferenced. Pointer subtraction/ordering has restrictions; do not treat unrelated allocations as one array.

```text
caller scope: uint8_t storage[3] ------------------ alive ------------------>
                  ^
                  | borrowed storage, never freed by ring
            eu_ring {head, tail, count}
callee scope: temporary parser object --validate--> copy to caller's packet
```

The B01 ring borrows its backing storage. The packet decoder instead copies up to 64 bytes into output that the caller owns. Borrowing avoids copying but demands lifetime control; ownership simplifies later use at a bounded copy cost. In C++, Resource Acquisition Is Initialization (RAII) can bind resource cleanup to object lifetime; it does not make a borrowed pointer outlive its owner. Study move semantics and exception policy when the JD calls for C++; C kernel code does not become C++ by using an ownership analogy.

## 3. Integer behavior and bit operations

Unsigned arithmetic wraps modulo one more than the type's maximum. Signed overflow is undefined behavior under the selected C11 model. Integer promotions mean a small integer often participates in arithmetic as `int`; mixing signed and unsigned types can change a comparison. For `int n=-1; size_t cap=8;`, `n < cap` is false on the selected common data models because conversion produces a large unsigned value. Validate a signed result before conversion to a size type. For example, check a POSIX `ssize_t` read result for negative errors before adding it to a `size_t` offset.

For allocation sizes, test multiplication before multiplying:

```c
if (element_size != 0u && count > SIZE_MAX / element_size)
    return false;
bytes = count * element_size;
```

`count * element_size` followed by checking whether it is too large is already too late if it wrapped. Widths are part of the contract: use size_t for object sizes, fixed-width unsigned types for protocol words, and suitable format macros/casts when printing. Do not truncate a size into uint8_t before validating it.

Use unsigned masks for bit fields. `(old & ~mask) | (value & mask)` replaces only selected bits. A shift count must be less than the width of the promoted left operand and nonnegative. B01 checks `position < 32` before shifting `UINT32_C(1)`. `1 << 31` is a poor portable way to make a 32-bit high-bit mask; signed arithmetic and widths matter. Bitwise operations on a register also require its hardware semantics: write-one-to-clear and read-to-clear registers cannot be handled safely with a generic read/modify/write formula. This lesson's helper operates on an ordinary integer value, not MMIO.

## 4. Byte order, alignment, layout and undefined behavior

Big-endian encoding stores the high-order byte first; little-endian encoding stores the low-order byte first. CPU byte order and wire byte order are independent choices. Decode explicitly:

```c
size_t length = ((size_t)wire[4] << 8u) | wire[5];
```

This expression is valid only after confirming that at least six bytes exist. Casting `wire + 4` to `uint16_t *` and dereferencing can violate alignment and effective-type requirements and assumes the host byte order. `memcpy` into a properly aligned integer avoids some alias/alignment issues but still requires explicit byte-order conversion. A packed struct is a compiler-specific layout tool, not a complete portable protocol.

Structures may include padding for alignment; `sizeof(struct)` may exceed the sum of fields. Padding bytes and ABI (Application Binary Interface) rules make blindly serializing a struct incorrect. A union shares storage and is useful for deliberate representations, but portable byte decoding should not depend on casually reinterpreting inactive members. Enums name states; validate values received from outside the program before using them as an index or dispatch state.

Undefined behavior means the language imposes no behavioral requirements for that execution; do not predict a universal output for `i = i++ + 1` in C11 or a use-after-free. Unspecified behavior allows multiple permitted choices, such as the relative evaluation order of independent function arguments. Implementation-defined behavior is chosen and documented by the implementation, such as whether plain char is signed. These categories require different interview answers: identify the category, explain why, then show a portable rewrite. A compiler warning, one observed output, or optimizer setting is not a language guarantee. See R01 for language rules; examples and B01 are original applied teaching material.

## 5. const, volatile, atomics and synchronization

`const uint8_t *p` prevents mutation through p; it neither owns the bytes nor proves another alias cannot mutate them. `uint8_t *const p` prevents reassigning that pointer object. Neither declaration promises thread safety or static storage.

`volatile` makes particular accesses observable under the implementation's rules. It does not provide mutual exclusion, make `x++` atomic, or establish interthread ordering. A firmware register declaration may use volatile under the toolchain/vendor's MMIO rules; Linux drivers should use the appropriate accessors. Device ordering, caches, DMA ownership and CPU ordering remain separate problems. The kernel's rationale is discussed in R06.

C11 `_Atomic` objects and operations provide atomicity and selected memory-order guarantees. A release store paired with an acquire load that observes it can publish earlier ordinary writes. Relaxed operations provide atomicity without that publication ordering. This is not permission to convert every field of B01's ring to atomic and assume correctness. A correct lock-free ring requires a documented single-producer/single-consumer model, slot ownership and both publication/reuse orderings. Linux kernel primitives follow its memory model; do not paste user-space C atomics into a kernel driver. For a first multithreaded queue, use one mutex and a condition predicate. See R09 for compiler atomic support and R23 for waits; the concurrency lesson M04 remains pending.

## 6. Worked example: validate then commit

B01's frame has six header bytes, at most 64 payload bytes and two CRC bytes. Let the input length be N and the declared payload length L. Before reading fields, reject N<8 or N>72. Check the magic/version. Read L from the two byte positions already covered by the length check. Reject L>64 and N!=L+8. Only then compute/compare CRC, copy L bytes into a zero-initialized local packet, and assign the output once.

Why that order? It makes the input length establish every later access. The upper bound makes adding eight safe. The local packet avoids half-filled output after a checksum error. The error enum communicates a reason without forcing callers to interpret a string. A decoder for a *stream* also needs accumulation, progress, timeout and resynchronization behavior; B01 accepts one exact frame.

For an 11-byte frame with a three-byte payload, the parser reads header bytes 0–5, payload bytes 6–8 and checksum bytes 9–10. CRC covers bytes 0–8. Supplying only the first ten bytes must return EU_LENGTH, not read a nonexistent final checksum byte. A frame with valid CRC and unknown version must still be rejected by the compatibility policy. Authentication is a different requirement from CRC integrity.

## 7. Worked example: ring representation and state

The ring owns no memory. Let head be the next write index, tail the next read index, and count the occupied slots. Invariants: `capacity>0`, `head<capacity`, `tail<capacity`, `count<=capacity`. Empty means count=0; full means count=capacity. This representation uses all slots. A different representation that reserves one slot uses a different full rule and effective capacity; mixing rules is a defect.

| Operation, capacity=3 | head | tail | count | Result |
|---|---:|---:|---:|---|
| init | 0 | 0 | 0 | empty |
| push A; push B | 2 | 0 | 2 | A,B |
| pop | 2 | 1 | 1 | returns A |
| push C; push D | 1 | 1 | 3 | B,C,D; full |
| push E | 1 | 1 | 3 | full error; unchanged |

A push writes one byte then advances head and count. A pop reads one byte then advances tail and decrements count. Both are O(1). That complexity does not prove a timing deadline: code generation, memory architecture and interrupt interference also matter. A shifting array model is O(n) but is simple enough to test this implementation against a different representation.

Function pointers can implement a dispatch table or callback; require an explicit signature, valid lifetime/context and checked table index. For small firmware behavior, a state machine with `enum state` and a `switch` is often easier to review. Example protocol states are WAIT_HEADER, WAIT_BODY and VALIDATE; a timeout returns to WAIT_HEADER. Every input must either advance state, consume a byte, or fail within a bound. No hidden infinite retry loop should appear on malformed input.

## 8. Guided lab and expected behavior

1. Open B01/include/embedded_util.h. Write down preconditions and errors before reading src/. Predict the capacity-one ring behavior and the zero-payload frame size.
2. From B01 run `python scripts/verify.py --cc clang` on Windows, or `python3 scripts/verify.py --cc cc` on Linux. Expected contract: PASS followed by `type=7 payload=3 frame=11`. Only the generated evidence JSON is an actual result.
3. Run the separate `--sanitize` variant. AddressSanitizer instruments supported memory accesses; UndefinedBehaviorSanitizer instruments supported undefined-behavior checks. Neither proves algorithmic correctness or covers all undefined behavior; support depends on compiler/target/runtime [R07/R08]. Keep normal and sanitizer records separate.
4. In a disposable branch, replace the full test with `count==capacity-1`, predict a counterexample, run tests, isolate capacity=1, then restore. Explain how the model disagrees.
5. In another disposable branch, remove the exact input-length check. Predict a truncation that reaches a checksum read outside the provided region; use tests/sanitizers to evaluate it. Restore and keep a regression explanation.
6. Try independent E01 below, then open its separate solution. Explain the code aloud without AI.

Troubleshooting: if the compiler is missing, select an actual compiler path; if warning-as-error triggers, inspect types and format specifiers; if the sanitizer runtime is unavailable, record that limitation and keep the normal test result; if a random-input test fails, retain seed and minimal input. A huge randomized count without a reproducible failure record is weak evidence.

## 9. Independent exercise and review questions

Attempt [M01 exercises](exercises/M01_Questions.md) before [solutions](solutions/M01_Solutions.md). Also do B01 E01/E02. Do not count guided modification of supplied source as an independent implementation.

Review: why can a non-null pointer still be invalid; what array information disappears at a function boundary; where must length checking happen; what behavior category applies to signed overflow; why can one-past be formed but not dereferenced; why does a CRC not identify a sender; when does a count-based ring become racy; and what does a sanitizer pass leave unknown? Connect answers to Q001–Q030 and the B01 demo defense.

## 10. Mastery checklist and references

- Explain each backing object's owner, lifetime, size and mutability.
- Implement exact-frame parsing with bounded lengths and unchanged output on failure.
- Distinguish host representation from wire encoding and identify nonportable casts.
- Demonstrate full, empty, wraparound, invalid input and capacity-one tests.
- Explain const/volatile/atomic/lock guarantees separately and identify caller serialization.
- Predict a minimal counterexample before running a seeded bug.
- Compile and test an independent extension; retain actual source and evidence.
- Repeat the explanation and a changed exercise after seven days without AI.

References, accessed 27 October 2026: [C11 committee draft R01](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf); [kernel circular-buffer discussion R05](https://docs.kernel.org/6.12/core-api/circular-buffers.html); [kernel volatile rationale R06](https://docs.kernel.org/6.12/process/volatile-considered-harmful.html); [Clang ASan R07](https://clang.llvm.org/docs/AddressSanitizer.html); [Clang UBSan R08](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html); [GCC atomic support R09](https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html). Older kernel references here explain concepts; they are not the API baseline for future 6.18.7 drivers.
''')

write('03_JD_JR_Skills_and_Learning_Content/exercises/M01_Questions.md', r'''
# M01 independent exercise and exit test

Prerequisites: M01 guided lab. Duration 60 minutes. Allowed: editor, compiler, local C documentation, debugger; no AI and no reference solution. Deliver a .c/.h pair, tests, actual compiler output and a 200-word explanation. Test data is below; add your own edge cases.

E-M01: implement `bool read_be16(const uint8_t *data, size_t size, size_t offset, uint16_t *out)` with an unchanged output on failure. A valid live data array and distinct live output object are caller preconditions. Null, insufficient bytes and huge offsets must return false; avoid `offset+2` overflow. Data `{0x12,0x34,0xab,0xcd}` at offsets 0 and 2 yields 0x1234 and 0xabcd. Offsets 3, 4 and SIZE_MAX fail; size 0 fails; null arguments fail. No unaligned casts or host-endian assumptions.

Explain: why `if (offset + 2 <= size)` can fail; why the out pointer cannot be “validated” by a null test alone; why no malloc is necessary; why a volatile output pointer would not add synchronization.

Score: correct byte result 25, all boundary/error semantics 25, portable types and lifetime reasoning 20, meaningful tests/evidence 20, explanation 10. Pass >=80 with no invalid access, overflow-based bounds defect or fabricated result. Failure remediation: draw the valid index interval, rewrite using subtraction after offset validation, add a regression for SIZE_MAX and retake on a 32-bit-byte-field decoder with a different input.
''')

write('03_JD_JR_Skills_and_Learning_Content/solutions/M01_Solutions.md', r'''
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
''')

write('04_Skill_Assessments/questions/D01_Initial_Diagnostic.md', r'''
# D01 — Initial diagnostic (questions only)

Purpose: obtain evidence before scoring your current ability. Duration 100 minutes: C25, Linux20, concurrency15, architecture10, debugging20, communication10. No prerequisite score. Allowed editor/compiler/debugger, local manual pages; no AI, answer keys or external code. If no working Linux environment exists, mark the Linux execution component unassessed, do the written parts and do not compute an overall pass until the missing practical is attempted. Never substitute the author's tests for your score.

Deliver source, actual commands/output, written explanations, time spent and clearly labeled unattempted tasks. Keep notes about hypotheses before compiling. Grade by section using the separate key; pass requires >=70/100, C>=15/25, Linux>=12/20 and no critical misconception. This routes learning; it is not a hiring prediction.

1. **C / 25 points / 25 minutes.** Implement a function that reads a big-endian 16-bit integer from an arbitrary byte offset. Input `{0x12,0x34,0xab,0xcd}`; test offset 0,2,3,SIZE_MAX. Define error/output behavior. Then classify `int i=1; int j=i++ + i++;` under C11; distinguish array size from pointer size inside a function. Deliver code and five tests.
2. **Linux / 20 / 20 minutes.** In a scratch directory create two files and a relative symlink; change one file to owner read/write only; show its permissions. Start a sleep process, find its PID, inspect `/proc/PID/status`, terminate it with SIGTERM and confirm it exited. Explain why a process can disappear between discovery and inspection. Deliver transcript. Do not operate on unrelated processes or files.
3. **Concurrency / 15 / 15 minutes.** Two threads modify `volatile int count` with count++. Explain the defect. Sketch a bounded queue's producer/consumer ownership, condition-variable wait predicate and shutdown. Specify what happens if shutdown arrives while the queue is full. Deliver state/locking explanation; code optional.
4. **Architecture / 10 / 10 minutes.** Explain application processor versus MCU, MMU versus MPU, virtual versus DMA address, interrupt handler versus task context. Say which statements you would verify in board/kernel docs before writing code. Deliver a short diagram.
5. **Debugging / 20 / 20 minutes.** A framed receiver works for one write but fails when a message arrives as 2+3+remaining bytes; after a timeout it spins at 100% CPU. List competing hypotheses, instrumentation, and a minimal fixture. Separately analyze the illustrative trace: `poll=1; read=2; poll=1; read=-1 EAGAIN; poll=0; loop repeats with timeout=0`. Do not claim a unique root cause from this alone.
6. **Communication / 10 / 10 minutes.** Describe a project you actually did, or honestly say you have no completed project. Separate your contribution from supplied code; state a limitation and a test you would add. No invented metrics or experience.

Critical blockers: predicting a universal output for unsequenced modifications; treating volatile as thread synchronization; unsafe bounds arithmetic; inventing successful execution. Remediation is in the answer key. Independent assessment must be followed by a changed-input retention test, not simply reading the solution.
''')

write('04_Skill_Assessments/answer_keys/D01_Key.md', r'''
# D01 key and remediation

Keep closed during the diagnostic. Do not assign the learner scores before reviewing their artifacts.

C25: 8 for valid endian decode without alignment assumptions, 8 for null/offset/remaining-space checks and unchanged output, 4 for useful tests, 3 for correctly identifying unsequenced modifications of i as undefined behavior under C11, 2 for parameter array adjustment. Unsafe accesses block G0 regardless of total. Remediate M01 and E-M01, then retest with a 32-bit field.

Linux20: 4 each for correct isolated file/symlink creation, permission verification, correct owned PID discovery, proc inspection with process-disappearance handling, and SIGTERM/exit confirmation. `/proc` results are dynamic; process identity can also be complicated by PID reuse. A proc path missing after enumeration is a normal race, not proof of corruption. On Linux a suitable scratch sequence is `mkdir scratch`, `cd scratch`, `touch one two`, `ln -s one alias`, `chmod 600 one`, `ls -l`, `sleep 120 &`, `pid=$!`, `cat /proc/$pid/status`, `kill -TERM "$pid"`, `wait "$pid"`; expected signal termination is handled as such, not a command-success requirement. Shell job-control output varies. This sequence is illustrative, not executed evidence. Missing environment means unassessed, not zero competence. Remediate basic shell/process labs before B02.

Concurrency15: 5 for volatile not providing atomicity/order and count++ being read-modify-write; 5 for mutex-protected state plus while-loop predicate and wake/recheck; 5 for shutdown flag/broadcast/join with declared drain/discard policy. Blocking a producer on a full queue forever after consumer shutdown is incorrect. Remediate single-owner queue plus one-mutex implementation; use a race tool where supported, then explain correctness without relying on the tool.

Architecture10: 2.5 each for distinct processor roles, MMU page translation versus MPU region protection (target-dependent), device DMA address not assumed equal to CPU pointer/physical address, and context-dependent sleep/interrupt rules. Remediate with the target memory map and callback-context table.

Debugging20: 5 for identifying partial-frame accumulation as a hypothesis, 5 for absolute deadline/recomputed remaining time and EAGAIN readiness races, 5 for bounded PTY fixture with fragmented input, 5 for measured observation and alternative explanations. Readiness does not guarantee that a later operation cannot return EAGAIN; the trace alone does not establish every cause of the CPU spin. Remediate B03 I/O state transitions and a timeout fixture.

Communication10: 4 accurate contribution, 3 evidence/limits, 3 clear next experiment. No experience is an acceptable honest starting point. Remediate by describing B01's supplied versus independent work.

Record scores, evidence, critical blockers and next task in skills_tracker.csv. Retake failed sections after at least a focused remediation cycle; use different input and state transitions. Do not average away critical failures.
''')

write('04_Skill_Assessments/ASSESSMENT_PLAN.md', r'''
# Assessment inventory and execution rules

Delivered questions/keys: D01 initial diagnostic; M01 independent exit test E-M01; B01 E01–E03 exercises and separate solutions. Program-wide G0–G7 criteria are defined in the roadmap. Later phase-exit question sets, timed coding suites, seeded Linux/kernel/firmware broken-code fixtures, crash-analysis fixtures, per-track full mocks and final practical reference solutions remain pending. A plan for those tests is not a delivered assessment.

Standard attempt record: assessment ID; prerequisites satisfied; start/end time; allowed tools and actual AI use; source/config revision; exact task/test data; actual stdout/stderr; expected-versus-observed behavior; rubric score; critical failures; remediation; retention-test date. Independent attempts exclude AI; assisted attempts are clearly labeled and cannot establish independent passage.

## Future timed formats and acceptance definitions

15-minute microtest: decode bounded bytes and explain a supplied edge case; no AI; header/manual allowed; deliver code/test/explanation. 45-minute coding task: handle fragmented pipe input with timeout and cleanup; local compiler/debugger allowed; deliver fixture, resource analysis and command log. 90-minute debugging task: seeded memory/race/hang defect; deliver initial hypotheses, minimal reproducer, fix and regression, not just a patch. These fixtures and separate reference solutions are not delivered yet.

Per-track mock design: 60 minutes, conceptual 10, coding/review 20, debugging 15, project defense 15. EL focuses partial I/O and service lifecycle; KD covers context/locking/lifetime and a probe/unbind scenario; FW covers startup, task/ISR ownership and a watchdog deadline. At least one changed-input task is done without hints. Full scripts/questions are pending.

Final practical plan: four hours after applicable gates, offline docs/compiler/debugger allowed, no AI for the independent grade. Fresh source setup, one unfamiliar failure, one constrained feature, normal/boundary/fault tests, and a 15-minute capstone defense. Proposed data: valid frame, fragmented frame, wrong version, duplicate sequence, worker stall, restart and disk-full fixture; actual runnable fixtures remain pending. Score with the gate rubric; pass >=80 and no critical failure. Retest the failed category using different data. Hardware timing claims require target instrumentation and measured evidence, not a simulation grade.
''')

if __name__ == '__main__':
    print('Authored M01, exercises, diagnostic and assessment policy')
