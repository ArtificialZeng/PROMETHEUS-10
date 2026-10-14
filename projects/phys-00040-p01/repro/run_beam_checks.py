#!/usr/bin/env python3
"""Replay the two exact beam calculations without modifying reference outputs."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
out = args.output_dir.resolve()
out.mkdir(parents=True, exist_ok=True)
here = Path(__file__).resolve().parent
checks = [
    ('beam_pair_check.py', 'product-pair-exact.json', 'expected-beam-pair.json'),
    ('beam_scaling_check.py', 'normalization-and-scaling-exact.json', 'expected-beam-scaling.json'),
]
results = []
for program, output, expected in checks:
    cmd = [sys.executable, str(here / program), '--output-dir', str(out)]
    run = subprocess.run(cmd, text=True, capture_output=True, timeout=90)
    log = out / (program + '.log')
    log.write_text(run.stdout + run.stderr)
    if run.returncode:
        raise SystemExit(f'{program} failed; inspect {log}')
    actual = json.loads((out / output).read_text())
    reference = json.loads((here / expected).read_text())
    if actual != reference:
        raise SystemExit(f'{program}: exact output differs from {expected}')
    results.append({'program': program, 'exit_code': run.returncode,
                    'exact_reference_equal': True,
                    'output': output,
                    'sha256': hashlib.sha256((out / output).read_bytes()).hexdigest()})
import sympy
receipt = {'python': platform.python_version(), 'sympy': sympy.__version__,
           'checks': results,
           'scope': 'Exact coefficient and scaling replay. The analytic integrations by parts, overlap estimates and solution differentiability require the manuscript proof.'}
(out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
