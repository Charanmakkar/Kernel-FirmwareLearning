# Solution guidance

Decode the configuration according to the exact datasheet and expose supported rates with IIO conventions. Serialize configuration changes and reads if both can occur; suspend should stop conversion only when policy allows, and resume must restore the chosen mode and wait for valid data. Add bus-failure rollback and teardown tests.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
