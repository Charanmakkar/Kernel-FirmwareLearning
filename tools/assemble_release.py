from build_program import ROOT, WORKSPACE, write, table, DATE
from pathlib import Path
import csv
import hashlib
import json
import re
import shutil
import zipfile

P=ROOT/'07_Projects/01_Basic/B01_Embedded_C_Utility_Library'
normal=json.loads((P/'evidence/host.json').read_text())
sanitize=json.loads((P/'evidence/sanitize.json').read_text())
assert normal['result']=='passed' and sanitize['result']=='passed'
write('10_Progress_Tracking/VALIDATION.md',r'''
# Validation report — release 1

Date: 27 October 2026 (user timezone Asia/Calcutta). Execution host: Windows x86-64. Exact compiler/runtime/command/source hash details are in B01/evidence/host.json and sanitize.json. This report distinguishes observed execution from planned work.

| Item | Authored | Build verified | Host executed | Emulator executed | Specified hardware executed |
|---|---|---|---|---|---|
| B01 library/demo/tests | yes | yes, Clang strict warnings | yes, normal and ASan/UBSan | not attempted | not attempted/not required for its portable acceptance |
| B01 exercise snippets | yes | not separately checked | not separately checked | not attempted | not attempted |
| M01 exercise snippet | yes | not separately checked | not separately checked | not attempted | not attempted |
| B02–C02 implementations | pending | pending | pending | pending | pending |
| Linux setup commands | yes | not applicable | not executed on Linux | not attempted | not applicable |
| Word documents/ZIP | generated | structural checks in package_audit.json | package audit executed | not applicable | not applicable |

Actual B01 normal and sanitizer stdout: `PASS: 1146739 checks; 340000 ring operations; 100000 parser inputs`, followed by `type=7 payload=3 frame=11`. Both test and demo processes returned 0 in each build. The strict flags were -std=c11 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror, with -O2 normal and -O1 plus address/undefined instrumentation for the sanitized run. See the JSON for full argv and stderr.

What that means: queue/codec arithmetic and tested memory accesses passed these host fixtures on the recorded Clang 22.1.0-rc3 Windows GNU target. It does not prove all possible inputs, all compilers, Linux execution, kernel context correctness or hardware timing. The local executable named gcc is the same Clang toolchain; independent GCC coverage is pending. The learner's competence is not assessed by these author-run tests.

Environment limitation observed: `wsl -d Ubuntu -- bash -lc ...` failed before Linux startup with error 0xd0000022 / Wsl/Service/CreateInstance/STATUS_ACCESS_DENIED. No Linux, QEMU, Buildroot, Yocto, RTOS simulation or physical board test is reported as passed. No WSL reset, host reboot, driver loading, disk flashing or hardware purchase was performed.

Remaining physical checks: exact Linux board image/kernel/toolchain and pinmux, Nucleo revision/jumpers/toolchain/startup, UART voltage/routing, sensor breakout/schematic/address/IRQ, bus electrical behavior, DMA/cache ownership, cold boot/watchdog, measured task/interrupt latency, power-interruption recovery and any robot actuator safety mechanisms. These belong to future implemented projects, not B01's portable test grade.

Package audit checks: exact project count/distribution, roadmap total, interview/category counts/IDs/fields, delivered-file links, evidence/source hashes, DOCX ZIP/XML integrity and ZIP inventory integrity. The audit does not substitute for visual rendering in Word or execution of Linux commands. Render status is recorded separately if performed.
''')

write('PROGRESS.md',r'''
# Progress — release 1, 27 October 2026

## Delivered in this coherent first release

- Profile assumptions, environment lanes and initial D01 diagnostic with separate answer key.
- Required folder organization and a navigable root index of delivered files.
- Three-track reference skills framework (25 rows), evidence tracker with no invented learner scores, and JD gap-closure method.
- Prerequisite map, measurable gates, 64-week/704-hour roadmap, shorter role paths and 30-day/45-hour revision calendar.
- Exactly 15 detailed project plans: 5 basic, 5 intermediate, 3 advanced, 2 capstones. C01/C02 have explicit requirements and proposed fault acceptance matrices.
- Complete M01 lesson with worked examples, guided lab, troubleshooting, independent exercise/separate solution, review and mastery criteria.
- Complete B01 reference implementation, build/run runner, meaningful tests, exercise/solution separation and actual normal/ASan/UBSan host evidence.
- 200-question interview bank with 44 coding, 56 debugging/scenario, 10 system-design, 3 code-output and 87 conceptual questions; every item has an assessed skill, spoken/deeper answer, assumptions, pitfall, follow-up and scoring discriminator.
- Interview strategy, honest project/portfolio guidance, AI engineering workflows and optional embedded anomaly experiment design.
- 37 primary references with version context/access dates; Word editions, CSVs, source files, manifest and ZIP.

## Partial or pending — full master prompt is NOT complete

- M02–M16 remain catalog/planning entries; their full ten-element lessons, independent exercises and separate solutions are pending. M17 has experiment design, not executable inference/training.
- B02–B05, I01–I05, A01–A03, C01/C02 have plans only; complete sources/configs/build/deployment scripts/fixtures remain pending. Exactly one of fifteen reference implementations is delivered.
- Question-bank coding answers are algorithms/contracts and relevant examples; a compiled, scored reference solution suite for all 44 exercises is not delivered. The bank itself is delivered; do not infer 44 tested coding implementations.
- D01, E-M01 and B01 exercises are delivered; full later topic/phase quizzes, timed task fixtures, broken-code/crash/log exercises, per-track full mock scripts and final practical/reference solutions remain pending.
- Linux and emulator execution are pending because WSL could not start and QEMU/toolchains are absent. Physical validation remains pending, including board version/wiring selection for hardware projects. Source research is not build evidence.
- No actual employer JD analysis, learner assessment or independent skill mastery is claimed.

## Exact next coherent task

Author **M02 (toolchain, linking, ELF/ABI, Git and automation)** and **M03's file/proc/process subset**, then deliver **B02 Linux process/resource inspector** with complete C source/build/fixture tests. Use a working Ubuntu 24.04 Linux environment; record tool/package versions, run proc-disappearance/permission/malformed-input tests and mark any unavailable execution honestly. Next complete M03's partial-I/O/termios subset and B03 before the multithreaded B04 work.

Continuation instruction:

> Continue from Embedded_Linux_Kernel_Firmware_Learning/PROGRESS.md and manifest.csv. Preserve the existing 15 project IDs, 200 question IDs and evidence. Complete the exact next task (M02, M03 file/process subset and B02 implementation), update roadmap/matrix links, execute available checks, and regenerate Word editions/ZIP without labeling pending projects complete. Do not overwrite any learner attempts or existing evidence.

No supported background task has been scheduled. Work does not continue after this response unless a new turn requests continuation. The generation scripts in tools/ reproduce the authored release and overwrite generated documents; review changes and preserve learner/evidence files before rerunning them.
''')

manifest=[]
def item(identifier,kind,path,status,validation,next_task):
    manifest.append({'ID':identifier,'Kind':kind,'Path':path,'Completion status':status,'Validation status':validation,'Next task':next_task})
item('START','orientation','00_Start_Here/PROFILE_AND_ASSUMPTIONS.md','complete authored','profile not assessed','Attempt D01')
item('ROADMAP','plan','01_Learning_Roadmap/roadmap_64_weeks.csv','complete authored','64 rows; 704 planned hours','Revise after learner/JD evidence')
item('MATRIX','skills','03_JD_JR_Skills_and_Learning_Content/reference_skills_matrix.csv','reference framework complete','not an employer JD; learner not assessed','Attach actual JD and diagnostic evidence')
item('BANK','interview bank','02_Interview_Questions_and_Answers/README.md','200 questions complete authored','counts/schema checked; no claim of 44 compiled coding solutions','Use independent practice and develop full coding fixtures')
for n in range(1,18):
    item(f'M{n:02d}','lesson','03_JD_JR_Skills_and_Learning_Content/'+('M01_C_Objects_Bytes_and_Contracts.md' if n==1 else 'MODULE_CATALOG.md'),
      'complete lesson' if n==1 else ('partial experiment design' if n==17 else 'pending full lesson'),
      'B01 guided host lab executed' if n==1 else 'not executed',
      'Independent exercise/retention' if n==1 else 'Author full lesson/exercise/solution')
with (ROOT/'01_Learning_Roadmap/project_plan.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):item(r['ID'],'project',r['Folder']+'/README.md','complete implementation' if r['ID']=='B01' else 'plan complete; implementation pending',
        'host and ASan/UBSan passed' if r['ID']=='B01' else 'not built/run','Learner independent extension' if r['ID']=='B01' else 'Complete source/config/tests; validate target')
item('D01','assessment','04_Skill_Assessments/questions/D01_Initial_Diagnostic.md','questions/key delivered','learner not assessed','Attempt independently')
item('ASSESS-LATER','assessments','04_Skill_Assessments/ASSESSMENT_PLAN.md','plan only','no later fixtures executed','Create topic/phase/timed/broken-code/mock/final fixtures and separate solutions')
for id_,path in [('STRATEGY','05_Interview_Strategy/INTERVIEW_PLAYBOOK.md'),('AI-WORK','06_AI_Integration/AI_ASSISTED_ENGINEERING.md'),('PORTFOLIO','08_Portfolio_and_Job_Readiness/PORTFOLIO_EVIDENCE.md'),('REFERENCES','09_References_and_Resources/REFERENCES.md')]:item(id_,'guidance',path,'complete authored','see access/evidence records','Apply to actual learner/target')
table('manifest.csv',manifest)
table('10_Progress_Tracking/progress_log.csv',[{'Date':DATE,'Item':'Release 1 authored','Evidence':'PROGRESS.md; manifest.csv','Independent learner work':'not assessed','Result':'staged release; full master prompt incomplete','Next task':'M02/M03 files-processes subset and complete B02'}])

readme=r'''
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

'''
# Word files are listed explicitly above, and all other current artifacts are indexed here.
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and 'build' not in p.relative_to(ROOT).parts and 'Word_Edition' not in p.relative_to(ROOT).parts and p.name not in ['README.md','package_audit.json','file_inventory.csv']:
        rel=p.relative_to(ROOT).as_posix()
        readme+=f'- [{rel}]({rel})\n'
# Include every project/section README too (only the root README is excluded).
for p in sorted(ROOT.rglob('README.md')):
    if p.parent!=ROOT:
        rel=p.relative_to(ROOT).as_posix();readme+=f'- [{rel}]({rel})\n'
readme+='\nFinal packaging checks: [audit](10_Progress_Tracking/package_audit.json), [file inventory](10_Progress_Tracking/file_inventory.csv).\n'
write('README.md',readme)

if __name__=='__main__':print('Assembled master index, truthful status manifest and validation report')
