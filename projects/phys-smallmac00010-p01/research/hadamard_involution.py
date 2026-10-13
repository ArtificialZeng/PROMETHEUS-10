"""Exact noncirculant U(4) noise-ray witness from a real flat basis.

The identity checked here is a proposed scoped construction, not a proof
of the full U(4) star-shapedness question.
"""

import json
import sympy as sp


H = sp.Matrix([[1, 1, 1, 1], [1, -1, 1, -1],
               [1, 1, -1, -1], [1, -1, -1, 1]])
F = H / 2
v = sp.Matrix([1, 2, 3, 5])
P = v * v.T / (v.T * v)[0]
S = sp.eye(4) - 2 * P
U = F * S
lam = sp.symbols("lam", real=True)
s, t = sp.symbols("s t", real=True)
V = s * U + sp.I * t * F
W = sp.ones(4) / 4
B = U.multiply_elementwise(U)
M = (1 - lam) * B + lam * W

assert F * F.T == S * S.T == U * U.T == sp.eye(4)
assert S * S == sp.eye(4)
assert U * F.T == F * U.T
assert sp.simplify(V * V.conjugate().T - (s*s + t*t)*sp.eye(4)) == sp.zeros(4)
assert sp.simplify(V.multiply_elementwise(V.conjugate()) - (s*s*B + t*t*W)) == sp.zeros(4)

def ms(row):
    return sorted([B[row, j] for j in range(4)])

row_multisets = [list(map(str, ms(i))) for i in range(4)]
assert len(set(tuple(x) for x in row_multisets)) > 1

# A rank-two projector yields the maximal-dimensional Grassmannian
# component of the quadrature family. Differentiate four independent
# bistochastic coordinates along all six antisymmetric generators.
w = sp.Matrix([2, -1, 0, 0])
assert (v.T*w)[0] == 0
P2 = P + w*w.T/(w.T*w)[0]
assert P2*P2 == P2 and P2.T == P2 and sp.trace(P2) == 2
U2 = F*(sp.eye(4)-2*P2)
B2 = U2.multiply_elementwise(U2)
assert len({tuple(sorted(B2[i,j] for j in range(4))) for i in range(4)}) > 1
columns = []
for i in range(4):
    for j in range(i+1,4):
        Omega = sp.zeros(4)
        Omega[i,j], Omega[j,i] = 1, -1
        dP = Omega*P2-P2*Omega
        dU = -2*F*dP
        dB = 2*U2.multiply_elementwise(dU)
        columns.append(sp.Matrix([dB[i,j] for i in range(3) for j in range(3)]))
J = sp.Matrix.hstack(*columns)
minor = sp.factor(J.extract([0,1,2,3],[0,1,2,3]).det())
assert minor != 0 and J.rank() == 4

def arr(A):
    return [[str(sp.simplify(A[i, j])) for j in range(A.cols)]
            for i in range(A.rows)]

out = {
    "scope": "For any real normalized flat F and any real symmetric orthogonal S, U=FS has an exact uniform-noise unistochastic ray V=sqrt(1-lambda)U+i sqrt(lambda)F, 0<=lambda<=1.",
    "proof": "S^T=S and S^2=I imply UF^T=F U^T. Therefore VV^dagger=(1-lambda)UU^T+lambda FF^T+i sqrt(lambda(1-lambda))(FU^T-UF^T)=I. Real U,F make entrywise cross terms vanish, so |V_ij|^2=(1-lambda)U_ij^2+lambda F_ij^2.",
    "H": arr(H), "F": arr(F), "vector_v": arr(v),
    "P": arr(P), "S": arr(S), "U": arr(U), "B": arr(B),
    "row_multisets_B": row_multisets,
    "noncirculant_reason": "A row/column permutation of any circulant matrix has equal entry multisets in every row; this B does not.",
    "rank_two_component": {
        "projector": arr(P2), "U": arr(U2), "B": arr(B2),
        "P_squared_equals_P": True,
        "four_by_four_tangent_minor": str(minor),
        "tangent_rank_of_probability_image": J.rank(),
        "interpretation": "The rank-two projector component is Gr(2,4), of dimension four. This nonzero exact Jacobian minor proves the associated B matrices have local dimension four at this algebraic example; the 4x4 noncirculant ray family is not merely an isolated point.",
    },
    "lambda_half_M": arr(M.subs(lam, sp.Rational(1, 2))),
    "lambda_half_V": arr(V.subs({s: sp.sqrt(sp.Rational(1, 2)), t: sp.sqrt(sp.Rational(1, 2))})),
    "exact_checks": {
        "F_orthogonal": True, "S_symmetric_involution": True,
        "U_orthogonal": True, "all_lambda_unitary": True,
        "all_lambda_moduli": True, "noncirculant_up_to_row_column_permutation": True,
    },
    "limitation": "This establishes a restricted sufficient family, not general U(4) star-shapedness and not a counterexample. Novelty and value require separate primary-literature review.",
}
print(json.dumps(out, indent=2))
