#!/usr/bin/env python3
"""Replay the supplied exact checks without using handoffs or audit records."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build/reproduction",
                        help="Project-relative output directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (root / args.output).resolve()
    if not output.is_relative_to(root):
        parser.error("The output directory must remain inside this project.")
    output.mkdir(parents=True, exist_ok=True)
    cases = [
        ("n2_equality_symbolic.py", "n2-equality-symbolic.log"),
        ("equality_geometry_certificate.py", "equality-geometry-certificate.log"),
        ("general_q_local_certificate.py", "general-q-local-certificate.log"),
    ]
    records = []
    for script, expected in cases:
        directory = root / "evidence/research"
        result = subprocess.run([sys.executable, str(directory / script)],
                                cwd=root, capture_output=True, timeout=180)
        (output / expected).write_bytes(result.stdout)
        (output / (expected + ".stderr")).write_bytes(result.stderr)
        matches = result.stdout == (directory / expected).read_bytes()
        record = {
            "script": "evidence/research/" + script,
            "returncode": result.returncode,
            "matches_preserved_output": matches,
            "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
        }
        records.append(record)
        print(json.dumps(record), flush=True)
        if result.returncode != 0 or not matches:
            (output / "summary.json").write_text(json.dumps(records, indent=2) + "\n")
            return 1
    (output / "summary.json").write_text(json.dumps(records, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
