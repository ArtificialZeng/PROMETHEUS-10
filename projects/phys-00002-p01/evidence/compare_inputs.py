#!/usr/bin/env python3
"""Compare the independently reconstructed inputs through an explicit basis map."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def decode_complex_matrix(rows: list) -> np.ndarray:
    return np.asarray([[complex(*z) for z in row] for row in rows])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-a", required=True)
    parser.add_argument("--input-b", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    a = json.loads(Path(args.input_a).read_text(encoding="utf-8"))
    b = json.loads(Path(args.input_b).read_text(encoding="utf-8"))
    la = decode_complex_matrix(a["L"])
    channel = decode_complex_matrix(a["channel"])
    gb = np.asarray(b["linear_generator"])
    cb = np.asarray(b["offset"])
    aug_b = np.zeros((4, 4))
    aug_b[:3, :3] = gb
    aug_b[:3, 3] = cb

    # q=(x,y,z,1).  For column vectorization (rho00,rho10,rho01,rho11),
    # vec(rho)=S q follows directly from rho=(I+r.sigma)/2.
    s = 0.5 * np.asarray(
        [
            [0, 0, 1, 1],
            [1, 1j, 0, 0],
            [1, -1j, 0, 0],
            [0, 0, -1, 1],
        ],
        dtype=complex,
    )
    aug_from_a = np.linalg.inv(s) @ la @ s
    residual = aug_from_a - aug_b

    # Choi matrix of the finite channel: J=sum_ij |i><j| tensor E(Eij).
    choi = np.zeros((4, 4), dtype=complex)
    for j in range(2):
        for i in range(2):
            out = channel[:, i + 2 * j].reshape((2, 2), order="F")
            choi[2 * i : 2 * i + 2, 2 * j : 2 * j + 2] = out
    choi_herm = (choi + choi.conj().T) / 2
    choi_eigs = np.linalg.eigvalsh(choi_herm)

    row_comparison = []
    for row in range(4):
        entries = []
        for col in range(4):
            entries.append(
                {
                    "column": col,
                    "from_matrix_units": [float(aug_from_a[row, col].real), float(aug_from_a[row, col].imag)],
                    "from_bloch": [float(aug_b[row, col]), 0.0],
                    "abs_residual": float(abs(residual[row, col])),
                }
            )
        row_comparison.append({"row": row, "entries": entries})

    ta, tb = a["transition"], b["transition"]
    result = {
        "basis_convention_map": {
            "matrix_units": "vec_F(rho)=(rho00,rho10,rho01,rho11)",
            "bloch": "q=(r_x,r_y,r_z,1), rho=(I+r.sigma)/2",
            "S_where_vec_rho_equals_Sq": [
                [[[float(z.real), float(z.imag)] for z in row] for row in s]
            ][0],
            "generator_map": "G_aug=S^{-1} L_matrix-unit S",
            "observable_map": "a=(1+Mzz+vz)/2; b=(1+Mzz-vz)/2",
            "author_code_map": "Julia arrays are column-major; E[1,1] and E[4,4] are survival probabilities for E00 and E11. Its reshuffle maps J_phi=gamma P_o tensor conj(P_i) to Phi(rho)=A rho A^dagger with A=sqrt(gamma)|psi_o><psi_i|.",
        },
        "row_by_row_generator_comparison": row_comparison,
        "generator_max_abs_residual": float(np.max(np.abs(residual))),
        "generator_last_row_max_abs": float(np.max(np.abs(aug_from_a[3, :]))),
        "transition_a_abs_residual": abs(ta["a"] - tb["a"]),
        "transition_b_abs_residual": abs(ta["b"] - tb["b"]),
        "transition_max_abs_residual": max(abs(ta["a"] - tb["a"]), abs(ta["b"] - tb["b"])),
        "finite_channel_checks": {
            "choi_eigenvalues": [float(x) for x in choi_eigs],
            "choi_min_eigenvalue": float(choi_eigs[0]),
            "choi_hermiticity_max_abs": float(np.max(np.abs(choi - choi.conj().T))),
            "probability_min": float(
                min(channel[0, 0].real, channel[3, 0].real, channel[0, 3].real, channel[3, 3].real)
            ),
            "probability_max": float(
                max(channel[0, 0].real, channel[3, 0].real, channel[0, 3].real, channel[3, 3].real)
            ),
        },
        "threshold": 1e-10,
        "status": "pass" if max(float(np.max(np.abs(residual))), abs(ta["a"] - tb["a"]), abs(ta["b"] - tb["b"])) < 1e-10 and choi_eigs[0] >= -1e-12 else "fail",
    }
    Path(args.json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("EXPLICIT BASIS/CONVENTION MAP")
    print(json.dumps(result["basis_convention_map"], indent=2))
    print("\nROW-BY-ROW AUGMENTED GENERATOR COMPARISON")
    for row in row_comparison:
        print(f"row {row['row']}")
        for e in row["entries"]:
            print(
                f"  col {e['column']}: A-map={e['from_matrix_units']} "
                f"B={e['from_bloch']} abs={e['abs_residual']:.3e}"
            )
    print("\nSUMMARY")
    print(json.dumps({k: result[k] for k in [
        "generator_max_abs_residual",
        "generator_last_row_max_abs",
        "transition_a_abs_residual",
        "transition_b_abs_residual",
        "transition_max_abs_residual",
        "finite_channel_checks",
        "threshold",
        "status",
    ]}, indent=2))


if __name__ == "__main__":
    main()
