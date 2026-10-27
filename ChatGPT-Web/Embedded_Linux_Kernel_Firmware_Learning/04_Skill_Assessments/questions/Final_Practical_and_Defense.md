# Final practical and capstone defense

## FINAL P Four hour practical

**Prerequisites:** G01–G05 plus one minimum-complete capstone path. **Time:** four hours active work, excluding documented image-download time. **Tools:** editor, compiler, debugger, local official documentation and existing project source; no AI or answer keys. The practical can run entirely in host simulation. Actual hardware observations remain a separate evidence layer.

Build or adapt a bounded Linux to MCU telemetry demonstrator. Use one primary simulated serial path, a versioned message with maximum 32-byte payload, explicit CRC parameters, monotonic freshness, persistent configuration and observable health. Choose C01 gateway or C02 simulated robot. Reuse existing components only if you can explain and modify them. C02 must start disarmed and enforce a local stale-command transition; no real motors are needed.

Use this fixed synthetic event sequence, recording actual execution rather than copying expected claims:

1. At start, load a valid configuration with sample interval 100 ms and maximum queue eight. Reject invalid interval zero and queue size beyond the implemented maximum.
2. Send 20 valid numbered records; verify order and accepted/processed counts.
3. Split one frame at every possible byte boundary in separate test runs.
4. Inject one bad CRC, one excessive length, one unknown version and one truncated frame. The parser must stay bounded and expose distinct diagnostics where specified.
5. Pause the consumer long enough to fill the queue. Apply and count the documented overflow policy.
6. Disconnect the peer, then restart it with a new session ID. Recover without accepting a stale command from the previous session.
7. Interrupt a configuration write before replacement using a controllable fault hook. Restart and select a valid old or new configuration according to the documented atomicity contract.
8. For C02, stop command updates beyond the configured local deadline, confirm output permission becomes false, and require explicit re-arm after recovery. For C01, mark data stale and keep health observable.
9. Request shutdown while waiting for input and while queued work exists. Terminate within the test's two-second host deadline under the defined drain/discard policy.

Submit source revision, requirements table, architecture/interface description, test runner, exact commands, raw outputs, a validation matrix and a five-minute demo script. Label each result authored/build/host/emulator/hardware/pending. No benchmark is required unless actually measured; proposed targets are not results.

**Scoring out of 100:** correctness 25, protocol/state reasoning 15, debugging and failure diagnosis 15, bounded resources 10, concurrency/shutdown 10, tests and independent oracles 15, communication/evidence 10. Pass at 80 with no critical gate failure and at least half in every category. Critical gates: no supplied-input bounds error, indefinite required shutdown, uncontrolled resource growth, stale C02 motion permission, fabricated evidence, or bypass of configured validation. A missing board is not a failure of the host practical, but target validation remains pending.

**Remediation:** isolate the failed requirement, reproduce it with a minimal input, correct the implementation, add a regression, then retake with a changed event order and new session identifiers. Reading the reference answer alone does not satisfy remediation.

## FINAL D Sixty minute capstone defense

Prerequisites: FINAL P evidence or an honestly documented incomplete practical. Tools: your architecture diagram, requirements matrix and raw evidence; no AI. Spend 10 minutes on requirements and boundaries, 15 on one code path from input to output, 15 on injected failure and recovery, 10 on a live requirement change, and 10 on limitations and deployment gaps.

The reviewer chooses five prompts: where is ownership transferred; which queue can fill; what wakes each blocked component; what survives restart; how does a malicious or corrupt length fail; what happens on peer reset; which measurements are host-only; what would need hardware validation; which AI suggestion was rejected; what changes for a real product?

Score architecture 20, code understanding 20, failure reasoning 20, live change 20 and evidence honesty 20. Pass at 80 with no critical failure. The live change can alter maximum payload from 32 to 24, queue policy from drop-newest to reject-producer, or timeout from 250 to 100 ms; update requirements, tests and explanation consistently. Do not silently patch only one constant.
