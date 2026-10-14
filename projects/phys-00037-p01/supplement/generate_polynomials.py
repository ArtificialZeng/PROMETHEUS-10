"""Exact n=3 normal-Hessian resolvent numerator; no inference from samples."""
import itertools
import json
import time
from pathlib import Path

import argparse
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--output-dir', type=Path, required=True)
_args = _parser.parse_args()
_OUTPUT = _args.output_dir.resolve()
_HERE = Path(__file__).resolve().parent
if _OUTPUT == _HERE or _HERE in _OUTPUT.parents:
    raise ValueError('Select an output directory outside the source supplement directory')
_OUTPUT.mkdir(parents=True, exist_ok=True)
if not __debug__:
    raise RuntimeError('Exact assertions require Python without -O')
import sympy as sp

a,b,c,d,e,f,z=sp.symbols('a b c d e f z')
variables=(a,b,c,d,e,f)
r=b*c
s=d*e
rows=[]
for t2,t3 in itertools.product((1,-1),repeat=2):
    W=1+a*r*t2+a*s*t3+r*s*t2*t3
    D=a+r*t2+s*t3+a*r*s*t2*t3
    F=f*(b*d+c*e*t2*t3+a*(c*d*t2+b*e*t3))
    rows.append((W,D,F))
coeff=[]
for k in range(4):
    expr=0
    for i,(W,D,F) in enumerate(rows):
        elementary=sum((sp.prod(rows[j][0] for j in subset)
                        for subset in itertools.combinations([j for j in range(4) if j!=i],k)),sp.Integer(0))
        expr+=(D**2-F**2)*elementary
    poly=sp.Poly(sp.expand(expr),variables)
    assert all(all(n%2==0 for n in powers) for powers in poly.monoms())
    V=sp.symbols('A B C D E F')
    expr2=sum(co*sp.prod(v**(n//2) for v,n in zip(V,powers))
              for powers,co in poly.terms())
    fact=sp.factor(expr2)
    print('COEFFICIENT',k,'TERMS',len(poly.terms()),'FACTORED',fact,flush=True)
    coeff.append({'k':k,'squared_variables':str(fact),'terms':[[list(powers),str(co)] for powers,co in sp.Poly(expr2,V).terms()]})
(_OUTPUT / 'polynomials.json').write_text(json.dumps({'definition':'sum_i (D_i^2-F_i^2) product_(j!=i)(1+z W_j)','squared_variables':['A=a^2','B=b^2','C=c^2','D=d^2','E=e^2','F=f^2'],'coefficients':coeff,'status':'exact_symbolic_identity_only'},indent=2)+'\n')
