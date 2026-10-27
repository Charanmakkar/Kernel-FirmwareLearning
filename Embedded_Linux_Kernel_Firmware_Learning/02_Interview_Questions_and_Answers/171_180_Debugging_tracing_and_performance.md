# Debugging, tracing and performance

## Q171 — How choose GDB, strace, perf or ftrace?

**Tags:** All; intermediate; technical screen; conceptual. **Assesses:** Question-to-observation mapping and limitations.

**Spoken answer:** Choose by the boundary: program state, syscall behavior, sampled performance or kernel execution/latency events.

**Deeper explanation/example:** Start from a hypothesis and needed observation, then account for overhead and permissions. A tool's availability does not make its output causal evidence.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** Always run every tool at once.

**Follow-up:** Which tool would distinguish blocked I/O from CPU looping?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Question-to-observation mapping and limitations. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q172 — A crash stack points inside libc. How investigate?

**Tags:** All; intermediate; debugging/code review; debugging/scenario. **Assesses:** Artifact identity and cause-versus-symptom reasoning.

**Spoken answer:** Use matching symbols/core/binary, inspect callers and corrupted arguments, and consider earlier memory corruption.

**Deeper explanation/example:** The crash site may be a victim. Reproduce under supported sanitizers, minimize input and compare object lifetimes; don't blame a library from one frame.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** The top frame is always the root cause.

**Follow-up:** What if optimization inlines or removes frames?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Artifact identity and cause-versus-symptom reasoning. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q173 — Build a reproducible latency measurement harness.

**Tags:** All; intermediate; coding practical; coding. **Assesses:** Reproducible data collection and valid event definition.

**Spoken answer:** Define start/end events, monotonic timestamps, workload/load/seed, warmup, repetitions and raw output schema before measuring.

**Deeper explanation/example:** Report distribution, sample count, duration and observer overhead. Separate queue delay from service time. A script computing a percentile cannot create unrecorded target observations.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** Publish one best run as worst-case latency.

**Follow-up:** How would you detect timestamp-domain mismatch?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Reproducible data collection and valid event definition. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q174 — What do ASan, UBSan and race tools miss?

**Tags:** All; intermediate; technical screen; conceptual. **Assesses:** Qualified evidence and complementary verification.

**Spoken answer:** They detect selected runtime classes in exercised paths/configurations; they do not prove algorithms, all UB, deadlines or all concurrency schedules correct.

**Deeper explanation/example:** Separate tool support and test coverage. Memory and race sanitizers may require separate builds. Keep a reasoning argument and meaningful tests alongside instrumentation.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** No sanitizer report means the program is correct.

**Follow-up:** Can a clean run establish thread safety?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Qualified evidence and complementary verification. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q175 — CPU utilization is high but throughput low. What investigate?

**Tags:** All; intermediate; debugging/code review; debugging/scenario. **Assesses:** Hypothesis, discriminating experiment and before/after evidence.

**Spoken answer:** Separate useful work, spinning, retries, lock contention, scheduling and I/O with profiles plus state/queue observations.

**Deeper explanation/example:** A hot retry loop may come from a zero timeout or persistent EAGAIN. A hotspot is an observation; change one cause and repeat comparable tests.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** Optimize the longest function without checking workload.

**Follow-up:** How do you test the proposed bottleneck causally?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Hypothesis, discriminating experiment and before/after evidence. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q176 — An apparent memory leak grows only under backlog. What test?

**Tags:** All; intermediate; debugging/code review; debugging/scenario. **Assesses:** Object-lifetime accounting and steady-state evidence.

**Spoken answer:** Observe queue depth, retained ownership, allocator behavior and memory after draining under a controlled workload.

**Deeper explanation/example:** Bounded caching/backpressure differs from a leak. Track objects through allocation/queue/consume/free and test repeated load/drain cycles. RSS alone is insufficient.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** Any nondecreasing RSS proves leaked allocations.

**Follow-up:** How would a fixed-capacity queue change diagnosis?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Object-lifetime accounting and steady-state evidence. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q177 — How interpret a kernel oops responsibly?

**Tags:** All; intermediate; technical screen; conceptual. **Assesses:** Complete evidence and uncertainty-aware diagnosis.

**Spoken answer:** Preserve full logs, kernel/build/config/module identity and trace context; symbolize against the exact artifacts and form hypotheses.

**Deeper explanation/example:** An oops can follow prior corruption. Tainted/out-of-tree modules and missing symbols limit conclusions. A panic is not merely another application exception.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** The last printk identifies the faulty source line.

**Follow-up:** Which additional fault/address data matters on your architecture?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Complete evidence and uncertainty-aware diagnosis. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q178 — A latency improvement appears only in one run. Can you claim it?

**Tags:** All; intermediate; debugging/code review; debugging/scenario. **Assesses:** Statistically cautious, reproducible comparative reasoning.

**Spoken answer:** No; repeat controlled trials, report variability and check workload/load/config/measurement differences.

**Deeper explanation/example:** Compare distributions and costs, not only averages or a single tail percentile. If the effect is below variation, say evidence is inconclusive; preserve raw samples.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** Any lower p99 proves the patch is better.

**Follow-up:** What regression workload should you add?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Statistically cautious, reproducible comparative reasoning. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q179 — How do KASAN and KCSAN relate to userspace sanitizers?

**Tags:** All; intermediate; technical screen; conceptual. **Assesses:** Layer/config support and separate diagnostic/performance claims.

**Spoken answer:** They target supported kernel memory/race diagnostics and require appropriate kernel/toolchain/configuration support.

**Deeper explanation/example:** Use a disposable guest and record config/overhead. They are not enabled by adding userspace -fsanitize flags to a driver build. Confirm architecture support before prescribing a run.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** Every kernel/board can run all sanitizers simultaneously.

**Follow-up:** How might instrumentation affect timing experiments?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Layer/config support and separate diagnostic/performance claims. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.

## Q180 — Intermittent failure disappears after adding logs. What do you do?

**Tags:** All; intermediate; debugging/code review; debugging/scenario. **Assesses:** Observer-effect awareness and an independent regression argument.

**Spoken answer:** Assume observation changed timing/state; retain minimal logging, use targeted traces and construct a deterministic fault/interleaving fixture.

**Deeper explanation/example:** Capture sequence IDs/timestamps or an event buffer where appropriate; distinguish log loss from actual event loss. Do not treat disappearance as a fix.

**Assumptions/version:** Tool/target/configuration support varies; no performance measurements are supplied.

**Common incorrect answer:** Keep massive logging and mark the race resolved.

**Follow-up:** How do you show a synchronization fix is correct?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Observer-effect awareness and an independent regression argument. [Learning: M14](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m14). References: R07; R08; R19; R33.
