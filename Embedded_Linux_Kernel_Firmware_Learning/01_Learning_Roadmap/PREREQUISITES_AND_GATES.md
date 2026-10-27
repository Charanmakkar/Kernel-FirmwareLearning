# Prerequisite map and competence gates

```text
D01 diagnostic
  +--> C lifetime, byte arithmetic, compiler/debugger --> B01
  |      +--> POSIX files/processes --> B02 --> B03 protocol
  |      +--> threads/ownership --> B04
  +--> architecture/ELF/toolchains --> B05 --> I01 Buildroot
          +--> contexts/locking/driver model --> I02 --> I03 --> A01
          +--> image metadata/packages --> I04 Yocto
  +--> MCU startup/peripheral state machines --> I05 RTOS/protocol
B04 + I02 --> A02 latency investigation
I01 + boot/persistence/keys --> A03 updates
B03 + I01 + I05 + A03 --> C01 gateway
B03 + I05 + A02 + C01 integration methods --> C02 simulated robot
```

Study deeply: pointer/object lifetime, integer bounds, error contracts, shared-data ownership, execution context, resource lifetime and state transitions. Implement immediately: byte decoding, bounded queues, file I/O loops, shutdown, packaging and recovery tests. Recognize initially: page-table levels, RCU read-side principles, DMA coherency, verified boot trust chains. Defer advanced architecture-specific barriers, new scheduler algorithms, complex bus controllers and ML accelerators until the actual JD asks for them.

| Gate | Required evidence | Pass rule | If failed |
|---|---|---|---|
| G0 prerequisite | D01 independent attempt + explanation | >=70/100 overall, C>=15/25 and Linux>=12/20, no critical memory/concurrency misconception | Spend 2 weeks on M01 and Linux file/process labs; retake different data |
| G1 safe C | B01 tests + unseen parser/ring change + M01 exit | >=80/100; no out-of-bounds, lifetime violation, unchecked length or fabricated output | Reproduce failing invariant, add regression, explain failure; retest independently |
| G2 Linux user space | B02–B04 artifacts + syscall and thread review | Partial I/O, errors, timeouts and shutdown all defended; >=80 | Rebuild a single-producer queue and bounded poll loop before adding features |
| G3 platform | B05/I01 boot and cross-debug record | Independently identify ELF ABI, loader, kernel/rootfs/init and persist config across reboot | Trace boot stage by stage and compare known-good configs |
| G4 kernel | I02/I03 guest/hardware evidence + locking review | No sleep-in-atomic, unsafe user dereference or lifetime race; >=80 | Draw each callback context and cleanup dependency; add failure injection |
| G5 firmware | I05 simulation plus specified MCU evidence | Bounded queues, watchdog policy and timeout-to-safe-state demonstrated | Measure one task and one interrupt path; simplify ownership and task graph |
| G6 integration | A01–A03 acceptance reports | Measurement reproducible; recovery tested; signature failure rejected | Repeat the specific fault with recorded build IDs; no average-score waiver |
| G7 portfolio | C01/C02 defense + final practical | Fresh reproduction, honest scope, failure test and independent explanation | Fix missing evidence before resume claim; focused mock interview |

An authored solution does not satisfy a gate. Grade correctness 30, reasoning 15, debugging method 15, resource handling 10, concurrency/timing 10, tests 10, communication 10. Critical failures block passage irrespective of average: memory unsafety; uncontrolled actuator behavior; sleeping in hard-IRQ context; secret exposure; bypassed signature checks; claiming unexecuted tests passed. Non-applicable categories are declared before the assessment and their points reassigned to correctness/testing, not silently granted.

## Shorter role paths

**Minimum readiness after foundations: 12 weeks, about 132 hours.** Weeks 1–2: D01/G1 remediation and B01. Weeks 3–4: B02/B03 partial I/O and protocol. Weeks 5–6: B04 concurrency and B05 ELF/cross build. Weeks 7–8: EL chooses I01; KD chooses the complete I02 driver before adding hardware; FW chooses I05 after a startup/peripheral lab. Weeks 9–10: timed practical, failure injection and code review. Weeks 11–12: targeted mock interviews, fresh reproduction and portfolio defense. This is a narrow junior interview path, not evidence of all three tracks, BSP bring-up or production firmware expertise. If foundations fail, add prerequisite weeks instead of compressing them.

**A 9–12-month single-track path:** work through shared weeks 1–18, select the role's depth work, finish one relevant capstone and revise. Keep the other projects planned in the 15-project catalog. The 64-week complete path retains all projects; branch priorities change order, not the catalog's counts.

Weekly 11-hour rhythm: 2 hours concept/source reading; 5 hours implementation/testing; 1 hour debugging notes; 1 hour independent assessment; 1 hour spaced review/mock answers; 1 hour contingency. Allocate 10–12 based on real availability. Every fourth week revisit two old questions and one old bug using different input data. Missed gates move subsequent milestones; calendar time is not competence.
