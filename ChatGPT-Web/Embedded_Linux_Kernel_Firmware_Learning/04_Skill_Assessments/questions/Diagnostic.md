# Initial diagnostic

**ID D00. Prerequisites:** none beyond access to a Linux shell and C compiler. **Time:** 90 minutes. **Allowed tools:** local compiler, editor, man pages; no AI, internet answers, or reference solutions. **Purpose:** find starting gaps. If setup is unavailable, answer on paper and mark every execution item pending rather than inventing results.

Submit one directory with `answers.md`, C source, command transcript, test output, and a short confidence/evidence table. Each item below is worth the stated points, totaling 100.

1. **D01 8 points:** explain the lifetime bug in `char *f(void) { char b[4]="ok"; return b; }`; propose two valid ownership contracts and their tradeoffs.
2. **D02 8 points:** classify `INT_MAX+1`, `UINT_MAX+1u`, and two unsequenced increments of one variable. State assumptions rather than guessing output.
3. **D03 12 points:** write checked `size_t` multiplication. Test `(0,SIZE_MAX)`, `(SIZE_MAX,1)`, `(SIZE_MAX,2)`, and null output. Failure must leave output unchanged.
4. **D04 8 points:** in a temporary directory, create a text file, show permissions, redirect stderr separately, locate lines matching `ERROR`, and record a Git commit in a temporary repository. Do not use a user's existing repository.
5. **D05 8 points:** explain why one write of 100 bytes may require several reads, and show how a writer tracks partial progress. Include EINTR, EOF, and EAGAIN distinctions.
6. **D06 10 points:** repair `if (count==0) pthread_cond_wait(&cv,&mu); take_item();` for multiple consumers and shutdown. State the lock and predicate invariants.
7. **D07 8 points:** describe a representative board boot chain and distinguish Linux application processors from MCU firmware. Name the assumptions needing board documentation.
8. **D08 8 points:** decide whether a hard-IRQ handler may take a mutex, allocate with GFP_KERNEL, or perform a sleeping bus transaction. Explain a suitable deferred design and configuration caveats.
9. **D09 8 points:** explain how an RTOS task and ISR exchange a completed DMA buffer without either overwriting data still owned by the other.
10. **D10 8 points:** using `fixtures/spin.trace`, identify one supported hypothesis and one unsupported conclusion. Propose a fix and a regression test.
11. **D11 7 points:** distinguish CRC, signed update verification, and verified boot. Give a failure each one does not solve alone.
12. **D12 7 points:** explain one real project or a clearly labeled practice task: requirement, your work, a failure, verification, and a remaining limitation. Do not invent experience.

**Interpretation:** use subtopic evidence. Below 60: prioritize M01–M05 and B01; 60–79: repair failed foundations before track depth; 80 or above: attempt the target track's phase gate. These ranges are planning aids, not a proficiency score for untested topics. Any critical bounds, lifetime, synchronization, trust, or truthfulness failure requires remediation regardless of total. Retake only after explaining and testing the correction.
