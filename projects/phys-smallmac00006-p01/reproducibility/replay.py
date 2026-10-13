"""Replay preserved calculations in a new local directory, never over evidence.

Run from the package root: python3 -B reproducibility/replay.py
The copies execute sequentially in the foreground. No external access is used.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT = ROOT / 'build' / ('replay-' + stamp)
OUT.mkdir(parents=True, exist_ok=False)
(OUT / 'code').mkdir()
(OUT / 'evidence').mkdir()
(OUT / 'history').mkdir()
code = ['reconstruct_a.py', 'reconstruct_b.py', 'compare_reproduction.py',
        'layered_exact_a.py', 'layered_exact_b.py', 'compare_layered.py']
for name in code:
    shutil.copyfile(ROOT / 'code' / name, OUT / 'code' / name)
shutil.copyfile(ROOT / 'evidence/layered-witness-spec.json',
                OUT / 'evidence/layered-witness-spec.json')
shutil.copyfile(ROOT / 'reproducibility/history_replay.py',
                OUT / 'history/history_replay.py')
commands = []
for relative in ['code/' + p for p in code] + ['history/history_replay.py']:
    start = time.perf_counter()
    command = [sys.executable, '-B', relative]
    result = subprocess.run(command, cwd=OUT, capture_output=True, text=True,
                            timeout=60)
    log = OUT / (Path(relative).stem + '.log')
    log.write_text(result.stdout + result.stderr, encoding='utf-8')
    commands.append({'command': command, 'exit_code': result.returncode,
                     'elapsed_seconds': time.perf_counter()-start,
                     'log': log.relative_to(ROOT).as_posix()})
    if result.returncode:
        raise RuntimeError('Replay failed: ' + str(log))

a = json.loads((OUT / 'evidence/layered-exact-a.json').read_text())
old = json.loads((ROOT / 'evidence/layered-exact-a.json').read_text())
for key in ['edges', 'energies', 'q_protocol', 'kernels', 'instantaneous_gibbs',
            'distributions', 'activities', 'mean_activity']:
    assert a[key] == old[key], key
h = json.loads((OUT / 'history/referee-replay.json').read_text())
assert F(h['A0']['exact']) == F(a['activities'][0])
assert F(h['A1']['exact']) == F(a['activities'][1])
assert F(h['mean']['exact']) == F(a['mean_activity'])
assert h['path_counts'][-1] == 704
record = {'status': 'pass', 'python': sys.version, 'platform': platform.platform(),
          'commands': commands, 'history_count': 704,
          'full_replay_equals_preserved_matrix_certificate': True,
          'history_activities_equal_matrix_activities': True,
          'error_control': 'exact Fraction and SymPy Rational; no tolerance',
          'accepted_inputs_changed': False,
          'output_directory': OUT.relative_to(ROOT).as_posix()}
(OUT / 'replay-summary.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
