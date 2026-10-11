#!/usr/bin/env python3
"""Finite-radius rank-two neighborhood certificate at the a=1/2 KKT point.

The one-jump variables use the transverse gauge slice

    z = (i v_x, u_y + i v_y, u_z),

and a second jump is written in the exact mixing-orthogonal chart

    w = (eta_1, eta_2,
         -(conj(z_x) eta_1 + conj(z_y) eta_2) / conj(z_z)).

Thus z^dagger w=0 identically whenever z_z is nonzero.  Together with an
arbitrary traceless Hamiltonian this parameterizes the rank-at-most-two
Kossakowski cone locally around the certified simple rank-one point, modulo
jump phase, jump mixing, and the fixed-basis diagonal rephasing that leaves
the observed transition probabilities invariant.

For F=b-lambda*a, define G=F+(a-1/2)^2.  On the fixed-a surface G=F.  At the
enclosed KKT root G is stationary, while the penalty supplies the normal
curvature.  Second-order automatic differentiation of the polynomial/rational
Bloch generator and Arb block exponentials encloses Hess(G) on a stated box.
A fixed whitening map makes a direct interval Gershgorin test effective.

Third-order automatic differentiation of the generator is also used with the
standard submultiplicative-norm Frechet bounds for exp(A).  This supplies an
explicit, conservative third-derivative/Taylor radius independent of the
stronger direct uniform-Hessian radius.

Scope: a local rank-at-most-two statement in the displayed chart.  This is
not a global restricted-family minimum, an unbounded-tail result, or a proof
about the full boundary of Q2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parent))
import research_interval_kkt as ikkt  # noqa: E402
import research_interval_second_variation as isv  # noqa: E402

from flint import arb, arb_mat, ctx  # noqa: E402


EXPECTED_SOURCE_SHA256 = ikkt.EXPECTED_SOURCE_SHA256
N = 11
X_ORDER = (
    "h_x", "h_y", "h_z", "Re_z_y", "Re_z_z", "Im_z_x", "Im_z_y",
    "Re_eta_1", "Re_eta_2", "Im_eta_1", "Im_eta_2",
)
TEST_RADII = ("3e-3", "1e-3", "3e-4", "1e-4", "3e-5", "1e-5")
PENALTY_KAPPA = arb(1)


def zeros2() -> list[list[arb]]:
    return [[arb(0) for _ in range(N)] for _ in range(N)]


def zeros3() -> list[list[list[arb]]]:
    return [[[arb(0) for _ in range(N)] for _ in range(N)] for _ in range(N)]


class Jet3:
    """Value and ordinary first/second/third partial derivatives."""

    __slots__ = ("v", "d", "h", "t")

    def __init__(self, value=0, index: int | None = None):
        self.v = value if isinstance(value, arb) else arb(value)
        self.d = [arb(0) for _ in range(N)]
        self.h = zeros2()
        self.t = zeros3()
        if index is not None:
            self.d[index] = arb(1)

    @classmethod
    def raw(cls, value: arb, d, h, t):
        result = cls.__new__(cls)
        result.v, result.d, result.h, result.t = value, d, h, t
        return result

    @staticmethod
    def coerce(other):
        return other if isinstance(other, Jet3) else Jet3(other)

    def __neg__(self):
        return Jet3.raw(
            -self.v,
            [-x for x in self.d],
            [[-x for x in row] for row in self.h],
            [[[-x for x in row] for row in slab] for slab in self.t],
        )

    def __add__(self, other):
        other = self.coerce(other)
        return Jet3.raw(
            self.v + other.v,
            [self.d[i] + other.d[i] for i in range(N)],
            [[self.h[i][j] + other.h[i][j] for j in range(N)] for i in range(N)],
            [[[
                self.t[i][j][k] + other.t[i][j][k] for k in range(N)
            ] for j in range(N)] for i in range(N)],
        )

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        value = self.v * other.v
        d = [self.d[i] * other.v + self.v * other.d[i] for i in range(N)]
        h = zeros2()
        t = zeros3()
        for i in range(N):
            for j in range(N):
                h[i][j] = (
                    self.h[i][j] * other.v
                    + self.d[i] * other.d[j]
                    + self.d[j] * other.d[i]
                    + self.v * other.h[i][j]
                )
                for k in range(N):
                    t[i][j][k] = (
                        self.t[i][j][k] * other.v
                        + self.h[i][j] * other.d[k]
                        + self.h[i][k] * other.d[j]
                        + self.h[j][k] * other.d[i]
                        + self.d[i] * other.h[j][k]
                        + self.d[j] * other.h[i][k]
                        + self.d[k] * other.h[i][j]
                        + self.v * other.t[i][j][k]
                    )
        return Jet3.raw(value, d, h, t)

    __rmul__ = __mul__

    def reciprocal(self):
        if self.v.contains(arb(0)):
            raise ZeroDivisionError("jet denominator interval contains zero")
        value = arb(1) / self.v
        d = [-(self.d[i] * value) / self.v for i in range(N)]
        h = zeros2()
        t = zeros3()
        for i in range(N):
            for j in range(N):
                h[i][j] = -(
                    self.h[i][j] * value
                    + self.d[i] * d[j]
                    + self.d[j] * d[i]
                ) / self.v
        # All second derivatives must exist before the third-order recurrence
        # reads h[j][k], h[i][k], and h[i][j].
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    t[i][j][k] = -(
                        self.t[i][j][k] * value
                        + self.h[i][j] * d[k]
                        + self.h[i][k] * d[j]
                        + self.h[j][k] * d[i]
                        + self.d[i] * h[j][k]
                        + self.d[j] * h[i][k]
                        + self.d[k] * h[i][j]
                    ) / self.v
        return Jet3.raw(value, d, h, t)

    def __truediv__(self, other):
        return self * self.coerce(other).reciprocal()

    def __rtruediv__(self, other):
        return self.coerce(other) / self


def cadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def cmul(left, right):
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def cconj(value):
    return value[0], -value[1]


def cdiv(left, right):
    denominator = right[0] * right[0] + right[1] * right[1]
    numerator = cmul(left, cconj(right))
    return numerator[0] / denominator, numerator[1] / denominator


def cross(left, right):
    return [
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    ]


def add_jump(generator, u, v):
    norm2 = sum((x * x for x in u + v), Jet3(0))
    for row in range(3):
        for col in range(3):
            generator[row][col] = generator[row][col] + 2 * (u[row] * u[col] + v[row] * v[col])
            if row == col:
                generator[row][col] = generator[row][col] - 2 * norm2
    translation = cross(u, v)
    for row in range(3):
        generator[row][3] = generator[row][3] + 4 * translation[row]


def chart_generator(variables: list[Jet3]):
    h = variables[:3]
    z = [
        (Jet3(0), variables[5]),
        (variables[3], variables[6]),
        (variables[4], Jet3(0)),
    ]
    eta1 = (variables[7], variables[9])
    eta2 = (variables[8], variables[10])
    numerator = cadd(cmul(cconj(z[0]), eta1), cmul(cconj(z[1]), eta2))
    w3 = cdiv((-numerator[0], -numerator[1]), cconj(z[2]))
    w = [eta1, eta2, w3]

    generator = [[Jet3(0) for _ in range(4)] for _ in range(4)]
    generator[0][1] = generator[0][1] - 2 * h[2]
    generator[0][2] = generator[0][2] + 2 * h[1]
    generator[1][0] = generator[1][0] + 2 * h[2]
    generator[1][2] = generator[1][2] - 2 * h[0]
    generator[2][0] = generator[2][0] - 2 * h[1]
    generator[2][1] = generator[2][1] + 2 * h[0]
    add_jump(generator, [item[0] for item in z], [item[1] for item in z])
    add_jump(generator, [item[0] for item in w], [item[1] for item in w])
    return generator, z, w


def extract_generator(jets):
    value = arb_mat(4, 4)
    first = [arb_mat(4, 4) for _ in range(N)]
    second = [[arb_mat(4, 4) for _ in range(N)] for _ in range(N)]
    third = [[[arb_mat(4, 4) for _ in range(N)] for _ in range(N)] for _ in range(N)]
    for row in range(4):
        for col in range(4):
            item = jets[row][col]
            value[row, col] = item.v
            for i in range(N):
                first[i][row, col] = item.d[i]
                for j in range(N):
                    second[i][j][row, col] = item.h[i][j]
                    for k in range(N):
                        third[i][j][k][row, col] = item.t[i][j][k]
    return value, first, second, third


def observable(matrix: arb_mat, kind: str, support_lambda: arb) -> arb:
    mzz, vz = matrix[2, 2], matrix[2, 3]
    if kind == "a":
        return (mzz + vz) / 2
    if kind == "f":
        return ((arb(1) - support_lambda) * mzz - (arb(1) + support_lambda) * vz) / 2
    raise ValueError(kind)


def channel_derivatives(generator, first, second, support_lambda):
    channel = generator.exp()
    aval = (arb(1) + channel[2, 2] + channel[2, 3]) / 2
    gradient_a = [arb(0) for _ in range(N)]
    hessian_a = arb_mat(N, N)
    hessian_f = arb_mat(N, N)
    first_channels = []
    for i in range(N):
        derivative = ikkt.block_frechet(generator, first[i])
        first_channels.append(derivative)
        gradient_a[i] = observable(derivative, "a", support_lambda)
    for i in range(N):
        for j in range(i, N):
            derivative = ikkt.second_frechet(generator, first[i], first[j])
            derivative += ikkt.block_frechet(generator, second[i][j])
            va = observable(derivative, "a", support_lambda)
            vf = observable(derivative, "f", support_lambda)
            hessian_a[i, j] = hessian_a[j, i] = va
            hessian_f[i, j] = hessian_f[j, i] = vf
    return aval, gradient_a, hessian_a, hessian_f


def augmented_hessian(generator, first, second, support_lambda):
    aval, gradient_a, hessian_a, hessian_f = channel_derivatives(
        generator, first, second, support_lambda
    )
    delta = aval - arb("0.5")
    result = arb_mat(N, N)
    for i in range(N):
        for j in range(N):
            result[i, j] = hessian_f[i, j] + 2 * PENALTY_KAPPA * (
                gradient_a[i] * gradient_a[j] + delta * hessian_a[i, j]
            )
    return result, aval, gradient_a, hessian_a, hessian_f


def direct_margins(matrix: arb_mat):
    margins = []
    for row in range(matrix.nrows()):
        radius = sum((abs(matrix[row, col]) for col in range(matrix.ncols()) if col != row), arb(0))
        margins.append(matrix[row, row] - radius)
    return margins


def records(values):
    return [ikkt.ball_record(value) for value in values]


def midpoint_array(matrix: arb_mat):
    return np.array([[float(matrix[i, j].mid()) for j in range(matrix.ncols())] for i in range(matrix.nrows())])


def transform_variables(root_x: list[arb], transform: np.ndarray, radius: str):
    y = [Jet3(arb(f"0 +/- {radius}"), index=i) for i in range(N)]
    variables = []
    for row in range(N):
        base = root_x[row] if row < 7 else arb(0)
        value = Jet3(base)
        for col in range(N):
            value = value + arb(repr(float(transform[row, col]))) * y[col]
        variables.append(value)
    return variables


def matrix_norm_bound(matrix: arb_mat) -> arb:
    # The entrywise l1 norm is submultiplicative and bounds every matrix entry.
    return sum((abs(matrix[i, j]) for i in range(matrix.nrows()) for j in range(matrix.ncols())), arb(0)).upper()


def third_derivative_bound(generator, first, second, third, support_lambda, radius):
    norm0 = matrix_norm_bound(generator)
    norm1 = [matrix_norm_bound(first[i]) for i in range(N)]
    norm2 = [[matrix_norm_bound(second[i][j]) for j in range(N)] for i in range(N)]
    norm3 = [[[matrix_norm_bound(third[i][j][k]) for k in range(N)] for j in range(N)] for i in range(N)]
    exponential = norm0.exp().upper()
    cf = (abs(arb(1) - support_lambda) + abs(arb(1) + support_lambda)).upper() / 2
    first_a = [(exponential * norm1[i]).upper() for i in range(N)]
    grad_a_bound = sum((value * value for value in first_a), arb(0)).sqrt().upper()
    delta_a_bound = (arb(radius) * grad_a_bound).upper()
    tensor_squares = arb(0)
    max_component = arb(0)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                composite = (
                    norm1[i] * norm1[j] * norm1[k]
                    + norm2[i][j] * norm1[k]
                    + norm2[i][k] * norm1[j]
                    + norm2[j][k] * norm1[i]
                    + norm3[i][j][k]
                )
                third_a = (exponential * composite).upper()
                second_ij = (exponential * (norm1[i] * norm1[j] + norm2[i][j])).upper()
                second_ik = (exponential * (norm1[i] * norm1[k] + norm2[i][k])).upper()
                second_jk = (exponential * (norm1[j] * norm1[k] + norm2[j][k])).upper()
                third_f = (cf * third_a).upper()
                third_g = (
                    third_f
                    + 2 * PENALTY_KAPPA * (
                        delta_a_bound * third_a
                        + first_a[i] * second_jk
                        + first_a[j] * second_ik
                        + first_a[k] * second_ij
                    )
                ).upper()
                tensor_squares += third_g * third_g
                if third_g > max_component:
                    max_component = third_g
    frobenius = tensor_squares.sqrt().upper()
    return {
        "matrix_norm": ikkt.ball_record(norm0),
        "exp_matrix_norm_bound": ikkt.ball_record(exponential),
        "gradient_a_euclidean_bound": ikkt.ball_record(grad_a_bound),
        "a_minus_half_bound_on_ball": ikkt.ball_record(delta_a_bound),
        "max_third_partial_bound": ikkt.ball_record(max_component),
        "third_tensor_frobenius_bound": ikkt.ball_record(frobenius),
    }, frobenius


def root_data():
    center = [arb(value) for value in ikkt.load_center()]
    slice_center = isv.full_slice_center(center)
    full_root, inclusion, residual = isv.full_slice_root_enclosure(slice_center, "1e-4")
    return full_root, inclusion, residual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--precision", type=int, default=256)
    args = parser.parse_args()
    ctx.prec = args.precision

    source = Path("source.md")
    source_before = hashlib.sha256(source.read_bytes()).hexdigest()
    root, root_inclusion, root_residual = root_data()
    root_x = root[:7] + [arb(0) for _ in range(4)]
    support_lambda = root[7]

    # First construct the augmented point Hessian in the native chart.
    native_variables = [Jet3(root_x[i], index=i) for i in range(N)]
    native_jets, _, _ = chart_generator(native_variables)
    native_generator, native_first, native_second, _ = extract_generator(native_jets)
    native_hessian, point_aval, _, _, _ = augmented_hessian(
        native_generator, native_first, native_second, support_lambda
    )
    point_channel = native_generator.exp()
    point_bval = (arb(1) + point_channel[2, 2] - point_channel[2, 3]) / 2
    native_midpoint = midpoint_array(native_hessian)
    native_midpoint = (native_midpoint + native_midpoint.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(native_midpoint)
    if eigenvalues[0] <= 0:
        raise RuntimeError("native augmented point Hessian midpoint is not positive definite")
    whitening = eigenvectors @ np.diag(1 / np.sqrt(eigenvalues))

    # Certify the point Hessian in the fixed whitened coordinates.
    transform_arb = isv.arb_from_numpy(whitening)
    point_whitened = transform_arb.transpose() * native_hessian * transform_arb
    point_margins = direct_margins(point_whitened)
    point_certified = all(value > 0 for value in point_margins)
    if not point_certified:
        raise RuntimeError("whitened point Hessian did not pass direct interval Gershgorin")

    trials = []
    successful_radius = None
    successful_payload = None
    for radius in TEST_RADII:
        variables = transform_variables(root_x, whitening, radius)
        jets, z, w = chart_generator(variables)
        generator, first, second, third = extract_generator(jets)
        hessian, aval, gradient_a, hessian_a, hessian_f = augmented_hessian(
            generator, first, second, support_lambda
        )
        margins = direct_margins(hessian)
        denominator = variables[4].v
        certified = all(value > 0 for value in margins) and not denominator.contains(arb(0))
        trial = {
            "radius": radius,
            "z_z_ball": ikkt.ball_record(denominator),
            "z_z_excludes_zero": not denominator.contains(arb(0)),
            "a_ball": ikkt.ball_record(aval),
            "direct_gershgorin_margins": records(margins),
            "uniform_augmented_hessian_positive": certified,
        }
        trials.append(trial)
        if certified and successful_radius is None:
            third_record, third_bound = third_derivative_bound(
                generator, first, second, third, support_lambda, radius
            )
            successful_radius = radius
            successful_payload = (trial, third_record, third_bound)

    if successful_payload is None:
        raise RuntimeError("no tested rank-two chart radius certified")
    chosen_trial, third_record, third_bound = successful_payload
    point_mu = min(point_margins)
    taylor_radius = (3 * point_mu / third_bound).lower()
    chosen = arb(successful_radius)
    if taylor_radius > chosen:
        taylor_radius = chosen

    source_after = hashlib.sha256(source.read_bytes()).hexdigest()
    data = {
        "job_id": "phys-00002-p01-research-147b1435c704",
        "method": "Arb interval Hessian on an exact rank-two Kossakowski amplitude chart, plus analytic Frechet norm bounds for the third derivative",
        "precision_bits": args.precision,
        "interval_dependency": {
            "package": "python-flint",
            "version": ikkt.flint.__version__,
            "arb_path": ikkt.ARB_PATH,
        },
        "source_sha256_before": source_before,
        "source_sha256_after": source_after,
        "source_immutable_check": source_before == source_after == EXPECTED_SOURCE_SHA256,
        "root": {
            "gauge_slice": "Re(z_x)=0 and Im(z_z)=0",
            "variable_order": list(isv.SLICE_VARIABLE_ORDER),
            "interval_newton_interior_by_coordinate": root_inclusion,
            "center_residual_balls": records(root_residual),
            "enclosure": records(root),
            "a_exact_at_root": "1/2 by the first KKT equation",
            "a_interval_reconstruction": ikkt.ball_record(point_aval),
            "b_star_enclosure": ikkt.ball_record(point_bval),
        },
        "rank_two_chart": {
            "native_coordinate_order": list(X_ORDER),
            "z": "(i Im_z_x, Re_z_y+i Im_z_y, Re_z_z)",
            "eta": "(eta_1,eta_2) in C^2",
            "w": "(eta_1,eta_2,-(conj(z_x)eta_1+conj(z_y)eta_2)/conj(z_z))",
            "orthogonality_identity": "z^dagger w=0 exactly",
            "kossakowski_matrix": "C=z z^dagger+w w^dagger, hence C is PSD and rank at most two",
            "local_coverage": "For a nearby rank-at-most-two PSD C with a simple leading eigenvalue, choose orthogonal spectral amplitudes z,w; jump phase and fixed-basis rephasing put z on the stated transverse slice, and z_z nonzero gives the displayed eta coordinates.",
            "whitening_matrix_rows": whitening.tolist(),
            "ball_definition": "native coordinates x=x_*+B y with B the recorded fixed whitening matrix and ||y||_2 no larger than the certified radius; interval work encloses the containing coordinate cube |y_i|<=radius",
        },
        "augmented_support": {
            "functional": "G=(b-lambda*a)+(a-1/2)^2",
            "fixed_a_logic": "On a=1/2, G=b-lambda/2, so G-G_*=b-b_*.",
            "stationarity": "The interval-Newton equations make all gauge-slice derivatives of b-lambda*a vanish at x_*; eta enters through D[w] quadratically, and a=1/2, hence grad G=0.",
            "native_midpoint_eigenvalues": eigenvalues.tolist(),
            "point_whitened_hessian_balls": ikkt.matrix_records(point_whitened),
            "point_direct_gershgorin_margins": records(point_margins),
            "point_positive_certified": point_certified,
        },
        "radius_trials": trials,
        "uniform_certificate": {
            "certified_radius_y_euclidean": successful_radius,
            "containing_cube_radius": successful_radius,
            "direct_interval_hessian_positive_on_cube": chosen_trial["uniform_augmented_hessian_positive"],
            "minimum_direct_gershgorin_margin_ball": min(
                chosen_trial["direct_gershgorin_margins"],
                key=lambda item: float(arb(item["ball"]).lower()),
            ),
            "conclusion": "Every chart point in the Euclidean y-ball with a=1/2 has b>=b_*; strict inequality holds away from gauge-equivalent representations of the root.",
        },
        "third_frechet_taylor_bound": {
            **third_record,
            "point_hessian_lower_bound_ball": ikkt.ball_record(point_mu),
            "certified_taylor_radius_y_euclidean": ikkt.ball_record(taylor_radius),
            "inequality": "G(y)-G(0)>=mu*||y||_2^2/2-L3*||y||_2^3/6, using the recorded Frobenius bound L3 for D^3G on the containing cube",
            "note": "The direct interval-Hessian radius is stronger; this separate conservative radius records an explicit third-Frechet/Lipschitz Taylor control.",
        },
        "status": {
            "rank_two_chart_admissible": True,
            "root_certified": all(root_inclusion),
            "point_augmented_hessian_positive": point_certified,
            "finite_radius_uniform_hessian_positive": chosen_trial["uniform_augmented_hessian_positive"],
            "finite_radius_taylor_remainder_certified": taylor_radius > 0,
            "rank_two_fixed_a_local_optimality_certified": (
                all(root_inclusion)
                and point_certified
                and chosen_trial["uniform_augmented_hessian_positive"]
                and taylor_radius > 0
            ),
            "global_restricted_minimum_certified": False,
            "unbounded_tail_certified": False,
            "q2_boundary_certified": False,
            "original_boundary_question": "unresolved",
        },
        "limitations": "The certificate is local in an explicitly normalized chart and covers rank-at-most-two Kossakowski matrices near the simple rank-one root. It does not cover rank-three dissipators, distant generators, unbounded rates/times, prove that b_* is the global restricted minimum, or identify the true Q2 boundary.",
    }
    Path(args.json).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    log_lines = [
        f"source immutable: {data['source_immutable_check']}",
        f"Arb precision bits: {args.precision}",
        f"root interval-Newton inclusion: {root_inclusion}",
        "native augmented midpoint eigenvalues: " + " ".join(f"{x:.15g}" for x in eigenvalues),
        "whitened point Gershgorin margins: " + " | ".join(str(x) for x in point_margins),
    ]
    for trial in trials:
        log_lines.append(
            f"radius {trial['radius']}: uniform Hessian positive={trial['uniform_augmented_hessian_positive']}; "
            f"z_z excludes zero={trial['z_z_excludes_zero']}"
        )
    log_lines.extend([
        f"selected direct uniform radius: {successful_radius}",
        f"third-tensor Frobenius bound: {third_bound}",
        f"conservative Taylor radius: {taylor_radius}",
        "SCIENCE STATUS: finite-radius fixed-a local optimality for the explicit nearby rank-at-most-two chart.",
        "NOT CERTIFIED: rank-three directions, global minimum, unbounded tails, or Q2 boundary.",
    ])
    Path(args.log).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(json.dumps({"json": args.json, "log": args.log, "status": data["status"]}, indent=2))


if __name__ == "__main__":
    main()
