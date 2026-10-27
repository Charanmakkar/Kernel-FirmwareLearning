# M11 Peripheral buses sensor subsystems DMA and power

## Objectives and prerequisites

Prerequisites: M10.

Read a datasheet into an interface contract, select a subsystem and explain data, DMA and power lifetimes.

## Lesson


UART is an asynchronous serial transport with configured baud, data and stop bits; it does not define application framing. I2C uses addressed transactions and requires attention to register conventions and bus errors. SPI usually has a controller, chip select, clock polarity/phase and device-specific transfers; there is no universal register command format. A driver must honor the actual datasheet, not the bus name alone.

Translate one sensor register completely: address, reset value, read/write behavior, byte order, signedness, scale, reserved bits and valid operating modes. A signed sample often needs sign extension before scaling. A wrong scale can produce plausible values, so test known negative, zero and full-scale bit patterns independently of the bus. A communication success does not mean the device is configured or settled.

Linux IIO provides a model for measurement channels, raw values, scales, buffers and triggers. hwmon often fits system health sensors; input fits user input events. The A01 driver is an educational subsystem exercise whose selected device and upstream alternative are described explicitly. Do not bind an educational replacement and an upstream driver to the same device simultaneously. [IIO]

Regmap can organize register access and caching, but cached values must respect volatile/precious registers and power transitions. A failed bus transfer should preserve state invariants and return an interpretable error; endless retries can block a shutdown or control path. Define a retry budget and recovery mechanism such as resetting a peripheral only when the hardware and ownership contract permit it.

For direct memory access, configure the device's DMA capabilities and use the DMA API to map buffers. Coherent allocations still require ordering and ownership discipline; streaming mappings require the appropriate synchronization transitions. Check mapping failure, use the required direction and never let the CPU or device use a buffer after its lifetime or mapping ends. A CPU virtual pointer is not the value to write into a device's DMA address register. [DMA]

Runtime power management suspends an idle device independently of whole-system sleep. A transaction must hold a valid usage reference and handle resume failure. On suspend, decide what happens to interrupts, in-flight transfers, cached registers and wakeup sources. On resume, restore the hardware state before reporting data valid. System suspend/resume adds coordination with the broader platform. [RPM]


## Worked lab and expected behavior


Use A01's conversion tests before connecting the sensor. Read the selected datasheet and annotate the corresponding source masks and scale. On hardware, check identity/mode and read the interface through its subsystem, then unplug or force a bus error under the project's procedure. Acceptance includes valid conversion, error propagation and successful recovery without stale data being reported as fresh.

For a DMA design review, draw CPU owns, device owns and completion transitions. Label each mapping/synchronization operation and the point where memory may be freed. For power management, inject a resume failure and confirm no register read occurs against a suspended device.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

When is hwmon preferable to IIO? What is a DMA mapping? Why must power resume precede register access? Interview bank: buses, drivers and power.

## Mastery checklist

- Decode signed values without relying on a packed cast.
- Identify standard subsystem fit.
- Explain DMA ownership transitions.
- Test bus and resume failures.

## Primary references

[IIO] Linux IIO. [DMA] Linux DMA mapping. [RPM] Runtime PM. [GPIO] GPIO consumer rules. A01 provides its exact device datasheet.
