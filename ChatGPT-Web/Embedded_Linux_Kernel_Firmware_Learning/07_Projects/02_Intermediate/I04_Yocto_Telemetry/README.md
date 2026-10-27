# I04 Custom Yocto telemetry image

## Purpose and learning outcome

Produce an image from an owned layer, install a service, generate an SDK, inspect build metadata and record exact layer revisions. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 22–36 hours plus unattended downloads and builds; allow remediation time when a prerequisite fails. Relevant learning modules: M04 M08 M14 M16. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Build B05/I01, understand recipes and a sysroot, and use a dedicated supported build host.

## Minimum scope and version boundary

Yocto/Poky tag yocto-5.0.9 Scarthgap, qemux86-64, dedicated Ubuntu 22.04 host. Native app checked with GCC 13.3.0 only. Image and SDK builds pending.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

The meta-learning layer supplies an application recipe, a systemd unit and an image recipe. The application prints monotonic simulated samples and handles termination. systemd owns restart and privilege isolation. The recipe passes target compiler and linker flags; no host binary is copied into the target image. The image is intentionally an isolated development image with debug-tweaks enabled.

## Build run debug and cleanup

1. Use a dedicated Ubuntu 22.04 x86-64 VM because this is an explicitly supported host in the frozen Yocto 5.0.9 documentation. The test container running this authoring session is not a verified Yocto build host. Allocate approximately 16–32 GB RAM and 150–250 GB free disk as practical estimates; exact requirements depend on image and parallelism.
2. Install the host prerequisites from the official 5.0.9 system-requirements page. Typical Ubuntu packages include `build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget xz-utils zstd lz4`. Enable an `en_US.UTF-8` locale and read the exact release documentation if a package check fails.
3. From this project directory run `sh scripts/setup.sh /absolute/empty/workdir`. It checks out tag `yocto-5.0.9`, adds this layer, configures qemux86-64 and systemd, then builds learning-image. It downloads and executes build tools from their official sources; run as an ordinary user.
4. In another shell `cd /absolute/workdir/poky` and `. oe-init-build-env build`; run `bitbake-layers show-layers` and save the output plus `git -C .. rev-parse HEAD`.
5. Boot with `runqemu qemux86-64 learning-image nographic`. In the guest inspect `systemctl status telemetry`, `journalctl -u telemetry`, and `systemctl stop telemetry`.
6. Generate the SDK with `bitbake learning-image -c populate_sdk`, install the generated script from `tmp/deploy/sdk` into a separate directory, source its environment-setup file and compile the application again. Inspect the ELF architecture before copying it to the guest.
7. Exit the guest normally and retain `conf`, layer source, revisions and logs. Remove the dedicated work directory only when downloads and evidence are backed up.

## Acceptance criteria and evidence

A clean image boots in QEMU; telemetry.service is enabled; sequential sample numbers appear with monotonic seconds; SIGTERM stops without a crash; the service runs unprivileged. The SDK emits a target ELF. A rebuild with the same saved configuration and inputs must have its artifact hashes compared, with any differences investigated rather than declared reproducible by assumption.

Run `python3 -m unittest discover -s tests -v` for a native compile and shutdown test. This checks application behavior only. Run BitBake parsing, image, QEMU boot, service sandbox and SDK tests on the supported host. Inspect `bitbake -e learning-telemetry` to diagnose recipe paths and inherited values.

**Observed validation:** Layer, recipes, service, configuration and setup scripts authored. Native application compile and one process integration test passed. BitBake parse, image build, QEMU boot and SDK creation have not been executed in this session.

## Troubleshooting and limitations

Frozen 5.0.9 is a reproducibility baseline, not a recommendation to deploy an outdated image. Before production, update to a maintained release, rebuild, review advisories and licensing, remove debug-tweaks, provision accounts/keys, define update/recovery policy and verify kernel support. The selected Yocto kernel is determined by its own pinned metadata and must not be confused with the standalone Linux 6.12 driver lab.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Package a separate configuration file and prove that updating the application does not overwrite operator-owned persistent settings. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show layer revision, recipe inputs, target ELF, service identity, sample logs and graceful stop; finish with a diagram showing host build, SDK and target runtime as separate environments.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.
