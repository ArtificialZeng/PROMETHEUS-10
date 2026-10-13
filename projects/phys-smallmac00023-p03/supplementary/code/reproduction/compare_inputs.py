"""Entrywise exact comparison and physical input checks; A/B created separately."""
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
t, s = sp.symbols("t s", nonnegative=True)
lam = sp.symbols("lam", nonnegative=True)
local = {"t":t, "s":s, "lam":lam}

def read_matrix(rows):
    return sp.Matrix([[sp.sympify(z, locals=local) for z in row] for row in rows])

def reduced(z):
    # All B Choi entries contain even s powers. Exact polynomial remainder,
    # with s^2+t^2=1, is valid including both physical endpoints.
    return sp.simplify(sp.rem(sp.expand(z), s*s+t*t-1, s))

def trace_b(J, d):
    return sp.Matrix(d, d, lambda m,n: sum(J[d*m+b,d*n+b] for b in range(d)))

if __name__ == "__main__":
    a = json.loads((ROOT/"evidence/input-a.json").read_text())
    b = json.loads((ROOT/"evidence/input-b.json").read_text())
    A = read_matrix(a["choi_ab"])
    B = read_matrix(b["choi_ba"])
    R = read_matrix(b["reverse_order_choi_ba"])
    P = sp.zeros(9)
    # v_AB=P v_BA, with P[3*m+b,3*b+m]=1: actual reshuffling, no transpose.
    for m in range(3):
        for out in range(3):
            P[3*m+out,3*out+m] = 1
    assert P*P.T == sp.eye(9)
    mapped = P*B*P.T
    source = A.subs(lam,t*t).applyfunc(sp.simplify)
    print("Convention map: lambda=t^2, 1-lambda=s^2, t,s>=0; gamma=ln2.")
    print("Tensor map P[3*m+b,3*b+m]=1; J_AB=P J_BA P^T.")
    print("Kraus beam-splitter loss branch signs (-1)^ell cancel within each outer product.")
    matches = 0
    for i in range(9):
        for j in range(9):
            residual = reduced(source[i,j]-mapped[i,j])
            print(f"entry ({i},{j}): A={source[i,j]}, B_mapped={reduced(mapped[i,j])}, residual={residual}")
            assert residual == 0, (i,j,residual)
            matches += 1
    print(f"EXACT PASS: {matches}/81 qutrit matrix entries, zero tolerance, no fitting.")
    assert (B-R).applyfunc(reduced) == sp.zeros(9)
    assert A == A.T
    assert (trace_b(A,3)-sp.eye(3)/3).applyfunc(sp.simplify) == sp.zeros(3)
    assert sp.simplify(sp.trace(A)) == 1
    completeness = sp.zeros(3)
    for row in b["composed_kraus"]:
        K = read_matrix(row)
        completeness += K.T*K
    assert (completeness-sp.eye(3)).applyfunc(reduced) == sp.zeros(3)
    print("PASS: both loss/dephasing composition orders agree exactly.")
    print("PASS: Hermiticity, Tr(J)=1, Tr_B(J)=I_3/3.")
    print("PASS: sum_K K^dagger K=I_3 on t^2+s^2=1; outer products imply complete positivity for every physical lambda.")
    for endpoint in [0,1]:
        target = sp.zeros(9)
        if endpoint == 0:
            for m in range(3): target[3*m,3*m] = sp.Rational(1,3)
        else:
            gram = read_matrix(b["gaussian_gram"])
            for m in range(3):
                for n in range(3): target[4*m,4*n] = gram[m,n]/3
        assert (A.subs(lam,endpoint)-target).applyfunc(sp.simplify) == sp.zeros(9)
        print(f"PASS: lambda={endpoint} exact reference limit.")
    permutation = [int(next(j for j in range(9) if P[i,j])) for i in range(9)]
    (ROOT/"evidence/convention-map.json").write_text(json.dumps({
        "ab_order":a["basis"], "ba_order":b["basis"],
        "ab_index_to_ba_index":permutation,
        "parameter_map":"lam=t^2, s^2=1-t^2, 0<=t<=1, s>=0",
        "matrix_map":"J_AB=P J_BA P^T, P[3*m+b,3*b+m]=1",
        "normalization":"Both representations use normalized Choi state (divide by d); unnormalized Choi would be d*J.",
        "environment_phase":"B preserves Eq.(19) (-1)^ell branch signs; rephasing environment |ell> by (-1)^ell yields positive-loss Kraus without changing the channel.",
        "comparison":"81 exact entries match after polynomial reduction s^2+t^2=1",
        "independence_limit":"Same agent and SymPy shared. B was initially derived/run before A; a local matrix-accumulation bug was corrected after the first comparison. The repaired B code never reads A inputs/outputs or imports A. Debugging feedback is shared; no independent referee audit claimed.",
    },indent=2)+"\n")
