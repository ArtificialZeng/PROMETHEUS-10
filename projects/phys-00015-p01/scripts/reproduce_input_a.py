#!/usr/bin/env python3
"""Input A: direct outgoing-edge transcription, exact stationarity, dense spectrum.

Reads no B input, script, spectrum, or cached calculation. All rates are in t0^-1.
"""
import json
from pathlib import Path

import numpy as np
import scipy.linalg
import sympy as sp
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
mp.mp.dps = 80

# Direct transcription of the OBS p. 2 uniform family, Omega=7, k=1, A=7 ln 8.
# The controls test conventions; they are not additional published data or claims.
SPECS = [
    ("published_uniform_7", [8, 8, 8, 8, 8, 8, 8], [1, 1, 1, 1, 1, 1, 1]),
    ("reverse_orientation", [1, 1, 1, 1, 1, 1, 1], [8, 8, 8, 8, 8, 8, 8]),
    ("time_scale_times_3", [24, 24, 24, 24, 24, 24, 24], [3, 3, 3, 3, 3, 3, 3]),
    ("equilibrium_control", [2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2]),
    ("entropy_convention_control", [8, 7, 9, 6, 10, 5, 11], [1, 2, 1, 3, 2, 1, 2]),
]


def decimal(q):
    if isinstance(q, sp.Rational):
        return mp.mpf(int(q.p)) / int(q.q)
    return mp.mpf(q)


def compute(name, u, d):
    n = len(u)
    R = sp.zeros(n)
    edges = []
    for origin in range(n):
        for destination, rate in (((origin + 1) % n, u[origin]),
                                  ((origin - 1) % n, d[origin])):
            R[destination, origin] += rate
            R[origin, origin] -= rate
            edges.append({"origin": origin, "destination": destination, "rate": rate})
    assert all(sum(R[:, j]) == 0 for j in range(n))
    assert all(R[i, j] >= 0 for i in range(n) for j in range(n) if i != j)
    assert R.rank() == n - 1
    system = R.copy()
    system[n - 1, :] = sp.ones(1, n)
    rhs = sp.zeros(n, 1)
    rhs[n - 1] = 1
    stationary = system.inv() * rhs
    assert R * stationary == sp.zeros(n, 1)
    assert sum(stationary) == 1 and all(p > 0 for p in stationary)
    currents = [stationary[i] * u[i] - stationary[(i + 1) % n] * d[(i + 1) % n]
                for i in range(n)]
    assert len(set(currents)) == 1
    sigma_edge = mp.fsum(
        decimal(currents[i]) * mp.log(decimal(stationary[i] * u[i]) /
                                     decimal(stationary[(i + 1) % n] * d[(i + 1) % n]))
        for i in range(n))
    sigma_directed_flow = mp.mpf(0)
    sigma_obs = mp.mpf(0)
    probability_correction = mp.mpf(0)
    for e in edges:
        i, j, rate = e["origin"], e["destination"], e["rate"]
        reverse_rate = R[i, j]
        forward = stationary[i] * rate
        reverse = stationary[j] * reverse_rate
        sigma_directed_flow += decimal(forward) * mp.log(decimal(forward) / decimal(reverse))
        sigma_obs += decimal(forward) * mp.log(decimal(rate) / decimal(reverse_rate))
        probability_correction += decimal(forward) * mp.log(decimal(stationary[i]) /
                                                           decimal(stationary[j]))
    affinity = mp.fsum(mp.log(mp.mpf(x)) for x in u) - mp.fsum(mp.log(mp.mpf(x)) for x in d)
    sigma_ja = decimal(currents[0]) * affinity
    assert max(abs(sigma_edge - sigma_directed_flow), abs(sigma_edge - sigma_obs),
               abs(sigma_edge - sigma_ja), abs(probability_correction)) < mp.mpf("1e-70")
    x = sp.Symbol("z")
    polynomial = R.charpoly(x).as_expr()
    numeric = np.array(R.tolist(), dtype=float)
    eigenvalues, right = scipy.linalg.eig(numeric)
    residuals = [float(np.linalg.norm(numeric @ right[:, k] - eigenvalues[k] * right[:, k], ord=np.inf))
                 for k in range(n)]
    nonzero = [z for z in eigenvalues if abs(z) > 1e-10]
    leading = max(z.real for z in nonzero)
    leaders = [z for z in nonzero if abs(z.real - leading) < 1e-10]
    result = {
        "name": name, "n": n, "u": u, "d": d,
        "column_generator_R": [[int(x) for x in row] for row in R.tolist()],
        "directed_edges": edges,
        "stationary_exact": [str(x) for x in stationary],
        "stationary_residual_exact": [str(x) for x in R * stationary],
        "currents_exact": [str(x) for x in currents],
        "affinity_decimal": mp.nstr(affinity, 78),
        "sigma_edge_once": mp.nstr(sigma_edge, 78),
        "sigma_directed_flow": mp.nstr(sigma_directed_flow, 78),
        "sigma_OBS_rate_ratio": mp.nstr(sigma_obs, 78),
        "sigma_current_affinity": mp.nstr(sigma_ja, 78),
        "probability_log_correction": mp.nstr(probability_correction, 10),
        "characteristic_polynomial_coefficients": [str(x) for x in sp.Poly(polynomial, x).all_coeffs()],
        "polynomial_gcd_with_derivative_degree": int(sp.degree(sp.gcd(polynomial, sp.diff(polynomial, x)), x)),
        "eigenvalues_scipy": [[float(z.real), float(z.imag)] for z in eigenvalues],
        "eigenvector_residual_max": max(residuals),
        "leading_real_part": float(leading),
        "all_leading_modes": [[float(z.real), float(z.imag)] for z in leaders],
        "eligible_leading_modes": [[float(z.real), float(z.imag)] for z in leaders
                                   if abs(z.imag) > 1e-10 and abs(z.imag) >= -z.real],
    }
    return result


def main():
    cases = [compute(*spec) for spec in SPECS]
    # This explicit matrix is a direct row-by-row transcription check for the benchmark.
    expected = [[-9, 1, 0, 0, 0, 0, 8], [8, -9, 1, 0, 0, 0, 0],
                [0, 8, -9, 1, 0, 0, 0], [0, 0, 8, -9, 1, 0, 0],
                [0, 0, 0, 8, -9, 1, 0], [0, 0, 0, 0, 8, -9, 1],
                [1, 0, 0, 0, 0, 8, -9]]
    assert cases[0]["column_generator_R"] == expected
    packet = {"representation": "A: probability-column generator assembled from explicit outgoing edges",
              "primary_source": "literature/2112.01607.pdf",
              "source_locator": "PDF p. 2 Eqs. (2)-(9), uniform-rate paragraph",
              "units": "rates and entropy rate in t0^-1, k_B=1, natural logs",
              "precision": "integer/rational matrix algebra; 80-decimal mpmath logs; float64 scipy eigenvalues",
              "code": "scripts/reproduce_input_a.py", "cases": cases}
    (ROOT / "evidence/input-a.json").write_text(json.dumps(packet, indent=2) + "\n")
    print("INPUT A: outgoing edges; exact rational stationarity; no B files read.")
    for c in cases:
        print(json.dumps({"case": c["name"], "exact_stationary": c["stationary_exact"],
                          "current": c["currents_exact"][0], "sigma": c["sigma_edge_once"],
                          "eigenvector_residual_max": c["eigenvector_residual_max"]}))
    print("PASS: positivity, exact stationarity/current conservation, four entropy formulas, row-by-row benchmark matrix.")


if __name__ == "__main__":
    main()
