"""Input B: reversed coefficient / SVD. Never reads A or its results."""
import json
from pathlib import Path
import numpy as np
import sympy as sy

HERE = Path(__file__).resolve().parent
TOLERANCE = 5e-12


def coefficient_schmidt(table, n):
    small = np.sqrt(table)
    logical = small.copy()
    for _ in range(n-1):
        logical = np.kron(logical, small)
    dim = logical.shape[0]
    # Directly populate reversed BS:AR coefficient entries.
    reversed_coefficient = np.zeros((dim*dim, dim*dim), dtype=complex)
    for b in range(dim):
        for a in range(dim):
            reversed_coefficient[b*dim+b, a*dim+a] = logical[a, b]
    singular = np.linalg.svd(reversed_coefficient, compute_uv=False)
    probabilities = singular**2
    entropy = -sum(v*np.log2(v) for v in probabilities if v > 1e-14)
    # Independent BA / SR environmental-amplitude representation.
    physical_amplitude = np.diag(logical.T.reshape(-1)).astype(complex)
    rho_ba = physical_amplitude @ physical_amplitude.conj().T
    assert abs(np.trace(rho_ba)-1) < TOLERANCE
    return {"coefficient": reversed_coefficient.real.tolist(),
            "physical_diagonal_ba": np.diag(rho_ba).real.tolist(),
            "physical_offdiagonal_error": float(np.max(np.abs(rho_ba-np.diag(np.diag(rho_ba))))),
            "trace_error": float(abs(sum(probabilities)-1)),
            "weights": probabilities.tolist(), "entropy_bits": float(entropy)}


def symbolic_column_pass():
    u, v, w, t = sy.symbols("x00 x01 x10 x11", nonnegative=True)
    logical = sy.Matrix([[u, v], [w, t]])
    reverse = sy.zeros(4)
    for b in range(2):
        for a in range(2):
            reverse[3*b, 3*a] = logical[a, b]
    gram = (reverse*reverse.T).extract([0,3],[0,3])
    record = json.loads((HERE/"input-b.json").read_text())
    local = {str(s): s for s in (u,v,w,t)}
    transcription = sy.Matrix([[sy.sympify(e, locals=local) for e in row]
                                for row in record["coefficient_matrix"]])
    transcribed_gram = sy.Matrix([[sy.sympify(e, locals=local) for e in row]
                                 for row in record["logical_gram"]])
    assert reverse == transcription and gram == transcribed_gram
    z = sy.Symbol("z")
    actual = sy.factor(gram.charpoly(z).as_expr())
    trace = u*u+v*v+w*w+t*t
    independent = z*z-trace*z+(u*t-v*w)**2
    assert sy.expand(actual-independent) == 0
    return {"method": "reversed coefficient and column Gram",
            "coefficient_transcription_match": True,
            "logical_gram_exact": True,
            "unnormalized_characteristic_polynomial": str(actual),
            "determinant": str(sy.factor(gram.det())),
            "normalized_characteristic_polynomial": "z**2-z+(x00*x11-x01*x10)**2"}


def exact_embedded_limits():
    z = sy.Symbol("z")
    distributions = {
        "uniform_product": [[sy.Rational(1,4)]*2]*2,
        "uniform_correlated": [[sy.Rational(1,2),0],[0,sy.Rational(1,2)]],
        "uniform_anticorrelated": [[0,sy.Rational(1,2)],[sy.Rational(1,2),0]],
        "deterministic": [[1,0],[0,0]]
    }
    records = []
    for name, table in distributions.items():
        base = sy.Matrix([[sy.sqrt(value) for value in row] for row in table])
        for n in (1,2):
            logical = base if n == 1 else sy.kronecker_product(base,base)
            d = 2**n
            reverse = sy.zeros(d*d)
            for b in range(d):
                for a in range(d):
                    reverse[b*d+b,a*d+a] = logical[a,b]
            gram = sy.simplify(reverse*reverse.T)
            polynomial = sy.factor(gram.charpoly(z).as_expr())
            if name in ("uniform_product","deterministic"):
                expected = z**(d*d-1)*(z-1)
                nonzero = ["1"]
                entropy = 0
            else:
                expected = z**(d*d-d)*(z-sy.Rational(1,d))**d
                nonzero = [str(sy.Rational(1,d))]*d
                entropy = n
            assert sy.expand(polynomial-expected) == 0
            records.append({"label":name, "copies":n,
                            "actual_characteristic_polynomial":str(polynomial),
                            "exact_nonzero_spectrum":nonzero,
                            "exact_entropy_bits":entropy})
    return records


def main():
    # Re-entered from the primary benchmark/domain specification, no A file read.
    tables = {
        "uniform_product": ("1/4","1/4","1/4","1/4"),
        "biased_product": ("1/12","1/4","1/6","1/2"),
        "uniform_correlated": ("1/2","0","0","1/2"),
        "uniform_anticorrelated": ("0","1/2","1/2","0"),
        "biased_correlated": ("1/3","0","0","2/3"),
        "deterministic": ("1","0","0","0"),
        "zero_row": ("0","0","1/3","2/3"),
        "asymmetric": ("1/10","1/5","3/10","2/5"),
        "three_support": ("0","1/4","1/4","1/2")
    }
    records = []
    for name, entries in tables.items():
        p = np.array([float(sy.Rational(value)) for value in entries]).reshape(2,2)
        assert (p >= 0).all() and abs(p.sum()-1) < TOLERANCE
        for n in (1,2):
            rec = coefficient_schmidt(p,n)
            rec.update({"label":name,"copies":n,
                        "probability":[list(entries[:2]),list(entries[2:])]})
            records.append(rec)
    result = {"method": "independently populated BS:AR coefficient / squared SVD",
              "symbolic":symbolic_column_pass(), "exact_baselines":exact_embedded_limits(),
              "numeric_tolerance":TOLERANCE, "dtype":"complex128",
              "entropy_zero_cutoff":1e-14,"cases":records}
    (HERE/"result-b.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"implementation":"B","exact_source":"pass",
                      "exact_baselines":len(result["exact_baselines"]),
                      "canonical_cases":len(records),"status":"pass"}))


if __name__ == "__main__":
    main()
