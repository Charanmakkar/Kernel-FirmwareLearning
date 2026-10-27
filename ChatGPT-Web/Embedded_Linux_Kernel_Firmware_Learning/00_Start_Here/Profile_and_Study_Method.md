# Your starting point and study method

This program develops evidence for three related jobs: embedded Linux system software, Linux kernel and board support, and microcontroller firmware with a real time operating system. Choose one primary hiring target after the diagnostic. Learn the shared foundations once, then allocate depth according to the target job description. Completion means you can explain, change, test and debug your own implementation.

## Working assumptions

No personal proficiency, specific job description, interview deadline, board inventory or computer specification has been supplied. Your starting skills are **not assessed**. The planning baseline is junior to mid level preparation with 10 to 12 study hours each week. The 52 week schedule contains 572 planned hours at 11 hours per week. This includes lessons, projects and assessment; project effort is not added a second time. Budget a further 80 to 180 hours if the diagnostic reveals weak C foundations or if you complete physical board bring-up. A full three-track study therefore merits approximately 12 to 18 months as an initial planning estimate, with longer duration possible. Nine to twelve months is a focused-track target only if prerequisites are already demonstrated.

The minimum project scope uses a Linux host, emulated applications, a real FreeRTOS host port, and explicitly identified host simulations for system integration. Physical GPIO, I2C, electrical timing, motor behavior and power interruption remain separate validation work. The robot capstone is an educational demonstrator. Its software stop condition is not an industrial safety function.

## Choose your primary track

| Track | Work you must demonstrate | Additional depth after shared foundations |
| --- | --- | --- |
| Embedded Linux system software | A service that handles real I/O failures and ships in a reproducible image | Process lifecycle, sockets, IPC, image integration, persistence, updates and observability |
| Kernel and BSP | A driver whose contexts, synchronization and resource lifetimes you can defend | Device tree, bus/subsystem APIs, IRQs, DMA, power management, configuration and board bring-up |
| MCU firmware and RTOS | A bounded state machine with measurable timing and recovery | Startup/linker configuration, peripherals, ISR contracts, scheduling, watchdogs and firmware updates |

Do not claim all three specialties from completing one demonstration. For a kernel position, hardware and kernel runtime evidence matter; a Python sensor simulator does not establish driver competence. For an MCU position, host-port execution does not establish interrupt latency or stack sufficiency on the selected chip.

## First study session

1. Read the environment guide and record the host/compiler versions.
2. Take the diagnostic in `04_Skill_Assessments` before opening its answer key. Save your attempt and time used.
3. Start M01 and M02. Build B01 from its README, then close the reference code and implement the independent ring-buffer exercise.
4. Record a source commit or file hash, test log and five-minute verbal explanation. Leave your tracker status as not assessed until evidence is scored.
5. Retake the weak topics after a delay with changed input data. A remembered solution is insufficient evidence of transfer.

## A sustainable study week

Allocate three hours to lessons and source reading, four to implementation, two to tests and fault investigation, one to independent recall, and one to review and evidence. Shift lesson time toward projects when integrating a capstone. End each week by explaining one bug, one design tradeoff and one result without AI assistance.

An exit test passes only if its required behaviors and critical correctness gates pass. Out-of-bounds access, a demonstrated race, unsafe resource lifetime, accepting invalid commands, or claiming unrun evidence requires correction even if other marks are high. Keep failed attempts: a defensible diagnosis and regression test are valuable interview evidence.

## Depth labels

**Explain** means reason accurately with an example. **Implement** means build the feature from a requirement. **Debug** means diagnose an unfamiliar failing case with evidence. **Recognize** means identify where the concept applies and find its authoritative contract. **Defer** means postpone until the JD or hardware demands it. C ownership, partial I/O, concurrency and failure handling require implement and debug depth across tracks. RCU and DMA begin at recognize/explain depth for a junior application role and become deeper requirements for a relevant driver role.
