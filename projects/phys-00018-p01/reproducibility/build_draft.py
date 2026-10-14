"""Clean local manuscript build with real command logs and TeX recorder."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", default="build/write-clean")
    args = parser.parse_args()
    out = (ROOT / args.outdir).resolve()
    if ROOT not in out.parents:
        raise SystemExit("Build directory must be inside the source package.")
    if out.exists() and any(out.iterdir()):
        raise SystemExit("Choose a new empty output directory for a clean build.")
    out.mkdir(parents=True, exist_ok=True)
    for tool in ("pdflatex", "bibtex"):
        if not shutil.which(tool):
            raise SystemExit(f"Required existing tool unavailable: {tool}")
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "-recorder", f"-output-directory={out}",
             "manuscript/main.tex"]
    with (out / "commands.log").open("w") as log:
        for command in [latex, ["bibtex", str((out / "main").relative_to(ROOT))], latex, latex]:
            log.write(json.dumps({"command": command}) + "\n")
            log.flush()
            subprocess.run(command, cwd=ROOT, stdout=log,
                           stderr=subprocess.STDOUT, check=True)
    print(json.dumps({"clean_build_completed": True,
                      "pdf": str((out / "main.pdf").relative_to(ROOT)),
                      "log": str((out / "commands.log").relative_to(ROOT))}))


if __name__ == "__main__":
    main()
