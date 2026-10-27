# B03 Exercise solutions

The stale response is consumed and ignored; the original absolute deadline remains. Restarting the deadline after any received byte lets noise keep the application alive indefinitely. The supplied resync test already includes sequence 99. For sequence 2, use one request-sequence variable, pass it to response matching instead of hardcoding 1, and parameterize the Python frame expectation. Check both stale and matching frames. For a persistent client, add bounded pending transactions and a wraparound policy; simply incrementing a 16-bit field does not handle replies that survive a wrap.

Compare the result with the complete original implementation in `src/`. Passing the supplied tests is one piece of evidence; explain the change without reading this solution before marking the skill demonstrated.
