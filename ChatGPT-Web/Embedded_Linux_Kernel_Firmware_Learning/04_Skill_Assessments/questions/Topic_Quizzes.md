# Topic retrieval quizzes

Each module quiz takes 20 minutes after completing that module. Allowed tools: plain text editor or paper only; no AI, answer bank or external references. For coding/design prompts, supply an algorithm, invariants and test cases; full execution is assessed in the timed practical suite. Submit three answers with assumptions and one uncertainty. Each answer earns 0–4 using its bank criteria; pass at 9/12 with no critical misconception. Failed quizzes route to the linked module lesson and a changed-example retake. These are short-answer retrieval tests, not multiple-choice guessing.

## T01 Module M01

**Prerequisite and remediation:** [Module M01](../../03_JD_JR_Skills_and_Learning_Content/Modules/M01/lesson.md).

1. **Q041:** Explain preprocessing, compilation, assembly, and linking using one missing-symbol error. Include this boundary: How would C++ name mangling affect linking a C library?

2. **Q049:** How do you use git bisect without misdiagnosing an intermittent fault? Include this boundary: How would you handle a bisect step that cannot build with the current host toolchain?

3. **Q050:** What do compiler warnings, static analysis, and sanitizers each contribute? Include this boundary: How would you design input generation to exercise a parser beyond its normal examples?

## T02 Module M02

**Prerequisite and remediation:** [Module M02](../../03_JD_JR_Skills_and_Learning_Content/Modules/M02/lesson.md).

1. **Q001:** How are an array and a pointer different when passed to a function? Include this boundary: How would you express read-only access and document whether null is valid at length zero?

2. **Q006:** Is `printf("%d %d", i++, i++)` guaranteed to print a particular pair? Include this boundary: Give an expression with unspecified evaluation order that does not have undefined behavior.

3. **Q018:** Why does volatile not fix a shared-counter data race? Include this boundary: When would acquire-release ordering be needed instead of a relaxed counter increment?

## T03 Module M03

**Prerequisite and remediation:** [Module M03](../../03_JD_JR_Skills_and_Learning_Content/Modules/M03/lesson.md).

1. **Q023:** Implement an eight-byte ring buffer with explicit full and empty states. Include this boundary: How would a single-producer single-consumer atomic implementation publish an element safely?

2. **Q028:** Parse a decimal uint32_t with no trailing characters or overflow. Include this boundary: How would you support optional base prefixes without silently accepting octal unexpectedly?

3. **Q039:** Implement hysteresis for a high-temperature alarm. Include this boundary: What should happen when the sensor reading is invalid or stale?

## T04 Module M04

**Prerequisite and remediation:** [Module M04](../../03_JD_JR_Skills_and_Learning_Content/Modules/M04/lesson.md).

1. **Q043:** What is the difference between an ABI and an API? Include this boundary: Which ABI evidence would you collect when a cross-compiled program crashes immediately?

2. **Q044:** How does RAII improve resource handling in C++ system code? Include this boundary: How would you expose an explicit finalize operation for a resource whose release can fail?

3. **Q047:** Why can a static library link fail depending on command-line order? Include this boundary: What do archive groups change, and why can excessive circular dependencies signal a design problem?

## T05 Module M05

**Prerequisite and remediation:** [Module M05](../../03_JD_JR_Skills_and_Learning_Content/Modules/M05/lesson.md).

1. **Q051:** How do a process, a thread, and a file descriptor differ? Include this boundary: How can close followed by open in another thread create a subtle reuse bug?

2. **Q101:** How is a Linux application processor different from a typical microcontroller target? Include this boundary: Which portions of a packet parser could be shared unchanged across both targets?

3. **Q102:** What do an MMU and an MPU each provide? Include this boundary: How would a DMA engine's access differ from CPU accesses checked by an MPU?

## T06 Module M06

**Prerequisite and remediation:** [Module M06](../../03_JD_JR_Skills_and_Learning_Content/Modules/M06/lesson.md).

1. **Q052:** Why must a read or write loop handle partial progress? Include this boundary: What timeout should cover the whole operation instead of restarting after every short transfer?

2. **Q055:** How should a daemon shut down cleanly after SIGTERM? Include this boundary: How would you guarantee that a worker blocked on a condition variable notices shutdown?

3. **Q059:** Why should timeouts normally use a monotonic clock? Include this boundary: How would you define whether a command timeout should elapse while a laptop is suspended?

## T07 Module M07

**Prerequisite and remediation:** [Module M07](../../03_JD_JR_Skills_and_Learning_Content/Modules/M07/lesson.md).

1. **Q071:** Why must a condition variable be paired with a predicate and mutex? Include this boundary: When should shutdown broadcast rather than signal one waiter?

2. **Q074:** What is priority inversion, and what does priority inheritance solve? Include this boundary: What would you measure to separate inversion from an intrinsically long critical section?

3. **Q077:** Why is cancellation harder than adding a stop flag? Include this boundary: How would you guarantee exactly one completion callback for a request canceled at the same time it succeeds?

## T08 Module M08

**Prerequisite and remediation:** [Module M08](../../03_JD_JR_Skills_and_Learning_Content/Modules/M08/lesson.md).

1. **Q103:** Describe a representative embedded Linux boot path without assuming every board uses U-Boot. Include this boundary: What evidence distinguishes a kernel decompression failure from a missing root filesystem?

2. **Q105:** What belongs in device tree, and what belongs in a driver? Include this boundary: Why is a binding a compatibility interface that deserves review beyond one driver revision?

3. **Q108:** What does a cross-compilation sysroot contain, and why is it important? Include this boundary: How can pkg-config accidentally supply host include paths during a cross build?

## T09 Module M09

**Prerequisite and remediation:** [Module M09](../../03_JD_JR_Skills_and_Learning_Content/Modules/M09/lesson.md).

1. **Q112:** What are process context and interrupt context in kernel code? Include this boundary: Which context would you choose for an I2C transaction triggered by a GPIO interrupt?

2. **Q114:** How do a mutex and a spinlock differ in the kernel? Include this boundary: Why might holding a spinlock across copy_to_user be invalid?

3. **Q116:** Why does devm allocation not eliminate the need for a removal design? Include this boundary: How would you handle a user process keeping a character device open during unbind?

## T10 Module M10

**Prerequisite and remediation:** [Module M10](../../03_JD_JR_Skills_and_Learning_Content/Modules/M10/lesson.md).

1. **Q123:** A read method directly dereferences the user's buffer pointer. What is wrong? Include this boundary: How would you avoid consuming an entire FIFO item when copying it to userspace fails partway?

2. **Q125:** Poll reports readable but the next read blocks. Is the driver necessarily wrong? Include this boundary: What ordering avoids missing a state change between checking readiness and registering a waiter?

3. **Q129:** A device is removed while a process is blocked in read. What behavior must the driver define? Include this boundary: How would you make close safe after the underlying hardware has disappeared?

## T11 Module M11

**Prerequisite and remediation:** [Module M11](../../03_JD_JR_Skills_and_Learning_Content/Modules/M11/lesson.md).

1. **Q134:** Why does IIO expose raw values and scale rather than only a floating-point value? Include this boundary: How would you validate a signed 12-bit sample stored in a 16-bit scan element?

2. **Q137:** Why is a DMA address different from a CPU virtual or physical address? Include this boundary: How would you test a driver on a system with an IOMMU to expose hidden address assumptions?

3. **Q139:** How do system suspend and runtime suspend differ? Include this boundary: Which information is lost when a sensor's power rail is removed rather than merely clock-gated?

## T12 Module M12

**Prerequisite and remediation:** [Module M12](../../03_JD_JR_Skills_and_Learning_Content/Modules/M12/lesson.md).

1. **Q141:** What must startup code establish before calling main on a microcontroller? Include this boundary: How would you diagnose a fault before main using the reset handler and linker map?

2. **Q143:** How should an interrupt service routine be structured? Include this boundary: How would you handle a burst larger than the ISR-to-task queue capacity?

3. **Q147:** How should a watchdog be integrated into a multitask firmware system? Include this boundary: What failures cannot a software-supervised watchdog detect if all tasks keep sending stale heartbeats?

## T13 Module M13

**Prerequisite and remediation:** [Module M13](../../03_JD_JR_Skills_and_Learning_Content/Modules/M13/lesson.md).

1. **Q153:** Why can a mutex be unsuitable in an interrupt handler? Include this boundary: What does a higher-priority-task-woken flag mean for the return-from-interrupt path?

2. **Q157:** What must a Linux to MCU protocol specify beyond a payload structure? Include this boundary: How would each peer recover when the other reboots and its sequence counter restarts?

3. **Q158:** How do you make a command timeout meaningful for a robot demonstrator? Include this boundary: Should a recovered link automatically re-arm motion, or require an explicit operator action?

## T14 Module M14

**Prerequisite and remediation:** [Module M14](../../03_JD_JR_Skills_and_Learning_Content/Modules/M14/lesson.md).

1. **Q171:** How would you choose between Buildroot and Yocto for a learning or product image? Include this boundary: Which evidence would justify switching build systems after an initial prototype?

2. **Q172:** What do a Yocto layer, recipe, and image each represent? Include this boundary: How would you package one telemetry service in your own layer without editing upstream recipes?

3. **Q173:** What belongs in a Buildroot external tree for a custom appliance? Include this boundary: How would you prove a clean build includes your application without manual post-build copying?

## T15 Module M15

**Prerequisite and remediation:** [Module M15](../../03_JD_JR_Skills_and_Learning_Content/Modules/M15/lesson.md).

1. **Q081:** A daemon uses 100 percent CPU after its serial peer disconnects. What do you inspect? Include this boundary: How would you avoid a new busy loop if reconnect itself fails immediately?

2. **Q088:** A periodic task drifts farther behind each minute. What timing pattern is suspect? Include this boundary: What policy would you choose if one cycle takes three times the nominal period?

3. **Q098:** A DMA buffer contains stale data on one architecture. What could host testing have missed? Include this boundary: How would an IOMMU make a physical-address assumption fail?

## T16 Module M16

**Prerequisite and remediation:** [Module M16](../../03_JD_JR_Skills_and_Learning_Content/Modules/M16/lesson.md).

1. **Q176:** How do signed updates differ from secure or verified boot? Include this boundary: How would you rotate an update signing key without stranding deployed devices?

2. **Q177:** What must an A/B updater do before marking a new slot good? Include this boundary: What health tests should run locally when the network is unavailable?

3. **Q180:** What makes a reliability test more useful than leaving a device running overnight? Include this boundary: How would you make a storage-full failure test verify both diagnosis and recovery?

## T17 Module M17

**Prerequisite and remediation:** [Module M17](../../03_JD_JR_Skills_and_Learning_Content/Modules/M17/lesson.md).

1. **Q181:** Design a bounded industrial sensor gateway using one MCU and one Linux computer. Include this boundary: How would you demonstrate that disconnecting the network cannot block MCU acquisition indefinitely?

2. **Q186:** Design a reliable serial protocol for commands and telemetry with 128-byte payloads. Include this boundary: How would a firmware update preserve compatibility with an older Linux peer?

3. **Q190:** Design a test strategy for a driver and firmware pair before boards arrive. Include this boundary: Which failure would you expect a PTY test to reveal, and which requires a logic analyzer?

## T18 Module M18

**Prerequisite and remediation:** [Module M18](../../03_JD_JR_Skills_and_Learning_Content/Modules/M18/lesson.md).

1. **Q191:** How would you explain a project you built with AI assistance honestly? Include this boundary: Which AI suggestion did you reject, and what evidence led you to reject it?

2. **Q196:** An AI suggests a kernel helper that is absent from your headers. What is your workflow? Include this boundary: How would you distinguish a missing Kconfig dependency from a completely invented API?

3. **Q197:** How can AI-generated tests give false confidence? Include this boundary: Which single mutation would reveal whether your overflow test actually exercises the overflow branch?
