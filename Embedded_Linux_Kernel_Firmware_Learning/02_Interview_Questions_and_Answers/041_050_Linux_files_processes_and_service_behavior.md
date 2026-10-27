# Linux files, processes and service behavior

## Q041 — What distinguishes process and thread?

**Tags:** EL/KD; foundation; technical screen; conceptual. **Assesses:** Discuss shared resources, failure isolation and communication cost.

**Spoken answer:** A process provides an address-space/resource context; threads within it share memory while retaining their own execution state and stack.

**Deeper explanation/example:** File-descriptor tables and signal details have specific sharing rules. Shared memory makes thread coordination necessary; separate processes still communicate through explicit IPC.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Threads have separate heaps by default.

**Follow-up:** When choose process isolation over threads?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Discuss shared resources, failure isolation and communication cost. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q042 — A PID disappears while your inspector reads /proc. Is this a bug?

**Tags:** EL/KD; foundation; debugging/code review; debugging/scenario. **Assesses:** Explicit race policy and deterministic fixture/process lifecycle test.

**Spoken answer:** It is an expected race in a dynamic system; handle missing entries and report a partial observation.

**Deeper explanation/example:** PID reuse can also make two reads refer to different process lifetimes. Record start identity where needed; do not claim a coherent global snapshot from directory enumeration.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Retry forever until every discovered PID is readable.

**Follow-up:** How would you test without depending on timing luck?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explicit race policy and deterministic fixture/process lifecycle test. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q043 — What do file permissions and umask control?

**Tags:** EL/KD; foundation; technical screen; conceptual. **Assesses:** Least-privilege explanation and actual access-path checks.

**Spoken answer:** Permission bits govern access subject to identity and other policy; umask removes permissions from newly created objects.

**Deeper explanation/example:** Directory read/search/write differ from file permissions. ACLs, capabilities, mount and security-module policies may further affect access. Never infer a permission problem from one chmod guess.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** chmod 777 is the right default fix.

**Follow-up:** Why does execute/search permission matter on a directory?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Least-privilege explanation and actual access-path checks. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q044 — Explain /proc, /sys and /dev.

**Tags:** EL/KD; foundation; technical screen; conceptual. **Assesses:** Connect discovery, kernel interface and userspace policy.

**Spoken answer:** proc exposes process/kernel observations, sysfs exposes kernel object attributes, and /dev contains device nodes used through subsystem interfaces.

**Deeper explanation/example:** A device node is an entry point, not stored hardware data. udev or other device management can create policy/names from kernel events; minimal images may use devtmpfs/mdev instead.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Every file under /dev is a regular disk file.

**Follow-up:** What creates a device node on a minimal image?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Connect discovery, kernel interface and userspace policy. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q045 — What happens during fork and exec?

**Tags:** EL/KD; foundation; technical screen; conceptual. **Assesses:** Resource inheritance and exec-failure cleanup.

**Spoken answer:** fork creates a child process context; exec replaces a process image while retaining selected resources such as descriptors not close-on-exec.

**Deeper explanation/example:** Close inherited pipe ends and set close-on-exec deliberately. Error reporting around exec should not assume the parent's multithreaded library state is safe for arbitrary child calls.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** exec creates a new PID automatically.

**Follow-up:** Why use posix_spawn in some designs?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Resource inheritance and exec-failure cleanup. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q046 — Your child process becomes a zombie. What happened?

**Tags:** EL/KD; foundation; debugging/code review; debugging/scenario. **Assesses:** Correct reaping mechanism and multi-child race handling.

**Spoken answer:** The child exited but its status has not been collected by a parent or appropriate reaper.

**Deeper explanation/example:** Use wait/waitpid with a robust signal/event design. A zombie consumes an entry/status, not an actively executing CPU thread. Avoid confusing it with a blocked live process.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Kill the zombie harder with SIGKILL.

**Follow-up:** How do you handle several children exiting together?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct reaping mechanism and multi-child race handling. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q047 — How should a service shut down on SIGTERM?

**Tags:** EL/KD; foundation; technical screen; conceptual. **Assesses:** Safe notification and orderly lifetime sequencing.

**Spoken answer:** Route notification into normal control flow, stop accepting work, wake waiters, release owned resources and exit within policy.

**Deeper explanation/example:** Keep signal handlers within async-signal-safe operations or use an appropriate signal-wait/event mechanism. Calling arbitrary logging/allocation from a handler can deadlock.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Perform all cleanup with printf and mutexes inside the handler.

**Follow-up:** How does a self-pipe help?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Safe notification and orderly lifetime sequencing. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q048 — A service runs manually but fails at boot. What compare?

**Tags:** EL/KD; foundation; debugging/code review; debugging/scenario. **Assesses:** Reproduce the actual service execution context.

**Spoken answer:** Compare environment, working directory, credentials, dependencies, device readiness and actual logs/exit code.

**Deeper explanation/example:** Use explicit paths and service dependencies. Boot can expose races with device creation or mounted persistence. Adding an arbitrary sleep hides rather than proves ordering.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Put sleep 30 before starting it.

**Follow-up:** What evidence identifies a missing runtime dependency?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Reproduce the actual service execution context. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q049 — What is virtual memory and why can RSS differ from address-space size?

**Tags:** EL/KD; foundation; technical screen; conceptual. **Assesses:** Separate mapping, residency, sharing and growth evidence.

**Spoken answer:** Virtual addresses map process regions; resident set measures currently resident pages under the reported metric.

**Deeper explanation/example:** Mappings can be uncommitted, file-backed, shared or swapped. A single number cannot establish a leak; compare workload and page accounting over time.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Virtual size equals physical RAM exclusively owned by the process.

**Follow-up:** What would you observe during copy-on-write?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Separate mapping, residency, sharing and growth evidence. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.

## Q050 — A deleted log still occupies disk space. Why?

**Tags:** EL/KD; foundation; debugging/code review; debugging/scenario. **Assesses:** Name versus open-object lifetime and safe operational remedy.

**Spoken answer:** An open descriptor can keep the unlinked file's data alive until the last reference closes.

**Deeper explanation/example:** Inspect the owning process/descriptors, then use a controlled reopen/rotation strategy. Deleting names alone does not force a service to release open files.

**Assumptions/version:** Linux userspace; proc/sys output and service policies vary by target.

**Common incorrect answer:** Filesystem corruption is the only explanation.

**Follow-up:** How should log rotation coordinate with a long-running writer?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Name versus open-object lifetime and safe operational remedy. [Learning: M03](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m03). References: R20; R21; R22.
