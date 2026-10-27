# Solution guidance

Keep defaults in a read-only package-owned location and copy missing defaults to a persistent state directory on first start. Version the configuration schema and migrate atomically. Test an old schema, corrupt file, read-only filesystem and interrupted migration; do not blindly copy defaults on every boot.

This is guidance for the optional extension. The complete minimum reference implementation is in src; a new extension is accepted only after its own implementation and tests exist.
