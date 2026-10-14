#!/usr/bin/env python3
"""Input B: backward action, roots-of-unity diagonalization, directed cycle trees.

No A artifact, cached matrix, stationary vector, or eigenvalues are read or imported.
Same-worker independence is representational and algorithmic, not referee independence.
"""
import json
from collections import deque
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import sympy as sy

ROOT = Path(__file__).resolve().parents[1]
mp.mp.dps = 80

# Separate transcription of the source uniform family's p,q and diagnostic controls.
CASES = [
    ("published_uniform_7", (8,) * 7, (1,) * 7),
    ("reverse_orientation", (1,) * 7, (8,) * 7),
    ("time_scale_times_3", (24,) * 7, (3,) * 7),
    ("equilibrium_control", (2,) * 7, (2,) * 7),
    ("entropy_convention_control", (8, 7, 9, 6, 10, 5, 11), (1, 2, 1, 3, 2, 1, 2)),
]


def tree_weights(p, q):
    """Delete each undirected cycle edge; orient remaining tree toward each root."""
    size = len(p)
    taus, terms = [], []
    for root in range(size):
        products = []
        for removed in range(size):
            neighbors = [[] for _ in range(size)]
            for edge in range(size):
                if edge == removed:
                    continue
                i, j = edge, (edge + 1) % size
                neighbors[i].append(j)
                neighbors[j].append(i)
            parent = {root: None}
            queue = deque([root])
            while queue:
                j = queue.popleft()
                for i in neighbors[j]:
                    if i not in parent:
                        parent[i] = j
                        queue.append(i)
            assert len(parent) == size
            weight = 1
            for i, j in parent.items():
                if j is not None:
                    weight *= p[i] if j == (i + 1) % size else q[i]
            products.append(weight)
        taus.append(sum(products))
        terms.append(products)
    return taus, terms


def act(f, p, q):
    n = len(f)
    return [p[j] * (f[(j + 1) % n] - f[j]) + q[j] * (f[(j - 1) % n] - f[j])
            for j in range(n)]


def compute(name, p, q):
    n = len(p)
    # Evaluate the function-space action on indicator functions to reconstruct Q.
    columns = []
    for column in range(n):
        basis = [int(j == column) for j in range(n)]
        columns.append(act(basis, p, q))
    Q = [[columns[k][j] for k in range(n)] for j in range(n)]
    assert act([1] * n, p, q) == [0] * n
    tau, terms = tree_weights(p, q)
    pi = [Fraction(t, sum(tau)) for t in tau]
    # Row stationarity check differs from A's linear solution.
    assert [sum(pi[j] * Q[j][k] for j in range(n)) for k in range(n)] == [0] * n
    flux = [pi[j] * p[j] - pi[(j + 1) % n] * q[(j + 1) % n] for j in range(n)]
    assert len(set(flux)) == 1
    def mf(r):
        return mp.mpf(r.numerator) / r.denominator
    affinity = mp.log(mp.mpf(sy.prod(p)) / int(sy.prod(q)))
    entropy = mp.fsum(mf(flux[j]) * mp.log(mf(pi[j] * p[j]) /
                                          mf(pi[(j + 1) % n] * q[(j + 1) % n])) for j in range(n))
    assert abs(entropy - mf(flux[0]) * affinity) < mp.mpf("1e-70")
    item = {"name": name, "n": n, "p_clockwise": list(p), "q_reverse": list(q),
            "row_backward_generator_Q": Q,
            "root_tree_weights": tau, "individual_tree_products": terms,
            "stationary_exact": [str(r) for r in pi],
            "currents_exact": [str(r) for r in flux],
            "affinity_decimal": mp.nstr(affinity, 78), "sigma_tree_flux": mp.nstr(entropy, 78)}
    if len(set(p)) == len(set(q)) == 1:
        right, left = p[0], q[0]
        spectra, residuals = [], []
        spectral_Q = mp.matrix(n)
        for mode in range(n):
            theta = 2 * mp.pi * mode / n
            omega = mp.exp(mp.j * theta)
            z = right * (omega - 1) + left * (mp.conj(omega) - 1)
            spectra.append([mp.nstr(z.real, 78), mp.nstr(z.imag, 78)])
            f = [omega ** j / mp.sqrt(n) for j in range(n)]
            result = act(f, p, q)
            residuals.append(max(abs(result[j] - z * f[j]) for j in range(n)))
            for j in range(n):
                for k in range(n):
                    spectral_Q[j, k] += z * f[j] * mp.conj(f[k])
        spectral_error = max(abs(spectral_Q[j, k] - Q[j][k]) for j in range(n) for k in range(n))
        assert spectral_error < mp.mpf("1e-70")
        zsym, w = sy.symbols("z w")
        # Product of -w over all nth roots of unity is -1 for every n.
        polynomial = -sy.resultant(w ** n - 1, right * w ** 2 - (zsym + right + left) * w + left, w)
        a = (right + left) * (1 - mp.cos(2 * mp.pi / n))
        b = abs(right - left) * mp.sin(2 * mp.pi / n)
        item.update({"fourier_sign": "+: f_m(j)=exp(+2*pi*i*m*(j-1)/n)/sqrt(n), source labels j=1..n",
                     "spectra_backward_by_m": spectra,
                     "fourier_eigenvector_residual_max": mp.nstr(max(residuals), 12),
                     "fourier_matrix_reconstruction_error_max": mp.nstr(spectral_error, 12),
                     "characteristic_polynomial_resultant_coefficients": [str(v) for v in sy.Poly(polynomial, zsym).all_coeffs()],
                     "a_leading": mp.nstr(a, 78), "b_leading": mp.nstr(b, 78)})
        if b > 0:
            coherence = b / (2 * mp.pi * a)
            period_entropy = 2 * mp.pi * entropy / b
            eq8 = 2 * mp.pi * abs(affinity) / (n * mp.sin(2 * mp.pi / n))
            eq9 = mp.cot(mp.pi / n) * mp.tanh(abs(affinity) / (2 * n)) / (2 * mp.pi)
            arg = 2 * mp.pi * coherence * mp.tan(mp.pi / n)
            eq10 = 4 * mp.pi * mp.atanh(arg) / mp.sin(2 * mp.pi / n)
            assert max(abs(period_entropy - eq8), abs(coherence - eq9), abs(period_entropy - eq10)) < mp.mpf("1e-70")
            item.update({"N_spectral": mp.nstr(coherence, 78), "DeltaS_spectral": mp.nstr(period_entropy, 78),
                         "OBS_eq8_DeltaS": mp.nstr(eq8, 78), "OBS_eq9_N": mp.nstr(eq9, 78),
                         "OBS_eq10_DeltaS": mp.nstr(eq10, 78), "eq10_atanh_argument": mp.nstr(arg, 78),
                         "source_formula_errors_before_serialization": {
                             "eq8_DeltaS_error": mp.nstr(abs(period_entropy - eq8), 12),
                             "eq9_N_error": mp.nstr(abs(coherence - eq9), 12),
                             "eq10_DeltaS_error": mp.nstr(abs(period_entropy - eq10), 12)},
                         "Y_sigma_a_over_b2": mp.nstr(entropy * a / b ** 2, 78),
                         "eligible": bool(b >= a)})
        else:
            item["eligible"] = False
            item["period_status"] = "undefined at b=0; no oscillatory leading mode"
    else:
        item["scope"] = "nonuniform diagnostic of matrix/entropy conventions only; no target inequality is tested"
    return item


def main():
    packet = {"representation": "B: backward action; Fourier symbol and cycle-tree/flux stationary representation",
              "primary_source": "literature/2112.01607.pdf", "code": "scripts/reproduce_input_b.py",
              "independence": "no A input or cached output read; separate constants, tree enumeration, resultant and 80-digit Fourier evaluation",
              "cases": [compute(*case) for case in CASES]}
    (ROOT / "evidence/input-b.json").write_text(json.dumps(packet, indent=2) + "\n")
    print("INPUT B: independently derived backward Fourier and cycle-tree representation; no A files read.")
    for c in packet["cases"]:
        print(json.dumps({"case": c["name"], "tree_weights": c["root_tree_weights"],
                          "stationary": c["stationary_exact"], "current": c["currents_exact"][0],
                          "Fourier_reconstruction_error": c.get("fourier_matrix_reconstruction_error_max"),
                          "a": c.get("a_leading"), "b": c.get("b_leading"), "Y": c.get("Y_sigma_a_over_b2")}))
    print("PASS: trees/flux exact stationarity; Fourier reconstruction and Eqs. (8)-(10) within 1e-70 at 80 digits.")


if __name__ == "__main__":
    main()
