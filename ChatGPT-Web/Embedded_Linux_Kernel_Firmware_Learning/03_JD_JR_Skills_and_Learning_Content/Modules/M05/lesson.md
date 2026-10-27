# M05 Processor and operating system foundations

## Objectives and prerequisites

Prerequisites: M02.

Explain virtual memory, privilege, scheduling and device access, and separate application processors from microcontrollers.

## Lesson


An application processor normally runs a rich OS with a memory management unit, or MMU, translating virtual addresses into physical mappings. A process has an address-space view, credentials and resources. Threads in one process share that view but have separate execution contexts and stacks. A context switch changes the executing task; a system call crosses a privilege boundary without necessarily switching to another process.

A microcontroller often uses a simpler memory map and a memory protection unit, or MPU, where present. An MPU controls permissions over regions rather than providing the general virtual-address translation expected by Linux applications. Firmware may execute directly from flash and manage peripherals itself. A successful Linux application build says nothing about the startup vector or linker script needed for an MCU image.

The CPU can reorder operations subject to architectural rules; compilers can transform code subject to language rules. A cache improves access latency but introduces visibility and ownership questions. Coherence and ordering are different: seeing a consistent value for one location does not define the order in which different locations become visible. Locks and atomic operations provide particular synchronization contracts; a compiler barrier alone does not necessarily constrain the CPU.

Memory-mapped input/output, or MMIO, assigns device registers to an address range. Reads can have side effects and writes can clear bits or start hardware. Do not use ordinary memory assumptions such as speculative reads, arbitrary-width access or read-modify-write without the register contract. Linux drivers use MMIO accessors, mappings and the DMA API. A DMA address is the address a device uses; it is not generally a CPU pointer or physical address. [DMA]

Interrupts report an event asynchronously. Keep the hard interrupt work bounded and defer sleepable operations to an appropriate context. Interrupt priority, masking and dispatch latency depend on the architecture and OS configuration. A high task priority cannot overcome a disabled-interrupt interval, a blocking bus transaction or an invalid control design.

The scheduler chooses runnable work. Throughput, fairness and deadlines are different objectives. A regular Linux scheduling observation is not a hard real-time guarantee. To claim a deadline, define the worst acceptable delay, the workload, interrupts, competing tasks and measurement method, then test the appropriate target and analyze bounds. An average latency conceals a long tail.


## Worked lab and expected behavior


Run B02 on your process and another accessible process. Compare thread count and resident memory; inspect mappings separately in `/proc/PID/maps`; do not interpret virtual size as physical RAM consumption. Inspect `/proc/self/maps` and explain executable, stack, library and anonymous mappings. Use `readelf -S` to relate executable sections to runtime mappings without assuming a one-to-one layout.

Draw the path from a user buffer through a system call, driver and device. Annotate which address is a user pointer, CPU virtual address and DMA address. If a tool's memory numbers disagree, identify units, shared pages, sampling time and permissions before concluding one tool is broken.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain process versus thread, MMU versus MPU and cache coherence versus ordering. Interview bank: architecture, OS and timing.

## Mastery checklist

- Trace one operation across privilege boundaries.
- Distinguish CPU and device addresses.
- State the limits of a host timing experiment.
- Explain application processor versus MCU startup.

## Primary references

[DMA] Linux DMA mapping guide. [CMSIS] Arm CMSIS startup. [NVIC] Arm NVIC documentation. [KLOCK] Linux lock types.
