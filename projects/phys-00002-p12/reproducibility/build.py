"""Clean local build using an existing TeX installation; installs nothing."""
import argparse
import pathlib
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
root = pathlib.Path(__file__).resolve().parents[1]
out = pathlib.Path(args.output).resolve()
if out.exists() and any(out.iterdir()):
    raise SystemExit("Output directory must be empty")
out.mkdir(parents=True, exist_ok=True)
for name in ("main.tex", "references.bib"):
    shutil.copy2(root / "manuscript" / name, out / name)
commands = [
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ["bibtex", "main"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
]
with (out / "build-command.log").open("w") as log:
    for command in commands:
        log.write("COMMAND: " + " ".join(command) + "\n")
        log.flush()
        subprocess.run(command, cwd=out, stdout=log, stderr=subprocess.STDOUT, check=True)
print(out / "main.pdf")
