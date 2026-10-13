#!/usr/bin/env python3
"""Exact rational certificate for the N=20 A1/A2 level-order reversal.

The computation uses integer symmetry bases and a positive diagonal Gram
matrix.  Consequently, the inertia of K - mu G counts generalized
eigenvalues below the rational threshold mu without any floating-point
rounding assumption.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import flint
from flint import fmpq


Site = tuple[str, int, int]
Edge = tuple[Site, Site]

LAMBDA_LEFT = Fraction("0.7919395246780079")
LAMBDA_RIGHT = Fraction("0.7919395246820078")
BISECTION_STEPS = 45
SEARCH_RADIUS = Fraction(1, 10**10)

# Float64 is used only to seed a broad 2e-10 search interval.  Exact inertia
# validates and shrinks every final interval.
SEEDS = {
    ("left", "A1"): Fraction("-0.55493041367818141"),
    ("left", "A2"): Fraction("-0.55493041367849627"),
    ("right", "A1"): Fraction("-0.55493041368433538"),
    ("right", "A2"): Fraction("-0.55493041368402052"),
}
TARGET_INDEX = {"A1": 43, "A2": 32}


def parse_site(label: str) -> Site:
    sublattice, coordinates = label.split(":")
    i, j = map(int, coordinates.split(","))
    return sublattice, i, j


def edge(x: Site, y: Site) -> Edge:
    return tuple(sorted((x, y)))


def rotate(x: Site, n: int) -> Site:
    sublattice, i, j = x
    return {"A": "B", "B": "C", "C": "A"}[sublattice], n - 1 - i - j, i


def reflect(x: Site) -> Site:
    sublattice, i, j = x
    return {"A": "A", "B": "C", "C": "B"}[sublattice], j, i


def endpoint_map(record: dict) -> dict[Edge, Fraction]:
    return {
        edge(parse_site(x), parse_site(y)): Fraction(item["weight"])
        for item in record["weighted_edges"]
        for x, y in [item["edge"]]
    }


def baseline_map(record: dict) -> dict[Edge, Fraction]:
    result = endpoint_map(record)
    for item in record["all_rotated_changes"]:
        x, y = map(parse_site, item["edge"])
        result[edge(x, y)] = Fraction(item["from"])
    return result


def integer_sector_basis(
    sites: list[Site], n: int, parity: int
) -> tuple[dict[Site, tuple[int, int]], list[int], dict]:
    """Return disjoint-support integer D3-sector columns and their Gram diagonal."""

    seen: set[Site] = set()
    orbits: list[list[Site]] = []
    for x in sites:
        if x in seen:
            continue
        orbit = [x, rotate(x, n), rotate(rotate(x, n), n)]
        if len(set(orbit)) != 3:
            raise RuntimeError("unexpected short C3 orbit")
        seen.update(orbit)
        orbits.append(orbit)
    if seen != set(sites):
        raise RuntimeError("C3 orbits do not cover the basis")

    orbit_index = {x: q for q, orbit in enumerate(orbits) for x in orbit}
    reflection = [orbit_index[reflect(orbit[0])] for orbit in orbits]
    columns: list[list[tuple[Site, int]]] = []
    fixed_orbits = 0
    paired_orbits = 0
    for q, r in enumerate(reflection):
        if reflection[r] != q:
            raise RuntimeError("reflection is not an involution on C3 orbits")
        if q > r:
            continue
        if q == r:
            fixed_orbits += 1
            if parity == 1:
                columns.append([(x, 1) for x in orbits[q]])
        else:
            paired_orbits += 1
            columns.append(
                [(x, 1) for x in orbits[q]]
                + [(x, parity) for x in orbits[r]]
            )

    site_column = {
        x: (column_index, coefficient)
        for column_index, column in enumerate(columns)
        for x, coefficient in column
    }
    if set(site_column) != set(sites):
        if parity == 1:
            raise RuntimeError("A1 columns do not cover all sites")
        expected = {x for q, orbit in enumerate(orbits) if reflection[q] != q for x in orbit}
        if set(site_column) != expected:
            raise RuntimeError("A2 columns have an unexpected support")
    gram = [sum(coefficient * coefficient for _, coefficient in column) for column in columns]
    metadata = {
        "C3_orbits": len(orbits),
        "reflection_fixed_C3_orbits": fixed_orbits,
        "reflection_paired_C3_orbits": paired_orbits,
        "dimension": len(columns),
        "gram_diagonal_values": sorted(set(gram)),
    }
    return site_column, gram, metadata


def projected_matrix(
    weights: dict[Edge, Fraction],
    site_column: dict[Site, tuple[int, int]],
    dimension: int,
) -> list[list[fmpq]]:
    matrix = [[fmpq(0) for _ in range(dimension)] for _ in range(dimension)]
    for (x, y), weight in weights.items():
        # A2 basis vectors vanish on reflection-fixed C3 orbits.
        if x not in site_column or y not in site_column:
            continue
        i, coefficient_x = site_column[x]
        j, coefficient_y = site_column[y]
        value = -fmpq(weight.numerator, weight.denominator) * coefficient_x * coefficient_y
        matrix[i][j] += value
        matrix[j][i] += value
    if any(matrix[i][j] != matrix[j][i] for i in range(dimension) for j in range(dimension)):
        raise RuntimeError("projected matrix is not symmetric")
    return matrix


def interpolate(
    matrix_0: list[list[fmpq]], matrix_1: list[list[fmpq]], lam: Fraction
) -> list[list[fmpq]]:
    q = fmpq(lam.numerator, lam.denominator)
    return [
        [x + q * (y - x) for x, y in zip(row_0, row_1)]
        for row_0, row_1 in zip(matrix_0, matrix_1)
    ]


def exact_inertia(matrix: list[list[fmpq]]) -> tuple[int, int, int]:
    """Return (negative, zero, positive) under exact symmetric congruence."""

    work = [row[:] for row in matrix]
    dimension = len(work)
    negative = zero = positive = 0
    k = 0
    while k < dimension:
        pivot = next((i for i in range(k, dimension) if work[i][i]), None)
        if pivot is not None:
            if pivot != k:
                work[k], work[pivot] = work[pivot], work[k]
                for row in work:
                    row[k], row[pivot] = row[pivot], row[k]
            diagonal = work[k][k]
            if diagonal > 0:
                positive += 1
            else:
                negative += 1
            for i in range(k + 1, dimension):
                entry = work[i][k]
                if not entry:
                    continue
                for j in range(i, dimension):
                    value = work[i][j] - entry * work[j][k] / diagonal
                    work[i][j] = value
                    work[j][i] = value
            k += 1
            continue

        pair = None
        for i in range(k, dimension):
            for j in range(i + 1, dimension):
                if work[i][j]:
                    pair = (i, j)
                    break
            if pair is not None:
                break
        if pair is None:
            zero += dimension - k
            break

        # All remaining diagonals vanish.  A nonzero off-diagonal 2x2 block
        # [[0,a],[a,0]] contributes one eigenvalue of each sign.
        p, q = pair
        for target in (k, k + 1):
            source = p if target == k else q
            if source != target:
                work[target], work[source] = work[source], work[target]
                for row in work:
                    row[target], row[source] = row[source], row[target]
                p = target if p == source else source if p == target else p
                q = target if q == source else source if q == target else q
        off_diagonal = work[k][k + 1]
        positive += 1
        negative += 1
        for i in range(k + 2, dimension):
            for j in range(i, dimension):
                value = work[i][j] - (
                    work[i][k] * work[j][k + 1]
                    + work[i][k + 1] * work[j][k]
                ) / off_diagonal
                work[i][j] = value
                work[j][i] = value
        k += 2
    return negative, zero, positive


def shifted_form(
    projected: list[list[fmpq]], gram: list[int], threshold: Fraction
) -> list[list[fmpq]]:
    result = [row[:] for row in projected]
    q = fmpq(threshold.numerator, threshold.denominator)
    for i, norm_squared in enumerate(gram):
        result[i][i] -= q * norm_squared
    return result


def count_below(
    projected: list[list[fmpq]], gram: list[int], threshold: Fraction
) -> tuple[int, int, int]:
    return exact_inertia(shifted_form(projected, gram, threshold))


def decimal_string(value: Fraction, digits: int = 42) -> str:
    with localcontext() as context:
        context.prec = digits
        return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def fraction_record(value: Fraction) -> dict:
    return {
        "rational": f"{value.numerator}/{value.denominator}",
        "decimal": decimal_string(value),
    }


def isolate_eigenvalue(
    projected: list[list[fmpq]],
    gram: list[int],
    index: int,
    seed: Fraction,
) -> dict:
    lower = seed - SEARCH_RADIUS
    upper = seed + SEARCH_RADIUS
    lower_inertia = count_below(projected, gram, lower)
    upper_inertia = count_below(projected, gram, upper)
    if lower_inertia[1] or upper_inertia[1]:
        raise RuntimeError("search endpoint is an exact generalized eigenvalue")
    if lower_inertia[0] != index or upper_inertia[0] != index + 1:
        raise RuntimeError(
            f"seed does not isolate eigenvalue {index}: {lower_inertia}, {upper_inertia}"
        )
    for _ in range(BISECTION_STEPS):
        midpoint = (lower + upper) / 2
        midpoint_inertia = count_below(projected, gram, midpoint)
        if midpoint_inertia[1]:
            raise RuntimeError("bisection hit an exact rational generalized eigenvalue")
        if midpoint_inertia[0] <= index:
            lower = midpoint
            lower_inertia = midpoint_inertia
        else:
            upper = midpoint
            upper_inertia = midpoint_inertia
    if lower_inertia[0] != index or upper_inertia[0] != index + 1:
        raise RuntimeError("final generalized-eigenvalue interval failed its inertia counts")
    return {
        "zero_based_index": index,
        "lower": fraction_record(lower),
        "upper": fraction_record(upper),
        "width": fraction_record(upper - lower),
        "inertia_at_lower": {
            "negative": lower_inertia[0],
            "zero": lower_inertia[1],
            "positive": lower_inertia[2],
        },
        "inertia_at_upper": {
            "negative": upper_inertia[0],
            "zero": upper_inertia[1],
            "positive": upper_inertia[2],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    root = args.project.resolve()

    input_a = json.loads((root / "evidence/geschner-input-a.json").read_text())
    input_b = json.loads((root / "evidence/geschner-input-b.json").read_text())
    endpoint_a = endpoint_map(input_a)
    endpoint_b = endpoint_map(input_b)
    baseline_a = baseline_map(input_a)
    baseline_b = baseline_map(input_b)
    if endpoint_a != endpoint_b or baseline_a != baseline_b:
        raise RuntimeError("the two source reconstructions disagree")
    n = input_a["flake"]["side_cells"]
    sites = [parse_site(label) for label in input_a["basis_order"]]
    if n != 20 or len(sites) != 630 or len(set(sites)) != 630:
        raise RuntimeError("certificate is bound to the reconstructed N=20 flake")

    # Verify exact D3 invariance directly on both rational edge maps.
    for name, weights in (("baseline", baseline_a), ("endpoint", endpoint_a)):
        rotated = {edge(rotate(x, n), rotate(y, n)): weight for (x, y), weight in weights.items()}
        reflected = {edge(reflect(x), reflect(y)): weight for (x, y), weight in weights.items()}
        if rotated != weights or reflected != weights:
            raise RuntimeError(f"{name} edge map is not exactly D3 invariant")

    sector_data = {}
    projected_by_sector = {}
    for sector, parity in (("A1", 1), ("A2", -1)):
        site_column, gram, metadata = integer_sector_basis(sites, n, parity)
        matrix_0 = projected_matrix(baseline_a, site_column, len(gram))
        matrix_1 = projected_matrix(endpoint_a, site_column, len(gram))
        sector_data[sector] = {"gram": gram, "metadata": metadata}
        projected_by_sector[sector] = (matrix_0, matrix_1)

    endpoint_results = {}
    for endpoint_name, lam in (("left", LAMBDA_LEFT), ("right", LAMBDA_RIGHT)):
        endpoint_results[endpoint_name] = {"lambda": fraction_record(lam), "sectors": {}}
        for sector in ("A1", "A2"):
            matrix_0, matrix_1 = projected_by_sector[sector]
            projected = interpolate(matrix_0, matrix_1, lam)
            endpoint_results[endpoint_name]["sectors"][sector] = isolate_eigenvalue(
                projected,
                sector_data[sector]["gram"],
                TARGET_INDEX[sector],
                SEEDS[(endpoint_name, sector)],
            )

    left_a1 = Fraction(endpoint_results["left"]["sectors"]["A1"]["lower"]["rational"])
    left_a2 = Fraction(endpoint_results["left"]["sectors"]["A2"]["upper"]["rational"])
    right_a1 = Fraction(endpoint_results["right"]["sectors"]["A1"]["upper"]["rational"])
    right_a2 = Fraction(endpoint_results["right"]["sectors"]["A2"]["lower"]["rational"])
    left_separation = left_a1 - left_a2
    right_separation = right_a2 - right_a1
    if left_separation <= 0 or right_separation <= 0:
        raise RuntimeError("certified sector intervals do not reverse order")

    record = {
        "schema_version": 1,
        "job_id": "phys-00021-p03-research-64db9546ea0d",
        "source_inputs": [
            "evidence/geschner-input-a.json",
            "evidence/geschner-input-b.json",
            "literature/2412.20460v1-source/live_version.tex",
        ],
        "exact_arithmetic": {
            "backend": f"python-flint {flint.__version__}",
            "coefficient_domain": "Q",
            "method": (
                "Integer D3 symmetry bases, diagonal positive Gram matrices, and exact "
                "symmetric-congruence inertia of K-mu*G with rational lambda and mu."
            ),
            "bisection_steps": BISECTION_STEPS,
            "floating_point_role": (
                "Prior float64 values seed only broad 2e-10 energy intervals; every "
                "reported enclosure and ordering is decided by exact rational inertia."
            ),
        },
        "flake": {"side_cells": n, "sites": len(sites)},
        "edge_maps": {
            "input_A_equals_input_B": True,
            "baseline_edges": len(baseline_a),
            "endpoint_edges": len(endpoint_a),
            "exact_C3_invariance": True,
            "exact_mirror_invariance": True,
        },
        "sectors": {
            sector: sector_data[sector]["metadata"] for sector in ("A1", "A2")
        },
        "endpoints": endpoint_results,
        "certified_ordering": {
            "left": "E_A2 < E_A1",
            "left_interval_separation_lower_bound": fraction_record(left_separation),
            "right": "E_A1 < E_A2",
            "right_interval_separation_lower_bound": fraction_record(right_separation),
        },
        "conclusion": (
            "The indexed A1 and A2 generalized eigenvalues reverse strict order between "
            "the two rational lambda endpoints. Hermitian eigenvalues depend continuously "
            "on lambda, so at least one exact A1/A2 degeneracy lies in the closed bracket. "
            "Because the two states have opposite exact mirror parity, this is a symmetry-"
            "allowed level crossing rather than an avoided crossing."
        ),
        "limitations": (
            "The certificate proves existence, sector indices, and the N=20 rational "
            "bracket. It does not prove uniqueness of the crossing, a thermodynamic limit, "
            "or the empirical finite-size convergence factor."
        ),
    }

    output_json = root / "evidence/parity-crossing-certificate.json"
    output_log = root / "evidence/parity-crossing-certificate.log"
    output_json.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    lines = [
        "Exact N=20 parity-crossing certificate",
        "=======================================",
        f"job_id={record['job_id']}",
        f"python_flint={flint.__version__}",
        "input_A_equals_input_B=True",
        "exact_D3_invariance=True",
        f"A1_dimension={record['sectors']['A1']['dimension']}",
        f"A2_dimension={record['sectors']['A2']['dimension']}",
    ]
    for endpoint_name in ("left", "right"):
        endpoint = endpoint_results[endpoint_name]
        lines.append(f"{endpoint_name}_lambda={endpoint['lambda']['rational']}")
        for sector in ("A1", "A2"):
            item = endpoint["sectors"][sector]
            lines.append(
                f"{endpoint_name}_{sector}_eigenvalue_{item['zero_based_index']} in "
                f"[{item['lower']['rational']}, {item['upper']['rational']}]"
            )
            lines.append(
                f"{endpoint_name}_{sector}_inertias="
                f"({item['inertia_at_lower']['negative']},"
                f"{item['inertia_at_lower']['zero']},"
                f"{item['inertia_at_lower']['positive']}) -> "
                f"({item['inertia_at_upper']['negative']},"
                f"{item['inertia_at_upper']['zero']},"
                f"{item['inertia_at_upper']['positive']})"
            )
    lines.extend(
        [
            f"left_order=E_A2<E_A1; separation>{decimal_string(left_separation)}",
            f"right_order=E_A1<E_A2; separation>{decimal_string(right_separation)}",
            "continuity_plus_opposite_mirror_parity=EXACT_CROSSING_EXISTS_IN_BRACKET",
            "verdict=EXACT_PASS",
        ]
    )
    output_log.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
