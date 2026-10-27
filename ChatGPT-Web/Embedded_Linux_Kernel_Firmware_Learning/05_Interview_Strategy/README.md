# Interview preparation playbook

Use this playbook after demonstrating the foundations. The aim is to explain, implement, debug and defend a small system under stated constraints. Use the [questions-only bank](../02_Interview_Questions_and_Answers/Questions_Only.md) before its answer key. No employer JD was supplied; the examples below are preparation methods, not claims about a company's hiring process.

## Prioritize an actual job description

Copy each explicit requirement into the skills matrix and preserve its wording and source. Separate required skills, preferred skills and your own inferred prerequisites. “Linux development” does not automatically mean kernel programming; determine whether the work concerns applications, drivers, BSP integration or firmware.

Select five requirements most central to the described work. For each, write your strongest evidence, one missing capability and the smallest task that could expose that gap. Mark untested skills “not assessed.” Start with required capabilities you cannot yet demonstrate, then deepen relevant strengths. Revisit this order after a diagnostic or mock; do not spend scarce revision time expanding an unrelated stack.

| Primary role | Depth to emphasize | Evidence to prepare |
|---|---|---|
| Embedded Linux applications | M06 M07 M14 M15 M16 | Partial I/O, service lifecycle, concurrency, image integration and C01 |
| Kernel and BSP | M08 M09 M10 M11 | Matching build, driver contexts, lifetimes, device descriptions and tested interfaces |
| MCU firmware | M12 M13 | Startup/map, ISR/task boundaries, queues, watchdog and target measurements |

Keep C, ownership, debugging and honest evidence common to all tracks. A simulated demonstration cannot substantiate a claim of physical board bring-up.

## Answer a conceptual question

Give the definition, the governing rule, a concrete example, and a limit. Aim for an initial answer of about one minute, then expand in response to follow-ups.

For a condition variable: “It lets a thread wait for a shared-state predicate. I hold the associated mutex and recheck the predicate in a loop because another consumer can act before I regain the lock. In my bounded queue, the predicate is nonempty or producers finished. The notification itself does not store an item.” This explains behavior the interviewer can challenge. An unexplained list of API names does not.

State assumptions when the answer depends on C dialect, architecture or kernel release. For undefined-behavior questions, identify the violated rule before discussing an observed compiler output. Practice Q001–Q020 and Q071–Q080, then change the example without consulting the answer.

## Solve a coding problem

For a 60-minute exercise, reserve five minutes for requirements, five for the invariant and tests, thirty for implementation, fifteen for verification and five for explanation. Adjust the allocation when the interviewer changes the scope.

Clarify input bounds, null/empty behavior, ownership, error reporting, concurrency and permitted libraries. State the simplest correct invariant before coding. For a ring buffer, explain how full and empty differ; for a complete-write helper, explain how progress survives a short write. Implement the normal path and error paths together. Test zero, one, maximum, malformed input and an appropriate resource failure. Explain unfinished work precisely instead of concealing it. Use Q021–Q040, Q061–Q070 or Q161–Q170 according to the role.

## Investigate a failure

Describe the symptom and its boundary, list observed facts, rank two plausible causes, and choose one observation that separates them. Do not announce a root cause before collecting evidence.

For a serial daemon spinning after disconnect, inspect syscall results and poll events before changing queue sizes. Repeated immediate hangup/error events can explain a busy loop; a trace should distinguish that from an application that never waits. After correcting the termination behavior, reproduce disconnect and normal traffic and check resources. Preserve a regression that fails on the old code. Practice Q081–Q100 and driver scenarios Q121–Q130 using this evidence sequence.

## Develop a design answer

First agree on rates, latency, memory, persistence, failure assumptions and deployment scope. Draw only the components needed for those requirements. Give every buffer, connection and persistent state an owner. Explain overload, startup, shutdown, restart, corrupted input and update interruption. Define what is measured and what result would fail acceptance.

For a Linux–MCU gateway, say which side controls timing, how message freshness is decided and what happens when Linux stops responding. Avoid claiming a watchdog solves every failure. Compare alternatives using the actual constraint: a queue may simplify ownership; a larger queue may worsen stale-data latency. Use Q181–Q190 and defend one tradeoff under a changed requirement.

## Handle unknowns and explain your contribution

A useful response is: “I have not used that exact API. I would first check its execution-context and lifetime contract in the selected release. My current hypothesis is …; this test would distinguish it from ….” Then reason from known principles. Repeated guessing weakens an otherwise sound answer.

For project discussions, state the problem, your own changes, one difficult failure, the evidence behind the fix and remaining limits. Distinguish reference code, dependencies, teammate contributions and AI assistance. Never turn package test results into personal achievements. For behavioral questions, describe a real situation, your responsibility, actions, observed outcome and what you changed afterward; leave outcomes unquantified when you lack records.

## Run a mock and use its feedback

Use the [30-day calendar](Thirty_Day_Revision.md), [revision sheets](Revision_Sheets.md) and [interview-day checklist](Interview_Day_Checklist.md). Ask the reviewer to record specific incorrect statements and missed test cases. Select at most two weaknesses for the next session, repair them, then retest with different inputs. Fluent recall alone does not pass the [readiness gate](../08_Portfolio_and_Job_Readiness/Readiness_Gate.md).
