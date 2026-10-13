#!/usr/bin/env python3
"""Replay the supplied exact calculations in a new, isolated local directory."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "reproduction/input_a.py",
    "reproduction/input_b.py",
    "reproduction/check_physics_inputs.py",
    "research/exhaustive_certificate.py",
    "research/independent_replay.py",
    "supplement/phase_replay.py",
    "supplement/affine_replay.py",
]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", default="replay-output", help="new directory inside the package root")
args = parser.parse_args()
relative = Path(args.output)
if relative.is_absolute() or ".." in relative.parts:
    raise SystemExit("Output must be a relative path inside the package root")
work = ROOT / relative
if work.exists():
    raise SystemExit("Output already exists; choose another directory to preserve earlier evidence")
work.mkdir(parents=True)
for directory in ("evidence", "generated", "logs"):
    (work / directory).mkdir()
for name in SCRIPTS:
    target = work / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, target)
environment = dict(os.environ)
environment.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
start = time.monotonic()
commands = []
for index, name in enumerate(SCRIPTS, 1):
    logfile = work / "logs" / (str(index) + "-" + Path(name).stem + ".log")
    command = [sys.executable, name]
    with logfile.open("w") as stream:
        result = subprocess.run(command, cwd=work, env=environment,
                                stdout=stream, stderr=subprocess.STDOUT, timeout=180)
    commands.append({"script": name, "exit_code": result.returncode,
                     "log": str(logfile.relative_to(work)),
                     "log_sha256": hashlib.sha256(logfile.read_bytes()).hexdigest()})
    print(json.dumps(commands[-1]), flush=True)
    if result.returncode:
        (work / "execution.json").write_text(json.dumps({"status": "failed", "commands": commands}, indent=2) + "\n")
        raise SystemExit(result.returncode)
record = {"status": "completed", "commands": commands,
          "elapsed_seconds": time.monotonic() - start,
          "single_foreground_process_at_a_time": True,
          "script_sha256": {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in SCRIPTS},
          "scope": "Executable reproducibility check; no new scientific acceptance or human review is asserted."}
(work / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"status": record["status"], "elapsed_seconds": record["elapsed_seconds"],
                  "record": str((work / "execution.json").relative_to(ROOT))}))
