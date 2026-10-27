SUMMARY = "Learning industrial monitoring gateway"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
FILESEXTRAPATHS:prepend := "${THISDIR}/../../../../src:${THISDIR}/../../..:"
SRC_URI = "file://gateway.py file://simulated_mcu.py file://gateway-sim.service"
S = "${WORKDIR}"
inherit systemd useradd
RDEPENDS:${PN} = "python3-core python3-modules"
SYSTEMD_SERVICE:${PN} = "gateway-sim.service"
USERADD_PACKAGES = "${PN}"
USERADD_PARAM:${PN} = "--system --no-create-home --shell /bin/false gateway"
do_install() {
    install -d ${D}/opt/learning-gateway/src ${D}${systemd_system_unitdir}
    install -m 0644 ${S}/gateway.py ${S}/simulated_mcu.py ${D}/opt/learning-gateway/src/
    install -m 0644 ${S}/gateway-sim.service ${D}${systemd_system_unitdir}/
}
FILES:${PN} += "/opt/learning-gateway"
