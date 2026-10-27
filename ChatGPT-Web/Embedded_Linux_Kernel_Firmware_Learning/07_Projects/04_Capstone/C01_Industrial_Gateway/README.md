# C01 Industrial monitoring and edge gateway

## Purpose and learning outcome

Integrate a bounded telemetry path, persisted validated configuration, freshness/alarm diagnostics, an unprivileged service and update health acceptance with executable fault tests. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 35–50 hours reusing earlier projects; allow remediation time when a prerequisite fails. Relevant learning modules: M06 M07 M13 M14 M16 M17. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Complete B03/I05, one image-builder project, and A03. Know the limits of CRC, sequence checks and durable configuration.

## Minimum scope and version boundary

Host Linux x86-64, Python 3.12.14; recorded kernel 6.18.55. No board required for the delivered host minimum.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

One byte-stream transport carries the I05 TL protocol. The parser rejects corruption and stale/replayed sequence numbers, allows sequence wrap within the half-range window, and retains at most an incomplete frame after processing. Valid data updates a latest-value snapshot and freshness time. The Linux process atomically persists configuration and health; EOF marks transport closed. A service definition connects a configured 115200 serial device. A separate acceptance script runs the capstone tests after an A03 trial boot and marks good only when they pass.

## Build run debug and cleanup

1. Use Linux and Python 3.12; no external Python packages are required. Run `python3 -m unittest discover -s tests -v`.
2. Run `python3 src/simulated_mcu.py | python3 src/gateway.py --state run`. Inspect run/config.json and run/health.json. On EOF, healthy becomes false because the transport has closed; this is expected.
3. Inject failures using `--corrupt` and `--replay` on the simulated MCU. Compare accepted/rejected counts and verify valid traffic after the bad packet recovers.
4. While running, inspect freshness and alarm behavior with the unit tests or stop the source temporarily. Persistent config defaults to limit_mC 30000 and stale_seconds 0.3; edit while stopped and restart. Invalid values fail startup.
5. Build the I05 firmware and use its frame output as the source. For an actual board, adapt the documented MCU transport, configure the serial device and permissions, and install config/gateway.service only after creating the dedicated gateway user and deploying source under /opt/learning-gateway.
6. In the I04 Yocto 5.0.9 build shell, add this complete layer using `bitbake-layers add-layer /absolute/C01_Industrial_Gateway/config/meta-gateway`, then `bitbake gateway-image` and `runqemu qemux86-64 gateway-image nographic`. The supplied recipe installs the source, creates the gateway user and enables a synthetic-source service. Verify `/var/lib/learning-gateway/health.json` and `journalctl -u gateway-sim`. For A/B deployment put that state directory on a persistent data partition; the minimum QEMU image retains state in its writable ext4 root. Image construction and boot were not executed here.
7. With an A03 initialized device and signed bundle, run `python3 scripts/accept_update.py DEVICE_ROOT BUNDLE_DIRECTORY`. The process trial boots, runs gateway acceptance, then confirms only on success. Clean up dedicated run directories after saving evidence.

## Acceptance criteria and evidence

Requirements C01-R1–R7: accept correct fragmented frames; reject corrupted frames; reject duplicate data without refreshing freshness; mark stale after configured timeout; keep the last accepted value and observable counters; survive restart with the same valid configuration; do not confirm an update when acceptance fails. No network listener or cloud dependency is needed for the minimum.

Eight tests cover counter units, fragmentation, freshness, replay, alarm, sequence wrap, invalid configuration and a real producer/consumer subprocess pipeline with corrupted and repeated frames. Add storage-full and interrupted-configuration fault injection before claiming field reliability. Gateway acceptance is source-level health, not a cryptographic binding between arbitrary installed image bytes and this host process.

**Observed validation:** Complete host gateway and simulated MCU pipeline authored; eight tests passed. Service units, a complete Yocto layer/image recipe and update acceptance integration authored. Board serial operation, final Linux image build, real update boot and industrial environmental testing remain pending.

## Troubleshooting and limitations

CRC detects accidental corruption and is not authentication. Sequence checks assume a continuous session; an MCU reboot needs an explicit session/handshake design before reconnect can safely reset the sequence baseline. The host snapshot store does not implement a long-term historian. The shell service unit is an integration example for a known ttyACM0 path; production should use stable device identity, controlled permissions and an appropriate persistent data partition.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Design and implement a boot-session identifier without allowing a replayed old hello packet to reset the anti-replay state. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show the system boundary, valid data flow, corruption recovery, stale-state transition, persisted configuration and update health gate. State clearly which code and tests you authored.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.

**Additional integration executed:** The actual FreeRTOS V11.1.0 POSIX firmware was connected through a FIFO to the gateway subprocess. All 20 records were accepted, zero were rejected, and the transport closed cleanly. See evidence/rtos-integration.log and scripts/test_rtos_link.py.

**Counter units:** accepted counts complete accepted frames; rejected counts a CRC-invalid packet candidate or a complete out-of-range/replayed frame; discarded_bytes counts bytes skipped during resynchronization. Noise bytes are not misreported as rejected frames.
