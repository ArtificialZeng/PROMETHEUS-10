#!/usr/bin/env python3
"""Interval certificate for the pointwise full second variation at a=1/2.

The restricted KKT root is first enclosed by interval Newton using
``research_interval_kkt``.  It is then mapped exactly (with Arb balls) to the
traceless one-jump coordinates

    L(rho) = -i[h.sigma,rho] + D[(u+i v).sigma](rho).

In the real affine Bloch representation the generator is polynomial in
(h,u,v), which permits outward-rounded first and second generator
derivatives.  Block matrix exponentials enclose the first and second Frechet
derivatives of exp(L).  Positivity on the fixed-a, gauge-quotiented tangent
space is certified by adding penalties for the three constraint normals and
proving positive definiteness of the penalized interval matrix after a fixed,
certifiably invertible congruence.  The transverse added-jump form is handled
in the same way after removing its two real jump-mixing directions.

The result is a pointwise second-order certificate at the enclosed KKT root.
It is not an explicit finite-radius nonlinear neighborhood, a global minimum,
an unbounded-tail bound, or a characterization of the Q2 boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parent))
import research_interval_kkt as ikkt  # noqa: E402

from flint import arb, arb_mat, ctx  # noqa: E402


EXPECTED_SOURCE_SHA256 = ikkt.EXPECTED_SOURCE_SHA256
COORDINATE_ORDER = (
    "h_x",
    "h_y",
    "h_z",
    "Re_z_x",
    "Re_z_y",
    "Re_z_z",
    "Im_z_x",
    "Im_z_y",
    "Im_z_z",
)
SLICE_COORDINATE_INDICES = (0, 1, 2, 4, 5, 6, 7)
SLICE_VARIABLE_ORDER = tuple(COORDINATE_ORDER[index] for index in SLICE_COORDINATE_INDICES) + (
    "lambda",
)


def arb_sum(values) -> arb:
    result = arb(0)
    for value in values:
        result += value
    return result


def cross(left: list[arb], right: list[arb]) -> list[arb]:
    return [
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    ]


def basis_vector(index: int) -> list[arb]:
    return [arb(1 if component == index else 0) for component in range(3)]


def normalized(vector: list[arb]) -> list[arb]:
    norm = arb_sum(value * value for value in vector).sqrt()
    if norm.contains(arb(0)):
        raise ZeroDivisionError("constraint normal could contain zero norm")
    return [value / norm for value in vector]


def outer_vector(left: list[arb], right: list[arb]) -> arb_mat:
    result = arb_mat(len(left), len(right))
    for row, lvalue in enumerate(left):
        for col, rvalue in enumerate(right):
            result[row, col] = lvalue * rvalue
    return result


def certified_root_enclosure(center_strings: list[str], radius: str) -> tuple[list[arb], list[bool]]:
    center = [arb(value) for value in center_strings]
    box = [arb(f"{value} +/- {radius}") for value in center_strings]
    function_center, _ = ikkt.kkt_function_and_jacobian(center)
    _, jacobian_box = ikkt.kkt_function_and_jacobian(box)
    image = ikkt.column(center) - jacobian_box.inv() * ikkt.column(function_center)
    inclusion = [box[index].contains_interior(image[index, 0]) for index in range(5)]
    if not all(inclusion):
        raise RuntimeError("interval-Newton root enclosure did not lie in the interior")
    return [image[index, 0] for index in range(5)], inclusion


def restricted_to_traceless(root: list[arb]) -> list[arb]:
    time, gamma, alpha, beta, _ = root
    q = (time * gamma).sqrt()
    difference = alpha - beta
    total = alpha + beta
    h_x = time - time * gamma * (arb(2) * difference).sin() / 8
    u = [arb(0), q * total.sin() / 2, q * total.cos() / 2]
    v = [q * difference.sin() / 2, arb(0), arb(0)]
    return [h_x, arb(0), arb(0)] + u + v


def affine_generator(h: list[arb], u: list[arb], v: list[arb]) -> arb_mat:
    result = arb_mat(4, 4)
    norm_squared = arb_sum(value * value for value in u + v)
    for row in range(3):
        for col in range(3):
            result[row, col] = 2 * (u[row] * u[col] + v[row] * v[col])
            if row == col:
                result[row, col] -= 2 * norm_squared
    # 2 h cross r
    result[0, 1] -= 2 * h[2]
    result[0, 2] += 2 * h[1]
    result[1, 0] += 2 * h[2]
    result[1, 2] -= 2 * h[0]
    result[2, 0] -= 2 * h[1]
    result[2, 1] += 2 * h[0]
    translation = cross(u, v)
    for row in range(3):
        result[row, 3] = 4 * translation[row]
    return result


def general_generator_derivatives(coordinate: list[arb]) -> tuple[arb_mat, list[arb_mat], list[list[arb_mat]]]:
    h, u, v = coordinate[:3], coordinate[3:6], coordinate[6:9]
    generator = affine_generator(h, u, v)
    first: list[arb_mat] = []
    for coordinate_index in range(9):
        direction = arb_mat(4, 4)
        if coordinate_index < 3:
            e = basis_vector(coordinate_index)
            direction[0, 1] -= 2 * e[2]
            direction[0, 2] += 2 * e[1]
            direction[1, 0] += 2 * e[2]
            direction[1, 2] -= 2 * e[0]
            direction[2, 0] -= 2 * e[1]
            direction[2, 1] += 2 * e[0]
        else:
            is_u = coordinate_index < 6
            local_index = coordinate_index - (3 if is_u else 6)
            base = u if is_u else v
            other = v if is_u else u
            e = basis_vector(local_index)
            for row in range(3):
                for col in range(3):
                    direction[row, col] = 2 * (
                        e[row] * base[col] + base[row] * e[col]
                    )
                    if row == col:
                        direction[row, col] -= 4 * base[local_index]
            translation = cross(e, other) if is_u else cross(other, e)
            for row in range(3):
                direction[row, 3] = 4 * translation[row]
        first.append(direction)

    second = [[arb_mat(4, 4) for _ in range(9)] for _ in range(9)]
    for first_index in range(3, 9):
        for second_index in range(first_index, 9):
            first_is_u = first_index < 6
            second_is_u = second_index < 6
            first_local = first_index - (3 if first_is_u else 6)
            second_local = second_index - (3 if second_is_u else 6)
            direction = arb_mat(4, 4)
            if first_is_u == second_is_u:
                ei, ej = basis_vector(first_local), basis_vector(second_local)
                for row in range(3):
                    for col in range(3):
                        direction[row, col] = 2 * (
                            ei[row] * ej[col] + ej[row] * ei[col]
                        )
                        if row == col and first_local == second_local:
                            direction[row, col] -= 4
            else:
                u_index = first_local if first_is_u else second_local
                v_index = second_local if first_is_u else first_local
                translation = cross(basis_vector(u_index), basis_vector(v_index))
                for row in range(3):
                    direction[row, 3] = 4 * translation[row]
            second[first_index][second_index] = direction
            second[second_index][first_index] = direction
    return generator, first, second


def differential_observable(matrix: arb_mat, support_lambda: arb) -> arb:
    da = (matrix[2, 2] + matrix[2, 3]) / 2
    db = (matrix[2, 2] - matrix[2, 3]) / 2
    return db - support_lambda * da


def a_differential(matrix: arb_mat) -> arb:
    return (matrix[2, 2] + matrix[2, 3]) / 2


def full_hessian(root: list[arb], coordinate: list[arb]) -> tuple[list[arb], list[arb], arb_mat, arb_mat]:
    support_lambda = root[4]
    generator, first, second = general_generator_derivatives(coordinate)
    gradient_a: list[arb] = []
    gradient_f: list[arb] = []
    for direction in first:
        derivative = ikkt.block_frechet(generator, direction)
        gradient_a.append(a_differential(derivative))
        gradient_f.append(differential_observable(derivative, support_lambda))

    hessian = arb_mat(9, 9)
    for row in range(9):
        for col in range(row, 9):
            derivative = ikkt.second_frechet(generator, first[row], first[col])
            derivative += ikkt.block_frechet(generator, second[row][col])
            value = differential_observable(derivative, support_lambda)
            hessian[row, col] = value
            hessian[col, row] = value
    return gradient_a, gradient_f, hessian, generator


def channel_a(generator: arb_mat) -> arb:
    channel = generator.exp()
    return (arb(1) + channel[2, 2] + channel[2, 3]) / 2


def slice_to_coordinate(slice_variables: list[arb]) -> list[arb]:
    """Gauge slice Re(z_x)=Im(z_z)=0, transverse near the reference root."""
    coordinate = [arb(0) for _ in range(9)]
    for local_index, full_index in enumerate(SLICE_COORDINATE_INDICES):
        coordinate[full_index] = slice_variables[local_index]
    return coordinate


def full_slice_kkt_function_and_jacobian(slice_variables: list[arb]) -> tuple[list[arb], arb_mat]:
    coordinate = slice_to_coordinate(slice_variables)
    support_lambda = slice_variables[-1]
    root_stub = [arb(0), arb(0), arb(0), arb(0), support_lambda]
    gradient_a, gradient_f, hessian, generator = full_hessian(root_stub, coordinate)
    function = [channel_a(generator) - arb("0.5")]
    function.extend(gradient_f[index] for index in SLICE_COORDINATE_INDICES)
    jacobian = arb_mat(8, 8)
    for col, full_col in enumerate(SLICE_COORDINATE_INDICES):
        jacobian[0, col] = gradient_a[full_col]
    for row, full_row in enumerate(SLICE_COORDINATE_INDICES):
        for col, full_col in enumerate(SLICE_COORDINATE_INDICES):
            jacobian[row + 1, col] = hessian[full_row, full_col]
        jacobian[row + 1, 7] = -gradient_a[full_row]
    return function, jacobian


def full_slice_center(restricted_center: list[arb]) -> list[arb]:
    coordinate = restricted_to_traceless(restricted_center)
    return [coordinate[index] for index in SLICE_COORDINATE_INDICES] + [restricted_center[4]]


def full_slice_root_enclosure(center_values: list[arb], radius: str) -> tuple[list[arb], list[bool], list[arb]]:
    centers = [arb(str(value.mid())) for value in center_values]
    radius_ball = arb(f"0 +/- {radius}")
    box = [value + radius_ball for value in centers]
    function_center, _ = full_slice_kkt_function_and_jacobian(centers)
    _, jacobian_box = full_slice_kkt_function_and_jacobian(box)
    image = ikkt.column(centers) - jacobian_box.inv() * ikkt.column(function_center)
    inclusion = [box[index].contains_interior(image[index, 0]) for index in range(8)]
    if not all(inclusion):
        raise RuntimeError(
            "full gauge-slice interval-Newton image did not lie in the interior: "
            + str(inclusion)
        )
    return [image[index, 0] for index in range(8)], inclusion, function_center


def midpoint_numpy(matrix: arb_mat) -> np.ndarray:
    return np.array(
        [
            [float(matrix[row, col].mid()) for col in range(matrix.ncols())]
            for row in range(matrix.nrows())
        ],
        dtype=float,
    )


def arb_from_numpy(matrix: np.ndarray) -> arb_mat:
    result = arb_mat(*matrix.shape)
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            result[row, col] = arb(repr(float(matrix[row, col])))
    return result


def congruence(matrix: arb_mat, transform: arb_mat) -> arb_mat:
    return transform.transpose() * matrix * transform


def positive_definiteness_certificate(matrix: arb_mat) -> dict:
    midpoint = midpoint_numpy(matrix)
    midpoint = (midpoint + midpoint.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(midpoint)
    transform = arb_from_numpy(eigenvectors)
    determinant = transform.det()
    transformed = congruence(matrix, transform)
    margins: list[arb] = []
    for row in range(matrix.nrows()):
        off_diagonal = arb_sum(
            abs(transformed[row, col])
            for col in range(matrix.ncols())
            if col != row
        )
        margins.append(transformed[row, row] - off_diagonal)
    return {
        "midpoint_eigenvalues": eigenvalues.tolist(),
        "transform_determinant": ikkt.ball_record(determinant),
        "transform_certifiably_invertible": not determinant.contains(arb(0)),
        "gershgorin_margin_balls": [ikkt.ball_record(value) for value in margins],
        "all_gershgorin_margins_strictly_positive": all(value > 0 for value in margins),
        "transformed_matrix": ikkt.matrix_records(transformed),
    }


def rank_one_penalty_certificate(
    coordinate: list[arb], gradient_a: list[arb], hessian: arb_mat
) -> tuple[arb_mat, dict, dict]:
    h, u, v = coordinate[:3], coordinate[3:6], coordinate[6:9]
    phase = [arb(0)] * 3 + [-value for value in v] + list(u)
    basis_complex_u = [-u[1], u[0], arb(0)]
    basis_complex_v = [-v[1], v[0], arb(0)]
    basis = [-h[1], h[0], arb(0)] + basis_complex_u + basis_complex_v
    normals = [normalized(phase), normalized(basis), normalized(gradient_a)]
    penalized = hessian
    for normal in normals:
        penalized = penalized + outer_vector(normal, normal)
    certificate = positive_definiteness_certificate(penalized)
    constraints = {
        "jump_phase_normal": [ikkt.ball_record(value) for value in phase],
        "fixed_basis_rephasing_normal": [ikkt.ball_record(value) for value in basis],
        "fixed_a_normal": [ikkt.ball_record(value) for value in gradient_a],
        "penalty": "sum of unit-normal outer products with coefficient 1",
    }
    return penalized, certificate, constraints


def added_jump_generator(real_part: list[arb], imag_part: list[arb]) -> arb_mat:
    return affine_generator([arb(0), arb(0), arb(0)], real_part, imag_part)


def transverse_q_certificate(
    root: list[arb], coordinate: list[arb], generator: arb_mat
) -> tuple[arb_mat, arb_mat, dict, dict]:
    support_lambda = root[4]

    def response(real_part: list[arb], imag_part: list[arb]) -> arb:
        direction = added_jump_generator(real_part, imag_part)
        derivative = ikkt.block_frechet(generator, direction)
        return differential_observable(derivative, support_lambda)

    zero = [arb(0), arb(0), arb(0)]
    q_real = arb_mat(3, 3)
    q_imag = arb_mat(3, 3)
    diagonal = [response(basis_vector(index), zero) for index in range(3)]
    for index, value in enumerate(diagonal):
        q_real[index, index] = value
    for row in range(3):
        for col in range(row + 1, 3):
            plus = [basis_vector(row)[i] + basis_vector(col)[i] for i in range(3)]
            real_part = (response(plus, zero) - diagonal[row] - diagonal[col]) / 2
            imag_part = (
                diagonal[row]
                + diagonal[col]
                - response(basis_vector(row), basis_vector(col))
            ) / 2
            q_real[row, col] = real_part
            q_real[col, row] = real_part
            q_imag[row, col] = imag_part
            q_imag[col, row] = -imag_part

    realification = arb_mat(6, 6)
    for row in range(3):
        for col in range(3):
            realification[row, col] = q_real[row, col]
            realification[row, col + 3] = -q_imag[row, col]
            realification[row + 3, col] = q_imag[row, col]
            realification[row + 3, col + 3] = q_real[row, col]

    u, v = coordinate[3:6], coordinate[6:9]
    mixing_real = list(u) + list(v)
    mixing_imag = [-value for value in v] + list(u)
    normals = [normalized(mixing_real), normalized(mixing_imag)]
    penalized = realification
    for normal in normals:
        penalized = penalized + outer_vector(normal, normal)
    certificate = positive_definiteness_certificate(penalized)
    constraints = {
        "real_part_z_dagger_v_normal": [ikkt.ball_record(value) for value in mixing_real],
        "imag_part_z_dagger_v_normal": [ikkt.ball_record(value) for value in mixing_imag],
        "penalty": "sum of unit-normal outer products with coefficient 1",
    }
    return realification, penalized, certificate, constraints


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--precision", type=int, default=256)
    parser.add_argument("--root-radius", default="1e-3")
    parser.add_argument("--full-root-radius", default="1e-4")
    args = parser.parse_args()

    ctx.prec = args.precision
    source_path = Path("source.md")
    source_hash_before = hashlib.sha256(source_path.read_bytes()).hexdigest()
    center_strings = ikkt.load_center()
    restricted_root, root_inclusion = certified_root_enclosure(center_strings, args.root_radius)
    slice_center = full_slice_center([arb(value) for value in center_strings])
    full_root, full_root_inclusion, full_center_residual = full_slice_root_enclosure(
        slice_center, args.full_root_radius
    )
    coordinate = slice_to_coordinate(full_root)
    root = [arb(0), arb(0), arb(0), arb(0), full_root[-1]]
    gradient_a, gradient_f, hessian, generator = full_hessian(root, coordinate)
    penalized_hessian, rank_one_certificate, rank_one_constraints = rank_one_penalty_certificate(
        coordinate, gradient_a, hessian
    )
    q_realification, q_penalized, q_certificate, q_constraints = transverse_q_certificate(
        root, coordinate, generator
    )
    source_hash_after = hashlib.sha256(source_path.read_bytes()).hexdigest()

    gradient_stationary_consistency = all(value.contains(arb(0)) for value in gradient_f)
    h, u, v = coordinate[:3], coordinate[3:6], coordinate[6:9]
    # On the chosen slice the omitted coordinates are Re(z_x) and Im(z_z).
    # The two exact gauge tangents have determinant u_y*u_z in those columns.
    gauge_slice_transversality = u[1] * u[2]
    full_stationarity_certified = all(full_root_inclusion) and not gauge_slice_transversality.contains(arb(0))
    rank_one_certified = (
        rank_one_certificate["transform_certifiably_invertible"]
        and rank_one_certificate["all_gershgorin_margins_strictly_positive"]
    )
    transverse_certified = (
        q_certificate["transform_certifiably_invertible"]
        and q_certificate["all_gershgorin_margins_strictly_positive"]
    )

    data = {
        "job_id": "phys-00002-p01-research-efbcc56428da",
        "method": "Arb interval Newton plus interval Frechet block exponentials in a real affine-Bloch representation",
        "precision_bits": args.precision,
        "root_source_box_radius": args.root_radius,
        "full_gauge_slice_source_box_radius": args.full_root_radius,
        "source_sha256_before": source_hash_before,
        "source_sha256_after": source_hash_after,
        "source_immutable_check": source_hash_before == source_hash_after == EXPECTED_SOURCE_SHA256,
        "restricted_kkt_root": {
            "parameter_order": list(ikkt.PARAMETER_ORDER),
            "interval_newton_interior_by_coordinate": root_inclusion,
            "enclosure": [ikkt.ball_record(value) for value in restricted_root],
            "existence_and_uniqueness_certified_in_source_box": all(root_inclusion),
        },
        "full_rank_one_kkt_root": {
            "gauge_slice": "Re(z_x)=0 and Im(z_z)=0",
            "variable_order": list(SLICE_VARIABLE_ORDER),
            "interval_newton_interior_by_coordinate": full_root_inclusion,
            "center_function_balls": [ikkt.ball_record(value) for value in full_center_residual],
            "enclosure": [ikkt.ball_record(value) for value in full_root],
            "existence_and_uniqueness_certified_in_source_box": all(full_root_inclusion),
            "gauge_slice_transversality_determinant": ikkt.ball_record(gauge_slice_transversality),
            "gauge_slice_transversality_certified": not gauge_slice_transversality.contains(arb(0)),
            "full_stationarity_logic": (
                "The interval root sets a=1/2 and all seven slice derivatives of "
                "b-lambda*a to zero. Both observables are exactly invariant under jump "
                "phase and fixed-basis rephasing. The two gauge tangents are transverse "
                "to the slice because their omitted-coordinate determinant u_y*u_z "
                "excludes zero, so slice plus gauge directions span all nine one-jump "
                "directions."
            ),
            "full_stationarity_certified": full_stationarity_certified,
        },
        "traceless_coordinates": {
            "coordinate_order": list(COORDINATE_ORDER),
            "enclosure": [ikkt.ball_record(value) for value in coordinate],
        },
        "rank_one_second_variation": {
            "functional": "F=b-lambda*a",
            "gradient_f_balls": [ikkt.ball_record(value) for value in gradient_f],
            "all_gradient_component_enclosures_contain_zero_consistency_check": gradient_stationary_consistency,
            "hessian_balls": ikkt.matrix_records(hessian),
            "constraint_normals": rank_one_constraints,
            "penalized_hessian_balls": ikkt.matrix_records(penalized_hessian),
            "positive_definiteness_certificate": rank_one_certificate,
            "fixed_a_gauge_quotient_hessian_positive_certified": rank_one_certified,
            "logic": (
                "The added unit-normal penalties vanish on the simultaneous kernel of the "
                "jump-phase, fixed-basis-rephasing, and fixed-a normals. Positive definiteness "
                "of the penalized matrix therefore certifies positivity of the original "
                "Hessian on that tangent space."
            ),
        },
        "transverse_added_jump": {
            "realification_coordinate_order": [
                "Re_v_x", "Re_v_y", "Re_v_z", "Im_v_x", "Im_v_y", "Im_v_z"
            ],
            "q_realification_balls": ikkt.matrix_records(q_realification),
            "constraint_normals": q_constraints,
            "penalized_q_balls": ikkt.matrix_records(q_penalized),
            "positive_definiteness_certificate": q_certificate,
            "transverse_q_positive_certified": transverse_certified,
            "logic": (
                "The two penalties vanish when z^dagger v=0. Positive definiteness of the "
                "penalized realification therefore certifies positivity of v^dagger Q v "
                "on the complex transverse subspace; jump mixing is excluded."
            ),
        },
        "status": {
            "restricted_kkt_root_certified": all(root_inclusion),
            "full_rank_one_kkt_root_certified": all(full_root_inclusion),
            "full_rank_one_stationarity_certified": full_stationarity_certified,
            "full_gradient_enclosures_contain_zero_consistency_check": gradient_stationary_consistency,
            "fixed_a_gauge_quotient_hessian_positive_certified": rank_one_certified,
            "transverse_added_jump_q_positive_certified": transverse_certified,
            "pointwise_combined_second_variation_certified": (
                all(root_inclusion)
                and full_stationarity_certified
                and rank_one_certified
                and transverse_certified
            ),
            "explicit_finite_radius_nonlinear_neighborhood_certified": False,
            "global_restricted_minimum_certified": False,
            "unbounded_tail_certified": False,
            "q2_boundary_certified": False,
            "candidate": False,
            "original_boundary_question": "unresolved",
        },
        "limitations": (
            "This is a pointwise second-order sufficient-condition certificate at one exact "
            "restricted KKT root. It does not provide an explicit nonlinear neighborhood "
            "radius, exclude distant or unbounded generators, prove the restricted point is "
            "globally minimizing, or identify the true boundary of Q2."
        ),
    }
    Path(args.json).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    rank_margins = rank_one_certificate["gershgorin_margin_balls"]
    q_margins = q_certificate["gershgorin_margin_balls"]
    log_lines = [
        f"source immutable: {data['source_immutable_check']}",
        f"Arb precision bits: {args.precision}",
        f"restricted KKT interval-Newton inclusion: {root_inclusion}",
        f"full gauge-slice KKT interval-Newton inclusion: {full_root_inclusion}",
        f"gauge-slice transversality determinant: {gauge_slice_transversality}",
        f"full one-jump stationarity certified: {full_stationarity_certified}",
        f"full F-gradient components contain zero (consistency only): {gradient_stationary_consistency}",
        "rank-one penalized congruence Gershgorin margins: "
        + " | ".join(item["ball"] for item in rank_margins),
        f"rank-one fixed-a gauge-quotient positivity certified: {rank_one_certified}",
        "transverse-Q penalized congruence Gershgorin margins: "
        + " | ".join(item["ball"] for item in q_margins),
        f"transverse added-jump positivity certified: {transverse_certified}",
        "SCIENCE STATUS: pointwise combined second variation at the enclosed root only.",
        "NOT CERTIFIED: explicit nonlinear neighborhood radius, global minimum, unbounded tails, or Q2 boundary.",
    ]
    Path(args.log).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(json.dumps({"json": args.json, "log": args.log, "status": data["status"]}, indent=2))


if __name__ == "__main__":
    main()
