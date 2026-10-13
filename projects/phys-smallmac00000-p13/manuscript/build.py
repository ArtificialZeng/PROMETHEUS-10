#!/usr/bin/env python3
"""Build the article into a new, empty local directory. No installation or upload."""
from pathlib import Path
import argparse
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
source = Path(__file__).resolve().parent
output = args.out.resolve()
if output.exists() and any(output.iterdir()):
    parser.error("A clean build requires an empty or nonexistent output directory.")
output.mkdir(parents=True, exist_ok=True)
command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
           "-file-line-error", "-recorder", "-outdir=" + str(output), "main.tex"]
with (output / "latexmk.log").open("w") as log:
    run = subprocess.run(command, cwd=source, stdout=log, stderr=subprocess.STDOUT)
print("Build log:", output / "latexmk.log")
if run.returncode:
    raise SystemExit(run.returncode)
print("PDF:", output / "main.pdf")
