# Timed coding answer key

C15 expected: empty rejected; `0` accepted as 0; maximum accepted; overflow, trailing text, sign and whitespace rejected. Failure preserves the previous output. Reference: coding_reference.c parse_u32, Q028. Critical failure: an overflowing intermediate or accepting a partial parse as complete.

C30 expected: after filling count is eight; ninth push leaves it eight; after three pops head is zero, tail three, count five; wraparound writes retain FIFO; final drain yields 3 through 10 exactly once. Reference: ring_push/ring_pop, Q023. Critical failure: full/empty ambiguity or storage access outside capacity.

C60 expected: parse header and payload in separate states, cap length before payload writes, preserve partial state, and reset to header state only by the documented explicit reset after invalid length. Empty chunk consumes zero. A complete zero-length record is emitted immediately after its header. Unknown type may be structurally accepted by this exercise. The answer is not allowed to silently claim recovery from arbitrary junk without a framing rule. Reference implementation: streaming_reference.c. Critical failure: any input writes beyond 16 bytes or an invalid length causes unbounded buffering.

C90 expected: mutex protects head, tail, count and stop. Producer waits while full and not stopped; consumer waits while empty and not stopped, and exits only when stopped and empty. Both predicates loop. Shutdown broadcasts. No thread is joined while the joining thread holds the queue mutex. See Q069 and the B04 project for a complete queue integration. Score independently from the delivered reference; actual candidate tests remain required.

C60F expected: FAULT event from any state enters FAULT; CLEAR only changes FAULT to DISARMED; ARM changes DISARMED to ARMED and leaves ARMED armed; timeout/disarm disable nonfault states; command cannot arm; fault state ignores arm/command/timeout except explicit clear. Reference: control_step and tick_due. Critical failure: any path allows motion in FAULT or re-arms solely because a command arrived.

For all tests, use the 100-point rubric and critical gates. Award tests points for independent expected values and boundary coverage, not merely calling the function many times. An unfinished optional extension must not erase a complete minimum solution, but document it rather than claiming it passed.
