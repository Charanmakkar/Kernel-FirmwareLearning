# Scoring and evidence rules

A score measures the submitted attempt, not the person's general proficiency. Use `not assessed` until there is an artifact, date, and reviewer or self-review record. Retain source revision, build command, input, output, and an explanation of remaining uncertainty.

For a 100-point practical assessment, score correctness 30, reasoning 15, debugging method 15, resource handling 10, concurrency or state handling 10, tests 10, and communication 10. When a category is inapplicable, its points must be reassigned in the assessment before the attempt; do not change the rubric afterward to improve the result. A default pass is at least 75 with all critical gates satisfied. A 90-minute diagnostic is routing evidence, not a certification or pass/fail employment test.

Critical gates override totals. Fail the relevant gate if the submission knowingly leaves exploitable bounds errors on supplied inputs, use-after-free, unsynchronized conflicting shared access, indefinite required shutdown, fabricated results, acceptance of an unauthenticated update where authentication is required, or motion continuing beyond the specified local timeout. A persuasive explanation does not compensate for those failures. Correct the defect, add a regression, and retake the affected part with changed inputs. Do not average a failed critical gate into a high overall score.

Mark evidence separately as authored, build verified, host tests executed, emulator tests executed, specified hardware tests executed, and pending checks. An emulator success is not a measurement of electrical behavior, interrupt latency, cache coherency, DMA, or sensor accuracy on an absent board.

For oral questions, use the four one-point criteria in the bank. Score 0 for no valid mechanism, 1 for one correct criterion, up to 4 for all four. Require a concise explanation first, then probe one boundary or failure. A critical misconception makes the question fail even if three superficial criteria are present. A question-level score cannot replace the practical gate.

Retakes use a new input seed or changed requirement. Keep the original attempt and a short error analysis; do not overwrite failures. Mark a skill `demonstrated independently` only after a clean independent practical and a credible explanation. Use `assisted practice` for AI-supported work. Mastery is never inferred from possession of a generated solution.
