#!/usr/bin/env python3
"""Clean, serial LaTeX/BibTeX build; execute from any working directory."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'manuscript'
BUILD = ROOT / 'build'


def main():
    BUILD.mkdir(exist_ok=True)
    # Only this script's generated outputs are removed. Authored inputs stay intact.
    for suffix in ['aux', 'bbl', 'blg', 'log', 'out', 'pdf', 'fls', 'toc']:
        (BUILD / ('main.' + suffix)).unlink(missing_ok=True)
    commands = [
        ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
         '-halt-on-error', '-file-line-error', '-recorder',
         '-output-directory=' + str(BUILD), 'main.tex'],
        ['bibtex', 'main'],
    ]
    commands += [commands[0], commands[0]]
    transcript = []
    runs = []
    for cmd in commands:
        env = os.environ.copy()
        if cmd[0] == 'bibtex':
            env['BIBINPUTS'] = str(SOURCE) + os.pathsep + env.get('BIBINPUTS', '')
        cwd = BUILD if cmd[0] == 'bibtex' else SOURCE
        run = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True,
                             timeout=90)
        transcript.append('$ ' + ' '.join(cmd) + '\n' + run.stdout + run.stderr)
        runs.append({'command': cmd, 'returncode': run.returncode})
        (BUILD / 'compile.log').write_text('\n'.join(transcript))
        if run.returncode:
            raise SystemExit('Build failed; inspect build/compile.log')
    info = subprocess.run(['pdfinfo', str(BUILD / 'main.pdf')],
                          capture_output=True, text=True, check=True)
    (BUILD / 'pdfinfo.txt').write_text(info.stdout)
    subprocess.run(['pdftotext', '-layout', str(BUILD / 'main.pdf'),
                    str(BUILD / 'main.txt')], check=True)
    record = {
        'built_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'clean_outputs_removed_before_build': True,
        'runs': runs,
        'tools': {name: shutil.which(name) for name in
                  ['pdflatex', 'bibtex', 'pdfinfo', 'pdftotext']},
        'source_sha256': {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
                          for name in ['main.tex', 'graph.tex', 'references.bib']},
        'pdf_sha256': hashlib.sha256((BUILD / 'main.pdf').read_bytes()).hexdigest(),
    }
    (BUILD / 'build-record.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
