#!/usr/bin/env python3
"""Clean, foreground LaTeX/BibTeX build; no download or installation."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='build/write-clean')
args = parser.parse_args()
out = (ROOT / args.output).resolve()
if ROOT not in out.parents:
    raise SystemExit('Output must be inside the project.')
out.mkdir(parents=True, exist_ok=True)
if any(out.iterdir()):
    raise SystemExit('A clean build requires an empty output directory.')
for name in ('main.tex', 'references.bib'):
    shutil.copyfile(ROOT / 'manuscript' / name, out / name)
commands = [
    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
    ['bibtex', 'main'],
    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
    ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
]
records = []
for i, cmd in enumerate(commands, 1):
    run = subprocess.run(cmd, cwd=out, text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, timeout=120)
    log = out / ('pass-%02d.log' % i)
    log.write_text(run.stdout)
    records.append({'command': cmd, 'returncode': run.returncode,
                    'log': str(log.relative_to(ROOT))})
    (out / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
    if run.returncode:
        print(run.stdout[-6000:])
        raise SystemExit(run.returncode)
final = (out / 'main.log').read_text()
bad = [line for line in final.splitlines()
       if any(term in line for term in
              ('Undefined control sequence', 'undefined references',
               'undefined citations', 'There were undefined', 'LaTeX Error:',
               'Overfull', 'Underfull'))]
info = subprocess.run(['pdfinfo', str(out / 'main.pdf')], text=True,
                      capture_output=True, check=True)
(out / 'pdfinfo.txt').write_text(info.stdout)
subprocess.run(['pdftotext', '-layout', str(out / 'main.pdf'),
                str(out / 'main.txt')], check=True)
print(json.dumps({'pdf': str((out / 'main.pdf').relative_to(ROOT)),
                  'commands_passed': len(records),
                  'final_log_diagnostics': bad}, indent=2))
if bad:
    sys.exit(2)
