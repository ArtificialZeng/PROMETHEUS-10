"""Input A: fixed-source symmetric projectors and local depolarizing maps.

No input from reconstruction B. Exact QQ[delta] matrix arithmetic, input first.
Run from the project root: python3 reproduction/input_a.py
"""
import itertools
import json
import math
from pathlib import Path
import sympy as S

d = S.Symbol('delta', real=True)


def bits(k, m):
    return [(k >> (m - 1 - j)) & 1 for j in range(m)]


def integer(v):
    return sum(a << (len(v) - 1 - j) for j, a in enumerate(v))


def permutation_matrix(order):
    m = len(order)
    out = S.zeros(2**m)
    for k in range(2**m):
        b = bits(k, m)
        out[integer([b[j] for j in order]), k] = 1
    return out


def symmetric_projector(m):
    out = S.zeros(2**m)
    for order in itertools.permutations(range(m)):
        out += permutation_matrix(order)
    out /= math.factorial(m)
    assert out * out == out and S.trace(out) == m + 1
    return out


def depolarize_site(mat, site, m):
    # Replacing a site by I/2 times its partial trace, in explicit bit indices.
    out = S.zeros(2**m)
    for i in range(2**m):
        a = bits(i, m)
        for j in range(2**m):
            b = bits(j, m)
            replacement = 0
            if a[site] == b[site]:
                for c in [0, 1]:
                    aa, bb = a.copy(), b.copy()
                    aa[site] = bb[site] = c
                    replacement += mat[integer(aa), integer(bb)] / 2
            out[i, j] = S.expand((1-d) * mat[i, j] + d * replacement)
    return out


def pt_inputs(mat, n):
    # i=2*a+b, j=2*c+e -> source entry 2*c+b, 2*a+e.
    return S.Matrix(2**(n+1), 2**(n+1),
                    lambda i,j: mat[2*(j//2)+i%2, 2*(i//2)+j%2])


def dump_matrix(mat):
    degree = max([S.Poly(v, d).degree() for v in mat if v != 0] or [0])
    return {'dimension': mat.rows, 'degree': int(degree),
            'rows': [[[str(S.expand(v).coeff(d,k)) for k in range(degree+1)]
                      for v in list(mat.row(i))] for i in range(mat.rows)]}


data = {'method': 'A: symmetric permutation projectors, local bit-index depolarization',
        'source': 'arXiv:2504.10516v2, Appendix B (S3), Appendix D (S3)-(S4)',
        'basis': '|a1,...,an,b>, a1 most significant; input first, output last',
        'variable': 'delta', 'coefficient_order': 'ascending powers, exact rational strings',
        'cases': {}}
for n in [2,3]:
    q = symmetric_projector(n+1) / (n+2)
    r0 = symmetric_projector(n) / (n+1)
    for site in range(n):
        q = depolarize_site(q, site, n+1)
        r0 = depolarize_site(r0, site, n)
    r = S.kronecker_product(r0, S.eye(2))
    data['cases'][str(n)] = {name: dump_matrix(mat) for name, mat in
                            [('Q',q),('R',r),('QT',pt_inputs(q,n)),('RT',pt_inputs(r,n))]}
    assert S.expand(S.trace(q)) == 1 and S.expand(S.trace(r)) == 2
    print(f'A n={n}: dimension={q.rows}, Tr Q=1, Tr R=2; exact matrices saved')
beta = (1-d)*d*(d-2)/24
D = beta * (2*S.eye(8) - permutation_matrix([1,2,0]) - permutation_matrix([2,0,1]))
data['published_dual'] = {'beta': str(S.expand(beta)), 'D': dump_matrix(D),
                           'W=DT': dump_matrix(pt_inputs(D,2))}
Path('evidence/input-a.json').write_text(json.dumps(data, indent=2)+'\n')
