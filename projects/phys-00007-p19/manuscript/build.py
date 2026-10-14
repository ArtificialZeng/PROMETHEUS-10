#!/usr/bin/env python3
"""Build the complete manuscript in a fresh local directory without installation."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build/manuscript", help="New directory inside the package root")
    args = parser.parse_args()
    out = (ROOT / args.output).resolve()
    if not out.is_relative_to(ROOT) or out == ROOT:
        parser.error("The output must be a new directory inside the package root")
    out.mkdir(parents=True, exist_ok=False)
    for name in ["main.tex", "references.bib"]:
        shutil.copy2(ROOT / "manuscript" / name, out / name)
    command = ["latexmk", "-pdf", "-recorder", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "main.tex"]
    result = subprocess.run(command, cwd=out, capture_output=True, text=True, timeout=180)
    (out / "build-driver.log").write_text(result.stdout + result.stderr)
    report = {"command": command, "exit_code": result.returncode,
              "pdf": str((out / "main.pdf").relative_to(ROOT)),
              "log": str((out / "main.log").relative_to(ROOT)),
              "driver_log": str((out / "build-driver.log").relative_to(ROOT)),
              "scope": "Writer build; fresh release audit is still required."}
    (out / "build-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
