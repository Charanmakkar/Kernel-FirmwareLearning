# Kernel device acceptance plan

Prerequisite: complete matching guest kernel and module build, saved VM snapshot, root access only inside guest. Allow 90 minutes. Tools allowed: compiler, Python, strace, dmesg, GDB and kernel documentation. Independent first pass; AI assistance must be recorded separately. Deliver exact guest versions, commands, test output and before/after kernel logs.

| Test | Expected result | Points |
|---|---|---|
| Automated device test | Zero lengths, EAGAIN, partial write, poll, blocking wake and 1 MiB stream pass | 35 |
| Two simultaneous writers and one reader | No corruption/loss; no claim of per-record atomicity | 15 |
| Interrupt blocked reader with a non-restarting signal handler | Interrupted syscall or documented restart behavior; no locked mutex leak | 10 |
| User buffer entirely PROT_NONE | EFAULT, no byte consumed when no byte can copy | 10 |
| User buffer crossing writable and inaccessible pages | Positive copied prefix where the uaccess helper reports partial copy; retained bytes consistent | 10 |
| Unload with open fd | Normal rmmod fails busy; closes then unload succeeds | 10 |
| Repeat load/unload and inspect logs | No new warning, oops, leak evidence, or stuck task | 10 |

Pass at 80/100 with no kernel warning, crash, deadlock, unexpected data loss, or unsafe forced unload. A failed gate requires root-cause evidence and a regression test. Modules_prepare/object build alone scores zero runtime points. Do not run this plan against the host kernel shared with other work.
