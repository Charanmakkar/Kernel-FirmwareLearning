# M01 Linux tools and reproducible engineering

## Objectives and prerequisites

Prerequisites: none.

Find files and logs confidently, compile a program, preserve a change in Git and capture enough context for someone else to reproduce a failure.

## Lesson


A compiler transforms source into object code; a linker resolves references between objects and libraries. An executable can still fail before `main` if its interpreter or shared libraries are unavailable. Treat source, compiler flags, target architecture and runtime libraries as one reproducibility record. A successful compile proves neither execution nor correct behavior.

On Linux, pathnames and file descriptors are different things. A pathname locates an object when a system call resolves it. A file descriptor is an integer handle in one process. Standard input, output and error normally use descriptors 0, 1 and 2. Redirect stdout into a data file and stderr into a log so machine-readable results remain parseable. A shell exit status of zero conventionally reports success; capture it before another command replaces `$?`.

Start with `pwd`, `ls -l`, `rg --files`, `rg pattern path`, `head`, `tail`, `less`, `find`, `stat`, `df -h`, `du -sh` and `ps`. `chmod` changes permission bits; `chown` changes ownership. Directory execute permission controls traversal. Permissions are checked using credentials and access policy; writing code that works only as root masks integration errors. Learn `systemctl status`, `journalctl -u` and `dmesg` as different observation tools for services and kernel messages; availability and permissions depend on the host.

Use Git to store meaningful changes. Inspect `git diff` before committing, name the behavioral change, and include its test. A branch is a movable reference, not a copy of every file. `git bisect` narrows the first bad commit only when the pass/fail test is reliable. Never mark an untestable revision good. For an unfamiliar repository, read its README and build instructions, inspect configuration and run a known test before making changes. [GIT]

Make expresses dependency relationships. If a header affects an object, the dependency graph must record it; otherwise an incremental build can differ from a clean build. A one-line shell script that ignores a failed compile can accidentally run yesterday's binary. Use explicit status checks, quote paths and remove or isolate stale outputs. In Bash, `set -eu` helps but is not a replacement for understanding command, pipeline and conditional behavior.


## Worked lab and expected behavior


In B01, run `make test` and inspect the command and test output. Then run the compiler directly on a small independent example:

```sh
printf '%s\n' '#include <stdio.h>' \
  'int main(void) { puts("ready"); return 0; }' > hello.c
gcc -std=c11 -Wall -Wextra -Wpedantic -Werror -g hello.c -o hello
./hello > result.txt
file hello
readelf -h hello
```

Expected behavior is one `ready` line and a host-architecture ELF executable. These are acceptance expectations, not fabricated execution logs. If `gcc` is missing, fix the tool installation. If the program cannot execute, inspect architecture, loader path, mount permissions and shared libraries before editing C code. Introduce a missing semicolon and confirm the compiler failure prevents a new executable. Then restore and commit the fix plus the observed error explanation.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

Explain why an old executable can run after a failed build. Explain file permissions on directories. Defend how your commit can be reproduced. Interview bank: build/tooling questions linked to M01.

## Mastery checklist

- Reproduce a clean build from source.
- Separate program data from error logs.
- Explain one compiler and one runtime failure.
- Review a diff before committing.

## Primary references

[GIT] Git official tutorial. [GCC-WARN] GCC warning options. [LD] GNU linker scripts.
