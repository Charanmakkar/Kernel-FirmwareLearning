# AI workflows and reusable prompts

Use these prompts after an independent attempt. Replace bracketed fields with verified context. Record assistance in the study log, and follow the allowed-tool rules of each assessment.

## Workflow 1 Socratic concept tutor

Context to supply: Your current explanation, a small example, module and target architecture.

Prompt:

> Act as a Socratic tutor for [concept]. Here is my explanation: [text]. Ask one question that reveals the most consequential misunderstanding. Do not give a full solution yet. After my answer, use one concrete counterexample and ask me to predict the result. Distinguish C language rules, compiler behavior and hardware behavior.

Verification: Explain a changed example without the conversation; check normative claims in the named official reference.

Common failure: A fluent analogy can hide incorrect ordering, ownership or version assumptions.

## Workflow 2 Read unfamiliar source

Context to supply: Repository commit, exact files, entry point and the behavior you want to trace.

Prompt:

> Trace [event] through these supplied source files at commit [commit]. Name the entry point, key state changes, resource owners, locks and error paths. Cite file and function names that actually exist in the supplied code. Mark any unavailable dependency as unknown. Finish with three observations I can collect to check your trace.

Verification: Search the source for every named function; step through or instrument one end-to-end transaction.

Common failure: Invented helper functions and unseen dependencies can make a false architecture look plausible.

## Workflow 3 Find the correct versioned API

Context to supply: Kernel/tool version, declaration you found, required context and compiler diagnostics.

Prompt:

> For [exact version], identify the official contract for [API]. State whether it can sleep, its return-value convention, ownership and cleanup requirements. Give the official URL or exact source path and quote only the minimal declaration needed. If you cannot inspect that version, say so and provide a search plan instead of inventing a signature.

Verification: Open the versioned source/header yourself and compile a minimal use under the actual configuration.

Common failure: An API can exist on a newer branch but have a different signature or behavior on the target.

## Workflow 4 Review a design before coding

Context to supply: Requirements, architecture, data ownership, execution contexts and target limits.

Prompt:

> Review this design against the stated requirements. Identify the three most consequential correctness risks, each with a failure sequence and a test that would expose it. Check buffer ownership, concurrency, blocking, restart and teardown. Separate required changes from optional complexity. Do not rewrite the system until the interface contracts are clear.

Verification: Walk a normal operation and a failure through every resource owner; implement a minimal risk-focused test.

Common failure: A review can recommend sophisticated mechanisms that solve no requirement and introduce new lifetimes.

## Workflow 5 Adversarial code review

Context to supply: Complete changed function plus callers, tests, protocol and build flags.

Prompt:

> Review only this change and its relevant callers. Look for bounds errors, integer overflow, partial I/O, stale state, deadlock, races and incomplete cleanup. For each finding give a concrete input or interleaving and the affected requirement. Do not report style preferences as bugs. State which context is missing.

Verification: Reproduce each claimed defect; reject findings that rely on an impossible precondition.

Common failure: False positives waste time, while isolated snippets hide caller guarantees or real shared-state hazards.

## Workflow 6 Generate independent tests

Context to supply: External interface contract and allowed/invalid input classes before implementation details.

Prompt:

> Design tests for this interface from its contract. Include boundaries, malformed inputs, repeated calls, allocation/I/O failure and state transitions. Define expected outcomes and explain which requirement each test checks. Keep a separate list of properties not covered by these tests. Do not derive expected results by calling the implementation under test.

Verification: Make one meaningful mutation or reintroduce the known bug and confirm the relevant test fails.

Common failure: Tests can mirror the same mistaken algorithm or merely check that a function returns.

## Workflow 7 Investigate build errors

Context to supply: Exact command, first meaningful error, tool versions, relevant configuration and recent diff.

Prompt:

> Analyze this build failure. Separate the first causal diagnostic from downstream messages. Rank at most three hypotheses and give a small check to distinguish them. Explain whether the issue is source, API version, configuration, toolchain or link/runtime mismatch. Do not suppress warnings or add casts without proving the type contract.

Verification: Run the smallest discriminating check and rebuild from a clean affected target.

Common failure: Changing random flags can hide an ABI mismatch or run an old executable after a failed build.

## Workflow 8 Analyze logs and crashes

Context to supply: Original timestamped logs, matching build ID, expected behavior and actions before failure.

Prompt:

> Create a timeline using only observed events. Label hypotheses separately. Identify the earliest divergence from expected behavior and what the evidence cannot establish. Propose the next two observations that would distinguish likely causes. Preserve raw error values and units. Do not invent missing log lines.

Verification: Correlate timestamps/clocks and reproduce with the same build; verify symbol files before trusting a backtrace.

Common failure: Merged clocks, truncated logs and mismatched symbols can produce a persuasive but false causal story.

## Workflow 9 Conduct a mock interview

Context to supply: Chosen track, level, covered modules and whether hints are allowed.

Prompt:

> Interview me for [track and level]. Ask one question at a time, wait for my answer, then probe assumptions with a changed case. Score correctness, reasoning, edge cases and communication using the package rubric. Do not reveal the full answer before I attempt it. Record concrete gaps and one practical retest for each.

Verification: Repeat a different variant with no assistant or reference material and compare the rubric evidence.

Common failure: Memorizing the assistant answer can inflate apparent readiness without implementation ability.

## Workflow 10 Write truthful project documentation

Context to supply: Your actual changes, test logs, limitations and measured values.

Prompt:

> Draft an architecture and demonstration note from the supplied evidence. Separate code authored, build verified, host execution, emulator execution and hardware execution. Do not invent speedups, reliability claims or personal contributions. Turn each test result into a bounded statement with its input and environment. List missing checks plainly.

Verification: Compare every claim and numeric value with an existing log or source artifact.

Common failure: Polished language can exaggerate an object compile into a working driver or a simulation into hardware proof.

## Independent learning checkpoint

After assistance, close the answer and explain the code from memory. Change one requirement and implement the change without copying. Run a fresh failure case. If you cannot do this, keep the learner status as implemented with assistance and plan a retest. AI can accelerate feedback; it cannot provide your evidence of independent competence.

## Handling code and credentials

Supply minimal reproducible examples. Remove secrets, credentials, customer identifiers and proprietary details unless your organization's approved environment and policy allow them. Do not paste private keys to ask whether signing works. Use disposable lab keys and share only the required public verification material. Keep an audit of accepted changes and their tests.

## Embedded inference extension

C02 contains a small optional anomaly pipeline after the deterministic robot core. Treat its synthetic dataset as a software-pipeline fixture. It does not establish detection quality on an AMR or industrial plant. Begin with a threshold or statistical baseline, split data by acquisition run/device/time, tune only on training/validation and evaluate the final model once on held-out data. Count false alarms and missed faults and report the sample population.

Measure model file bytes, working memory, latency distribution and CPU cost on the target that will run inference. A host latency is not an MCU latency. Keep sampling/control and hard limits deterministic, and define fallback for invalid input, model failure, excessive latency and distribution shift. Linux user-space inference or a supported MCU runtime are options; select based on actual operators and resource limits, not model marketing. [LITERT] [ONNX]

The extension passes only if the core acceptance tests still pass, the evaluation split is documented, the baseline comparison is reported honestly and failure never extends command freshness or actuator permission.
