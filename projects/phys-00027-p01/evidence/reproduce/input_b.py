"""Input B: independently derived orthonormal Choi/Kraus representation.

Primary anchors: 2405.11216v3 PDF p2 Eqs. (4),(6), p3 RHS Eq. (12)
and mixture Eq. (13). Choi sectors and normalization are derived in input-b.md.
No import of input_a, no reading of A-generated files, no direct-map function.
Weights multiply normalized matrices F, meaning Kraus K=sqrt(weight)*F.
This avoids unnecessary square-root simplification in exact arithmetic.
"""
import json
from pathlib import Path
import sympy as sp

X_WEIGHT, Y_WEIGHT = sp.symbols('x y', real=True)


def component(d, i, j):
    m = sp.zeros(d)
    m[i, j] = 1
    return m


def weighted_basis(d, x, y):
    # The Omega eigenvector maps to I/sqrt(d); its J eigenvalue is below.
    out = [('omega', d*(1-x-y) + 2*y/(d+1), sp.eye(d)/sp.sqrt(d))]
    for i in range(d):
        for j in range(i+1, d):
            out.append((f'symmetric_{i}_{j}', 2*y/(d+1),
                        (component(d, i, j)+component(d, j, i))/sp.sqrt(2)))
    for m in range(1, d):
        f = sp.zeros(d)
        for i in range(m):
            f[i, i] = 1
        f[m, m] = -m
        out.append((f'diagonal_traceless_{m}', 2*y/(d+1),
                    f/sp.sqrt(m*(m+1))))
    for i in range(d):
        for j in range(i+1, d):
            out.append((f'antisymmetric_{i}_{j}', 2*x/(d-1),
                        (component(d, i, j)-component(d, j, i))/sp.sqrt(2)))
    return out


def apply_kraus(m, x, y):
    out = sp.zeros(m.rows)
    for label, weight, f in weighted_basis(m.rows, x, y):
        out += weight * f * m * f.H
    return out.applyfunc(sp.simplify)


def choi(d, x, y):
    # |F>>_io has entries F[a,i] in coordinate i*d+a (vec_F(F)).
    out = sp.zeros(d*d)
    for label, weight, f in weighted_basis(d, x, y):
        v = sp.Matrix([f[a, i] for i in range(d) for a in range(d)])
        out += weight * v * v.H
    return out.applyfunc(sp.simplify)


def superoperator(d, x, y):
    # Independently unreshuffle J, rather than evaluating a direct channel.
    jmat = choi(d, x, y)
    out = sp.zeros(d*d)
    for a in range(d):
        for b in range(d):
            for i in range(d):
                for j in range(d):
                    out[a+d*b, i+d*j] = jmat[i*d+a, j*d+b]
    return out


def encode(m):
    return [[str(sp.simplify(m[i, j])) for j in range(m.cols)] for i in range(m.rows)]


def main():
    d = 3
    x, y = sp.Rational(1,4), sp.Rational(1,4)
    # Independent transcription of PDF p6 Eq. (28), not read from A.
    psi = sp.Matrix([sp.I,1,0]) / sp.sqrt(2)
    rho = psi * psi.H
    basis = weighted_basis(d, X_WEIGHT, Y_WEIGHT)
    obj = {
        'representation': 'B: normalized Choi eigenvectors and Kraus operators',
        'source': 'literature/2405.11216v3.pdf',
        'locator': 'PDF p2 Eqs. (4),(6); p3 RHS Eq. (12), Eq. (13); p6 Eq. (28)',
        'derivation': 'evidence/reproduce/input-b.md',
        'basis': '0-based computational basis; source |m> maps to local |m-1>',
        'normalization': 'J trace=d; J/d trace=1; K=sqrt(J_eigenvalue)*F; Tr(F^dagger F)=1',
        'choi_index': 'input tensor output: row=i*d+a, column=j*d+b',
        'superoperator_index': 'vec_F: row=a+d*b, column=i+d*j',
        'weighted_orthonormal_matrices': [
            {'label':label,'J_eigenvalue':str(sp.simplify(weight)),
             'normalized_matrix':encode(f)} for label,weight,f in basis],
        'symbolic_d3_superoperator': encode(superoperator(d, X_WEIGHT, Y_WEIGHT)),
        'symbolic_d3_choi': encode(choi(d, X_WEIGHT, Y_WEIGHT)),
        'benchmark': {'d':d, 'x':str(x), 'y':str(y), 'rho':encode(rho),
                      'output':encode(apply_kraus(rho,x,y)),
                      'superoperator':encode(superoperator(d,x,y)),
                      'choi':encode(choi(d,x,y)),
                      'normalized_choi':encode(choi(d,x,y)/d)},
        'independence': 'Same agent, independent representation/implementation; no A imports or A result reads.'
    }
    path = Path(__file__).with_name('input-b.json')
    path.write_text(json.dumps(obj, indent=2) + '\n')
    print('Generated ' + str(path) + ' from orthonormal Choi/Kraus derivation.')


if __name__ == '__main__':
    main()
