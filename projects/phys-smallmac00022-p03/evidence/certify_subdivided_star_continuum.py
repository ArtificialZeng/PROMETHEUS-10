#!/usr/bin/env python3
"""Exact all-parameter certificates for finitely many subdivided stars.

For T_q (q leaves at C and the path C--A--B), this script proves the
strict gap inequality on 0<t=s^2<1 for each requested integer q.  It uses
the exact leaf-spin/charge decomposition and a root-crossing certificate:
if the top Q=0 root came within 1-t of any other eigenvalue, an explicitly
computed resultant would vanish.  Every interior resultant root is
isolated over QQ and surrounded by a rational interval on which the true
spectral margin stays positive by Weyl's inequality.  One exact reference
point then fixes the sign on the whole connected interval.

The matrices below are the nonorthogonal collective-weight matrices.  For
t>0 they are diagonally similar to the real-symmetric spin matrices, so
their characteristic roots are precisely the physical eigenvalues.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import sympy as sp


S, T, X = sp.symbols("s t x")


def multiplicity(q: int, r: int) -> int:
    return math.comb(q, r) - (math.comb(q, r - 1) if r else 0)


def states(q: int, r: int, charge: int) -> list[tuple[int, int, int, int]]:
    result: list[tuple[int, int, int, int]] = []
    for c in (0, 1):
        for a in (0, 1):
            for b in (0, 1):
                k = charge - a + c + b
                if r <= k <= q - r:
                    result.append((c, a, b, k))
    return result


def charge_matrix(q: int, r: int, charge: int) -> sp.Matrix:
    basis = states(q, r, charge)
    index = {state: position for position, state in enumerate(basis)}
    matrix = sp.zeros(len(basis))
    for state, column in index.items():
        c, a, b, k = state
        matrix[column, column] += q - k if c == 0 else S**2 * k
        target = (1, a, b, k + 1) if c == 0 else (0, a, b, k - 1)
        if target in index:
            matrix[index[target], column] += S * (
                k - r + 1 if c == 0 else q - r - k + 1
            )

        if c == a == 0:
            matrix[column, column] += 1
            matrix[index[(1, 1, b, k)], column] += S
        elif c == a == 1:
            matrix[column, column] += S**2
            matrix[index[(0, 0, b, k)], column] += S

        if a == b == 0:
            matrix[column, column] += 1
            matrix[index[(c, 1, 1, k)], column] += S
        elif a == b == 1:
            matrix[column, column] += S**2
            matrix[index[(c, 0, 0, k)], column] += S
    return matrix


def polynomial_in_t(matrix: sp.Matrix) -> sp.Poly:
    raw = sp.Poly(sp.expand(matrix.charpoly(X).as_expr()), S)
    assert all(power[0] % 2 == 0 for power, _ in raw.terms())
    expression = sp.expand(
        sum(coefficient * T ** (power[0] // 2)
            for power, coefficient in raw.terms())
    )
    return sp.Poly(expression, X, T, domain=sp.QQ)


def remove_zero_roots(polynomial: sp.Poly) -> tuple[sp.Poly, int]:
    expression = polynomial.as_expr()
    count = 0
    while sp.Poly(expression, X, T, domain=sp.QQ).eval({X: 0}) == 0:
        expression = sp.cancel(expression / X)
        count += 1
    return sp.Poly(expression, X, T, domain=sp.QQ), count


def coefficient_digest(polynomial: sp.Poly) -> str:
    primitive = sp.Poly(polynomial, *polynomial.gens, domain=sp.QQ).clear_denoms()[1]
    payload = json.dumps(
        [
            {"monomial": list(monomial), "coefficient": str(coefficient)}
            for monomial, coefficient in primitive.terms()
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def endpoint_free_squarefree(resultant: sp.Expr) -> tuple[sp.Poly, int, int]:
    polynomial = sp.Poly(resultant, T, domain=sp.QQ)
    zero_order = 0
    one_order = 0
    while polynomial.eval(0) == 0:
        polynomial = polynomial.exquo(sp.Poly(T, T, domain=sp.QQ))
        zero_order += 1
    while polynomial.eval(1) == 0:
        polynomial = polynomial.exquo(sp.Poly(T - 1, T, domain=sp.QQ))
        one_order += 1
    return polynomial.sqf_part().monic(), zero_order, one_order


def rational_text(value: sp.Rational) -> str:
    value = sp.Rational(value)
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def decimal_text(value: sp.Rational, digits: int = 16) -> str:
    return str(sp.N(value, digits))


def real_intervals(polynomial: sp.Poly, epsilon_power: int) -> list[tuple[sp.Rational, sp.Rational, int]]:
    raw = polynomial.intervals(eps=sp.Rational(1, 10**epsilon_power))
    return [
        (sp.Rational(interval[0]), sp.Rational(interval[1]), int(multiplicity_))
        for interval, multiplicity_ in raw
    ]


def physical_root_intervals(polynomial: sp.Poly, t_value: sp.Rational,
                            epsilon_power: int = 28) -> list[tuple[sp.Rational, sp.Rational]]:
    specialized = sp.Poly(polynomial.as_expr().subs(T, t_value), X, domain=sp.QQ)
    intervals = real_intervals(specialized, epsilon_power)
    assert sum(multiplicity_ for _lo, _hi, multiplicity_ in intervals) == specialized.degree()
    expanded: list[tuple[sp.Rational, sp.Rational]] = []
    for lo, hi, multiplicity_ in intervals:
        expanded.extend([(lo, hi)] * multiplicity_)
    expanded.sort()
    return expanded


def margin_at(blocks: list[dict[str, object]], ground: sp.Poly,
              t_value: sp.Rational) -> sp.Rational:
    ground_roots = physical_root_intervals(ground, t_value)
    assert ground_roots
    ground_lo = ground_roots[-1][0]
    competitor_upper = sp.Rational(0)  # every stripped x root is harmless but retained here

    for block in blocks:
        roots = physical_root_intervals(block["polynomial"], t_value)
        if block["ground"]:
            assert roots[-1][1] < ground_lo or roots[-1] == ground_roots[-1]
            roots = roots[:-1]
        if roots:
            competitor_upper = max(competitor_upper, max(hi for _lo, hi in roots))
    return sp.factor(ground_lo - competitor_upper - (1 - t_value))


def block_inventory(q: int) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    represented_dimension = 0
    for r in range(q // 2 + 1):
        spin_dimension = 0
        for charge in range(r - 2, q - r + 2):
            basis = states(q, r, charge)
            if not basis:
                continue
            polynomial, zero_roots = remove_zero_roots(
                polynomial_in_t(charge_matrix(q, r, charge))
            )
            spin_dimension += len(basis)
            if polynomial.degree(X) == 0:
                continue
            blocks.append({
                "r": r,
                "charge": charge,
                "parity": charge % 2,
                "dimension": len(basis),
                "zero_roots": zero_roots,
                "ground": r == 0 and charge == 0,
                "polynomial": polynomial,
            })
        represented_dimension += multiplicity(q, r) * spin_dimension
    assert represented_dimension == 2 ** (q + 3)
    assert sum(1 for block in blocks if block["ground"]) == 1
    return blocks


def certify_q(q: int, resultant_epsilon_power: int) -> dict[str, object]:
    blocks = block_inventory(q)
    ground = next(block["polynomial"] for block in blocks if block["ground"])
    assert ground.degree(X) == 6

    resultant_records: list[dict[str, object]] = []
    candidate_intervals: list[tuple[sp.Rational, sp.Rational, str]] = []
    for block in blocks:
        shifted = block["polynomial"].as_expr().subs(X, X - (1 - T))
        resultant = sp.resultant(ground.as_expr(), shifted, X)
        if resultant == 0:
            raise RuntimeError(f"identically zero crossing resultant at q={q}, block={block}")
        core, zero_order, one_order = endpoint_free_squarefree(resultant)
        intervals = real_intervals(core, resultant_epsilon_power)
        interior = []
        label = f"r={block['r']},Q={block['charge']}"
        for lo, hi, _multiplicity in intervals:
            if hi <= 0 or lo >= 1:
                continue
            if not (0 < lo <= hi < 1):
                raise RuntimeError(f"endpoint-straddling interval {lo, hi} for {label}")
            interior.append((lo, hi))
            candidate_intervals.append((lo, hi, label))
        resultant_records.append({
            "block": label,
            "parity": block["parity"],
            "resultant_degree_after_endpoint_removal": core.degree(),
            "resultant_coefficient_sha256": coefficient_digest(core),
            "t_zero_order": zero_order,
            "t_one_order": one_order,
            "interior_real_roots": len(interior),
        })

    # The derivative of one local edge term has norm
    # s+sqrt(1+s^2) < 5/2 on 0<s<1.  With q+2 edges, every ordered
    # eigenvalue is L-Lipschitz in s for L=5(q+2)/2.
    lipschitz = sp.Rational(5 * (q + 2), 2)
    neighborhood_records: list[dict[str, str]] = []
    minimum_slack: sp.Rational | None = None
    for lo, hi, label in candidate_intervals:
        midpoint = (lo + hi) / 2
        lower_margin = margin_at(blocks, ground, midpoint)
        half_width = (hi - lo) / 2
        # sqrt(t)+sqrt(t0) >= 2*sqrt(lo) >= 2*lo on (0,1).
        variation_bound = sp.factor(half_width * (lipschitz / lo + 1))
        slack = sp.factor(lower_margin - variation_bound)
        if not slack > 0:
            raise RuntimeError(
                f"continuity enclosure failed q={q}, {label}, interval={(lo, hi)}"
            )
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        neighborhood_records.append({
            "block": label,
            "t_lo": rational_text(lo),
            "t_hi": rational_text(hi),
            "t_mid_decimal": decimal_text(midpoint),
            "exact_margin_lower": rational_text(lower_margin),
            "continuity_variation_upper": rational_text(variation_bound),
            "certified_slack_decimal": decimal_text(slack),
        })

    reference_t = sp.Rational(1, 4)
    reference_margin = margin_at(blocks, ground, reference_t)
    assert reference_margin > 0
    return {
        "q": q,
        "n": q + 3,
        "edge_count": q + 2,
        "nonzero_charge_spin_blocks": len(blocks),
        "ground_factor": "r=0,Q=0,degree=6",
        "ground_coefficient_sha256": coefficient_digest(ground),
        "crossing_resultants": resultant_records,
        "interior_candidate_root_count_with_duplicates": len(candidate_intervals),
        "candidate_root_neighborhoods": neighborhood_records,
        "reference_t": "1/4",
        "reference_margin_lower": rational_text(reference_margin),
        "reference_margin_lower_decimal": decimal_text(reference_margin),
        "minimum_candidate_neighborhood_slack_decimal": (
            decimal_text(minimum_slack) if minimum_slack is not None else "not_applicable"
        ),
        "conclusion": "Delta(T_q,s)>1-s^2 for every real 0<s<1",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-q", type=int, default=2)
    parser.add_argument("--max-q", type=int, default=8)
    parser.add_argument("--resultant-epsilon-power", type=int, default=24)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 2 <= args.min_q <= args.max_q:
        raise SystemExit("require 2 <= min-q <= max-q")
    records = [
        certify_q(q, args.resultant_epsilon_power)
        for q in range(args.min_q, args.max_q + 1)
    ]
    packet = {
        "job_id": "phys-00022-p03-research-3760713db390",
        "status": "exact_computer_assisted_continuum_certificate",
        "operator": "K_s=-H_s with unnormalized |00>+s|11> edge terms",
        "family": "T_q: q leaves at C plus C--A--B",
        "parameter_domain": "integer min_q<=q<=max_q and real 0<s<1",
        "method": (
            "exact QQ[t,x] charge-spin characteristic polynomials; exact crossing "
            "resultants and exact VAS continued-fraction real-root isolation; "
            "rational root enclosures; Weyl "
            "continuity bound around every interior resultant root; one exact "
            "reference sign per q"
        ),
        "logical_scope": (
            "A zero of the actual strict margin forces one of the enumerated "
            "resultants to vanish. Every such interior root has a neighborhood "
            "with positive actual margin, and the reference margin is positive; "
            "continuity excludes a zero anywhere in (0,1)."
        ),
        "zero_eigenvalue_exclusion": (
            "The all-zero computational state has Rayleigh quotient q+2 for K_s, "
            "so the top root minus a stripped zero root exceeds 1-t."
        ),
        "local_derivative_bound": (
            "||d |phi_s><phi_s|/ds|| = s+sqrt(1+s^2) < 5/2; "
            "the certificate uses L=5(q+2)/2 for each ordered eigenvalue."
        ),
        "min_q": args.min_q,
        "max_q": args.max_q,
        "records": records,
        "limitations": (
            "Finite q range only. This does not establish the whole subdivided-star "
            "family, exclude arbitrary trees, or prove the universal source conjecture."
        ),
    }
    args.output.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")
    print(f"continuum_certificates=PASS q={args.min_q}..{args.max_q}")
    print(f"cases={len(records)}")
    print("strict_margin_domain=0<s<1")
    print("scope=finite_subdivided_star_range_only")


if __name__ == "__main__":
    main()
