# I03 Device tree GPIO interrupt platform driver

## Purpose and learning outcome

Bind a device from firmware description, request its GPIO as input, count IRQ events, expose one read-only sysfs attribute, and prove teardown ordering. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 18–26 hours; allow remediation time when a prerequisite fails. Relevant learning modules: M08 M09 M10. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Build I02, explain sleepable context, read a device tree phandle, and identify physical versus BCM pin numbers.

## Minimum scope and version boundary

Linux mainline v6.12, GCC matching the target architecture; Raspberry Pi 4 Model B hardware path. This frozen kernel is educational, not a security-maintained production recommendation.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

The device tree describes GPIO17. The platform bus matches the private compatible string and calls probe. Probe acquires state, GPIO, then threaded IRQ, then publishes sysfs. The threaded handler increments an atomic counter. Managed cleanup removes the sysfs group first, quiesces/releases the IRQ, releases GPIO, then frees state. No timer, background worker, or custom character-device lifetime is hidden behind automatic cleanup.

## Build run debug and cleanup

1. Prepare a disposable Raspberry Pi 4 Model B SD-card system using mainline Linux tag v6.12 and a symbol-enabled BCM2711 DTB. Keep the original boot media untouched and a known working recovery card.
2. Build the kernel with `ARCH=arm64`, a matching AArch64 compiler and `CONFIG_PINCTRL_BCM2835`, `CONFIG_OF`, `CONFIG_MODULES`, `CONFIG_SYSFS`. Use the kernel source configuration for the exact board; confirm the actual GPIO symbol exists in the base DTB before applying the overlay.
3. Build this module with `make KDIR=/absolute/linux-build ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-` after the kernel build has generated its headers and symbol versions. Do not insert a module compiled for a different running kernel.
4. Compile the overlay with `dtc -@ -I dts -O dtb -o learning-edge.dtbo config/learning-edge-overlay.dts`. Apply offline with `fdtoverlay -i bcm2711-rpi-4-b.dtb -o learning-rpi4.dtb learning-edge.dtbo`; boot this DTB together with the matching kernel through the documented boot configuration on your prepared image.
5. Power down, wire the 3.3 V pulse source as [documented](hardware/WIRING.md), then boot. Load `learning_edge_counter.ko` with `sudo insmod learning_edge_counter.ko`.
6. Locate the actual attribute using `find /sys/bus/platform/devices -path '*/learning_edge/edges' -o -path '*/learning_edge*/edges'`. Read it with `cat`. Device names can contain an address/prefix; use the path actually discovered.
7. Debug with `dmesg -w`, the device `driver` symlink, the decoded live device tree, and `/proc/interrupts`. Stop pulses, unload using `sudo rmmod learning_edge_counter`, and restore the original DTB to clean up.

## Acceptance criteria and evidence

A clean 10 Hz source must add exactly 100 counts during an externally gated 100-pulse burst. Read repeatedly during pulses; values must never decrease. Unbind and rebind 20 times without kernel warnings, use-after-free reports or stale sysfs access. A missing event-gpios property must fail probe cleanly. Verify that no pin is driven by this driver. Manual switch bounce is not an exact-count test.

Run `python3 tests/check_count.py /actual/sysfs/edges --seconds 10 --expected 100` only with the gated pulse source synchronized to the interval. The script is a target acceptance helper, not a host IRQ simulation. Device-tree schema checking requires placing the private binding in a kernel schema tree and resolving its educational vendor prefix; do not call it an upstream accepted binding.

**Observed validation:** Source, overlay, binding, wiring, and test helper authored. Hardware IRQ, unload stress, device tree application and electrical behavior are pending. Module compile status is recorded separately in evidence/STATUS.md.

## Troubleshooting and limitations

A GPIO event is counted, not debounced, timestamped, queued or interpreted as an industrial safety input. IRQF_ONESHOT prevents reentry into the threaded handler but does not make pulse counting lossless at arbitrary rates. For buttons use the existing gpio-keys subsystem; for timestamped high-rate data choose a suitable hardware/subsystem interface.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Extend the interface with a last-edge monotonic timestamp without exposing a torn pair of count and timestamp. Explain the synchronization and ABI before changing code. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show the DT property and pin table, load the module, send a measured pulse burst, show count change, then unload while a reader is active. Explain why sysfs is acquired last.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.

**Offline device tree check passed:** The overlay compiled with dtc from Linux v6.12 and applied with fdtoverlay to a symbol-enabled BCM2711 Raspberry Pi 4 Model B base DTB. See evidence/device-tree.log. This establishes syntax and phandle resolution, not a booted board or peripheral behavior.
