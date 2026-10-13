"""Input B: independent Bloch integration and signed Pauli transposition.

Does not read or import input A or its code. Own basis is output first.
Run from the project root: python3 reproduction/input_b.py
"""
from itertools import product
from math import prod
from pathlib import Path
import json
import sympy as S

t = S.Symbol('t', real=True)  # t=1-delta
I = S.eye(2)
# Deliberately different label order; matrices explicitly transcribed here.
pauli = {'I':I, 'Z':S.diag(1,-1),
         'X':S.Matrix([[0,1],[1,0]]), 'Y':S.Matrix([[0,-S.I],[S.I,0]])}


def tensor(labels):
    out = S.ones(1,1)
    for label in labels:
        out = S.kronecker_product(out, pauli[label])
    return out


def dfact(k):
    return prod(range(k,0,-2))


def sphere_moment(labels):
    # Integrating the uniform unit sphere: odd exponent -> zero;
    # even exponents 2a,2b,2c -> prod((2a-1)!!)/(2a+2b+2c+1)!!.
    exponents = [labels.count(axis) for axis in ['X','Y','Z']]
    if any(e % 2 for e in exponents):
        return S.Rational(0)
    return S.Rational(prod(dfact(e-1) for e in exponents), dfact(sum(exponents)+1))


def pack(mat):
    order = max([S.Poly(x,t).degree() for x in mat if x != 0] or [0])
    return {'dimension': mat.rows, 'degree': int(order),
            'rows': [[[str(S.expand(mat[i,j]).coeff(t,k)) for k in range(order+1)]
                      for j in range(mat.cols)] for i in range(mat.rows)]}


assert sphere_moment(['X','X']) == S.Rational(1,3)
assert sphere_moment(['X']*4) == S.Rational(1,5)
assert sphere_moment(['X','X','Y','Y']) == S.Rational(1,15)
out = {'method': 'B: normalized Bloch sphere integration; transpose by input-Y parity',
       'source': 'Primary input definition plus sphere moments; Appendix D (S10) for dual',
       'basis': '|b,a1,...,an>, b most significant; Pauli enumeration I,Z,X,Y',
       'variable':'t=1-delta', 'coefficient_order':'ascending powers, exact rational strings',
       'cases':{}}
for n in [2,3]:
    mats = {k:S.zeros(2**(n+1)) for k in ['Q','R','QT','RT']}
    terms = {'Q':[], 'R':[]}
    for labels in product(pauli, repeat=n+1):
        # Slot 0 is the noiseless output; each nonidentity input has one factor t.
        degree = sum(x!='I' for x in labels[1:])
        c = sphere_moment(labels) / 2**(n+1)
        cp = c * t**degree
        sign = (-1)**labels[1:].count('Y')
        if c:
            p = tensor(labels)
            mats['Q'] += cp*p
            mats['QT'] += sign*cp*p
            terms['Q'].append({'labels':''.join(labels), 'coefficient':str(c), 't_degree':degree})
        if labels[0]=='I':
            c = sphere_moment(labels[1:]) / 2**n
            if c:
                p = tensor(labels)
                mats['R'] += c*t**degree*p
                mats['RT'] += sign*c*t**degree*p
                terms['R'].append({'labels':''.join(labels), 'coefficient':str(c), 't_degree':degree})
    out['cases'][str(n)] = {k:pack(v) for k,v in mats.items()}
    out['cases'][str(n)]['pauli_terms'] = terms
    print(f'B n={n}: Bloch moments and input-Y parity, {len(terms["Q"])} Q terms, {len(terms["R"])} R terms')

# Separate transcription of the final Pauli coefficient formula, PDF p.16 (S10).
# In this output-first basis the Pauli string is (v,r,w).
beta = t*(t*t-1)/24
W = S.zeros(8)
ys = []
for r,w,v in product(pauli, repeat=3):
    c = 3*S.Integer(r==w==v=='I') - S.Rational(1,2)*(
        S.Integer(r==w and v=='I')
        +(-1)**(w=='Y')*S.Integer(r=='I' and w==v)
        +(-1)**(r=='Y')*S.Integer(w=='I' and r==v))
    if c:
        W += beta*c*tensor((v,r,w))
        ys.append({'labels':v+r+w, 'coefficient_over_beta':str(c)})
out['published_dual'] = {'W=DT':pack(W), 'pauli_coefficients_over_beta':ys}
Path('evidence/input-b.json').write_text(json.dumps(out,indent=2)+'\n')
