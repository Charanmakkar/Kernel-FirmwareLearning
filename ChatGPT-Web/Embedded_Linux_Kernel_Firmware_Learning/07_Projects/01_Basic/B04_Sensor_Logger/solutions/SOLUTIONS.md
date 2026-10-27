# B04 Exercise solutions

Per-producer ordering and exactly-once delivery must remain true for the original blocking policy; global interleaving is unspecified. A drop-oldest policy must update head and count under the same mutex and increment a loss counter. Sequence gaps expose loss per producer, but a final total dropped count is also needed to account for data lost after the last delivered sequence. Report policy and loss counters in the output schema. It is incorrect to remove the full-queue wait and overwrite data without recording the change in behavior. Retain the original implementation for comparison and benchmark under the same flush policy.

Compare the result with the complete original implementation in `src/`. Passing the supplied tests is one piece of evidence; explain the change without reading this solution before marking the skill demonstrated.
