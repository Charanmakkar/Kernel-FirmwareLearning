# A02 Linux latency and performance investigation

## Purpose and learning outcome

Separate accumulated periodic drift from wakeup lateness, collect raw measurements, compare a scheduling change and report uncertainty honestly. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 18–26 hours; allow remediation time when a prerequisite fails. Relevant learning modules: M05 M07 M15. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Understand scheduling and monotonic clocks; finish B04 and basic tracing lessons.

## Minimum scope and version boundary

Host Linux x86-64, Python 3.12.14; recorded kernel 6.18.55. No board required for the delivered host minimum.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

A single Python process runs relative-sleep and absolute-deadline policies using monotonic nanoseconds. An optional separate busy process is pinned to the same allowed CPU to add contention. Each observation records planned and actual times. Percentiles summarize the sample; raw CSVs remain available. An optional trace-cmd wrapper records scheduler wakeup/switch events in a disposable VM.

## Build run debug and cleanup

1. Use Python 3.12 on Linux. Run `python3 -m unittest discover -s tests -v`.
2. Record kernel, CPU model/governor, power state, affinity and background workload. The script records kernel/Python/affinity, but these are not the entire environment.
3. Run `python3 src/latency.py --out evidence/idle --samples 300`.
4. Run `python3 src/latency.py --out evidence/loaded --samples 300 --load`.
5. Read each summary.json alongside its raw CSV. The relative policy accumulates oversleep; the absolute policy aims at a fixed timeline and can catch up. Compare them as different scheduling policies.
6. In a disposable VM with tracing permission, run `sudo sh scripts/trace.sh`, inspect with `trace-cmd report` or KernelShark, and correlate long late samples with runnable versus executing intervals.
7. For a tighter C experiment replace Python sleeps with `clock_nanosleep(CLOCK_MONOTONIC,TIMER_ABSTIME,...)` and record that as a new experiment; do not mix those values with the supplied Python results.

## Acceptance criteria and evidence

Every run saves exactly the requested number of samples, nondecreasing deadlines and environment metadata. Explain max, p99 and cumulative drift correctly. Identify at least one plausible scheduling cause using trace evidence before making a tuning claim. Show that a design improvement preserves correctness and report any throughput/power cost. No latency threshold is universal across hosts.

Two host tests validate sample accounting and evidence recording. Actual idle and loaded experiments each collected 300 samples per policy. No ftrace/perf data was collected here; the tracing command is supplied for the target environment.

**Observed validation:** Host tests and measurements executed. Actual records are in evidence/idle and evidence/loaded. The delivered results are observations from this shared host, not a PREEMPT_RT benchmark or deadline guarantee.

## Troubleshooting and limitations

Python overhead, host contention, virtualized scheduling, clock behavior, sample size and run order affect results. The loaded case can sometimes have a lower median due to noise/power state; do not select only favorable statistics. Comparing relative cumulative drift with absolute deadline error does not isolate scheduler latency. Use repeated interleaved runs and a C timing harness for a stronger study.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Explain a run where median improves but maximum worsens; design an experiment that distinguishes periodic drift, CPU starvation and lock contention. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show one raw late sample, compute its lateness manually, explain a scheduling trace, then justify the absolute-deadline change and its catch-up behavior.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.
