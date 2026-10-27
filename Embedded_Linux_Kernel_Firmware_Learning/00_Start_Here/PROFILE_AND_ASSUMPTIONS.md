# Profile, assumptions, and scope

Prepared 27 October 2026. This is release 1 of a staged program, not a claim that the entire master prompt has been completed. Read PROGRESS.md for exact coverage. A learning artifact existing is never evidence of the learner's skill.

No experience profile, target job description (JD), job requirements (JR), interview date, board inventory, or budget was supplied. Your workspace is Windows with PowerShell. We observed Python 3.13.2 and an LLVM-MinGW Clang 22.1.0-rc3 toolchain; the executable called gcc is also Clang, not a second compiler. WSL lists Ubuntu but launching it failed with STATUS_ACCESS_DENIED. We did not change your WSL installation or computer settings.

Provisional learner: junior-to-mid-level applicant, 10–12 hours weekly, no presumed proficiency. C, Linux, electronics, and debugging are **not assessed**. These assumptions choose a starting point; they do not estimate your current ability. Complete D01 before deciding what to skip.

The requested 9–12 months is an initial planning window. At 11 hours/week, 39–52 weeks supplies 429–572 hours. The complete three-track program below budgets 704 hours over 64 weeks: 386 project hours and 318 lesson, practice, assessment, review, and contingency hours. That is roughly 15 months, with another 8–16 weeks possible if C/Linux prerequisites fail. These are planning estimates, not measured learning times or a mastery guarantee. The tracks share foundations but require different evidence. Preparing for one role can fit a shorter path; completing all 15 projects should not delay a well-supported application to a narrower role.

## Three tracks

| Track | Core evidence | Additional depth | Recognize initially; defer until relevant |
|---|---|---|---|
| EL: Embedded Linux/system software | Robust C service, IPC, cross-built executable, image boot, logs and failure tests | Packaging, sysroots, deployment, networking, storage, updates, service operations | Deep scheduler modifications, custom bus controller drivers |
| KD: Kernel/drivers/BSP | Build the selected kernel; defend driver lifetimes and locking; device-tree binding and probe evidence | Execution contexts, subsystem interfaces, IRQ/DMA ownership, power management, platform boot | New filesystem, GPU, or network stack implementation |
| FW: MCU/bare metal/RTOS | Link/start a target, peripheral state machine, bounded task/ISR design, measured timing and recovery | MCU memory map, startup/vector/linker work, interrupt priorities, watchdog and stack budgeting | Linux VM internals and Yocto layer internals unless the role integrates them |

Shared foundations: C object lifetime and integer behavior, interfaces, state machines, reproducible builds, Git, debugging, test design, and accurate technical communication. An application processor with a Memory Management Unit (MMU) running Linux and a Cortex-M microcontroller running firmware are different targets. QEMU virt is a virtual application processor board; Zephyr native_sim is a host simulation of RTOS application behavior, not a model of the chosen STM32's electrical or interrupt timing.

## Personalization inputs to add after D01

Record the actual JD text and URL; target track and seniority; diagnostic artifacts; available hours and deadline; host RAM/disk; boards and tools already owned; budget and industry. These materially change priorities. Until then, all skills-matrix requirements are an explicitly authored reference framework, not an employer's requirements. Do not assign a numeric proficiency score from a chat description alone.

## Start today (about two hours)

1. Attempt D01 without AI and save source, command transcript, and explanations.
2. Install no board software yet. Read ENVIRONMENT.md and run the B01 portable test command if your compiler is available.
3. Study M01, implement exercise E01 independently, then compare the separate solution.
4. Put your result and artifact path in skills_tracker.csv; leave all other skills unassessed.

Keep reference answers closed until you attempt a task. A Windows-native C pass supports portable utility logic only; it says nothing about POSIX APIs, kernel modules, or MCU peripherals.
