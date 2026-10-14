#!/usr/bin/env python3
"""Build with latexmk into a new, project-local output directory."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", default="build/clean-v1")
args = parser.parse_args()
destination = (ROOT / args.output_dir).resolve()
if not destination.is_relative_to(ROOT / "build"):
    raise SystemExit("Output directory must be inside this project's build/")
destination.mkdir(parents=True, exist_ok=True)
if any(destination.iterdir()):
    raise SystemExit("A clean build requires a new empty output directory.")
command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
           "-file-line-error", "-recorder", "-outdir="+str(destination), "main.tex"]
result = subprocess.run(command, cwd=ROOT / "manuscript", text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(destination / "compiler-console.log").write_text(result.stdout)
(destination / "build-command.json").write_text(json.dumps({
    "command":command, "cwd":"manuscript", "returncode":result.returncode,
    "clean_output_directory":True,
    "source_policy":"Compiler reads the canonical manuscript sources; no source copies or scientific inputs are rewritten."
}, indent=2)+"\n")
print(result.stdout[-6000:])
raise SystemExit(result.returncode)
