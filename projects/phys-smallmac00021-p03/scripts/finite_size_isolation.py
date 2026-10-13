#!/usr/bin/env python3
"""Symmetry-resolved finite-size test near the Fig. 3 corner/edge merger."""

from __future__ import annotations

import argparse
import json
from collections import deque
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq, least_squares, minimize_scalar


Site = tuple[str, int, int]
Edge = tuple[Site, Site]


def site(i: int, j: int, sublattice: str) -> Site:
    return sublattice, i, j


def edge(x: Site, y: Site) -> Edge:
    return tuple(sorted((x, y)))


def rotate(x: Site, n: int) -> Site:
    sublattice, i, j = x
    return {"A": "B", "B": "C", "C": "A"}[sublattice], n - 1 - i - j, i


def reflect(x: Site) -> Site:
    sublattice, i, j = x
    return {"A": "A", "B": "C", "C": "B"}[sublattice], j, i


LOCAL_TARGETS: tuple[tuple[Site, Site, Fraction], ...] = (
    (site(0, 0, "A"), site(0, 0, "B"), Fraction(1)),
    (site(0, 0, "A"), site(0, 0, "C"), Fraction(1)),
    (site(0, 0, "B"), site(0, 0, "C"), Fraction(1)),
    (site(1, 0, "A"), site(1, 0, "B"), Fraction(1)),
    (site(0, 1, "A"), site(0, 1, "C"), Fraction(1)),
    (site(2, 0, "A"), site(2, 0, "C"), Fraction(1)),
    (site(0, 2, "A"), site(0, 2, "B"), Fraction(1)),
    (site(0, 0, "B"), site(1, 0, "A"), Fraction(1, 10)),
    (site(0, 0, "C"), site(0, 1, "A"), Fraction(1, 10)),
    (site(1, 0, "B"), site(2, 0, "A"), Fraction(1, 10)),
    (site(0, 1, "C"), site(0, 2, "A"), Fraction(1, 10)),
    (site(2, 0, "C"), site(2, 1, "A"), Fraction(1, 10)),
    (site(2, 0, "C"), site(1, 1, "B"), Fraction(1, 10)),
    (site(1, 1, "C"), site(0, 2, "B"), Fraction(1, 10)),
    (site(0, 2, "B"), site(1, 2, "A"), Fraction(1, 10)),
)


def label(x: Site) -> str:
    return f"{x[0]}:{x[1]},{x[2]}"


def flake(n: int) -> tuple[list[Site], dict[Edge, Fraction], dict[Edge, Fraction]]:
    cells = [(i, j) for j in range(n) for i in range(n - j)]
    basis = [site(i, j, sublattice) for i, j in cells for sublattice in "ABC"]
    baseline: dict[Edge, Fraction] = {}
    for i, j in cells:
        a, b, c = (site(i, j, sublattice) for sublattice in "ABC")
        for x, y in ((a, b), (a, c), (b, c)):
            baseline[edge(x, y)] = Fraction(1, 10)
        if i + 1 < n - j:
            baseline[edge(b, site(i + 1, j, "A"))] = Fraction(1)
        if j + 1 < n - i:
            baseline[edge(c, site(i, j + 1, "A"))] = Fraction(1)
        if i > 0:
            baseline[edge(c, site(i - 1, j + 1, "B"))] = Fraction(1)

    endpoint = dict(baseline)
    changed: set[Edge] = set()
    for x0, y0, target in LOCAL_TARGETS:
        x, y = x0, y0
        for _ in range(3):
            current = edge(x, y)
            if current not in endpoint or endpoint[current] == target:
                raise RuntimeError(f"invalid local change for N={n}: {current}")
            endpoint[current] = target
            changed.add(current)
            x, y = rotate(x, n), rotate(y, n)
    if len(changed) != 45:
        raise RuntimeError(f"the 45 symmetry-completed changes overlap for N={n}")
    rotated = {edge(rotate(x, n), rotate(y, n)): weight for (x, y), weight in endpoint.items()}
    mirrored = {edge(reflect(x), reflect(y)): weight for (x, y), weight in endpoint.items()}
    if rotated != endpoint or mirrored != endpoint:
        raise RuntimeError(f"endpoint symmetry check failed for N={n}")
    return basis, baseline, endpoint


def dense_matrix(basis: list[Site], weights: dict[Edge, Fraction]) -> np.ndarray:
    index = {x: i for i, x in enumerate(basis)}
    matrix = np.zeros((len(basis), len(basis)))
    for (x, y), weight in weights.items():
        i, j = index[x], index[y]
        matrix[i, j] = matrix[j, i] = -float(weight)
    return matrix


def symmetry_bases(basis: list[Site], n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    index = {x: i for i, x in enumerate(basis)}
    seen: set[Site] = set()
    orbits: list[list[Site]] = []
    for x in basis:
        if x in seen:
            continue
        orbit = [x, rotate(x, n), rotate(rotate(x, n), n)]
        if len(set(orbit)) != 3:
            raise RuntimeError("unexpected short C3 orbit")
        seen.update(orbit)
        orbits.append(orbit)
    orbit_index = {x: q for q, orbit in enumerate(orbits) for x in orbit}
    invariant = np.zeros((len(basis), len(orbits)))
    omega_basis = np.zeros((len(basis), len(orbits)), dtype=complex)
    omega = np.exp(2j * np.pi / 3)
    for q, orbit in enumerate(orbits):
        for coefficient, x in zip((1, 1, 1), orbit):
            invariant[index[x], q] = coefficient / np.sqrt(3)
        for coefficient, x in zip((1, omega, omega**2), orbit):
            omega_basis[index[x], q] = coefficient / np.sqrt(3)

    reduced_reflection = np.zeros((len(orbits), len(orbits)))
    for q, orbit in enumerate(orbits):
        for x in orbit:
            reduced_reflection[orbit_index[reflect(x)], q] += Fraction(1, 3)
    reflection_values, reflection_vectors = eigh(reduced_reflection)
    a1 = invariant @ reflection_vectors[:, reflection_values > 0.5]
    a2 = invariant @ reflection_vectors[:, reflection_values < -0.5]
    return a1, a2, omega_basis


def tracked_index(h0: np.ndarray, h1: np.ndarray, trial: np.ndarray) -> tuple[int, np.ndarray]:
    previous = trial / np.linalg.norm(trial)
    chosen = -1
    for lam in np.arange(0, 0.751, 0.01):
        values, vectors = eigh(h0 + lam * (h1 - h0), driver="evr")
        chosen = int(np.argmax(np.abs(vectors.conj().T @ previous) ** 2))
        previous = vectors[:, chosen]
    return chosen, previous


def selected_eigenpair(
    h0: np.ndarray, h1: np.ndarray, lam: float, eigen_index: int
) -> tuple[float, np.ndarray, float]:
    values, vectors = eigh(h0 + lam * (h1 - h0), driver="evr")
    value = float(values[eigen_index])
    vector = vectors[:, eigen_index]
    residual = float(np.linalg.norm((h0 + lam * (h1 - h0)) @ vector - value * vector))
    return value, vector, residual


def corner_region(
    basis: list[Site], weights: dict[Edge, Fraction], n: int, radius: int = 4
) -> tuple[np.ndarray, np.ndarray, list[int]]:
    index = {x: i for i, x in enumerate(basis)}
    adjacency = [[] for _ in basis]
    for x, y in weights:
        i, j = index[x], index[y]
        adjacency[i].append(j)
        adjacency[j].append(i)
    corners = [index[site(0, 0, "A")], index[site(n - 1, 0, "B")], index[site(0, n - 1, "C")]]
    distance = np.full(len(basis), 10**9, dtype=int)
    queue: deque[int] = deque(corners)
    for q in corners:
        distance[q] = 0
    while queue:
        q = queue.popleft()
        for p in adjacency[q]:
            if distance[p] > distance[q] + 1:
                distance[p] = distance[q] + 1
                queue.append(p)
    boundary = np.array([i == 0 or j == 0 or i + j == n - 1 for _, i, j in basis])
    return distance <= radius, boundary, corners


def source_edge_map(record: dict) -> dict[Edge, Fraction]:
    def parse(value: str) -> Site:
        sublattice, ij = value.split(":")
        i, j = map(int, ij.split(","))
        return site(i, j, sublattice)

    return {edge(parse(x), parse(y)): Fraction(item["weight"]) for item in record["weighted_edges"] for x, y in [item["edge"]]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    root = args.project.resolve()
    source_input_a = json.loads((root / "evidence/geschner-input-a.json").read_text())
    source_input_b = json.loads((root / "evidence/geschner-input-b.json").read_text())

    records = []
    e_gaps = []
    max_lifted_residual = 0.0
    for n in range(8, 21):
        basis, baseline, endpoint = flake(n)
        if n == 20 and not (
            endpoint == source_edge_map(source_input_a) == source_edge_map(source_input_b)
        ):
            raise RuntimeError("finite-size generator does not reproduce both source inputs at N=20")
        full0, full1 = dense_matrix(basis, baseline), dense_matrix(basis, endpoint)
        a1_basis, a2_basis, e_basis = symmetry_bases(basis, n)
        blocks = []
        for transform in (a1_basis, a2_basis, e_basis):
            blocks.append(
                (
                    np.real_if_close(transform.conj().T @ full0 @ transform),
                    np.real_if_close(transform.conj().T @ full1 @ transform),
                    transform,
                )
            )

        # The A-corner semi-infinite trial is mirror even.  Its projections select
        # the A1 and E components of the three-state corner branch without using
        # a near-zero eigenvalue tolerance.
        trial_full = np.zeros(len(basis))
        for q, (_, i, j) in enumerate(basis):
            if basis[q][0] == "A":
                trial_full[q] = (-0.1) ** (i + j)
        a1_0, a1_1, a1_transform = blocks[0]
        a2_0, a2_1, a2_transform = blocks[1]
        e_0, e_1, e_transform = blocks[2]
        a1_index, a1_reference = tracked_index(a1_0, a1_1, a1_transform.T @ trial_full)
        e_index, _ = tracked_index(e_0, e_1, e_transform.conj().T @ trial_full)

        a1_probe = eigh(a1_0 + 0.79 * (a1_1 - a1_0), eigvals_only=True)[a1_index]
        a2_probe = eigh(a2_0 + 0.79 * (a2_1 - a2_0), eigvals_only=True)
        a2_index = int(np.argmin(np.abs(a2_probe - a1_probe)))

        def parity_difference(lam: float) -> float:
            x = eigh(
                a1_0 + lam * (a1_1 - a1_0),
                eigvals_only=True,
                subset_by_index=[a1_index, a1_index],
                driver="evr",
            )[0]
            y = eigh(
                a2_0 + lam * (a2_1 - a2_0),
                eigvals_only=True,
                subset_by_index=[a2_index, a2_index],
                driver="evr",
            )[0]
            return float(x - y)

        grid = np.linspace(0.75, 0.82, 141)
        brackets = [
            (x, y)
            for x, y in zip(grid[:-1], grid[1:])
            if parity_difference(x) * parity_difference(y) < 0
        ]
        if not brackets:
            raise RuntimeError(f"no A1/A2 crossing bracket for N={n}")
        coarse = min(brackets, key=lambda interval: abs(np.mean(interval) - 0.792))
        crossing = brentq(parity_difference, *coarse, xtol=5e-15, rtol=1e-14)

        # Make a sign-changing bracket whose endpoint margins dominate the actual
        # eigenpair residuals; this is a controlled float64 bracket, not directed
        # interval arithmetic.
        half_width = 2e-12
        while True:
            left, right = crossing - half_width, crossing + half_width
            endpoint_data = []
            for lam in (left, right):
                e1, v1, r1 = selected_eigenpair(a1_0, a1_1, lam, a1_index)
                e2, v2, r2 = selected_eigenpair(a2_0, a2_1, lam, a2_index)
                endpoint_data.append((e1 - e2, r1 + r2))
            if (
                endpoint_data[0][0] * endpoint_data[1][0] < 0
                and all(abs(delta) > 20 * residual for delta, residual in endpoint_data)
            ):
                break
            half_width *= 2
            if half_width > 1e-7:
                raise RuntimeError(f"could not residual-separate crossing bracket for N={n}")

        a1_energy, a1_vector_reduced, a1_residual = selected_eigenpair(
            a1_0, a1_1, crossing, a1_index
        )
        a2_energy, a2_vector_reduced, a2_residual = selected_eigenpair(
            a2_0, a2_1, crossing, a2_index
        )
        a1_vector = a1_transform @ a1_vector_reduced
        a2_vector = a2_transform @ a2_vector_reduced
        h_cross = full0 + crossing * (full1 - full0)
        lifted_a1_residual = float(np.linalg.norm(h_cross @ a1_vector - a1_energy * a1_vector))
        lifted_a2_residual = float(np.linalg.norm(h_cross @ a2_vector - a2_energy * a2_vector))
        max_lifted_residual = max(max_lifted_residual, lifted_a1_residual, lifted_a2_residual)
        region, boundary, corners = corner_region(basis, baseline, n)

        def localization(vector: np.ndarray) -> dict:
            probability = np.abs(vector) ** 2
            return {
                "three_corner_site_weight": float(np.sum(probability[corners])),
                "corner_region_radius4_weight": float(np.sum(probability[region])),
                "boundary_weight": float(np.sum(probability[boundary])),
                "ipr": float(np.sum(probability**2)),
            }

        record = {
            "side_cells": n,
            "sites": len(basis),
            "A1_dimension": a1_0.shape[0],
            "A2_dimension": a2_0.shape[0],
            "A1_corner_branch_index_zero_based": a1_index,
            "A2_edge_branch_index_zero_based": a2_index,
            "crossing_lambda": crossing,
            "crossing_energy": (a1_energy + a2_energy) / 2,
            "sector_energy_mismatch_at_root": abs(a1_energy - a2_energy),
            "residual_separated_bracket": {
                "left": left,
                "right": right,
                "difference_left": endpoint_data[0][0],
                "difference_right": endpoint_data[1][0],
                "sum_residual_bound_left": endpoint_data[0][1],
                "sum_residual_bound_right": endpoint_data[1][1],
            },
            "lifted_eigenpair_residuals": {
                "A1": lifted_a1_residual,
                "A2": lifted_a2_residual,
            },
            "A1_corner_branch_localization": localization(a1_vector),
            "A2_edge_branch_localization": localization(a2_vector),
        }

        if n in (8, 14, 20):
            scipy_full = eigh(h_cross, eigvals_only=True, driver="evr")
            numpy_full = np.linalg.eigvalsh(h_cross)
            nearest = np.argsort(np.abs(scipy_full - record["crossing_energy"]))[:4]
            record["independent_full_matrix_check"] = {
                "maximum_numpy_scipy_spectrum_difference": float(
                    np.max(np.abs(numpy_full - scipy_full))
                ),
                "four_nearest_scipy_energies": scipy_full[nearest].tolist(),
                "maximum_distance_of_two_nearest_levels_from_sector_crossing": float(
                    np.max(np.abs(scipy_full[nearest[:2]] - record["crossing_energy"]))
                ),
            }

        if n <= 14:
            e_values = eigh(e_0 + 0.792 * (e_1 - e_0), eigvals_only=True)
            neighbor = min(
                (q for q in (e_index - 1, e_index + 1) if 0 <= q < len(e_values)),
                key=lambda q: abs(e_values[q] - e_values[e_index]),
            )
            lo, hi = sorted((e_index, neighbor))

            def e_gap(lam: float) -> float:
                values = eigh(
                    e_0 + lam * (e_1 - e_0),
                    eigvals_only=True,
                    subset_by_index=[lo, hi],
                    driver="evr",
                )
                return float(values[-1] - values[0])

            optimum = minimize_scalar(
                e_gap,
                bounds=(0.77, 0.81),
                method="bounded",
                options={"xatol": 5e-15, "maxiter": 300},
            )
            record["E_sector_avoided_crossing"] = {
                "lambda": float(optimum.x),
                "gap": float(optimum.fun),
                "indices_zero_based": [lo, hi],
            }
            e_gaps.append((n, float(optimum.fun)))
        records.append(record)

    ns = np.array([item["side_cells"] for item in records if item["side_cells"] >= 12], dtype=float)
    roots = np.array([item["crossing_lambda"] for item in records if item["side_cells"] >= 12])
    fit = least_squares(
        lambda p: p[0] + p[1] * p[2] ** (ns - 12) - roots,
        np.array([0.79193952468, roots[0] - 0.79193952468, -0.145]),
        xtol=1e-15,
        ftol=1e-15,
        gtol=1e-15,
        max_nfev=100000,
    )
    root_prediction = fit.x[0] + fit.x[1] * fit.x[2] ** (ns - 12)

    gap_ns = np.array([q[0] for q in e_gaps], dtype=float)
    gap_values = np.array([q[1] for q in e_gaps])
    gap_line = np.polyfit(gap_ns, np.log(gap_values), 1)
    gap_prediction = np.exp(np.polyval(gap_line, gap_ns))

    result = {
        "schema_version": 1,
        "job_id": "phys-00021-p03-research-0e0b8f4a71ad",
        "source_inputs": [
            "evidence/geschner-input-a.json",
            "evidence/geschner-input-b.json",
            "literature/2412.20460v1-source/live_version.tex",
        ],
        "parameters": {"t": 0.1, "t_prime": 1.0, "side_cells": [8, 20]},
        "symmetry_resolution": (
            "Exact graph C3 and mirror symmetries; dense float64 Hamiltonians projected into "
            "mirror-even A1, mirror-odd A2, and complex C3 E sectors."
        ),
        "records": records,
        "crossing_conclusion": (
            "For every tested N=8,...,20, the continued mirror-even corner branch and a "
            "mirror-odd edge branch reverse order inside a residual-separated bracket. "
            "Opposite mirror parity forbids hybridization, so the finite-spectrum isolation "
            "gap reaches zero between the bracket endpoints."
        ),
        "crossing_lambda_scaling_fit": {
            "model": "lambda_N=lambda_infinity+A*q^(N-12)",
            "fit_range": "N=12,...,20",
            "lambda_infinity": float(fit.x[0]),
            "A": float(fit.x[1]),
            "q": float(fit.x[2]),
            "maximum_absolute_fit_residual": float(np.max(np.abs(root_prediction - roots))),
            "interpretation": "descriptive finite-size fit, not an analytic thermodynamic-limit proof",
        },
        "E_sector_gap_scaling_fit": {
            "model": "gap_N=gap_at_N8*q^(N-8) (log-linear fit)",
            "fit_range": "N=8,...,14",
            "q": float(np.exp(gap_line[0])),
            "A_at_N8": float(np.exp(np.polyval(gap_line, 8))),
            "maximum_relative_fit_residual": float(np.max(np.abs(gap_prediction / gap_values - 1))),
            "interpretation": "the same-parity avoided gap decreases exponentially over the resolved range",
        },
        "error_control": {
            "dtype": "float64",
            "eigensolver": "scipy.linalg.eigh driver=evr",
            "root_solver": "scipy.optimize.brentq",
            "maximum_lifted_eigenpair_residual": max_lifted_residual,
            "brackets": (
                "Endpoint signs are opposite and each energy-difference magnitude exceeds "
                "20 times the sum of the two computed sector eigenpair residuals."
            ),
            "limitation": (
                "No directed-rounding interval eigensolver was used; lambda fits and E-sector "
                "gaps are controlled numerical evidence, not exact algebraic certificates."
            ),
        },
    }
    (root / "evidence/finite-size-isolation.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )

    lines = [
        "Symmetry-resolved finite-size isolation test",
        "============================================",
        "t=0.1, t'=1; 45-bond C3-completed Fig. 3 interpolation",
        "N  sites  lambda_cross          E_cross             bracket_width       lifted_residual_max",
    ]
    for item in records:
        bracket = item["residual_separated_bracket"]
        lines.append(
            f"{item['side_cells']:2d} {item['sites']:5d} "
            f"{item['crossing_lambda']:.15f} {item['crossing_energy']:.12f} "
            f"{bracket['right']-bracket['left']:.3e} "
            f"{max(item['lifted_eigenpair_residuals'].values()):.3e}"
        )
    lines.extend(
        [
            "",
            "At every listed N, the A1-A2 energy difference changes sign across the recorded bracket.",
            "Mirror parity is exact for the graph, so this is a symmetry-allowed true crossing and the cluster isolation reaches zero.",
            f"lambda_infinity fit={fit.x[0]:.15f}, q={fit.x[2]:.9f}, max_abs_residual={np.max(np.abs(root_prediction-roots)):.3e}",
            f"resolved E-sector avoided-gap ratio q={np.exp(gap_line[0]):.9f}, max_relative_fit_residual={np.max(np.abs(gap_prediction/gap_values-1)):.3g}",
            f"maximum lifted eigenpair residual={max_lifted_residual:.3e}",
            "Verdict: the coarse lambda=0.8 positive gap was a grid artifact; finite-size isolation vanishes near lambda=0.79194.",
        ]
    )
    (root / "evidence/finite-size-isolation.log").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
