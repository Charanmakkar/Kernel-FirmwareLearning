# B05 Version record

Frozen cross route: Bootlin AArch64 glibc stable-2024.05-1; QEMU user 8.2.2. See cross/emulator evidence for resolved versions.

| Component | Recorded value |
|---|---|
| Research and validation date | 27 October 2026 |
| Host architecture | x86_64 |
| Host kernel reported | 6.18.55 |
| Host C compiler | GCC 13.3.0 Ubuntu 13.3.0-6ubuntu2~24.04 |
| Host Python | 3.12.14 |
| Language | C11 plus documented POSIX/Linux APIs |
| Hardware tests | None executed |

Release pins support repeatable learning. They are not recommendations to deploy old security patch levels. Preserve the exact command, source version, configuration and output when adding validation evidence. No board performance numbers are estimated or implied.

## Executed cross toolchain and emulator

Bootlin glibc stable-2024.05-1 resolves to GCC 13.3.0. Its archive SHA256 matched the publisher file: `b0fad860eb94b503a56d66ca8b9ba06d2d4826943e37ebd1d7217423f6ea5bb2`. QEMU reported `8.2.2 (Debian 1:8.2.2+ds-0ubuntu1)`. The source and static/dynamic binaries used the same toolchain sysroot. Emulator evidence is in `evidence/cross_qemu.log`; the relocatable launcher was separately executed successfully. No remote GDB session or full-system boot was run.
