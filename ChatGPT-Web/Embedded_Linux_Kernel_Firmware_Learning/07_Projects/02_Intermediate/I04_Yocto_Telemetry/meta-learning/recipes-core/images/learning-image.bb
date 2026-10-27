SUMMARY = "QEMU learning telemetry image"
LICENSE = "MIT"
inherit core-image
IMAGE_INSTALL = "packagegroup-core-boot learning-telemetry ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_FEATURES += "debug-tweaks"
IMAGE_LINGUAS = "en-us"
IMAGE_FSTYPES = "ext4"
