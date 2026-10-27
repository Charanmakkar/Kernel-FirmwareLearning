# M02 reference solution and reasoning

Reject used > capacity first, then test input_length > capacity - used so the check itself cannot overflow. Validate pointers under the stated zero-length convention. If overlap is supported, use memmove; otherwise document and detect only what is safely detectable without invalid pointer comparisons. Update used only after a successful copy. Concurrency requires serialized access or appropriate atomics; volatile does not make the compound increment indivisible.
