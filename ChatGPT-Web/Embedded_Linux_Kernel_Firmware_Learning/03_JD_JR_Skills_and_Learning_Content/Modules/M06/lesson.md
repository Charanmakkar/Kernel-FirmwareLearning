# M06 Linux I/O processes and event loops

## Objectives and prerequisites

Prerequisites: M01 M02 M05.

Write correct partial-I/O loops, manage child processes and implement bounded timeouts and graceful termination.

## Lesson


`read` asks for up to a count of bytes. A positive return is progress, which may be smaller than requested. Zero means end-of-file for ordinary files and streams in their normal modes, but terminal timeout modes need their own contract. A negative result reports an error through errno. `write` can also complete partially. Preserve your offset, handle interruption and integrate nonblocking retry with readiness rather than spinning. [READ] [WRITE]

A read-ready event means an operation should not block according to that interface; it does not promise a complete application message. `poll` scans a descriptor set; `epoll` maintains an interest set and returns events. With edge-triggered nonblocking epoll, drain the operation until EAGAIN or a terminal condition so unread work does not remain without a new edge. A hangup can coexist with buffered readable data. [EPOLL]

Use a monotonic clock for elapsed-time deadlines. Recompute remaining time after EINTR, otherwise repeated signals can extend a timeout indefinitely. Decide what your API promises after partial progress and failure. A caller often needs both the number of bytes transferred and the reason it stopped. A blocking send-all helper without a deadline can hang a control path forever.

`fork` creates a child execution context and `exec` replaces the process image; the child does not become a separate program until exec succeeds. File descriptors can be inherited. Use close-on-exec where appropriate, close unused pipe ends, and reap child status with waitpid to avoid zombies. Shared file-description offsets can explain surprising I/O after duplication or fork.

Signals interrupt ordinary control flow. Most library calls, including typical formatted logging, are not safe inside an asynchronous handler. A simple handler can set a suitable flag or write to a self-pipe under the correct restrictions; a design can also consume blocked signals synchronously in a dedicated thread. Publish a shutdown request, stop accepting work, wake blocked workers, drain or discard according to policy, join and release resources. [SIGNAL]

`/proc` exposes process and kernel state, `/sys` describes kernel objects and attributes, and `/dev` contains device interfaces. They have different contracts. Device names can change; discover a device by stable attributes or managed rules rather than assuming that the first USB serial adapter is always the desired one. udev normally manages device events on distributions that use it; a small BusyBox image may instead use devtmpfs and a different policy.


## Worked lab and expected behavior


Use B03's pseudo-terminal tests. Verify that a fragment sent before a timeout is preserved or discarded according to the published transaction policy. Confirm that malformed input does not leave the terminal settings changed after exit. For B02, pass a nonexistent PID and verify a clear error return rather than a crash. Try a process that disappears during inspection and document that snapshots are inherently racy.

To debug a blocked read, inspect which descriptor is open, whether its peer is alive, whether termios is in canonical mode and whether your timeout uses the intended clock. Use strace when installed to distinguish no data from an application that never issued a read.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain why one read cannot be assumed to equal one message. Compare epoll trigger modes and explain a signal-safe shutdown. Interview bank: POSIX, debugging and IPC.

## Mastery checklist

- Demonstrate fragmented and concatenated messages.
- Bound blocking operations.
- Distinguish EOF, timeout and error.
- Reap children and close unneeded pipe ends.

## Primary references

[READ] read manual. [WRITE] write manual. [EPOLL] epoll_ctl manual. [SIGNAL] signal-safety manual. [PROC] proc_pid_stat manual.
