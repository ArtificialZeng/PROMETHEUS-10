#!/usr/bin/env python3
"""Replay both unchanged certifiers in a new local output tree.

No frozen reference file is overwritten. No third-party Python package is used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--output', default=str(HERE.parent / 'build' / 'certificate-replay'))
args = parser.parse_args()
out = Path(args.output).resolve()
if HERE == out or HERE in out.parents:
    raise SystemExit('Place generated output outside the supplement source tree.')
out.mkdir(parents=True, exist_ok=True)
if any(out.iterdir()):
    raise SystemExit('Replay output directory must be empty.')
hashes = json.loads((HERE / 'input-hashes.json').read_text())
for rel, expected in hashes.items():
    data = (HERE / rel).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise SystemExit('Supplement input changed: ' + rel)
    if rel.startswith('code/') or rel.startswith('evidence/'):
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
(out / 'audit').mkdir()
commands = ['research_certificate.py', 'independent_certificate.py']
runs = []
for name in commands:
    command = [sys.executable, '-S', str(out / 'code' / name)]
    run = subprocess.run(command, cwd=out, text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, timeout=120)
    (out / (name + '.log')).write_text(run.stdout)
    runs.append({'program': name, 'command': command, 'returncode': run.returncode})
    if run.returncode:
        print(run.stdout)
        raise SystemExit(run.returncode)
ignore = {'elapsed_seconds', 'runtime_seconds', 'peak_rss_bytes_macos', 'python', 'platform'}
pairs = [
    ('reference/complex-certificate.json', 'evidence/research/interval-certificate.json'),
    ('reference/scalar-certificate.json', 'audit/independent-certificate.json'),
]
comparisons = []
for reference, result in pairs:
    old = json.loads((HERE / reference).read_text())
    new = json.loads((out / result).read_text())
    expected = {k: v for k, v in old.items() if k not in ignore}
    actual = {k: v for k, v in new.items() if k not in ignore}
    if not all(new['tests'].values()):
        raise SystemExit('Certificate assertion did not pass: ' + result)
    same = expected == actual
    comparisons.append({'reference': reference, 'result': result,
                        'all_scientific_fields_identical': same,
                        'all_certificate_tests_passed': True})
    if not same:
        raise SystemExit('Scientific output differs from the archived certificate: ' + result)
summary = {'standard_library_only': True, 'runs': runs, 'comparisons': comparisons,
           'runtime_fields_excluded_from_equality': sorted(ignore),
           'scope': 'Replay of coefficient certificates and exact source calibrations; '
                    'the analytic passage to original-ODE cycles is in the manuscript.'}
(out / 'replay-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
