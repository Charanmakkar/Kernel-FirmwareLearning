# Interview bank — 200 distinct questions with answers

This bank is delivered for all three tracks. It is interview practice, not a substitute for the still-pending full lessons and project implementations. Primary-source IDs resolve in ../09_References_and_Resources/REFERENCES.md. Concept and design answers use stated assumptions; target API signatures must be checked in the selected source before implementation. No company-specific interview pattern or experience claim is asserted.

**Scoring for every question:** 0 = unsafe/incorrect or invented evidence; 1 = recognizes terminology but misses the contract; 2 = gives the core spoken answer with key assumptions; 3 = explains the deeper example and avoids the named pitfall; 4 = also satisfies the question-specific discriminator, handles the follow-up, and proposes a meaningful boundary/failure test. A memory-safety/context/security critical error blocks passage regardless of average. Use changed input for a retention attempt. Coding answers describe complete algorithm/contracts; only code explicitly delivered in project/solution files is a compiled reference implementation. Do not treat design outlines as executed code.

Use questions_only.md for attempts, then open a topic answer file. Difficulty and round are practice organization, not employer claims. Module links for undelivered lessons lead to a status catalog.

- [001–010: C objects and ownership](001_010_C_objects_and_ownership.md) — All; M01.
- [011–020: Integers, representation and behavior](011_020_Integers_representation_and_behavior.md) — All; M01.
- [021–030: Data structures, parsing and state machines](021_030_Data_structures_parsing_and_state_machines.md) — All; M01.
- [031–040: Tools, ABI, C++ and workflow](031_040_Tools_ABI_C++_and_workflow.md) — All; M02.
- [041–050: Linux files, processes and service behavior](041_050_Linux_files_processes_and_service_behavior.md) — EL/KD; M03.
- [051–060: POSIX I/O, IPC and readiness](051_060_POSIX_I_O_IPC_and_readiness.md) — EL; M03.
- [061–070: Threads, locks and shutdown](061_070_Threads_locks_and_shutdown.md) — All; M04.
- [071–080: Architecture, MMIO, interrupts and DMA](071_080_Architecture_MMIO_interrupts_and_DMA.md) — KD/FW; M05.
- [081–090: Cross-build and boot diagnosis](081_090_Cross-build_and_boot_diagnosis.md) — EL/KD; M05/M06.
- [091–100: Kernel contexts, allocation and concurrency](091_100_Kernel_contexts_allocation_and_concurrency.md) — KD; M07.
- [101–110: Driver interfaces and lifetimes](101_110_Driver_interfaces_and_lifetimes.md) — KD; M08.
- [111–120: Device tree, GPIO and platform integration](111_120_Device_tree_GPIO_and_platform_integration.md) — KD; M09.
- [121–130: Buses, IIO, DMA and power](121_130_Buses_IIO_DMA_and_power.md) — KD; M13.
- [131–140: MCU startup, peripheral state and faults](131_140_MCU_startup_peripheral_state_and_faults.md) — FW; M11.
- [141–150: RTOS timing, priorities and fault policy](141_150_RTOS_timing_priorities_and_fault_policy.md) — FW; M12.
- [151–160: Linux–MCU framing and recovery](151_160_Linux_MCU_framing_and_recovery.md) — EL/FW; M12.
- [161–170: Buildroot, Yocto and reproducibility](161_170_Buildroot_Yocto_and_reproducibility.md) — EL/KD; M10.
- [171–180: Debugging, tracing and performance](171_180_Debugging_tracing_and_performance.md) — All; M14.
- [181–190: Persistence, security, updates and maintenance](181_190_Persistence_security_updates_and_maintenance.md) — EL/KD; M15.
- [191–200: System design and project defense](191_200_System_design_and_project_defense.md) — All; M16.

Actual category counts (each question has one primary category): conceptual: 87, coding: 44, debugging/scenario: 56, code-output analysis: 3, system design: 10. Some coding/design questions also contain debugging scenarios, but those overlaps are not counted twice.
