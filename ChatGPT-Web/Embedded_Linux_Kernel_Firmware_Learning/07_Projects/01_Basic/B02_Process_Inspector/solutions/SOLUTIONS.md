# B02 Exercise solutions

For matching process identity, CPU seconds used between snapshots equal delta ticks divided by ticks_per_second. Divide by monotonic elapsed seconds and multiply by 100 for one-core-equivalent percent; a multithreaded process can exceed 100. Retain the stat starttime identity and reject differing identities. The exact time interval is measured, not assumed from sleep duration. A process disappearing is a rejected sample pair. The optional fd field should become -1 without fabricating zero; the required status/stat fields must still validate. Testing permissions as root can defeat a chmod-only fixture, so run that test as an unprivileged account or inject the directory-open failure through a test abstraction.

Compare the result with the complete original implementation in `src/`. Passing the supplied tests is one piece of evidence; explain the change without reading this solution before marking the skill demonstrated.
