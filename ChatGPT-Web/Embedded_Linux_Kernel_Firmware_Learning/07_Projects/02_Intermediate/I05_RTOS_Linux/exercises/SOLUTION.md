# Solution guidance

Define a separate command kind and response kind, bound outstanding commands, cache the last accepted sequence/result, and resend the cached acknowledgement for duplicates. Do not restart a deadline when corrupted/duplicate bytes arrive. Test lost acknowledgement, repeated command, sequence wrap and reset/session identification.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
