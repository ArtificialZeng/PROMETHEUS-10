"""Replay existing consistency code in an isolated project build directory.

The original frozen scripts and outputs are never overwritten. This executes
ordinary scientific Python, not an agent or a background worker.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "general_variation_check.py": "6008825a458dbb6a45d40338728a268a9c59944e6f219ac1a10122147090cba9",
    "sinusoidal.py": "2225b54d725cecc62d5cfdef2dcc6e37e3e49e847832d6f285d426ffd294ce45"
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True,
                        help="A new empty directory below build/")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if not output.is_relative_to(ROOT / "build"):
        raise ValueError("Replay destination must be inside build/")
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Choose an empty replay directory")
    for name, expected in EXPECTED.items():
        original = ROOT / "evidence/research" / name
        if hashlib.sha256(original.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Accepted script hash changed: {name}")
        shutil.copyfile(original, output / name)
    result = subprocess.run([sys.executable, str(output / "general_variation_check.py")],
                            cwd=ROOT, capture_output=True, text=True)
    (output / "replay.log").write_text(result.stdout + result.stderr)
    print(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError("Consistency replay failed; inspect the preserved actual log")
    data = json.loads((output / "general-variation-check.json").read_text())
    if not data["passed_attack_checks"]:
        raise RuntimeError("Numerical attacks failed")
    print(json.dumps({"output": str(output.relative_to(ROOT)),
                      "original_evidence_unmodified": True,
                      "interpretation": "Finite numerical consistency check; not a certificate or a referee verdict."}))


if __name__ == "__main__":
    main()
