# Solution guidance

Keep workloads and frequency policy stable, randomize or alternate order, retain long-tail events, and correlate traces. Measure wakeup-to-run delay separately from work completion. Instrument mutex acquisition and service time; a low median can coexist with rare long blocks. State the sample size and confidence limits without assuming a worst-case bound.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
