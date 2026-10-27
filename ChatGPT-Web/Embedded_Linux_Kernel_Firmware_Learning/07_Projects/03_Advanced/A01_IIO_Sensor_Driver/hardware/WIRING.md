# TMP102 with Raspberry Pi 4 Model B

Use a TMP102 breakout with accessible ADD0 and known schematic; this pin table refers to signal labels, not package pin order. Supply V+ from Pi physical pin 1 at 3.3 V, GND from pin 6, SDA from pin 3 (GPIO2), SCL from pin 5 (GPIO3), and ADD0 to GND for address 0x48. Leave ALERT unconnected in this polling lab. Inspect breakout pull-ups: all must go to 3.3 V, and parallel pull-ups must not exceed the device sink-current budget. Pi GPIO2/3 already have board pull-ups. Wire with power removed.

Enable the actual I2C1 controller through the compiled board device tree and verify pinmux. The overlay targets the i2c1 label in a symbol-enabled BCM2711 board DTB. Disable any existing ti,tmp102 node before using the private lab node; never bind both drivers to one address.

The upstream Linux TMP102 hwmon driver is the preferred existing solution for ordinary product temperature monitoring. This project deliberately reimplements a small direct-mode subset through IIO for learning. It is not a proposed upstream replacement.

References: TI TMP102 datasheet https://www.ti.com/lit/ds/symlink/tmp102.pdf ; Raspberry Pi pin map https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio . Accessed 2026-10-27.
