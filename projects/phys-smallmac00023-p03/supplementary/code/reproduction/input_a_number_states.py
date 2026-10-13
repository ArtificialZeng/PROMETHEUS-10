"""Representation A: direct transcription of primary Lemma25, all number pairs."""
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
lam = sp.symbols("lam", nonnegative=True)

def reconstruct(d):
    J = sp.zeros(d*d)
    action = []
    for m in range(d):
        for n in range(d):
            output = sp.zeros(d)
            # The Gaussian coefficient is transcribed directly from Lemma25.
            dephasing = sp.Pow(2, -sp.Rational((m-n)**2, 2))
            for ell in range(min(m, n)+1):
                coefficient = dephasing * sp.sqrt(sp.binomial(m, ell)*sp.binomial(n, ell))
                coefficient *= (1-lam)**ell * lam**(sp.Rational(m+n, 2)-ell)
                output[m-ell, n-ell] += coefficient
                J[d*m+m-ell, d*n+n-ell] += coefficient/d
            action.append({"m":m, "n":n,
                           "output": [[str(sp.simplify(z)) for z in output.row(i)] for i in range(d)]})
    return J.applyfunc(sp.simplify), action

if __name__ == "__main__":
    J, action = reconstruct(3)
    J2, action2 = reconstruct(2)
    data = {
        "construction": "Direct transcription of the full action formula in Mele et al. Lemma25; loop over all 9 matrix units and allowed photon losses; normalized maximally entangled input",
        "source_locator": "Lemma25 (unnumbered channel formula), Definition33/Eq.(59), normalized Choi Definition2/Eq.(12)",
        "basis": [f"|{m}>_A|{b}>_B" for m in range(3) for b in range(3)],
        "parameters": "lam=lambda in [0,1] (transmissivity); gamma=ln(2)",
        "choi_normalization": "sum_mn |m><n|_A tensor N(|m><n|)_B / 3",
        "channel_matrix_units": action,
        "choi_ab": [[str(z) for z in J.row(i)] for i in range(9)],
        "qubit_choi_ab": [[str(z) for z in J2.row(i)] for i in range(4)],
        "qubit_matrix_units": action2,
    }
    (ROOT / "evidence/input-a.json").write_text(json.dumps(data, indent=2)+"\n")
    print("A directly reconstructed for each matrix unit from Lemma25.")
    for i in range(9):
        print("row", i, list(J.row(i)))
    print("Saved qutrit and qubit normalized A,B Choi matrices.")
