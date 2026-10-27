# M02 independent exercise

Timebox 60 minutes. Write a bounded buffer append API with capacity, used length and input length. Preserve the existing buffer on rejected input. Test exact fit, one-byte overflow, empty input, size overflow and overlapping source/destination. State whether overlap is supported. Then explain why volatile int counter; counter++ is not thread-safe.
