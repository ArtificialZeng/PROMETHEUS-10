#!/usr/bin/env python3
"""Search and independently verify phase-bound margins for symmetric complete K3.

The discovery solver integrates the full 3x3 fundamental matrix over one period and
extracts its normalized Floquet fixed point.  The checker eliminates p3 and solves the
resulting two-coordinate periodic ODE by global Fourier collocation.  The two paths
share only the frozen rate law and analytic drive; neither consumes the other's state.

This script writes no files.  Preserve stdout as the computation log.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
import sys
from dataclasses import dataclass

import numpy as np
import scipy
from scipy.integrate import simpson, solve_ivp


@dataclass(frozen=True)
class Drive:
    offset: np.ndarray       # (3,)
    sin_coeff: np.ndarray    # (M,3)
    cos_coeff: np.ndarray    # (M,3)
    omega: float
    k0: float = 1.0

    def values(self, t: float | np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        tt = np.asarray(t, dtype=float)
        scalar = tt.ndim == 0
        tt = np.atleast_1d(tt)
        m = np.arange(1, self.sin_coeff.shape[0] + 1, dtype=float)[:, None]
        phase = m * self.omega * tt[None, :]
        sinp = np.sin(phase)
        cosp = np.cos(phase)
        e = self.offset[:, None] + self.sin_coeff.T @ sinp + self.cos_coeff.T @ cosp
        edot = self.sin_coeff.T @ (m * self.omega * cosp) - self.cos_coeff.T @ (m * self.omega * sinp)
        eddot = -self.sin_coeff.T @ ((m * self.omega) ** 2 * sinp) - self.cos_coeff.T @ ((m * self.omega) ** 2 * cosp)
        if scalar:
            return e[:, 0], edot[:, 0], eddot[:, 0]
        return e.T, edot.T, eddot.T

    def record(self) -> dict[str, object]:
        return {
            "k0": self.k0,
            "omega": self.omega,
            "offset": self.offset.tolist(),
            "sin_coeff": self.sin_coeff.tolist(),
            "cos_coeff": self.cos_coeff.tolist(),
        }


def generator(e: np.ndarray, k0: float) -> np.ndarray:
    """Column generator for departure rates k_ij=k0 exp[(E_i-E_j)/2]."""
    ratio = np.exp((e[:, None] - e[None, :]) / 2.0)
    rates = k0 * ratio
    np.fill_diagonal(rates, 0.0)
    out = rates.T.copy()
    np.fill_diagonal(out, -np.sum(rates, axis=1))
    return out


def _observables(t: np.ndarray, p: np.ndarray, drive: Drive, quadrature: str) -> tuple[float, float]:
    _, edot, eddot = drive.values(t)
    wb = np.sum(p * edot, axis=1)
    wa = np.sum(p * eddot, axis=1)
    if quadrature == "simpson":
        period = 2.0 * math.pi / drive.omega
        return float(simpson(wa, x=t) / period), float(simpson(wb, x=t) / period)
    if quadrature == "periodic_mean":
        return float(np.mean(wa)), float(np.mean(wb))
    raise ValueError(quadrature)


def propagator_solution(
    drive: Drive,
    *,
    rtol: float = 2e-11,
    atol: float = 2e-13,
    nodes: int = 4097,
) -> dict[str, float | list[float]]:
    """Full 3-coordinate fundamental-matrix/Floquet solution."""
    period = 2.0 * math.pi / drive.omega

    def fundamental_rhs(t: float, flat: np.ndarray) -> np.ndarray:
        e, _, _ = drive.values(t)
        return (generator(e, drive.k0) @ flat.reshape(3, 3)).ravel()

    common = {"method": "DOP853", "rtol": rtol, "atol": atol}
    fund = solve_ivp(fundamental_rhs, (0.0, period), np.eye(3).ravel(), **common)
    if not fund.success:
        raise RuntimeError(fund.message)
    phi = fund.y[:, -1].reshape(3, 3)
    lhs = np.vstack((phi - np.eye(3), np.ones((1, 3))))
    rhs = np.array([0.0, 0.0, 0.0, 1.0])
    p0, *_ = np.linalg.lstsq(lhs, rhs, rcond=None)

    def state_rhs(t: float, p: np.ndarray) -> np.ndarray:
        e, _, _ = drive.values(t)
        return generator(e, drive.k0) @ p

    t = np.linspace(0.0, period, nodes)
    sol = solve_ivp(state_rhs, (0.0, period), p0, t_eval=t, **common)
    if not sol.success:
        raise RuntimeError(sol.message)
    p = sol.y.T
    a, b = _observables(t, p, drive, "simpson")
    return {
        "A": a,
        "B": b,
        "A_minus_k0B": a - drive.k0 * b,
        "A_minus_2k0B": a - 2.0 * drive.k0 * b,
        "A_over_k0B": a / (drive.k0 * b) if b != 0.0 else math.nan,
        "phase": math.atan2(drive.omega * b, a),
        "periodic_residual_inf": float(np.max(np.abs(phi @ p0 - p0))),
        "normalization_residual_inf": float(np.max(np.abs(np.sum(p, axis=1) - 1.0))),
        "min_probability": float(np.min(p)),
        "p0": p0.tolist(),
        "fundamental_nfev": float(fund.nfev),
        "state_nfev": float(sol.nfev),
    }


def fourier_derivative_matrix(n: int, omega: float) -> np.ndarray:
    """Real Fourier collocation derivative on x_j=2*pi*j/n, d/dt=omega*d/dx."""
    eye = np.eye(n)
    modes = np.fft.fftfreq(n, d=1.0 / n)
    deriv = np.fft.ifft(1j * modes[:, None] * np.fft.fft(eye, axis=0), axis=0)
    return omega * np.real_if_close(deriv, tol=1000).real


def collocation_solution(drive: Drive, *, nodes: int = 192) -> dict[str, float | list[float]]:
    """Independent two-coordinate Fourier-collocation periodic solution."""
    period = 2.0 * math.pi / drive.omega
    t = period * np.arange(nodes, dtype=float) / nodes
    e, _, _ = drive.values(t)
    mats = np.asarray([generator(row, drive.k0) for row in e])
    # With p3=1-p1-p2, ydot=M(t)y+b(t).
    m = mats[:, :2, :2] - mats[:, :2, 2][:, :, None]
    forcing = mats[:, :2, 2]
    dmat = fourier_derivative_matrix(nodes, drive.omega)
    block = np.block(
        [
            [dmat - np.diag(m[:, 0, 0]), -np.diag(m[:, 0, 1])],
            [-np.diag(m[:, 1, 0]), dmat - np.diag(m[:, 1, 1])],
        ]
    )
    rhs = np.concatenate((forcing[:, 0], forcing[:, 1]))
    answer = np.linalg.solve(block, rhs)
    p = np.column_stack((answer[:nodes], answer[nodes:]))
    p = np.column_stack((p, 1.0 - np.sum(p, axis=1)))
    a, b = _observables(t, p, drive, "periodic_mean")
    residual = block @ answer - rhs
    return {
        "A": a,
        "B": b,
        "A_minus_k0B": a - drive.k0 * b,
        "A_minus_2k0B": a - 2.0 * drive.k0 * b,
        "A_over_k0B": a / (drive.k0 * b) if b != 0.0 else math.nan,
        "phase": math.atan2(drive.omega * b, a),
        "collocation_residual_inf": float(np.max(np.abs(residual))),
        "normalization_residual_inf": float(np.max(np.abs(np.sum(p, axis=1) - 1.0))),
        "min_probability": float(np.min(p)),
        "p0": p[0].tolist(),
    }


def gauge_fix(array: np.ndarray) -> np.ndarray:
    return array - np.mean(array, axis=-1, keepdims=True)


def random_drive(rng: np.random.Generator, harmonics: int, scale: float, offset_scale: float) -> Drive:
    offset = gauge_fix(rng.normal(0.0, offset_scale, size=(1, 3)))[0]
    sins = gauge_fix(rng.normal(0.0, scale, size=(harmonics, 3)))
    coses = gauge_fix(rng.normal(0.0, scale, size=(harmonics, 3)))
    # Log-uniform frequency range, in units k0=1.
    omega = float(10.0 ** rng.uniform(-1.0, 1.0))
    return Drive(offset, sins, coses, omega, 1.0)


def coarse_result(drive: Drive) -> dict[str, float | list[float]]:
    return propagator_solution(drive, rtol=3e-9, atol=3e-11, nodes=513)


def scan(seed: int, single: int, multi: int) -> list[tuple[float, Drive, dict[str, float | list[float]]]]:
    rng = np.random.default_rng(seed)
    accepted: list[tuple[float, Drive, dict[str, float | list[float]]]] = []
    total = single + multi
    for idx in range(total):
        h = 1 if idx < single else int(rng.integers(2, 4))
        scale = float(10.0 ** rng.uniform(-1.0, 0.65))
        offset_scale = float(rng.uniform(0.0, 4.0))
        drive = random_drive(rng, h, scale, offset_scale)
        try:
            result = coarse_result(drive)
        except (FloatingPointError, RuntimeError, ValueError, np.linalg.LinAlgError):
            continue
        a = float(result["A"])
        b = float(result["B"])
        if a > 1e-9 and b > 1e-9 and float(result["min_probability"]) > -1e-7:
            ratio = float(result["A_over_k0B"])
            accepted.append((ratio, drive, result))
    accepted.sort(key=lambda item: item[0])
    return accepted


def convergence_report(label: str, drive: Drive) -> None:
    print(f"CASE {label}")
    print("DRIVE " + json.dumps(drive.record(), sort_keys=True, separators=(",", ":")))
    for rtol, atol, nodes in [(2e-9, 2e-11, 1025), (2e-11, 2e-13, 4097), (2e-13, 2e-15, 8193)]:
        result = propagator_solution(drive, rtol=rtol, atol=atol, nodes=nodes)
        print(
            "PROPAGATOR "
            + json.dumps(
                {"rtol": rtol, "atol": atol, "nodes": nodes, **result},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    for nodes in [48, 96, 192, 384]:
        result = collocation_solution(drive, nodes=nodes)
        print(
            "COLLOCATION "
            + json.dumps({"nodes": nodes, **result}, sort_keys=True, separators=(",", ":"))
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1403)
    parser.add_argument("--single", type=int, default=60)
    parser.add_argument("--multi", type=int, default=120)
    parser.add_argument("--scan-only", action="store_true")
    parser.add_argument("--verify-drive", type=str)
    args = parser.parse_args()
    print("ENV " + json.dumps({
        "executable": sys.executable,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }, sort_keys=True, separators=(",", ":")))
    print("MODEL complete_K3; k_ij=k0*exp((E_i-E_j)/2); p_column; finite_Fourier_drive")
    print("SOLVER_A full_3x3_fundamental_matrix_DOP853_plus_Simpson")
    print("SOLVER_B eliminate_p3_two_coordinate_global_Fourier_collocation_plus_periodic_trapezoid")
    if args.verify_drive:
        with open(args.verify_drive, encoding="utf-8") as handle:
            rec = json.load(handle)
        drive = Drive(
            np.asarray(rec["offset"], dtype=float),
            np.asarray(rec["sin_coeff"], dtype=float),
            np.asarray(rec["cos_coeff"], dtype=float),
            float(rec["omega"]),
            float(rec["k0"]),
        )
        convergence_report("provided_drive", drive)
        return
    found = scan(args.seed, args.single, args.multi)
    print(f"SCAN seed={args.seed} requested_single={args.single} requested_multi={args.multi} admissible={len(found)}")
    if not found:
        raise RuntimeError("no admissible cases")
    for rank, (ratio, drive, result) in enumerate(found[:10], start=1):
        print("SCAN_BEST " + json.dumps({
            "rank": rank,
            "ratio": ratio,
            "drive": drive.record(),
            "coarse": result,
        }, sort_keys=True, separators=(",", ":")))
    # Verify the lowest frozen-bound ratio and, separately, the first clear violation
    # of the neighboring A-2k0B inequality (normally the same case).
    if not args.scan_only:
        convergence_report("minimum_ratio_from_scan", found[0][1])
        stronger = next((item for item in found if item[0] < 1.95), None)
        if stronger is not None and stronger[1].record() != found[0][1].record():
            convergence_report("neighboring_stronger_bound_witness", stronger[1])
    print("SUMMARY " + json.dumps({
        "minimum_scanned_A_over_k0B": found[0][0],
        "frozen_negative_found_coarse": any(item[0] < 1.0 for item in found),
        "neighboring_A_minus_2k0B_negative_found_coarse": any(item[0] < 2.0 for item in found),
        "scope": "finite deterministic random scan; absence is not proof",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
