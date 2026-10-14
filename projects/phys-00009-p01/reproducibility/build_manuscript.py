"""Build the manuscript in a new, empty local directory without deleting files."""
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='build/author-rebuild')
args = parser.parse_args()
relative = Path(args.output)
if relative.is_absolute() or '..' in relative.parts:
    parser.error('Output must be a project-relative directory.')
destination = ROOT/relative
destination.mkdir(parents=True, exist_ok=True)
if any(destination.iterdir()):
    parser.error('Choose an empty build directory; existing files are preserved.')
command = ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
           '-file-line-error', '-recorder', '-outdir='+relative.as_posix(),
           'manuscript/main.tex']
with (destination/'command.log').open('w') as log:
    log.write('Command: '+' '.join(command)+'\n')
    log.flush()
    completed = subprocess.run(command, cwd=ROOT, stdout=log,
                               stderr=subprocess.STDOUT, check=False)
print('Exit status:', completed.returncode)
print('Command/compiler logs:', destination)
raise SystemExit(completed.returncode)
