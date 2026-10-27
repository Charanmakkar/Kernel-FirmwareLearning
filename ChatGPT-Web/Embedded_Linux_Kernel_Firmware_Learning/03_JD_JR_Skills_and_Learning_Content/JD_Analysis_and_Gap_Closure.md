# Reference skills and JD gap closure

The supplied matrix is a reference framework authored for this program. It is not a transcription of an employer's requirements and does not score your proficiency. Every current-evidence and skill-gap field starts at not assessed. The priority column expresses curriculum emphasis only; replace it with the actual must-have or nice-to-have language when a JD is supplied.

## Convert a real JD into evidence requirements

Save the JD text, employer URL and access date. Give each explicit requirement a separate JD identifier and preserve its original wording. Add inferred recommendations in separate rows labelled inferred. Identify the role track, the expected action and depth, then connect the requirement to prerequisites, modules, project code, question IDs and an assessment. Do not infer a requirement for every topic simply because the job title contains embedded.

For example, an explicit requirement to develop Linux I2C drivers maps to M08 through M11 and A01. Evidence should include datasheet interpretation, subsystem choice, matching/binding, error handling and kernel/hardware runtime checks. A host conversion test supports the numerical portion but does not close the entire driver gap. An explicit requirement to maintain a telemetry service maps primarily to M06, M07, M14, M16 and C01; custom kernel development may be optional.

## Prioritize after the diagnostic

First correct critical C and concurrency failures that would invalidate later work. Next prioritize explicit must-haves with no evidence, then high-frequency responsibilities represented in the actual JD, and finally nice-to-haves. Record the impact of each gap in plain language: cannot safely handle partial reads, cannot reproduce a target image, or cannot explain driver teardown. Avoid a numerical confidence score without assessment evidence.

For each gap define one specific completion artifact: a changed source file and regression test, a boot log with version record, a timing report with raw data, or a recorded project defense. Set the next task small enough to finish in one or two study sessions. Reassess the requirement after the task; do not mark a skill mastered because the supplied reference code already exists.

## Record depth honestly

Use not assessed, learning, implemented with assistance, independently demonstrated and needs refresh as learner states. Track execution evidence separately: authored, compile checked, host tested, emulator tested and named-hardware tested. These are different axes. A driver can be authored and object-compiled while the learner still needs to understand it and hardware validation remains pending.

The question bank contains a module column. Filter by that column to choose oral checks, then replace the matrix's module-based question selector with exact Q IDs relevant to the selected employer requirement. An oral answer supplements a practical demonstration; it does not replace one.
