# Timed coding tests

Each test is independent and uses C11 on the host unless explicitly stated. Allowed tools are compiler, editor, local man pages, debugger and sanitizers; no AI or answer keys. Submit source, commands, results and a short explanation. Pass at 75/100 with no critical failure. Apply correctness 30, reasoning 15, debugging 15, resource handling 10, state handling 10, tests 10, communication 10.

## C15 Checked conversion in 15 minutes

Prerequisites M02–M03. Implement `parse_u32` from Q028 with strict decimal grammar and unchanged output on failure. Inputs: empty, `0`, `4294967295`, `4294967296`, `12x`, `-1`, ` 1`. Record exact expected outputs before running. Extension only after the minimum passes: accept a separate explicit base parameter. Exit evidence is a strict-warning build and boundary tests. Remediation: integer conversion and precondition checks in M02, then repeat with uint16_t.

## C30 Ring buffer in 30 minutes

Prerequisites M03. Implement capacity eight FIFO push/pop with full/empty rejection, no heap, and unchanged state after failed operations. Fill 0–7; reject 8; pop three; push 8–10; drain expected 3–10; reject an empty pop. State whether concurrent use is supported. Do not add unrequested lock-free behavior. Remediation: draw head/tail/count after each step, then repeat at capacity three.

## C60 Fragmented protocol in 60 minutes

Prerequisites M03 and M06. Implement a streaming decoder for one-byte type, one-byte length and up to 16 payload bytes. It must accept arbitrary fragmentation and multiple records per chunk; reject lengths above 16; reset by explicit API after a malformed header. Inputs in fragments.json plus an empty chunk, a 16-byte payload, and length 17. Return consumed length and complete frames without overrunning output. The reset rule deliberately does not claim automatic resynchronization. Tests must exercise every split of one valid frame. Remediation: state diagrams and remaining-length invariants, then add a delimiter-based recovery extension only after the minimum passes.

## C90 Bounded queue in 90 minutes

Prerequisites M07. Write a POSIX producer/consumer queue of capacity four with one producer, one consumer, 100 numbered items, and drain-on-shutdown. No item accepted before shutdown may be lost or duplicated. Stop once while empty and once while full using synchronization barriers rather than sleeps. Join threads before destroying queue storage. Test termination within a specified two-second host test deadline; this is a test bound, not a real-time guarantee. Remediation: condition-variable predicates and cancellation wake paths.

## C60F Firmware state logic in 60 minutes

Prerequisites M12–M13. Implement Q164 robot states with events ARM, DISARM, COMMAND, TIMEOUT, FAULT, CLEAR. Start DISARMED; timeout disarms; FAULT latches; ARM cannot clear it; CLEAR returns to DISARMED. Output permission must be false unless ARMED. Use a table-driven test of every state/event pair and a wraparound deadline test. No real motor output is required. Remediation: explicit transitions and stale-command policy; retake with a new RECOVERY state and documented allowed transitions.
