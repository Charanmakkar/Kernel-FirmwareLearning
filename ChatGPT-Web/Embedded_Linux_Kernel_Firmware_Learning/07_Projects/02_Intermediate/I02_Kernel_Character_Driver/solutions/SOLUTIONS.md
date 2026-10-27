# I02 Exercise solutions

The blocked writer can make progress once space exists, but another writer may take it first. After wakeup it must recheck under the mutex. A positive partial return, possibly one byte, is legal for this byte stream; callers must loop. For hot unplug, separate hardware ownership from open-file state, mark the device removed under synchronization, stop new opens, wake sleepers, return a specified error/hangup, and retain the file-visible state until its last reference is released. Managed allocation alone does not protect open users after remove. The static module example intentionally avoids that more complex lifetime contract.

Compare the result with the complete original implementation in `src/`. Passing the supplied tests is one piece of evidence; explain the change without reading this solution before marking the skill demonstrated.
