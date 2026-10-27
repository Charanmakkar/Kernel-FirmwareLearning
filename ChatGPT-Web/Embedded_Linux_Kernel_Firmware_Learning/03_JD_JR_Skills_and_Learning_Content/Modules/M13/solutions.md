# M13 reference solution and reasoning

Use a local monotonic receive timestamp for the freshness deadline; do not trust a remote clock without synchronization. Only a valid current-session command updates the deadline. Duplicate or corrupt commands do not extend authorization unless the protocol deliberately defines accepted retransmission. On stale input transition to DISABLED/FAULT and apply bounded local output behavior. A new boot/session requires re-arming. Test boundary values around 200 ms in deterministic simulated time, then measure physical timing separately.
