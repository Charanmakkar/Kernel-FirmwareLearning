#!/usr/bin/env python3
"""Run the package's existing offline Linux host suites from any location.

No downloads, privileged operations, kernel loads, or target emulators occur.
Each invocation creates new aggregate evidence; existing evidence is preserved.
The timing suite checks its existing contracts, not benchmark performance.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import signal
import subprocess
import sys
import time
import uuid


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def suites() -> list[dict]:
    python = sys.executable
    return [
        dict(id="B01", path="07_Projects/01_Basic/B01_C_Utility_Library",
             command=["make", "-B", "test"], tools=["make", "cc"],
             scope="Portable C ring, checked bit updates, CRC and parser tests"),
        dict(id="B02", path="07_Projects/01_Basic/B02_Process_Inspector",
             command=["make", "-B", "test"], tools=["make", "cc", "python3"],
             scope="Linux proc inspection and deterministic malformed-record fixtures"),
        dict(id="B03", path="07_Projects/01_Basic/B03_UART_Framed_Protocol",
             command=["make", "-B", "test"], tools=["make", "cc", "python3"],
             scope="PTY framing, timeout, corruption and terminal restoration including SIGINT, SIGTERM and broken stdout"),
        dict(id="B04", path="07_Projects/01_Basic/B04_Sensor_Logger",
             command=["make", "-B", "test"], tools=["make", "cc", "python3"],
             scope="Pthread queue ordering, finite completion, termination and output-error tests"),
        dict(id="B05", path="07_Projects/01_Basic/B05_Cross_Compile_QEMU",
             command=["make", "-B", "test"], tools=["make", "cc", "python3"],
             scope="Native reference build and boundary/invalid-input tests only"),
        dict(id="I01", path="07_Projects/02_Intermediate/I01_Buildroot_Appliance",
             command=["make", "-B", "test"], tools=["make", "cc", "python3"],
             scope="Native persistence, process-crash checkpoints, concurrency and corruption tests"),
        dict(id="I02", path="07_Projects/02_Intermediate/I02_Kernel_Character_Driver",
             command=["make", "-B", "client"], tools=["make", "cc"],
             scope="Userspace client and fault-test compilation only; no module or device execution"),
        dict(id="I04", path="07_Projects/02_Intermediate/I04_Yocto_Telemetry",
             command=[python, "tests/test_telemetry.py"], tools=["cc"],
             scope="Native telemetry program compilation, output and shutdown test only"),
        dict(id="A01", path="07_Projects/03_Advanced/A01_IIO_Sensor_Driver",
             command=[python, "tests/test_decode.py"], tools=[],
             scope="Independent Python sensor-conversion contract tests; not execution of the kernel C driver"),
        dict(id="A02", path="07_Projects/03_Advanced/A02_Latency_Investigation",
             command=[python, "tests/test_latency.py"], tools=[],
             scope="Existing sampling/recording tests only; durations are not new benchmark claims"),
        dict(id="A03", path="07_Projects/03_Advanced/A03_Signed_AB_Update",
             command=[python, "tests/test_updates.py"], tools=["openssl"],
             scope="Host signed-update state-machine and failure tests with temporary lab keys"),
        dict(id="C01", path="07_Projects/04_Capstone/C01_Industrial_Gateway",
             command=[python, "tests/test_gateway.py"], tools=[],
             scope="Host gateway framing, configuration, health and process integration tests"),
        dict(id="C02", path="07_Projects/04_Capstone/C02_Robot_Control_Diagnostics",
             command=[python, "tests/test_robot.py"], tools=[],
             scope="Deterministic simulated robot state and control-boundary tests"),
        dict(id="M04", path="03_JD_JR_Skills_and_Learning_Content/Modules/M04/lab",
             command=["make", "-B", "test"], tools=["make", "g++"],
             scope="C++17 move-only file-descriptor ownership example build and execution"),
    ]


EXPECTED_SKIPS = [
    dict(id="B01_B04_instrumentation", status="skipped", expected=True,
         reason="Sanitizer targets are separate existing project checks; this portable gate does not require sanitizer runtime support. Retain earlier project instrumentation evidence separately."),
    dict(id="B05_target", status="skipped", expected=True,
         reason="AArch64 toolchain, QEMU execution and remote GDB are outside this offline native gate. Earlier project cross/emulator evidence remains separate."),
    dict(id="I01_image", status="skipped", expected=True,
         reason="Full Buildroot image/toolchain build and full-system guest boot require external sources and target tools."),
    dict(id="I02_I03_kernel", status="skipped", expected=True,
         reason="Kernel compilation, module linking/loading and GPIO board tests require matching external kernel/guest/board environments. No module is loaded by this runner."),
    dict(id="I04_image", status="skipped", expected=True,
         reason="Yocto metadata/image/SDK builds and guest deployment require the external pinned checkout and its dependencies."),
    dict(id="I05_RTOS", status="skipped", expected=True,
         reason="FreeRTOS POSIX and MCU builds require the pinned downloaded RTOS/toolchain; this runner does not download them or require an existing checkout."),
    dict(id="A01_hardware", status="skipped", expected=True,
         reason="Kernel-driver execution and physical sensor/bus behavior are not established by Python conversion tests."),
    dict(id="A02_tracing", status="skipped", expected=True,
         reason="Privileged tracing and performance experiments are not run; existing test-suite timings are functional observations only."),
    dict(id="A03_physical", status="skipped", expected=True,
         reason="Flash partitions, bootloader trust, physical power loss and a hardware secure-boot chain are not exercised by the host simulator."),
    dict(id="C01_C02_target", status="skipped", expected=True,
         reason="RTOS link hardware, physical robot/sensors, image deployment and optional AI experiments remain separate from the existing host suites."),
]


def run_command(command: list[str], cwd: Path, timeout: float) -> dict:
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True,
                               encoding="utf-8", errors="replace",
                               start_new_session=True)
    timed_out = False
    try:
        output, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGTERM)
        try:
            output, _ = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            output, _ = process.communicate()
    return dict(returncode=process.returncode, timed_out=timed_out,
                duration_seconds=round(time.monotonic()-started, 6),
                output=output)


def version(command: list[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        lines = (result.stdout or result.stderr).splitlines()
        return lines[0] if lines else f"exit {result.returncode}"
    except (OSError, subprocess.TimeoutExpired) as error:
        return str(error)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=PACKAGE_ROOT/"10_Progress_Tracking/evidence")
    parser.add_argument("--timeout", type=float, default=120,
                        help="Maximum seconds per existing suite (default 120)")
    parser.add_argument("--label", default="host_package",
                        help="Alphanumeric label recorded in the aggregate filenames")
    args = parser.parse_args()
    if args.timeout <= 0 or not args.label or any(not (c.isalnum() or c in "_-") for c in args.label):
        parser.error("timeout must be positive and label must contain only letters, numbers, underscore or hyphen")
    if sys.platform != "linux":
        parser.error("These projects require Linux proc, PTYs and POSIX behavior; run in the documented Linux host environment")
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc)
    stem = f"{args.label}_{timestamp:%Y%m%dT%H%M%SZ}_{uuid.uuid4().hex[:8]}"
    log_path = output_dir/(stem+".log")
    json_path = output_dir/(stem+".json")
    report = dict(schema_version=1, started_utc=timestamp.isoformat(),
                  package_root=str(PACKAGE_ROOT), label=args.label,
                  scope="Existing offline Linux host suites and selected userspace builds only",
                  network_used=False, privileged_actions=False,
                  timings_are_benchmarks=False,
                  environment=dict(platform=platform.platform(), python=sys.version.split()[0],
                                   compiler=version(["cc", "--version"]),
                                   cpp_compiler=version(["g++", "--version"]),
                                   make=version(["make", "--version"]),
                                   openssl=version(["openssl", "version"])),
                  suites=[], external_and_optional_checks=EXPECTED_SKIPS)
    with log_path.open("x", encoding="utf-8") as log:
        def record(message: str) -> None:
            print(message, flush=True)
            log.write(message+"\n")
            log.flush()
        record(f"Offline host package gate at {timestamp.isoformat()}")
        record(f"Relocatable package root: {PACKAGE_ROOT}")
        record("Suite durations are execution metadata, not performance benchmark results.")
        for spec in suites():
            row = dict(spec)
            row.pop("tools")
            missing = [tool for tool in spec["tools"] if shutil.which(tool) is None]
            directory = PACKAGE_ROOT/spec["path"]
            record(f"\n[{spec['id']}] {spec['scope']}")
            record(f"cwd: {spec['path']}\ncommand: {shlex.join(spec['command'])}")
            if not directory.is_dir():
                row.update(status="failed", reason="Required delivered project directory is missing")
            elif missing:
                row.update(status="skipped", expected=False,
                           reason="Missing host dependency: "+", ".join(missing))
            else:
                try:
                    row.update(run_command(spec["command"], directory, args.timeout))
                    row["status"] = "passed" if row["returncode"] == 0 and not row["timed_out"] else "failed"
                except OSError as error:
                    row.update(status="failed", reason=str(error))
            report["suites"].append(row)
            record(row.get("output", row.get("reason", "")).rstrip())
            record(f"Result: {row['status']}")
        record("\nExplicitly skipped external or optional portions")
        for item in EXPECTED_SKIPS:
            record(f"{item['id']}: SKIPPED — {item['reason']}")
        counts={state:sum(row["status"]==state for row in report["suites"])
                for state in ["passed", "failed", "skipped"]}
        report["summary"]=dict(host_suites=counts,
                               expected_external_skips=len(EXPECTED_SKIPS))
        report["finished_utc"]=datetime.now(timezone.utc).isoformat()
        report["exit_code"]=1 if counts["failed"] else (2 if counts["skipped"] else 0)
        record("\nHost summary: "+json.dumps(counts))
        record("Expected external/optional skips: "+str(len(EXPECTED_SKIPS)))
        record(f"Aggregate JSON: {json_path.name}")
    with json_path.open("x", encoding="utf-8") as output:
        json.dump(report,output,indent=2,ensure_ascii=False)
        output.write("\n")
    print(f"Evidence: {json_path}\nLog: {log_path}", flush=True)
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
