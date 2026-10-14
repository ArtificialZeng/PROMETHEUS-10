#!/usr/bin/env python3
"""Build the local draft in a new directory, retaining actual compiler output."""
import argparse
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', default='build/draft',
                    help='New project-relative directory; existing nonempty paths are refused')
args = parser.parse_args()
out = (ROOT / args.output_dir).resolve()
if not out.is_relative_to(ROOT):
    parser.error('Output must remain within the project')
if out.exists() and any(out.iterdir()):
    parser.error('Use a new output directory to preserve previous builds')
out.mkdir(parents=True, exist_ok=True)
latexmk = shutil.which('latexmk')
if latexmk is None:
    parser.error('latexmk must already be installed; this script installs nothing')
command = [latexmk, '-pdf', '-interaction=nonstopmode', '-halt-on-error',
           '-file-line-error', '-recorder', f'-outdir={out}', 'manuscript/main.tex']
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = subprocess.run(command, cwd=ROOT, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(out / 'compiler-output.log').write_text(result.stdout)
record = {'started_at': started,
          'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'command': command, 'cwd': str(ROOT), 'clean_directory_at_start': True,
          'exit_code': result.returncode, 'pdf': (out / 'main.pdf').relative_to(ROOT).as_posix(),
          'stdout_log': (out / 'compiler-output.log').relative_to(ROOT).as_posix(),
          'tex_log': (out / 'main.log').relative_to(ROOT).as_posix()}
(out / 'build-record.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
if result.returncode:
    print(result.stdout[-8000:], file=sys.stderr)
sys.exit(result.returncode)
