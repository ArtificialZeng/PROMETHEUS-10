#!/usr/bin/env python3
"""Exact k=5 classification of the two Figure-5 Sierpinski--Hanoi landmarks.

The reproduced generator supplies the signed all-cycle-+1 augmented root graph.
This script keeps all algebra over ZZ/QQ (and uses i only for the final spectral
interpretation).  Its principal variable ``x`` is the eigenvalue of ``2 i h``;
the plotted source variable is therefore ``lambda=x/2``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
GENERATOR = HERE / "reproduce_sierpinski_hanoi.py"
RESULT = HERE / "exact-k5-degeneracy.json"
KERNEL = HERE / "exact-k5-kernel-basis.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("sierpinski_reproduction", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load reproduced graph generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_rank_mod_p(matrix: sp.Matrix, prime: int) -> int:
    """Deterministic dense row rank over F_p for the small certificate matrix."""
    rows = [[int(matrix[i, j]) % prime for j in range(matrix.cols)]
            for i in range(matrix.rows)]
    rank = 0
    for col in range(matrix.cols):
        pivot = next((row for row in range(rank, matrix.rows)
                      if rows[row][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, prime)
        rows[rank] = [(entry * inv) % prime for entry in rows[rank]]
        for row in range(matrix.rows):
            if row != rank and rows[row][col]:
                q = rows[row][col]
                rows[row] = [(a - q * b) % prime
                             for a, b in zip(rows[row], rows[rank])]
        rank += 1
        if rank == matrix.rows:
            break
    return rank


def primitive_integer_rows(matrix: sp.Matrix) -> list[list[int]]:
    output: list[list[int]] = []
    for row in range(matrix.rows):
        values = list(matrix.row(row))
        scale = math.lcm(*(int(sp.denom(value)) for value in values))
        integers = [int(value * scale) for value in values]
        common = math.gcd(*(abs(value) for value in integers))
        if common:
            integers = [value // common for value in integers]
        first = next(value for value in integers if value)
        if first < 0:
            integers = [-value for value in integers]
        output.append(integers)
    return output


def coordinates_on_columns(operator: sp.Matrix, basis: sp.Matrix,
                           pivot_rows: tuple[int, ...], inverse_pivot: sp.Matrix) -> sp.Matrix:
    image = operator * basis
    return inverse_pivot * image.extract(pivot_rows, range(basis.cols))


def positive_character(operator_rep: sp.Matrix, complex_structure_rep: sp.Matrix) -> sp.Expr:
    # On ker(B^2+I), the positive eigenvalue of iB is selected by (I+iB)/2.
    return sp.simplify(
        (sp.trace(operator_rep) + sp.I * sp.trace(operator_rep * complex_structure_rep)) / 2
    )


def irrep_multiplicities(characters: dict[str, int]) -> dict[str, int]:
    identity = characters["identity"]
    rotation = characters["three_cycle"]
    reflection = characters["reflection"]
    return {
        "A1_trivial": (identity + 2 * rotation + 3 * reflection) // 6,
        "A2_sign": (identity + 2 * rotation - 3 * reflection) // 6,
        "E_standard_2d": (identity - rotation) // 3,
    }


def rational_text(value: sp.Rational) -> str:
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def main() -> None:
    expected_python = os.environ.get("PHYSICS_PYTHON")
    if not expected_python or Path(sys.executable).resolve() != Path(expected_python).resolve():
        raise RuntimeError(
            f"scientific Python mismatch: executable={sys.executable!r}, "
            f"PHYSICS_PYTHON={expected_python!r}"
        )

    rr = load_generator()
    addresses, terms, frustration, _ = rr.graph_from_cells(5)
    cliques, root_edges, _ = rr.krausz_root(len(addresses), frustration)
    oriented, _, _, flux = rr.all_plus_orientation(terms, root_edges)
    n, augmented_edges, augmented_oriented, local_vertices, degrees = rr.augment_local(
        root_edges, oriented, cliques
    )
    if (n, len(root_edges), len(local_vertices), len(flux)) != (108, 81, 39, 13):
        raise RuntimeError("reproduced k=5 graph counts changed")

    J, z, x = sp.symbols("J z x")
    twice_h = sp.zeros(n)
    for edge, (u, v) in enumerate(augmented_oriented):
        weight = sp.Integer(1) if edge < len(root_edges) else J
        twice_h[u, v] = weight
        twice_h[v, u] = -weight
    if twice_h.T != -twice_h:
        raise RuntimeError("2h is not antisymmetric")

    domain_matrix = DomainMatrix.from_Matrix(twice_h)
    charpoly_coefficients = domain_matrix.charpoly()
    coefficients = [domain_matrix.domain.to_sympy(value)
                    for value in charpoly_coefficients]
    charpoly = sp.Poly.from_list(coefficients, gens=z)
    unit, raw_factors = sp.factor_list(charpoly.as_expr())
    if unit != 1 or sum(sp.degree(factor, z) * exponent
                        for factor, exponent in raw_factors) != n:
        raise RuntimeError("bivariate characteristic factorization is incomplete")

    hat_factors: list[tuple[sp.Expr, int]] = []
    for factor, exponent in raw_factors:
        transformed = sp.factor(sp.expand(factor.subs(z, -sp.I * x)))
        # The sole odd factor is z^24 in the full product.  Normalize its
        # individual representative -i*x to x; the discarded phase has
        # twenty-fourth power one and hence does not change the determinant.
        if transformed.has(sp.I):
            transformed = sp.factor(sp.expand(sp.I * transformed))
        if transformed.has(sp.I):
            raise RuntimeError("unexpected complex coefficient after spectral substitution")
        hat_factors.append((transformed, exponent))
    reconstructed = sp.prod(factor ** exponent for factor, exponent in raw_factors)
    if sp.Poly(sp.expand(reconstructed - charpoly.as_expr()), z, J) != 0:
        raise RuntimeError("factor product does not reconstruct det(zI-2h)")

    flat = next(factor for factor, exponent in hat_factors
                if exponent == 13 and sp.expand(factor - (J**2 - x**2)) == 0)
    if sp.expand(flat - (J**2 - x**2)) != 0:
        raise RuntimeError("persistent flat-band factor not found")
    dispersive_z = next(factor for factor, exponent in raw_factors
                        if sp.degree(factor, z) == 8 and exponent == 1)
    dispersive = sp.factor(sp.expand(dispersive_z.subs(z, -sp.I * x)))
    if sp.expand(dispersive.subs(x, J) - (1 - 9 * J**2)) != 0:
        raise RuntimeError("dispersive branch does not meet x=|J| only at J^2=1/9")

    special_J = sp.Rational(1, 3)
    # B=3(2h) at J=+1/3 is integral.  The target x=+/-1/3 is equivalent
    # to the B eigenvalues -/+ i, hence to ker(B^2+I).
    B_plus = sp.zeros(n)
    B_minus = sp.zeros(n)
    for edge, (u, v) in enumerate(augmented_oriented):
        plus_weight = 3 if edge < len(root_edges) else 1
        minus_weight = 3 if edge < len(root_edges) else -1
        B_plus[u, v], B_plus[v, u] = plus_weight, -plus_weight
        B_minus[u, v], B_minus[v, u] = minus_weight, -minus_weight
    pendant_start = len(cliques)
    gauge_entries = [1 if vertex < pendant_start else -1 for vertex in range(n)]
    sign_gauge = sp.diag(*gauge_entries)
    if B_minus != sign_gauge * B_plus * sign_gauge:
        raise RuntimeError("J -> -J pendant-sign gauge failed")

    kernel_matrix = B_plus * B_plus + sp.eye(n)
    kernel_rows = DomainMatrix.from_Matrix(kernel_matrix).to_field().nullspace().to_Matrix()
    integer_kernel_rows = primitive_integer_rows(kernel_rows)
    integer_kernel = sp.Matrix(integer_kernel_rows)
    if integer_kernel.shape != (28, n) or integer_kernel.rank() != 28:
        raise RuntimeError("unexpected exact kernel basis dimension")
    if kernel_matrix * integer_kernel.T != sp.zeros(n, 28):
        raise RuntimeError("stored integer kernel vectors fail exact substitution")
    primes = (1000003, 1000033)
    modular_ranks = {str(prime): matrix_rank_mod_p(kernel_matrix, prime)
                     for prime in primes}
    if set(modular_ranks.values()) != {80}:
        raise RuntimeError(f"modular rank certificate failed: {modular_ranks}")

    scaled_special_coefficients = DomainMatrix.from_Matrix(B_plus).charpoly()
    scaled_domain = DomainMatrix.from_Matrix(B_plus).domain
    scaled_special = sp.Poly.from_list(
        [scaled_domain.to_sympy(value) for value in scaled_special_coefficients], gens=z
    )
    scaled_factors = sp.factor_list(scaled_special.as_expr())[1]
    target_factor = next((factor, exponent) for factor, exponent in scaled_factors
                         if sp.factor(factor - (z**2 + 1)) == 0)
    if target_factor[1] != 14:
        raise RuntimeError("special algebraic multiplicity is not 14 per signed eigenvalue")

    # Build the peg-permutation S3 action, lift each graph automorphism to a
    # signed permutation preserving B, and choose coherent generator phases.
    address_index = {address: index for index, address in enumerate(addresses)}
    clique_index = {tuple(clique): index for index, clique in enumerate(cliques)}
    local_position = {vertex: index for index, vertex in enumerate(local_vertices)}

    def unsigned_vertex_permutation(peg_permutation: tuple[int, int, int]) -> list[int]:
        term_permutation = []
        for address in addresses:
            state = rr.address_to_state(address)
            mapped_state = tuple(peg_permutation[peg] for peg in state)
            term_permutation.append(address_index[rr.state_to_address(mapped_state)])
        vertex_permutation = []
        for clique in cliques:
            mapped = tuple(sorted(term_permutation[term] for term in clique))
            vertex_permutation.append(clique_index[mapped])
        for vertex in local_vertices:
            mapped_vertex = vertex_permutation[vertex]
            vertex_permutation.append(pendant_start + local_position[mapped_vertex])
        if sorted(vertex_permutation) != list(range(n)):
            raise RuntimeError("peg permutation did not lift to augmented root vertices")
        return vertex_permutation

    adjacency = [[] for _ in range(n)]
    for u, v in augmented_edges:
        adjacency[u].append(v)
        adjacency[v].append(u)

    def signed_lift(peg_permutation: tuple[int, int, int]) -> tuple[sp.Matrix, list[int], list[int]]:
        permutation = unsigned_vertex_permutation(peg_permutation)
        signs: list[int | None] = [None] * n
        signs[0] = 1
        queue = [0]
        for u in queue:
            for v in adjacency[u]:
                ratio = int(B_plus[u, v] / B_plus[permutation[u], permutation[v]])
                proposed = int(signs[u]) * ratio
                if signs[v] is None:
                    signs[v] = proposed
                    queue.append(v)
                elif signs[v] != proposed:
                    raise RuntimeError("automorphism has inconsistent edge-orientation gauge")
        if any(sign is None for sign in signs):
            raise RuntimeError("signed-lift propagation did not cover the graph")
        integer_signs = [int(sign) for sign in signs]
        operator = sp.zeros(n)
        for vertex in range(n):
            operator[permutation[vertex], vertex] = integer_signs[vertex]
        if operator.T * B_plus * operator != B_plus:
            raise RuntimeError("signed graph automorphism does not preserve 2h")
        return operator, permutation, integer_signs

    identity, identity_perm, identity_sign = signed_lift((0, 1, 2))
    rotation_raw, rotation_perm, rotation_sign_raw = signed_lift((1, 2, 0))
    reflection, reflection_perm, reflection_sign = signed_lift((0, 2, 1))
    rotation = -rotation_raw  # fixes Q_r^3=+I instead of the projective -I lift
    rotation_sign = [-sign for sign in rotation_sign_raw]
    if identity != sp.eye(n):
        raise RuntimeError("identity lift is not identity")
    if rotation**3 != sp.eye(n) or reflection**2 != sp.eye(n):
        raise RuntimeError("S3 generator orders failed")
    if reflection * rotation * reflection != rotation**2:
        raise RuntimeError("S3 conjugation relation failed")
    if sign_gauge * rotation != rotation * sign_gauge or sign_gauge * reflection != reflection * sign_gauge:
        raise RuntimeError("J-sign gauge does not commute with S3 lift")

    def characters_on_target(integer_B: sp.Matrix) -> tuple[dict[str, int], dict[str, int]]:
        target_kernel = integer_B * integer_B + sp.eye(n)
        basis = DomainMatrix.from_Matrix(target_kernel).to_field().nullspace().to_Matrix().T
        pivot_rows = basis.T.rref()[1]
        pivot_block = basis.extract(pivot_rows, range(basis.cols))
        inverse_pivot = pivot_block.inv()
        B_rep = coordinates_on_columns(integer_B, basis, pivot_rows, inverse_pivot)
        if B_rep * B_rep != -sp.eye(basis.cols):
            raise RuntimeError("target kernel does not carry B^2=-I")
        characters: dict[str, int] = {}
        real_characters: dict[str, int] = {}
        for name, operator in (
            ("identity", identity),
            ("three_cycle", rotation),
            ("reflection", reflection),
        ):
            rep = coordinates_on_columns(operator, basis, pivot_rows, inverse_pivot)
            if operator * basis != basis * rep:
                raise RuntimeError(f"kernel is not invariant under {name}")
            real_trace = sp.trace(rep)
            character = positive_character(rep, B_rep)
            if not real_trace.is_Integer or not character.is_Integer:
                raise RuntimeError("nonintegral finite-group character")
            real_characters[name] = int(real_trace)
            characters[name] = int(character)
        return characters, real_characters

    special_characters, special_real_characters = characters_on_target(B_plus)
    # At the generic rational point J=x=1/2, scale by two: the same target
    # kernel is exactly the persistent 13-fold positive flat band.
    B_flat = sp.zeros(n)
    for edge, (u, v) in enumerate(augmented_oriented):
        weight = 2 if edge < len(root_edges) else 1
        B_flat[u, v], B_flat[v, u] = weight, -weight
    flat_characters, flat_real_characters = characters_on_target(B_flat)
    extra_characters = {name: special_characters[name] - flat_characters[name]
                        for name in special_characters}
    special_irreps = irrep_multiplicities(special_characters)
    flat_irreps = irrep_multiplicities(flat_characters)
    extra_irreps = irrep_multiplicities(extra_characters)
    if (special_irreps, flat_irreps, extra_irreps) != (
        {"A1_trivial": 2, "A2_sign": 4, "E_standard_2d": 4},
        {"A1_trivial": 1, "A2_sign": 4, "E_standard_2d": 4},
        {"A1_trivial": 1, "A2_sign": 0, "E_standard_2d": 0},
    ):
        raise RuntimeError("unexpected symmetry-block decomposition")

    # Exact rational root isolation on both sides of +1/3.  J -> -J is
    # exactly gauge-equivalent, so these intervals simultaneously track the
    # two negative-J Figure-5 branches.
    brackets = (
        (sp.Rational(33, 100), sp.Rational(3320027980036, 10**13),
         sp.Rational(3320027980037, 10**13)),
        (sp.Rational(101, 300), sp.Rational(3346694193990, 10**13),
         sp.Rational(3346694193991, 10**13)),
    )
    tracking = []
    for j_value, lower, upper in brackets:
        polynomial = sp.Poly(dispersive.subs(J, j_value), x, domain=sp.QQ)
        count = int(polynomial.count_roots(lower, upper))
        if count != 1 or not (lower > 0 and upper > lower):
            raise RuntimeError("rational branch-isolation interval failed")
        if upper < j_value:
            ordering = "dispersive_below_flat"
        elif lower > j_value:
            ordering = "dispersive_above_flat"
        else:
            raise RuntimeError("isolated dispersive interval overlaps flat x=J")
        tracking.append({
            "J": rational_text(j_value),
            "mirrored_negative_J": rational_text(-j_value),
            "flat_x_exact": rational_text(j_value),
            "flat_lambda_exact": rational_text(j_value / 2),
            "dispersive_x_interval": [rational_text(lower), rational_text(upper)],
            "dispersive_x_interval_decimal": [float(lower), float(upper)],
            "dispersive_lambda_interval": [rational_text(lower / 2), rational_text(upper / 2)],
            "isolated_root_count": count,
            "ordering": ordering,
            "G_at_flat_x": rational_text(sp.Rational(dispersive.subs({J: j_value, x: j_value}))),
        })

    derivative_J = sp.diff(dispersive, J).subs({J: special_J, x: special_J})
    derivative_x = sp.diff(dispersive, x).subs({J: special_J, x: special_J})
    dispersive_slope = sp.factor(-derivative_J / derivative_x)
    if (derivative_J, derivative_x, dispersive_slope) != (4, -10, sp.Rational(2, 5)):
        raise RuntimeError("unexpected crossing derivatives")

    kernel_payload = {
        "schema_version": 1,
        "matrix": "K=B^2+I_108, B=3(2h_5(1/3)); original signed edges are +/-3 and local pendant edges are +/-1",
        "basis_orientation": "each rational null vector cleared to a primitive integer row with first nonzero entry positive",
        "shape": [28, 108],
        "vectors": integer_kernel_rows,
    }
    KERNEL.write_text(json.dumps(kernel_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = {
        "schema_version": 1,
        "job_id": os.environ.get("PHYSICS_JOB_ID", "phys-00021-p01-research-10e483bf8edf"),
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "sympy_version": sp.__version__,
        },
        "input_binding": {
            "generator": "evidence/reproduce_sierpinski_hanoi.py",
            "generator_sha256": sha256(GENERATOR),
            "source_sha256": sha256(PROJECT / "source.md"),
            "depth_k": 5,
            "sector": "all 13 canonical cycle generators projected to +1",
            "root_vertices": len(cliques),
            "root_edges": len(root_edges),
            "local_pendant_edges": len(local_vertices),
            "augmented_dimension": n,
        },
        "normalization": {
            "symbolic_matrix": "A(J)=2h_5(J), real antisymmetric",
            "characteristic_polynomial_computed": "det(z I-A(J)) over ZZ[J,z]",
            "physical_spectral_polynomial": "P_hat_5(x,J)=det(x I-iA(J))=det(x I-2ih_5(J))",
            "source_plot": "lambda=|x|/2",
        },
        "exact_bivariate_factorization": {
            "degree": int(charpoly.degree()),
            "term_count_before_factoring": len(charpoly.terms()),
            "det_zI_minus_A_factors": [
                {"factor": sp.sstr(factor), "exponent": int(exponent)}
                for factor, exponent in raw_factors
            ],
            "P_hat_factors": [
                {"factor": sp.sstr(factor), "exponent": int(exponent)}
                for factor, exponent in hat_factors
            ],
            "persistent_flat_factor": "(J^2-x^2)^13",
            "dispersive_factor": sp.sstr(dispersive),
            "dispersive_on_flat_locus": sp.sstr(sp.factor(dispersive.subs(x, J))),
        },
        "special_point_certificate": {
            "points": [
                {"J": "1/3", "x": "1/3", "lambda": "1/6"},
                {"J": "-1/3", "x": "1/3", "lambda": "1/6"},
            ],
            "J_sign_equivalence": "B(-1/3)=D B(1/3) D, D=+1 on 69 root modes and -1 on 39 pendant modes",
            "scaled_characteristic_factors_at_J_plus_1_over_3": [
                {"factor": sp.sstr(factor), "exponent": int(exponent)}
                for factor, exponent in scaled_factors
            ],
            "target_scaled_factor": "(z^2+1)^14",
            "algebraic_multiplicity_of_each_x_sign": 14,
            "geometric_multiplicity_of_each_x_sign": 14,
            "combined_kernel": "ker(B^2+I)",
            "combined_kernel_dimension": 28,
            "combined_kernel_modular_ranks": modular_ranks,
            "kernel_basis_file": "evidence/exact-k5-kernel-basis.json",
            "kernel_basis_sha256": sha256(KERNEL),
            "hermiticity_reason": "iA(J) is Hermitian for real J, so algebraic and geometric multiplicities agree and no exceptional point is possible",
        },
        "symmetry_blocks": {
            "group": "S3 peg permutations with signed orientation-gauge lifts",
            "lift_convention": "r=(0 1 2) is globally signed so Q_r^3=I; s=(1 2) has root-mode-0 sign +1; Q_s Q_r Q_s=Q_r^2",
            "relations_exact": True,
            "J_sign_gauge_commutes_with_lift": True,
            "generator_signed_permutations": {
                "rotation": [[rotation_perm[index], rotation_sign[index]] for index in range(n)],
                "reflection": [[reflection_perm[index], reflection_sign[index]] for index in range(n)],
            },
            "special_positive_eigenspace_characters": special_characters,
            "special_real_combined_kernel_characters": special_real_characters,
            "special_positive_eigenspace_irreps": special_irreps,
            "generic_flat_positive_band_characters_at_J_half": flat_characters,
            "generic_flat_real_combined_kernel_characters_at_J_half": flat_real_characters,
            "generic_flat_positive_band_irreps": flat_irreps,
            "extra_dispersive_branch_characters": extra_characters,
            "extra_dispersive_branch_irreps": extra_irreps,
            "interpretation": "the 14-fold point is a transverse meeting of a 13-fold flat band with one additional A1 singlet; the flat band already contains one A1 singlet, so the meeting is within the same one-dimensional symmetry block, not a distinct-irrep protected crossing",
            "reflection_lift_note": "multiplying every reflection lift by -1 swaps the names A1 and A2 but leaves all dimensions and the same-irrep conclusion unchanged",
        },
        "rational_branch_tracking": tracking,
        "transversality": {
            "at_J_x_plus_one_third": {
                "partial_G_partial_J": rational_text(sp.Rational(derivative_J)),
                "partial_G_partial_x": rational_text(sp.Rational(derivative_x)),
                "dispersive_dx_dJ": rational_text(sp.Rational(dispersive_slope)),
                "flat_dx_dJ": "1",
                "first_order_x_separation_coefficient": "3/5",
                "first_order_lambda_separation_coefficient": "3/10",
            },
            "negative_point": "by exact J-sign gauge, slopes are -2/5 (dispersive) and -1 (positive flat branch)",
        },
        "scope": {
            "established": "both k=5 Figure-5 landmarks are exact finite-size crossings at J=+/-1/3 and lambda=1/6 in the reconstructed all-cycle-+1 sector",
            "not_established": "no claim for k other than 5, other cycle sectors, a many-body physical-parity gap, a boundary recursion, thermodynamic scaling, or literature novelty",
        },
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "pass",
        "result": str(RESULT.relative_to(PROJECT)),
        "kernel": str(KERNEL.relative_to(PROJECT)),
        "source_sha256": result["input_binding"]["source_sha256"],
        "flat_factor": result["exact_bivariate_factorization"]["persistent_flat_factor"],
        "special_multiplicity": result["special_point_certificate"]["algebraic_multiplicity_of_each_x_sign"],
        "special_irreps": special_irreps,
        "flat_irreps": flat_irreps,
        "extra_irreps": extra_irreps,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
