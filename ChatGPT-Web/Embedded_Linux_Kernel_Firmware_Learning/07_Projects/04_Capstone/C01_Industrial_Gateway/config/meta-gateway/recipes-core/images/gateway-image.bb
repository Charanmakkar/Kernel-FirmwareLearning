SUMMARY = "Learning gateway image for qemux86-64"
LICENSE = "MIT"
inherit core-image
IMAGE_INSTALL = "packagegroup-core-boot learning-gateway ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_FEATURES += "debug-tweaks"
IMAGE_FSTYPES = "ext4"
