#!/usr/bin/env python3
"""Independent representation and published-baseline checks for phys-00018-p01.

This script writes nothing.  Its stdout is captured verbatim in the evidence log by
the reproduce worker.  Representation A is the magnetic-sublattice Bloch matrix;
representation B is independently assembled in the three momentum-harmonic basis.
"""

from __future__ import annotations

import platform

import numpy as np
import scipy
import sympy as sp


PI = np.pi


def h_sublattice(theta: float, kappa: float, r: float, m: float) -> np.ndarray:
    """A: basis s=(-1,0,+1), cell convention psi_(3n+s)=e^(i*kappa*n)u_s."""
    return np.array(
        [
            [m - 2 * r * np.cos(theta - 2 * PI / 3), -1, -np.exp(-1j * kappa)],
            [-1, -2 * r * np.cos(theta), -1],
            [-np.exp(1j * kappa), -1, -m - 2 * r * np.cos(theta + 2 * PI / 3)],
        ],
        dtype=complex,
    )


def h_harmonic(theta: float, kappa: float, r: float, m: float) -> np.ndarray:
    """B: independently assembled basis q_l=kappa/3+2*pi*l/3, l=0,1,2."""
    kx = kappa / 3
    out = np.zeros((3, 3), dtype=complex)
    for ell in range(3):
        out[ell, ell] = -2 * np.cos(kx + 2 * PI * ell / 3)
        out[ell, (ell + 1) % 3] += -r * np.exp(-1j * theta) - 1j * m / np.sqrt(3)
        out[ell, (ell - 1) % 3] += -r * np.exp(1j * theta) + 1j * m / np.sqrt(3)
    return out


def harmonic_to_sublattice(kappa: float) -> np.ndarray:
    """u_s=sum_l F_(s,l)c_l for s=(-1,0,+1)."""
    s = np.array([-1, 0, 1], dtype=float)
    q = kappa / 3 + 2 * PI * np.arange(3) / 3
    return np.exp(1j * np.outer(s, q)) / np.sqrt(3)


def fhs_chern_source_convention(n_grid: int) -> np.ndarray:
    """Link-variable Chern numbers; sign converted to A=i<u|du> convention."""
    vec = np.empty((n_grid, n_grid, 3, 3), dtype=complex)
    for i, kappa in enumerate(np.linspace(-PI, PI, n_grid, endpoint=False)):
        for j, theta in enumerate(np.linspace(-PI, PI, n_grid, endpoint=False)):
            _, vec[i, j] = np.linalg.eigh(h_sublattice(theta, kappa, 1.0, 0.0))
    raw = np.zeros(3)
    min_overlap = np.full(3, np.inf)
    for band in range(3):
        for i in range(n_grid):
            ip = (i + 1) % n_grid
            for j in range(n_grid):
                jp = (j + 1) % n_grid
                ux = np.vdot(vec[i, j, :, band], vec[ip, j, :, band])
                uy_x = np.vdot(vec[ip, j, :, band], vec[ip, jp, :, band])
                ux_y = np.vdot(vec[i, jp, :, band], vec[ip, jp, :, band])
                uy = np.vdot(vec[i, j, :, band], vec[i, jp, :, band])
                min_overlap[band] = min(
                    min_overlap[band], abs(ux), abs(uy_x), abs(ux_y), abs(uy)
                )
                ux /= abs(ux)
                uy_x /= abs(uy_x)
                ux_y /= abs(ux_y)
                uy /= abs(uy)
                raw[band] += np.angle(ux * uy_x / (ux_y * uy))
    # With links <u(k)|u(k+dk)>, the plaquette phase is minus the curvature for
    # the source's Berry connection A=i<u|du>.  Hence the explicit minus sign.
    return -raw / (2 * PI), min_overlap


def kubo_chern(n_grid: int) -> np.ndarray:
    """Independent gauge-invariant curvature quadrature on midpoint grid."""
    total = np.zeros(3)
    step = 2 * PI / n_grid
    for i in range(n_grid):
        kappa = -PI + (i + 0.5) * step
        for j in range(n_grid):
            theta = -PI + (j + 0.5) * step
            ham = h_sublattice(theta, kappa, 1.0, 0.0)
            energy, vec = np.linalg.eigh(ham)
            d_kappa = np.zeros((3, 3), dtype=complex)
            d_kappa[0, 2] = 1j * np.exp(-1j * kappa)
            d_kappa[2, 0] = -1j * np.exp(1j * kappa)
            d_theta = np.diag(
                [
                    2 * np.sin(theta - 2 * PI / 3),
                    2 * np.sin(theta),
                    2 * np.sin(theta + 2 * PI / 3),
                ]
            ).astype(complex)
            for band in range(3):
                z = 0j
                for other in range(3):
                    if other == band:
                        continue
                    z += (
                        (vec[:, band].conj() @ d_kappa @ vec[:, other])
                        * (vec[:, other].conj() @ d_theta @ vec[:, band])
                        / (energy[band] - energy[other]) ** 2
                    )
                # Omega_(kappa,theta) for A=i<u|du> is -2 Im(z).
                total[band] += -2 * np.imag(z)
    return total * step**2 / (2 * PI)


def symbolic_checks() -> None:
    E, r, m, theta, kappa = sp.symbols("E r m theta kappa", real=True)
    d_minus = m - 2 * r * sp.cos(theta - 2 * sp.pi / 3)
    d_zero = -2 * r * sp.cos(theta)
    d_plus = -m - 2 * r * sp.cos(theta + 2 * sp.pi / 3)
    ham = sp.Matrix(
        [
            [d_minus, -1, -sp.exp(-sp.I * kappa)],
            [-1, d_zero, -1],
            [-sp.exp(sp.I * kappa), -1, d_plus],
        ]
    )
    a_formula = m**2 + 3 * r**2 + 3 - 2 * sp.sqrt(3) * m * r * sp.sin(theta)
    det_formula = (
        2 * m**2 * r * sp.cos(theta)
        - 2 * sp.sqrt(3) * m * r**2 * sp.sin(2 * theta)
        - 2 * r**3 * sp.cos(3 * theta)
        - 2 * sp.cos(kappa)
    )
    trace_residual = sp.trigsimp(sp.trace(ham))
    a_residual = sp.trigsimp(sp.expand_trig(sp.trace(ham * ham) / 2 - a_formula), method="fu")
    det_residual = sp.simplify(sp.expand_complex(sp.expand_trig(ham.det() - det_formula)))
    char_residual = sp.simplify(
        sp.expand_complex(
            sp.expand_trig(
                (E * sp.eye(3) - ham).det() - (E**3 - a_formula * E - det_formula)
            )
        )
    )
    assert trace_residual == 0
    assert a_residual == 0
    assert det_residual == 0
    assert char_residual == 0
    print("SYMBOLIC trace=0: PASS")
    print("SYMBOLIC tr(H^2)/2=A: PASS")
    print("SYMBOLIC det(H)=D: PASS")
    print("SYMBOLIC det(EI-H)=E^3-A*E-D: PASS")
    print("A = m^2 + 3 r^2 + 3 - 2 sqrt(3) m r sin(theta)")
    print(
        "D = 2 m^2 r cos(theta) - 2 sqrt(3) m r^2 sin(2 theta) "
        "- 2 r^3 cos(3 theta) - 2 cos(kappa)"
    )


def main() -> None:
    print("JOB phys-00018-p01-reproduce-89a4399f0c1c")
    print("Python", platform.python_version())
    print("NumPy", np.__version__)
    print("SciPy", scipy.__version__)
    print("SymPy", sp.__version__)
    print()

    cases = [
        (0.0, 0.0, 1.0, 0.0),
        (0.3, -2.1, 0.7, 0.8),
        (-1.2, 2.9, 2.0, -3.0),
        (PI / 2, PI, 0.5, np.sqrt(3) / 2),
    ]
    worst_map = 0.0
    worst_spectrum = 0.0
    for theta, kappa, r, m in cases:
        ha = h_sublattice(theta, kappa, r, m)
        hb = h_harmonic(theta, kappa, r, m)
        f = harmonic_to_sublattice(kappa)
        map_error = np.max(np.abs(ha - f @ hb @ f.conj().T))
        spectrum_error = np.max(np.abs(np.linalg.eigvalsh(ha) - np.linalg.eigvalsh(hb)))
        herm_a = np.max(np.abs(ha - ha.conj().T))
        herm_b = np.max(np.abs(hb - hb.conj().T))
        unitary = np.max(np.abs(f.conj().T @ f - np.eye(3)))
        worst_map = max(worst_map, map_error)
        worst_spectrum = max(worst_spectrum, spectrum_error)
        print(
            "MAP case theta={:.16g} kappa={:.16g} r={:.16g} m={:.16g} "
            "entry_err={:.3e} spectrum_err={:.3e} hermA={:.3e} hermB={:.3e} "
            "unitary_err={:.3e}".format(
                theta, kappa, r, m, map_error, spectrum_error, herm_a, herm_b, unitary
            )
        )
    assert worst_map < 5e-14 and worst_spectrum < 5e-14
    print("A/B explicit-unitary comparison: PASS")
    print()

    symbolic_checks()
    print()

    print("UNDEFORMED r=1,m=0 characteristic: E^3-6E+2(cos(3theta)+cos(kappa))")
    print("Exact band ranges:")
    print("  E1 in [-1-sqrt(3), -2]")
    print("  E2 in [1-sqrt(3), sqrt(3)-1]")
    print("  E3 in [2, 1+sqrt(3)]")
    print("Exact direct gaps d1=d2=3-sqrt(3)")
    for theta, kappa in [(0.0, 0.0), (0.0, PI), (PI / 3, 0.0)]:
        vals = np.linalg.eigvalsh(h_sublattice(theta, kappa, 1.0, 0.0))
        print(
            "SPECTRUM theta={:.16g} kappa={:.16g}: [{:.15g}, {:.15g}, {:.15g}]".format(
                theta, kappa, *vals
            )
        )
    print()

    for n_grid in (11, 21, 41, 81):
        c, overlaps = fhs_chern_source_convention(n_grid)
        print(
            "FHS N={}: C=[{:.15g}, {:.15g}, {:.15g}] min_link_overlap=[{:.6g}, {:.6g}, {:.6g}]".format(
                n_grid, *c, *overlaps
            )
        )
        assert np.max(np.abs(c - np.array([1.0, -2.0, 1.0]))) < 1e-10
    for n_grid in (12, 24, 48, 96):
        c = kubo_chern(n_grid)
        print("KUBO N={}: C=[{:.15g}, {:.15g}, {:.15g}]".format(n_grid, *c))
    c96 = kubo_chern(96)
    assert np.max(np.abs(c96 - np.array([1.0, -2.0, 1.0]))) < 1e-10
    print("Published Chern tuple (+1,-2,+1), two algorithms: PASS")
    print()

    # Exact direct-closure construction.  At m=sigma*sqrt(3)r and
    # theta=sigma*pi/2 all three diagonal entries vanish.  The resulting ring
    # has eigenvalues (-2,1,1) at kappa=0 and (-1,-1,2) at kappa=pi.
    for r in (0.5, 1.0, 2.0):
        for sigma in (-1.0, 1.0):
            theta = sigma * PI / 2
            m = sigma * np.sqrt(3) * r
            diag_error = np.max(np.abs(np.diag(h_sublattice(theta, 0.0, r, m))))
            at_zero = np.linalg.eigvalsh(h_sublattice(theta, 0.0, r, m))
            at_pi = np.linalg.eigvalsh(h_sublattice(theta, PI, r, m))
            print(
                "DIRECT r={:.1f} sigma={:+.0f}: diag_err={:.3e} "
                "kappa0=[{:.12g},{:.12g},{:.12g}] kappapi=[{:.12g},{:.12g},{:.12g}]".format(
                    r, sigma, diag_error, *at_zero, *at_pi
                )
            )
            assert diag_error < 2e-15
            assert np.max(np.abs(at_zero - np.array([-2.0, 1.0, 1.0]))) < 2e-14
            assert np.max(np.abs(at_pi - np.array([-1.0, -1.0, 2.0]))) < 2e-14
    print("Direct closures m=+/-sqrt(3)r at theta=sign(m)*pi/2, kappa=0,pi: PASS")
    print("Completeness lemma: a double eigenvalue makes H-lambda I rank one.")
    print("Because all three off-diagonal magnitudes equal one, its three diagonal entries")
    print("are equal; tracelessness forces d_- = d_0 = d_+ = 0.  Solving gives")
    print("theta=+/-pi/2 and m=+/-sqrt(3)r with matching signs; the zero-diagonal")
    print("ring discriminant then vanishes only for sin(kappa)=0.")
    print("ALL REPRODUCTION CHECKS: PASS")


if __name__ == "__main__":
    main()
