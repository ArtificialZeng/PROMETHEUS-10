#!/usr/bin/env python3
"""Exact comparison and integer sign certificate; not a fresh referee audit."""
from pathlib import Path
import json
from fractions import Fraction as Q
from math import comb
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
A=json.loads((ROOT/'evidence/research-20261012-four-support-output-a.json').read_text())
B=json.loads((ROOT/'evidence/research-20261012-four-support-output-b.json').read_text())
assert all(s.simplify(s.sympify(A['coefficients_k'][k])-s.sympify(B['coefficients_q'][9-k]))==0 for k in range(10))
entries=0
for t in range(1,5):
 R=s.Matrix([[s.sympify(x) for x in row] for row in A['marginals'][str(t)]['rho_sym']])
 S=s.Matrix([[s.sympify(x) for x in row] for row in B['marginals'][str(t)]['rho_down']])
 rev=s.zeros(t+1)
 for k in range(t+1):rev[k,t-k]=1
 assert (R-rev.T*S*rev).applyfunc(s.simplify)==s.zeros(t+1)
 assert s.simplify(s.sympify(A['marginals'][str(t)]['purity'])-s.sympify(B['marginals'][str(t)]['purity']))==0
 entries+=(t+1)**2
 print('Exact basis reversal comparison t=',t,'PASS',flush=True)
print('All',entries,'marginal entries and ten coefficients agree exactly.')

# Third calculation: diagonal partial traces using ONLY standard-library fractions,
# with four support weights transcribed explicitly. No output A/B value is read.
weights={0:Q(1,6),3:Q(1,3),6:Q(1,3),9:Q(1,6)}
diagonals={}
for t in range(1,4):
 diagonal=[sum((p*Q(comb(t,a)*comb(9-t,k-a),comb(9,k)) for k,p in weights.items() if 0<=k-a<=9-t),Q(0)) for a in range(t+1)]
 assert diagonal==[Q(1,t+1)]*(t+1)
 diagonals[str(t)]=[str(x) for x in diagonal]
 print('Standard-library exact diagonals t=',t,diagonal)
# The three corner terms have lengths a,b,a, with a=1/(6 sqrt(42)), b=5/63.
# Use Q(sqrt(42)) represented as pairs (rational part, sqrt(42) coefficient).
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]+42*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
corner=(Q(5,63),Q(-1,126))
pure=add((Q(1,4),Q(0)),mul((Q(2),Q(0)),mul(corner,corner)))
gap=(Q(789,3136)-pure[0],-pure[1])
assert pure==(Q(4253,15876),Q(-10,3969))
assert gap==(Q(-4139,254016),Q(10,3969))
assert Q(10,3969)*254016==640
square_gap=640**2*42-4139**2
assert 640>0 and 4139>0 and square_gap==71879>0
print('Independent Q(sqrt(42)) purity=',pure,'; gap=',gap)
print('Strict positivity: 640^2*42-4139^2=',square_gap,'>0, so 640 sqrt(42)>4139.')
# Positive marginal eigenvalues: |corner|<1/4. Since 0<sqrt(42)<7<10,
# 0<corner<10/126=5/63<1/4.
assert 0<42<7**2 and Q(5,63)<Q(1,4)
print('rho3 eigenvalues 1/4 (twice), 1/4 +/- (10-sqrt(42))/126 are positive.')
# Baseline plus signs have opposite interference, a different SU(2)-invariant purity.
plus_corner=(Q(5,63),Q(1,126))
plus_purity=add((Q(1,4),Q(0)),mul((Q(2),Q(0)),mul(plus_corner,plus_corner)))
assert plus_purity!=pure
print('All-positive published support has purity',plus_purity,'and cannot be SU(2)-equivalent to the witness.')
out={'basis_comparison':{'coefficient_count':10,'marginal_entry_count':entries,'all_residuals':'exact zero'},
 'stdlib_independent_diagonals':diagonals,
 'stdlib_radical_field_purity':{'rational':str(pure[0]),'sqrt42_coefficient':str(pure[1])},
 'purity_gap':{'rational':str(gap[0]),'sqrt42_coefficient':str(gap[1]),'integer_sign_certificate':square_gap},
 'positive_rho3_eigenvalues':True,
 'published_positive_phase_purity':{'rational':str(plus_purity[0]),'sqrt42_coefficient':str(plus_purity[1])},
 'independence_limit':'Same proposer, same proposed vector. Different full-qubit and Schmidt algorithms share SymPy; third arithmetic check uses Python fractions and explicitly stated support weights. This is proposer verification, not referee acceptance.'}
(ROOT/'evidence/research-20261012-four-support-verification.json').write_text(json.dumps(out,indent=2)+'\n')

