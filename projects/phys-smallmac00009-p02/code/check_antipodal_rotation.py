#!/usr/bin/env python3
"""Exact adversarial check of phase, root choice and collective rotation.

This checks the nontrivial c!=0 branch after choosing the third coherent root,
not one of the antipodal pair. It is a finite regression check; the universal
root argument remains the analytic proof, not an inference from this example.
"""
from pathlib import Path
from itertools import product
from datetime import datetime,timezone
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'evidence/check-full-kernel-structure-v1.json').read_text())
r=s.symbols('r',real=True)
bases=[s.Matrix([[s.sympify(v,locals={'r':r}).subs(r,2) for v in row] for row in m]) for m in D['chart_records'][0]['basis']]
K=sum((t*B for t,B in zip([1,2,-1,1,2,3],bases)),s.zeros(8))
e=s.eye(8);S1=e[:,1]+e[:,2]+e[:,4];S2=e[:,3]+e[:,5]+e[:,6]
U=s.Matrix.hstack(e[:,0],S1,S2,e[:,7])
V=s.Matrix.hstack(e[:,1]-e[:,2],e[:,1]+e[:,2]-2*e[:,4],e[:,3]-e[:,5],e[:,3]+e[:,5]-2*e[:,6])
eta=S1/3+2*S2/3
assert (U.T*K*V).rank()==1 and K*(2*S1-S2)==s.zeros(8,1)
phase=(s.Integer(3)+4*s.I)/5
g=s.diag(phase,s.conjugate(phase))*s.Matrix([[2,-1],[1,2]])/s.sqrt(5)
assert (g.H*g).applyfunc(s.simplify)==s.eye(2) and s.simplify(g.det())==1
R=s.kronecker_product(g,g,g)
L=(R*K*R.H).applyfunc(s.simplify)
u=(5*s.sqrt(5)*U.T*R*eta).applyfunc(s.simplify)
C=(U.T*L*V).applyfunc(s.simplify)
assert C.rank()==1 and C[0,:]==s.zeros(1,4)
assert u[0]==0 and u[3]!=0 and C[3,:]!=s.zeros(1,4)
assert s.Matrix.hstack(C,u).rank()==1
a,b,c=u[1:]
assert s.simplify(a*s.conjugate(a)-c*s.conjugate(c))==0
assert s.simplify(s.conjugate(c)*b+a*s.conjugate(b))==0
z=s.symbols('z')
q=a+b*z+c*z*z
qsharp=s.conjugate(c)-s.conjugate(b)*z+s.conjugate(a)*z*z
assert s.Poly(s.expand(qsharp-s.conjugate(c)*q/a),z).is_zero
assert s.simplify(s.trace(L*L*L))==0
# Rebuild all 37 observables directly as tensor Pauli sums, without input A/B.
pa={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Y':s.Matrix([[0,-s.I],[s.I,0]]),'Z':s.diag(1,-1)}
groups={}
for word in product('IXYZ',repeat=3):
    if word==('I','I','I'):continue
    key=(tuple(j for j,v in enumerate(word) if v!='I'),tuple(word.count(v) for v in 'XYZ'))
    M=s.kronecker_product(*(pa[v] for v in word))
    groups[key]=groups.get(key,s.zeros(8))+M
assert len(groups)==37 and all(s.simplify(s.trace(L*M))==0 for M in groups.values())
record={'at':datetime.now(timezone.utc).isoformat(),
 'job_id':'phys-smallmac00009-p02-research-10b8522d8222',
 'purpose':'Choose the third root of a cubic with an antipodal pair, then add a complex collective Z phase; exercise u0=0,c!=0 and conjugation conventions',
 'g':[[str(v) for v in row] for row in g.tolist()], 'transformed_u':[str(v) for v in u],
 'C_rank':1,'all_37_fresh_tensor_Pauli_measurements_zero':True,'quadratic_antipodal_identity_exact':True,
 'trace_cubic_exact':'0','coefficient_inputs':[1,2,-1,1,2,3],'chart_ratio':2,
 'arithmetic':'Exact Gaussian rationals and sqrt(5); no floating tolerances',
 'limits':'One nontrivial phase/root-choice regression, not a proof by sampling; shared chart certificate; no independent referee.'}
(ROOT/'evidence/check-antipodal-rotation-v1.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
