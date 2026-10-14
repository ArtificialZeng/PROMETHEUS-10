"""Input A: direct transcription of 2405.11216v3 PDF p3 Eqs. (14),(15).

This implementation does not import input_b or read its generated records.
The complex-linear transpose in Eq. (14) is transposed(), not adjoint().
Run with the pre-existing research Python from the project root.
"""
import json
from pathlib import Path
import sympy as sp

X_WEIGHT, Y_WEIGHT = sp.symbols('x y', real=True)


def matrix_unit(d, i, j):
    m = sp.zeros(d)
    m[i, j] = 1
    return m


def direct_map(m, x, y):
    d = m.rows
    xd = x / (d - 1)
    yd = y / (d + 1)
    return ((1 - x - y) * m + (xd + yd) * sp.trace(m) * sp.eye(d)
            + (yd - xd) * m.T)


def superoperator(d, x, y):
    # vec_F(E_ij) has coordinate i+d*j. Rows are output a+d*b.
    columns = []
    for j in range(d):
        for i in range(d):
            m = direct_map(matrix_unit(d, i, j), x, y)
            columns.append(sp.Matrix([m[a, b] for b in range(d) for a in range(d)]))
    return sp.Matrix.hstack(*columns)


def choi(d, x, y):
    # J=sum E_ij (input) tensor Phi(E_ij) (output).
    m = sp.zeros(d*d)
    for i in range(d):
        for j in range(d):
            m += sp.kronecker_product(matrix_unit(d, i, j),
                                      direct_map(matrix_unit(d, i, j), x, y))
    return m


def encode(m):
    return [[str(sp.simplify(m[i, j])) for j in range(m.cols)] for i in range(m.rows)]


def main():
    d = 3
    x, y = sp.Rational(1, 4), sp.Rational(1, 4)
    psi = sp.Matrix([sp.I, 1, 0]) / sp.sqrt(2)
    rho = psi * psi.H
    obj = {
        'representation': 'A: direct complex-linear trace/transpose channel',
        'source': 'literature/2405.11216v3.pdf',
        'locator': 'PDF p3 Eqs. (14),(15); PDF p6 Eq. (28)',
        'basis': '0-based computational basis; source |m> maps to local |m-1>',
        'superoperator_index': 'vec_F: row=a+d*b, column=i+d*j',
        'choi_index': 'input tensor output: row=i*d+a, column=j*d+b',
        'symbolic_d3_superoperator': encode(superoperator(d, X_WEIGHT, Y_WEIGHT)),
        'symbolic_d3_choi': encode(choi(d, X_WEIGHT, Y_WEIGHT)),
        'benchmark': {'d': d, 'x': str(x), 'y': str(y),
                      'rho': encode(rho), 'output': encode(direct_map(rho, x, y)),
                      'superoperator': encode(superoperator(d, x, y)),
                      'choi': encode(choi(d, x, y))},
        'independence': 'Written from the direct primary Eq. (14); no B imports or cached B results.'
    }
    path = Path(__file__).with_name('input-a.json')
    path.write_text(json.dumps(obj, indent=2) + '\n')
    print('Generated ' + str(path) + ' from direct primary transcription.')


if __name__ == '__main__':
    main()
