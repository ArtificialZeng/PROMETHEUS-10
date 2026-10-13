#!/usr/bin/env python3
"""Complete first-order U(16) tangent split and numerical entropy Hessian.

The flag basis is x=(I,J), I,J=0,...,3.  At the canonical isometry W=I,
the coefficient matrix across AA':BB' is

    M(W)_(I,a),(J,b) = C_(I,J) W_(a,b),(I,J).

All generators below are orthonormal for Re Tr(K^* L).  The fixed-rank
tangent kernel consists exactly of diagonal generators and grid edges sharing
I or J.  The complementary grid edges open Schmidt support at first order.
"""

from __future__ import annotations

import platform
import sys

import numpy as np
import scipy
from scipy.linalg import null_space, svdvals


R = 0.5
N = 16
IDENTITY = np.eye(N, dtype=complex)
C1 = np.array([[R, 1.0], [1.0, 1.0]]) / np.sqrt(3.0 + R * R)
C = np.kron(C1, C1)


def coefficient_matrix(w: np.ndarray) -> np.ndarray:
    return np.einsum(
        "ij,abij->iajb", C, w.reshape(4, 4, 4, 4), optimize=True
    ).reshape(16, 16)


def entropy(w: np.ndarray, top_four_only: bool = False) -> float:
    squared = svdvals(coefficient_matrix(w)) ** 2
    if top_four_only:
        squared = squared[:4]
    squared = squared[squared > 1.0e-28]
    return float(-np.sum(squared * np.log2(squared)))


F0 = entropy(IDENTITY, top_four_only=True)


def u4_basis() -> list[np.ndarray]:
    answer: list[np.ndarray] = []
    for x in range(4):
        k = np.zeros((4, 4), dtype=complex)
        k[x, x] = 1j
        answer.append(k)
    for x in range(4):
        for y in range(x + 1, 4):
            k = np.zeros((4, 4), dtype=complex)
            k[y, x] = 1.0 / np.sqrt(2.0)
            k[x, y] = -1.0 / np.sqrt(2.0)
            answer.append(k)
            k = np.zeros((4, 4), dtype=complex)
            k[y, x] = 1j / np.sqrt(2.0)
            k[x, y] = 1j / np.sqrt(2.0)
            answer.append(k)
    return answer


def tangent_bases() -> tuple[list[np.ndarray], list[str], list[np.ndarray]]:
    kernel: list[np.ndarray] = []
    labels: list[str] = []
    opening: list[np.ndarray] = []
    for x in range(16):
        k = np.zeros((16, 16), dtype=complex)
        k[x, x] = 1j
        kernel.append(k)
        labels.append(f"phase({x // 4},{x % 4})")
    for x in range(16):
        i, j = divmod(x, 4)
        for y in range(x + 1, 16):
            a, b = divmod(y, 4)
            destination = kernel if (i == a or j == b) else opening
            for imaginary in (False, True):
                k = np.zeros((16, 16), dtype=complex)
                if imaginary:
                    k[y, x] = 1j / np.sqrt(2.0)
                    k[x, y] = 1j / np.sqrt(2.0)
                else:
                    k[y, x] = 1.0 / np.sqrt(2.0)
                    k[x, y] = -1.0 / np.sqrt(2.0)
                destination.append(k)
                if destination is kernel:
                    kind = "imag" if imaginary else "real"
                    labels.append(f"{kind}({i},{j})-({a},{b})")
    return kernel, labels, opening


KERNEL, LABELS, OPENING = tangent_bases()


def cayley(k: np.ndarray, step: float) -> np.ndarray:
    return np.linalg.solve(IDENTITY - 0.5 * step * k, IDENTITY + 0.5 * step * k)


def directional_curvature(k: np.ndarray, step: float) -> float:
    plus = cayley(k, step)
    minus = plus.conj().T
    return (
        entropy(plus, top_four_only=True)
        + entropy(minus, top_four_only=True)
        - 2.0 * F0
    ) / (step * step)


def richardson_curvature(k: np.ndarray, coarse: float) -> float:
    fine = coarse / 2.0
    return (
        4.0 * directional_curvature(k, fine)
        - directional_curvature(k, coarse)
    ) / 3.0


def hessian(coarse: float) -> np.ndarray:
    diagonal = np.array([richardson_curvature(k, coarse) for k in KERNEL])
    h = np.diag(diagonal)
    for i in range(len(KERNEL)):
        for j in range(i + 1, len(KERNEL)):
            # Polarization of q(v)=v^T H v.
            value = (
                richardson_curvature(KERNEL[i] + KERNEL[j], coarse)
                - diagonal[i]
                - diagonal[j]
            ) / 2.0
            h[i, j] = value
            h[j, i] = value
    return h


def coordinates(k: np.ndarray) -> np.ndarray:
    return np.array([np.trace(b.conj().T @ k).real for b in KERNEL])


def gauge_and_quotient() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    local = u4_basis()
    columns = [coordinates(np.kron(x, np.eye(4))) for x in local]
    columns += [coordinates(np.kron(np.eye(4), y)) for y in local]
    gauge = np.array(columns).T
    quotient = null_space(gauge.T, rcond=1.0e-12)
    singular = np.linalg.svd(gauge, compute_uv=False)
    return gauge, quotient, singular


GAUGE, QUOTIENT, GAUGE_SINGULAR = gauge_and_quotient()


def clusters(values: np.ndarray, tolerance: float = 3.0e-6) -> list[tuple[float, int]]:
    answer: list[list[float | int]] = []
    for value in values:
        if not answer or abs(value - float(answer[-1][0])) > tolerance:
            answer.append([float(value), 1])
        else:
            old_mean, count = float(answer[-1][0]), int(answer[-1][1])
            answer[-1] = [(old_mean * count + value) / (count + 1), count + 1]
    return [(float(mean), int(count)) for mean, count in answer]


def normal_block_norm_squared(k: np.ndarray) -> float:
    m1 = coefficient_matrix(k)
    active = {0, 5, 10, 15}
    normal_rows = [x for x in range(16) if x not in active]
    normal_cols = [x for x in range(16) if x not in active]
    return float(np.linalg.norm(m1[np.ix_(normal_rows, normal_cols)]) ** 2)


def main() -> None:
    print(f"python={platform.python_version()} executable={sys.executable}")
    print(f"numpy={np.__version__} scipy={scipy.__version__}")
    source_norms = [np.linalg.norm(x) for x in KERNEL + OPENING]
    anti_residual = max(np.linalg.norm(x + x.conj().T) for x in KERNEL + OPENING)
    print(
        "basis "
        f"fixed_rank_kernel={len(KERNEL)} support_opening={len(OPENING)} "
        f"total={len(KERNEL)+len(OPENING)} "
        f"norm_range=[{min(source_norms):.17g},{max(source_norms):.17g}] "
        f"antihermitian_residual={anti_residual:.3e}"
    )
    opening_norms = np.array([normal_block_norm_squared(x) for x in OPENING])
    kernel_norms = np.array([normal_block_norm_squared(x) for x in KERNEL])
    print(
        "normal_block_map "
        f"kernel_max_norm2={kernel_norms.max():.3e} "
        f"opening_min_norm2={opening_norms.min():.12e} "
        f"opening_max_norm2={opening_norms.max():.12e}"
    )
    gauge_rank = int(np.sum(GAUGE_SINGULAR > 1.0e-10))
    print(
        "gauge "
        f"columns=32 rank={gauge_rank} quotient_dimension={QUOTIENT.shape[1]} "
        f"smallest_nonzero_singular={GAUGE_SINGULAR[gauge_rank-1]:.15g}"
    )
    print(f"canonical_entropy_bits={F0:.17g}")

    h1 = hessian(2.0e-3)
    h2 = hessian(1.0e-3)
    for coarse, h in ((2.0e-3, h1), (1.0e-3, h2)):
        quotient_spectrum = np.linalg.eigvalsh(QUOTIENT.T @ h @ QUOTIENT)
        full_spectrum = np.linalg.eigvalsh(h)
        print(
            f"hessian coarse={coarse:.1e} "
            f"quotient_min={quotient_spectrum[0]:.15g} "
            f"quotient_max={quotient_spectrum[-1]:.15g} "
            f"full_near_zero={np.sum(np.abs(full_spectrum)<2.0e-6)} "
            f"min_full={full_spectrum[0]:.3e} "
            f"gauge_residual_op={np.linalg.norm(h @ GAUGE,2):.3e}"
        )
    quotient_spectrum = np.linalg.eigvalsh(QUOTIENT.T @ h1 @ QUOTIENT)
    print("quotient_spectrum_clusters_bits_per_t2")
    for mean, multiplicity in clusters(quotient_spectrum):
        print(f"  {mean:.12f} multiplicity={multiplicity}")
    print(
        "hessian_scale_difference_op="
        f"{np.linalg.norm(QUOTIENT.T @ (h2-h1) @ QUOTIENT,2):.6e}"
    )

    # The weakest quotient mode is phase-only; record its normalized phase table.
    eigenvalues, eigenvectors = np.linalg.eigh(QUOTIENT.T @ h1 @ QUOTIENT)
    weakest_coordinates = QUOTIENT @ eigenvectors[:, 0]
    phase_weight = np.linalg.norm(weakest_coordinates[:16]) ** 2
    rook_weight = np.linalg.norm(weakest_coordinates[16:]) ** 2
    phase = weakest_coordinates[:16].reshape(4, 4)
    if phase[0, 0] < 0:
        phase = -phase
    print(
        f"weakest_mode curvature={eigenvalues[0]:.15g} "
        f"phase_weight={phase_weight:.12g} rook_weight={rook_weight:.12g}"
    )
    print("weakest_phase_table")
    for row in phase:
        print("  " + " ".join(f"{x:+.17g}" for x in row))

    # A full random U(16) direction checks the vanishing symmetric first derivative.
    rng = np.random.default_rng(2201)
    z = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16))
    random_k = z - z.conj().T
    random_k /= np.linalg.norm(random_k)
    for step in (2.0e-3, 1.0e-3, 5.0e-4):
        plus = cayley(random_k, step)
        minus = plus.conj().T
        derivative = (entropy(plus) - entropy(minus)) / (2.0 * step)
        print(f"stationarity_random step={step:.1e} symmetric_slope={derivative:.12e}")

    # An explicit both-coordinate edge illustrates the universal -t^2 log(t^2) term.
    opening_k = np.zeros((16, 16), dtype=complex)
    x, y = 0, 5  # (I,J)=(0,0) and (1,1)
    opening_k[y, x] = 1.0 / np.sqrt(2.0)
    opening_k[x, y] = -1.0 / np.sqrt(2.0)
    mu = normal_block_norm_squared(opening_k)
    print(f"support_example edge=(0,0)-(1,1) mu_norm2={mu:.17g}")
    for step in (2.0e-2, 1.0e-2, 5.0e-3, 2.5e-3, 1.25e-3):
        delta = entropy(cayley(opening_k, step)) - F0
        leading = -2.0 * mu * step * step * np.log2(step)
        print(
            f"support_example step={step:.5e} delta_bits={delta:.12e} "
            f"leading_bits={leading:.12e} ratio={delta/leading:.9f}"
        )


if __name__ == "__main__":
    main()
