# Environment and target policy

## Host lanes

**Portable lane, available now:** Windows x86-64, Python 3.13.2 and LLVM-MinGW Clang 22.1.0-rc3. B01 uses ISO C11, fixed-width unsigned bytes, and no OS APIs. The Python runner invokes the compiler directly, so Make is optional. Windows uses LLP64; a Linux x86-64 host commonly uses LP64. Never assume long or pointers have equal widths.

**Linux lane, required for B02 onward:** choose a disposable Ubuntu 24.04 LTS x86-64 VM, native installation, or working WSL2 Ubuntu. Use a Linux filesystem such as ~/embedded-labs for builds; a Windows-mounted directory can introduce permission, case, and filesystem differences. A VM snapshot is recommended before module experiments. WSL alone does not provide the target QEMU kernel or physical board environment. Use QEMU guests for driver tests; never load these experimental drivers into a daily-use host.

Recommended planning capacity (estimates): 16 GB host RAM and 100 GB free for the early Linux/Buildroot work; for Yocto prefer 32 GB RAM, 8 CPU threads, and 250–350 GB free SSD space. These are program planning allowances, not vendor minimums. Recheck the selected Yocto release's official requirements [R04] before building. Reduce parallelism if the out-of-memory killer terminates compilers.

On the Linux lane, from a normal user shell:

```sh
sudo apt update
sudo apt install build-essential clang gdb git cmake ninja-build python3 python3-venv \
  pkg-config strace valgrind socat qemu-system-arm qemu-user gcc-aarch64-linux-gnu \
  binutils-aarch64-linux-gnu bc bison flex libssl-dev libelf-dev \
  libncurses-dev cpio rsync unzip file wget xz-utils
mkdir -p ~/embedded-labs
cd ~/embedded-labs
uname -a
cc --version
git --version
qemu-system-aarch64 --version
```

This installs common tools, not a complete Yocto dependency set. Follow R04 for its additional host packages. The commands are authored instructions and have not been executed on a Linux host in this release. Save exact apt package versions with `dpkg-query -W > host-packages.txt` once installed. No root privileges are needed to compile B01. Do not run entire builds with sudo.

## Selected future project targets (planned, not validated)

| Lane | Selection | Boundary |
|---|---|---|
| Buildroot/QEMU | Buildroot tag 2026.08.1; qemu_aarch64_virt_defconfig; AArch64 virt with Cortex-A53; kernel 6.18.7 from that defconfig | Upstream file inspected [R02]. Source/build/toolchain hashes still pending. This is a teaching baseline, not a claim of current security patch status. |
| Kernel labs | Same Linux 6.18.7 configured build and guest; match module build tree, configuration, and compiler | Use 6.18 documentation/source for implementation, not arbitrary tutorials. R05/R06 are explicitly older conceptual references, not API authority for future code. |
| Yocto | Poky tag yocto-5.0.14 (Scarthgap), MACHINE=qemuarm64 | Separate image lineage. Its kernel and toolchain must be recorded from BitBake; do not inject the Buildroot kernel or modules. Tag/recipe build not yet validated. |
| RTOS simulation | Zephyr v4.2.0, native_sim/native/64 | Simulation choice checked against versioned docs [R10]. SDK/tool manifest must be locked when I05 is authored. |
| MCU hardware | ST NUCLEO-F446RE, MB1136; STM32F446RE Cortex-M4; Zephyr v4.2.0 pending board-tag verification | Board docs [R11/R12] checked; exact revision, jumpers and firmware build not verified. Current board docs are not silently treated as a v4.2.0 API guarantee. |
| Linux GPIO/IIO hardware | BeagleBone Black Rev C, AM335x Cortex-A8; ADXL345 breakout at 3.3 V | This is ARMv7, not AArch64 virt. Board-specific kernel/configuration/image must be pinned separately before I03/A01 source is written. No wiring procedure is authorized by this plan alone. |
| Update capstone | RAUC 1.13 + isolated QEMU disk + explicit boot attempt/health state | Full A/B boot integration remains to be implemented and tested; a signed file copy alone is not rollback. |

The Buildroot tag's checked defconfig selects Linux 6.18.7 [R02]. Reproduction will also require a manifest of actual downloaded inputs, generated `.config`, compiler, and image hashes. For production, review advisories and move to supported patched releases with regression tests; this package is not a security-maintenance service.

## Why start without hardware

B01–B05 and I01/I02/I04 can establish memory safety, protocol behavior, IPC, toolchain and image skills with host tests or QEMU. I03/A01 need physical validation of pinmux, IRQ behavior and the actual sensor bus. I05 can establish RTOS state and protocol logic in native_sim, but MCU timing, stack limits, startup, fault registers and watchdog wiring need the Nucleo. C02 begins with a simulated plant, with no motor connected.

Do not buy boards before completing B01 and choosing a role. Hardware additions by outcome: Nucleo + existing USB cable for MCU debugging and serial; Linux board + microSD + documented power supply for boot/GPIO; ADXL345 breakout for IIO integration; logic analyzer for timing/bus verification. Prices and availability are not assumed. Verify breakout schematic, voltage, board revision and shared-pin conflicts before wiring. Use documented 3.3 V logic, not RS-232 voltage. Use the Nucleo ST-LINK virtual COM port as the first serial path; check board solder bridges and UART routing before adding external wires.

## Record versions before interpreting a failure

```sh
uname -r
cc -dumpmachine
cc --version
file ./application
readelf -h ./application
git rev-parse HEAD
sha256sum ./application
```

Wrong executable architecture gives an exec-format error; a missing ELF interpreter can look like a missing file even when the executable exists. Check `readelf -l`. A sysroot supplies target headers/libraries; it is not a CPU emulator. For out-of-tree modules use the target kernel's configured build output, not `/lib/modules/$(uname -r)/build` on an unrelated host.

## Troubleshooting the observed host limitation

WSL failed with error 0xd0000022 / Wsl/Service/CreateInstance/STATUS_ACCESS_DENIED. This package records that failure as evidence; it does not diagnose a specific Windows policy or perform invasive repair. Use the portable lane now, then a working Linux environment for B02. Do not reset or unregister an existing distribution to follow a tutorial. No emulator, guest, Linux syscall, or hardware result is reported as passed here.
