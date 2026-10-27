# B05 Cross compilation and QEMU application debugging

Compile the same C program for the host and for AArch64, inspect both ELF files, and run the AArch64 version through QEMU's Linux user-mode emulator. Plan 10–14 hours after M04, M05, and M08. The complete program computes the sum of integers from 1 through a bounded N and identifies its compiled architecture. This deliberately small workload keeps the focus on ABI, toolchains, sysroots, dynamic loaders, and remote debugging.

## Scope and measurable outcomes

Show that the native binary identifies x86_64 on the recorded host, the cross binary identifies aarch64, and both return the same result for boundary values. Explain the ELF machine, interpreter path, pointer size, and the difference between static and dynamic linking. A successful user-mode run does not validate kernel boot, drivers, device tree, interrupts, or board peripherals. I01 introduces a full-system guest.

## Environment and pinned route

The baseline host is x86_64 Ubuntu 24.04-compatible Linux. The verified downloadable toolchain route uses Bootlin `aarch64--glibc--stable-2024.05-1` and QEMU user 8.2.2. The exact compiler, sysroot, and emulator versions appear in `VERSIONS.md` and the recorded log. These are frozen educational inputs, not assertions that older packages contain current security fixes.

For a normal Ubuntu workstation, `gcc-aarch64-linux-gnu`, `qemu-user`, and `gdb-multiarch` provide a convenient alternative, but their installed package versions must be recorded. Do not mix a loader from one sysroot with libraries from another without checking ABI compatibility.

## Build and run

From this project directory, for distribution-installed tools:

```sh
make test
make cross
sh scripts/run_qemu.sh
```

For a relocated Bootlin toolchain, use its actual extracted location:

```sh
export CROSS_COMPILE=/absolute/toolchain/bin/aarch64-buildroot-linux-gnu-
make cross
qemu-aarch64 -L "$(${CROSS_COMPILE}gcc -print-sysroot)" ./build/target_sum_aarch64 1000000
qemu-aarch64 ./build/target_sum_aarch64_static 1000000
${CROSS_COMPILE}readelf -h build/target_sum_aarch64
${CROSS_COMPILE}readelf -l build/target_sum_aarch64
```

The expected sum for N equal to 1,000,000 is 500000500000. It is computed with a 64-bit accumulator. N is capped before the loop so integer limits and unreasonable run times are explicit. The program rejects negative, nonnumeric, overflowing, and above-limit inputs.

## Remote debugging lab

In terminal one, run `qemu-aarch64 -g 1234 -L SYSROOT ./build/target_sum_aarch64 10`, substituting the actual sysroot path. In terminal two:

```sh
gdb-multiarch ./build/target_sum_aarch64
```

Then enter `set sysroot SYSROOT`, `target remote :1234`, `break sum_to`, `continue`, `info registers`, and `step`. Debugger path expressions are commands, not literal shell variable expansions inside GDB. Replace SYSROOT with the real path. The remote-debug session is an instructed lab unless its own log is supplied; emulator functional tests alone do not establish that this debugger step ran.

QEMU user mode translates guest system calls to the host kernel. A foreign userspace program is running, but there is no separate AArch64 kernel. [QEMU user-mode documentation](https://www.qemu.org/docs/master/user/main.html). To learn boot flow and real kernel-driver integration, proceed to I01 and the kernel projects.

## Troubleshooting and acceptance

An `Exec format error` from executing the cross binary directly means no compatible loader/emulation path was used. A missing `/lib/ld-linux-aarch64.so.1` usually indicates a wrong or absent sysroot. `file` and `readelf` should resolve architecture and interpreter uncertainty before code changes. Static linking reduces runtime-loader dependencies but does not remove kernel ABI assumptions or make the binary universally portable.

Run the native tests, then compare native and emulated outputs for 0, 1, 10, and 1,000,000. Record command, return code, architecture, and numeric result. Reject the invalid inputs under emulation too. `make clean` removes only generated binaries.

## Interview demonstration and extension

Show an ELF header, run the AArch64 binary, and explain the sysroot. Defend why a cross compiler's machine tuple does not specify the entire board support package. Add a small file-I/O workload and discuss which behavior is exercised by syscall translation. Keep any measured emulator throughput separate from target hardware performance.

## Primary references

- [Bootlin toolchain release archive](https://toolchains.bootlin.com/downloads/releases/toolchains/aarch64/tarballs/)
- [QEMU Linux user mode](https://www.qemu.org/docs/master/user/main.html)
- [QEMU GDB usage](https://www.qemu.org/docs/master/system/gdb.html)

Access date: 27 October 2026.
