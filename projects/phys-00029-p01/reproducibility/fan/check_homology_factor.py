#!/usr/bin/env python3
"""Post-calculation full-polynomial check of the homology-preserving trace.
Uses enumerated original polynomials, so is explicitly not an independent
source reconstruction. The geometric weighted KW checker is independent.
"""
from pathlib import Path
import json,sympy as s
b=Path(__file__).resolve().parent
r=s.symbols('r',positive=True)
results=[]
upvec=s.Matrix([r,1])/(r+1)
M=s.Matrix([[r*r,1],[1,1]])/(r+1)
rows=json.loads((b/'fan-check-results.json').read_text())['original_homology_checks']
for row in rows:
    n=row['N']; t=(r-1)/(r+1)
    poly=sum(s.Integer(c)*t**k for k,c in enumerate(row['signed_original_coefficients_ascending']))
    w=M**(n-1)*upvec
    up=(s.Matrix([[r,1/r]])*w)[0]; um=sum(w)
    reduction=2**(2*n+2)*r**(n+1)/(r+1)**(2*n+3)*(2-r*r*up+um)
    residual=s.factor(poly-reduction)
    assert residual==0
    results.append({'N':n,'full_symbolic_original_signed_polynomial_matches_trace_reduction':True,
                    'residual':'0','original_r_factor':str(s.factor(poly))})
print(json.dumps(results,indent=2))
(b/'homology-factor-check.json').write_text(json.dumps(results,indent=2)+'\n')
