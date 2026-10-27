# M18 AI assisted learning and embedded inference

## Objectives and prerequisites

Prerequisites: M02 M15 M17.

Use AI to improve reasoning without losing independent competence, and evaluate a small inference extension against a non-AI baseline.

## Lesson


Use the sequence independent attempt, hint, implementation, test and explanation without AI. Begin with a concrete requirement and your own hypothesis. Ask for the smallest useful hint before asking for a complete implementation. After using generated code, inspect ownership, bounds, errors, synchronization and the exact versioned API. A plausible function name or explanation is not documentation.

Supply context deliberately: architecture, source tag, compiler diagnostics, minimal reproducer, expected behavior and constraints. Ask the assistant to separate observations from hypotheses and to propose a test that distinguishes them. For a kernel answer, require the exact declaration in the selected source tree. If a suggested API is missing, investigate the mismatch; do not paste a fabricated prototype into your project to make compilation progress.

AI-generated tests can mirror the implementation's mistake. Define an external behavioral oracle and adversarial cases first. Check boundaries, resource exhaustion, partial progress, concurrency and teardown. Run both a normal build and relevant instrumentation where supported. Review fixes independently and preserve the original failure as a regression. On an assessment, record whether AI was allowed; a good assisted score does not establish unassisted competence.

Before sharing code or logs, remove credentials, customer identifiers and confidential material unless the chosen environment and policy explicitly allow it. Keep secrets outside prompts and repositories. Respect interview rules; never present assisted work as an independent performance when that would be misleading.

For product AI, start from a measurable need such as sensor anomaly detection. Define a non-AI baseline, collect representative data and split training, validation and test by time or device to avoid correlated samples leaking across sets. Choose a threshold on validation data only. Report false alarms and missed faults under the relevant prevalence, not accuracy alone. Synthetic training data is useful for checking a pipeline, but does not establish field accuracy.

Inference belongs in a layer with a defined resource and timing budget. Linux user space can host a suitable runtime; a supported MCU runtime can run small models under tighter memory/operator constraints. LiteRT for Microcontrollers has a distinct deployment model and supported operations; verify compatibility before selecting a board. Quantization can reduce model costs but requires accuracy and hardware evaluation. [LITERT] [ONNX]

Keep deterministic control limits independent of the model. A stale, uncertain or failed inference produces a defined fallback rather than extending motor authorization. Measure model bytes, working memory, latency distribution and CPU usage on the chosen target. C02's optional model extension is a small educational pipeline; its synthetic results must remain labeled as such.


## Worked lab and expected behavior


Use the reusable prompts in `06_AI_Integration`. Take one assessment bug, attempt it independently, then request only competing hypotheses. Test the leading hypothesis and explain the result without reopening the response. Keep an assistance log with the supplied context, suggestion accepted/rejected and evidence.

Run C02's optional anomaly example only after the core simulator passes. Compare it with its deterministic baseline on a held-out set. Treat host execution and synthetic dataset metrics as limited evidence. A model that performs poorly should remain an analysis exercise; it must not replace a working control boundary.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

How did you verify generated code? Why can random dataset splits leak? What happens when inference fails? Interview bank: AI verification and capstone defense.

## Mastery checklist

- Keep an assistance log.
- Verify APIs against selected versions.
- Explain and modify code independently.
- Compare inference with a baseline and preserve fallback.

## Primary references

[LITERT] Google LiteRT for Microcontrollers. [ONNX] ONNX Runtime quantization. Core engineering contracts use the sources in the relevant preceding modules.
