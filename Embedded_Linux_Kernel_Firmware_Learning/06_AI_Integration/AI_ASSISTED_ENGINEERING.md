# AI as a learning and engineering assistant

Use the same loop for every workflow: **attempt independently → request a hint → implement → compile/test → explain without AI**. Record where assistance changed your implementation. An AI-produced file does not demonstrate your competence or establish a working API.

| Workflow | Context to supply | Reusable request | Verification | Common failure |
|---|---|---|---|---|
| Tutor | Target level, own explanation, small misconception | “Ask three questions that expose gaps in my explanation; give one hint at a time, no solution yet.” | Re-derive concept and implement changed example independently | Fluent explanation conceals missing preconditions |
| Source reading | Exact version/commit, header and relevant call sites | “Trace owner/context/error path; cite exact supplied symbols; label unknowns.” | Open definitions and callers in pinned tree; compile tiny use | Invented APIs or stale signatures |
| Documentation lookup | Selected release, architecture and needed behavior | “Find primary references; quote at most a short excerpt; separate documented facts from inference.” | Open cited page/source; confirm release and access date | Link exists but does not support claim |
| Design review | Requirements, rates, state diagram, resource/lock owners | “List concrete failure interleavings and one test for each; prioritize contract violations.” | Walk interleavings and fault fixtures; revise requirements | Generic best practices without an executable test |
| Implementation plan | Interfaces, constraints, current code and accepted design | “Propose smallest complete change with cleanup and verification steps; do not invent dependencies.” | Review API availability; compile incrementally | Large patch hides partial error handling |
| Code review | Small diff, context/ownership contract, selected APIs | “For each suspected bug show input/interleaving and source line; separate certainty and hypothesis.” | Reproduce or reason from documented contract; inspect false positives | Confident but impossible bug scenario |
| Bug hypotheses | Actual error/log, exact command/config, expected behavior | “Rank three causes and propose a cheap discriminating experiment; do not claim diagnosis yet.” | Run one experiment and update hypothesis | Plausible causal story from insufficient trace |
| Tests/edge cases | Input contract and current tests | “Find missing normal/boundary/invalid/fault cases; avoid mirroring my algorithm.” | Independent oracle/model; prove fixture reaches defect | Tests repeat same wrong implementation |
| Build/log analysis | Compiler output, tool versions, relevant snippets | “Identify first meaningful failure and version-dependent assumptions; propose minimal reproduction.” | Run command; preserve full log; verify dependencies | Fixing downstream noise instead of first cause |
| Interview practice | Target track/JD, real project facts, allowed assistance | “Interview one question at a time; score reasoning and evidence; do not invent experience.” | Independent timed task and no-AI explanation | Memorized answer mistaken for competence |
| Documentation | Actual code/test artifacts, audience and limitations | “Write reproducible instructions; label authored/built/run/hardware-pending separately.” | Fresh checkout and link/command audit | Polished docs claim unrun tests passed |

## Gate a generated change

1. Check every API against the chosen headers/source version, not another model response. Confirm callback signatures, configuration dependencies and permissible context.
2. Inspect all allocation/error/cleanup paths, user pointers, integer bounds, concurrency and asynchronous teardown.
3. Compile with strict warnings. Use static analysis supported by the toolchain; warnings are hypotheses to understand, not dismiss blindly.
4. Run meaningful normal/boundary/invalid/failure tests; model a simpler independent oracle where useful. Use sanitizers where supported, with separate race and memory instrumentation if required.
5. Review the actual diff, test logs and coverage limits. Explain the implementation without opening the model answer. Retain evidence and update the matrix only for demonstrated work.

Check invented kernel APIs by searching the pinned tree for the declaration and in-tree users. A real function name can still be wrong for the selected kernel, target configuration or callback context. A patch that compiles can still leak resources, use freed state or mis-handle DMA ownership. Tests do not replace a resource-lifetime argument.

Provide the smallest relevant code/log context. Remove credentials, tokens, keys, customer data and confidential source you are not authorized to share. Follow actual employer/provider policy before sending private code. A model prompt is not a secret vault. Keep production signing keys out of training examples, repositories and chat. During independent assessments/interviews, obey the declared tool rules and disclose assistance honestly.
