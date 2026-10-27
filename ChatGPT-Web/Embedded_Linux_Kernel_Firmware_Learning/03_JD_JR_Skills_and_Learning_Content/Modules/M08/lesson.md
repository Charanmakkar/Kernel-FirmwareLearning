# M08 Cross compilation boot and device tree

## Objectives and prerequisites

Prerequisites: M04 M05.

Build for a foreign target, identify boot-stage evidence and describe hardware with validated bindings.

## Lesson


A cross compiler runs on the host and generates code for a target. Its target triple, headers, libraries and linker need to agree. A sysroot is a target filesystem view used during development; it is not automatically a bootable image. B05 deliberately starts with Linux user-mode QEMU to isolate application and loader questions before I01 introduces a whole guest machine. [CMAKE] [QEMU-USER]

Boot is platform-specific. A common application-processor chain starts in immutable boot ROM, loads early firmware that initializes memory, then a bootloader, kernel and an initial userspace program. Some systems use UEFI; others use U-Boot and vendor stages. Do not draw one universal sequence and call it every ARM board. Observe serial output at each transition and identify the first missing milestone. Kernel logs cannot diagnose a failure before the kernel began executing.

An initramfs is unpacked into an early root filesystem in memory. It can supply /init and discover or mount the final root. A persistent root filesystem holds userspace and configuration according to the image design. A kernel panic about no working init differs from inability to mount root: the former can involve a missing executable, interpreter or libraries, while the latter can involve storage drivers, filesystem support or a wrong root argument.

Device tree describes hardware through nodes and properties governed by bindings. A compatible string allows matching a device description to driver support. Addresses, interrupt specifiers, clocks, regulators and pins have parent-specific meanings. A device-tree blob is data, not executable driver code. A correct-looking node cannot compensate for a missing driver or disabled clock. Use the kernel's schema validation and the selected board's actual source. [DT] [DTSCHEMA]

An overlay changes a base tree and depends on symbols, target labels and firmware support. Its use on one board release does not prove that the same overlay works elsewhere. GPIO descriptors express logical state and active polarity; pin control configures electrical/multiplexing characteristics separately. Record the exact base device tree, board revision and overlay with the driver evidence.

A board support package combines bootloader, kernel, device descriptions, firmware, toolchain/image integration and patches for a supported platform. Count the maintenance burden of downstream patches. A board booting once establishes a milestone, but repeated cold boot, shutdown, peripheral recovery and update behavior still need verification.


## Worked lab and expected behavior


In B05 compare `file` and `readelf -h` for the host and AArch64 binaries. In I01 capture a full-system guest serial boot log and identify the kernel start and init/service start. In I03 compile the supplied overlay against the documented tree and run schema checks as instructed. Emulator and board steps are pending unless your own log demonstrates them.

If a foreign dynamically linked binary says it cannot find its loader, inspect the ELF interpreter and supply the intended target sysroot; do not copy host libraries. If a driver never probes, examine node status, compatible matching, kernel configuration and deferred dependencies before changing interrupt code.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain sysroot versus rootfs, initramfs versus persistent root, and device tree versus driver. Interview bank: boot, BSP and cross-compilation.

## Mastery checklist

- Identify host and target for every tool.
- Capture and annotate boot stages.
- Validate a device-tree binding.
- Explain which dependencies can defer probe.

## Primary references

[CMAKE] CMake toolchains. [QEMU-USER] QEMU userspace. [QEMU-VIRT] Generic virt machine. [DT] Linux device tree. [DTSCHEMA] Binding schemas.
