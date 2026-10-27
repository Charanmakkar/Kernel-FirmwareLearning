# Embedded Linux, Kernel and Firmware Learning

**Release 1 — 27 October 2026. Full program still in progress.** Start with [profile and first actions](00_Start_Here/PROFILE_AND_ASSUMPTIONS.md), then attempt [D01](04_Skill_Assessments/questions/D01_Initial_Diagnostic.md) independently. Read [PROGRESS](PROGRESS.md), [manifest](manifest.csv) and [validation](10_Progress_Tracking/VALIDATION.md) before assuming a project or test is complete.

## Read or edit

- [Main Word learning program](Word_Edition/Learning_Program_Release_1.docx)
- [Word interview bank — 200 answers](Word_Edition/Interview_Bank_200_Release_1.docx)
- [Word assessment and practice questions only](Word_Edition/Assessment_Questions_Release_1.docx)
- [Word separate assessment answer keys](Word_Edition/Assessment_Answer_Keys_Release_1.docx)
- [64-week roadmap CSV](01_Learning_Roadmap/roadmap_64_weeks.csv), [project plan CSV](01_Learning_Roadmap/project_plan.csv), [skills matrix CSV](03_JD_JR_Skills_and_Learning_Content/reference_skills_matrix.csv), [learner skills tracker CSV](10_Progress_Tracking/skills_tracker.csv).

Prerequisites: editor, Python and C11 compiler for B01; working Linux for later POSIX/kernel/image work. Follow [environment setup](00_Start_Here/ENVIRONMENT.md); no board purchase required to begin. The observed Windows host passed B01 normal and sanitized tests; WSL startup failed, so Linux/emulator/hardware checks remain pending.

Recommended order: D01 → [prerequisites/gates](01_Learning_Roadmap/PREREQUISITES_AND_GATES.md) → [M01 lesson](03_JD_JR_Skills_and_Learning_Content/M01_C_Objects_Bytes_and_Contracts.md) → [B01 implementation](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/README.md) → independent exercise → role-specific branch. The full three-track plan estimates 704 hours; use actual assessments and a JD to refine it.

The project catalog preserves exactly 5 basic, 5 intermediate, 3 advanced and 2 capstone projects. One reference implementation is delivered; the remaining 14 contain detailed plans. Interview answers are delivered for 200 distinct questions, including 44 coding, 56 debugging/scenario and 10 system-design questions. All learner skills begin unassessed.

CSV files are UTF-8 with BOM for spreadsheet compatibility. Markdown is the editable source of the prose; Word editions are formatted reading copies. Source files use LF newlines. Windows paths in author-run evidence identify the executed host; portable runner paths derive from the project location. The ZIP excludes generated executables and includes code, tests, docs and evidence.

## Navigable index of delivered files

- [00_Start_Here/ENVIRONMENT.md](00_Start_Here/ENVIRONMENT.md)
- [00_Start_Here/PROFILE_AND_ASSUMPTIONS.md](00_Start_Here/PROFILE_AND_ASSUMPTIONS.md)
- [01_Learning_Roadmap/PREREQUISITES_AND_GATES.md](01_Learning_Roadmap/PREREQUISITES_AND_GATES.md)
- [01_Learning_Roadmap/PROJECT_CATALOG.md](01_Learning_Roadmap/PROJECT_CATALOG.md)
- [01_Learning_Roadmap/project_plan.csv](01_Learning_Roadmap/project_plan.csv)
- [01_Learning_Roadmap/roadmap_64_weeks.csv](01_Learning_Roadmap/roadmap_64_weeks.csv)
- [02_Interview_Questions_and_Answers/001_010_C_objects_and_ownership.md](02_Interview_Questions_and_Answers/001_010_C_objects_and_ownership.md)
- [02_Interview_Questions_and_Answers/011_020_Integers_representation_and_behavior.md](02_Interview_Questions_and_Answers/011_020_Integers_representation_and_behavior.md)
- [02_Interview_Questions_and_Answers/021_030_Data_structures_parsing_and_state_machines.md](02_Interview_Questions_and_Answers/021_030_Data_structures_parsing_and_state_machines.md)
- [02_Interview_Questions_and_Answers/031_040_Tools_ABI_C++_and_workflow.md](02_Interview_Questions_and_Answers/031_040_Tools_ABI_C++_and_workflow.md)
- [02_Interview_Questions_and_Answers/041_050_Linux_files_processes_and_service_behavior.md](02_Interview_Questions_and_Answers/041_050_Linux_files_processes_and_service_behavior.md)
- [02_Interview_Questions_and_Answers/051_060_POSIX_I_O_IPC_and_readiness.md](02_Interview_Questions_and_Answers/051_060_POSIX_I_O_IPC_and_readiness.md)
- [02_Interview_Questions_and_Answers/061_070_Threads_locks_and_shutdown.md](02_Interview_Questions_and_Answers/061_070_Threads_locks_and_shutdown.md)
- [02_Interview_Questions_and_Answers/071_080_Architecture_MMIO_interrupts_and_DMA.md](02_Interview_Questions_and_Answers/071_080_Architecture_MMIO_interrupts_and_DMA.md)
- [02_Interview_Questions_and_Answers/081_090_Cross-build_and_boot_diagnosis.md](02_Interview_Questions_and_Answers/081_090_Cross-build_and_boot_diagnosis.md)
- [02_Interview_Questions_and_Answers/091_100_Kernel_contexts_allocation_and_concurrency.md](02_Interview_Questions_and_Answers/091_100_Kernel_contexts_allocation_and_concurrency.md)
- [02_Interview_Questions_and_Answers/101_110_Driver_interfaces_and_lifetimes.md](02_Interview_Questions_and_Answers/101_110_Driver_interfaces_and_lifetimes.md)
- [02_Interview_Questions_and_Answers/111_120_Device_tree_GPIO_and_platform_integration.md](02_Interview_Questions_and_Answers/111_120_Device_tree_GPIO_and_platform_integration.md)
- [02_Interview_Questions_and_Answers/121_130_Buses_IIO_DMA_and_power.md](02_Interview_Questions_and_Answers/121_130_Buses_IIO_DMA_and_power.md)
- [02_Interview_Questions_and_Answers/131_140_MCU_startup_peripheral_state_and_faults.md](02_Interview_Questions_and_Answers/131_140_MCU_startup_peripheral_state_and_faults.md)
- [02_Interview_Questions_and_Answers/141_150_RTOS_timing_priorities_and_fault_policy.md](02_Interview_Questions_and_Answers/141_150_RTOS_timing_priorities_and_fault_policy.md)
- [02_Interview_Questions_and_Answers/151_160_Linux_MCU_framing_and_recovery.md](02_Interview_Questions_and_Answers/151_160_Linux_MCU_framing_and_recovery.md)
- [02_Interview_Questions_and_Answers/161_170_Buildroot_Yocto_and_reproducibility.md](02_Interview_Questions_and_Answers/161_170_Buildroot_Yocto_and_reproducibility.md)
- [02_Interview_Questions_and_Answers/171_180_Debugging_tracing_and_performance.md](02_Interview_Questions_and_Answers/171_180_Debugging_tracing_and_performance.md)
- [02_Interview_Questions_and_Answers/181_190_Persistence_security_updates_and_maintenance.md](02_Interview_Questions_and_Answers/181_190_Persistence_security_updates_and_maintenance.md)
- [02_Interview_Questions_and_Answers/191_200_System_design_and_project_defense.md](02_Interview_Questions_and_Answers/191_200_System_design_and_project_defense.md)
- [02_Interview_Questions_and_Answers/bank.json](02_Interview_Questions_and_Answers/bank.json)
- [02_Interview_Questions_and_Answers/category_counts.json](02_Interview_Questions_and_Answers/category_counts.json)
- [02_Interview_Questions_and_Answers/question_index.csv](02_Interview_Questions_and_Answers/question_index.csv)
- [02_Interview_Questions_and_Answers/questions_only.md](02_Interview_Questions_and_Answers/questions_only.md)
- [03_JD_JR_Skills_and_Learning_Content/exercises/M01_Questions.md](03_JD_JR_Skills_and_Learning_Content/exercises/M01_Questions.md)
- [03_JD_JR_Skills_and_Learning_Content/JD_ANALYSIS_AND_GAP_CLOSURE.md](03_JD_JR_Skills_and_Learning_Content/JD_ANALYSIS_AND_GAP_CLOSURE.md)
- [03_JD_JR_Skills_and_Learning_Content/M01_C_Objects_Bytes_and_Contracts.md](03_JD_JR_Skills_and_Learning_Content/M01_C_Objects_Bytes_and_Contracts.md)
- [03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md](03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md)
- [03_JD_JR_Skills_and_Learning_Content/reference_skills_matrix.csv](03_JD_JR_Skills_and_Learning_Content/reference_skills_matrix.csv)
- [03_JD_JR_Skills_and_Learning_Content/solutions/M01_Solutions.md](03_JD_JR_Skills_and_Learning_Content/solutions/M01_Solutions.md)
- [04_Skill_Assessments/answer_keys/D01_Key.md](04_Skill_Assessments/answer_keys/D01_Key.md)
- [04_Skill_Assessments/ASSESSMENT_PLAN.md](04_Skill_Assessments/ASSESSMENT_PLAN.md)
- [04_Skill_Assessments/questions/D01_Initial_Diagnostic.md](04_Skill_Assessments/questions/D01_Initial_Diagnostic.md)
- [05_Interview_Strategy/INTERVIEW_PLAYBOOK.md](05_Interview_Strategy/INTERVIEW_PLAYBOOK.md)
- [05_Interview_Strategy/revision_30_days.csv](05_Interview_Strategy/revision_30_days.csv)
- [06_AI_Integration/AI_ASSISTED_ENGINEERING.md](06_AI_Integration/AI_ASSISTED_ENGINEERING.md)
- [06_AI_Integration/OPTIONAL_EMBEDDED_ANOMALY_EXTENSION.md](06_AI_Integration/OPTIONAL_EMBEDDED_ANOMALY_EXTENSION.md)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/docs/REVIEW.md](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/docs/REVIEW.md)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/evidence/host.json](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/evidence/host.json)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/evidence/sanitize.json](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/evidence/sanitize.json)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/exercises/EXERCISES.md](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/exercises/EXERCISES.md)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/exercises/REFERENCE_SOLUTIONS.md](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/exercises/REFERENCE_SOLUTIONS.md)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/include/embedded_util.h](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/include/embedded_util.h)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/Makefile](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/Makefile)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/scripts/verify.py](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/scripts/verify.py)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/src/demo.c](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/src/demo.c)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/src/embedded_util.c](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/src/embedded_util.c)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/tests/test_util.c](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/tests/test_util.c)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/VERSIONS.md](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/VERSIONS.md)
- [07_Projects/04_Capstone/CAPSTONE_REQUIREMENTS.md](07_Projects/04_Capstone/CAPSTONE_REQUIREMENTS.md)
- [08_Portfolio_and_Job_Readiness/PORTFOLIO_EVIDENCE.md](08_Portfolio_and_Job_Readiness/PORTFOLIO_EVIDENCE.md)
- [09_References_and_Resources/REFERENCES.md](09_References_and_Resources/REFERENCES.md)
- [09_References_and_Resources/sources.csv](09_References_and_Resources/sources.csv)
- [10_Progress_Tracking/progress_log.csv](10_Progress_Tracking/progress_log.csv)
- [10_Progress_Tracking/skills_tracker.csv](10_Progress_Tracking/skills_tracker.csv)
- [10_Progress_Tracking/VALIDATION.md](10_Progress_Tracking/VALIDATION.md)
- [manifest.csv](manifest.csv)
- [PROGRESS.md](PROGRESS.md)
- [02_Interview_Questions_and_Answers/README.md](02_Interview_Questions_and_Answers/README.md)
- [07_Projects/01_Basic/B01_Embedded_C_Utility_Library/README.md](07_Projects/01_Basic/B01_Embedded_C_Utility_Library/README.md)
- [07_Projects/01_Basic/B02_Linux_process_and_resource_inspector/README.md](07_Projects/01_Basic/B02_Linux_process_and_resource_inspector/README.md)
- [07_Projects/01_Basic/B03_UART_terminal_and_framed-protocol_tool/README.md](07_Projects/01_Basic/B03_UART_terminal_and_framed-protocol_tool/README.md)
- [07_Projects/01_Basic/B04_Multithreaded_sensor_simulator_and_logger/README.md](07_Projects/01_Basic/B04_Multithreaded_sensor_simulator_and_logger/README.md)
- [07_Projects/01_Basic/B05_Cross-compiled_application_running_in_QEMU/README.md](07_Projects/01_Basic/B05_Cross-compiled_application_running_in_QEMU/README.md)
- [07_Projects/02_Intermediate/I01_Custom_Buildroot_appliance/README.md](07_Projects/02_Intermediate/I01_Custom_Buildroot_appliance/README.md)
- [07_Projects/02_Intermediate/I02_Kernel_character_driver_and_user-space_client/README.md](07_Projects/02_Intermediate/I02_Kernel_character_driver_and_user-space_client/README.md)
- [07_Projects/02_Intermediate/I03_Device-tree_GPIO_interrupt_platform_driver/README.md](07_Projects/02_Intermediate/I03_Device-tree_GPIO_interrupt_platform_driver/README.md)
- [07_Projects/02_Intermediate/I04_Custom_Yocto_telemetry_image/README.md](07_Projects/02_Intermediate/I04_Custom_Yocto_telemetry_image/README.md)
- [07_Projects/02_Intermediate/I05_RTOS_MCU_firmware_connected_to_Linux/README.md](07_Projects/02_Intermediate/I05_RTOS_MCU_firmware_connected_to_Linux/README.md)
- [07_Projects/03_Advanced/A01_Sensor_driver_using_the_IIO_subsystem/README.md](07_Projects/03_Advanced/A01_Sensor_driver_using_the_IIO_subsystem/README.md)
- [07_Projects/03_Advanced/A02_Linux_latency_and_performance_investigation/README.md](07_Projects/03_Advanced/A02_Linux_latency_and_performance_investigation/README.md)
- [07_Projects/03_Advanced/A03_Signed_A_B_update_and_rollback_system/README.md](07_Projects/03_Advanced/A03_Signed_A_B_update_and_rollback_system/README.md)
- [07_Projects/04_Capstone/C01_Industrial_monitoring_and_edge_gateway/README.md](07_Projects/04_Capstone/C01_Industrial_monitoring_and_edge_gateway/README.md)
- [07_Projects/04_Capstone/C02_Linux_MCU_robot_control_and_diagnostics_platform/README.md](07_Projects/04_Capstone/C02_Linux_MCU_robot_control_and_diagnostics_platform/README.md)

Final packaging checks: [audit](10_Progress_Tracking/package_audit.json), [file inventory](10_Progress_Tracking/file_inventory.csv).

- [Word rendering attempt record](10_Progress_Tracking/word_render_attempt.json)
