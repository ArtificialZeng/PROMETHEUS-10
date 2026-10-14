"""Replay the local clock calculation in a new, isolated working directory.

Existing frozen evidence is never overwritten. No package installation or network
access is performed. Use an interpreter with the packages in requirements.txt.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SUITES = {
    "baseline": [
        "scripts/reproduce_input_a.py",
        "scripts/reproduce_input_b.py",
        "scripts/compare_reproduction.py",
    ],
    "algebra": [
        "scripts/research_symbolic_curvature.py",
        "scripts/check_curvature_sign.py",
        "scripts/check_local_variation_exact.py",
    ],
    "independent": [
        "reproducibility/independent_symbolic.py",
        "reproducibility/independent_direct.py",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path,
                        help="New output directory; it must not already exist.")
    parser.add_argument("--suite", choices=[*SUITES, "all"], default="all")
    args = parser.parse_args()
    target = args.output.resolve()
    if target.exists() or target == ROOT or target in ROOT.parents:
        parser.error("Choose a new output directory distinct from the source tree.")
    target.mkdir(parents=True, exist_ok=False)
    for folder in ["scripts", "evidence", "logs"]:
        (target / folder).mkdir()
    packages = {name: importlib.metadata.version(name)
                for name in ["numpy", "scipy", "sympy", "mpmath"]}
    chosen = list(SUITES) if args.suite == "all" else [args.suite]
    files = [p for suite in chosen for p in SUITES[suite]]
    manifest = {
        "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version,
        "executable": sys.executable,
        "libraries": packages,
        "suite": args.suite,
        "source_hashes": {},
        "commands": [],
        "interpretation": "Reproduction only; does not issue scientific or release acceptance.",
    }
    for relative in files:
        source = ROOT / relative
        destination = target / "scripts" / source.name
        shutil.copyfile(source, destination)
        manifest["source_hashes"][relative] = hashlib.sha256(source.read_bytes()).hexdigest()
    exit_code = 0
    for relative in files:
        basename = Path(relative).name
        command = [sys.executable, "scripts/" + basename]
        start = time.monotonic()
        result = subprocess.run(command, cwd=target, capture_output=True, text=True)
        log = "logs/" + Path(basename).stem + ".log"
        (target / log).write_text(result.stdout + result.stderr)
        manifest["commands"].append({
            "command": command,
            "returncode": result.returncode,
            "elapsed_seconds": time.monotonic() - start,
            "log": log,
        })
        print(json.dumps(manifest["commands"][-1]), flush=True)
        if result.returncode:
            exit_code = result.returncode
            break
    manifest["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest["exit_code"] = exit_code
    (target / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
