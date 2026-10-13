#!/usr/bin/env python3
"""Independent check of an exact all-CPTP Markov upper bound at n=2.

The certificate uses only trace-norm contractivity of CPTP maps, explicit
coarse-instrument images of the Pauli operators, the Markov factorisation, and
Frobenius Cauchy--Schwarz.  Numerical matrices here replay the exact rational
calculation documented in evidence/gad-global-bound.md.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAIRING = ((0, 3), (1, 2))


def gad(p: float, gamma: float) -> list[np.ndarray]:
    q = 1.0 - p
    s = math.sqrt(1.0 - gamma)
    return [
        math.sqrt(p) * np.diag([1.0, s]).astype(complex),
        math.sqrt(p * gamma) * np.array([[0, 1], [0, 0]], complex),
        math.sqrt(q) * np.diag([s, 1.0]).astype(complex),
        math.sqrt(q * gamma) * np.array([[0, 0], [1, 0]], complex),
    ]


def instrument_image(k: list[np.ndarray], b: int, a: np.ndarray) -> np.ndarray:
    return sum((k[x] @ a @ k[x].conj().T for x in PAIRING[b]),
               np.zeros((2, 2), complex))


def trace_norm_hermitian(a: np.ndarray) -> float:
    return float(np.sum(np.abs(np.linalg.eigvalsh((a + a.conj().T) / 2.0))))


def sop(a: np.ndarray) -> np.ndarray:
    return np.kron(a.conj(), a)


def direct_history_fidelity(k: list[np.ndarray]) -> float:
    r1 = {0: I, 1: X}
    r2 = {(0, 0): I, (0, 1): I, (1, 0): X, (1, 1): X}
    ans = 0.0
    for b1, b2 in itertools.product(range(2), repeat=2):
        for x1 in PAIRING[b1]:
            for x2 in PAIRING[b2]:
                a = r2[(b1, b2)] @ k[x2] @ r1[b1] @ k[x1]
                ans += abs(np.trace(a)) ** 2 / 4.0
    return float(ans)


def liouville_history_fidelity(k: list[np.ndarray]) -> float:
    ib = [sum((sop(k[x]) for x in PAIRING[b]), np.zeros((4, 4), complex))
          for b in range(2)]
    r1 = {0: I, 1: X}
    r2 = {(0, 0): I, (0, 1): I, (1, 0): X, (1, 1): X}
    total = np.zeros((4, 4), complex)
    for b1, b2 in itertools.product(range(2), repeat=2):
        total += sop(r2[(b1, b2)]) @ ib[b2] @ sop(r1[b1]) @ ib[b1]
    return float(np.trace(total).real / 4.0)


def main() -> None:
    p = Fraction(18, 25)
    gamma = Fraction(3, 10)
    q = 1 - p
    column_bound_sq = 2 * (1 - gamma) + p * p
    markov_upper = (1 + column_bound_sq) / 4
    history_exact = 1 - gamma + p * gamma * gamma / 2
    certified_gap = history_exact - markov_upper

    k = gad(float(p), float(gamma))
    gram = sum((a.conj().T @ a for a in k), np.zeros((2, 2), complex))
    vectors = np.column_stack([a.reshape(-1, order="F") for a in k])
    choi = vectors @ vectors.conj().T
    images = {(b, name): instrument_image(k, b, a)
              for b in range(2) for name, a in (("X", X), ("Y", Y), ("Z", Z))}
    caps = {}
    for name in ("X", "Y", "Z"):
        caps[name] = sum(trace_norm_hermitian(images[(b, name)]) for b in range(2)) / 2.0

    f_direct = direct_history_fidelity(k)
    f_liouville = liouville_history_fidelity(k)
    expected_caps = {"X": math.sqrt(0.7), "Y": math.sqrt(0.7), "Z": 0.72}

    print("certificate=all-CPTP Markov n=2 upper via Pauli trace-norm contractions")
    print("model=generalized_amplitude_damping;p=18/25;gamma=3/10;pairing=03|12")
    print(f"parameter_region_check=1-p<=gamma<=p:{q <= gamma <= p}")
    print(f"tp_inf_residual={np.linalg.norm(gram-I, ord=np.inf):.3e}")
    print("choi_eigenvalues=" + np.array2string(np.linalg.eigvalsh(choi), precision=15, separator=","))
    print(f"choi_rank_tol_1e-12={np.sum(np.linalg.eigvalsh(choi)>1e-12)}")
    print(f"diagonal_kraus_minor_squared=p*(1-p)*gamma^2={p*q*gamma*gamma}")
    for b in range(2):
        for name in ("X", "Y", "Z"):
            print(f"I{b}({name})=" + np.array2string(images[(b, name)], precision=15, separator=","))
    for name in ("X", "Y", "Z"):
        print(f"bloch_column_cap_{name}={caps[name]:.15f};expected={expected_caps[name]:.15f};residual={abs(caps[name]-expected_caps[name]):.3e}")
    print(f"frobenius_squared_cap=2*(1-gamma)+p^2={column_bound_sq}={float(column_bound_sq):.15f}")
    print(f"F_markov_global_upper=(1+cap)/4={markov_upper}={float(markov_upper):.15f}")
    print(f"F_history_direct={f_direct:.15f}")
    print(f"F_history_liouville={f_liouville:.15f}")
    print(f"F_history_exact=1-gamma+p*gamma^2/2={history_exact}={float(history_exact):.15f}")
    print(f"history_representation_residual={abs(f_direct-f_liouville):.3e}")
    print(f"history_formula_residual={abs(f_direct-float(history_exact)):.3e}")
    print(f"certified_Delta2_lower={certified_gap}={float(certified_gap):.15f}")
    print("scope=upper covers arbitrary qubit CPTP recoveries in the current-bit Markov class; no unitary or Pauli restriction")

    assert q <= gamma <= p
    assert np.linalg.norm(gram - I, ord=np.inf) < 1e-14
    assert np.sum(np.linalg.eigvalsh(choi) > 1e-12) == 4
    assert max(abs(caps[name] - expected_caps[name]) for name in caps) < 1e-14
    assert abs(f_direct - float(history_exact)) < 2e-15
    assert abs(f_liouville - float(history_exact)) < 2e-15
    assert certified_gap == Fraction(7, 2500)


if __name__ == "__main__":
    main()
