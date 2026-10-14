"""Compare the completed independent passes; supplemental finite-ancilla tests."""
import json
import platform
import sys
import contextlib
import io
from pathlib import Path
import numpy as np
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
TOL = 5e-12


def entropy(q):
    return float(-sum(v*np.log2(v) for v in q if v > 1e-14))


def exact_map():
    variables = sp.symbols("x00 x01 x10 x11", nonnegative=True)
    local = {str(v):v for v in variables}
    inputs = [json.loads((HERE/name).read_text()) for name in ("input-a.json","input-b.json")]
    k = [sp.Matrix([[sp.sympify(e, locals=local) for e in row]
                    for row in rec["coefficient_matrix"]]) for rec in inputs]
    g = [sp.Matrix([[sp.sympify(e, locals=local) for e in row]
                    for row in rec["logical_gram"]]) for rec in inputs]
    assert k[0] == k[1].T
    assert sp.expand(g[0].det()-g[1].det()) == 0
    z = sp.Symbol("z")
    assert sp.expand(g[0].charpoly(z).as_expr()-g[1].charpoly(z).as_expr()) == 0
    print("EXACT: K_B=K_A^T entry by entry; G_A and G_B equal characteristic polynomials.")
    print("EXACT: det(G_A)=det(G_B)=(x00*x11-x01*x10)^2; normalization supplies trace=1.")


def compare_cases(a,b):
    right = {(r["label"],r["copies"]):r for r in b["cases"]}
    rows = []
    max_errors = {"coefficient":0.0,"spectrum":0.0,"entropy_bits":0.0,"physical_marginal":0.0,"reference_entropy_bits":0.0}
    for left in a["cases"]:
        key = (left["label"],left["copies"])
        other = right[key]
        assert left["probability"] == other["probability"]
        d = 2**left["copies"]
        ka, kb = np.array(left["coefficient"]), np.array(other["coefficient"])
        assert np.max(np.abs(ka-kb.T)) < TOL
        diag_a = np.array(left["physical_diagonal_ab"])
        diag_b = np.array(other["physical_diagonal_ba"]).reshape(d,d).T.flatten()
        assert np.max(np.abs(diag_a-diag_b)) < TOL
        # Reconstruct expected physical density in source copy-interleaved order.
        p = np.array([[float(sp.Rational(v)) for v in row] for row in left["probability"]])
        with mp.workdps(80):
            exact_p = [[sp.Rational(v) for v in row] for row in left["probability"]]
            amplitudes = [[mp.sqrt(mp.mpf(int(v.p))/int(v.q)) for v in row]
                          for row in exact_p]
            determinant = (amplitudes[0][0]*amplitudes[1][1]
                           -amplitudes[0][1]*amplitudes[1][0])**2
            discriminant = 1-4*determinant
            # At C=1, 80-digit square-root arithmetic can make zero slightly negative.
            # Exact positivity follows from the normalized Gram; record/check the scale.
            assert discriminant >= -mp.mpf("1e-70")
            plus = (1+mp.sqrt(max(mp.mpf(0),discriminant)))/2
            minus = determinant/plus
            reference = float(-sum(q*mp.log(q,2) for q in (plus,minus) if q > 0))*left["copies"]
        if left["copies"] == 1:
            expected = p.flatten()
        else:
            original = np.kron(p.flatten(),p.flatten()).reshape(2,2,2,2)
            expected = original.transpose(0,2,1,3).flatten()
        errors = {
            "coefficient": float(np.max(np.abs(ka-kb.T))),
            "spectrum": float(np.max(np.abs(np.array(left["weights"])-other["weights"]))),
            "entropy_bits": abs(left["entropy_bits"]-other["entropy_bits"]),
            "reference_entropy_bits": abs(left["entropy_bits"]-reference),
            "physical_marginal": float(max(np.max(np.abs(diag_a-expected)),
                                          np.max(np.abs(diag_a-diag_b)),
                                          left["physical_offdiagonal_error"],
                                          other["physical_offdiagonal_error"]))}
        assert max(errors.values()) < TOL
        for name,value in errors.items():
            max_errors[name] = max(max_errors[name],value)
        print(f"CANONICAL {key}: S_A={left['entropy_bits']:.16g} S_B={other['entropy_bits']:.16g} bits; marginal and basis map PASS")
        rows.append({"label":key[0],"copies":key[1],"source_reference_entropy_bits":reference,
                     "errors":errors,"status":"pass",
                     "reference_scope":"n times the exact single-copy value; for general n=2 cases this is an attainable upper bound only"})
    assert len(right) == len(rows)
    return rows,max_errors


def supplement():
    rng = np.random.default_rng(20261012)
    fixed = [
        np.ones((2,2))/4, np.diag([.5,.5]), np.array([[0,.5],[.5,0]]),
        np.array([[1,0],[0,0]]), np.array([[0,0],[1/3,2/3]]),
        np.array([[0,.25],[.25,.5]])
    ]
    random_tables = [rng.dirichlet(np.ones(4)).reshape(2,2) for _ in range(32)]
    splits = [(1,4),(4,1),(2,2),(2,3),(3,2),(4,3),(3,4),(4,4)]
    largest_marginal_error = largest_norm_error = largest_spectral_error = 0.0
    minimum_spectral_slack = minimum_entropy_slack = float("inf")
    trials = 0
    for p in fixed+random_tables:
        root = np.sqrt(p)
        delta = np.linalg.det(root)**2
        lam_plus = (1+np.sqrt(max(0,1-4*delta)))/2
        lam_minus = delta/lam_plus  # stable at the product endpoint
        target_entropy = entropy([lam_plus,lam_minus])
        for dr,ds in splits:
            # Independent complex auxiliary isometry; not an entropy optimization.
            raw = rng.normal(size=(dr*ds,4))+1j*rng.normal(size=(dr*ds,4))
            env,_ = np.linalg.qr(raw,mode="reduced")
            assert np.max(np.abs(env.conj().T@env-np.eye(4))) < TOL
            tensor = np.zeros((2,2,dr,ds),complex)
            kb = np.zeros((2*ds,2*dr),complex)
            for i in range(2):
                for j in range(2):
                    phi = env[:,2*i+j].reshape(dr,ds)
                    tensor[i,j,:,:] = root[i,j]*phi
                    # separately populated reverse coefficient, transpose not adjoint
                    for s in range(ds):
                        for r in range(dr):
                            kb[j*ds+s,i*dr+r] = root[i,j]*phi[r,s]
            ka = tensor.transpose(0,2,1,3).reshape(2*dr,2*ds)
            assert np.max(np.abs(ka-kb.T)) < TOL
            phys = tensor.reshape(4,dr*ds)
            marginal = phys@phys.conj().T
            err = float(np.max(np.abs(marginal-np.diag(p.flatten()))))
            assert err < TOL
            largest_marginal_error = max(largest_marginal_error,err)
            q_a = np.linalg.eigvalsh(ka@ka.conj().T)[::-1]
            q_b = np.linalg.svd(kb,compute_uv=False)**2
            k = min(len(q_a),len(q_b))
            spectral_error = float(np.max(np.abs(q_a[:k]-q_b[:k])))
            assert spectral_error < TOL
            largest_spectral_error = max(largest_spectral_error,spectral_error)
            assert abs(q_a.sum()-1) < TOL and q_a[-1] > -TOL
            assert q_a[0] <= lam_plus+TOL
            assert np.all(np.cumsum(q_a)[1:] <= 1+TOL)
            minimum_spectral_slack = min(minimum_spectral_slack,lam_plus-q_a[0])
            minimum_entropy_slack = min(minimum_entropy_slack,entropy(q_a)-target_entropy)
            assert entropy(q_a) >= target_entropy-TOL
            x = rng.normal(size=(2,dr))+1j*rng.normal(size=(2,dr))
            y = rng.normal(size=(2,ds))+1j*rng.normal(size=(2,ds))
            x /= np.linalg.norm(x); y /= np.linalg.norm(y)
            overlap = abs(np.einsum("ir,js,ijrs->",x.conj(),y.conj(),tensor))
            norm_bound = np.linalg.norm(x,axis=1)@root@np.linalg.norm(y,axis=1)
            assert overlap <= norm_bound+TOL and norm_bound <= np.sqrt(lam_plus)+TOL
            w = rng.normal(size=(2,ds))+1j*rng.normal(size=(2,ds))
            w /= np.linalg.norm(w)
            actual_norm = np.linalg.norm(ka@w.flatten())
            compressed_norm = np.linalg.norm(root@np.linalg.norm(w,axis=1))
            violation = max(0,actual_norm-compressed_norm,compressed_norm-np.sqrt(lam_plus))
            assert violation < TOL
            largest_norm_error = max(largest_norm_error,float(violation))
            trials += 1
    return {"trials":trials,"fixed_tables":len(fixed),"random_tables":len(random_tables),
            "auxiliary_splits":[list(s) for s in splits],"rng_seed":20261012,
            "largest_marginal_error":largest_marginal_error,
            "largest_spectrum_disagreement":largest_spectral_error,
            "largest_norm_chain_violation":largest_norm_error,
            "minimum_largest_weight_slack":float(minimum_spectral_slack),
            "minimum_entropy_slack_bits":float(minimum_entropy_slack),
            "status":"pass","meaning":"finite floating-point diagnostics, not a proof of arbitrary dimension or two-copy additivity"}


def main():
    print("COMMAND: python3 evidence/reproduction/compare_and_baseline.py")
    print(f"ENVIRONMENT: Python {platform.python_version()}, NumPy {np.__version__}, SymPy {sp.__version__}")
    print("NUMERIC: complex128, absolute tolerance 5e-12, entropy cutoff 1e-14; exact polynomials certify the 0/1/2-bit baseline values.")
    comparison_output = io.StringIO()
    with contextlib.redirect_stdout(comparison_output):
        exact_map()
    a = json.loads((HERE/"result-a.json").read_text())
    b = json.loads((HERE/"result-b.json").read_text())
    exact_b = {(r["label"],r["copies"]):r for r in b["exact_baselines"]}
    for row in a["exact_baselines"]:
        other = exact_b[(row["label"],row["copies"])]
        assert row["exact_nonzero_spectrum"] == other["exact_nonzero_spectrum"]
        assert row["exact_entropy_bits"] == other["exact_entropy_bits"]
        print(f"PUBLISHED BASELINE {row['label']} n={row['copies']}: exact nonzero spectrum {row['exact_nonzero_spectrum']}; S={row['exact_entropy_bits']} bits PASS")
    with contextlib.redirect_stdout(comparison_output):
        rows,errors = compare_cases(a,b)
    print(comparison_output.getvalue(),end="")
    (HERE/"input-comparison.log").write_text(
        "COMMAND: compare_and_baseline.py; captured exact-map and case-comparison output from this execution.\n"
        +comparison_output.getvalue()+"MAX_ERRORS: "+json.dumps(errors,sort_keys=True)+"\n")
    random_checks = supplement()
    print("SUPPLEMENT: "+json.dumps(random_checks,sort_keys=True))
    result = {"status":"pass","exact_entry_and_characteristic_map":"pass",
              "published_exact_baseline_cases":len(a["exact_baselines"]),
              "comparison_cases":rows,"max_errors":errors,"supplement":random_checks,
              "limitations":"Known one-copy and special tensor-power results only; no new optimization, no universal two-copy result, no referee acceptance."}
    (HERE/"comparison-results.json").write_text(json.dumps(result,indent=2)+"\n")
    print("RESULT: PASS; reproduction only.")


if __name__ == "__main__":
    main()
