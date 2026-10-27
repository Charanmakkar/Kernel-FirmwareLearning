# Solution guidance

Use a short spinlock-protected snapshot for the count/timestamp pair, or a correctly initialized seqcount with a single serialized writer. Do not place a potentially sleeping GPIO read inside a spinlock. Preserve sysfs publication and teardown order. Test concurrent readers and IRQ load, including zero edges.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
