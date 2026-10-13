#!/usr/bin/env python3
"""Run the independent reconstructions and compare only their final observables."""
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def run(name):
    completed = subprocess.run(
        [sys.executable, str(HERE / name)],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return json.loads(completed.stdout)


a = run("reproduce_input_a.py")
b = run("reproduce_input_b.py")


def maxdiff(xs, ys):
    if len(xs) != len(ys):
        raise RuntimeError("spectrum lengths disagree")
    return max(abs(float(x) - float(y)) for x, y in zip(xs, ys))


checks = {
    "one_copy_spectrum_max_abs": maxdiff(a["one_copy_spectrum"], b["one_copy_nonzero_spectrum"]),
    "product_spectrum_max_abs": maxdiff(a["product_two_copy_spectrum"], b["product_two_copy_nonzero_spectrum"]),
    "signed_spectrum_max_abs": maxdiff(a["signed_two_copy_spectrum"], b["signed_two_copy_nonzero_spectrum"]),
    "one_entropy_abs_bits": abs(a["one_copy_renyi_half_bits"] - float(b["one_copy_renyi_half_bits"])),
    "product_entropy_abs_bits": abs(a["product_two_copy_renyi_half_bits"] - float(b["product_two_copy_renyi_half_bits"])),
    "signed_entropy_abs_bits": abs(a["signed_two_copy_renyi_half_bits"] - float(b["signed_two_copy_renyi_half_bits"])),
    "witness_difference_abs_bits": abs(a["signed_minus_product_bits"] - float(b["signed_minus_product_bits"])),
}
tolerance = 1.0e-12
margin = -float(b["signed_minus_product_bits"])
result = {
    "status": "pass" if max(checks.values()) < tolerance and margin > tolerance else "fail",
    "r_exact": "1/5",
    "alpha_exact": "1/2",
    "entropy_convention": "base-2 Renyi entropy",
    "cut": "AA_prime:BB_prime",
    "basis_convention_map": {
        "A_rows": "A logical rows [0_L,1_L], two-copy lexicographic [00,01,10,11]",
        "B_left_indices": "B combines the physical A and flag A_prime as 4*A+A_prime; nonzero canonical rows satisfy A_prime=A and map in lexicographic I order",
        "right_indices": "the same map holds for physical B and flag B_prime",
        "observable_equivalence": "squared singular values of A's coefficient matrix equal the nonzero eigenvalues after B's explicit partial trace"
    },
    "observed_differences": checks,
    "comparison_tolerance_bits_or_absolute_spectrum": tolerance,
    "conservative_reported_roundoff_bound_bits": tolerance,
    "signed_minus_product_bits_method_a": a["signed_minus_product_bits"],
    "signed_minus_product_bits_method_b_100dps": b["signed_minus_product_bits"],
    "strict_negative_margin_over_reported_bound": margin / tolerance,
    "caveat": "The 1e-12 bound is a conservative numerical roundoff/reconstruction bound supported by independent double-SVD and 100-digit partial-trace agreement; it is not an interval-arithmetic certificate for new research."
}
print(json.dumps(result, sort_keys=True, indent=2))
if result["status"] != "pass":
    raise SystemExit(1)
