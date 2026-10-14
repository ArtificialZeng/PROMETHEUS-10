"""Replay the accepted witness without changing scientific evidence files.
Run from the project/package root: python3 code/reproduce_manuscript.py
No third-party modules, network, random search or finite differences.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from thermal_search import calculate
from check_witness import characteristic

root = Path(__file__).resolve().parent.parent
spec = json.loads((root / 'evidence/witness-frozen.json').read_text())
saved = json.loads((root / 'evidence/witness-check.json').read_text())
c, p, edges, derivatives = calculate(spec)
d, B, residual, coefficients = characteristic()
assert c == d == list(map(F, saved['cumulants']))
assert c[1] > 0 and c[3] < 0
assert residual == [0] * 5
assert B == F(saved['stationary_branch_simple_B'])
assert coefficients['A'] == F(saved['characteristic_coefficients']['A'])
for field in ['B_derivatives', 'C_derivatives']:
    assert coefficients[field] == list(map(F, saved['characteristic_coefficients'][field]))
assert p == [F(n, 484942013513) for n in (300458657988,172970937252,11512418273)]
print(json.dumps({'status': 'pass', 'arithmetic': 'exact fractions',
    'cumulants_dimensionless': list(map(str, c)),
    'stationary': list(map(str, p)),
    'characteristic_coefficients': coefficients,
    'residual': residual, 'ratio_dimensionless': str(c[3]/c[1]),
    'scope': 'the accepted fixed three-state witness only'}, default=str, indent=2))
