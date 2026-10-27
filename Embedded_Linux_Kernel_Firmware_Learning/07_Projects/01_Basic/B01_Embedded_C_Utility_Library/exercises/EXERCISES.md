# B01 independent exercises — answers separate

Prerequisites M01 and a normal verification pass. Allow 60 minutes, editor/compiler/debugger and API header; no AI or reference implementation. Work in a copy/branch. Deliver source diff, tests and a short invariant explanation. Score behavior 40, boundary tests 25, resource/alias reasoning 20, communication 15; pass >=80 and no unsafe access.

E01: add `eu_ring_peek(const eu_ring *r, uint8_t *out)` that returns the oldest byte without removing it. Invalid arguments yield EU_INVALID; empty yields EU_EMPTY; out and ring remain unchanged on failure. Test capacity one, wrapped state and empty. Do not solve by popping then pushing.

E02: add `eu_packet_payload_sum(const eu_packet *packet, uint32_t *out)` with explicit length checking and unchanged output on failure. Payload bytes sum as unsigned values; no CRC recomputation. Test zero bytes, all 64 bytes equal 255, length 65, and null parameters.

E03 debugging: change the ring full test to `count == capacity - 1`. Predict the affected capacity-one behavior before execution, reproduce a minimal failure, fix it, and explain why the original model test detects it.

Then retest one week later with a different API: peek the newest byte without removal. Independent retention matters more than remembering this solution.
