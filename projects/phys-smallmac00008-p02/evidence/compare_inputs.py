#!/usr/bin/env python3
"""Post-transcription convention-map comparison of independently prepared inputs A and B."""
import json
import sympy as sp

with open("evidence/input-a.json", encoding="utf-8") as f:
    a = json.load(f)
with open("evidence/input-b.json", encoding="utf-8") as f:
    b = json.load(f)

env = {"sqrt": sp.sqrt, "pi": sp.pi, "I": sp.I, "exp": sp.exp}
def val(s): return sp.sympify(s, locals=env)
def rows(x): return sp.Matrix([[val(z) for z in row] for row in x])
def actions(x):
    cols = [sp.Matrix([val(z) for z in image]) for image in x]
    return sp.Matrix.hstack(*cols)

names = ["T1", "T2", "T3"]
direct = [rows(a["kraus_matrices"][n]) for n in names]
action = [actions(b["original_actions"][n]) for n in names]
u = rows(a["specialization"]["U"])
mixed_a = [sp.simplify(sum((u[i, j] * direct[j] for j in range(3)), sp.zeros(2))) for i in range(3)]
mixed_b = [actions(b["derived_mixed_actions"][f"K{i+1}"]) for i in range(3)]
original_residuals = [sp.simplify(direct[i] - action[i]) for i in range(3)]
mixed_residuals = [sp.simplify(mixed_a[i] - mixed_b[i]) for i in range(3)]
assert all(x == sp.zeros(2) for x in original_residuals + mixed_residuals)
assert sp.simplify(u.T * u) == sp.eye(3)
print(json.dumps({
    "comparison": "exact",
    "basis_map": "B's successive ket images are exactly A's matrix columns; both use rows=output, columns=input.",
    "environment_map": "A's U rows multiply (T1,T2,T3)^T and reproduce B's independently derived K1,K2,K3 actions.",
    "choi_map": "column-major vec(K) orders input first and output second: (K00,K10,K01,K11).",
    "original_matrix_residuals": [[[str(v) for v in row] for row in x.tolist()] for x in original_residuals],
    "mixed_matrix_residuals": [[[str(v) for v in row] for row in x.tolist()] for x in mixed_residuals],
    "u_transpose_u": [[str(v) for v in row] for row in (u.T*u).tolist()]
}, indent=2, sort_keys=True))
