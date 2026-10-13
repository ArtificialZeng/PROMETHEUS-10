"""Build the manuscript in a clean, project-local staging directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    out=root / "build"
    stage=out / "clean"
    out.mkdir(exist_ok=True)
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir()
    for name in ["main.tex", "references.bib"]:
        shutil.copyfile(root / "manuscript" / name, stage / name)
    shutil.copytree(root / "manuscript" / "figures", stage / "figures")
    env=os.environ.copy()
    env["SOURCE_DATE_EPOCH"]="1789171200"
    env["FORCE_SOURCE_DATE"]="1"
    tex=["pdflatex","-no-shell-escape","-interaction=nonstopmode","-halt-on-error","-file-line-error","-recorder","main.tex"]
    commands=[tex,["bibtex","main"],tex,tex]
    with (out / "commands.log").open("w") as log:
        for cmd in commands:
            log.write("COMMAND "+json.dumps(cmd)+"\n");log.flush()
            p=subprocess.run(cmd,cwd=stage,env=env,stdout=log,stderr=subprocess.STDOUT)
            if p.returncode:
                raise SystemExit(f"Build failed; inspect {out / 'commands.log'}")
    for name,target in [("main.pdf","main.pdf"),("main.log","build.log"),
                        ("main.bbl","main.bbl"),("main.blg","bibliography.log"),
                        ("main.fls","dependencies.fls")]:
        shutil.copyfile(stage / name,out / target)
    extraction=subprocess.run(["pdftotext","-layout",str(out / "main.pdf"),str(out / "main.txt")],capture_output=True,text=True)
    extraction.check_returncode()
    info=subprocess.run(["pdfinfo",str(out / "main.pdf")],capture_output=True,text=True,check=True)
    (out / "pdfinfo.txt").write_text(info.stdout)
    print(info.stdout)
    print("PDF SHA-256",hashlib.sha256((out / "main.pdf").read_bytes()).hexdigest())

if __name__ == "__main__":
    main()
