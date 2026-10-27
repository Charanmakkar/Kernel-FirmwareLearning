# A03 Signed A B update and rollback simulator

## Purpose and learning outcome

Authenticate release metadata and payload, write only an inactive slot, trial boot with a finite retry budget, confirm health, reject old versions and preserve a working active slot across an injected interruption. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 24–36 hours; allow remediation time when a prerequisite fails. Relevant learning modules: M03 M16 M17. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Understand hashes versus signatures, atomic file replacement, persistence and failure-state machines.

## Minimum scope and version boundary

Host Linux x86-64, Python 3.12.14; recorded kernel 6.18.55. No board required for the delivered host minimum. OpenSSL 3.0.13; P-256 ephemeral test signing keys.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

A signed manifest binds compatibility, release version and SHA-256 payload digest. OpenSSL verifies a detached signature against a provisioned public key. The installer snapshots verified bytes, writes the inactive file slot, fsyncs files/directories, then commits pending metadata. Each simulated boot consumes one trial before returning the candidate slot. Two unconfirmed attempts cause rollback. Health confirmation promotes the slot and advances the stored minimum accepted version. A filesystem lock serializes operations.

## Build run debug and cleanup

1. Use Linux, Python 3.12 and OpenSSL 3.0. No block-device access or root privilege is required.
2. Run `python3 -m unittest discover -s tests -v`. The suite generates ephemeral P-256 test keys inside temporary directories; no private key is shipped.
3. Run `sh scripts/demo.sh`. This creates signed factory/update bundles, provisions a fresh simulated device, installs B, trial boots B and confirms it.
4. Inspect `python3 src/update.py --help` for individual bundle/init/install/boot/good/status operations. Store release private keys outside a real target; only a public trust anchor belongs on it.
5. To demonstrate rollback, perform install then boot three times without good. The first two selections are B and the third is A.
6. To demonstrate tamper rejection, modify image.bin after signing and attempt installation; it must fail without changing active or pending state.
7. Delete only the dedicated simulation directory to reset. Never point this program at a real boot partition or existing device state.

## Acceptance criteria and evidence

All nine tests pass. Unauthenticated metadata, payload corruption, premature confirmation and non-increasing versions fail. A fault before pending-state commit leaves A selected. A bad trial image falls back to the verified active slot. Two unconfirmed trials restore A. Confirmation switches active and updates the minimum version. Every claimed durability boundary is tied to a write/fsync/rename step.

The tests execute real OpenSSL signatures and verify simulator state after injected failures. The demo executed successfully and ended with active B, min_version 2, no pending slot. Power loss is simulated at one transaction boundary; actual flash, filesystem, controller and bootloader behavior are not established.

**Observed validation:** Complete host simulator authored; nine tests and a signing/install/confirm demo passed. Real bootloader integration, storage power-cut testing, secure key storage, monotonic hardware counters and verified boot are pending production work.

## Troubleshooting and limitations

The simulator trusts its local directory, public-key file and state metadata. An attacker who can rewrite those can defeat rollback policy; the counter is not tamper resistant. Signatures authenticate an update package but do not establish secure boot, runtime integrity or trusted recovery. Use a maintained update framework such as RAUC and board-specific boot integration for a deployable system, then test the real interruption matrix.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Add a signed hardware compatibility mismatch test and a second trusted key for planned rotation, with an explicit revocation policy. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show one valid manifest, reject a changed byte, demonstrate two failed trial boots, then confirm a healthy update and explain why secure boot remains a separate requirement.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.
