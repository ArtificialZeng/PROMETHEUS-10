#!/usr/bin/env python3
"""Build in a new, empty directory using an existing local TeX installation."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output-dir", default="build/manuscript")
args = parser.parse_args()
out = (ROOT / args.output_dir).resolve()
if not out.is_relative_to(ROOT) or out == ROOT:
    raise SystemExit("Output must be a subdirectory of the project.")
out.mkdir(parents=True, exist_ok=True)
if any(out.iterdir()):
    raise SystemExit("Use a new empty output directory for a clean build.")
for name in ("main.tex", "references.bib"):
    shutil.copyfile(ROOT / "manuscript" / name, out / name)
environment = os.environ.copy()
environment["SOURCE_DATE_EPOCH"] = "1789171200"
commands = [
    ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
    ["bibtex", "main"],
    ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
    ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-recorder", "main.tex"],
]
with (out / "build-transcript.log").open("w") as log:
    for command in commands:
        log.write("$ " + " ".join(command) + "\n")
        log.flush()
        result = subprocess.run(command, cwd=out, env=environment, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise SystemExit("Build failed; inspect " + str(out / "build-transcript.log"))
print(out.relative_to(ROOT) / "main.pdf")
