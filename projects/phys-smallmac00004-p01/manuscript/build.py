#!/usr/bin/env python3
"""Clean REVTeX build in a newly created project-relative output directory."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCES=['main.tex','references.bib','certificate-table.tex','rates-table.tex']

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT) or out==ROOT:
        raise SystemExit('Build output must be strictly inside the project/archive root.')
    out.mkdir(parents=True,exist_ok=False)
    for filename in SOURCES:shutil.copyfile(ROOT/'manuscript'/filename,out/filename)
    latex=['pdflatex','-no-shell-escape','-recorder','-interaction=nonstopmode','-halt-on-error','main.tex']
    commands=[latex,['bibtex','main'],latex,latex]
    with (out/'build.log').open('w') as log:
        for command in commands:
            log.write('COMMAND: '+' '.join(command)+'\n');log.flush()
            proc=subprocess.run(command,cwd=out,stdout=log,stderr=subprocess.STDOUT,timeout=90)
            if proc.returncode:raise SystemExit(f'Build failed: see {out}/build.log')
    assert (out/'main.pdf').read_bytes().startswith(b'%PDF-')
    print(json.dumps({'ok':True,'pdf':str((out/'main.pdf').relative_to(ROOT)),
                      'build_log':str((out/'build.log').relative_to(ROOT)),
                      'clean_directory':True}))

if __name__=='__main__': main()
