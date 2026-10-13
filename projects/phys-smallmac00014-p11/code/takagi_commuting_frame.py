#!/usr/bin/env python3
"""Construct and check the Takagi-optimal commuting-effect frame.

This is a deterministic numerical replay of the exact quaternion/two-plane
construction in evidence/takagi-commuting-frame-proof.md.  Floating-point
residuals are diagnostics, not the proof.
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("three_use", ROOT / "code/search_three_use.py")
THREE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(THREE)


def qmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    aw, av = a[0], a[1:]
    bw, bv = b[0], b[1:]
    return np.r_[aw * bw - av @ bv, aw * bv + bw * av + np.cross(av, bv)]


QBASIS = np.eye(4)


def left(a: np.ndarray) -> np.ndarray:
    return np.column_stack([qmul(a, e) for e in QBASIS])


def right(a: np.ndarray) -> np.ndarray:
    return np.column_stack([qmul(e, a) for e in QBASIS])


LEFT = [left(QBASIS[k]) for k in range(1, 4)]
RIGHT = [right(QBASIS[k]) for k in range(1, 4)]


def takagi_mixer(q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vals, w = np.linalg.eigh(q.conj().T @ q)
    w = w[:, np.argsort(vals)[::-1]]
    diagonal = np.diag(w.T @ q @ w)
    w = w @ np.diag(np.exp(-0.5j * np.angle(diagonal)))
    u = w.T
    sigma = np.abs(diagonal)
    return u, sigma


def bloch_forms(frame: list[np.ndarray]) -> list[np.ndarray]:
    forms = []
    for pauli in THREE.PAULI:
        h = np.array([
            [(0.5 * np.trace(frame[i].conj().T @ frame[j] @ pauli)).real
             for j in range(4)] for i in range(4)
        ])
        forms.append((h + h.T) / 2)
    return forms


def c_matrix(h: np.ndarray) -> np.ndarray:
    return np.array([[np.trace(h @ LEFT[a] @ RIGHT[b]) for b in range(3)]
                     for a in range(3)])


def neutral_plane(forms: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, float]:
    cs = [c_matrix(h) for h in forms]

    def unit(t: float) -> np.ndarray:
        return np.array([np.cos(t), np.sin(t), 0.0])

    def cubic(t: float) -> float:
        u = unit(t)
        return float(np.linalg.det(np.column_stack([c.T @ u for c in cs])))

    grid = np.linspace(0.0, np.pi, 257)
    values = [cubic(t) for t in grid]
    root = None
    for a, b, fa, fb in zip(grid[:-1], grid[1:], values[:-1], values[1:]):
        if abs(fa) < 1e-14:
            root = a
            break
        if fa * fb < 0:
            root = brentq(cubic, a, b, xtol=5e-15)
            break
    if root is None:
        root = grid[int(np.argmin(np.abs(values)))]
    u = unit(root)
    constraints = np.vstack([c.T @ u for c in cs])
    _, singular, vh = np.linalg.svd(constraints)
    v = vh[-1]
    gamma = sum(u[a] * LEFT[a] for a in range(3)) @ sum(v[b] * RIGHT[b] for b in range(3))
    eigenvalues, eigenvectors = np.linalg.eigh((gamma + gamma.T) / 2)
    minus = eigenvectors[:, eigenvalues < 0]
    plus = eigenvectors[:, eigenvalues > 0]
    return plus, minus, float(singular[-1])


def plane_map(forms: list[np.ndarray], basis: np.ndarray) -> np.ndarray:
    compressed = [basis.T @ h @ basis for h in forms]
    return np.column_stack([
        np.array([c[0, 0] for c in compressed]),
        np.array([c[0, 1] for c in compressed]),
    ])


def pair_from_double_angle(basis: np.ndarray, coeff: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    coeff = coeff / np.linalg.norm(coeff)
    theta = 0.5 * np.arctan2(coeff[1], coeff[0])
    c, s = np.cos(theta), np.sin(theta)
    return c * basis[:, 0] + s * basis[:, 1], -s * basis[:, 0] + c * basis[:, 1]


def collinear_basis(forms: list[np.ndarray]) -> tuple[np.ndarray, dict[str, float]]:
    plus, minus, null_residual = neutral_plane(forms)
    tp, tm = plane_map(forms, plus), plane_map(forms, minus)
    sp = np.linalg.svd(tp, compute_uv=False)
    sm = np.linalg.svd(tm, compute_uv=False)
    tol = 2e-11
    if sp[1] < tol:
        cp = np.linalg.svd(tp)[2][-1]
        cm = np.array([1.0, 0.0])
    elif sm[1] < tol:
        cp = np.array([1.0, 0.0])
        cm = np.linalg.svd(tm)[2][-1]
    else:
        np_normal = np.cross(tp[:, 0], tp[:, 1])
        nm_normal = np.cross(tm[:, 0], tm[:, 1])
        line = np.cross(np_normal, nm_normal)
        if np.linalg.norm(line) < tol:
            line = tp[:, 0]
        cp = np.linalg.lstsq(tp, line, rcond=None)[0]
        cm = np.linalg.lstsq(tm, line, rcond=None)[0]
    p1, p2 = pair_from_double_angle(plus, cp)
    m1, m2 = pair_from_double_angle(minus, cm)
    o = np.vstack([p1, p2, m1, m2])
    vectors = np.array([[row @ h @ row for h in forms] for row in o])
    singular = np.linalg.svd(vectors, compute_uv=False)
    return o, {
        "neutral_null": null_residual,
        "orthogonal": float(np.linalg.norm(o @ o.T - np.eye(4))),
        "collinear_second_sv": float(singular[1]),
        "collinear_third_sv": float(singular[2]),
    }


def generic_form_checks() -> float:
    worst = 0.0
    for seed in range(12):
        rng = np.random.default_rng(91000 + seed)
        forms = []
        for _ in range(3):
            h = rng.normal(size=(4, 4))
            h = (h + h.T) / 2
            forms.append(h - np.trace(h) * np.eye(4) / 4)
        _, report = collinear_basis(forms)
        worst = max(worst, *report.values())
    return worst


def channel_checks() -> None:
    worst = {"takagi": 0.0, "s": 0.0, "commutator": 0.0, "score": 0.0,
             "construction": 0.0, "brute": 0.0}
    for seed in (14011, 14022, 14033, 14044, 14055, 14066, 14077, 14088):
        frame = THREE.random_frame(seed)
        q = THREE.determinant_form(frame)
        u0, sigma = takagi_mixer(q)
        takagi_residual = np.linalg.norm(u0 @ q @ u0.T - np.diag(sigma))
        transformed = THREE.mix(frame, u0)
        forms = bloch_forms(transformed)
        o, construction = collinear_basis(forms)
        u = o @ u0
        mixed = THREE.mix(frame, u)
        effects = [k.conj().T @ k for k in mixed]
        commutator = max(np.linalg.norm(a @ b - b @ a) for a, b in itertools.product(effects, repeat=2))
        s_value = sum(abs(np.linalg.det(k)) for k in mixed)
        s_residual = abs(s_value - sigma.sum())
        score_residual = 0.0
        for n in range(1, 8):
            fm, fb, _, _ = THREE.fast_scores(frame, u, n=n)
            score_residual = max(score_residual, abs(fm - fb), abs(fb - (1 + sigma.sum() ** n) / 2))
        fm3, fb3 = THREE.brute_scores(frame, u, n=3)
        brute_residual = max(abs(fm3 - fb3), abs(fb3 - (1 + sigma.sum() ** 3) / 2))
        worst["takagi"] = max(worst["takagi"], takagi_residual)
        worst["s"] = max(worst["s"], s_residual)
        worst["commutator"] = max(worst["commutator"], commutator)
        worst["score"] = max(worst["score"], score_residual)
        worst["construction"] = max(worst["construction"], *construction.values())
        worst["brute"] = max(worst["brute"], brute_residual)
        print(f"CHANNEL seed={seed} choi_min={THREE.choi_eigenvalues(frame)[0]:.12e} "
              f"takagi={takagi_residual:.3e} s={s_residual:.3e} commute={commutator:.3e} "
              f"score_n1_7={score_residual:.3e} brute_n3={brute_residual:.3e}")
    print("WORST " + " ".join(f"{key}={value:.3e}" for key, value in worst.items()))
    if max(worst.values()) > 2e-9:
        raise SystemExit("FAIL: construction residual exceeds diagnostic tolerance")


def main() -> None:
    print("TAKAGI_COMMUTING_FRAME_REPLAY_V1")
    print(f"runtime_python={sys.version.split()[0]} numpy={np.__version__} scipy={scipy.__version__}")
    print(f"generic_triple_worst_residual={generic_form_checks():.3e}")
    channel_checks()
    print("STATUS=PASS_FLOATING_POINT_REPLAY_EXACT_PROOF_IS_SEPARATE")


if __name__ == "__main__":
    main()
