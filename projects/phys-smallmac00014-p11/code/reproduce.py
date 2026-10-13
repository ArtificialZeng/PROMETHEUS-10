#!/usr/bin/env python3
"""Independent source reconstruction and baseline checks for phys-00014-p11.

Conventions
-----------
Kraus operators act on column vectors in the ordered basis (|0>, |1>).
Rows of U mix a source Kraus frame: K_x = sum_a U[x,a] A_a.
Histories are chronological (x1,...,xn), so an uncorrected branch is
K[xn] ... K[x1].  All Choi--Bell fidelities use normalized
|Phi> = (|00>+|11>)/sqrt(2).
"""

from __future__ import annotations

import itertools
import json
import sys
from dataclasses import dataclass

import numpy as np
import scipy
from scipy.linalg import expm
from scipy.optimize import minimize


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PHI = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2.0)


def matrix_abs(a: np.ndarray, tol: float = 2e-13) -> np.ndarray:
    """Positive square root |a|=(a^dagger a)^(1/2), via Hermitian eigh."""
    gram = a.conj().T @ a
    gram = (gram + gram.conj().T) / 2
    vals, vecs = np.linalg.eigh(gram)
    if vals.min() < -tol:
        raise ValueError(f"non-positive Gram eigenvalue {vals.min():.3e}")
    vals = np.maximum(vals, 0.0)
    return (vecs * np.sqrt(vals)) @ vecs.conj().T


def polar_unitary(a: np.ndarray) -> np.ndarray:
    """Unitary polar factor, with the SVD providing a kernel extension."""
    left, _, right_h = np.linalg.svd(a)
    return left @ right_h


def mix_kraus(frame: list[np.ndarray], u: np.ndarray) -> list[np.ndarray]:
    if u.shape != (len(frame), len(frame)):
        raise ValueError("mixing unitary and Kraus frame have incompatible sizes")
    return [sum(u[x, a] * frame[a] for a in range(len(frame))) for x in range(len(frame))]


def cptp_residual(frame: list[np.ndarray]) -> float:
    total = sum(k.conj().T @ k for k in frame)
    return float(np.linalg.norm(total - I2, ord="fro"))


def choi_spectrum(frame: list[np.ndarray]) -> np.ndarray:
    # Unnormalized column-vectorized Choi matrix; its trace is d=2.
    choi = sum(np.outer(k.reshape(-1, order="F"), k.reshape(-1, order="F").conj()) for k in frame)
    return np.linalg.eigvalsh((choi + choi.conj().T) / 2)


def bell_fidelity(branches: list[np.ndarray]) -> float:
    """Direct Choi--Bell evaluation, without using the trace identity."""
    rho = np.zeros((4, 4), dtype=complex)
    for branch in branches:
        vec = np.kron(I2, branch) @ PHI
        rho += np.outer(vec, vec.conj())
    return float(np.real(PHI.conj() @ rho @ PHI))


def trace_fidelity(branches: list[np.ndarray]) -> float:
    return float(sum(abs(np.trace(branch)) ** 2 for branch in branches) / 4.0)


@dataclass
class Scores:
    markov_trace: float
    markov_bell: float
    bayes_recursive_trace: float
    bayes_recursive_bell: float
    final_only_trace: float
    final_only_bell: float
    max_markov_trace_imag: float


def branch_scores(frame: list[np.ndarray], n: int) -> Scores:
    """Enumerate every r^n branch in three independent representations."""
    abs_frame = [matrix_abs(k) for k in frame]
    markov: list[np.ndarray] = []
    bayes_recursive: list[np.ndarray] = []
    final_only: list[np.ndarray] = []
    max_imag = 0.0

    for history in itertools.product(range(len(frame)), repeat=n):
        raw = I2.copy()
        m_branch = I2.copy()
        b_branch = None
        for x in history:
            raw = frame[x] @ raw
            m_branch = abs_frame[x] @ m_branch
            b_branch = abs_frame[x] if b_branch is None else matrix_abs(frame[x] @ b_branch)
        assert b_branch is not None
        markov.append(m_branch)
        bayes_recursive.append(b_branch)
        final_only.append(matrix_abs(raw))
        max_imag = max(max_imag, abs(float(np.imag(np.trace(m_branch)))))

    return Scores(
        markov_trace=trace_fidelity(markov),
        markov_bell=bell_fidelity(markov),
        bayes_recursive_trace=trace_fidelity(bayes_recursive),
        bayes_recursive_bell=bell_fidelity(bayes_recursive),
        final_only_trace=trace_fidelity(final_only),
        final_only_bell=bell_fidelity(final_only),
        max_markov_trace_imag=max_imag,
    )


def example8_direct(lam: float, theta23: float = 0.0) -> list[np.ndarray]:
    """Input A: direct row-by-row transcription of Rexiti et al. Eqs. (35),(39)-(43)."""
    t1 = np.sqrt(lam) * np.array([[1, 0], [0, 0]], dtype=complex)
    t2 = np.sqrt(lam) * np.array([[0, 1], [0, 0]], dtype=complex)
    t3 = np.sqrt(1 - lam) * I2
    theta13 = np.pi / 2 - 0.5 * np.arcsin(np.sqrt(lam))  # Eq. (43), k=1
    c13, s13 = np.cos(theta13), np.sin(theta13)
    c23, s23 = np.cos(theta23), np.sin(theta23)
    return [
        c13 * t1 + s13 * t3,
        -s13 * s23 * t1 + c23 * t2 + c13 * s23 * t3,
        -s13 * c23 * t1 - s23 * t2 + c13 * c23 * t3,
    ]


def extreme_rank2(theta: float, phi: float) -> tuple[np.ndarray, np.ndarray]:
    """Rexiti et al. Eq. (20), independently used to derive Input B."""
    t0 = np.array([[np.cos(theta), 0], [0, np.cos(phi)]], dtype=complex)
    t1 = np.array([[0, np.sin(phi)], [np.sin(theta), 0]], dtype=complex)
    return t0, t1


def example8_derived(lam: float, theta23: float = 0.0) -> list[np.ndarray]:
    """Input B: derive Eq. (35) from the convex-channel construction Eqs. (20)-(23)."""
    first = extreme_rank2(0.0, np.pi / 2)
    second = extreme_rank2(0.0, 0.0)
    four = [np.sqrt(lam) * first[0], np.sqrt(lam) * first[1],
            np.sqrt(1 - lam) * second[0], np.sqrt(1 - lam) * second[1]]
    if np.linalg.norm(four[3]) > 5e-15:
        raise AssertionError("the fourth derived Kraus operator should vanish")
    base = four[:3]
    theta13 = np.pi / 2 - 0.5 * np.arcsin(np.sqrt(lam))
    c13, s13 = np.cos(theta13), np.sin(theta13)
    c23, s23 = np.cos(theta23), np.sin(theta23)
    u = np.array([
        [c13, 0, s13],
        [-s13 * s23, c23, c13 * s23],
        [-s13 * c23, -s23, c13 * c23],
    ], dtype=complex)
    return mix_kraus(base, u)


def depolarizing_frame(p: float) -> list[np.ndarray]:
    # E(rho)=(1-p)rho+p I/2; all four Choi eigenvalues are positive for 0<p<1.
    return [np.sqrt(1 - 3 * p / 4) * I2,
            np.sqrt(p / 4) * X, np.sqrt(p / 4) * Y, np.sqrt(p / 4) * Z]


def gad_frame(gamma: float, equilibrium_ground_weight: float) -> list[np.ndarray]:
    """Strictly full-rank generalized amplitude-damping Kraus frame."""
    g, q = gamma, equilibrium_ground_weight
    return [
        np.sqrt(q) * np.array([[1, 0], [0, np.sqrt(1 - g)]], dtype=complex),
        np.sqrt(q) * np.array([[0, np.sqrt(g)], [0, 0]], dtype=complex),
        np.sqrt(1 - q) * np.array([[np.sqrt(1 - g), 0], [0, 1]], dtype=complex),
        np.sqrt(1 - q) * np.array([[0, 0], [np.sqrt(g), 0]], dtype=complex),
    ]


def haar_unitary(rng: np.random.Generator, n: int) -> np.ndarray:
    z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = phases / np.abs(phases)
    return q @ np.diag(phases.conj())


def hermitian_from_vector(x: np.ndarray) -> np.ndarray:
    h = np.zeros((4, 4), dtype=complex)
    h[np.diag_indices(4)] = x[:4]
    cursor = 4
    for i in range(4):
        for j in range(i + 1, 4):
            h[i, j] = x[cursor] + 1j * x[cursor + 1]
            h[j, i] = h[i, j].conj()
            cursor += 2
    return h


def optimize_same_measurement(frame: list[np.ndarray], which: str, seed: int = 231) -> dict:
    """Haar screen plus local U(4) tangent optimization for an n=2 score."""
    rng = np.random.default_rng(seed)
    candidates = [np.eye(4, dtype=complex)] + [haar_unitary(rng, 4) for _ in range(320)]

    def score_u(u: np.ndarray) -> float:
        s = branch_scores(mix_kraus(frame, u), 2)
        return s.markov_trace if which == "markov" else s.final_only_trace

    screened = sorted(((score_u(u), u) for u in candidates), key=lambda z: z[0], reverse=True)
    best_score, best_u = screened[0]
    starts = screened[:4]
    reports = []
    for initial_score, u0 in starts:
        def objective(x: np.ndarray) -> float:
            u = expm(1j * hermitian_from_vector(x)) @ u0
            return -score_u(u)

        opt = minimize(objective, np.zeros(16), method="BFGS",
                       options={"gtol": 2e-10, "maxiter": 180, "disp": False})
        u_opt = expm(1j * hermitian_from_vector(opt.x)) @ u0
        val = score_u(u_opt)
        reports.append({"initial": initial_score, "final": val,
                        "success": bool(opt.success), "nit": int(opt.nit),
                        "grad_norm": float(np.linalg.norm(opt.jac)) if opt.jac is not None else None})
        if val > best_score:
            best_score, best_u = val, u_opt
    return {
        "score": float(best_score),
        "unitarity_residual": float(np.linalg.norm(best_u.conj().T @ best_u - np.eye(4))),
        "screen_best": float(screened[0][0]),
        "screen_second": float(screened[1][0]),
        "local_reports": reports,
        "unitary_real_imag_rows": [[[float(z.real), float(z.imag)] for z in row] for row in best_u],
    }


def main() -> None:
    print("REPRODUCTION_BASELINE_V1")
    print(f"runtime python={sys.version.split()[0]} numpy={np.__version__} scipy={scipy.__version__}")
    print("basis=(|0>,|1>); U_rows_mix_Kraus; history_order=K[xn]...K[x1]; Phi_normalized=true")

    max_input_residual = 0.0
    max_baseline_residual = 0.0
    for lam in (0.04, 0.36, 0.81):
        a = example8_direct(lam)
        b = example8_derived(lam)
        input_res = max(np.linalg.norm(x - y) for x, y in zip(a, b))
        max_input_residual = max(max_input_residual, input_res)
        print(f"INPUT_AB lambda={lam:.2f} max_row_fro_residual={input_res:.3e} "
              f"cptp_A={cptp_residual(a):.3e} cptp_B={cptp_residual(b):.3e}")
        for n in (1, 2, 3, 5):
            target = 0.5 + 0.5 * np.sqrt(1 - lam) ** n
            sa, sb = branch_scores(a, n), branch_scores(b, n)
            values = [sa.markov_trace, sa.markov_bell, sa.bayes_recursive_trace,
                      sa.bayes_recursive_bell, sa.final_only_trace, sa.final_only_bell,
                      sb.markov_trace, sb.final_only_trace]
            residual = max(abs(v - target) for v in values)
            max_baseline_residual = max(max_baseline_residual, residual)
            print(f"EXAMPLE8_EQ46 lambda={lam:.2f} n={n} target={target:.15f} "
                  f"M={sa.markov_trace:.15f} Brec={sa.bayes_recursive_trace:.15f} "
                  f"Bfinal={sa.final_only_trace:.15f} BellM={sa.markov_bell:.15f} "
                  f"max_residual={residual:.3e}")

    # Gregoratti--Werner Proposition 4: polar inverse reaches Eq. (18),
    # independently evaluated by the normalized Bell state.
    rng = np.random.default_rng(404)
    prop4_frame = mix_kraus(gad_frame(0.37, 0.61), haar_unitary(rng, 4))
    prop4_rhs = sum(float(np.trace(matrix_abs(k)).real) ** 2 for k in prop4_frame) / 4
    corrected = [polar_unitary(k).conj().T @ k for k in prop4_frame]
    prop4_bell = bell_fidelity(corrected)
    prop4_polar_res = max(np.linalg.norm(l - matrix_abs(k)) for l, k in zip(corrected, prop4_frame))
    print(f"GREGORATTI_PROP4 rhs_eq18={prop4_rhs:.15f} direct_bell={prop4_bell:.15f} "
          f"fidelity_residual={abs(prop4_rhs-prop4_bell):.3e} polar_branch_residual={prop4_polar_res:.3e}")
    max_baseline_residual = max(max_baseline_residual, abs(prop4_rhs - prop4_bell), prop4_polar_res)

    dep = depolarizing_frame(0.32)
    dep_s = branch_scores(dep, 2)
    dep_choi = choi_spectrum(dep)
    print(f"DEPOLARIZING p=0.32 cptp={cptp_residual(dep):.3e} "
          f"choi_min={dep_choi.min():.15f} choi_rank={np.count_nonzero(dep_choi>1e-12)} "
          f"M2={dep_s.markov_trace:.15f} B2={dep_s.final_only_trace:.15f} "
          f"direct_bell_residual={abs(dep_s.markov_trace-dep_s.markov_bell):.3e}")

    gad = gad_frame(0.37, 0.61)
    gad_s = branch_scores(gad, 2)
    gad_choi = choi_spectrum(gad)
    print(f"GAD_CANONICAL gamma=0.37 q=0.61 cptp={cptp_residual(gad):.3e} "
          f"choi_min={gad_choi.min():.15f} choi_rank={np.count_nonzero(gad_choi>1e-12)} "
          f"M2={gad_s.markov_trace:.15f} Brec2={gad_s.bayes_recursive_trace:.15f} "
          f"Bfinal2={gad_s.final_only_trace:.15f} "
          f"BellM_residual={abs(gad_s.markov_trace-gad_s.markov_bell):.3e} "
          f"Prop5_sum_residual={abs(gad_s.bayes_recursive_trace-gad_s.final_only_trace):.3e}")

    # Separate numerical optimizations are a bounded control, not a global certificate.
    opt_m = optimize_same_measurement(gad, "markov", seed=231)
    opt_b = optimize_same_measurement(gad, "bayes", seed=947)
    print("GAD_OPT_M2 " + json.dumps(opt_m, sort_keys=True, separators=(",", ":")))
    print("GAD_OPT_B2 " + json.dumps(opt_b, sort_keys=True, separators=(",", ":")))
    print(f"GAD_OPT_COMPARISON M2={opt_m['score']:.15f} B2={opt_b['score']:.15f} "
          f"BminusM={opt_b['score']-opt_m['score']:.3e} "
          "scope=independent_Haar_plus_local_numerical_not_global_certificate")

    # Exhibit why physical n=3 Markovian fidelity must use |tr L|^2.
    u_complex = haar_unitary(np.random.default_rng(903), 4)
    complex_s = branch_scores(mix_kraus(gad, u_complex), 3)
    print(f"COMPLEX_TRACE_CONTROL max_abs_imag_trace={complex_s.max_markov_trace_imag:.3e} "
          f"M_trace={complex_s.markov_trace:.15f} M_Bell={complex_s.markov_bell:.15f} "
          f"M_residual={abs(complex_s.markov_trace-complex_s.markov_bell):.3e} "
          f"Brec={complex_s.bayes_recursive_trace:.15f} "
          f"Bfinal={complex_s.final_only_trace:.15f} "
          f"Prop5_sum_residual={abs(complex_s.bayes_recursive_trace-complex_s.final_only_trace):.3e} "
          f"Brec_Bell_residual={abs(complex_s.bayes_recursive_trace-complex_s.bayes_recursive_bell):.3e} "
          f"Bfinal_Bell_residual={abs(complex_s.final_only_trace-complex_s.final_only_bell):.3e}")

    print(f"SUMMARY max_input_AB_residual={max_input_residual:.3e} "
          f"max_published_baseline_residual={max_baseline_residual:.3e}")
    if max_input_residual > 5e-13 or max_baseline_residual > 2e-11:
        raise SystemExit("FAIL: reconstruction or published baseline tolerance exceeded")
    if cptp_residual(gad) > 2e-13 or gad_choi.min() <= 1e-10:
        raise SystemExit("FAIL: GAD control is not strictly full Choi rank CPTP")
    print("STATUS PASS")


if __name__ == "__main__":
    main()
