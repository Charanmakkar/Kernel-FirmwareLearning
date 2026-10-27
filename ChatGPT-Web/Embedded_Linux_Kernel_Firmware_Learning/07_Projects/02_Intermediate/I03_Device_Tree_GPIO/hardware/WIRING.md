# Raspberry Pi 4 Model B edge input

Power down before changing wiring. Use a 3.3 V logic pulse source. Connect pulse output to physical pin 11, BCM GPIO17, through a 1 kΩ series resistor. Connect source ground to pin 6. Connect a 10 kΩ pull-down from pin 11 to pin 6 to define idle low. Never use a 5 V pulse. Use a current-limited logic source; do not drive a pin configured as an output.

The selected driver requests GPIO17 as input and counts rising edges. Mechanical switch bounce intentionally counts as multiple electrical edges; the minimum implementation is not a debounce driver. For manual checking use a switch between 3.3 V pin 1 and the series resistor; expect multiple counts unless debounced externally. The quantitative acceptance test requires a clean pulse generator at 10 Hz. No external output is driven by this project.

Official pin and voltage reference: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio accessed 2026-10-27.
