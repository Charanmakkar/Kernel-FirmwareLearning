# JD analysis and prioritized gap closure

No actual employer posting was supplied or sampled. The CSV is a reference skills framework. Its must-have labels are this program's track-level recommendations, not claims about any company. Current evidence and gap remain “not assessed.” The interview ranges reserve a taxonomy across Q001–Q200; check the bank's delivery index before assuming an answer exists.

When a JD arrives, retain exact requirement text and source URL/access date locally. Give it a JD-specific ID, mark explicit wording versus inference, and classify requirement/desired qualification. For example, “develop SPI drivers” explicitly points to driver depth; “embedded Linux” alone does not establish Yocto, a particular RTOS, or GPU expertise. Record those as inferred possibilities until clarified.

For each requirement: state observable expected depth; map prerequisites; attach existing evidence without inventing a proficiency score; identify missing evidence; link module, project, assessment and question IDs. Use `not assessed`, `attempted`, `demonstrated with help`, `independent pass`, or `retention pass`. A copied reference implementation cannot be `independent pass`.

Prioritization: P0 safety/correctness foundations S01–S03/S08, P1 explicit must-have requirements in the selected role, P2 gaps blocking a relevant portfolio project, P3 desired requirements, P4 optional extensions. Within one priority choose the dependency that unlocks the most required work, not the newest technology. Do not assign numerical gap scores before assessment.

After D01: if C fails, start M01/B01 and postpone kernel work; if Linux practical fails, practice files/processes before image building; if synchronization fails, implement a bounded producer-consumer queue before lock-free or ISR-shared structures. Reassess using changed inputs, an independent explanation and a new fault. Update the tracker and source evidence after each gate, not after reading a chapter.

A focused KD interview path may put I02/I03 ahead of I04. A firmware JD may prioritize startup, UART DMA, RTOS and measured watchdog behavior, while postponing Yocto. An EL systems role usually needs robust process/service and deployment evidence before custom kernel interfaces. Keep a dated explanation for each branch decision.
