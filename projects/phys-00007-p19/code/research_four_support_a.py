#!/usr/bin/env python3
"""Explicit ordinary-qubit partial trace of independently specified spin terms."""
from pathlib import Path
from math import comb
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'evidence/research-20261012-four-support-input-a.json'
data=json.loads(INPUT.read_text())
N=data['N']; c=[s.S.Zero]*(N+1)
for item in data['magnetic_terms']:
 k=(N+item['twice_m'])//2
 assert 2*k-N==item['twice_m']
 c[k]=s.sympify(item['coefficient'])
psi=[c[x.bit_count()]/s.sqrt(comb(N,x.bit_count())) for x in range(1<<N)]
clean=lambda x:s.simplify(s.expand(x))
norm=clean(sum(x*s.conjugate(x) for x in psi));assert norm==1
for i in range(N-1):
 for x in range(1<<N):
  y=x if ((x>>i)&1)==((x>>(i+1))&1) else x^(1<<i)^(1<<(i+1))
  assert psi[x]==psi[y]
out={'input_file':str(INPUT.relative_to(ROOT)),'norm':str(norm),'coefficients_k':[str(v) for v in c],'marginals':{}}
for t in range(1,5):
 env=1<<(N-t)
 rho=s.Matrix(1<<t,1<<t,lambda a,b:clean(sum(psi[a*env+e]*s.conjugate(psi[b*env+e]) for e in range(env))))
 D=s.Matrix(1<<t,t+1,lambda a,b:1/s.sqrt(comb(t,int(b))) if int(a).bit_count()==b else 0)
 R=(D.T*rho*D).applyfunc(clean)
 assert D.T*D==s.eye(t+1)
 assert (rho-D*R*D.T).applyfunc(clean)==s.zeros(1<<t)
 assert R==R.conjugate().T and s.trace(R)==1
 if t<=2:assert R==s.eye(t+1)/s.Integer(t+1)
 P=clean(s.trace(R*R)); A=clean(s.Rational(t+1,t)*(1-P))
 out['marginals'][str(t)]={'rho_sym':[[str(v) for v in row] for row in R.tolist()],'purity':str(P),'A':str(A)}
 print('A full trace t=',t,'rho=',R,'purity=',P,'A=',A,flush=True)
P3=s.sympify(out['marginals']['3']['purity']);gap=clean(s.Rational(789,3136)-P3)
print('Exact P3 improvement:',gap,'; decimal diagnostic:',gap.evalf(25),flush=True)
# Sign verification is the separate rational-square certificate in the proof.
out['purity_improvement']=str(gap)
out['checks']={'normalization':'1','permutation_symmetry':'all adjacent swaps','symmetric_support':'exact t=1..4','rho1_constraint':'exact','rho2_constraint':'exact'}
(ROOT/'evidence/research-20261012-four-support-output-a.json').write_text(json.dumps(out,indent=2)+'\n')

