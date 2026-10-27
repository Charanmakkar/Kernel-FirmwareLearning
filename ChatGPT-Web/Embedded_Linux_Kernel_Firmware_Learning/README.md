# Embedded Linux Kernel and Firmware Learning

Start with the diagnostic, then use the roadmap to build evidence for your chosen role. The program keeps embedded Linux applications, kernel/BSP development and MCU firmware/RTOS distinct while sharing C and engineering foundations.

## Open first

1. [Profile and study method](00_Start_Here/Profile_and_Study_Method.md)
2. [Environment setup and version contract](00_Start_Here/Environment_Setup.md)
3. [Diagnostic and assessment folder](04_Skill_Assessments/README.md)
4. [Roadmap and prerequisite sequence](01_Learning_Roadmap/Roadmap_and_Prerequisites.md)
5. [Learning modules](03_JD_JR_Skills_and_Learning_Content/README.md)
6. [B01 C utility library](07_Projects/01_Basic/B01_C_Utility_Library/README.md)

The schedule is a 572-hour core plan spread over 52 weeks. Extra prerequisite remediation and hardware bring-up may extend it. Your skills begin as not assessed; fill the tracker with your own independent evidence.

## Main deliverables

| Folder | Material |
| --- | --- |
| 00_Start_Here | Assumptions, setup, diagrams and original prompt |
| 01_Learning_Roadmap | Full weekly roadmap and focused interview path |
| 02_Interview_Questions_and_Answers | 200 questions, separate structured answers and index |
| 03_JD_JR_Skills_and_Learning_Content | 18 lessons, exercises, solutions and reference skills matrix |
| 04_Skill_Assessments | Diagnostic, timed tasks, broken-code/log fixtures, mocks and separate keys |
| 05_Interview_Strategy | 30-day revision calendar and practical interview playbook |
| 06_AI_Integration | 10 reusable workflows, verification rules and assistance log |
| 07_Projects | Exactly 5 basic, 5 intermediate, 3 advanced and 2 capstone projects |
| 08_Portfolio_and_Job_Readiness | Project evidence and truthful resume/defense guidance |
| 09_References_and_Resources | Primary references with access dates and refresh policy |
| 10_Progress_Tracking | Editable workbook/CSVs, validation records and learner evidence tracker |

The [Word handbook](Embedded_Linux_Kernel_Firmware_Handbook.docx) consolidates reading material. The [tracking workbook](10_Progress_Tracking/Learning_Roadmap_and_Skills_Tracker.xlsx) has learner, weekly roadmap and skills matrix sheets. [FILE_INDEX.md](FILE_INDEX.md) links every packaged file.

## Run and verify

On a Linux host with Python 3, C/C++ compilers, make and OpenSSL, run:

```sh
python3 tools/verify_host_package.py
```

This offline runner rebuilds and checks the applicable host portions. Cross builds, real RTOS dependencies, emulation, image builds and hardware have their own setup instructions. Read [Validation_Summary.md](10_Progress_Tracking/Validation_Summary.md) before interpreting a pass. The reference logs establish package checks; they do not establish your proficiency.

## How to study

Attempt each exercise before opening its solution. Use AI for a hint or review only after your attempt, then explain a changed case independently. Keep questions and answer keys separate during timed work. Pass the current phase's critical correctness gates before adding harder features. Link every claim to source, test or observation.

Kernel examples target frozen source APIs in disposable guests. No physical hardware execution is claimed. Complete the named board/runtime checks before representing a driver, firmware target or robot as hardware validated. See [PROGRESS.md](PROGRESS.md) for remaining execution and a precise next task.
