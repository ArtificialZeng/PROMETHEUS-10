#!/usr/bin/env python3
"""Frozen-seed search for three-use history advantage in full-rank qubit channels.

The fast evaluator uses the qubit identities

  F_B,n(U) = (1 + s(U)**n)/2,  s(U) = sum_x |det K_x(U)|,
  F_M,n(U) = (1 + tr(R(U)**n))/4,
  R(U) = s(U) I_3 + 2 sum_x b_x b_x^T,

where |K_x| = a_x I + b_x.sigma.  The reported finalist is replayed by
explicit enumeration of all 4**3 Kraus histories, without using either fast
score identity.  This is a bounded numerical search, not a global certificate
for the Markovian maximum.
"""

from __future__ import annotations

import itertools
import json
import sys

import numpy as np
import scipy
from scipy.linalg import expm
from scipy.optimize import minimize


I2 = np.eye(2, dtype=complex)
PAULI = (
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
)


def matrix_abs(a: np.ndarray) -> np.ndarray:
    gram = a.conj().T @ a
    vals, vecs = np.linalg.eigh((gram + gram.conj().T) / 2)
    if vals.min() < -3e-12:
        raise ValueError(f"negative Gram eigenvalue {vals.min()}")
    return (vecs * np.sqrt(np.maximum(vals, 0.0))) @ vecs.conj().T


def invsqrt(a: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh((a + a.conj().T) / 2)
    if vals.min() <= 0:
        raise ValueError("normalization matrix is not positive definite")
    return (vecs * (1 / np.sqrt(vals))) @ vecs.conj().T


def random_frame(seed: int) -> list[np.ndarray]:
    """Four generic Kraus matrices, right-normalized to a CPTP frame."""
    rng = np.random.default_rng(seed)
    raw = [rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)) for _ in range(4)]
    normalizer = invsqrt(sum(g.conj().T @ g for g in raw))
    return [g @ normalizer for g in raw]


def mix(frame: list[np.ndarray], u: np.ndarray) -> list[np.ndarray]:
    return [sum(u[x, a] * frame[a] for a in range(4)) for x in range(4)]


def haar(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    return q @ np.diag((phases / np.abs(phases)).conj())


def hermitian(x: np.ndarray) -> np.ndarray:
    h = np.zeros((4, 4), dtype=complex)
    h[np.diag_indices(4)] = x[:4]
    cursor = 4
    for i in range(4):
        for j in range(i + 1, 4):
            h[i, j] = x[cursor] + 1j * x[cursor + 1]
            h[j, i] = h[i, j].conj()
            cursor += 2
    return h


def cptp_residual(frame: list[np.ndarray]) -> float:
    return float(np.linalg.norm(sum(a.conj().T @ a for a in frame) - I2))


def nonunital_residual(frame: list[np.ndarray]) -> float:
    return float(np.linalg.norm(sum(a @ a.conj().T for a in frame) - I2))


def choi_eigenvalues(frame: list[np.ndarray]) -> np.ndarray:
    j = sum(np.outer(a.reshape(-1, order="F"), a.reshape(-1, order="F").conj())
            for a in frame)
    return np.linalg.eigvalsh((j + j.conj().T) / 2)


def determinant_form(frame: list[np.ndarray]) -> np.ndarray:
    """Symmetric Q such that det(sum_a u_a A_a) = u^T Q u."""
    q = np.zeros((4, 4), dtype=complex)
    for a in range(4):
        q[a, a] = np.linalg.det(frame[a])
        for b in range(a + 1, 4):
            cross = (np.linalg.det(frame[a] + frame[b])
                     - np.linalg.det(frame[a]) - np.linalg.det(frame[b]))
            q[a, b] = q[b, a] = cross / 2
    return q


def fast_scores(frame: list[np.ndarray], u: np.ndarray, n: int = 3) -> tuple[float, float, float, np.ndarray]:
    ks = mix(frame, u)
    ps = [matrix_abs(k) for k in ks]
    s = float(sum(abs(np.linalg.det(k)) for k in ks))
    bmat = np.zeros((3, 3), dtype=float)
    for p in ps:
        b = np.array([0.5 * np.trace(p @ sig).real for sig in PAULI])
        bmat += np.outer(b, b)
    r = s * np.eye(3) + 2 * bmat
    fm = float((1 + np.trace(np.linalg.matrix_power(r, n)).real) / 4)
    fb = float((1 + s**n) / 2)
    return fm, fb, s, bmat


def brute_scores(frame: list[np.ndarray], u: np.ndarray, n: int = 3) -> tuple[float, float]:
    ks = mix(frame, u)
    ps = [matrix_abs(k) for k in ks]
    markov = 0.0
    bayes = 0.0
    for hist in itertools.product(range(4), repeat=n):
        lm = I2.copy()
        raw = I2.copy()
        for x in hist:
            lm = ps[x] @ lm
            raw = ks[x] @ raw
        markov += abs(np.trace(lm)) ** 2 / 4
        bayes += np.trace(matrix_abs(raw)).real ** 2 / 4
    return float(markov), float(bayes)


def optimize_markov(frame: list[np.ndarray], search_seed: int, screens: int = 700,
                     starts: int = 6) -> dict:
    rng = np.random.default_rng(search_seed)
    population = [np.eye(4, dtype=complex)] + [haar(rng) for _ in range(screens)]
    ranked = sorted(((fast_scores(frame, u)[0], u) for u in population),
                    key=lambda item: item[0], reverse=True)
    best_score, best_u = ranked[0]
    reports = []
    for initial, u0 in ranked[:starts]:
        def objective(x: np.ndarray) -> float:
            return -fast_scores(frame, expm(1j * hermitian(x)) @ u0)[0]

        opt = minimize(objective, np.zeros(16), method="BFGS",
                       options={"gtol": 1e-10, "maxiter": 260, "disp": False})
        u = expm(1j * hermitian(opt.x)) @ u0
        val = fast_scores(frame, u)[0]
        reports.append({
            "initial": float(initial), "final": float(val),
            "success": bool(opt.success), "nit": int(opt.nit),
            "grad_norm": None if opt.jac is None else float(np.linalg.norm(opt.jac)),
        })
        if val > best_score:
            best_score, best_u = val, u
    return {"score": float(best_score), "u": best_u, "screen_best": float(ranked[0][0]),
            "screen_second": float(ranked[1][0]), "reports": reports}


def optimize_bayes_feasible(frame: list[np.ndarray], search_seed: int, screens: int = 350,
                            starts: int = 3) -> dict:
    rng = np.random.default_rng(search_seed)
    population = [np.eye(4, dtype=complex)] + [haar(rng) for _ in range(screens)]
    ranked = sorted(((fast_scores(frame, u)[2], u) for u in population),
                    key=lambda item: item[0], reverse=True)
    best_s, best_u = ranked[0]
    reports = []
    for initial, u0 in ranked[:starts]:
        def objective(x: np.ndarray) -> float:
            return -fast_scores(frame, expm(1j * hermitian(x)) @ u0)[2]

        opt = minimize(objective, np.zeros(16), method="BFGS",
                       options={"gtol": 1e-11, "maxiter": 260, "disp": False})
        u = expm(1j * hermitian(opt.x)) @ u0
        sval = fast_scores(frame, u)[2]
        reports.append({"initial_s": float(initial), "final_s": float(sval),
                        "success": bool(opt.success), "nit": int(opt.nit)})
        if sval > best_s:
            best_s, best_u = sval, u
    return {"s": float(best_s), "u": best_u, "reports": reports}


def serial_complex(a: np.ndarray) -> list[list[list[float]]]:
    return [[[float(z.real), float(z.imag)] for z in row] for row in a]


def main() -> None:
    print("THREE_USE_SEARCH_V1")
    print(f"runtime python={sys.version.split()[0]} numpy={np.__version__} scipy={scipy.__version__}")
    seeds = (14011, 14022, 14033, 14044, 14055, 14066, 14077, 14088)
    summaries = []
    for index, seed in enumerate(seeds):
        frame = random_frame(seed)
        q = determinant_form(frame)
        s_upper = float(np.linalg.svd(q, compute_uv=False).sum())
        b_upper = float((1 + s_upper**3) / 2)
        opt_m = optimize_markov(frame, 70000 + seed)
        gap_to_b_upper = b_upper - opt_m["score"]
        summary = {
            "seed": seed,
            "cptp_residual": cptp_residual(frame),
            "nonunital_residual": nonunital_residual(frame),
            "choi_eigenvalues": [float(x) for x in choi_eigenvalues(frame)],
            "bayes_s_global_upper": s_upper,
            "bayes_f3_global_upper": b_upper,
            "markov_f3_numerical_lower": opt_m["score"],
            "observed_gap_to_bayes_upper": gap_to_b_upper,
            "screen_best": opt_m["screen_best"],
            "best_local_values": sorted([x["final"] for x in opt_m["reports"]], reverse=True),
        }
        summaries.append((gap_to_b_upper, frame, opt_m, summary))
        print("CHANNEL " + json.dumps(summary, sort_keys=True, separators=(",", ":")))

    # Replay the channel with the largest observed separation from the exact Bayesian ceiling.
    _, frame, opt_m, summary = max(summaries, key=lambda item: item[0])
    opt_b = optimize_bayes_feasible(frame, 99000 + summary["seed"])
    fm_fast, fb_at_m, s_at_m, bmat = fast_scores(frame, opt_m["u"])
    fm_brute, fb_brute_at_m = brute_scores(frame, opt_m["u"])
    fm_at_b, fb_fast, s_feasible, bmat_b = fast_scores(frame, opt_b["u"])
    fm_brute_at_b, fb_brute = brute_scores(frame, opt_b["u"])
    finalist = {
        **summary,
        "bayes_feasible_f3": fb_fast,
        "bayes_feasible_s": s_feasible,
        "bayes_upper_minus_feasible": summary["bayes_f3_global_upper"] - fb_fast,
        "markov_fast": fm_fast,
        "markov_brute": fm_brute,
        "markov_replay_residual": abs(fm_fast - fm_brute),
        "bayes_at_markov_fast": fb_at_m,
        "bayes_at_markov_brute": fb_brute_at_m,
        "bayes_markov_u_replay_residual": abs(fb_at_m - fb_brute_at_m),
        "bayes_fast": fb_fast,
        "bayes_brute": fb_brute,
        "bayes_replay_residual": abs(fb_fast - fb_brute),
        "markov_at_bayes_fast": fm_at_b,
        "markov_at_bayes_brute": fm_brute_at_b,
        "markov_bayes_u_replay_residual": abs(fm_at_b - fm_brute_at_b),
        "s_at_markov": s_at_m,
        "bmat_eigenvalues_at_markov": [float(x) for x in np.linalg.eigvalsh(bmat)],
        "bmat_eigenvalues_at_bayes": [float(x) for x in np.linalg.eigvalsh(bmat_b)],
        "markov_u": serial_complex(opt_m["u"]),
        "bayes_u": serial_complex(opt_b["u"]),
        "frame": [serial_complex(a) for a in frame],
        "markov_local_reports": opt_m["reports"],
        "bayes_local_reports": opt_b["reports"],
        "scope": "frozen-seed numerical lower bounds; Bayesian ceiling analytic; no certified strict Markovian upper bound",
    }
    print("FINALIST " + json.dumps(finalist, sort_keys=True, separators=(",", ":")))
    if finalist["cptp_residual"] > 3e-13 or finalist["choi_eigenvalues"][0] <= 1e-8:
        raise SystemExit("FAIL: finalist is not strict full-rank CPTP")
    if finalist["nonunital_residual"] <= 1e-6:
        raise SystemExit("FAIL: finalist is not demonstrably nonunital")
    if max(finalist["markov_replay_residual"], finalist["bayes_replay_residual"],
           finalist["bayes_markov_u_replay_residual"],
           finalist["markov_bayes_u_replay_residual"]) > 2e-11:
        raise SystemExit("FAIL: independent replay mismatch")
    print("STATUS PASS_NUMERICAL_SEARCH_NOT_GLOBAL_MARKOV_CERTIFICATE")


if __name__ == "__main__":
    main()
