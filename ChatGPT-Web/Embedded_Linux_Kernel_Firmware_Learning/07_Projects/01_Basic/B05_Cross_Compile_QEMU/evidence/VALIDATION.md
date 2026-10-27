# B05 Validation evidence

Recorded 27 October 2026. No score or mastery is assigned to the learner. These records describe the supplied implementation only.

| Stage | Result |
|---|---|
| Code authored | Complete C application, Makefile and relocatable emulator launcher |
| Host build and tests | Passed native normal and boundary/invalid cases |
| Cross build | Passed Bootlin AArch64 GCC 13.3.0 dynamic and static linking |
| Emulator tests | Passed QEMU user 8.2.2 for 0, 1, 10 and 1,000,000 on both binaries; malformed inputs rejected |
| Remote debugging | Procedure supplied; GDB session not executed |
| System or hardware tests | No guest kernel boot and no physical board test |

## Evidence files

- [cross_qemu.log](cross_qemu.log)
- [host_tests.log](host_tests.log)
- [run_script.log](run_script.log)

A passed test records an observed case and does not prove every possible input or schedule. Where a step is pending, follow the runbook and add the real command, versions, exit code and logs before marking it passed.
