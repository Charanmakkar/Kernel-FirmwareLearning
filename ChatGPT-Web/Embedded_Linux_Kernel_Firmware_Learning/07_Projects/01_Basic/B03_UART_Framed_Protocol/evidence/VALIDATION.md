# B03 Validation evidence

Recorded 27 October 2026. No score or mastery is assigned to the learner. These records describe the supplied implementation only.

| Stage | Result |
|---|---|
| Code authored | Complete codec, POSIX transaction tool and independent Python peer |
| Host build | Passed GCC 13.3.0 with warnings as errors |
| Host tests | PTY normal, fragmentation, corrupt/stale/noise, timeout, boundary and attribute restoration on success/error/SIGINT/SIGTERM/broken stdout passed |
| Emulator tests | PTY is a host kernel interface; not a hardware UART emulator |
| Hardware tests | Not executed; voltage, pinmux, baud clock and physical faults pending |

## Evidence files

- [host_tests.log](host_tests.log)

A passed test records an observed case and does not prove every possible input or schedule. Where a step is pending, follow the runbook and add the real command, versions, exit code and logs before marking it passed.
