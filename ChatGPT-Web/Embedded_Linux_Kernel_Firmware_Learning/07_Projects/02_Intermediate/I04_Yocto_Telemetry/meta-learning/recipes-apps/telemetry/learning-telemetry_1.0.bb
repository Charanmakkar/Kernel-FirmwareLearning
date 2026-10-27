SUMMARY = "Minimal learning telemetry producer"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
SRC_URI = "file://telemetry.c file://telemetry.service"
S = "${WORKDIR}"
inherit systemd
SYSTEMD_SERVICE:${PN} = "telemetry.service"
do_compile() {
    ${CC} ${CFLAGS} ${CPPFLAGS} ${LDFLAGS} ${S}/telemetry.c -o learning-telemetry
}
do_install() {
    install -d ${D}${bindir} ${D}${systemd_system_unitdir}
    install -m 0755 learning-telemetry ${D}${bindir}/learning-telemetry
    install -m 0644 ${S}/telemetry.service ${D}${systemd_system_unitdir}/telemetry.service
}
