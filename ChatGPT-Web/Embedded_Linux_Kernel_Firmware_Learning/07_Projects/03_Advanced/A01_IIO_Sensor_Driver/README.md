# A01 Sensor driver using the IIO subsystem

## Purpose and learning outcome

Register a real IIO temperature channel, use correct bus byte order and units, propagate bus errors and restore device configuration on removal. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 24–36 hours; allow remediation time when a prerequisite fails. Relevant learning modules: M09 M10 M11 M15. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Complete I02/I03, decode signed bit fields, understand I2C transactions and managed resource lifetimes.

## Minimum scope and version boundary

Linux mainline v6.12, GCC matching the target architecture; Raspberry Pi 4 Model B hardware path. This frozen kernel is educational, not a security-maintained production recommendation.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

An I2C client probe reads and saves the TMP102 configuration, selects 12-bit continuous mode, waits for conversion, and registers a direct-mode IIO device. Read raw returns the sign-extended 12-bit value. Scale is 62.5 millidegrees Celsius per count. Managed cleanup unregisters IIO before restoring the original sensor configuration. SMBus word-swapped helpers account for the sensor most-significant-byte-first register format.

## Build run debug and cleanup

1. Use Linux v6.12 on Raspberry Pi 4 Model B and a TI TMP102 breakout with documented schematic. Follow hardware/WIRING.md; connect SDA pin 3, SCL pin 5, V+ pin 1 at 3.3 V, GND pin 6 and ADD0 to ground for address 0x48.
2. Enable I2C controller support, `CONFIG_IIO` and modules in the matching kernel configuration. Remove any existing conflicting TMP102 node or driver binding. The supplied private compatible selects only this educational driver.
3. Build with `make KDIR=/absolute/linux-build ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-`. Build the selected kernel first, including symbol metadata; compile against that same tree.
4. Compile and apply `config/learning-tmp102-overlay.dts` using `dtc -@` and `fdtoverlay` against a symbol-enabled BCM2711 DTB. Ensure I2C1 pinmux and board boot configuration select the new DTB; the overlay does not magically replace boot firmware configuration.
5. Load `learning_tmp102.ko`. Locate the IIO directory whose `name` contains `learning_tmp102`. Read `in_temp_raw` and `in_temp_scale`; multiply to get millidegrees Celsius, then divide by 1000 for Celsius.
6. Debug probe errors through dmesg, the I2C adapter identity, logic-analyzer ACK/address traces and the hardware schematic. Do not repeatedly scan a shared production bus; use this isolated sensor bus.
7. Unload with `sudo rmmod learning_tmp102`; inspect that the original configuration was restored. Remove the overlay to clean up.

## Acceptance criteria and evidence

At raw word 0x1900 the decode is 25 °C; 0xE700 is −25 °C; 0xFFF0 is −0.0625 °C. All host golden vectors pass. On a board, compare measurements with a reference thermometer within the relevant datasheet accuracy and thermal-settling limits; resolution alone is not accuracy. Disconnecting the sensor must return an I/O error, not a fabricated temperature. Reprobe and concurrent reads must not warn or leak.

Run `python3 -m unittest discover -s tests -v`. Seven golden-vector checks verify the numeric reference model, including both signed boundaries and wire order. They do not call the kernel driver or emulate an I2C controller. Pending board tests include bus NACK, power loss, unbind/rebind, actual IIO units and configuration restoration.

**Observed validation:** Complete direct-mode IIO driver, overlay, wiring and decoding tests authored. Seven numeric host tests passed. Kernel-module compile status is recorded in evidence/STATUS.md; hardware execution is pending.

## Troubleshooting and limitations

The upstream TMP102 driver uses hwmon and is normally the suitable existing production driver. This private IIO implementation is for subsystem education. It omits alerts, runtime power management, triggered buffers and calibration. Add those only after selecting a real requirement; this device is a low-rate temperature sensor, not a high-speed inertial sensor.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Add a read-only sampling-frequency description based on configured conversion-rate bits, then design suspend/resume behavior that preserves operator configuration. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show register-to-value arithmetic, compare IIO raw and scale, demonstrate a bus failure, and explain why an existing hwmon driver is usually preferred.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.

**Offline device tree check passed:** The overlay compiled with dtc from Linux v6.12 and applied with fdtoverlay to a symbol-enabled BCM2711 Raspberry Pi 4 Model B base DTB. See evidence/device-tree.log. This establishes syntax and phandle resolution, not a booted board or peripheral behavior.
