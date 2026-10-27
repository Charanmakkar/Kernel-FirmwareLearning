# Interview preparation playbook

Prerequisite for the 30-day revision calendar: completed foundations and usable project evidence. It budgets 90 minutes/day, 45 hours total (roughly 10.5 hours/week). It is revision, not a replacement for first-time kernel or firmware learning. Question/module IDs may include planned material; use the bank index and module delivery catalog to identify what is available.

## Read the role before preparing

Extract exact JD requirements and separate required from desired. Choose EL, KD or FW depth, map each explicit requirement to code/test/defense evidence and identify prerequisites. Ask meaningful role clarifications in the actual interview: userspace versus kernel ownership, target board/kernel, real-time boundaries, update responsibility and required depth. Do not infer a company's exact interview process from general industry patterns.

## Answer structures that expose engineering judgment

Concept: state the definition in one sentence, its boundary/guarantee, one concrete example, then the relevant exception or version qualification. For volatile: describe observable accesses, say what synchronization it does not establish, give a target MMIO context, then identify the correct shared-data primitive.

Coding: clarify inputs/ownership/limits/error behavior; state invariants; propose a small correct implementation; test normal/boundary/invalid/failure input; discuss complexity and resources. Do not optimize away clarity before correctness. If asked for code output, classify undefined/unspecified/implementation-defined behavior before giving a number. A specific compiler observation must be labeled an observation.

Debugging: separate symptom from cause; state two or three hypotheses; choose the cheapest discriminating experiment; inspect an actual return code/trace; minimize; fix; add regression; explain remaining uncertainty. “I would add logs everywhere” is weaker than identifying a state boundary and the values needed to test one hypothesis.

Design: clarify functional requirements, rate/size/deadline/failure budgets and trust boundaries. Draw components/interfaces and owners; specify state/recovery, persistence, update and observability; estimate capacity with stated assumptions; name tradeoffs; define acceptance. Do not let a box diagram replace error handling or timing analysis.

Unknown: say which part you know, identify what is uncertain, reason from a known contract and name the source/experiment you would use. For a kernel callback, “I would verify the signature and context in our pinned tree” is credible; invented API confidence is not.

## Project defense and contribution

Prepare a two-minute account: problem/constraints; architecture/interface; your exact contribution; one serious failure; evidence/fix; limitation and next test. Distinguish authored code, adapted code, supplied reference and independent extension. Use STAR (Situation, Task, Action, Result) only with true events; if no industry example exists, use an honest course/project example. Results may be qualitative when no measurement exists.

Example bullet template, fill only with actual evidence: “Implemented [specific component] for [target/constraint]; validated [named normal/fault cases] using [actual tool]; measured [value/workload] in [report path].” Before independent contribution, say you studied or executed supplied material. Never fill a template with invented uptime, latency, performance percentage or ownership.

## Weekly mock and score review

Calendar days 7/14/21/28 reserve one 60-minute mock plus 30-minute review. Rotate C/Linux, KD, FW then chosen target role. Use a peer or AI interviewer, but record assistance and do the scored code/explanation independently. Score with the gate rubric and block critical failures. Keep recurring-weakness rows: topic, failed reasoning, minimal counterexample, remediation, changed-input retest, retention result. Do not simply rehearse the previous answer.

Revision sheets: (1) object lifetime/size/integer bounds; (2) read/write/EOF/EINTR/EAGAIN; (3) lock/context/owner/teardown table; (4) boot/ELF/sysroot; (5) MCU task/ISR/deadline/watchdog; (6) signature/slot/health/recovery. For each sheet write one invariant, one bug and one test from your own project.

Interview day: confirm time/timezone and allowed tools; ensure a known-good demo with local logs; have source/build IDs ready; check audio/editor; read the actual JD; state assumptions aloud; ask before using AI; preserve confidentiality; and end with known limitations. Do not covertly use assistance where independent work is expected. No learning plan guarantees selection.
