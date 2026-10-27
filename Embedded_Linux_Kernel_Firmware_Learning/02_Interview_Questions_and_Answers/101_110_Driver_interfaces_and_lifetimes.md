# Driver interfaces and lifetimes

## Q101 — Why use copy_to_user/copy_from_user?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Correct access/context/return handling.

**Spoken answer:** User pointers need controlled access with fault/error handling; directly dereferencing them violates kernel interface rules.

**Deeper explanation/example:** Check the exact helper return contract: common copy helpers return bytes not copied, not a conventional negative errno. User access can fault/sleep in applicable contexts.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** Treat copy_to_user returning nonzero as a positive byte count successfully copied.

**Follow-up:** How do partial copies affect read semantics?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Correct access/context/return handling. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q102 — A read succeeds but poll never wakes. What inspect?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Consistent predicate and lost-wakeup prevention.

**Spoken answer:** Compare the readiness predicate, poll wait registration, state update visibility and wake path.

**Deeper explanation/example:** read and poll must describe the same protected queue state. Test empty-to-nonempty with a waiter already registered and with an event racing registration.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** poll can just return readable unconditionally.

**Follow-up:** How do hangup/error states appear?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Consistent predicate and lost-wakeup prevention. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q103 — What should a character read return when no data exists?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Object-specific EOF and blocking semantics.

**Spoken answer:** It depends on blocking policy: wait interruptibly, return EAGAIN for nonblocking, or EOF only for a genuine end condition.

**Deeper explanation/example:** Zero is not a generic “try later” marker for a live stream. Define zero-length request, signal interruption and partial-progress behavior in the ABI.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** Return zero whenever queue is empty.

**Follow-up:** How does this affect a userspace cat loop?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Object-specific EOF and blocking semantics. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q104 — A module unloads while an open descriptor still calls it. What review?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Distinguish code reference, object reference and active operation lifetime.

**Spoken answer:** Review file-operation/module ownership, open references and separate device-object lifetime during unbind.

**Deeper explanation/example:** Module code lifetime and device state lifetime are related but different. A driver can remain loaded while a detached device must reject operations safely.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** A global boolean removed prevents all lifetime bugs.

**Follow-up:** How would you keep per-open state alive?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Distinguish code reference, object reference and active operation lifetime. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q105 — How do you design a stable ioctl ABI?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Layout/compat/error policy and a justified need for ioctl.

**Spoken answer:** Use a justified operation, fixed-width fields, explicit layout/version/reserved handling and compatibility rules; validate sizes and values.

**Deeper explanation/example:** Avoid native pointers/long in shared structures unless a documented compat strategy exists. Prefer established subsystem interfaces when they fit. Unknown commands must fail predictably.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** Expose the driver's internal struct directly.

**Follow-up:** How would 32-bit userspace on 64-bit kernel work?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Layout/compat/error policy and a justified need for ioctl. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q106 — Design a poll-capable bounded kernel queue.

**Tags:** KD; intermediate; coding practical; coding. **Assesses:** Readiness, copy context and concurrent-consumer contract.

**Spoken answer:** Protect queue state, register poll waiters with the supported API, report readiness from the same predicate as read/write and wake after changes.

**Deeper explanation/example:** Use sleepable user-copy paths without raw spinlock held; stage data or choose an appropriate lock design. Multi-client consumption needs explicit ownership and partial-fault semantics.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** Hold a spinlock while copying arbitrary userspace buffers.

**Follow-up:** How do you preserve data on a failed copy?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Readiness, copy context and concurrent-consumer contract. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q107 — What do managed resources simplify and leave unsolved?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Logical stop sequence beyond automatic release.

**Spoken answer:** They release registered resources at device lifecycle boundaries, reducing manual error unwinding.

**Deeper explanation/example:** The driver must still stop IRQ/work/timer activity and manage references outside that lifetime. Resource registration order affects release dependencies.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** devm guarantees no use-after-free on unbind.

**Follow-up:** When would devm be inappropriate for a longer-lived object?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Logical stop sequence beyond automatic release. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q108 — A driver reports success after hardware initialization fails. What consequence?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Required/optional/deferred failure semantics.

**Spoken answer:** Userspace sees a bound but unusable device and later faults become misleading; propagate the real failure and unwind state.

**Deeper explanation/example:** Differentiate optional feature failures from required initialization. Log context without masking an error code or spamming retries. Test failure at each setup boundary.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** Probe should always return zero so the system boots.

**Follow-up:** How do you handle a temporarily unavailable provider?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Required/optional/deferred failure semantics. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q109 — Why is a learning char device not always a production sensor interface?

**Tags:** KD; intermediate; technical screen; conceptual. **Assesses:** Subsystem-fit tradeoff and educational scope.

**Spoken answer:** Subsystem APIs provide established units, discovery, buffering and userspace conventions that a private interface would duplicate.

**Deeper explanation/example:** Use IIO/hwmon/input/tty/etc. based on device semantics. The char queue teaches copying/waits/lifetimes; it does not justify a custom ABI for every peripheral.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** A custom ioctl is always simpler and therefore better.

**Follow-up:** What behavior would IIO supply for an accelerometer?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Subsystem-fit tradeoff and educational scope. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.

## Q110 — A multi-client driver duplicates or loses records. Where look?

**Tags:** KD; intermediate; debugging/code review; debugging/scenario. **Assesses:** Explicit consumer semantics and race-free commit point.

**Spoken answer:** Clarify record ownership and lock coverage across readiness check, user copy and consume; two readers may observe the same head.

**Deeper explanation/example:** Define whether reads consume globally or each open has a cursor. Handle partial faults without silently discarding unreported data. A lock around count alone may be insufficient.

**Assumptions/version:** Linux 6.18.7 intended build; no driver code executed in this release.

**Common incorrect answer:** Increase buffer capacity until the race disappears.

**Follow-up:** How would you test two readers deterministically?

**Scoring:** use the bank's 0–4 rubric; full credit specifically requires: Explicit consumer semantics and race-free commit point. [Learning: M08](../03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md#m08). References: R29; R30.
