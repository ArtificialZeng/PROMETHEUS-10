#!/usr/bin/env python3
"""Build the manuscript into a new local directory; never delete an older build."""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build/write-clean",
                        help="New project-relative build directory")
    args = parser.parse_args()
    relative = Path(args.output)
    if relative.is_absolute() or ".." in relative.parts:
        parser.error("--output must stay inside the project")
    out = ROOT / relative
    if out.exists() and any(out.iterdir()):
        parser.error("--output already contains files; choose a new directory")
    out.mkdir(parents=True, exist_ok=True)
    command = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
               "-file-line-error", "-recorder", "-outdir=" + str(out), "main.tex"]
    started = datetime.now(timezone.utc).isoformat()
    run = subprocess.run(command, cwd=ROOT / "manuscript", capture_output=True, text=True)
    (out / "build-command.log").write_text(
        "Command: " + json.dumps(command) + "\n"
        "Working directory: " + str(ROOT / "manuscript") + "\n"
        "Started UTC: " + started + "\n\n" + run.stdout + run.stderr,
        encoding="utf-8")
    (out / "build-command.json").write_text(json.dumps({
        "command": command, "working_directory": str(ROOT / "manuscript"),
        "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(),
        "returncode": run.returncode,
        "pdf": relative.as_posix() + "/main.pdf",
        "compiler_log": relative.as_posix() + "/main.log"
    }, indent=2) + "\n", encoding="utf-8")
    if run.returncode:
        raise SystemExit(run.returncode)
    pdf = out / "main.pdf"
    if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
        raise SystemExit("No valid PDF was generated")
    print(json.dumps({"pdf": str(pdf.relative_to(ROOT)), "returncode": run.returncode}))

if __name__ == "__main__":
    main()
