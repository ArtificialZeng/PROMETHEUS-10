#!/usr/bin/env python3
"""Exact replay and boundary attacks for the coarse-GAD robustness certificate.

The logical checks use SymPy exact arithmetic.  No floating-point value is used in
an assertion or in the certified lower bound.
"""

from __future__ import annotations

import sympy as sp


def instrument_image(kraus_bin: tuple[sp.Matrix, ...], operator: sp.Matrix) -> sp.Matrix:
    return sp.simplify(sum((k * operator * k.adjoint() for k in kraus_bin), sp.zeros(2)))


def main() -> None:
    # q and r are declared positive independently so that SymPy handles
    # conjugates of their square roots exactly.  Every completed expression is
    # then restricted to q=1-p and r=1-gamma.
    p, q, gamma, r = sp.symbols("p q gamma r", positive=True, real=True)
    s = sp.sqrt(r)
    zero = sp.Integer(0)

    identity = sp.eye(2)
    pauli_x = sp.Matrix([[0, 1], [1, 0]])
    pauli_y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    pauli_z = sp.diag(1, -1)

    k0 = sp.sqrt(p) * sp.diag(1, s)
    k1 = sp.Matrix([[0, sp.sqrt(p * gamma)], [0, 0]])
    k2 = sp.sqrt(q) * sp.diag(s, 1)
    k3 = sp.Matrix([[0, 0], [sp.sqrt(q * gamma), 0]])
    kraus = (k0, k1, k2, k3)
    bins = ((k0, k3), (k1, k2))

    normalize = lambda expression: sp.simplify(expression.subs({q: 1 - p, r: 1 - gamma}))
    completeness = normalize(sum((k.adjoint() * k for k in kraus), sp.zeros(2)))
    assert completeness == identity

    expected_images = {
        "x": (p * s * pauli_x, q * s * pauli_x),
        "y": (p * s * pauli_y, q * s * pauli_y),
        "z": (sp.diag(p, gamma - p), sp.diag(q - gamma, -q)),
    }
    for label, operator in (("x", pauli_x), ("y", pauli_y), ("z", pauli_z)):
        for bit in (0, 1):
            actual = instrument_image(bins[bit], operator)
            assert normalize(actual - expected_images[label][bit]) == sp.zeros(2)

    # Independently sum all sixteen hidden paths for the fixed history policy.
    disclosed_bit = (0, 1, 1, 0)
    recoveries = (identity, pauli_x)
    path_squares: list[sp.Expr] = []
    for a1 in range(4):
        first = recoveries[disclosed_bit[a1]]
        for a2 in range(4):
            final = recoveries[disclosed_bit[a1]]  # second recovery retains b1
            branch = final * kraus[a2] * first * kraus[a1]
            trace = sp.simplify(sp.trace(branch))
            path_squares.append(sp.expand_complex(trace * sp.conjugate(trace)))
    history = normalize(sum(path_squares) / 4)
    expected_history = 1 - gamma + p * gamma**2 / 2
    assert sp.simplify(history - expected_history) == zero

    # In 1-p <= gamma <= p, the Hermitian trace-norm sums give column caps
    # sqrt(1-gamma), sqrt(1-gamma), p.  The following expression is therefore
    # an upper bound for every two-stage current-bit CPTP policy.
    upper = sp.simplify((1 + 2 * (1 - gamma) + p**2) / 4)
    gap = sp.factor(history - upper)
    expected_gap = (1 - 2 * gamma + 2 * p * gamma**2 - p**2) / 4
    assert sp.simplify(gap - expected_gap) == zero

    p_minus = sp.Rational(71, 100)
    p_plus = sp.Rational(723, 1000)
    gamma_minus = sp.Rational(29, 100)
    gamma_plus = sp.Rational(303, 1000)
    epsilon = sp.Rational(1, 1000)

    # Closed-box domain and absolute-value chamber, including equality at the
    # lower-left corner gamma=1-p.
    chamber_lower_margin = sp.simplify(gamma_minus - (1 - p_minus))
    chamber_upper_margin = sp.simplify(p_minus - gamma_plus)
    assert 0 < p_minus < sp.Rational(18, 25) < p_plus < 1
    assert 0 < gamma_minus < sp.Rational(3, 10) < gamma_plus < 1
    assert chamber_lower_margin == zero
    assert chamber_upper_margin > 0

    # Exact monotonicity over the entire box.  These two positive margins show
    # dG/dp<0 and dG/dgamma<0 without sampling.
    dp_negative_margin = sp.simplify(p_minus - gamma_plus**2)
    dgamma_negative_margin = sp.simplify(sp.Rational(1, 2) - p_plus * gamma_plus)
    assert dp_negative_margin > 0
    assert dgamma_negative_margin > 0

    gap_min = sp.factor(gap.subs({p: p_plus, gamma: gamma_plus}))
    residual = sp.factor(gap_min - epsilon)
    assert residual > 0

    # Full Choi rank is uniform: K1 and K3 occupy distinct nonzero off-diagonal
    # matrix units, while the squared determinant of the two diagonal-coordinate
    # vectors from K0 and K2 is p(1-p)gamma^2.  A simple exact lower bound on the
    # box is positive (p(1-p) decreases for p>1/2).
    rank_margin = sp.factor(p_plus * (1 - p_plus) * gamma_minus**2)
    assert rank_margin > 0

    boundary_gap = sp.factor(gap.subs({p: p_minus, gamma: gamma_minus}))
    assert boundary_gap > epsilon

    # A strict rectangular superset obtained by keeping the lower sides and
    # expanding both upper sides to centre+1/200 remains in the same chamber but
    # fails this sufficient certificate at its upper corner.
    p0 = sp.Rational(18, 25)
    gamma0 = sp.Rational(3, 10)
    r_fail = sp.Rational(1, 200)
    larger_p = p0 + r_fail
    larger_gamma = gamma0 + r_fail
    larger_gap = sp.factor(gap.subs({p: larger_p, gamma: larger_gamma}))
    assert 1 - larger_p <= larger_gamma <= larger_p
    assert larger_gap < 0

    # Exact bracket for the first same-direction zero of the certificate.
    r_pass = sp.Rational(1, 225)
    bracket_positive = sp.factor(gap.subs({p: p0 + r_pass, gamma: gamma0 + r_pass}))
    bracket_negative = larger_gap
    assert bracket_positive > 0 > bracket_negative

    # Cross the lower absolute-value chamber at fixed gamma.  Here z=1-gamma,
    # so using z=p would be invalid even though the general certificate remains
    # positive at this diagnostic point.
    cross_p = sp.Rational(709, 1000)
    cross_gamma = sp.Rational(29, 100)
    assert cross_gamma < 1 - cross_p < cross_p
    cross_z = 1 - cross_gamma
    general_upper = (1 + 2 * (1 - cross_gamma) + cross_z**2) / 4
    cross_history = expected_history.subs({p: cross_p, gamma: cross_gamma})
    cross_gap = sp.factor(cross_history - general_upper)
    chamber_surrogate = sp.factor(gap.subs({p: cross_p, gamma: cross_gamma}))
    branch_overstatement = sp.factor(chamber_surrogate - cross_gap)
    assert cross_gap > 0
    assert branch_overstatement > 0

    print("arithmetic=exact_sympy")
    print("kraus_completeness=true")
    print("instrument_pauli_images=true")
    print(f"history_formula={history}")
    print(f"markov_upper_chamber={upper}")
    print(f"gap_polynomial={gap}")
    print(f"rectangle_p=[{p_minus},{p_plus}]")
    print(f"rectangle_gamma=[{gamma_minus},{gamma_plus}]")
    print(f"chamber_lower_margin={chamber_lower_margin}")
    print(f"chamber_upper_margin={chamber_upper_margin}")
    print(f"dp_negative_margin={dp_negative_margin}")
    print(f"dgamma_negative_margin={dgamma_negative_margin}")
    print(f"gap_min_upper_corner={gap_min}")
    print(f"uniform_epsilon={epsilon}")
    print(f"epsilon_residual={residual}")
    print(f"rank_margin_lower_bound={rank_margin}")
    print(f"touching_chamber_boundary_gap={boundary_gap}")
    print(f"strict_superset_p=[{p_minus},{larger_p}]")
    print(f"strict_superset_gamma=[{gamma_minus},{larger_gamma}]")
    print(f"strict_superset_upper_corner_gap={larger_gap}")
    print(f"same_direction_zero_bracket=({r_pass},{r_fail})")
    print(f"zero_bracket_gaps=({bracket_positive},{bracket_negative})")
    print(f"cross_chamber_point=({cross_p},{cross_gamma})")
    print(f"cross_chamber_z={cross_z}")
    print(f"cross_chamber_general_gap={cross_gap}")
    print(f"invalid_p_branch_overstatement={branch_overstatement}")
    print("certificate_status=pass")


if __name__ == "__main__":
    main()
