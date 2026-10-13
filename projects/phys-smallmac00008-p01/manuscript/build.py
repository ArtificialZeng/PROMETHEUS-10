#!/usr/bin/env python3
"""Clean foreground REVTeX build; all outputs stay within this project."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', default='build/manuscript',
                    help='New project-relative build directory; never overwritten.')
args = parser.parse_args()
OUT = (ROOT / args.output).resolve()
if ROOT not in OUT.parents:
    raise SystemExit('Output must be a directory inside the project.')
if OUT.exists():
    raise SystemExit('Refusing to reuse an existing build directory; choose a new --output.')
OUT.mkdir(parents=True)
for name in ('main.tex', 'references.bib'):
    shutil.copy2(ROOT / 'manuscript' / name, OUT / name)
commands = [
    ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-recorder', 'main.tex'],
    ['bibtex', 'main'],
    ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-recorder', 'main.tex'],
    ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-recorder', 'main.tex'],
]
with (OUT / 'build-transcript.log').open('w') as log:
    for command in commands:
        log.write('$ ' + ' '.join(command) + '\n')
        log.flush()
        run = subprocess.run(command, cwd=OUT, stdout=log, stderr=subprocess.STDOUT)
        if run.returncode:
            raise SystemExit('Build failed; inspect ' + str(OUT/'build-transcript.log'))
subprocess.run(['pdftotext', '-layout', str(OUT/'main.pdf'), str(OUT/'main.txt')], check=True)
info = subprocess.run(['pdfinfo', str(OUT/'main.pdf')], capture_output=True, text=True, check=True)
(OUT/'pdfinfo.txt').write_text(info.stdout)
print(json.dumps({'status':'compiled', 'pdf':str((OUT/'main.pdf').relative_to(ROOT)),
                  'compiler_log':str((OUT/'main.log').relative_to(ROOT)),
                  'transcript':str((OUT/'build-transcript.log').relative_to(ROOT))}))
