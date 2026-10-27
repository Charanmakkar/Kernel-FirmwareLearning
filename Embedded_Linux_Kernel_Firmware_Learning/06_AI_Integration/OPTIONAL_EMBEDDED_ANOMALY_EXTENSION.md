# Optional capstone extension — anomaly diagnostics

Status: complete experiment design; executable training/inference implementation and measurements pending. This extension cannot replace core C/Linux/kernel/firmware deliverables.

Start with C01 or C02 sensor/health telemetry. Choose one diagnostic question, such as identifying a simulated sensor that becomes stuck or increasingly noisy. Log timestamp, raw value, operating mode, load, fault injection ID, session ID and reset epoch. Do not infer ground truth solely from the model's output. Use deterministic injected faults first, then separately collect real device sessions with documented conditions.

Baseline: per-mode range/freshness/rate-of-change checks with thresholds chosen on training data. Evaluate false alarms and missed fault events before adding machine learning. A simple window-feature linear/logistic model can be a first learned comparator; a neural network is not an automatic improvement. Use an established runtime only if its model/operator/memory constraints justify it. R36 documents MCU inference context; no supported MCU runtime/model build is claimed here.

Split data by session/run/device *before* making overlapping windows, for example 60/20/20 percent train/validation/test sessions. These are proposed split proportions, not data that has been collected. Fit normalization only on training data. Tune features/thresholds on validation, freeze them, then evaluate held-out test sessions once. Randomly splitting adjacent overlapping windows leaks near-duplicate information and makes accuracy look better than deployment behavior.

Run Linux inference in a lower-priority userspace worker reading copied samples. It publishes a bounded-age diagnostic score through a queue; it must never block acquisition or the MCU control loop. A possible MCU deployment requires a supported toolchain/runtime, fixed memory budget and measured interference; it is a separate exercise. Preserve deterministic stale-data and lease/watchdog rules regardless of AI availability.

Fallback: use the baseline when model loading fails, score is invalid/stale, inference exceeds the declared budget or distribution checks warn. Mark the score unavailable and keep the control/health contract. Do not implement safety-critical control by waiting for an inference result.

Acceptance report template: dataset/session IDs and hashes; preprocessing fitted state; baseline and learned-model versions; confusion matrix, precision/recall, false alarms per hour, missed faults and detection delay by fault type; model bytes; peak resident/arena memory; CPU utilization; p50/p95/p99 inference latency; sample count and host/target configuration. Compare baseline and model on the same held-out sessions. All result fields remain **not measured** until executed. No accuracy/latency estimate is presented as a measurement.

Maintenance: version data/model/features together, monitor invalid/stale scores and input drift, retain rollback to baseline, and re-evaluate changed hardware/operating conditions with new session-separated tests. A simulated anomaly classifier does not establish predictive maintenance performance on an industrial machine.
