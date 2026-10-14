#!/usr/bin/env python3
"""Build the complete manuscript in a new, project-local directory."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ['main.tex', 'references.bib', 'certificate-center.tex',
          'certificate-preconditioner.tex', 'comparison-table.tex']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='build/clean')
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if output == ROOT or not output.is_relative_to(ROOT):
        parser.error('--output must be inside the project')
    if output.exists():
        parser.error('--output must not exist before a clean build')
    output.mkdir(parents=True)
    for name in INPUTS:
        shutil.copy2(ROOT / 'manuscript' / name, output / name)
    commands = [['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
                 '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
                ['bibtex', 'main'],
                ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
                 '-halt-on-error', '-file-line-error', '-recorder', 'main.tex'],
                ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode',
                 '-halt-on-error', '-file-line-error', '-recorder', 'main.tex']]
    log_parts = []
    for index, command in enumerate(commands, 1):
        result = subprocess.run(command, cwd=output, capture_output=True, text=True)
        part = 'Command: ' + ' '.join(command) + '\n' + result.stdout + result.stderr
        (output / f'pass-{index}.log').write_text(part)
        log_parts.append(part)
        (output / 'build-command.log').write_text('\n'.join(log_parts))
        if result.returncode != 0:
            raise RuntimeError(f'Build command failed: {command}; see pass-{index}.log')
    subprocess.run(['pdftotext', 'main.pdf', 'main.txt'], cwd=output, check=True)
    if not (output / 'main.txt').read_text().strip():
        raise RuntimeError('PDF text extraction is empty')
    print(json.dumps({'output': str(output.relative_to(ROOT)),
                      'commands_completed': len(commands), 'pdf': str((output / 'main.pdf').relative_to(ROOT)),
                      'scope': 'Actual clean compilation; no independent release acceptance asserted'}))


if __name__ == '__main__':
    main()
