# B05 Exercise solutions

The dynamic ELF names an AArch64 loader. An empty sysroot cannot supply it, so loader discovery fails before main. Confirm the interpreter with readelf and restore the toolchain sysroot. A 32-bit unsigned accumulator wraps modulo 2^32; N=1,000,000 must return 500000500000 and will reveal the bug. Unsigned wrap is defined arithmetic, but it violates this application's numerical contract. A compiler warning or sanitizer need not detect every incorrect choice of numeric range. Restore uint64_t and keep the boundary test.

Compare the result with the complete original implementation in `src/`. Passing the supplied tests is one piece of evidence; explain the change without reading this solution before marking the skill demonstrated.
