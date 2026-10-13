#!/usr/bin/env python3
"""Deterministic discovery scan of the Takagi-optimal O(4) family.

This is finite-precision discovery evidence, not a global certificate.  A full-rank
qubit CPTP channel is generated from four complex 2x2 matrices by right TP
normalization.  The Kraus-column matrix uses vec_F(K)/sqrt(2), matching the
input-tensor-output Choi convention in problem.md.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm
from scipy.optimize import least_squares


Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SPIN = np.kron(Y, Y)
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]


def psqrt(h: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh((h + h.conj().T) / 2)
    if np.min(w) < -2e-12:
        raise RuntimeError(f"non-positive input, min eigenvalue {np.min(w)}")
    return (v * np.sqrt(np.maximum(w, 0.0))) @ v.conj().T


def random_cptp(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(4, 2, 2)) + 1.0j * rng.normal(size=(4, 2, 2))
    gram = sum(k.conj().T @ k for k in raw)
    w, v = np.linalg.eigh(gram)
    invsqrt = (v * (1.0 / np.sqrt(w))) @ v.conj().T
    return raw @ invsqrt


def kraus_columns(kraus: np.ndarray) -> np.ndarray:
    return np.column_stack([k.reshape(4, order="F") / np.sqrt(2.0) for k in kraus])


def columns_to_kraus(x: np.ndarray) -> np.ndarray:
    return np.stack(
        [(np.sqrt(2.0) * x[:, i]).reshape((2, 2), order="F") for i in range(4)]
    )


@dataclass
class Takagi:
    t: np.ndarray
    singular_values: np.ndarray
    diagonal_residual: float
    reconstruction_residual: float


def takagi_from_qdagq(q: np.ndarray) -> Takagi:
    """Independent eigensystem construction of T^T Q T = diag(sigma).

    This branch assumes the generic, nondegenerate singular values used in the
    deterministic scan.  Degeneracy would require an additional block Takagi step.
    """
    eigenvalues, e = np.linalg.eigh(q.conj().T @ q)
    order = np.argsort(eigenvalues)[::-1]
    e = e[:, order]
    raw = e.T @ q @ e
    off = raw - np.diag(np.diag(raw))
    phases = np.exp(-0.5j * np.angle(np.diag(raw)))
    t = e @ np.diag(phases)
    d = t.T @ q @ t
    sigma = np.real(np.diag(d))
    reconstructed = t.conj() @ np.diag(sigma) @ t.conj().T
    return Takagi(
        t=t,
        singular_values=sigma,
        diagonal_residual=float(np.linalg.norm(off)),
        reconstruction_residual=float(np.linalg.norm(q - reconstructed)),
    )


def takagi_from_svd(q: np.ndarray) -> Takagi:
    """Second construction using the left/right phase relation in an SVD."""
    left, sigma, vh = np.linalg.svd(q)
    right = vh.conj().T
    phase_square = np.asarray([left[:, i].T @ right[:, i] for i in range(4)])
    w = left @ np.diag(np.exp(-0.5j * np.angle(phase_square)))
    t = w.conj()
    d = t.T @ q @ t
    reconstructed = t.conj() @ np.diag(sigma) @ t.conj().T
    return Takagi(
        t=t,
        singular_values=sigma,
        diagonal_residual=float(np.linalg.norm(d - np.diag(np.diag(d)))),
        reconstruction_residual=float(np.linalg.norm(q - reconstructed)),
    )


def skew(parameters: np.ndarray) -> np.ndarray:
    a = np.zeros((4, 4), dtype=float)
    for value, (i, j) in zip(parameters, PAIRS):
        a[i, j] = value
        a[j, i] = -value
    return a


def orthogonal(parameters: np.ndarray) -> np.ndarray:
    return expm(skew(parameters))


def orthogonal_givens(parameters: np.ndarray) -> np.ndarray:
    out = np.eye(4)
    for theta, (i, j) in zip(parameters, PAIRS):
        g = np.eye(4)
        c, s = np.cos(theta), np.sin(theta)
        g[i, i], g[j, j] = c, c
        g[i, j], g[j, i] = -s, s
        out = out @ g
    return out


def mixed_kraus(x: np.ndarray, t: np.ndarray, parameters: np.ndarray) -> np.ndarray:
    # X -> X V, V=T O.  Hence the environment row mixing is U=V^T.
    return columns_to_kraus(x @ t @ orthogonal(parameters))


def positive_parts(kraus: np.ndarray) -> list[np.ndarray]:
    return [psqrt(k.conj().T @ k) for k in kraus]


def commutator_vector(parameters: np.ndarray, x: np.ndarray, t: np.ndarray) -> np.ndarray:
    parts = positive_parts(mixed_kraus(x, t, parameters))
    out = []
    for i, j in PAIRS:
        c = parts[i] @ parts[j] - parts[j] @ parts[i]
        out.extend(np.real(c).ravel())
        out.extend(np.imag(c).ravel())
    return np.asarray(out)


def commutator_vector_givens(parameters: np.ndarray, x: np.ndarray, t: np.ndarray) -> np.ndarray:
    parts = positive_parts(columns_to_kraus(x @ t @ orthogonal_givens(parameters)))
    out = []
    for i, j in PAIRS:
        c = parts[i] @ parts[j] - parts[j] @ parts[i]
        out.extend(np.real(c).ravel())
        out.extend(np.imag(c).ravel())
    return np.asarray(out)


def fidelity_values(kraus: np.ndarray) -> tuple[float, float, float, float]:
    parts = positive_parts(kraus)
    fm = 0.25 * sum(
        float(np.real(np.trace(parts[j] @ parts[i]))) ** 2
        for i in range(4)
        for j in range(4)
    )
    fb = 0.0
    for i in range(4):
        for j in range(4):
            x = kraus[j] @ parts[i]
            fb += np.sum(np.linalg.svd(x, compute_uv=False)) ** 2 / 4.0
    dsum = sum(abs(np.linalg.det(k)) for k in kraus)
    gap_identity = 0.125 * sum(
        np.linalg.norm(parts[i] @ parts[j] - parts[j] @ parts[i]) ** 2
        for i in range(4)
        for j in range(4)
    )
    return float(fm), float(fb), float(dsum), float(gap_identity)


def scan_seed(seed: int, starts: int, max_nfev: int) -> dict:
    kraus = random_cptp(seed)
    x = kraus_columns(kraus)
    q = x.T @ SPIN @ x
    tk = takagi_from_qdagq(q)
    tk_svd = takagi_from_svd(q)
    rng = np.random.default_rng(seed + 10_000)

    candidates = []
    initial = [np.zeros(6)] + [rng.uniform(-np.pi, np.pi, size=6) for _ in range(starts - 1)]
    for p0 in initial:
        result = least_squares(
            commutator_vector,
            p0,
            args=(x, tk.t),
            method="trf",
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
            max_nfev=max_nfev,
        )
        candidates.append((float(np.dot(result.fun, result.fun)), result.x, result.nfev))
    candidates.sort(key=lambda item: item[0])
    residual_sq, pbest, nfev = candidates[0]
    kbest = mixed_kraus(x, tk.t, pbest)
    fm, fb, dsum, gap_identity = fidelity_values(kbest)

    # Independent SO(4) coordinates: a fixed product of six plane rotations.
    givens_candidates = []
    for p0 in [np.zeros(6)] + [rng.uniform(-np.pi, np.pi, size=6) for _ in range(max(7, starts // 2) - 1)]:
        result = least_squares(
            commutator_vector_givens,
            p0,
            args=(x, tk_svd.t),
            method="trf",
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
            max_nfev=max_nfev,
        )
        givens_candidates.append(float(np.dot(result.fun, result.fun)))

    tp = sum(k.conj().T @ k for k in kraus)
    j = 2.0 * x @ x.conj().T
    q_diag = tk.t.T @ q @ tk.t
    determinant_match = max(
        abs(abs(x[:, a].T @ SPIN @ x[:, a]) - abs(np.linalg.det(kraus[a])))
        for a in range(4)
    )
    sigma_svd = np.linalg.svd(q, compute_uv=False)
    return {
        "seed": seed,
        "choi_eigenvalues": [float(v) for v in np.linalg.eigvalsh(j)],
        "choi_rank_tolerance_1e-12": int(np.linalg.matrix_rank(j, tol=1e-12)),
        "tp_residual_fro": float(np.linalg.norm(tp - np.eye(2))),
        "q_singular_values": [float(v) for v in sigma_svd],
        "q_min_singular_value": float(np.min(sigma_svd)),
        "q_distinct_min_gap": float(np.min(np.abs(np.diff(np.sort(sigma_svd))))),
        "takagi_diagonal_residual_fro": tk.diagonal_residual,
        "takagi_reconstruction_residual_fro": tk.reconstruction_residual,
        "takagi_unitarity_residual_fro": float(np.linalg.norm(tk.t.conj().T @ tk.t - np.eye(4))),
        "takagi_diagonal_imag_max": float(np.max(np.abs(np.imag(np.diag(q_diag))))),
        "takagi_sigma_vs_svd_max": float(np.max(np.abs(np.sort(tk.singular_values) - np.sort(sigma_svd)))),
        "svd_takagi_diagonal_residual_fro": tk_svd.diagonal_residual,
        "svd_takagi_reconstruction_residual_fro": tk_svd.reconstruction_residual,
        "two_takagi_frames_abs_overlap_offdiag_max": float(
            np.max(np.abs((tk.t.conj().T @ tk_svd.t) - np.diag(np.diag(tk.t.conj().T @ tk_svd.t))))
        ),
        "original_qdiag_absdet_max_residual": float(determinant_match),
        "o4_starts": starts,
        "best_least_squares_residual_sq": residual_sq,
        "best_least_squares_residual_norm": float(np.sqrt(residual_sq)),
        "best_least_squares_nfev": int(nfev),
        "best_independent_svd_givens_residual_sq": float(min(givens_candidates)),
        "best_parameter_vector": [float(v) for v in pbest],
        "at_best_fm": fm,
        "at_best_fb": fb,
        "at_best_direct_gap": fb - fm,
        "at_best_commutator_gap_identity": gap_identity,
        "at_best_determinant_sum": dsum,
        "analytic_determinant_sum_max": float(np.sum(sigma_svd)),
        "determinant_sum_max_residual": float(abs(dsum - np.sum(sigma_svd))),
        "fb_trace_determinant_identity_residual": float(abs(fb - (1.0 + dsum * dsum) / 2.0)),
        "gap_identity_residual": float(abs((fb - fm) - gap_identity)),
        "local_minima_residual_sq_first_ten": [float(c[0]) for c in candidates[:10]],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[20260913, 20260914, 20260915])
    parser.add_argument("--starts", type=int, default=32)
    parser.add_argument("--max-nfev", type=int, default=3000)
    args = parser.parse_args()
    records = [scan_seed(seed, args.starts, args.max_nfev) for seed in args.seeds]
    print(json.dumps({"precision": "numpy complex128/float64", "records": records}, indent=2))


if __name__ == "__main__":
    main()
