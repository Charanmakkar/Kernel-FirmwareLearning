# Capstone requirements and acceptance design

These are authored requirements and proposed test criteria, not executed results. The two capstones will reuse earlier components but add integration, versioned contracts, failure boundaries and fresh acceptance evidence. All tests currently pending.

## C01 — Manageable industrial gateway

Scope: one MCU or simulator sending one sensor stream at 10 Hz over one serial framing protocol to one Linux service. The gateway stores bounded JSON-line telemetry, persistent configuration and an observable health snapshot. A 10 Hz rate is a design target, not measured capability. Remote cloud, dashboards and multiple fieldbuses are extensions.

| ID | Requirement and rationale | Acceptance input and expected result |
|---|---|---|
| C01-R1 | One versioned serial communication path; all frames length/CRC checked | 100 nominal fixture frames plus corruption; only valid frames counted and errors observed |
| C01-R2 | Fresh/stale/disconnected states based on monotonic time | Stop sender; stale within configured 500 ms plus declared scheduling margin; reconnect requires compatible session |
| C01-R3 | Persistent config schema version with range validation | Restart preserves accepted config; unknown version/bad range leaves previous accepted config active |
| C01-R4 | Durable replacement policy | Inject stop before/after write, file fsync, rename and directory fsync; restart selects valid old/new config, never malformed content |
| C01-R5 | Bounded resource consumption | Fixture overload for 30 minutes; queue/log bounds maintained; consumed+dropped/error accounting reconciled |
| C01-R6 | Observable health | Health output names build/protocol/session, last valid sample age, dropped frames, queue utilization and update state |
| C01-R7 | Signed update and health-gated activation | Wrong signature/target rejected; unhealthy candidate exhausts attempts and returns to known-good slot |
| C01-R8 | Automated integration regression | Fresh isolated test setup runs nominal, bad CRC/version, link loss, disk-full, config-corruption and interrupted-update cases |
| C01-R9 | Honest reproduction and defense | New checkout reproduces accepted behavior; report identifies reused/supplied and learner-authored components and physical gaps |

Durability depends on filesystem/storage guarantees; file+directory fsync is a designed protocol to test on selected storage, not a universal promise against defective hardware. Do not add networking before these core requirements pass. Planned integration adds health-state policy, persistence and update semantics beyond a serial demo.

## C02 — Simulated robot with explicit Linux/MCU boundary

Linux owns goals/planning/diagnostics. MCU owns a 100 Hz control state machine, bounded output, command lease, watchdog progress and safe transition. A deterministic plant supplies wheel/state measurements. No real motors are connected. Proposed periods and thresholds below are requirements to evaluate in simulation and later re-establish on hardware.

| ID | Requirement and rationale | Acceptance input and expected result |
|---|---|---|
| C02-R1 | Explicit states INIT, DISARMED, ARMED, FAULT | Outputs zero until initialization and explicit arm conditions hold; no startup actuation |
| C02-R2 | Command lease max 200 ms in MCU monotonic domain | Linux exit/link loss expires lease; command setpoint becomes zero within one 10 ms control tick after expiry in deterministic simulation |
| C02-R3 | Bounded and versioned commands | Out-of-range, malformed, unknown version, replayed/stale sequence rejected; defined wrap and reset-epoch semantics |
| C02-R4 | Independent control cadence | Add Linux delays and slow optional inference; MCU control scheduling decisions unchanged in the deterministic model |
| C02-R5 | Sensor freshness and overrun fault | Freeze sensor or exceed configured control budget; latch FAULT and zero command; controlled explicit recovery only |
| C02-R6 | Diagnostic evidence | Timestamp state transitions and accepted/rejected commands; test output includes source/build/config/seed |
| C02-R7 | Testable simulated dynamics | Known stationary/straight/turn inputs meet specified model invariants; integration tests expose overshoot/error rather than inventing motion accuracy |
| C02-R8 | Optional AI does not alter safety boundary | Missing/slow/invalid score falls back to deterministic threshold diagnostic; commands never depend on inference completion |
| C02-R9 | Declared production gaps | Document real sensor latency, actuator inertia, electrical limits, independent e-stop, hazard analysis, power behavior and physical timing tests still required |

Zero command is a software state, not proof of physical stopping distance or safety certification. Hardware integration is a separate stage requiring actual motor driver, encoder, current/voltage limits, mechanical rig and an independently reviewed stop path. Keep simulation results separate from measurements on NUCLEO-F446RE and any Linux board.
