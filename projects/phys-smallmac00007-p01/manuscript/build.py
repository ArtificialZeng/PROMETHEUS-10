#!/usr/bin/env python3
"""Stage and build the article in an empty local directory; no shell escape."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='build/local')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out = Path(args.output).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit('Clean build requires a new or empty output directory.')
    out.mkdir(parents=True, exist_ok=True)
    for rel in ['main.tex', 'references.bib', 'figures/bias-gap.pdf']:
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / rel, dst)
    commands = [
        ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
        ['bibtex', 'main'],
        ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
        ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
    ]
    records = []
    for index, command in enumerate(commands, 1):
        result = subprocess.run(command, cwd=out, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        name = 'step-{}-{}.log'.format(index, command[0])
        (out / name).write_text(result.stdout)
        records.append({'command': command, 'returncode': result.returncode, 'log': name})
        if result.returncode:
            print(result.stdout[-8000:])
            raise SystemExit(result.returncode)
    report = {'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'clean_staging': True, 'shell_escape': False, 'commands': records,
              'pdf_sha256': hashlib.sha256((out / 'main.pdf').read_bytes()).hexdigest()}
    (out / 'build-record.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
