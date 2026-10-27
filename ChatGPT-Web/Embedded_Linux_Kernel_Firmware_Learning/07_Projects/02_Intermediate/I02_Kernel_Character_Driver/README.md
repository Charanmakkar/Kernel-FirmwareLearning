# I02 Kernel character driver and user space client

Implement an educational Linux miscellaneous character device backed by a bounded byte FIFO. It supports blocking reads and writes, nonblocking `EAGAIN`, partial transfers, `poll`, concurrent access, and normal module lifetime rules. Plan 24–32 hours after M09 and M10. Its purpose is to learn user/kernel boundaries and concurrency; a real sensor should normally use the appropriate Linux subsystem developed in A01.

## Supported environment and acceptance

The API baseline is upstream Linux 6.12.0 with an x86_64 build tree. Use a disposable guest with the same built kernel and module configuration. A host compiler cannot prove a module will load into an arbitrary running kernel. The provided client is Linux userspace C11. Source is complete, but the supplied validation distinguishes object compilation, final module linking, guest loading, and device runtime tests.

Accept a passing zero-length operation, empty/full nonblocking semantics, partial writes, read/write readiness, a sleeping reader awakened by a writer, and a 1 MiB concurrent ordered stream. Repeat stress tests while checking kernel logs. Add the user-copy and unload tests in the separate test plan. A kernel warning, memory fault, blocked teardown, or lost data is a critical failure even if some transfer tests pass.

## Driver architecture

The driver registers `/dev/learn_fifo` with mode 0600. A single mutex protects the FIFO's data and indices. User copies can fault and sleep, so they occur under a sleepable mutex. An atomic byte-count snapshot provides wait and poll predicates; the actual FIFO remains locked. After moving data, operations update readiness and wake the opposite side. Every wake is followed by a predicate recheck under the mutex because another thread may consume the opportunity first.

Read and write return positive partial counts when some user bytes were transferred, even if the remaining copy faulted. They return an error when no bytes were transferred. Poll registers both wait queues before sampling readiness. The interface is a shared byte stream: it has no per-message atomicity, per-client queue, broadcast semantics, or EOF-on-last-writer behavior. Normal module unloading is blocked while open file references pin `.owner = THIS_MODULE`. This simple static device does not claim safe hot-unplug support.

Linux 6.12 no longer provides the old `no_llseek` name used in many tutorials; this source uses `stream_open` and no seek callback. Consult the selected tree instead of copying API names from unrelated versions. [Linux 6.12 misc device lifetime](https://docs.kernel.org/6.12/driver-api/misc_devices.html) and [kernel FIFO APIs](https://docs.kernel.org/6.12/core-api/kernel-api.html) support the design choices.

## Build and deploy inside the guest

Build and boot the selected Linux 6.12 kernel following M09, preserving its full output directory and `Module.symvers`. Then from the project directory:

```sh
make client
make module KDIR=/absolute/linux-6.12-built-tree
```

Copy the project and module into that guest, install Python 3 there for the automated runtime test, and run as guest root:

```sh
sh scripts/guest_test.sh
```

The script loads the module, runs the small client, runs the device tests, displays recent kernel messages, and unloads on exit. Do not run it against the shared host kernel. If building through a separate `O=` kernel output directory, point KDIR to that output tree. `modules_prepare` prepares headers and build tools but does not supply a complete `Module.symvers`; an object-only check is useful but cannot replace a full module build.

## Guided debugging lab

First inspect `/sys/class/misc/learn_fifo/dev` and the corresponding device node. Use `strace` in the guest on `build/fifo_client /dev/learn_fifo hello`. Observe that readiness and transfers are separate calls. Empty the FIFO, start a reader, verify that it sleeps, then write from a second terminal. Fill the FIFO in nonblocking mode and show `EAGAIN`. Retain the log before and after a concurrent stream test.

For deeper debugging, use the kernel's documented GDB/QEMU workflow with debug symbols, or add temporary tracepoints and remove them after isolating the failure. Do not print one message per byte in a timing experiment. A one-writer/one-reader ordering test does not prove arbitrary many-writer record atomicity, because this interface does not promise record boundaries.

## Validation and limitations

The supplied evidence records GCC 13.3.0 userspace client compilation and a `W=1` kernel composite-object build against prepared Linux 6.12.0. Final `.ko` modpost checks, insertion, all device runtime tests, signal interruption, copy faults, and unload stress are pending in a disposable guest. No runtime success is inferred from object compilation.

If `/dev/learn_fifo` is absent, inspect registration errors and devtmpfs/udev. If `insmod` reports a format or symbol error, compare the running release, configuration, compiler options, and module symbol versions. Never bypass that mismatch with forced loading. Before cleanup, close clients and unload normally; `make clean KDIR=...` then removes local outputs.

## Interview demonstration

Defend why the lock is a mutex, why a wakeup is not ownership of data, how partial user copies are reported, and which references prevent normal unload. Explain why this FIFO needs no ioctl for its minimum functionality. A meaningful extension is a carefully specified statistics interface with stable types, or a dynamically allocated per-device lifetime design using reference counting and explicit removal behavior.

## Primary references

- [Linux 6.12 external module builds](https://docs.kernel.org/6.12/kbuild/modules.html)
- [Linux 6.12 miscellaneous devices](https://docs.kernel.org/6.12/driver-api/misc_devices.html)
- [Linux 6.12 kernel FIFO API](https://docs.kernel.org/6.12/core-api/kernel-api.html)

Access date: 27 October 2026.
