"""Reproduce primary Eq.(62), Lemma7, Theorem38 and Lemma39 Fact3 exactly."""
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
lam, r = sp.symbols("lam r", nonnegative=True)
J = sp.Matrix([[1,0,0,sp.sqrt(r*lam)], [0,0,0,0],
               [0,0,1-lam,0], [sp.sqrt(r*lam),0,0,lam]])/2

if __name__ == "__main__":
    a = json.loads((ROOT/"evidence/input-a.json").read_text())
    transcribed = sp.Matrix([[sp.sympify(z,locals={"lam":lam}) for z in row] for row in a["qubit_choi_ab"]])
    assert (J.subs(r,sp.Rational(1,2))-transcribed).applyfunc(sp.simplify) == sp.zeros(4)
    output = sp.Matrix(2,2,lambda b,c:sum(J[2*m+b,2*m+c] for m in range(2)))
    purity_b = sp.simplify(sp.trace(output*output))
    purity_j = sp.simplify(sp.trace(J*J))
    determinant = sp.simplify(J.det())
    gap = sp.factor(purity_b-purity_j+4*sp.sqrt(determinant))
    assert sp.simplify(gap-(1-lam*(1+r))/2) == 0
    print("Eq.(62) transcribed explicitly in |00>,|01>,|10>,|11>, tensor A,B, normalized 1/2.")
    print("PASS: all 16 entries agree with the separately generated Lemma25 qubit restriction at gamma=ln2.")
    print("r=exp(-gamma), not exp(-gamma/2); coherence is sqrt(r*lambda)/2.")
    print("rho_B =", output)
    print("Tr(rho_B^2) =", purity_b)
    print("Tr(J^2) =", purity_j)
    print("det(J) =", determinant)
    print("Lemma7 symmetric-extension gap =", gap)
    print("For lambda in [0,1], r in (0,1], gap>=0 iff lambda<=1/(1+r).")
    threshold = sp.simplify((1/(1+r)).subs(r,sp.Rational(1,2)))
    assert threshold == sp.Rational(2,3)
    print("EXACT PASS: published lambda_2(ln2) =", threshold)
    for point in [sp.Rational(0),sp.Rational(1,2),threshold,sp.Rational(3,4),sp.Rational(1)]:
        val = gap.subs({r:sp.Rational(1,2),lam:point})
        print(f"lambda={point}: gap={val}, symmetric-extension criterion={val>=0}")
    assert sp.simplify((1/(1+r)).subs(r,1)) == sp.Rational(1,2)
    assert sp.limit(1/(1+r),r,0,dir="+") == 1
    print("PASS: gamma=0 pure-loss qubit boundary 1/2; gamma->infinity boundary tends to 1.")
    # Additional exact baseline endpoint extension, independently checked by
    # direct partial traces; does not certify the qutrit target.
    v = sp.zeros(8,1)
    v[0] = sp.sqrt(sp.Rational(1,2))  # |000>
    v[5] = sp.sqrt(sp.Rational(1,6))  # |101>
    v[6] = sp.sqrt(sp.Rational(1,6))  # |110>
    w = sp.zeros(8,1)
    w[7] = sp.sqrt(sp.Rational(1,6))  # |111>
    X = v*v.T+w*w.T
    S = sp.zeros(8)
    for aa in range(2):
        for b in range(2):
            for c in range(2): S[4*aa+2*b+c,4*aa+2*c+b]=1
    marginal = sp.Matrix(4,4,lambda i,j:sum(X[2*i+c,2*j+c] for c in range(2)))
    reference = J.subs({lam:threshold,r:sp.Rational(1,2)})
    assert (marginal-reference).applyfunc(sp.simplify) == sp.zeros(4)
    assert S*X*S.T == X and sp.trace(X)==1
    eigenvalues = X.eigenvals()
    assert eigenvalues == {sp.Rational(5,6):1,sp.Rational(1,6):1,sp.Integer(0):6}
    print("PASS: explicit 8x8 qubit endpoint extension is PSD, swap invariant, normalized; both AB marginals reproduce J.")
    print("Endpoint extension eigenvalues:",eigenvalues)
    data={"published_source":"Mele et al. arXiv:2401.15634v3",
          "locators":"Eq.(62), Lemma7 (unnumbered qubit criterion), Theorem38 Proof3, Lemma39 Fact3",
          "exact_threshold":"2/3", "gap_general":str(gap),
          "method":"Exact symbolic substitution, determinant and trace identities; Lemma7 is used only for two qubits.",
          "precision":"Exact rational/algebraic/symbolic expressions, zero residual; no SDP, finite-tolerance feasibility, statistical fit or discretization.",
          "endpoint_extension_basis":"A,B1,B2 lexicographic number basis",
          "endpoint_extension":[[str(z) for z in X.row(i)] for i in range(8)],
          "endpoint_extension_eigenvalues":["5/6","1/6","0 (multiplicity 6)"],
          "scope":"Published qubit baseline only. The qutrit gamma=ln2 endpoint, any improved bracket, and Fig.4 numerical point remain uncomputed."}
    (ROOT/"evidence/qubit-baseline.json").write_text(json.dumps(data,indent=2)+"\n")
