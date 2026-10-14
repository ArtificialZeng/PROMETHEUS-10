#!/usr/bin/env python3
"""Replay certificates in an isolated project-local directory."""
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
stage = root / "replay-work"
if stage.exists():
    raise SystemExit("replay-work exists; retain or move it before a new replay")
(stage / "evidence").mkdir(parents=True)
scripts = [
    "interval-survival-check.py", "finite_survival.py", "barrier_cover.py",
    "interval_survival.py", "antecedent_exclusion.py",
    "independent_survival_check.py", "independent_exclusion_check.py",
]
inputs = ["barrier-cover-result.json", "antecedent-exclusion-result.json"]
for name in scripts + inputs:
    shutil.copy2(root / "evidence" / name, stage / "evidence" / name)
for name in scripts:
    log = stage / "evidence" / (name + ".replay.log")
    with log.open("w") as output:
        result = subprocess.run(
            [sys.executable, str(stage / "evidence" / name)],
            cwd=stage, stdout=output, stderr=subprocess.STDOUT,
        )
    print(f"{name}: exit {result.returncode}; {log.relative_to(root)}", flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
