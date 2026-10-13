#!/usr/bin/env python3
"""Build the article from copied sources in a fresh directory inside the project."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--build-dir", default="build",
                    help="Project-relative directory; default: build")
args = parser.parse_args()
base = (root / args.build_dir).resolve()
if root != base and root not in base.parents:
    parser.error("The build directory must be inside the project.")
base.mkdir(parents=True, exist_ok=True)
clean = Path(tempfile.mkdtemp(prefix="clean-", dir=base))
for name in ("main.tex", "references.bib"):
    shutil.copyfile(root / "manuscript" / name, clean / name)
env = dict(os.environ)
env["SOURCE_DATE_EPOCH"] = "1789171200"  # 2026-09-12 00:00:00 UTC
env["FORCE_SOURCE_DATE"] = "1"
commands = [
    ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode",
     "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
    ["bibtex", "main"],
    ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode",
     "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
    ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode",
     "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
]
with (clean / "commands.log").open("w") as log:
    for command in commands:
        log.write("$ " + " ".join(command) + "\n")
        log.flush()
        run = subprocess.run(command, cwd=clean, env=env, stdout=log,
                             stderr=subprocess.STDOUT, timeout=120)
        if run.returncode:
            raise SystemExit("Build failed; see " + str(clean / "commands.log"))
for name in ("main.pdf", "main.log", "main.bbl", "main.blg",
             "main.fls", "commands.log"):
    shutil.copyfile(clean / name, base / name)
record = {
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "clean_directory": str(clean.relative_to(root)),
    "commands": commands,
    "source_date_epoch": env["SOURCE_DATE_EPOCH"],
    "source_hashes": {
        "manuscript/" + name: hashlib.sha256((clean / name).read_bytes()).hexdigest()
        for name in ("main.tex", "references.bib")
    },
    "pdf_sha256": hashlib.sha256((base / "main.pdf").read_bytes()).hexdigest(),
    "final_log_sha256": hashlib.sha256((base / "main.log").read_bytes()).hexdigest(),
}
(base / "build-record.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
