# Interview attempts — questions only

Use 2–4 minutes for a conceptual answer, 15–45 minutes for a coding task and 20–40 minutes for a design depending on scope. State assumptions and tool/AI rules before starting. Scored reference solutions for every coding implementation remain a separate future deliverable; the bank provides spoken/deeper reference answers.

## Q001 — Implement a bounded big-endian 16-bit read.

All; foundation; coding practical; coding.

## Q002 — Write a checked allocation-size helper.

All; foundation; coding practical; coding.

## Q003 — Copy a bounded string into a fixed buffer with an explicit policy.

All; foundation; coding practical; coding.

## Q004 — Design an ownership-safe function returning parsed data.

All; foundation; coding practical; coding.

## Q005 — What does const guarantee?

All; foundation; technical screen; conceptual.

## Q006 — Implement a resource cleanup path after several allocations.

All; foundation; coding practical; coding.

## Q007 — Explain automatic, static and allocated storage duration.

All; foundation; technical screen; conceptual.

## Q008 — Predict int i=1; int j=i++ + i++; under C11.

All; foundation; technical screen; code-output analysis.

## Q009 — Implement overlapping byte movement safely.

All; foundation; coding practical; coding.

## Q010 — How do arrays differ from pointers at function boundaries?

All; foundation; technical screen; conceptual.

## Q011 — Create a checked single-bit uint32_t mask.

All; foundation; coding practical; coding.

## Q012 — Replace only selected bits of an integer.

All; foundation; coding practical; coding.

## Q013 — Decode a signed 16-bit sensor sample portably.

All; foundation; coding practical; coding.

## Q014 — Parse an unsigned decimal CLI argument robustly.

All; foundation; coding practical; coding.

## Q015 — What is the result of comparing int n=-1 with size_t cap=8?

All; foundation; technical screen; code-output analysis.

## Q016 — Test whether a positive integer is a power of two.

All; foundation; coding practical; coding.

## Q017 — Why should a protocol not serialize a native struct?

All; foundation; technical screen; conceptual.

## Q018 — Add two size values with overflow detection.

All; foundation; coding practical; coding.

## Q019 — Classify char c=255 and signed right shift under C11.

All; foundation; technical screen; code-output analysis.

## Q020 — What do alignment and effective type protect?

All; foundation; technical screen; conceptual.

## Q021 — Implement a full-capacity byte ring.

All; foundation; coding practical; coding.

## Q022 — Implement ring peek without mutation.

All; foundation; coding practical; coding.

## Q023 — Implement CRC-16 for a precisely named variant.

All; foundation; coding practical; coding.

## Q024 — Implement exact-frame validation with an owned result.

All; foundation; coding practical; coding.

## Q025 — Design a bounded stream framing state machine.

All; foundation; coding practical; coding.

## Q026 — When choose an array, linked list or ring?

All; foundation; technical screen; conceptual.

## Q027 — Implement a finite-state machine for a timed request.

All; foundation; coding practical; coding.

## Q028 — Implement a callback dispatch table safely.

All; foundation; coding practical; coding.

## Q029 — Parse a type-length-value buffer defensively.

All; foundation; coding practical; coding.

## Q030 — Why are complexity and timing different claims?

All; foundation; technical screen; conceptual.

## Q031 — Explain compilation versus linking.

All; foundation; technical screen; conceptual.

## Q032 — A declaration is visible but linking reports undefined reference. What next?

All; foundation; debugging/code review; debugging/scenario.

## Q033 — Write a minimal Make rule that rebuilds after header changes.

All; foundation; coding practical; coding.

## Q034 — What is an ABI?

All; foundation; technical screen; conceptual.

## Q035 — How do linker scripts and map files help firmware?

All; foundation; technical screen; conceptual.

## Q036 — What should a small code review prioritize?

All; foundation; technical screen; conceptual.

## Q037 — How does C++ RAII help embedded software?

All; foundation; technical screen; conceptual.

## Q038 — Design a move-only file-descriptor owner.

All; foundation; coding practical; coding.

## Q039 — A build passes locally but fails in CI. How investigate?

All; foundation; debugging/code review; debugging/scenario.

## Q040 — What belongs in an engineering commit and automation script?

All; foundation; technical screen; conceptual.

## Q041 — What distinguishes process and thread?

EL/KD; foundation; technical screen; conceptual.

## Q042 — A PID disappears while your inspector reads /proc. Is this a bug?

EL/KD; foundation; debugging/code review; debugging/scenario.

## Q043 — What do file permissions and umask control?

EL/KD; foundation; technical screen; conceptual.

## Q044 — Explain /proc, /sys and /dev.

EL/KD; foundation; technical screen; conceptual.

## Q045 — What happens during fork and exec?

EL/KD; foundation; technical screen; conceptual.

## Q046 — Your child process becomes a zombie. What happened?

EL/KD; foundation; debugging/code review; debugging/scenario.

## Q047 — How should a service shut down on SIGTERM?

EL/KD; foundation; technical screen; conceptual.

## Q048 — A service runs manually but fails at boot. What compare?

EL/KD; foundation; debugging/code review; debugging/scenario.

## Q049 — What is virtual memory and why can RSS differ from address-space size?

EL/KD; foundation; technical screen; conceptual.

## Q050 — A deleted log still occupies disk space. Why?

EL/KD; foundation; debugging/code review; debugging/scenario.

## Q051 — Implement write-all with partial progress and a deadline.

EL; foundation; coding practical; coding.

## Q052 — What can a read result mean?

EL; foundation; technical screen; conceptual.

## Q053 — Design an absolute timeout for an I/O loop.

EL; foundation; coding practical; coding.

## Q054 — poll reports readable but read returns EAGAIN. Is that impossible?

EL; foundation; debugging/code review; debugging/scenario.

## Q055 — Implement a bounded line reader over a byte stream.

EL; foundation; coding practical; coding.

## Q056 — Create a pipe-based parent/child exchange without descriptor leaks.

EL; foundation; coding practical; coding.

## Q057 — When use shared memory instead of a pipe/socket?

EL; foundation; technical screen; conceptual.

## Q058 — Your epoll edge-triggered receiver stalls despite unread data. Why?

EL; foundation; debugging/code review; debugging/scenario.

## Q059 — How do stream and datagram sockets affect protocol design?

EL; foundation; technical screen; conceptual.

## Q060 — A writer dies with SIGPIPE when its reader closes. How handle it?

EL; foundation; debugging/code review; debugging/scenario.

## Q061 — Implement a mutex/condition-variable bounded queue.

All; foundation; coding practical; coding.

## Q062 — Why can a condition wait return with no usable item?

All; foundation; debugging/code review; debugging/scenario.

## Q063 — Publish an immutable configuration snapshot between threads.

All; foundation; coding practical; coding.

## Q064 — The queue deadlocks only during shutdown when full. What inspect?

All; foundation; debugging/code review; debugging/scenario.

## Q065 — What is priority inversion?

All; foundation; technical screen; conceptual.

## Q066 — Two individually correct mutex-protected functions deadlock together. Why?

All; foundation; debugging/code review; debugging/scenario.

## Q067 — Why is volatile count++ unsafe across threads?

All; foundation; technical screen; conceptual.

## Q068 — Design a single-producer/single-consumer ring publication protocol.

All; foundation; coding practical; coding.

## Q069 — A test passes under a debugger but races in release. What next?

All; foundation; debugging/code review; debugging/scenario.

## Q070 — When should a thread own a resource exclusively?

All; foundation; technical screen; conceptual.

## Q071 — How do MMU and MPU differ?

KD/FW; intermediate; technical screen; conceptual.

## Q072 — What is MMIO and why not use an ordinary pointer casually?

KD/FW; intermediate; technical screen; conceptual.

## Q073 — A register read always returns zero. How investigate?

KD/FW; intermediate; debugging/code review; debugging/scenario.

## Q074 — Why can DMA fail despite correct CPU memory contents?

KD/FW; intermediate; technical screen; conceptual.

## Q075 — A DMA buffer works on one board but contains stale data on another. Why?

KD/FW; intermediate; debugging/code review; debugging/scenario.

## Q076 — What is interrupt latency versus handler execution time?

KD/FW; intermediate; technical screen; conceptual.

## Q077 — How do barriers differ from locks?

KD/FW; intermediate; technical screen; conceptual.

## Q078 — An IRQ fires continuously after enabling a peripheral. What inspect?

KD/FW; intermediate; debugging/code review; debugging/scenario.

## Q079 — Implement rollover-safe elapsed-time comparison for a timer.

KD/FW; intermediate; coding practical; coding.

## Q080 — Why is disabling local interrupts not a multicore lock?

KD/FW; intermediate; technical screen; conceptual.

## Q081 — What is a cross toolchain and sysroot?

EL/KD; intermediate; technical screen; conceptual.

## Q082 — An AArch64 binary exists but cannot execute. What check?

EL/KD; intermediate; debugging/code review; debugging/scenario.

## Q083 — Write a cross-build configuration that avoids host leakage.

EL/KD; intermediate; coding practical; coding.

## Q084 — How do QEMU user mode and system mode differ?

EL/KD; intermediate; technical screen; conceptual.

## Q085 — Remote debugging shows wrong source lines. What inspect?

EL/KD; intermediate; debugging/code review; debugging/scenario.

## Q086 — Explain a platform boot chain without assuming U-Boot everywhere.

EL/KD; intermediate; technical screen; conceptual.

## Q087 — Kernel boots but cannot mount root filesystem. What check?

EL/KD; intermediate; debugging/code review; debugging/scenario.

## Q088 — Kernel finds rootfs but reports no working init. What next?

EL/KD; intermediate; debugging/code review; debugging/scenario.

## Q089 — What is an initramfs compared with persistent rootfs?

EL/KD; intermediate; technical screen; conceptual.

## Q090 — What belongs in a BSP?

EL/KD; intermediate; technical screen; conceptual.

## Q091 — What determines whether kernel code may sleep?

KD; intermediate; technical screen; conceptual.

## Q092 — A warning says sleeping function called from invalid context. What inspect?

KD; intermediate; debugging/code review; debugging/scenario.

## Q093 — How choose mutex, spinlock_t or raw_spinlock_t?

KD; intermediate; technical screen; conceptual.

## Q094 — How do kmalloc and vmalloc differ?

KD; intermediate; technical screen; conceptual.

## Q095 — A probe leaks resources on its third failure path. How fix?

KD; intermediate; debugging/code review; debugging/scenario.

## Q096 — What does a wait queue provide?

KD; intermediate; technical screen; conceptual.

## Q097 — When use a workqueue?

KD; intermediate; technical screen; conceptual.

## Q098 — What problem does RCU solve?

KD; intermediate; technical screen; conceptual.

## Q099 — A timer callback accesses freed driver state after removal. What happened?

KD; intermediate; debugging/code review; debugging/scenario.

## Q100 — Why are atomics insufficient for many kernel invariants?

KD; intermediate; technical screen; conceptual.

## Q101 — Why use copy_to_user/copy_from_user?

KD; intermediate; technical screen; conceptual.

## Q102 — A read succeeds but poll never wakes. What inspect?

KD; intermediate; debugging/code review; debugging/scenario.

## Q103 — What should a character read return when no data exists?

KD; intermediate; technical screen; conceptual.

## Q104 — A module unloads while an open descriptor still calls it. What review?

KD; intermediate; debugging/code review; debugging/scenario.

## Q105 — How do you design a stable ioctl ABI?

KD; intermediate; technical screen; conceptual.

## Q106 — Design a poll-capable bounded kernel queue.

KD; intermediate; coding practical; coding.

## Q107 — What do managed resources simplify and leave unsolved?

KD; intermediate; technical screen; conceptual.

## Q108 — A driver reports success after hardware initialization fails. What consequence?

KD; intermediate; debugging/code review; debugging/scenario.

## Q109 — Why is a learning char device not always a production sensor interface?

KD; intermediate; technical screen; conceptual.

## Q110 — A multi-client driver duplicates or loses records. Where look?

KD; intermediate; debugging/code review; debugging/scenario.

## Q111 — What does device tree describe?

KD; intermediate; technical screen; conceptual.

## Q112 — A device-tree node exists but probe never runs. What inspect?

KD; intermediate; debugging/code review; debugging/scenario.

## Q113 — When should probe return deferred-probe error?

KD; intermediate; technical screen; conceptual.

## Q114 — Outline a GPIO IRQ platform driver using modern resources.

KD; intermediate; coding practical; coding.

## Q115 — How do GPIO logical values differ from electrical levels?

KD; intermediate; technical screen; conceptual.

## Q116 — A GPIO driver works on a simulator but not the board. Why?

KD; intermediate; debugging/code review; debugging/scenario.

## Q117 — How do clocks and regulators affect probe and runtime?

KD; intermediate; technical screen; conceptual.

## Q118 — An overlay compiles but the wrong device appears. What inspect?

KD; intermediate; debugging/code review; debugging/scenario.

## Q119 — Why validate a device-tree binding schema?

KD; intermediate; technical screen; conceptual.

## Q120 — A button produces many interrupts for one press. How respond?

KD; intermediate; debugging/code review; debugging/scenario.

## Q121 — Compare I2C, SPI and UART integration concerns.

KD; intermediate; technical screen; conceptual.

## Q122 — An I2C register read returns NACK. What investigate?

KD; intermediate; debugging/code review; debugging/scenario.

## Q123 — What must match for an SPI peripheral?

KD; intermediate; technical screen; conceptual.

## Q124 — Convert ADXL345 register bytes to physical units.

KD; intermediate; coding practical; coding.

## Q125 — Why expose sensor channels through IIO?

KD; intermediate; technical screen; conceptual.

## Q126 — Sensor samples are plausible but scaled incorrectly. What inspect?

KD; intermediate; debugging/code review; debugging/scenario.

## Q127 — What is a triggered IIO buffer?

KD; intermediate; technical screen; conceptual.

## Q128 — A bus read sleeps inside a hard IRQ and warns. What change?

KD; intermediate; debugging/code review; debugging/scenario.

## Q129 — What is runtime PM versus system suspend?

KD; intermediate; technical screen; conceptual.

## Q130 — DMA completion occurs after the client buffer was released. What failed?

KD; intermediate; debugging/code review; debugging/scenario.

## Q131 — What happens before main on a Cortex-M firmware target?

FW; intermediate; technical screen; conceptual.

## Q132 — Write the logic for nonblocking UART receive processing.

FW; intermediate; coding practical; coding.

## Q133 — Firmware enters a fault handler after an interrupt. What capture?

FW; intermediate; debugging/code review; debugging/scenario.

## Q134 — What are .text, .data, .bss and stack?

FW; intermediate; technical screen; conceptual.

## Q135 — How should a watchdog be fed?

FW; intermediate; technical screen; conceptual.

## Q136 — Timer periods drift when other work increases. Why?

FW; intermediate; debugging/code review; debugging/scenario.

## Q137 — What must peripheral initialization establish?

FW; intermediate; technical screen; conceptual.

## Q138 — Design a debounced button state machine.

FW; intermediate; coding practical; coding.

## Q139 — When use polling, interrupt or DMA?

FW; intermediate; technical screen; conceptual.

## Q140 — MCU application works after debugger download but not power-cycle. Why?

FW; intermediate; debugging/code review; debugging/scenario.

## Q141 — How assign task priorities?

FW; intermediate; technical screen; conceptual.

## Q142 — A high-priority task starves lower-priority maintenance. What inspect?

FW; intermediate; debugging/code review; debugging/scenario.

## Q143 — What can priority inheritance fix and not fix?

FW; intermediate; technical screen; conceptual.

## Q144 — Design a watchdog supervisor with task progress counters.

FW; intermediate; coding practical; coding.

## Q145 — How do queues, mutexes and semaphores differ?

FW; intermediate; technical screen; conceptual.

## Q146 — A task stack overflows only during error logging. How investigate?

FW; intermediate; debugging/code review; debugging/scenario.

## Q147 — What is a deadline miss and how should firmware react?

FW; intermediate; technical screen; conceptual.

## Q148 — An ISR calls an RTOS queue API and crashes. What check?

FW; intermediate; debugging/code review; debugging/scenario.

## Q149 — What does native_sim validate and leave unverified?

FW; intermediate; technical screen; conceptual.

## Q150 — A task is running but the system produces no useful output. How diagnose?

FW; intermediate; debugging/code review; debugging/scenario.

## Q151 — What does a reliable serial protocol need beyond a CRC?

EL/FW; intermediate; technical screen; conceptual.

## Q152 — Design duplicate-safe command handling.

EL/FW; intermediate; coding practical; coding.

## Q153 — Implement bounded resynchronization after malformed input.

EL/FW; intermediate; coding practical; coding.

## Q154 — Design version negotiation for a Linux–MCU link.

EL/FW; intermediate; coding practical; coding.

## Q155 — The same valid command executes twice after timeout. What failed?

EL/FW; intermediate; debugging/code review; debugging/scenario.

## Q156 — How choose a protocol timeout?

EL/FW; intermediate; technical screen; conceptual.

## Q157 — Communication stops after either endpoint resets. What investigate?

EL/FW; intermediate; debugging/code review; debugging/scenario.

## Q158 — Validate a packet field used as an array index.

EL/FW; intermediate; coding practical; coding.

## Q159 — How do checksums, CRCs and MACs differ?

EL/FW; intermediate; technical screen; conceptual.

## Q160 — A command is valid but dangerously stale. Where enforce freshness?

EL/FW; intermediate; debugging/code review; debugging/scenario.

## Q161 — Compare Buildroot and Yocto for a product.

EL/KD; intermediate; technical screen; conceptual.

## Q162 — What is a Buildroot external tree?

EL/KD; intermediate; technical screen; conceptual.

## Q163 — Describe the minimum complete custom application package.

EL/KD; intermediate; coding practical; coding.

## Q164 — What is a Yocto layer, recipe, package and image?

EL/KD; intermediate; technical screen; conceptual.

## Q165 — A recipe builds but the target service cannot start. What inspect?

EL/KD; intermediate; debugging/code review; debugging/scenario.

## Q166 — What is the SDK used for?

EL/KD; intermediate; technical screen; conceptual.

## Q167 — An image changes despite unchanged application source. Why?

EL/KD; intermediate; debugging/code review; debugging/scenario.

## Q168 — What does sstate or a build cache guarantee?

EL/KD; intermediate; technical screen; conceptual.

## Q169 — What belongs in license and SBOM evidence?

EL/KD; intermediate; technical screen; conceptual.

## Q170 — A clean image build runs out of memory. What change first?

EL/KD; intermediate; debugging/code review; debugging/scenario.

## Q171 — How choose GDB, strace, perf or ftrace?

All; intermediate; technical screen; conceptual.

## Q172 — A crash stack points inside libc. How investigate?

All; intermediate; debugging/code review; debugging/scenario.

## Q173 — Build a reproducible latency measurement harness.

All; intermediate; coding practical; coding.

## Q174 — What do ASan, UBSan and race tools miss?

All; intermediate; technical screen; conceptual.

## Q175 — CPU utilization is high but throughput low. What investigate?

All; intermediate; debugging/code review; debugging/scenario.

## Q176 — An apparent memory leak grows only under backlog. What test?

All; intermediate; debugging/code review; debugging/scenario.

## Q177 — How interpret a kernel oops responsibly?

All; intermediate; technical screen; conceptual.

## Q178 — A latency improvement appears only in one run. Can you claim it?

All; intermediate; debugging/code review; debugging/scenario.

## Q179 — How do KASAN and KCSAN relate to userspace sanitizers?

All; intermediate; technical screen; conceptual.

## Q180 — Intermittent failure disappears after adding logs. What do you do?

All; intermediate; debugging/code review; debugging/scenario.

## Q181 — How replace persistent configuration robustly?

EL/KD; advanced; technical screen; conceptual.

## Q182 — Power loss leaves a zero-length config. What investigate?

EL/KD; advanced; debugging/code review; debugging/scenario.

## Q183 — What does signing an update guarantee?

EL/KD; advanced; technical screen; conceptual.

## Q184 — How does A/B rollback work?

EL/KD; advanced; technical screen; conceptual.

## Q185 — An image is signed but for another product. What must happen?

EL/KD; advanced; debugging/code review; debugging/scenario.

## Q186 — Design a health gate before committing an update.

EL/KD; advanced; coding practical; coding.

## Q187 — How do secure boot, verified filesystems and signed updates differ?

EL/KD; advanced; technical screen; conceptual.

## Q188 — What is least privilege for an embedded service?

EL/KD; advanced; technical screen; conceptual.

## Q189 — An SBOM reports an old component version. What next?

EL/KD; advanced; debugging/code review; debugging/scenario.

## Q190 — What should a product maintenance plan contain?

EL/KD; advanced; technical screen; conceptual.

## Q191 — Design a one-path industrial monitoring gateway.

All; advanced; design/project defense; system design.

## Q192 — Design a Linux service supervising several device tasks.

All; advanced; design/project defense; system design.

## Q193 — Design a sensor acquisition driver interface.

All; advanced; design/project defense; system design.

## Q194 — Design a safe field-update workflow for a gateway.

All; advanced; design/project defense; system design.

## Q195 — Design a low-latency Linux telemetry pipeline.

All; advanced; design/project defense; system design.

## Q196 — Design Linux–MCU robot control responsibilities.

All; advanced; design/project defense; system design.

## Q197 — Design diagnostic anomaly inference without disturbing control.

All; advanced; design/project defense; system design.

## Q198 — Design shared DMA buffer ownership for acquisition.

All; advanced; design/project defense; system design.

## Q199 — Design an automated embedded CI test ladder.

All; advanced; design/project defense; system design.

## Q200 — Defend a capstone and plan its next production step.

All; advanced; design/project defense; system design.
