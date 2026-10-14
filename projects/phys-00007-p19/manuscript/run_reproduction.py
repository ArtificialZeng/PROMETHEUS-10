#!/usr/bin/env python3
"""Replay the selected existing programs in a new isolated directory.

Never run the original scripts in the accepted project root: they write outputs.
This wrapper copies only code and four defining input files before execution.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "code/reproduce_full_qubit_a.py",
    "code/reproduce_schmidt_b.py",
    "code/compare_reconstructions.py",
    "code/research_recoupling.py",
    "code/research_four_support_a.py",
    "code/research_four_support_b.py",
    "code/research_verify_four_support.py",
    "code/research_fidelity_compare.py",
]
INPUTS = [
    "evidence/reproduce-20261012-input-a.json",
    "evidence/reproduce-20261012-input-b.json",
    "evidence/research-20261012-four-support-input-a.json",
    "evidence/research-20261012-four-support-input-b.json",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", default=sys.executable, help="Interpreter with the recorded dependencies")
    parser.add_argument("--output", default="build/reproduction", help="New output directory, relative to package root")
    args = parser.parse_args()
    out = (ROOT / args.output).resolve()
    if not out.is_relative_to(ROOT) or out == ROOT:
        parser.error("The output must be a new directory inside the package root")
    out.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for name in SCRIPTS + INPUTS:
        src = ROOT / name
        dst = out / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        hashes[name] = hashlib.sha256(src.read_bytes()).hexdigest()
    runs = []
    report = {
        "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": args.python,
        "copied_input_and_code_hashes": hashes,
        "runs": runs,
        "scope": "Manuscript reproduction in a copied tree; no fresh scientific acceptance.",
    }
    for i, name in enumerate(SCRIPTS, 1):
        start = time.monotonic()
        result = subprocess.run(
            [args.python, name], cwd=out, capture_output=True, text=True, timeout=180
        )
        log = out / f"step-{i:02d}.log"
        log.write_text(result.stdout + result.stderr)
        runs.append({
            "script": name, "exit_code": result.returncode,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "log": str(log.relative_to(ROOT)),
        })
        report["all_scripts_passed"] = all(r["exit_code"] == 0 for r in runs)
        (out / "reproduction-report.json").write_text(json.dumps(report, indent=2) + "\n")
        print(f"{i}/{len(SCRIPTS)} {name}: exit {result.returncode}", flush=True)
        if result.returncode:
            return result.returncode
    report["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (out / "reproduction-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
