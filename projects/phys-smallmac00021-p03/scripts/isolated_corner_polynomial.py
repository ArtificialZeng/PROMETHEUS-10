#!/usr/bin/env python3
"""Exact t=0 corner-core polynomial for Geschner et al. Fig. 3.

The graph is reconstructed from integer plot coordinates.  At t=0 the
interpolation support is a finite invariant component; all algebra is exact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
E, LAM = sp.symbols("E lambda")
N = 6

# Bonds read from the left-corner author raster.  Short grey bonds ramp on;
# long black bonds ramp off under H_lambda=(1-lambda)H+lambda H'.
RAMP_ON = [
    ((0, 0), (2, 0)), ((0, 0), (1, 1)), ((2, 0), (1, 1)),
    ((6, 0), (8, 0)), ((3, 3), (4, 4)), ((12, 0), (13, 1)),
    ((6, 6), (8, 6)),
]
RAMP_OFF = [
    ((2, 0), (6, 0)), ((1, 1), (3, 3)), ((8, 0), (12, 0)),
    ((4, 4), (6, 6)), ((13, 1), (15, 3)), ((13, 1), (11, 3)),
    ((10, 4), (8, 6)), ((8, 6), (12, 6)),
]


def canon(a, b):
    return tuple(sorted((tuple(a), tuple(b))))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_coordinate_graph():
    sites = {}
    for j in range(N):
        for i in range(N - j):
            entries = {
                f"A:{i},{j}": (6 * i + 3 * j, 3 * j),
                f"B:{i},{j}": (6 * i + 3 * j + 2, 3 * j),
                f"C:{i},{j}": (6 * i + 3 * j + 1, 3 * j + 1),
            }
            for label, point in entries.items():
                assert point not in sites
                sites[point] = label

    def metric2(a, b):
        return (a[0] - b[0]) ** 2 + 3 * (a[1] - b[1]) ** 2

    points = sorted(sites)
    strong = set()
    for ia, a in enumerate(points):
        for b in points[ia + 1 :]:
            if sites[a][0] != sites[b][0] and metric2(a, b) == 16:
                strong.add(canon(a, b))

    generic = strong | {canon(*edge) for edge in RAMP_ON}
    component = {(0, 0)}
    frontier = [(0, 0)]
    while frontier:
        x = frontier.pop()
        for a, b in generic:
            if x == a and b not in component:
                component.add(b); frontier.append(b)
            elif x == b and a not in component:
                component.add(a); frontier.append(a)
    edges = sorted(edge for edge in generic if edge[0] in component)
    assert all(edge[1] in component for edge in edges)
    return sites, sorted(component), edges, strong


def verify_three_corner_decomposition():
    """Exact graph check that the N=20 deformation has three disjoint cores."""
    n = 20
    sites = {}
    for j in range(n):
        for i in range(n - j):
            for sub, point in {
                "A": (6 * i + 3 * j, 3 * j),
                "B": (6 * i + 3 * j + 2, 3 * j),
                "C": (6 * i + 3 * j + 1, 3 * j + 1),
            }.items():
                sites[point] = f"{sub}:{i},{j}"
    points = sorted(sites)
    strong = set()
    for ia, a in enumerate(points):
        for b in points[ia + 1 :]:
            if sites[a][0] == sites[b][0]:
                continue
            if (a[0] - b[0]) ** 2 + 3 * (a[1] - b[1]) ** 2 == 16:
                strong.add(canon(a, b))

    length = 6 * n - 4
    cu, cv = Q(length, 2), Q(length, 6)

    def rotate(p):
        x, y = Q(p[0]) - cu, Q(p[1]) - cv
        u = cu - x / 2 - 3 * y / 2
        v = cv + x / 2 - y / 2
        assert u.denominator == v.denominator == 1
        q = (int(u), int(v))
        assert q in sites
        return q

    on0, off0 = {canon(*e) for e in RAMP_ON}, {canon(*e) for e in RAMP_OFF}
    all_on, all_off = set(), set()
    for collection, target in ((on0, all_on), (off0, all_off)):
        for a0, b0 in collection:
            a, b = a0, b0
            for _ in range(3):
                target.add(canon(a, b))
                a, b = rotate(a), rotate(b)
    assert len(all_on) == 21 and len(all_off) == 24
    generic = strong | all_on

    corners = []
    corner = (0, 0)
    for _ in range(3):
        component, frontier = {corner}, [corner]
        while frontier:
            x = frontier.pop()
            for a, b in generic:
                y = b if x == a else a if x == b else None
                if y is not None and y not in component:
                    component.add(y); frontier.append(y)
        core_edges = {e for e in generic if e[0] in component or e[1] in component}
        assert all(a in component and b in component for a, b in core_edges)
        assert (len(component), len(core_edges)) == (15, 17)
        assert sum(e in all_on for e in core_edges) == 7
        assert sum(e in all_off for e in core_edges) == 8
        corners.append(component)
        corner = rotate(corner)
    assert not (corners[0] & corners[1] or corners[0] & corners[2] or corners[1] & corners[2])
    assert all(a in set.union(*corners) and b in set.union(*corners) for a, b in all_on | all_off)
    return {
        "flake_N": n,
        "site_count": len(sites),
        "corner_component_sizes": [len(c) for c in corners],
        "components_pairwise_disjoint": True,
        "ramp_on_edges": len(all_on),
        "ramp_off_edges": len(all_off),
        "all_changed_edges_inside_three_cores": True,
    }


def sector_polynomial(H, reflection, parity):
    used = set()
    columns = []
    for i in range(H.rows):
        if i in used:
            continue
        j = reflection[i]
        used.update((i, j))
        col = sp.zeros(H.rows, 1)
        if i == j:
            if parity == 1:
                col[i] = 1
                columns.append(col)
        else:
            col[i], col[j] = 1, parity
            columns.append(col)
    B = sp.Matrix.hstack(*columns)
    G, K = B.T * B, B.T * H * B
    return sp.Poly(sp.cancel((E * G - K).det() / G.det()), E, LAM)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--log", required=True)
    args = parser.parse_args()

    sites, vertices, edges, strong = build_coordinate_graph()
    assert (len(vertices), len(edges)) == (15, 17)
    index = {point: i for i, point in enumerate(vertices)}
    on = {canon(*edge) for edge in RAMP_ON}
    off = {canon(*edge) for edge in RAMP_OFF}
    edge_records = []
    H = sp.zeros(15)
    counts = {"lambda": 0, "one_minus_lambda": 0, "one": 0}
    for a, b in edges:
        if (a, b) in on:
            weight, kind = LAM, "lambda"
        elif (a, b) in off:
            weight, kind = 1 - LAM, "one_minus_lambda"
        else:
            assert (a, b) in strong
            weight, kind = sp.Integer(1), "one"
        counts[kind] += 1
        i, j = index[a], index[b]
        H[i, j] = H[j, i] = -weight
        edge_records.append({"i": i, "j": j, "kind": kind})
    assert counts == {"lambda": 7, "one_minus_lambda": 8, "one": 2}

    # Reflection through the plotted corner bisector in the metric du^2+3dv^2.
    reflected = lambda p: ((p[0] + 3 * p[1]) // 2, (p[0] - p[1]) // 2)
    reflection = {i: index[reflected(p)] for i, p in enumerate(vertices)}
    assert all(reflection[reflection[i]] == i for i in reflection)
    assert H.extract([reflection[i] for i in range(15)], [reflection[i] for i in range(15)]) == H

    chi = sp.Poly(H.charpoly(E).as_expr(), E, LAM)
    even = sector_polynomial(H, reflection, +1)
    odd = sector_polynomial(H, reflection, -1)
    assert sp.expand(even.as_expr() * odd.as_expr() - chi.as_expr()) == 0
    assert sp.rem(even.as_expr(), E - 1, E) == 0
    assert sp.rem(odd.as_expr(), E - 1, E) == 0
    p7 = sp.Poly(sp.cancel(even.as_expr() / (E - 1)), E, LAM)
    p6 = sp.Poly(sp.cancel(odd.as_expr() / (E - 1)), E, LAM)
    assert p7.degree(E) == 7 and p6.degree(E) == 6

    lam_coeffs = [sp.Poly(c, E) for c in sp.Poly(chi.as_expr(), LAM).all_coeffs() if c != 0]
    gcd = lam_coeffs[0]
    for coefficient in lam_coeffs[1:]:
        gcd = sp.gcd(gcd, coefficient)
    gcd = gcd.monic()
    assert sp.expand(gcd.as_expr() - (E - 1) ** 2) == 0
    quotient = sp.Poly(sp.cancel(chi.as_expr() / (E - 1) ** 2), E, LAM)
    q11 = sp.Poly(quotient.as_expr(), LAM).coeff_monomial(LAM ** 11)
    q12 = sp.Poly(quotient.as_expr(), LAM).coeff_monomial(LAM ** 12)
    assert sp.gcd(sp.Poly(q11, E), sp.Poly(q12, E)).degree() == 0

    endpoint0 = sp.factor(chi.as_expr().subs(LAM, 0))
    endpoint1 = sp.factor(chi.as_expr().subs(LAM, 1))
    assert sp.expand(endpoint0 - E * (E - 1) ** 8 * (E + 1) ** 4 * (E + 2) ** 2) == 0
    assert sp.expand(endpoint1 - (E - 1) ** 8 * (E + 1) ** 6 * (E + 2)) == 0

    coeff_table = [
        {"E_power": int(pe), "lambda_power": int(pl), "coefficient": int(c)}
        for (pe, pl), c in sorted(chi.terms(), reverse=True)
    ]
    record = {
        "schema_version": 1,
        "job_id": "phys-00021-p03-research-09fdc4c78c93",
        "source": {
            "identifier": "arXiv:2412.20460v1, Fig. 3 and Eq. (5)",
            "figure": "literature/2412.20460v1-source/figures/interpolation.png",
            "figure_sha256": sha256(ROOT / "literature/2412.20460v1-source/figures/interpolation.png"),
            "tex": "literature/2412.20460v1-source/live_version.tex",
            "tex_sha256": sha256(ROOT / "literature/2412.20460v1-source/live_version.tex"),
            "published_doi": "10.1103/vfyz-74qy",
        },
        "hamiltonian_convention": "det(E I-H), H_ij=-w_ij, t'=1, t=0, H_lambda=(1-lambda)H+lambda H'",
        "vertices": [
            {"index": i, "plot_coordinate": list(p), "site": sites[p]}
            for i, p in enumerate(vertices)
        ],
        "edges": edge_records,
        "edge_counts": counts,
        "reflection": [reflection[i] for i in range(15)],
        "characteristic_polynomial": sp.sstr(chi.as_expr()),
        "expanded_coefficients": coeff_table,
        "factorization": {
            "form": "(E - 1)^2 * P6(E,lambda) * P7(E,lambda)",
            "P6": sp.sstr(p6.as_expr()),
            "P7": sp.sstr(p7.as_expr()),
            "P6_sector": "mirror_odd",
            "P7_sector": "mirror_even_after_one_fixed_E=1_factor",
        },
        "coefficient_gcd_in_QE": sp.sstr(gcd.as_expr()),
        "coprime_quotient_witness": {
            "lambda_11": sp.sstr(q11),
            "lambda_12": sp.sstr(q12),
            "gcd": "1",
        },
        "endpoints": {"lambda_0": sp.sstr(endpoint0), "lambda_1": sp.sstr(endpoint1)},
        "counting": {
            "component_dimension": 15,
            "lambda_independent_factor_degree": 2,
            "nonconstant_root_degree_per_corner": 13,
            "three_disjoint_corners": 39,
        },
        "three_corner_decomposition": verify_three_corner_decomposition(),
        "scope": "Exact for each raster-defined invariant corner component at t=0; three-corner count assumes the three D3-related components are disjoint, as in the N=20 flake. It is not a t=0.1 or thermodynamic claim.",
    }
    out = ROOT / args.output
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    log_lines = [
        "Exact isolated-corner polynomial reconstruction",
        f"vertices={len(vertices)} edges={len(edges)} counts={counts}",
        f"factorization={record['factorization']['form']}",
        f"gcd={record['coefficient_gcd_in_QE']}",
        f"q11={q11}", f"q12={q12}",
        f"lambda=0: {endpoint0}", f"lambda=1: {endpoint1}",
        "fixed-degree=2 nonconstant-degree=13 three-corner-degree=39",
        f"certificate_sha256={sha256(out)}",
    ]
    (ROOT / args.log).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "output": args.output, "log": args.log, "certificate_sha256": sha256(out)}, sort_keys=True))


if __name__ == "__main__":
    main()
