#!/usr/bin/env python3
"""Compare already completed independent A and B; never generate one from the other."""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
mp.mp.dps = 80
TOLERANCE_SPECTRUM = 1e-11
TOLERANCE_LOGS = mp.mpf("1e-70")


def main():
    A = json.loads((ROOT / "evidence/input-a.json").read_text())
    B = json.loads((ROOT / "evidence/input-b.json").read_text())
    assert len(A["cases"]) == len(B["cases"]) == 5
    comparisons = []
    print("CONVENTION MAP: A i=0..6 <-> B/source j=i+1. R_A = transpose(Q_B).")
    print("Fourier + modes: z_A(m)=z_B((-m) mod n); the spectrum is unchanged by transpose.")
    print("B is a backward generator acting on functions, not a forward probability-row generator.")
    for a, b in zip(A["cases"], B["cases"]):
        assert a["name"] == b["name"]
        n = a["n"]
        R = a["column_generator_R"]
        Q = b["row_backward_generator_Q"]
        row_matches = [R[j] == [Q[k][j] for k in range(n)] for j in range(n)]
        assert all(row_matches)
        assert all(sp.Rational(x) == sp.Rational(y) for x, y in zip(a["stationary_exact"], b["stationary_exact"]))
        assert all(sp.Rational(x) == sp.Rational(y) for x, y in zip(a["currents_exact"], b["currents_exact"]))
        sigma_error = abs(mp.mpf(a["sigma_edge_once"]) - mp.mpf(b["sigma_tree_flux"]))
        assert sigma_error < TOLERANCE_LOGS
        entry = {"case": a["name"], "matrix_rows_exact_match": row_matches,
                 "stationary_and_current_exact_match": True,
                 "entropy_error": mp.nstr(sigma_error, 12)}
        if "spectra_backward_by_m" in b:
            assert a["characteristic_polynomial_coefficients"] == b["characteristic_polynomial_resultant_coefficients"]
            eigen_A = np.array([complex(*z) for z in a["eigenvalues_scipy"]])
            eigen_B = np.array([complex(float(z[0]), float(z[1])) for z in b["spectra_backward_by_m"]])
            distances = np.abs(eigen_A[:, None] - eigen_B[None, :])
            rows, modes = linear_sum_assignment(distances)
            assert len(set(modes.tolist())) == n
            error = float(max(distances[j, m] for j, m in zip(rows, modes)))
            assert error < TOLERANCE_SPECTRUM
            entry.update({"characteristic_polynomial_exact_match": True,
                          "all_eigenvalues_max_absolute_error": error,
                          "mapping_A_index_to_B_mode": [[int(j), int(m)] for j, m in zip(rows, modes)]})
            assert np.max(np.abs(np.asarray(R) @ np.asarray(R).T - np.asarray(R).T @ np.asarray(R))) == 0
            if a["name"] == "published_uniform_7":
                assert a["polynomial_gcd_with_derivative_degree"] == 0
                assert len(a["all_leading_modes"]) == len(a["eligible_leading_modes"]) == 2
                print("FULL BENCHMARK SPECTRUM (every A eigenvalue matched to independent B):")
                for j, m in zip(rows, modes):
                    print(json.dumps({"A_index": int(j), "B_mode": int(m),
                                      "A_float64": a["eigenvalues_scipy"][j],
                                      "B_80digits": b["spectra_backward_by_m"][m],
                                      "absolute_error": float(distances[j, m])}))
                analytic_a, analytic_b = mp.mpf(b["a_leading"]), mp.mpf(b["b_leading"])
                direct_leader = next(z for z in a["all_leading_modes"] if z[1] > 0)
                direct_a, direct_b = mp.mpf(-direct_leader[0]), mp.mpf(direct_leader[1])
                direct_sigma = mp.mpf(a["sigma_edge_once"])
                direct_observables = {"N": direct_b / (2 * mp.pi * direct_a),
                                      "DeltaS": 2 * mp.pi * direct_sigma / direct_b,
                                      "Y": direct_sigma * direct_a / direct_b ** 2}
                direct_errors = {"N": abs(direct_observables["N"] - mp.mpf(b["OBS_eq9_N"])),
                                 "DeltaS": abs(direct_observables["DeltaS"] - mp.mpf(b["OBS_eq8_DeltaS"])),
                                 "Y": abs(direct_observables["Y"] - mp.mpf(b["Y_sigma_a_over_b2"]))}
                assert max(direct_errors.values()) < mp.mpf("1e-11")
                gap = 9 * (mp.cos(2 * mp.pi / 7) - mp.cos(4 * mp.pi / 7))
                entry.update({"all_leading_modes": a["all_leading_modes"],
                              "spectral_gap_to_next_pair": mp.nstr(gap, 78),
                              "b_over_a": mp.nstr(analytic_b / analytic_a, 78),
                              "eligibility_margin_b_minus_a": mp.nstr(analytic_b - analytic_a, 78),
                              "A_direct_spectrum_observables": {k: mp.nstr(v, 18) for k, v in direct_observables.items()},
                              "A_observable_errors_vs_B_source_formulas": {k: mp.nstr(v, 12) for k, v in direct_errors.items()},
                              "all_eigenvalues_simple_exact": True,
                              "normal_generator_diagonalizable": True})
                assert gap > 0 and analytic_b > analytic_a
            elif a["name"] == "equilibrium_control":
                assert not a["eligible_leading_modes"] and mp.mpf(a["sigma_edge_once"]) == 0
        comparisons.append(entry)
        print(json.dumps(entry))

    base = B["cases"][0]
    reverse, scale = B["cases"][1], B["cases"][2]
    for key in ("N_spectral", "DeltaS_spectral", "Y_sigma_a_over_b2"):
        assert abs(mp.mpf(base[key]) - mp.mpf(reverse[key])) < TOLERANCE_LOGS
        assert abs(mp.mpf(base[key]) - mp.mpf(scale[key])) < TOLERANCE_LOGS
    for key in ("a_leading", "b_leading", "sigma_tree_flux"):
        assert abs(mp.mpf(scale[key]) - 3 * mp.mpf(base[key])) < TOLERANCE_LOGS
    record = {"status": "pass", "comparison_scope": "published uniform ring plus convention controls; no heterogeneous target resolution",
              "basis_map": "j_B=i_A+1; R_A=Q_B^T; z_A,m=z_B,(-m mod n)",
              "spectrum_absolute_tolerance": TOLERANCE_SPECTRUM,
              "decimal_entropy_and_formula_tolerance": str(TOLERANCE_LOGS),
              "comparisons": comparisons, "orientation_and_time_scale_checks": "pass"}
    (ROOT / "evidence/input-comparison.json").write_text(json.dumps(record, indent=2) + "\n")
    print("PASS: row-by-row exact matrices, independent stationarity, full characteristic polynomials/spectra, orientation/time scaling, entropy conventions.")
    # A distinct baseline log reports the source formula comparisons and scope.
    lines = ["PUBLISHED BASELINE: OBS arXiv:2112.01607v2, PDF p. 2 Eqs. (8)-(10).",
             "Instance: n=7, u=8/t0, d=1/t0, k_B=1, A=7 ln 8.",
             "All seven eigenvalues checked; leading modes m=1,6 only. Uniform Fourier normality excludes Jordan defects.",
             "Exact leadership: cos(2pi/7)>cos(4pi/7)>cos(6pi/7).",
             "Exact eligibility: b/a=(7/9)cot(pi/7)>(7/9)sqrt(3)>1.",
             "Exact stationary law pi_i=1/7; J=1/t0; sigma=7 ln 8/t0."]
    for key in ("a_leading", "b_leading", "N_spectral", "DeltaS_spectral", "Y_sigma_a_over_b2",
                "OBS_eq8_DeltaS", "OBS_eq9_N", "OBS_eq10_DeltaS", "eq10_atanh_argument"):
        lines.append(key + " = " + base[key])
    for name, error_string in base["source_formula_errors_before_serialization"].items():
        assert mp.mpf(error_string) < TOLERANCE_LOGS
        lines.append(name + " (before serialized-value rounding) = " + error_string)
    for name, value in comparisons[0]["A_direct_spectrum_observables"].items():
        lines.append("A_direct_spectrum_" + name + " = " + value)
        lines.append("A_" + name + "_error_vs_independent_B_source = " + comparisons[0]["A_observable_errors_vs_B_source_formulas"][name])
    lines.extend(["Exact Eq. (10) argument is 7/9, inside (-1,1).",
                  "At 80-digit precision source-formula errors are <1e-70; float64 full-spectrum tolerance is 1e-11.",
                  "High-precision values are numerical agreement, not interval certificates; analytic identities establish this known homogeneous baseline.",
                  "PASS: actual published analytic family reproduced; original all-heterogeneous assertion remains unresolved.",
                  "This is reproduction only, with no new value/claim packet or independent referee acceptance."])
    (ROOT / "evidence/baseline.log").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
