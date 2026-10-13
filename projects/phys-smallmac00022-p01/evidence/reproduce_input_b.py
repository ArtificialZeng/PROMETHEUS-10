#!/usr/bin/env python3
"""Reconstruction B: independent ket assembly and explicit partial trace."""
import hashlib
import json
from pathlib import Path

import mpmath as mp


HERE = Path(__file__).resolve().parent
INPUT = HERE / "input-b.json"
data = json.loads(INPUT.read_text(encoding="utf-8"))
if data["r_exact"] != "1/5" or data["alpha_exact"] != "1/2":
    raise RuntimeError("unexpected frozen B parameters")

mp.mp.dps = 100
r = mp.mpf(1) / 5
alpha = mp.mpf(1) / 2
D = 3 + r * r


def branch_amplitude(i, j):
    # Separately transcribed from probabilities in Eq. (C1), not from A's matrix.
    numerator = r if (i == 0 and j == 0) else mp.mpf(1)
    return numerator / mp.sqrt(D)


def nonzero_eigenvalues(matrix, cutoff=mp.mpf("1e-80")):
    vals = list(mp.eigsy(matrix, eigvals_only=True))
    vals = [mp.re(v) for v in vals if abs(v) > cutoff]
    vals.sort(reverse=True)
    return vals


def renyi(values):
    return mp.log(sum(v ** alpha for v in values), 2) / (1 - alpha)


# Full single-copy ket indexed as (A,B,A',B').
psi1 = {}
for i in range(2):
    for j in range(2):
        psi1[(i, j, i, j)] = branch_amplitude(i, j)

# Explicit trace over B,B'; AA' has dimension four.
rho1 = mp.matrix(4, 4)
for i in range(2):
    for ap in range(2):
        row = 2 * i + ap
        for k in range(2):
            for kp in range(2):
                col = 2 * k + kp
                rho1[row, col] = sum(
                    psi1.get((i, j, ap, bp), mp.mpf(0))
                    * psi1.get((k, j, kp, bp), mp.mpf(0))
                    for j in range(2) for bp in range(2)
                )
one_spectrum = nonzero_eigenvalues(rho1)


def assemble_two_copy(signed):
    # Full ket indexed as (A1A2,B1B2,A1'A2',B1'B2').
    psi = {}
    for i1 in range(2):
        for i2 in range(2):
            I = 2 * i1 + i2
            for j1 in range(2):
                for j2 in range(2):
                    J = 2 * j1 + j2
                    amp = branch_amplitude(i1, j1) * branch_amplitude(i2, j2)
                    if signed and i1 == i2 == j1 == j2 == 0:
                        amp = -amp
                    psi[(I, J, I, J)] = amp
    # Explicit trace over B1B2 and B1'B2'; AA' has dimension 16.
    rho = mp.matrix(16, 16)
    for A in range(4):
        for Ap in range(4):
            row = 4 * A + Ap
            for K in range(4):
                for Kp in range(4):
                    col = 4 * K + Kp
                    rho[row, col] = sum(
                        psi.get((A, B, Ap, Bp), mp.mpf(0))
                        * psi.get((K, B, Kp, Bp), mp.mpf(0))
                        for B in range(4) for Bp in range(4)
                    )
    return rho


rho_product = assemble_two_copy(False)
rho_signed = assemble_two_copy(True)
product_spectrum = nonzero_eigenvalues(rho_product)
signed_spectrum = nonzero_eigenvalues(rho_signed)
one_entropy = renyi(one_spectrum)
product_entropy = renyi(product_spectrum)
signed_entropy = renyi(signed_spectrum)


def fmt(value):
    return mp.nstr(value, 80)


out = {
    "method": "B explicit physical-plus-flag ket and partial trace",
    "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    "mpmath_dps": mp.mp.dps,
    "r": fmt(r),
    "alpha": fmt(alpha),
    "D": fmt(D),
    "one_copy_nonzero_spectrum": [fmt(v) for v in one_spectrum],
    "one_copy_trace_error": fmt(abs(sum(one_spectrum) - 1)),
    "one_copy_renyi_half_bits": fmt(one_entropy),
    "product_two_copy_nonzero_spectrum": [fmt(v) for v in product_spectrum],
    "signed_two_copy_nonzero_spectrum": [fmt(v) for v in signed_spectrum],
    "product_two_copy_renyi_half_bits": fmt(product_entropy),
    "twice_one_copy_renyi_half_bits": fmt(2 * one_entropy),
    "product_additivity_error_bits": fmt(abs(product_entropy - 2 * one_entropy)),
    "signed_two_copy_renyi_half_bits": fmt(signed_entropy),
    "signed_minus_product_bits": fmt(signed_entropy - product_entropy),
    "product_trace_error": fmt(abs(sum(product_spectrum) - 1)),
    "signed_trace_error": fmt(abs(sum(signed_spectrum) - 1)),
}
print(json.dumps(out, sort_keys=True, indent=2))
