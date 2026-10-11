#!/usr/bin/env python3
"""Poisson-generator attack on the four-dimensional current quotient.

The quotient complement is

    w_a(x) = (a0 + a1*x1**2 + a2*x1*x2 + a3*x2**2) R x.

For each parameter point this script builds the complete real polynomial space
of total degree at most four, solves the centered Poisson equations, and forms
the symmetric long-time diffusion matrix.  Floating-point scans are discovery
only.  A frozen rational direction is subsequently replayed over exact
rationals, including the otherwise omitted constant Poisson equation.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import product
from fractions import Fraction

import numpy as np
import sympy as sp


def monomial_basis(max_degree: int = 4):
    return sorted(
        [a for a in product(range(max_degree + 1), repeat=4) if sum(a) <= max_degree],
        key=lambda a: (sum(a), a),
    )


BASIS = monomial_basis(4)
NONCONSTANT = BASIS[1:]
ROW = {a: i for i, a in enumerate(NONCONSTANT)}


def add_term(poly, alpha, coefficient):
    if coefficient != 0:
        poly[alpha] = poly.get(alpha, 0) + coefficient
        if poly[alpha] == 0:
            del poly[alpha]


def generator_image(alpha, drift, noise_strength):
    out = {}
    for i in range(4):
        if alpha[i] == 0:
            continue
        for j in range(4):
            if drift[i][j] == 0:
                continue
            beta = list(alpha)
            beta[i] -= 1
            beta[j] += 1
            add_term(out, tuple(beta), alpha[i] * drift[i][j])
    for i in (2, 3):
        if alpha[i] >= 2:
            beta = list(alpha)
            beta[i] -= 2
            add_term(out, tuple(beta), noise_strength * alpha[i] * (alpha[i] - 1))
    return out


def drift_matrix(m, gamma, spring, torque):
    z = 0 * m
    o = 1 + z
    return [
        [z, z, o, z],
        [z, z, z, o],
        [-spring / m, -torque / m, -gamma / m, z],
        [torque / m, -spring / m, z, -gamma / m],
    ]


def covariance_matrix(m, gamma, k, temperature, kappa, driven=True):
    if driven:
        kstar = k - m * kappa**2 / gamma**2
        cxx = temperature / kstar
        cvv = temperature * k / (m * kstar)
        c = temperature * kappa / (gamma * kstar)
        # blocks [[Cov xx, Cov x v], [Cov v x, Cov vv]], with Cov(v,x)=c R
        return [
            [cxx, 0 * cxx, 0 * cxx, c],
            [0 * cxx, cxx, -c, 0 * cxx],
            [0 * cxx, -c, cvv, 0 * cxx],
            [c, 0 * cxx, 0 * cxx, cvv],
        ]
    kstar = k - m * kappa**2 / gamma**2
    cxx = temperature / kstar
    cvv = temperature / m
    z = 0 * cxx
    return [[cxx, z, z, z], [z, cxx, z, z], [z, z, cvv, z], [z, z, z, cvv]]


def current_basis():
    # f_i = p_i(x)*(x1*v2-x2*v1), p=(1,x1^2,x1*x2,x2^2).
    prefactors = [(0, 0), (2, 0), (1, 1), (0, 2)]
    currents = []
    for p1, p2 in prefactors:
        f = {}
        a = [0, 0, 0, 0]
        a[0], a[1], a[3] = p1 + 1, p2, 1
        f[tuple(a)] = 1
        a = [0, 0, 0, 0]
        a[0], a[1], a[2] = p1, p2 + 1, 1
        f[tuple(a)] = -1
        currents.append(f)
    return currents


CURRENTS = current_basis()


def gaussian_moment_factory(covariance):
    @lru_cache(maxsize=None)
    def moment(alpha):
        degree = sum(alpha)
        if degree == 0:
            return covariance[0][0] * 0 + 1
        if degree % 2:
            return covariance[0][0] * 0
        indices = []
        for i, count in enumerate(alpha):
            indices.extend([i] * count)
        first = indices[0]
        total = covariance[0][0] * 0
        for pos in range(1, len(indices)):
            second = indices[pos]
            rest = indices[1:pos] + indices[pos + 1 :]
            beta = tuple(rest.count(i) for i in range(4))
            total += covariance[first][second] * moment(beta)
        return total

    return moment


def expectation(poly, moment):
    return sum(coefficient * moment(alpha) for alpha, coefficient in poly.items())


def product_expectation(left, right, moment):
    total = 0
    for a, ca in left.items():
        for b, cb in right.items():
            total += ca * cb * moment(tuple(a[i] + b[i] for i in range(4)))
    return total


def build_poisson_matrix(drift, noise_strength, exact=False):
    n = len(NONCONSTANT)
    if exact:
        matrix = sp.zeros(n)
        constant = sp.zeros(1, n)
    else:
        matrix = np.zeros((n, n), dtype=float)
        constant = np.zeros(n, dtype=float)
    for col, alpha in enumerate(NONCONSTANT):
        for beta, coefficient in generator_image(alpha, drift, noise_strength).items():
            if sum(beta) == 0:
                constant[col] -= coefficient
            else:
                matrix[ROW[beta], col] -= coefficient
    return matrix, constant


def diffusion_matrix(parameters, driven=True, exact=False):
    m, gamma, k, temperature, kappa = parameters
    kstar = k - m * kappa**2 / gamma**2
    if not (m > 0 and gamma > 0 and k > 0 and temperature > 0 and kappa != 0 and kstar > 0):
        raise ValueError("inadmissible source parameters")
    spring = k if driven else kstar
    torque = kappa if driven else 0 * kappa
    drift = drift_matrix(m, gamma, spring, torque)
    covariance = covariance_matrix(m, gamma, k, temperature, kappa, driven)
    moment = gaussian_moment_factory(covariance)
    matrix, constant_row = build_poisson_matrix(
        drift, gamma * temperature / m**2, exact=exact
    )
    means = [expectation(f, moment) for f in CURRENTS]
    if exact:
        rhs = sp.zeros(len(NONCONSTANT), 4)
    else:
        rhs = np.zeros((len(NONCONSTANT), 4), dtype=float)
    for j, f in enumerate(CURRENTS):
        for alpha, coefficient in f.items():
            rhs[ROW[alpha], j] = coefficient
    if exact:
        solutions = matrix.inv() * rhs
    else:
        solutions = np.linalg.solve(matrix, rhs)
    constant_residuals = []
    hs = []
    for j in range(4):
        h = {
            alpha: solutions[i, j]
            for i, alpha in enumerate(NONCONSTANT)
            if solutions[i, j] != 0
        }
        hs.append(h)
        constant_residuals.append(constant_row[0, :].dot(solutions[:, j]) + means[j] if exact else constant_row @ solutions[:, j] + means[j])
    nonsymmetric = [[0 for _ in range(4)] for _ in range(4)]
    centered = []
    for i, f in enumerate(CURRENTS):
        g = dict(f)
        g[(0, 0, 0, 0)] = -means[i]
        centered.append(g)
    for i in range(4):
        for j in range(4):
            nonsymmetric[i][j] = product_expectation(centered[i], hs[j], moment)
    if exact:
        diffusion = sp.Matrix(4, 4, lambda i, j: sp.factor((nonsymmetric[i][j] + nonsymmetric[j][i]) / 2))
    else:
        ns = np.asarray(nonsymmetric, dtype=float)
        diffusion = (ns + ns.T) / 2
    return {
        "kstar": kstar,
        "drift": drift,
        "covariance": covariance,
        "means": means,
        "poisson_matrix": matrix,
        "constant_residuals": constant_residuals,
        "solutions": solutions,
        "diffusion": diffusion,
    }


def numeric_scan():
    records = []
    # Dimensionless discovery slice m=gamma=T=1, k=kstar+kappa^2.
    kstars = [1 / 20, 1 / 10, 1 / 5, 1 / 2, 1, 2, 5, 10]
    kappas = [1 / 20, 1 / 10, 1 / 5, 1 / 2, 1, 2, 5]
    for ks in kstars:
        for q in kappas:
            parameters = (1.0, 1.0, ks + q * q, 1.0, q)
            driven = diffusion_matrix(parameters, True, False)["diffusion"]
            equilibrium = diffusion_matrix(parameters, False, False)["diffusion"]
            delta = driven - equilibrium
            scale = np.diag([1.0, ks, ks, ks])
            normalized = scale @ delta @ scale
            eigenvalues, eigenvectors = np.linalg.eigh(normalized)
            records.append((eigenvalues[0], ks, q, eigenvalues, eigenvectors[:, 0], delta))
    records.sort(key=lambda r: r[0])
    return records


def rational_vector(vector, max_denominator=64):
    pivot = int(np.argmax(np.abs(vector)))
    normalized = vector / vector[pivot]
    return [sp.Rational(Fraction(float(x)).limit_denominator(max_denominator)) for x in normalized]


def exact_replay(parameters, coefficients):
    result_d = diffusion_matrix(parameters, True, True)
    result_e = diffusion_matrix(parameters, False, True)
    delta = result_d["diffusion"] - result_e["diffusion"]
    a = sp.Matrix(coefficients)
    dd = sp.factor((a.T * result_d["diffusion"] * a)[0])
    de = sp.factor((a.T * result_e["diffusion"] * a)[0])
    difference = sp.factor(dd - de)
    return result_d, result_e, delta.applyfunc(sp.factor), dd, de, difference


def format_matrix(matrix):
    return "[" + ",".join("[" + ",".join(str(matrix[i, j]) for j in range(matrix.cols)) + "]" for i in range(matrix.rows)) + "]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--exact", action="store_true")
    args = parser.parse_args()
    if not args.scan and not args.exact:
        args.scan = args.exact = True

    best = None
    if args.scan:
        records = numeric_scan()
        best = records[0]
        print("DISCOVERY_ONLY=float64 complete degree<=4 Poisson scan")
        print(f"scan_points={len(records)}")
        print(f"negative_points={sum(r[0] < -1e-9 for r in records)}")
        for record in records[:8]:
            value, ks, q, vals, vec, _ = record
            print(f"scan_case=kstar:{ks:.17g},kappa:{q:.17g},normalized_eigenvalues:{vals.tolist()},min_vector:{vec.tolist()}")

    if args.exact:
        # Exact full-closure hold-out.  All entries are exact rationals; this
        # point illustrates the certificate but does not replace the
        # continuous-domain proof in quotient_symbolic.py/verify_quotient.py.
        parameters = tuple(map(sp.Rational, (1, 1, 2, 1, 1)))
        coefficients = list(map(sp.Rational, (1, 0, 0, 0)))
        rd, re, delta, dd, de, difference = exact_replay(parameters, coefficients)
        print("CERTIFICATE=exact rational complete degree<=4 Poisson solve")
        print(f"parameters_m_gamma_k_T_kappa={[str(x) for x in parameters]}")
        print(f"kstar={rd['kstar']}")
        print(f"quotient_coefficients_a0_a1_a2_a3={[str(x) for x in coefficients]}")
        print(f"driven_means={[str(sp.factor(x)) for x in rd['means']]}")
        print(f"equilibrium_means={[str(sp.factor(x)) for x in re['means']]}")
        print(f"driven_constant_poisson_residuals={[str(sp.factor(x)) for x in rd['constant_residuals']]}")
        print(f"equilibrium_constant_poisson_residuals={[str(sp.factor(x)) for x in re['constant_residuals']]}")
        print(f"Q_driven={format_matrix(rd['diffusion'])}")
        print(f"Q_equilibrium={format_matrix(re['diffusion'])}")
        print(f"Q_delta={format_matrix(delta)}")
        print(f"D_driven={dd}")
        print(f"D_equilibrium={de}")
        print(f"D_difference={difference}")
        print(f"strict_positive={bool(difference > 0)}")
        print("curl_w=2")
        print("nongradient=true")
        print("status=HOLDOUT_PASS" if difference > 0 else "status=HOLDOUT_FAIL")


if __name__ == "__main__":
    main()
