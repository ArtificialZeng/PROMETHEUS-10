#!/usr/bin/env python3
"""Run the unchanged exact checker in a new directory without overwriting evidence."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', default='reproducibility/runs/exact',
                    help='New project-relative directory for the log and generated summary')
args = parser.parse_args()
out = (ROOT / args.output_dir).resolve()
if not out.is_relative_to(ROOT):
    parser.error('Output must remain within the project')
if out.exists() and any(out.iterdir()):
    parser.error('Use a new output directory to preserve earlier runs')
out.mkdir(parents=True, exist_ok=True)
(out / 'evidence').mkdir(exist_ok=True)
checker = ROOT / 'evidence/n4k2_exact_checks.py'
original_digest = hashlib.sha256(checker.read_bytes()).hexdigest()
command = [sys.executable, str(checker)]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = subprocess.run(command, cwd=out, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
(out / 'check.log').write_text(result.stdout)
unchanged = hashlib.sha256(checker.read_bytes()).hexdigest() == original_digest
record = {'started_at': started,
          'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'command': command, 'cwd': str(out), 'clean_directory_at_start': True,
          'checker': checker.relative_to(ROOT).as_posix(), 'checker_sha256': original_digest,
          'checker_unchanged': unchanged, 'exit_code': result.returncode,
          'log': (out / 'check.log').relative_to(ROOT).as_posix(),
          'summary': (out / 'evidence/n4k2-exact-check-summary.json').relative_to(ROOT).as_posix(),
          'interpretation': 'Exact algebraic replay; finite checks do not replace the analytic proof or fresh release review.'}
(out / 'run-record.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
if result.returncode:
    print(result.stdout[-8000:], file=sys.stderr)
sys.exit(result.returncode if unchanged else 1)
