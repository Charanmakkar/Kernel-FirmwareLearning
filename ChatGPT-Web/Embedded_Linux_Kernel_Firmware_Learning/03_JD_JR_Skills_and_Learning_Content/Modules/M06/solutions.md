# M06 reference solution and reasoning

Maintain used length and scan each received chunk for delimiters. Append only within the bound. On overflow, either reject the whole stream or discard through the next delimiter under a documented policy. EOF is a state transition; handle the last partial record explicitly. Retry EINTR with the same absolute deadline. On nonblocking EAGAIN wait for readiness. Close every owned descriptor on all exit paths.
