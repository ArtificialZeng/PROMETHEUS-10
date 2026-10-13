#!/usr/bin/env python3
"""Build the manuscript in a new local directory using installed TeX tools."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import time

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", default="build/clean", help="new project-relative directory")
args = parser.parse_args()
out = root / args.output
if Path(args.output).is_absolute() or ".." in Path(args.output).parts:
    raise SystemExit("Output must be inside this project")
if out.exists():
    raise SystemExit("Output already exists; choose a new directory for a clean build")
out.mkdir(parents=True)
for name in ("main.tex", "references.bib"):
    shutil.copy2(root / "manuscript" / name, out / name)
commands = [
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
    ["bibtex", "main"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
]
start = time.monotonic()
with (out / "build-transcript.log").open("w") as log:
    for command in commands:
        log.write("COMMAND " + " ".join(command) + "\n")
        log.flush()
        result = subprocess.run(command, cwd=out, stdout=log, stderr=subprocess.STDOUT, timeout=120)
        log.write("EXIT " + str(result.returncode) + "\n")
        log.flush()
        if result.returncode:
            raise SystemExit("Build failed; see " + str(out / "build-transcript.log"))
pdf = out / "main.pdf"
record = {
    "commands": commands,
    "output": str(out.relative_to(root)),
    "started_with_absent_output_directory": True,
    "elapsed_seconds": time.monotonic() - start,
    "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    "source_sha256": {n: hashlib.sha256((root / "manuscript" / n).read_bytes()).hexdigest()
                      for n in ("main.tex", "references.bib")},
    "scope": "Build execution only; compiler-log and visual review are separate checks."
}
(out / "build-execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record))
