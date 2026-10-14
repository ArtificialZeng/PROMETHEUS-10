#!/usr/bin/env python3
"""Exact specialization of arXiv:2509.18533v3 Eq.58; necessary relaxation only."""
import json
from pathlib import Path
import sympy as s
from sympy.physics.wigner import wigner_6j, clebsch_gordan
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[1]
j=s.Rational(9,2)
L=s.Matrix(10,10,lambda l,k:(-1)**(9+l+k)*(2*l+1)*wigner_6j(j,j,l,j,j,k))
assert L*L==s.eye(10)
assert s.trace(L)==0
assert all((2*k+1)*L[l,k]==(2*l+1)*L[k,l] for l in range(10) for k in range(10))
r=s.symbols('r0:10')
constraints=list((L-s.eye(10))*s.Matrix(r))+[r[0]-s.Rational(1,10),r[1],r[2]]
sol=list(s.linsolve(constraints,r))[0]
print('lambda^2=I; trace(lambda)=0; weighted symmetry: exact PASS')
print('Necessary affine locus with r0=1/10, r1=r2=0:',sol)
A=L-s.eye(10)
A=A.col_join(s.eye(10)[:3,:])
b=s.zeros(10,1).col_join(s.Matrix([s.Rational(1,10),0,0]))
fit=linprog([0,0,0,1,0,0,0,0,0,0],A_eq=[[float(v) for v in row] for row in A.tolist()],b_eq=[float(v) for v in b],bounds=[(0,None)]*10,method='highs')
assert fit.success
print('Floating discovery only; relaxed min r3:',fit.fun,'point:',fit.x)
# Reconstruct an EXACT vertex using zero coordinates discovered by the LP.
zeros=[r[i] for i,v in enumerate(fit.x) if abs(v)<1e-9]
vertices=list(s.linsolve(constraints+zeros,r))
assert len(vertices)==1
vertex=vertices[0]
assert not any(x.free_symbols for x in vertex)
assert all(x>=0 for x in vertex)
assert (L-s.eye(10))*s.Matrix(vertex)==s.zeros(10,1)
assert vertex[0]==s.Rational(1,10) and vertex[1]==vertex[2]==0
assert vertex[3]==0
assert sum(vertex)==1
print('Exact nonnegative relaxed witness with r3=0:',vertex)
# Normalized polarization tensor: T_l0(j) top diagonal = CG(j,j;j,-j;l,0).
# SU(2)-covariant partial trace acts by a scalar on each irreducible rank l.
big=clebsch_gordan(j,j,3,j,-j,0)
small=clebsch_gordan(s.Rational(3,2),s.Rational(3,2),3,s.Rational(3,2),-s.Rational(3,2),0)
alpha2=s.simplify(small**2/big**2)
print('Rank-3 channel alpha^2:',alpha2,'; P3=1/4+alpha^2*r3 for r1=r2=0')
out={'source':'arXiv:2509.18533v3 Appendix C Eq.58 and III.2 Eq.27',
 'lambda':[[str(x) for x in row] for row in L.tolist()],
 'exact_checks':{'lambda_squared':'I10','trace_lambda':'0','weighted_symmetry':True,'sum_vertex':'1'},
 'affine_solution':[str(x) for x in sol],
 'floating_discovery':{'minimum_r3':float(fit.fun),'point':fit.x.tolist()},
 'exact_relaxation_vertex':[str(x) for x in vertex],
 'rank3_partial_trace_alpha_squared':str(alpha2),
 'purity_map':'P3=1/4+('+str(alpha2)+')*r3 when r1=r2=0',
 'conclusion':'Published linear compatibility and nonnegative multipole norms permit r3=0 and hence do not imply P3>=789/3136. The vertex is not claimed to arise from a physical pure state.'}
(ROOT/'evidence/research-20261012-recoupling.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['conclusion'])

