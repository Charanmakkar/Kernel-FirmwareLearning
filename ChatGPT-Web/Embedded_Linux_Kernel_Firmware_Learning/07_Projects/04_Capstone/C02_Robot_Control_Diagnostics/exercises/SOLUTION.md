# Solution guidance

Schedule delivery events with original creation time and session identity. Reject out-of-order sequence numbers and bound accepted command age using a clock/synchronization strategy or a request/lease protocol. Define whether recovery requires explicit rearm. Test duplicate, reorder, reset, wrap, prolonged loss and clock disagreement independently. Retain local MCU expiry even if Linux reports healthy.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
