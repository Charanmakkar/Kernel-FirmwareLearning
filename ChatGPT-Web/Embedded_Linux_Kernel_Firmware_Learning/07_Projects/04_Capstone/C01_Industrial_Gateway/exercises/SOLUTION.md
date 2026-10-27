# Solution guidance

Define authenticated session establishment if the transport is adversarial, or an explicit local reconnect policy for a trusted wire. Bind sequence state to a session ID and reject old sessions after establishment. A random UUID alone is not authentication. Test MCU reset, Linux restart, stale buffer contents, lost handshake and session collision.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
