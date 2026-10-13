"""Independent representation B: primary beam splitter + Gaussian phase integral.

This module never imports input A or reads its files. The same worker writes both
representations, so this is implementation/derivation independence, not a fresh audit.
"""
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
t, s = sp.symbols("t s", nonnegative=True)
x, y, phi = sp.symbols("x y phi", real=True)
g = sp.symbols("g", positive=True)

def matrix_data(M):
    return [[str(sp.simplify(M[i, j])) for j in range(M.cols)] for i in range(M.rows)]

def reconstruct():
    # Lemma9/Eq.(18): a^dagger -> t a_B^dagger - s a_E^dagger.
    # Expand transformed creation polynomial; factorials convert monomials to
    # normalized number states. No channel-action or Choi formula from A is used.
    loss = [sp.zeros(3) for _ in range(3)]
    polynomials = []
    for n in range(3):
        polynomial = sp.Poly(sp.expand((t*x-s*y)**n / sp.sqrt(sp.factorial(n))), x, y)
        polynomials.append(str(polynomial.as_expr()))
        for (b, e), coefficient in polynomial.terms():
            loss[e][b, n] = coefficient * sp.sqrt(sp.factorial(b)*sp.factorial(e))

    # Definition17 and Eq.(24), independently from the channel formula.
    characteristic = []
    for k in range(3):
        integral = sp.integrate(sp.exp(-phi**2/(2*g))*sp.cos(k*phi)/sp.sqrt(2*sp.pi*g),
                                (phi, -sp.oo, sp.oo))
        integral = sp.simplify(integral)
        assert sp.simplify(integral-sp.exp(-g*k*k/2)) == 0
        characteristic.append(integral)
    gram = sp.Matrix(3, 3, lambda b, c: sp.simplify(characteristic[abs(b-c)].subs(g, sp.log(2))))
    factor = gram.cholesky()
    assert (factor*factor.T-gram).applyfunc(sp.simplify) == sp.zeros(3)
    dephase = [sp.diag(*factor[:, j]) for j in range(3)]
    # Dephasing follows loss in B; A transcribes a pre-factor on input coherences.
    kraus = [D*L for L in loss for D in dephase]
    reverse = [L*D for L in loss for D in dephase]
    matrices = []
    for operators in [kraus, reverse]:
        destination = sp.zeros(9)
        for K in operators:
            # Output-first row vectorization: index 3*b+m, tensor order B,A.
            v = sp.Matrix([K[b, m] for b in range(3) for m in range(3)])
            destination += v*v.T/3
        matrices.append(destination)
    J_ba, J_ba_reverse = matrices
    return {
        "construction": "Expansion of (t*x-s*y)^n/sqrt(n!), n=0,1,2, and exact Gaussian characteristic integrals; Gram-Cholesky dephasing Kraus; outer products of output-first Kraus vectors",
        "source_locators": "Lemma9/Eq.(18), Lemma10/Eq.(19), Definition17/Eq.(24), Definition33/Eq.(59)",
        "basis": [f"|{b}>_B|{m}>_A" for b in range(3) for m in range(3)],
        "parameters": "t=sqrt(lambda), s=sqrt(1-lambda), t,s>=0, t^2+s^2=1; gamma=ln(2)",
        "choi_normalization": "sum_K |vec_BA(K)><vec_BA(K)| / 3",
        "creation_polynomials": polynomials,
        "gaussian_characteristic": [str(z) for z in characteristic],
        "gaussian_gram": matrix_data(gram), "gram_factor": matrix_data(factor),
        "loss_kraus": [matrix_data(K) for K in loss],
        "dephasing_kraus": [matrix_data(K) for K in dephase],
        "composed_kraus": [matrix_data(K) for K in kraus],
        "choi_ba": matrix_data(J_ba),
        "reverse_order_choi_ba": matrix_data(J_ba_reverse),
        "independence": "No import of A and no read of A inputs, outputs or cached Choi entries. Same human-model worker and SymPy are shared; not an independent referee.",
    }

if __name__ == "__main__":
    data = reconstruct()
    (ROOT / "evidence/input-b.json").write_text(json.dumps(data, indent=2)+"\n")
    print("B reconstructed from creation polynomials and Gaussian integrals.")
    print("Loss Kraus:", data["loss_kraus"])
    print("Gaussian characteristic:", data["gaussian_characteristic"])
    print("Dephasing Gram:", data["gaussian_gram"])
    print("Cholesky factor:", data["gram_factor"])
    print("Saved output-first 9x9 Choi and reverse-composition matrix.")
