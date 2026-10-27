# Reference implementation validation

Date: 27 October 2026. Host compiler observed: `cc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0`. These are tests of the delivered reference routines, not scores for the learner.

`coding_reference.c` compiled with `-std=c11 -Wall -Wextra -Werror -pedantic`. Execution passed the included assertions for 30 routines covering boundaries, invalid input, wraparound and state transitions. `posix_reference.c` compiled with the same flags and passed its normal pipe and invalid-descriptor tests. Its test does not claim to force every partial-write or EINTR path.

A build of coding_reference.c with `-fsanitize=address,undefined -fno-omit-frame-pointer` succeeded. The initial execution failed in LeakSanitizer runtime initialization because the container could not read another task's `/proc/.../task` under its execution/tracing restrictions. Re-running with `ASAN_OPTIONS=detect_leaks=0` passed. Therefore AddressSanitizer and UndefinedBehaviorSanitizer execution are recorded as passed for these inputs, while leak detection is explicitly not validated. The routines use fixed storage; no claim of general memory-safety proof is made.

The supplied broken source and synthetic traces are intentional assessment fixtures. They are not passing implementations, real crash evidence, or hardware measurements. No board, real UART, DMA, IRQ, analog sensor, flash power-cut or motor-control validation was performed by this assessment suite. Target-specific checks remain pending.

Additional executed checks: `streaming_reference.c` and `parser_repair.c` both compiled with the same strict C11 warning flags and passed. Streaming tests covered every split of a valid frame, zero-length and coalesced records, excessive length, latched error and explicit reset, truncated-state detection, and maximum payload. The parser repair passed supplied valid, truncated, oversized and unchanged-on-failure cases. No sanitizer run is claimed for these two additional files.
