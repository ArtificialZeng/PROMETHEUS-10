#!/usr/bin/env python3
"""Replay packaged exact checks in fresh copies without changing frozen evidence."""
import argparse
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', default='build/reproduction',
                    help='New project-relative output directory; never overwritten.')
args = parser.parse_args()
OUT = (ROOT/args.output).resolve()
if ROOT not in OUT.parents:
    raise SystemExit('Output must be a directory inside the project.')
if OUT.exists():
    raise SystemExit('Refusing to overwrite replay outputs; choose a new --output.')
OUT.mkdir(parents=True)
names = ['check_witness.py', 'witness-input.json', 'old-figure-input.json',
         'replay_quantum.py', 'independent-circuit-input.json']
for name in names:
    shutil.copy2(ROOT/'evidence'/'research-pass1'/name, OUT/name)
shutil.copy2(ROOT/'supplement'/'referee_replay.py',OUT/'referee_replay.py')
for name in ('referee_replay.py', 'check_witness.py', 'replay_quantum.py'):
    with (OUT/(name+'.log')).open('w') as log:
        run = subprocess.run([sys.executable,str(OUT/name)], cwd=OUT,
                             stdout=log, stderr=subprocess.STDOUT)
    if run.returncode:
        raise SystemExit('Replay failed: '+name+'; see '+str(OUT/(name+'.log')))
import sympy
result={'status':'pass','output_directory':str(OUT.relative_to(ROOT)),
        'implementations':3,'arithmetic':'exact',
        'python':platform.python_version(),'sympy':sympy.__version__}
(OUT/'reproduction-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
