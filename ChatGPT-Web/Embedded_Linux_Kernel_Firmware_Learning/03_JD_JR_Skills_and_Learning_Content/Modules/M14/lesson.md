# M14 Buildroot Yocto and image maintenance

## Objectives and prerequisites

Prerequisites: M08 M06.

Choose the build-system scope, package a service and preserve a reproducible image configuration.

## Lesson


Buildroot creates a toolchain, root filesystem and often a bootloader/kernel for an embedded image. Keep project changes in a br2-external tree and save a minimal defconfig plus any selected component configs. A changed option can require a clean rebuild; copying one newly compiled file into an old image can conceal inconsistent dependencies. The release-local manual and project configuration are the execution contract. [BUILDROOT]

Yocto is a broader build ecosystem using OpenEmbedded metadata and BitBake tasks. A recipe describes fetching, configuring, compiling and packaging a component; a layer organizes metadata and configuration. An image selects packages and policies. A machine selects hardware integration; a distribution configuration selects wider policy. An SDK gives application developers a compatible cross environment. These roles are different, so keep application recipe changes separate from hardware policy where possible.

Pin source revisions and record layer branches, configuration, checksums and license information. A recipe that fetches a moving branch without a fixed revision can change without your code changing. Reusing a build cache speeds development but does not excuse an undeclared dependency. Reproduce a release from a clean documented setup and compare the intended outputs; a timestamp difference must be explained rather than ignored.

Service integration includes the executable, configuration, user account, writable directories and lifecycle policy. A service should fail clearly on invalid configuration, use bounded restart behavior and expose health. A systemd unit belongs only in an image that uses systemd; a BusyBox init script has a different contract. Writing to /var on a read-only root requires a writable mount or an explicit transient-storage design.

Separate immutable image content from persistent device configuration. A new image must understand the stored configuration or migrate it transactionally with a rollback policy. Test full storage, malformed configuration and interrupted writes. A persistent partition is not automatically safe if the application rewrites a file in place.

Build systems can generate license manifests and software bills of materials, or SBOMs. Yocto's SPDX output describes components and relationships useful for release inventory. An SBOM is not proof that the image is secure or that every license obligation has been satisfied; it is evidence used in those reviews. [YOCTO-SBOM]


## Worked lab and expected behavior


Build I01's minimal appliance first. Verify the custom program is installed and starts through the intended init system. Then use I04 to add a telemetry recipe and service in its own Yocto layer. Record configuration and inspect the generated image manifest. Generate an SDK using I04's command and build the client with that SDK.

Expected image behaviors require guest boot logs. A recipe parsed without errors has not been compiled, packaged or booted. If a service is missing, inspect image package inclusion, recipe install paths and init-system integration in that order. Avoid editing files directly inside tmp/work as the permanent fix.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain recipe versus layer versus image. How do you pin a release? What does an SDK contain? Interview bank: build systems and deployment.

## Mastery checklist

- Rebuild from saved configuration.
- Trace a source file to an installed package.
- Demonstrate service lifecycle.
- Explain persistent state across upgrades.

## Primary references

[BUILDROOT] Official manual and pinned release-local manual. [YOCTO-HOST] Yocto 5.0.9 requirements. [YOCTO-SBOM] Yocto SPDX generation. I04 includes exact layer/recipe references.
