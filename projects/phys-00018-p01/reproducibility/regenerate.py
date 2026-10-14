"""Optional full certificate regeneration in a fresh local work directory."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "evidence/research-pass2/joint_stationary.py",
    "evidence/research-pass3/palm_and_coercivity.py",
    "evidence/research-pass3/l2_gram.py",
    "evidence/research-pass4/riesz_residual.py",
    "evidence/research-pass4/check_riesz_exact.py",
]


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    work = ROOT / "build" / f"full-regeneration-{stamp}"
    work.mkdir(parents=True, exist_ok=False)
    for rel in SCRIPTS:
        dest = work / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dest)
    spec = importlib.util.spec_from_file_location("parent_generation", work / SCRIPTS[1])
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    # Generate the parents without the historical n16 exploratory branches.
    for d in (1, 2):
        parent.parent(d)
    commands = [
        [sys.executable, str(work / SCRIPTS[2]), "--basis", "64",
         "--RNA-cap", "48", "--protein-cap", "128"],
        [sys.executable, str(work / SCRIPTS[3]), "--basis", "32"],
        [sys.executable, str(work / SCRIPTS[3]), "--basis", "48"],
        [sys.executable, str(work / SCRIPTS[4])],
    ]
    for index, command in enumerate(commands, 1):
        with (work / f"step-{index}.log").open("w") as log:
            subprocess.run(command, cwd=work, check=True,
                           stdout=log, stderr=subprocess.STDOUT)
    print(json.dumps({"output_directory": str(work.relative_to(ROOT)),
                      "completed": True,
                      "meaning": "New approximants with exact certificate signs checked."}))


if __name__ == "__main__":
    main()
