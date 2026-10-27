# I01 Custom Buildroot appliance

Build a minimal x86_64 Linux appliance containing a custom C package, a startup service, and a separate persistent data disk. Every service iteration safely advances an on-disk counter and prints JSON. The host-testable counter gives a small but complete persistence and recovery problem before a long image build. Plan 20–30 hours after B05 and M14, allowing extra download and build time outside active study.

## Learning outcomes and acceptance

Keep product customization in a `br2-external` tree, resolve a pinned Buildroot configuration, cross-build an application using the target compiler, boot a guest, and preserve state across a reboot. Demonstrate normal writes, concurrent writers, a crash before rename, a crash after rename, corrupt state, missing storage, and interrupted service operation. Configuration validation is not image-build validation; host filesystem tests are not physical power-loss tests.

## Supported target and contents

Reference: Buildroot 2025.02.1, upstream `qemu_x86_64_defconfig`, Linux 6.12.9, GCC 13.3.0, binutils 2.43.1, and the release's selected libc and BusyBox. Those values come from the resolved configuration, retained in evidence. The Linux version intentionally differs from I02's separately frozen 6.12.0 API-check tree. These learning pins need updating and revalidation before any real deployment.

No physical board is required. QEMU presents the root filesystem as `/dev/vda` and a separate 64 MiB ext4 data image as `/dev/vdb`. The root drive uses a temporary QEMU snapshot; the data drive is persistent. Networking is disabled in the provided launcher. Image creation only formats a project-owned regular file; never substitute a host block-device path.

`src/telemetry_once.c` is the complete app. `br2-external/` contains package metadata and root filesystem overlay. `config/learning.fragment` records customization. `scripts/configure.sh` layers the changes over the release's upstream defconfig. `tests/test_counter.py` exercises the state logic on the host.

## Architecture and recovery behavior

The service mounts its data filesystem before starting. A lock file serializes writers. Each update reads and validates the current versioned counter record, creates a new record, writes a temporary file, calls `fsync` on the file, renames it in the same directory, and synchronizes the directory. The record includes an XOR check word to detect common accidental changes; it is not a cryptographic integrity check. Invalid existing state is preserved and the service stops for diagnosis.

The previous or new complete file is expected after an interrupted update on a filesystem with the stated rename and synchronization semantics. The host tests inject process exits at specific checkpoints. Storage-controller caches, real power loss, torn sectors, and filesystem damage need separate destructive tests on disposable hardware. The persistent disk is intentionally excluded from root-image replacement; update partition design is developed in A03.

## Guided build and run

First validate the application:

```sh
make test
mkdir -p build/state
./build/telemetry-once build/state
```

Download the official `buildroot-2025.02.1.tar.xz` release and its signature from the [Buildroot archive](https://buildroot.org/downloads/), verify it using the project's documented release keys, and extract it outside this project. Install the host dependencies documented in that release's manual. Then:

```sh
sh scripts/configure.sh /absolute/buildroot-2025.02.1
make -C buildroot-output -j4
sh scripts/run_qemu.sh
```

The launcher creates the project data image only if it does not already exist. Log in on the serial console of this isolated teaching guest and inspect `cat /data/counter`. Stop the service using `/etc/init.d/S50learn-telemetry stop`, run `telemetry-once /data`, then restart it. Reboot and confirm the counter advances from the previous value. Use QEMU's console exit sequence only after testing normal shutdown first.

The upstream defconfig also enables a host QEMU build. You may use that generated emulator from `buildroot-output/host/bin` by placing the directory on PATH, or a compatible installed QEMU. Record the version. Run `make -C buildroot-output legal-info` and retain the generated manifest; supplied package metadata alone is not a complete image license review.

## Tests and evidence

Host acceptance tests cover initial state, regular increments, both crash checkpoints, forty concurrent writers with unique increments, corrupt state preservation, symlink rejection, and missing-directory errors. `LEARN_CRASH_AT=after_file_sync` exits before the committed rename; `after_rename` exits before directory synchronization. A process-exit test cannot prove power-failure durability. Configuration resolution was executed; the full toolchain/image build and guest boot are pending unless additional evidence is added.

Debug the C app with `gdb --args build/telemetry-once build/state`. In the guest, use service logs and mount status before suspecting the parser. A missing `/dev/vdb` keeps the service stopped. A corrupt record should never be silently overwritten with zero. For cleanup, stop QEMU before removing build output; retain the data image while investigating recovery. Delete that image only when intentionally resetting the lab.

## Project defense

Explain the difference between a Buildroot package and a rootfs overlay, why target compilation uses `TARGET_CC`, why file `fsync` alone is insufficient for a new directory entry, and why process-crash tests leave storage power-loss behavior unverified. Demonstrate the counter fault tests before discussing larger product architectures. Extensions include a bounded retention policy, schema migration, and a read-only configuration inspection command.

## Primary references

- [Buildroot manual](https://buildroot.org/downloads/manual/manual.html); the exact 2025.02.1 manual is also bundled in its archive.
- [Linux fsync documentation](https://man7.org/linux/man-pages/man2/fsync.2.html)
- [Buildroot release archive](https://buildroot.org/downloads/)

Access date: 27 October 2026.
