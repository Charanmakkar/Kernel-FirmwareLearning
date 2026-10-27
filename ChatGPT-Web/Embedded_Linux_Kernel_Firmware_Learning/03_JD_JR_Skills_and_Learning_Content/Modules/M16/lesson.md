# M16 Persistence security and reliable updates

## Objectives and prerequisites

Prerequisites: M14 M07.

Make configuration writes recoverable, distinguish update trust from boot trust and test rollback state transitions.

## Lesson


Crash-safe persistence starts with a failure model. A process crash, OS crash and sudden power loss have different effects. For an atomic file replacement on a suitable local filesystem, write a temporary file in the same directory, flush the file, rename it into place and flush the directory as required by the durability contract. Preserve permissions and validation. Atomic rename does not by itself prove durability on every filesystem or storage device. Recovery tests must match the target media and failure modes.

A signed update authenticates an image or manifest under a trusted verification key. Hashing detects change but does not identify an authorized signer. Secure or verified boot checks the boot chain according to the platform's trust root; it is a separate mechanism from an application's update verification. A correctly signed but vulnerable old image can still be a downgrade risk, so version/rollback policy and protected state matter. [UBOOT]

An A/B arrangement writes an inactive slot, verifies its contents, selects it for a limited trial boot, checks health and commits or rolls back. The old slot remains the recovery candidate until the new one is accepted. Define which state survives interruption at each transition. An application health check that merely confirms process existence can commit a device whose sensors or persistent configuration are unusable. [RAUC]

The A03 project implements this state machine over files and uses real signature verification. It is a host simulator, not a bootloader, flash partition manager or hardware secure-boot chain. It establishes software behavior for exercised signature, state and interruption cases. Porting it to a board requires partition layout, bootloader integration, trusted-key storage, recovery entry, storage durability and power-cut tests. Reuse a maintained update framework when the product scope warrants it.

Apply least privilege to services: only required device access, files, network endpoints and capabilities. Validate untrusted lengths, protocol states and configuration. Avoid secrets in logs and source trees. Maintain dependency versions, provenance and a vulnerability-response process. An SBOM supports inventory; reviewing reachable exposure and deploying fixes remain engineering tasks. [YOCTO-SBOM]

Recovery is part of the interface. A technician should be able to identify the running version, previous known-good image, reset reason and last update result. Protect access to diagnostic endpoints, but make the information available through an intentional service path. Define behavior for full storage and corrupted state instead of assuming writes always succeed.


## Worked lab and expected behavior


Run A03's tests for an authentic image, modified payload, invalid signature, interrupted installation, failed health and successful commit. Inspect the generated public/private key separation; generate lab keys locally and never treat them as production keys. Then execute C01's invalid-configuration and restart tests.

For each update phase, write the expected active slot before and after a crash. Acceptance requires deterministic recovery to a verified allowed state, not merely a script returning zero. Physical power interruption and boot ROM trust remain pending until target tests exist.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

How do signing, secure boot and rollback differ? What does atomic rename guarantee? What makes a health check meaningful? Interview bank: production and system design.

## Mastery checklist

- Identify trust and recovery boundaries.
- Test every persisted-state transition.
- Preserve a known-good image.
- State untested storage and hardware assumptions.

## Primary references

[UBOOT] U-Boot verified boot. [RAUC] RAUC basics. [YOCTO-SBOM] SBOM generation. [FSYNC] fsync durability. [RENAME] rename semantics.
