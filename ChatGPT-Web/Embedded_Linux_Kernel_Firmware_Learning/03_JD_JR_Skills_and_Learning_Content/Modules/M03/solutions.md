# M03 reference solution and reasoning

Keep parser state, buffered count and a deadline based on a monotonic clock. On timeout discard the incomplete frame and restart prefix search. Reject unsupported versions according to the published resynchronization rule; do not trust their payload length without a bound. Test that every call consumes input or returns a defined need-more state. Sequence handling belongs to a session with reset rules. A fixed-size buffer bounds memory independently of corrupted lengths.
