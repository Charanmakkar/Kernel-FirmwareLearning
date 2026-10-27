# B02 Linux process and resource inspector

Create a command-line inspector that turns a process's Linux `/proc` records into one JSON report. It reads the name, state, thread count, resident memory, CPU ticks, and number of open file descriptors. Plan 8–10 hours after M01, M02, M05, and M06. This project provides evidence for Linux file I/O, error handling, command-line design, data parsing, and debugging.

## Outcomes and acceptance

Produce valid JSON for a live process and deterministic fixtures, reject malformed PIDs, preserve a process name containing spaces and parentheses, and exit with failure if required process records disappear. Understand that `/proc` is a kernel-provided view, and its individual files do not form one atomic snapshot. Missing optional resident-memory data is `-1`; an unreadable descriptor directory is also `-1`. These values mean unavailable, never zero usage.

## Environment and structure

Use Linux with a mounted `/proc`, GCC, Make, and Python 3 for tests. No external Python modules or hardware are needed. `src/inspect.c` is complete; `tests/test_inspect.py` creates isolated fixtures and exercises real `/proc/self`. `VERSIONS.md` and `evidence/` record validation. There is no driver, board configuration, or wiring component.

## Architecture and data flow

The CLI validates the PID before constructing paths. It reads named fields in `status`, then locates the final right parenthesis in `stat` before numbering fields from the state field. Splitting the entire stat line on whitespace would misparse a command name containing spaces. User and kernel CPU ticks are fields 14 and 15; the report includes `_SC_CLK_TCK` so a caller can convert ticks to seconds. [Linux proc stat documentation](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html).

The file-descriptor count is a separate directory enumeration. For `self`, opening the enumeration directory itself can affect the observed count; do not use it as an exact historical count. A process may terminate between reads, and access can be restricted by permissions, namespaces, or proc mount policy. The tool returns an explicit error rather than inventing a consistent snapshot.

## Guided run and investigation

```sh
make test
./build/inspect self
./build/inspect 1
gdb --args ./build/inspect self
```

The second invocation prints JSON. The PID 1 invocation can succeed or be denied depending on the host; that environmental result is informative. Compare a successful report to `/proc/PID/status` immediately, allowing for process changes. Calculate `(user_ticks + system_ticks) / ticks_per_second` as accumulated CPU seconds. It is not CPU utilization; utilization needs two samples over elapsed time and a stated normalization convention.

In GDB, break after the stat line is read and inspect the point returned by `strrchr`. Use the test fixture with a command containing `)` to justify using the last closing parenthesis. Deliberately remove the fixture `stat` file between runs and explain the failure path. `--root PROC_ROOT PID` is explicitly a testing interface; it must point to trusted fixtures when used by privileged code.

Run `make clean` to remove the build output. Do not stop or modify another process as part of this project.

## Test plan and troubleshooting

The automated suite tests live self-inspection, invalid and overflowing PID strings, JSON escaping of quotes, parenthesized and spaced names, exact CPU counter mapping, malformed records, and absent process directories. A nonzero return during inspection of a short-lived process can be a normal race. A negative RSS field for a kernel thread means unavailable. If JSON parsing fails, inspect escaping and accidental diagnostics on standard output; errors belong on standard error.

The implementation is a bounded educational inspector, not a complete process accounting tool. It does not provide RSS accounting across shared pages, cgroup limits, historical samples, CPU percentages, or process identity stability across PID reuse. An extension should retain a start-time identity and use pidfds where appropriate, without claiming that a pidfd turns all proc reads into an atomic transaction.

## Independent practice and defense

Attempt the separate exercises before reading their solutions. In a five-minute demonstration, show live output, run the tricky-name fixture, explain one permission failure, and calculate CPU seconds. Interview questions: Why is parsing `stat` with `%s` unsafe? What changes between two proc reads? Why is RSS different from virtual size? What does `-1` mean in this interface? State exactly which fields are required and which are optional.

## Primary references

- [Linux process stat fields](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html)
- [Linux process status fields](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)

Access date: 27 October 2026.
