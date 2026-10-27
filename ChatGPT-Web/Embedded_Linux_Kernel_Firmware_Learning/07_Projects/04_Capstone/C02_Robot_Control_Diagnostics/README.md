# C02 Linux MCU robot control and diagnostics simulation

## Purpose and learning outcome

Demonstrate Linux command generation, MCU-side validity and freshness checks, independent command expiry, latched emergency-stop semantics, differential-drive simulation and fault-oriented acceptance tests. This is an authored learning reference, not evidence of the learner's proficiency. Estimated effort: 40–60 hours plus optional AI work; allow remediation time when a prerequisite fails. Relevant learning modules: M03 M05 M13 M15 M17 M18. The reference skills framework covers this work; no employer-specific JD was supplied.

**Prerequisites:** Complete I05 and C01 concepts; understand differential drive kinematics, state machines, bounded command interfaces and timing evidence.

## Minimum scope and version boundary

Host Linux x86-64, Python 3.12.14; recorded kernel 6.18.55. No board required for the delivered host minimum.

The minimum source is complete for the stated target. Hardware-specific claims and optional integrations are separated from executed host checks. See [VERSIONS.md](VERSIONS.md) and [evidence/STATUS.md](evidence/STATUS.md).

## Architecture and failure handling

The Linux role produces versioned CRC-protected velocity frames every 50 ms. The simulated MCU validates length, version, CRC, speed bounds and sequence freshness, then applies a 200 ms command lifetime. Invalid or repeated commands never refresh the deadline. A local emergency-stop latch forces zero output until deliberate rearm; rearm itself does not enable motion. A 10 ms simulation tick integrates wheel speeds into planar motion. The optional anomaly experiment runs beside this control model and never changes its output.

## Build run debug and cleanup

1. Run `python3 -m unittest discover -s tests -v` using Python 3.12.
2. Run `python3 src/robot.py --output evidence/robot.csv`. The default planner stops transmitting at one second. Inspect the final fresh command at 0.95 s and the first stale state at 1.15 s.
3. Plot time, left/right command and x position from the CSV. The deterministic model stops at approximately 0.345 m in this scripted case; the result assumes instantaneous speed response and is not a physical stopping distance.
4. Run `python3 src/anomaly.py --out evidence/ai` for the optional diagnostic extension. Review the fixed-threshold baseline and learned decision stump on the held-out synthetic test set.
5. Use I05 as the next RTOS implementation target for the MCU role, and C01 for transport diagnostics. Before hardware, add a motor-controller protocol, encoder acquisition, calibrated units and saturation, a real control loop, watchdog reset handling and independently engineered stopping hardware.
6. There are no motor pin assignments in the minimum: it never drives physical motors. Select an actual motor driver and board only after electrical limits, interfaces and safety requirements are known. Do not connect the simulation directly to power hardware.
7. Run config/ci.sh for tests and both evidence generators. Delete only generated evidence/run outputs when resetting experiments.

## Acceptance criteria and evidence

Requirements C02-R1–R9: startup output zero; malformed frame rejected; CRC corruption rejected; command bounds enforced; duplicate does not renew lifetime; sequence wraps correctly; expiry at 200 ms or first subsequent tick forces zero; emergency-stop remains latched across new frames; rearm alone leaves zero. The integrated default scenario must reach STALE at 1.15 s and hold zero afterward.

Nine executed tests cover these invariants plus in-place turning and the full command-loss simulation. They exercise the supplied deterministic software model. No physical braking distance, RTOS scheduling jitter, interrupt latency, electrical fault, functional safety level or industrial compliance is implied.

**Observed validation:** Simulation and acceptance tests passed; 201 time samples were recorded. The optional AI experiment executed and recorded accuracy, confusion matrices, timing, process CPU time, model bytes and memory observations. Physical robot and Linux–MCU transport integration remain explicitly separate work.

## Troubleshooting and limitations

This is a learning demonstrator. A single Python process does not establish isolation between Linux and MCU, and CRC does not authenticate a remote controller. The emergency-stop object is a software state machine, not an independent safety circuit. Mechanical dynamics, wheel slip, motor torque, communication jitter and hazardous failure handling must be engineered and validated before any production use.

If a command fails, record the command, version, first meaningful error, expected behavior and smallest reproducer before changing dependencies. Fix one hypothesis at a time. Keep build failures separate from runtime failures and unavailable hardware.

## Independent exercise

Introduce delayed and reordered command delivery, then show that stale commands cannot resume motion after an outage. Define a safe reset/session handshake. Attempt it before opening [the solution guidance](exercises/SOLUTION.md).

## Demonstration and interview defense

Show the responsibility boundary, inject command loss and a duplicate, demonstrate the stop latch, defend the 200 ms policy as a chosen lab parameter, then explain the hardware evidence still needed.

Be ready to answer: What owns each resource? Which failure first changes the visible state? What did the executed tests actually prove? What remains unverified? How would you reproduce a failure on another machine? A credible portfolio description names the selected environment, your contribution, the actual evidence and remaining limitations; do not claim industrial deployment from a lab simulation.

## Files and references

Source and build files implement the minimum behavior; tests define its acceptance gates; configuration holds target integration data; evidence holds recorded checks. Hardware directories are included only where a board path is meaningful. No hidden source archive is required except explicitly fetched official dependencies. Read [sources.json](sources.json) for primary-source URLs, access date and claims.
