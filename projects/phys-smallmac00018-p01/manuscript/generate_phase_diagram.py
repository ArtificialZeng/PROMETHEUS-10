#!/usr/bin/env python3
"""Generate the phase-boundary data and deterministic manuscript figure.

The plotted curves are evaluations of the accepted exact parametrization.  The
floating-point samples are for visualization only; the proof uses rational/Sturm
arithmetic in the frozen certificate scripts.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path

import numpy as np
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "build" / "mplconfig"))
import matplotlib.pyplot as plt  # noqa: E402


SQRT3 = np.sqrt(3.0)
XC = (7.0 + np.sqrt(33.0)) / 16.0
RC = np.sqrt((69.0 - 11.0 * np.sqrt(33.0)) / 8.0)


def boundary_point(x_value: float) -> tuple[float, ...]:
    """Return (V,u,e,r,m,E,theta_c,theta_v) on the physical branch."""
    x = float(x_value)
    v_squared = (
        3.0 * (2.0 * x - 1.0) ** 2 * (8.0 * x**2 - 4.0 * x - 1.0)
        / (4.0 * (40.0 * x**3 - 36.0 * x**2 + 6.0 * x - 1.0))
    )
    root_x = np.sqrt(x)
    root_one_minus_x = np.sqrt(1.0 - x)
    root_v = np.sqrt(v_squared)
    t_value = 4.0 * root_x * root_v / (2.0 * x - 1.0)
    u_value = (
        4.0 * root_v * root_one_minus_x * (4.0 * x - 1.0)
        / (3.0 * (2.0 * x - 1.0))
    )
    e_value = (
        2.0
        * root_x
        * ((2.0 * x - 1.0) * (1.0 - x) + (2.0 * x + 1.0) * v_squared)
        / (root_v * (4.0 * x - 1.0))
    )
    h_value = (
        2.0 * (1.0 + 2.0 * v_squared) * t_value
        - 8.0 * np.sqrt(x * v_squared) * (4.0 * x - 3.0)
    )
    k_value = h_value + e_value**3 - 3.0 * e_value * (1.0 + u_value**2)
    roots = np.roots([k_value, 0.0, -3.0 * e_value, 2.0])
    positive = sorted(
        float(root.real)
        for root in roots
        if abs(root.imag) < 2.0e-6 and root.real > 0.0
    )
    if len(positive) != 2:
        raise RuntimeError(f"Expected two positive roots at X={x:.16g}: {roots}")
    r_value = positive[-1]
    energy = e_value * r_value
    phi = -np.arccos(root_x)
    delta = np.arccos(-root_v)
    theta_c = phi + delta
    theta_v = phi - delta
    return (
        v_squared,
        u_value,
        e_value,
        r_value,
        SQRT3 * u_value * r_value,
        energy,
        theta_c,
        theta_v,
    )


def x_at_r_two(left_branch: bool) -> float:
    if left_branch:
        bracket = (0.750000001, XC - 1.0e-6)
    else:
        bracket = (XC + 1.0e-6, 0.999999999)
    return brentq(
        lambda x: boundary_point(x)[3] - 2.0,
        *bracket,
        xtol=5.0e-15,
        rtol=5.0e-15,
    )


def sampled_branch(left_branch: bool, count: int = 320) -> list[tuple[float, ...]]:
    edge = x_at_r_two(left_branch)
    if left_branch:
        x_values = np.linspace(edge, XC - 2.0e-6, count)
    else:
        x_values = np.linspace(XC + 2.0e-6, edge, count)
    rows = [boundary_point(float(x)) + (float(x),) for x in x_values]
    rows.sort(key=lambda row: row[3])
    return rows


def write_data(lower_mass: list[tuple[float, ...]], upper_mass: list[tuple[float, ...]]) -> None:
    output = ROOT / "data" / "phase_boundary.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["branch", "X", "V", "u", "e", "r", "m", "E", "theta_c", "theta_v"]
        )
        writer.writerow(
            ["cusp", XC, (9.0 - np.sqrt(33.0)) / 16.0, 1.0, 1.0 / RC,
             RC, SQRT3 * RC, 1.0, np.nan, np.nan]
        )
        for name, rows in (("m_minus", lower_mass), ("m_plus", upper_mass)):
            for v_squared, u_value, e_value, r_value, mass, energy, tc, tv, x in rows:
                writer.writerow(
                    [name, x, v_squared, u_value, e_value, r_value, mass, energy, tc, tv]
                )


def plot(lower_mass: list[tuple[float, ...]], upper_mass: list[tuple[float, ...]]) -> None:
    lower_r = np.array([row[3] for row in lower_mass])
    lower_m = np.array([row[4] for row in lower_mass])
    upper_r = np.array([row[3] for row in upper_mass])
    upper_m = np.array([row[4] for row in upper_mass])
    common_r = np.linspace(RC, 2.0, 600)
    m_minus = np.interp(common_r, lower_r, lower_m)
    m_plus = np.interp(common_r, upper_r, upper_m)

    fig, ax = plt.subplots(figsize=(7.15, 4.65), constrained_layout=True)
    metal_color = "#E69F00"
    boundary_color = "#0072B2"
    direct_color = "#4D4D4D"
    ax.fill_between(common_r, m_minus, m_plus, color=metal_color, alpha=0.24)
    ax.fill_between(common_r, -m_plus, -m_minus, color=metal_color, alpha=0.24,
                    label="indirect band overlap ($G<0$)")

    direct_r = np.linspace(0.5, 2.0, 500)
    ax.plot(direct_r, SQRT3 * direct_r, ls="--", lw=1.25, color=direct_color,
            label=r"direct closure $|m|=\sqrt{3}r$")
    ax.plot(direct_r, -SQRT3 * direct_r, ls="--", lw=1.25, color=direct_color)
    direct_boundary_r = np.linspace(0.5, RC, 180)
    ax.plot(direct_boundary_r, SQRT3 * direct_boundary_r, lw=2.15,
            color=boundary_color)
    ax.plot(direct_boundary_r, -SQRT3 * direct_boundary_r, lw=2.15,
            color=boundary_color)
    ax.plot(lower_r, lower_m, lw=2.15, color=boundary_color)
    ax.plot(upper_r, upper_m, lw=2.15, color=boundary_color,
            label=r"global insulating boundary $G=0$")
    ax.plot(lower_r, -lower_m, lw=2.15, color=boundary_color)
    ax.plot(upper_r, -upper_m, lw=2.15, color=boundary_color)
    ax.scatter([RC, RC], [SQRT3 * RC, -SQRT3 * RC], s=30,
               color="#D55E00", zorder=4, label=r"cusps $r=r_c$")

    ax.text(1.55, 0.16, r"insulator: $(+1,-2,+1)$", ha="center", fontsize=9)
    ax.text(1.53, 5.45, r"insulator: $(0,0,0)$", ha="center", fontsize=9)
    ax.text(1.53, -5.78, r"insulator: $(0,0,0)$", ha="center", fontsize=9)
    ax.text(1.63, 2.9, "metal", rotation=18, color="#8C5200", fontsize=9)
    ax.text(1.63, -3.35, "metal", rotation=-18, color="#8C5200", fontsize=9)
    ax.annotate(
        rf"$r_c={RC:.6f}$",
        xy=(RC, SQRT3 * RC), xytext=(0.61, 3.15),
        arrowprops={"arrowstyle": "->", "lw": 0.9}, fontsize=9,
    )
    ax.set_xlim(0.5, 2.0)
    ax.set_ylim(-7.55, 7.55)
    ax.set_xlabel(r"anisotropy $r=t_y/t_x$")
    ax.set_ylabel(r"period-three mass $m/t_x$")
    ax.grid(True, color="0.88", lw=0.65)
    ax.legend(loc="upper left", frameon=True, fontsize=8)
    fig.savefig(ROOT / "figures" / "phase_diagram.pdf")
    fig.savefig(ROOT / "figures" / "phase_diagram.png", dpi=220)
    plt.close(fig)


def main() -> None:
    lower_mass = sampled_branch(left_branch=False)
    upper_mass = sampled_branch(left_branch=True)
    write_data(lower_mass, upper_mass)
    plot(lower_mass, upper_mass)

    checks = {
        0.90: (1.491168750337, 1.732042744620),
        1.00: (1.522145273973, 2.269195105327),
        1.50: (1.646066824501, 4.789938828072),
        2.00: (1.721949718751, 7.074701110742),
    }
    for target_r, expected in checks.items():
        values = []
        for left in (False, True):
            if abs(target_r - 2.0) < 1.0e-12:
                x = x_at_r_two(left)
            else:
                if left:
                    bracket = (0.750000001, XC - 1.0e-6)
                else:
                    bracket = (XC + 1.0e-6, 0.999999999)
                x = brentq(lambda xx: boundary_point(xx)[3] - target_r, *bracket)
            values.append(boundary_point(x)[4])
        if max(abs(values[i] - expected[i]) for i in range(2)) > 8.0e-10:
            raise AssertionError((target_r, values, expected))
        print(f"r={target_r:.2f}: m_minus={values[0]:.12f}, m_plus={values[1]:.12f}")
    print(f"cusp: r_c={RC:.15f}, m_c={SQRT3 * RC:.15f}")
    print("phase-boundary figure/data checks: PASS")


if __name__ == "__main__":
    main()
