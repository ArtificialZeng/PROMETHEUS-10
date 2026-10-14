#!/usr/bin/env python3
"""Build the draft from a fresh, project-local staging directory.

No network, installation or manuscript modification is performed.
Compiler and bibliography output are retained for the later release review.
"""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "build" / "write-538487f99b86"
DEST.mkdir(parents=True, exist_ok=True)
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
stage = DEST / ("clean-" + stamp)
stage.mkdir(exist_ok=False)
inputs = [ROOT / "manuscript" / "main.tex", ROOT / "manuscript" / "references.bib"]
for src in inputs:
    shutil.copyfile(src, stage / src.name)

commands = [
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-recorder", "main.tex"],
    ["bibtex", "main"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-recorder", "main.tex"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-recorder", "main.tex"],
]
log = DEST / "build.log"
records = []
with log.open("w") as handle:
    for command in commands:
        handle.write("COMMAND: " + " ".join(command) + "\n")
        handle.flush()
        result = subprocess.run(command, cwd=stage, stdout=handle,
                                stderr=subprocess.STDOUT, timeout=90)
        records.append({"command": command, "returncode": result.returncode})
        if result.returncode:
            print(json.dumps({"ok": False, "log": str(log.relative_to(ROOT)),
                              "stage": str(stage.relative_to(ROOT)),
                              "commands": records}))
            sys.exit(result.returncode)
for name in ["main.pdf", "main.log", "main.bbl", "main.blg", "main.fls"]:
    shutil.copyfile(stage / name, DEST / name)
record = {
    "ok": True,
    "clean_stage": str(stage.relative_to(ROOT)),
    "source_copies": [{"source": str(p.relative_to(ROOT)),
                        "copy": str((stage / p.name).relative_to(ROOT)),
                        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                        "byte_identical": p.read_bytes() == (stage / p.name).read_bytes()}
                       for p in inputs],
    "commands": records,
    "pdf": str((DEST / "main.pdf").relative_to(ROOT)),
    "pdf_sha256": hashlib.sha256((DEST / "main.pdf").read_bytes()).hexdigest(),
    "compiler_log": str((DEST / "main.log").relative_to(ROOT)),
    "command_log": str(log.relative_to(ROOT)),
    "note": "Writing-stage build record; fresh release audits remain required."
}
(DEST / "build-record.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record))
