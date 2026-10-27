# Cancellation cleanup defect and correction

Independent review exercised SIGTERM while a request was waiting for a response. The initial implementation restored termios on normal errors, but the default signal action terminated the process before its cleanup label. The PTY remained in raw mode. This was an actual observed defect, not an intentionally broken exercise.

The corrected single-threaded client catches SIGINT, SIGTERM and SIGHUP with a minimal handler that records a sig_atomic_t cancellation value. The ordinary polling loop notices cancellation and returns through cleanup. Restoring termios retries EINTR. SIGPIPE is ignored so a broken stdout pipe is reported through the write error path. No allocation, stdio or termios work occurs inside the handler.

The regression test waits until the PTY has received the outgoing request, then sends SIGINT or SIGTERM and compares the complete original terminal attributes with the post-exit attributes. A separate test closes the stdout pipe reader before responding and verifies cleanup after EPIPE. All these cases passed in the final host_tests.log. SIGKILL and a terminal device that has disappeared cannot be made recoverable by a user-space handler.

Interview lesson: cleanup implemented as a common return path does not imply that asynchronous process termination reaches that path. Identify the termination contract and test it explicitly.
