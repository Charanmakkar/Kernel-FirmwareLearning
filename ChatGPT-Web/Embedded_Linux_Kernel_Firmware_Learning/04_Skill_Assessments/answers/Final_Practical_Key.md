# Final practical and defense marking key

A strong submission makes one path complete and bounded before adding features. The parser has explicit partial-frame state, rejects excessive length before writing, validates CRC before exposing data, and specifies recovery after malformed input. Tests use known vectors and all split points rather than only self-round-trips.

The queue has a fixed limit and a visible overload policy. The accepted, rejected/dropped and processed counts reconcile under that policy. A peer session change invalidates old command authority; raw sequence numbers alone do not prove a new boot's identity. Staleness uses a monotonic deadline local to the responsible component.

Persistence preserves a valid configuration through the injected pre-replacement failure. The result is labeled host-filesystem evidence; real power-cut behavior is pending without target storage testing. Shutdown wakes every blocking path and releases state after users quiesce. A two-second observed host test pass is not a real-time bound for arbitrary deployment.

For C02, all startup, stale, disconnected and FAULT paths must leave output permission false until the defined explicit re-arm transition. A simulator demonstrates state logic, not a certified stopping function. For C01, stale measurements carry invalid/freshness state rather than silently remaining apparently current.

There is no single mandatory architecture beyond the stated requirements. Award full points to simpler correct designs with clear contracts. Do not require networking, cloud services or AI inference. Optional AI must not substitute for protocol, state, resource or recovery work. Penalize overclaims and missing failure tests, not a transparent pending hardware item.

During defense, trace one actual object through allocation, publication, use, cancellation and destruction. Ask the learner to predict a test outcome before running it. A live requirement change must update validation, buffer/limit assumptions, protocol compatibility and documentation where relevant. If the learner cannot explain delivered generated code, record that skill as assisted or unassessed rather than mastered.
