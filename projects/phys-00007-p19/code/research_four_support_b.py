#!/usr/bin/env python3
"""Opposite-count Schmidt construction; reads only separate weights input B."""
from pathlib import Path
from math import comb
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'evidence/research-20261012-four-support-input-b.json'
data=json.loads(INPUT.read_text()); n=data['N']
b=[s.S.Zero]*(n+1)
for item in data['down_count_terms']:
 b[item['q']]=s.sqrt(s.Rational(item['weight']))*s.sympify(item['phase'])
assert s.simplify(sum(x*s.conjugate(x) for x in b))==1
out={'input_file':str(INPUT.relative_to(ROOT)),'norm':'1','coefficients_q':[str(v) for v in b],'marginals':{}}
for t in range(1,5):
 M=s.Matrix(t+1,n-t+1,lambda a,e:b[a+e]*s.sqrt(s.Rational(comb(t,int(a))*comb(n-t,int(e)),comb(n,int(a+e)))))
 R=(M*M.conjugate().T).applyfunc(s.simplify)
 assert s.trace(R)==1 and R==R.conjugate().T
 if t<=2:assert R==s.eye(t+1)/s.Integer(t+1)
 P=s.simplify(s.trace(R*R)); A=s.simplify(s.Rational(t+1,t)*(1-P))
 out['marginals'][str(t)]={'schmidt':[[str(v) for v in row] for row in M.tolist()],'rho_down':[[str(v) for v in row] for row in R.tolist()],'purity':str(P),'A':str(A)}
 print('B Schmidt t=',t,'rho=',R,'purity=',P,'A=',A,flush=True)
(ROOT/'evidence/research-20261012-four-support-output-b.json').write_text(json.dumps(out,indent=2)+'\n')

