#!/usr/bin/env python3
"""Exact sign certificate and full-closure hold-outs for the quotient theorem."""

from __future__ import annotations

import sympy as sp

from quotient_poisson import diffusion_matrix


a, u = sp.symbols("a u", positive=True, finite=True)


H = 16 * a**2 + 32 * a * u + 24 * a + 16 * u**2 + 40 * u + 9

P_ISO = (
    448 * a**5
    + 2944 * a**4 * u
    + 1700 * a**4
    + 5568 * a**3 * u**2
    + 8220 * a**3 * u
    + 2683 * a**3
    + 4096 * a**2 * u**3
    + 12480 * a**2 * u**2
    + 8432 * a**2 * u
    + 1872 * a**2
    + 1024 * a * u**4
    + 6144 * a * u**3
    + 8256 * a * u**2
    + 3424 * a * u
    + 432 * a
    + 768 * u**4
    + 2304 * u**3
    + 1440 * u**2
    + 336 * u
    + 27
)

P_ANGULAR = (
    10496 * a**7
    + 60928 * a**6 * u
    + 41024 * a**6
    + 147200 * a**5 * u**2
    + 235488 * a**5 * u
    + 70512 * a**5
    + 189440 * a**4 * u**3
    + 529920 * a**4 * u**2
    + 359932 * a**4 * u
    + 65772 * a**4
    + 136960 * a**3 * u**4
    + 591680 * a**3 * u**3
    + 702445 * a**3 * u**2
    + 278523 * a**3 * u
    + 28404 * a**3
    + 52736 * a**2 * u**5
    + 335040 * a**2 * u**4
    + 633102 * a**2 * u**3
    + 458033 * a**2 * u**2
    + 105507 * a**2 * u
    + 3564 * a**2
    + 8448 * a * u**6
    + 83424 * a * u**5
    + 251037 * a * u**4
    + 299256 * a * u**3
    + 142527 * a * u**2
    + 19332 * a * u
    + 4608 * u**6
    + 30960 * u**5
    + 61749 * u**4
    + 50670 * u**3
    + 16893 * u**2
    + 1620 * u
)


def formula_components():
    q00 = 2 * u * (5 * a + 4 * u + 1) / a**3
    q01 = 16 * u * (4 * a + 4 * u + 1) / a**4
    determinant = 32 * u**2 * P_ISO / (a**8 * (4 * a + 3) * H)
    q11 = sp.factor((determinant + q01**2) / q00)
    r = 16 * a**2 + 32 * a * u + 12 * a + 16 * u**2 - 13 * u
    s_squared = 4 * u * (20 * a + 20 * u + 3) ** 2
    angular_denominator = (
        a**3
        * (4 * a + 3)
        * ((a + u) ** 2 + u)
        * (4 * a + 3 * u + 3)
        * (r**2 + s_squared)
    )
    angular = 16 * u * P_ANGULAR / angular_denominator
    return tuple(map(sp.factor, (q00, q01, q11, determinant, angular)))


def full_matrix():
    q00, q01, q11, _, angular = formula_components()
    # Isotropic coordinates are (a0,s), s=(a1+a3)/2; the angular
    # coordinates are d=(a1-a3)/2 and e=a2, with D(e*x*y*A)=angular*e^2/4.
    return sp.Matrix(
        [
            [q00, q01 / 2, 0, q01 / 2],
            [q01 / 2, (q11 + angular) / 4, 0, (q11 - angular) / 4],
            [0, 0, angular / 4, 0],
            [q01 / 2, (q11 - angular) / 4, 0, (q11 + angular) / 4],
        ]
    ).applyfunc(sp.factor)


def positive_coefficients(poly):
    p = sp.Poly(poly, a, u)
    return len(p.terms()), min(int(c) for c in p.coeffs()), all(c > 0 for c in p.coeffs())


def main():
    q00, q01, q11, determinant, angular = formula_components()
    exact_formula = full_matrix()
    print("THEOREM_DOMAIN=a=m*kstar/gamma^2>0,u=(m*kappa/gamma^2)^2>0")
    print("SIGN_EQUIVALENCE=positive_time_length_prefactor_and_nonsingular_current_congruence")
    print("QISO_DELTA_00=" + str(q00))
    print("QISO_DELTA_01=" + str(q01))
    print("QISO_DELTA_11=" + str(q11))
    print("QISO_DELTA_DETERMINANT=" + str(determinant))
    print("DANGULAR_TWO_DELTA=" + str(angular))
    print(f"P_ISO_COEFFICIENT_AUDIT={positive_coefficients(P_ISO)}")
    print(f"P_ANGULAR_COEFFICIENT_AUDIT={positive_coefficients(P_ANGULAR)}")
    print(f"H_COEFFICIENT_AUDIT={positive_coefficients(H)}")
    print("DENOMINATOR_AUDIT=a,(4a+3),H,((a+u)^2+u),(4a+3u+3),and_R^2+4u(20a+20u+3)^2_are_strictly_positive")
    print("Q_DELTA_ASSEMBLY=[[q00,q01/2,0,q01/2],[q01/2,(q11+g)/4,0,(q11-g)/4],[0,0,g/4,0],[q01/2,(q11-g)/4,0,(q11+g)/4]]")

    holdouts = [
        (sp.Rational(1), sp.Rational(1)),
        (sp.Rational(2), sp.Rational(1, 2)),
        (sp.Rational(3, 2), sp.Rational(-2, 3)),
    ]
    for aa, bb in holdouts:
        parameters = (sp.Integer(1), sp.Integer(1), aa + bb**2, sp.Integer(1), bb)
        driven = diffusion_matrix(parameters, True, True)
        equilibrium = diffusion_matrix(parameters, False, True)
        complete_delta = (driven["diffusion"] - equilibrium["diffusion"]).applyfunc(sp.factor)
        predicted = exact_formula.subs({a: aa, u: bb**2}).applyfunc(sp.factor)
        residual = (complete_delta - predicted).applyfunc(sp.factor)
        assert residual == sp.zeros(4)
        assert all(sp.factor(x) == 0 for x in driven["constant_residuals"])
        assert all(sp.factor(x) == 0 for x in equilibrium["constant_residuals"])
        print(f"holdout_a_b=({aa},{bb})")
        print("full_69_unknown_residual=zero_matrix")
        print("constant_poisson_residuals=all_zero")
        print(f"Q_delta={complete_delta.tolist()}")

    assert positive_coefficients(P_ISO)[2]
    assert positive_coefficients(P_ANGULAR)[2]
    print("conclusion=Q_delta_is_positive_definite_on_the_four_dimensional_quotient_for_all_a>0,u>0")
    print("equality_scope=only_gradient_boundary_classes_have_zero_asymptotic_difference")
    print("status=PASS")


if __name__ == "__main__":
    main()
