#!/usr/bin/env python3
"""Outward-rounded interval-Newton test for the restricted five-equation KKT root.

The Appendix-A family is evaluated in the independently derived real affine
Bloch representation.  All interval operations, including matrix
exponentials, use python-flint/Arb balls.  First and second parameter
derivatives of exp(A) are obtained from block exponentials, so the interval
Jacobian of the KKT system contains the full nonlinear dependence on
(t, gamma, alpha, beta, lambda).

This script certifies only existence and uniqueness of the restricted KKT
root inside a stated box when the interval-Newton inclusion succeeds.  It
does not by itself certify the arbitrary-one-jump constrained Hessian, the
added-jump cone, a boundary value, or any global/unbounded statement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ARB_PATH = "standard Python environment (python-flint)"

import flint  # noqa: E402
from flint import arb, arb_mat, ctx  # noqa: E402


EXPECTED_SOURCE_SHA256 = "7bfa09317b0b519a4be6488e9e980431f7cdd49e11fe6adf216f9b9d32dccfc8"
TARGET_A = arb("0.5")
PARAMETER_ORDER = ("t", "gamma", "alpha", "beta", "lambda")
TEST_RADII = ("1e-2", "3e-3", "1e-3", "3e-4", "1e-4", "1e-6", "1e-10", "1e-20", "1e-30", "1e-40")


def zero_matrix(rows: int, columns: int) -> arb_mat:
    return arb_mat(rows, columns)


def column(values: list[arb]) -> arb_mat:
    result = arb_mat(len(values), 1)
    for index, value in enumerate(values):
        result[index, 0] = value
    return result


def outer(left: list[arb], right: list[arb]) -> arb_mat:
    result = zero_matrix(len(left), len(right))
    for row, lvalue in enumerate(left):
        for col, rvalue in enumerate(right):
            result[row, col] = lvalue * rvalue
    return result


def vector_add(left: list[arb], right: list[arb], scale: arb = arb(1)) -> list[arb]:
    return [lvalue + scale * rvalue for lvalue, rvalue in zip(left, right)]


def d0_matrix(no: list[arb], ni: list[arb], offset_sign: arb = arb(1)) -> arb_mat:
    """Return D0 with linear block no ni^T and affine column no-sign*ni.

    The caller subtracts I from the top-left block only for the undifferentiated
    D0.  ``offset_sign`` is retained to make the beta derivatives explicit.
    """
    result = zero_matrix(4, 4)
    product = outer(no, ni)
    for row in range(3):
        for col in range(3):
            result[row, col] = product[row, col]
        result[row, 3] = no[row] - offset_sign * ni[row]
    return result


def affine_generator_derivatives(params: list[arb]) -> tuple[arb_mat, list[arb_mat], list[list[arb_mat]]]:
    """Return A, A_i and A_ij for x=(t,gamma,alpha,beta)."""
    time, gamma, alpha, beta = params
    two = arb(2)
    half = arb("0.5")

    sa, ca = (two * alpha).sin(), (two * alpha).cos()
    sb, cb = (two * beta).sin(), (two * beta).cos()
    no = [arb(0), sa, ca]
    ni = [arb(0), sb, cb]
    noa = [arb(0), two * ca, -two * sa]
    nib = [arb(0), two * cb, -two * sb]
    noaa = [arb(0), -arb(4) * sa, -arb(4) * ca]
    nibb = [arb(0), -arb(4) * sb, -arb(4) * cb]

    d0 = d0_matrix(no, ni)
    for index in range(3):
        d0[index, index] -= 1

    d0a = zero_matrix(4, 4)
    block = outer(noa, ni)
    for row in range(3):
        for col in range(3):
            d0a[row, col] = block[row, col]
        d0a[row, 3] = noa[row]

    d0b = zero_matrix(4, 4)
    block = outer(no, nib)
    for row in range(3):
        for col in range(3):
            d0b[row, col] = block[row, col]
        d0b[row, 3] = -nib[row]

    d0aa = zero_matrix(4, 4)
    block = outer(noaa, ni)
    for row in range(3):
        for col in range(3):
            d0aa[row, col] = block[row, col]
        d0aa[row, 3] = noaa[row]

    d0ab = zero_matrix(4, 4)
    block = outer(noa, nib)
    for row in range(3):
        for col in range(3):
            d0ab[row, col] = block[row, col]

    d0bb = zero_matrix(4, 4)
    block = outer(no, nibb)
    for row in range(3):
        for col in range(3):
            d0bb[row, col] = block[row, col]
        d0bb[row, 3] = -nibb[row]

    ham = zero_matrix(4, 4)
    ham[1, 2] = -2
    ham[2, 1] = 2
    base = ham + (gamma * half) * d0
    generator = time * base

    first = [
        base,
        (time * half) * d0,
        (time * gamma * half) * d0a,
        (time * gamma * half) * d0b,
    ]
    second = [[zero_matrix(4, 4) for _ in range(4)] for _ in range(4)]

    def set_symmetric(i: int, j: int, value: arb_mat) -> None:
        second[i][j] = value
        second[j][i] = value

    set_symmetric(0, 1, half * d0)
    set_symmetric(0, 2, (gamma * half) * d0a)
    set_symmetric(0, 3, (gamma * half) * d0b)
    set_symmetric(1, 2, (time * half) * d0a)
    set_symmetric(1, 3, (time * half) * d0b)
    set_symmetric(2, 2, (time * gamma * half) * d0aa)
    set_symmetric(2, 3, (time * gamma * half) * d0ab)
    set_symmetric(3, 3, (time * gamma * half) * d0bb)
    return generator, first, second


def block_frechet(generator: arb_mat, direction: arb_mat) -> arb_mat:
    dimension = generator.nrows()
    block = zero_matrix(2 * dimension, 2 * dimension)
    for row in range(dimension):
        for col in range(dimension):
            block[row, col] = generator[row, col]
            block[row + dimension, col + dimension] = generator[row, col]
            block[row, col + dimension] = direction[row, col]
    exponential = block.exp()
    result = zero_matrix(dimension, dimension)
    for row in range(dimension):
        for col in range(dimension):
            result[row, col] = exponential[row, col + dimension]
    return result


def ordered_second(generator: arb_mat, left: arb_mat, right: arb_mat) -> arb_mat:
    dimension = generator.nrows()
    block = zero_matrix(3 * dimension, 3 * dimension)
    for row in range(dimension):
        for col in range(dimension):
            block[row, col] = generator[row, col]
            block[row + dimension, col + dimension] = generator[row, col]
            block[row + 2 * dimension, col + 2 * dimension] = generator[row, col]
            block[row, col + dimension] = left[row, col]
            block[row + dimension, col + 2 * dimension] = right[row, col]
    exponential = block.exp()
    result = zero_matrix(dimension, dimension)
    for row in range(dimension):
        for col in range(dimension):
            result[row, col] = exponential[row, col + 2 * dimension]
    return result


def second_frechet(generator: arb_mat, left: arb_mat, right: arb_mat) -> arb_mat:
    return ordered_second(generator, left, right) + ordered_second(generator, right, left)


def channel_observables(matrix: arb_mat) -> tuple[arb, arb]:
    mzz, vz = matrix[2, 2], matrix[2, 3]
    return (arb(1) + mzz + vz) / 2, (arb(1) + mzz - vz) / 2


def differential_observables(matrix: arb_mat) -> tuple[arb, arb]:
    """Observable map for a channel derivative (there is no derivative of 1)."""
    mzz, vz = matrix[2, 2], matrix[2, 3]
    return (mzz + vz) / 2, (mzz - vz) / 2


def kkt_function_and_jacobian(all_params: list[arb]) -> tuple[list[arb], arb_mat]:
    generator, generator_first, generator_second = affine_generator_derivatives(all_params[:4])
    channel = generator.exp()
    aval, _ = channel_observables(channel)

    first_observables: list[tuple[arb, arb]] = []
    for direction in generator_first:
        first_observables.append(differential_observables(block_frechet(generator, direction)))

    second_observables: list[list[tuple[arb, arb]]] = [
        [(arb(0), arb(0)) for _ in range(4)] for _ in range(4)
    ]
    for first in range(4):
        for second in range(first, 4):
            channel_second = second_frechet(
                generator, generator_first[first], generator_first[second]
            ) + block_frechet(generator, generator_second[first][second])
            value = differential_observables(channel_second)
            second_observables[first][second] = value
            second_observables[second][first] = value

    support_lambda = all_params[4]
    function = [aval - TARGET_A]
    for da, db in first_observables:
        function.append(db - support_lambda * da)

    jacobian = zero_matrix(5, 5)
    for col in range(4):
        jacobian[0, col] = first_observables[col][0]
    for row in range(4):
        for col in range(4):
            daa, dbb = second_observables[row][col]
            jacobian[row + 1, col] = dbb - support_lambda * daa
        jacobian[row + 1, 4] = -first_observables[row][0]
    return function, jacobian


def ball_record(value: arb) -> dict[str, str]:
    return {
        "ball": str(value),
        "midpoint": str(value.mid()),
        "radius": str(value.rad()),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
    }


def matrix_records(matrix: arb_mat) -> list[list[dict[str, str]]]:
    return [
        [ball_record(matrix[row, col]) for col in range(matrix.ncols())]
        for row in range(matrix.nrows())
    ]


def load_center() -> list[str]:
    record = json.loads(Path("evidence/second-variation-verification.json").read_text(encoding="utf-8"))
    values = record["high_precision_kkt"]["params_t_gamma_alpha_beta_lambda"]
    if len(values) != 5:
        raise ValueError("expected five high-precision KKT coordinates")
    return values


def interval_newton_trial(center_strings: list[str], radius: str) -> dict:
    center = [arb(value) for value in center_strings]
    box = [arb(f"{value} +/- {radius}") for value in center_strings]
    function_center, _ = kkt_function_and_jacobian(center)
    _, jacobian_box = kkt_function_and_jacobian(box)
    try:
        inverse = jacobian_box.inv()
        newton = column(center) - inverse * column(function_center)
        inclusion = [box[index].contains_interior(newton[index, 0]) for index in range(5)]
        success = all(inclusion)
        return {
            "radius": radius,
            "jacobian_interval_invertible": True,
            "interval_newton_interior_by_coordinate": inclusion,
            "certified_unique_root_in_box": success,
            "box": [ball_record(value) for value in box],
            "newton_image": [ball_record(newton[index, 0]) for index in range(5)],
            "jacobian": matrix_records(jacobian_box),
        }
    except (ValueError, ZeroDivisionError) as error:
        return {
            "radius": radius,
            "jacobian_interval_invertible": False,
            "interval_newton_interior_by_coordinate": [False] * 5,
            "certified_unique_root_in_box": False,
            "box": [ball_record(value) for value in box],
            "error": f"{type(error).__name__}: {error}",
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--precision", type=int, default=256)
    args = parser.parse_args()

    ctx.prec = args.precision
    source_path = Path("source.md")
    source_hash_before = hashlib.sha256(source_path.read_bytes()).hexdigest()
    center_strings = load_center()
    center = [arb(value) for value in center_strings]
    function_center, jacobian_center = kkt_function_and_jacobian(center)
    trials = [interval_newton_trial(center_strings, radius) for radius in TEST_RADII]
    successful = [trial for trial in trials if trial["certified_unique_root_in_box"]]
    source_hash_after = hashlib.sha256(source_path.read_bytes()).hexdigest()

    data = {
        "job_id": "phys-00002-p01-research-efbcc56428da",
        "method": "Arb outward-rounded interval Newton in the affine-Bloch representation",
        "parameter_order": list(PARAMETER_ORDER),
        "center_decimal_strings": center_strings,
        "precision_bits": args.precision,
        "software": {
            "python_flint": flint.__version__,
            "arb_path": ARB_PATH,
            "matrix_exponential": "flint.arb_mat.exp",
        },
        "source_sha256_before": source_hash_before,
        "source_sha256_after": source_hash_after,
        "source_immutable_check": source_hash_before == source_hash_after == EXPECTED_SOURCE_SHA256,
        "center_function_balls": [ball_record(value) for value in function_center],
        "center_jacobian_balls": matrix_records(jacobian_center),
        "trials": trials,
        "successful_radii": [trial["radius"] for trial in successful],
        "largest_tested_successful_radius": successful[0]["radius"] if successful else None,
        "status": {
            "restricted_kkt_root_existence_and_uniqueness_certified": bool(successful),
            "arbitrary_rank_one_hessian_interval_certified": False,
            "transverse_added_jump_interval_certified": False,
            "finite_neighborhood_certified": False,
            "global_boundary_claim": False,
            "original_boundary_question": "unresolved",
            "candidate": False,
        },
        "limitations": (
            "Interval Newton concerns only the five restricted-family KKT equations. "
            "It neither proves that this stationary point is the restricted global minimum "
            "nor certifies the full gauge-fixed one-jump Hessian, the transverse added-jump "
            "form, unbounded tails, or the boundary of Q2."
        ),
    }
    Path(args.json).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    log_lines = [
        f"source immutable: {data['source_immutable_check']}",
        f"python-flint: {flint.__version__}; Arb precision bits: {args.precision}",
        "center KKT balls: " + " | ".join(str(value) for value in function_center),
    ]
    for trial in trials:
        log_lines.append(
            "radius "
            + trial["radius"]
            + ": invertible="
            + str(trial["jacobian_interval_invertible"]).lower()
            + ", interior="
            + str(trial["interval_newton_interior_by_coordinate"])
            + ", certified_unique_root="
            + str(trial["certified_unique_root_in_box"]).lower()
        )
    log_lines.extend(
        [
            "SCIENCE STATUS: restricted KKT root enclosure only.",
            "NOT CERTIFIED: arbitrary-rank-one Hessian, added-jump form, finite neighborhood, tails, global restricted minimum, or Q2 boundary.",
        ]
    )
    Path(args.log).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "json": args.json,
                "log": args.log,
                "successful_radii": data["successful_radii"],
                "status": data["status"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
