"""Input A: full tensor / partial trace. Does not import or read B."""
import json
from pathlib import Path
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
TOL = 5e-12


def tensor_trace(probability, copies):
    d = 2**copies
    weight = np.zeros((d, d))
    ket = np.zeros((d, d, d, d), dtype=np.complex128)  # A B R S
    for i in range(d):
        for j in range(d):
            w = 1.0
            for k in range(copies):
                w *= probability[(i >> k) & 1, (j >> k) & 1]
            weight[i, j] = w
            ket[i, j, i, j] = np.sqrt(w)
    physical_environment = ket.reshape(d*d, d*d)
    physical = physical_environment @ physical_environment.conj().T
    reduced = np.einsum("ijrs,kjts->irkt", ket, ket.conj()).reshape(d*d, d*d)
    coefficient = ket.transpose(0, 2, 1, 3).reshape(d*d, d*d)
    q = np.linalg.eigvalsh(reduced)[::-1]
    entropy = float(-sum(v*np.log2(v) for v in q if v > 1e-14))
    marginal_error = float(np.max(np.abs(physical-np.diag(weight.flatten()))))
    assert marginal_error < TOL
    assert abs(np.trace(reduced)-1) < TOL and q[-1] > -TOL
    return {
        "coefficient": coefficient.real.tolist(),
        "physical_diagonal_ab": np.diag(physical).real.tolist(),
        "physical_offdiagonal_error": marginal_error,
        "trace_error": float(abs(np.trace(reduced)-1)),
        "weights": q.tolist(), "entropy_bits": entropy
    }


def exact_source_check():
    symbols = sp.symbols("x00 x01 x10 x11", nonnegative=True)
    x00, x01, x10, x11 = symbols
    amp = [[x00, x01], [x10, x11]]
    def t(i, j, r, s):
        return amp[i][j] if (i == r and j == s) else sp.Integer(0)
    # Direct four-index contractions, rather than a compressed Gram shortcut.
    reduced = sp.Matrix(4, 4, lambda row, col:
        sum(t(row//2, j, row%2, s)*t(col//2, j, col%2, s)
            for j in range(2) for s in range(2)))
    physical = sp.Matrix(4, 4, lambda row, col:
        sum(t(row//2, row%2, r, s)*t(col//2, col%2, r, s)
            for r in range(2) for s in range(2)))
    k = sp.Matrix(4, 4, lambda row, col: t(row//2, col//2, row%2, col%2))
    record = json.loads((HERE/"input-a.json").read_text())
    loc = {str(s): s for s in symbols}
    transcribed = sp.Matrix([[sp.sympify(v, locals=loc) for v in row]
                             for row in record["coefficient_matrix"]])
    transcribed_g = sp.Matrix([[sp.sympify(v, locals=loc) for v in row]
                               for row in record["logical_gram"]])
    assert k == transcribed
    g = reduced.extract([0, 3], [0, 3])
    assert g == transcribed_g
    assert physical == sp.diag(x00**2, x01**2, x10**2, x11**2)
    determinant = sp.factor(g.det())
    assert determinant == (x00*x11-x01*x10)**2
    return {"method": "explicit tensor contractions",
            "coefficient_transcription_match": True,
            "physical_marginal_exact": True,
            "logical_gram_exact": True, "determinant": str(determinant),
            "trace": str(sp.trace(g)),
            "normalized_characteristic_polynomial": "z**2-z+(x00*x11-x01*x10)**2"}


def exact_baselines():
    z = sp.Symbol("z")
    matrices = {
        "uniform_product": sp.ones(2)/2,
        "uniform_correlated": sp.eye(2)/sp.sqrt(2),
        "uniform_anticorrelated": sp.Matrix([[0,1],[1,0]])/sp.sqrt(2),
        "deterministic": sp.Matrix([[1,0],[0,0]])
    }
    result = []
    for label, m in matrices.items():
        for n in (1, 2):
            mn = m if n == 1 else sp.kronecker_product(m, m)
            g = sp.simplify(mn*mn.T)
            actual = sp.factor(g.charpoly(z).as_expr())
            d = 2**n
            if label in ("uniform_product", "deterministic"):
                expected = z**(d-1)*(z-1)
                q = ["1"]+["0"]*(d-1)
                bits = 0
            else:
                expected = (z-sp.Rational(1,d))**d
                q = [str(sp.Rational(1,d))]*d
                bits = n
            assert sp.expand(actual-expected) == 0
            result.append({"label": label, "copies": n,
                           "actual_characteristic_polynomial": str(actual),
                           "exact_nonzero_spectrum": [v for v in q if v != "0"],
                           "exact_entropy_bits": bits})
    return result


def main():
    # Independently entered rational tables, including source endpoint limits.
    cases = [
        ("uniform_product", [["1/4","1/4"],["1/4","1/4"]]),
        ("biased_product", [["1/12","1/4"],["1/6","1/2"]]),
        ("uniform_correlated", [["1/2","0"],["0","1/2"]]),
        ("uniform_anticorrelated", [["0","1/2"],["1/2","0"]]),
        ("biased_correlated", [["1/3","0"],["0","2/3"]]),
        ("deterministic", [["1","0"],["0","0"]]),
        ("zero_row", [["0","0"],["1/3","2/3"]]),
        ("asymmetric", [["1/10","1/5"],["3/10","2/5"]]),
        ("three_support", [["0","1/4"],["1/4","1/2"]])
    ]
    results = []
    for label, rational in cases:
        p = np.array([[float(sp.Rational(v)) for v in row] for row in rational])
        assert np.all(p >= 0) and abs(p.sum()-1) < TOL
        for n in (1, 2):
            result = tensor_trace(p, n)
            result.update({"label": label, "copies": n, "probability": rational})
            results.append(result)
    packet = {"method": "A B R S tensor and explicit partial trace / Hermitian eigensolver",
              "symbolic": exact_source_check(), "exact_baselines": exact_baselines(),
              "numeric_tolerance": TOL, "dtype": "complex128",
              "entropy_zero_cutoff": 1e-14, "cases": results}
    (HERE/"result-a.json").write_text(json.dumps(packet, indent=2)+"\n")
    print(json.dumps({"implementation": "A", "exact_source": "pass",
                      "exact_baselines": len(packet["exact_baselines"]),
                      "canonical_cases": len(results), "status": "pass"}))


if __name__ == "__main__":
    main()
