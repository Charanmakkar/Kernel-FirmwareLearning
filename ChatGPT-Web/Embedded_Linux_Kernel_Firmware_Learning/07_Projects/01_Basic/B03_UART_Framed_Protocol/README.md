# B03 UART terminal and framed protocol tool

Implement one bounded request-response transaction over a POSIX terminal device. The tool sends a framed UTF-8/ASCII command, waits for a matching reply, tolerates byte fragmentation and noise, and restores the terminal configuration before exit. Plan 12–16 hours after B01 and M06. It teaches UART configuration, stream framing, partial I/O, deadlines, and protocol tests without requiring hardware initially.

## Scope and measurable outcomes

The minimum tool accepts `DEVICE PAYLOAD TIMEOUT_MS`, uses 115200 baud with eight data bits, no parity, one stop bit, and no hardware flow control, and sends request type 1 with sequence 1. It accepts response type 2 with that sequence. Payload size is 0–128 bytes. A single monotonic deadline covers both transmission and response; irrelevant traffic cannot restart that deadline. Pass all PTY tests and explain why readable does not mean one full message is available.

## Architecture and interface

The B01 codec is included locally so this folder can be built independently. A nonblocking terminal feeds a bounded accumulation buffer. Invalid candidates consume one byte, preserving possible later sync. A valid but stale sequence is discarded. Incomplete candidates wait for additional bytes. The protocol is specified in [docs/PROTOCOL.md](docs/PROTOCOL.md); it is a private teaching protocol and does not provide authentication, retransmission, or duplicate suppression.

The terminal library uses `tcgetattr`, `cfmakeraw`, explicit speed and stop-bit settings, `tcsetattr`, and nonblocking `poll`. Restoring saved settings happens through one cleanup path after success, transaction failure, SIGINT, SIGTERM or SIGHUP. A minimal signal handler records cancellation; ordinary code performs cleanup. SIGPIPE is ignored so a broken stdout pipe becomes a handled write error. SIGKILL and a device that no longer accepts termios operations cannot be repaired by user-space cleanup. POSIX terminal behavior and noncanonical read settings are described in [termios](https://man7.org/linux/man-pages/man3/termios.3.html). Readiness and hangup details are described in [poll](https://man7.org/linux/man-pages/man2/poll.2.html).

## Environment and files

Use Linux, GCC 13.3.0 or a compatible C11 compiler, Make, and Python 3. A pseudo-terminal, or PTY, acts as the peer in tests. This exercises software transport behavior, not electrical signaling or UART peripheral timing. Source is in `src/`, the shared codec contract in `include/`, and the independent Python peer in `tests/`. Hardware measurements remain separate from PTY evidence.

## Guided lab

```sh
make test
./build/uart_frame /dev/ttyUSB0 hello 1000
gdb --args ./build/uart_frame /dev/ttyUSB0 hello 1000
```

The second command requires a compatible connected peer and device access. Without a reply it exits with a timeout, which is correct behavior. For an emulator-only start, run the tests first; they create and name a PTY automatically. Read `test_pty.py` and identify where the peer fragments bytes, injects noise and a stale frame, damages the CRC, or withholds a response.

Set a breakpoint at `frame_decode` in the receiver. Watch the accumulator grow while the same logical frame arrives over many reads. Then explain why checking only `read() == packet_size` would discard valid communication. The client does not call an unbounded `tcdrain`, so deadline handling is not defeated by a stalled device drain operation. `make clean` removes generated binaries.

## Hardware integration path

Use a USB-to-UART adapter and a documented 3.3 V TTL UART target. Cross adapter TX to target RX, adapter RX to target TX, and connect signal grounds. Board pin numbers depend on the selected board and its alternate-function settings; the hardware worksheet requires those values before connection. Do not substitute RS-232 voltage levels or assume every USB adapter is 3.3 V. No adapter-to-board power connection is required for independently powered devices. The exact reference target is the host PTY; the physical UART path is optional and unverified in this package.

## Acceptance and troubleshooting

The suite covers normal replies, one-byte fragmentation, noise/stale/corrupt-frame recovery, timeout after a corrupt-only reply, zero and maximum payloads, overlength rejection, and terminal attribute restoration after success, errors, SIGINT, SIGTERM, and a broken stdout pipe. The fixed sequence is reused across separate invocations; an old sequence-1 response can therefore pass in a later invocation. This limitation is explicit in the protocol contract. A device-open failure suggests permissions or a wrong path. A consistent CRC failure suggests endian or CRC coverage disagreement. Immediate disconnect errors suggest cable removal or a PTY master closing. A successful PTY test does not validate the board's baud clock, ground integrity, overrun behavior, or framing-error recovery.

## Extensions and interview demonstration

Extend the protocol with negotiated version support or a bounded retry policy only after defining duplicate behavior. Show the PTY test, explain one monotonic deadline, and draw the receive state transitions: accumulate, incomplete, discard, accepted. Defend why a CRC is not a security feature and why `volatile` is unrelated to robust serial buffering. Practice tasks and worked solutions are in separate folders.
