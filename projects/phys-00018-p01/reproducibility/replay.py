"""Replay supplied certificates in a new local directory, preserving inputs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILES = [
    "evidence/research-pass4/check_riesz_exact.py",
    "evidence/research-pass3/l2-gram-n64-exact.json",
    "evidence/research-pass3/l2-gram-n64-results.json",
    "evidence/research-pass3/palm-delta1-S64.json",
    "evidence/research-pass3/palm-delta2-S64.json",
    "evidence/research-pass3/l2-certificate-n64-B1-contraction.json",
    "evidence/research-pass3/l2-certificate-n64-B2_transpose-contraction.json",
] + [
    f"evidence/research-pass4/riesz-d{d}-n{n}-exact.json"
    for n in (32, 48) for d in (1, 2)
] + [
    f"evidence/research-pass4/riesz-n{n}-results.json" for n in (32, 48)
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    work = ROOT / "build" / f"certificate-replay-{stamp}"
    work.mkdir(parents=True, exist_ok=False)
    before = {p: sha(ROOT / p) for p in INPUT_FILES}
    for rel in INPUT_FILES:
        target = work / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, target)
    with (work / "replay.log").open("w") as log:
        run = subprocess.run([sys.executable, str(work / INPUT_FILES[0])],
                             cwd=work, stdout=log, stderr=subprocess.STDOUT,
                             timeout=1800)
    preserved = before == {p: sha(ROOT / p) for p in INPUT_FILES}
    record = {"exit_code": run.returncode, "inputs_preserved": preserved,
              "input_sha256": before, "log": "replay.log",
              "meaning": "Replay of supplied data; not a fresh scientific audit."}
    (work / "replay-record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"exit_code": run.returncode, "inputs_preserved": preserved,
                      "output_directory": str(work.relative_to(ROOT))}))
    if run.returncode or not preserved:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
