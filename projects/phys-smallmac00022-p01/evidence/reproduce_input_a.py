#!/usr/bin/env python3
"""Reconstruction A: coefficient-matrix SVD, with no dependency on input B."""
import hashlib
import json
from pathlib import Path

import numpy as np
import scipy


HERE = Path(__file__).resolve().parent
INPUT = HERE / "input-a.json"


def entropy_renyi(values, alpha):
    values = np.asarray(values, dtype=np.float64)
    return float(np.log2(np.sum(values ** alpha)) / (1.0 - alpha))


data = json.loads(INPUT.read_text(encoding="utf-8"))
if data["r_exact"] != "1/5" or data["alpha_exact"] != "1/2":
    raise RuntimeError("unexpected frozen A parameters")

r = np.float64(1.0 / 5.0)
alpha = np.float64(1.0 / 2.0)
D = np.float64(3.0 + r * r)

# Direct transcription of Eq. (C3) in row (0_L,1_L), column (0_R,1_R) order.
C1 = np.array([[r, 1.0], [1.0, 1.0]], dtype=np.float64) / np.sqrt(D)
sigma = C1 @ C1.T
one_spectrum = np.sort(np.linalg.svd(C1, compute_uv=False) ** 2)[::-1]
disc = np.sqrt(1.0 - 4.0 * (1.0 - r) ** 2 / D ** 2)
analytic_spectrum = np.array([(1.0 + disc) / 2.0, (1.0 - disc) / 2.0])

# Eq. (C7): product coefficient matrix and the single all-zero sign flip.
C2_product = np.kron(C1, C1)
C2_signed = C2_product.copy()
C2_signed[0, 0] = -C2_signed[0, 0]
product_spectrum = np.sort(np.linalg.svd(C2_product, compute_uv=False) ** 2)[::-1]
signed_spectrum = np.sort(np.linalg.svd(C2_signed, compute_uv=False) ** 2)[::-1]

one_entropy = entropy_renyi(one_spectrum, alpha)
product_entropy = entropy_renyi(product_spectrum, alpha)
signed_entropy = entropy_renyi(signed_spectrum, alpha)

out = {
    "method": "A coefficient-matrix singular values",
    "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    "python": __import__("sys").version.split()[0],
    "numpy": np.__version__,
    "scipy": scipy.__version__,
    "r": float(r),
    "alpha": float(alpha),
    "D": float(D),
    "one_copy_coefficient_matrix": C1.tolist(),
    "one_copy_left_marginal": sigma.tolist(),
    "one_copy_spectrum": one_spectrum.tolist(),
    "analytic_spectrum": analytic_spectrum.tolist(),
    "spectrum_formula": "lambda_pm=(1+-sqrt(1-4(1-r)^2/(3+r^2)^2))/2",
    "max_one_spectrum_formula_error": float(np.max(np.abs(one_spectrum - analytic_spectrum))),
    "one_copy_trace_error": float(abs(np.sum(one_spectrum) - 1.0)),
    "one_copy_renyi_half_bits": one_entropy,
    "product_two_copy_spectrum": product_spectrum.tolist(),
    "signed_two_copy_spectrum": signed_spectrum.tolist(),
    "product_two_copy_renyi_half_bits": product_entropy,
    "twice_one_copy_renyi_half_bits": 2.0 * one_entropy,
    "product_additivity_error_bits": float(abs(product_entropy - 2.0 * one_entropy)),
    "signed_two_copy_renyi_half_bits": signed_entropy,
    "signed_minus_product_bits": signed_entropy - product_entropy,
    "product_trace_error": float(abs(np.sum(product_spectrum) - 1.0)),
    "signed_trace_error": float(abs(np.sum(signed_spectrum) - 1.0)),
}
print(json.dumps(out, sort_keys=True, indent=2))
