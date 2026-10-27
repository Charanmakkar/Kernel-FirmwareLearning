# Solution guidance

Compatibility must be inside authenticated metadata and checked before any slot write. Key rotation needs an authenticated transition with overlap and recovery, protected against replay. Do not accept a public key supplied by the unauthenticated bundle. Test old-only, new-only, revoked, malformed and lost-update cases.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
