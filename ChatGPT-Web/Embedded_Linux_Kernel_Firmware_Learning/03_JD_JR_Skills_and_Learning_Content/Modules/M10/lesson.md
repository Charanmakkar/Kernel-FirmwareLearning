# M10 Character and platform drivers

## Objectives and prerequisites

Prerequisites: M09.

Implement an educational character interface, define blocking and poll semantics, and choose a standard subsystem for real hardware.

## Lesson


A character driver is useful for learning how file operations reach kernel code. Define its user ABI first: byte stream or records, blocking behavior, nonblocking EAGAIN, EOF, short operations, errors and concurrency. `copy_to_user` and `copy_from_user` report bytes not copied, not the usual negative errno convention. They can fault; do not use them under a context or lock that forbids sleeping. Handle partial transfer deliberately rather than silently losing queued data. [UACCESS]

A wait queue waits for a predicate such as data available or shutdown. Registration, state changes and wakeups must form a race-free protocol. After waking, another reader may have consumed the data, so recheck under the correct synchronization. `poll` registers interest using poll_wait and reports the currently satisfied conditions. Readiness may change before the caller performs I/O. A correct nonblocking operation remains necessary even when poll exists.

File-private state can hold per-open data, but shared device state needs a lifetime rule. `.owner = THIS_MODULE` helps protect module code while open file operations use it; it is not a complete hot-unplug memory ownership design. If the exercise intentionally permits unload only after close, state that scope and test it. Production removable devices need a more complete reference-counted lifetime.

Platform drivers bind devices that are not discoverable through a self-enumerating bus such as PCI. Firmware description can provide resources, and probe resolves them through device-managed or explicit APIs. A successful probe publishes a usable interface; a failed probe must unwind cleanly. The `.remove` callback signature and helper APIs can change across kernel releases, so build against the frozen source and review exact declarations before migrating. [DRIVER]

An ioctl should be used only when existing file operations and subsystem interfaces do not fit. Define fixed-width fields, alignment, compatibility, size and direction consistently; never expose a raw kernel pointer or a layout with implicit architecture-dependent padding. A stable user ABI costs maintenance. Standard subsystems such as input, hwmon, IIO and GPIO already supply discovery and user interfaces. Use the existing subsystem for a real device when its semantics fit rather than inventing a custom character device for every sensor. [IIO]


## Worked lab and expected behavior


Build the I02 driver against its named kernel tree and its user-space client with the host compiler. Run in the matching disposable guest. Exercise empty blocking read, empty nonblocking read, full write, short user buffer, concurrent users and poll wakeup. A host-only client compile cannot validate any kernel behavior.

In I03 inspect matching compatible strings and GPIO descriptor names across binding, overlay and driver. If probe returns an error, retain the errno and distinguish an unavailable dependency from invalid configuration. Check logical active state and debounce policy before assuming every interrupt represents a physical event.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Why do uaccess helpers return a residual count? How does poll avoid lost wakeups? When is a custom ioctl justified? Interview bank: driver implementation and design.

## Mastery checklist

- Publish an explicit user ABI.
- Test blocking/nonblocking behavior.
- Review user-copy failure handling.
- Explain subsystem selection and teardown.

## Primary references

[UACCESS] Kernel uaccess API. [DRIVER] Linux driver model. [GPIO] GPIO consumers. [IIO] Industrial I/O subsystem.
