# M11 reference solution and reasoning

Assemble bytes into an unsigned 16-bit value, shift the 12-bit field into the low bits and explicitly sign-extend values >= 0x800 by subtracting 4096. For exact scale, 1 LSB = 62.5 milliunits; use a wider integer representing half-milliunits or document rounding. +25 uses raw 400, -1 uses raw -16 and minimum is -2048. Board evidence includes correct voltage/wiring, address/mode, bus transactions, errors, binding and driver runtime tests. The exercise scale is a worked example; use A01's actual device format there.
