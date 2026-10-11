#!/usr/bin/env python3
"""Exact convention/basis comparison performed only after A and B are frozen."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


PROJECT = Path(__file__).resolve().parents[1]


def main():
    input_a = json.loads((PROJECT / "evidence/input-a.json").read_text())
    input_b = json.loads((PROJECT / "evidence/input-b.json").read_text())
    assert input_a["id"] == "input-a-real-poisson"
    assert input_b["id"] == "input-b-complex-wick"
    assert input_a["implementation"] != input_b["implementation"]

    m, gamma, k, temperature, kappa = sp.symbols(
        "m gamma k T kappa", nonzero=True, finite=True
    )
    A = sp.Matrix(
        [
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [-k / m, -kappa / m, -gamma / m, 0],
            [kappa / m, -k / m, 0, -gamma / m],
        ]
    )
    Q = sp.diag(0, 0, 2 * gamma * temperature / m**2, 2 * gamma * temperature / m**2)
    F = sp.zeros(4)
    F[0, 3] = F[3, 0] = kappa / 2
    F[1, 2] = F[2, 1] = -kappa / 2
    P = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])

    re_c = sp.Matrix([[0, 1], [-k / m, -gamma / m]])
    im_c = sp.Matrix([[0, 0], [kappa / m, 0]])
    M_complex_realified = re_c.row_join(-im_c).col_join(im_c.row_join(re_c))
    Q_b = sp.diag(0, 2 * gamma * temperature / m**2, 0, 2 * gamma * temperature / m**2)
    F_b = sp.zeros(4)
    F_b[0, 3] = F_b[3, 0] = kappa / 2
    F_b[2, 1] = F_b[1, 2] = -kappa / 2

    drift_residual = (P * A * P.T - M_complex_realified).applyfunc(sp.simplify)
    noise_residual = (P * Q * P.T - Q_b).applyfunc(sp.simplify)
    current_residual = (P * F * P.T - F_b).applyfunc(sp.simplify)
    assert drift_residual == sp.zeros(4)
    assert noise_residual == sp.zeros(4)
    assert current_residual == sp.zeros(4)

    kappa_cfs = -kappa
    kappa0 = kappa_cfs / k
    m0 = k * m / gamma**2
    tau = gamma / k
    kstar = k - m * kappa**2 / gamma**2
    cfs_mean = 2 * kappa0**2 * temperature / ((1 - kappa0**2 * m0) * tau)
    cfs_diffusion = (
        2
        * kappa0**2
        * (1 + kappa0**2 * (1 + 3 * m0))
        * temperature**2
        / ((1 - kappa0**2 * m0) ** 3 * tau)
    )
    source_mean = 2 * kappa**2 * temperature / (gamma * kstar)
    source_diffusion = (
        2
        * kappa**2
        * temperature**2
        * (k**2 + kappa**2 + 3 * m * k * kappa**2 / gamma**2)
        / (gamma * kstar**3)
    )
    mean_residual = sp.factor(cfs_mean - source_mean)
    diffusion_residual = sp.factor(cfs_diffusion - source_diffusion)
    stability_map_residual = sp.factor(1 - kappa0**2 * m0 - kstar / k)
    assert mean_residual == 0
    assert diffusion_residual == 0
    assert stability_map_residual == 0

    print("input_a_id=input-a-real-poisson")
    print("input_b_id=input-b-complex-wick")
    print("shared_implementation=none")
    print("basis_map_y_equals_Pz=verified_exactly")
    print("drift_map_residual=zero_matrix")
    print("noise_map_residual=zero_matrix")
    print("work_quadratic_form_map_residual=zero_matrix")
    print("torque_map=kappa_CFS=-kappa_source")
    print("magnetic_field_map=B0=0")
    print("stability_map=1-kappa0^2*m0=kstar/k")
    print(f"stability_map_residual={stability_map_residual}")
    print("variance_rate_map=D_CFS=lim_Var_over_2t=D_project")
    print(f"published_mean_conversion_residual={mean_residual}")
    print(f"published_D_conversion_residual={diffusion_residual}")
    print("independence_limit=same_agent_and_same_primary_PDFs_but_separate_transcription_basis_algorithm_and_no_A_to_B_data_or_code_dependency")
    print("status=PASS")


if __name__ == "__main__":
    main()
