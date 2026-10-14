"""Clean local TeX/BibTeX build without changing scientific inputs.

From the project root:
  python3 reproducibility/build_manuscript.py --build-dir build/clean-example
The destination must be empty. No tools are installed and no network is used.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-dir", required=True)
    args = parser.parse_args()
    destination = (ROOT / args.build_dir).resolve()
    if not destination.is_relative_to(ROOT / "build"):
        raise ValueError("Build destination must be inside the project's build directory")
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError("A clean build requires an empty destination; choose a fresh name")
    for name in ("pdflatex", "bibtex", "pdfinfo", "pdftotext"):
        if shutil.which(name) is None:
            raise RuntimeError(f"Required installed tool unavailable: {name}")
    tex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
           "-file-line-error", "-recorder",
           f"-output-directory={destination}", "manuscript/main.tex"]
    # BibTeX's standard openout_any=p requires a relative output filename.
    bibtex_target = str(destination.relative_to(ROOT) / "main")
    commands = [tex, ["bibtex", bibtex_target], tex, tex]
    transcript = []
    results = []
    for command in commands:
        # REVTeX creates mainNotes.bib in the clean output directory.
        # Make that local generated database visible without changing TeX's
        # output-security settings or copying it into the source tree.
        build_env = os.environ.copy()
        build_env["BIBINPUTS"] = str(destination) + ":" + str(ROOT) + ":" + build_env.get("BIBINPUTS", "")
        result = subprocess.run(command, cwd=ROOT, env=build_env,
                                capture_output=True)
        transcript.append(("COMMAND: " + " ".join(command) + "\n").encode() +
                          result.stdout + result.stderr)
        results.append({"command": command, "exit_code": result.returncode})
        (destination / "build-driver.log").write_bytes(b"\n".join(transcript))
        if result.returncode != 0:
            print((result.stdout + result.stderr).decode("utf-8", errors="replace"), file=sys.stderr)
            raise RuntimeError(f"Build command failed: {command[0]}")
    pdf = destination / "main.pdf"
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True)
    (destination / "pdfinfo.txt").write_text(info.stdout + info.stderr)
    subprocess.run(["pdftotext", "-layout", str(pdf), str(destination / "main.txt")], check=True)
    summary = {"build_directory": str(destination.relative_to(ROOT)),
               "empty_destination_at_start": True, "commands": results,
               "pdf": str(pdf.relative_to(ROOT)),
               "compiler_log": str((destination / "main.log").relative_to(ROOT)),
               "driver_log": str((destination / "build-driver.log").relative_to(ROOT)),
               "scientific_inputs_modified": False,
               "scope": "Writer build only; fresh release audits remain required."}
    (destination / "build-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
