#!/usr/bin/env python3
"""Check the newly typeset Schur response matrix against the defining form."""
import json
import sympy as s

ar, ai, dr, di, t = s.symbols("ar ai dr di t", real=True)
a, d = ar + s.I * ai, dr + s.I * di
A = s.Matrix([[a, t], [0, d]])
P = s.kronecker_product(A.T, s.eye(2))
Q = s.kronecker_product(s.eye(2), A)
H = P.conjugate().T * P + Q.conjugate().T * Q / 2
H -= 3 * (P.conjugate().T * Q + Q.conjugate().T * P) / 4
h22 = a * s.conjugate(a) + d * s.conjugate(d) / 2 + 3 * t**2 / 2
h22 -= 3 * s.re(s.conjugate(a) * d) / 2
h33 = d * s.conjugate(d) + a * s.conjugate(a) / 2
h33 -= 3 * s.re(s.conjugate(a) * d) / 2
display = s.Matrix([
    [t**2, -s.conjugate(a)*t/4, t*(d-3*a/4), -3*t**2/4],
    [-a*t/4, h22, 0, t*d/4],
    [t*(s.conjugate(d)-3*s.conjugate(a)/4), 0, h33,
     t*(s.conjugate(a)/2-3*s.conjugate(d)/4)],
    [-3*t**2/4, t*s.conjugate(d)/4, t*(a/2-3*d/4), t**2/2],
])
residuals = [s.expand(z) for z in H - display]
assert all(z == 0 for z in residuals)
print(json.dumps({
    "check": "typeset Schur response matrix",
    "method": "exact polynomial subtraction from column-vectorized defining form",
    "coverage": "ar,ai,dr,di,t arbitrary real; q=1/2",
    "residuals": [str(z) for z in residuals],
    "scope": "transcription check of an accepted auxiliary identity; not fresh scientific acceptance"
}, indent=2))
