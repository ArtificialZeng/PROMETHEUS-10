#!/usr/bin/env python3
"""Exact two-sheet algebra and high-precision checks for the triad audit."""

from __future__ import annotations

import os
import sys

import mpmath as mp
import sympy as sp


def positive_frequency(k: mp.mpf, gravity: mp.mpf, tension: mp.mpf, gamma: mp.mpf) -> mp.mpf:
    return (-gamma + mp.sqrt(gamma * gamma + 4 * k * (gravity + tension * k * k))) / 2


def main() -> None:
    expected = os.environ.get("PHYSICS_PYTHON")
    if expected and os.path.realpath(sys.executable) != os.path.realpath(expected):
        raise RuntimeError(f"interpreter mismatch: {sys.executable} != {expected}")

    x, y, r, sigma = sp.symbols("k1 k2 r sigma", positive=True)
    gamma = sp.symbols("gamma", real=True)
    k3 = x + y
    a = sigma * x * (r + x**2)
    b = sigma * y * (r + y**2)
    c = sigma * k3 * (r + k3**2)
    ell = sp.factor(c - a - b)
    p = ell / 2
    n = sp.factor(ell**2 - 4 * a * b)
    qcap = sp.factor(c**2 - (a - b) ** 2)
    d2 = sp.factor(2 * ell * qcap)
    eliminated = sp.factor(d2 * gamma**2 - n**2)

    assert sp.simplify(ell - 3 * sigma * x * y * k3) == 0
    assert sp.simplify(d2 - 2 * ell * (c - a + b) * (c + a - b)) == 0

    # Complete real polynomial classification.  The epsilon=-1 solution is
    # a genuine negative-frequency sheet, not an extraneous gamma root.
    w1_plus = sp.sqrt(p) * (c + a - b) / sp.sqrt(qcap)
    w2_plus = sp.sqrt(p) * (c - a + b) / sp.sqrt(qcap)
    w3_plus = 2 * c * sp.sqrt(p) / sp.sqrt(qcap)
    gamma_plus = -n / sp.sqrt(d2)
    assert sp.simplify(w1_plus + w2_plus - w3_plus) == 0
    assert sp.simplify(2 * w1_plus * w2_plus - ell) == 0
    for w, q in ((w1_plus, a), (w2_plus, b), (w3_plus, c)):
        assert sp.simplify(w**2 + gamma_plus * w - q) == 0
    for w, q in ((-w1_plus, a), (-w2_plus, b), (-w3_plus, c)):
        assert sp.simplify(w**2 - gamma_plus * w - q) == 0

    # Algebraic value of C on the true resonance manifold.
    c_numerator = sp.factor(16 * a * b * (c - a) * (c - b) - ell**4)
    c_denominator = d2
    assert sp.simplify((4 * a * b / ell - n**2 / d2) - c_numerator / c_denominator) == 0

    A = 3 * x**2 + 3 * x * y + y**2
    B = x**2 + 3 * x * y + 3 * y**2
    coupling_poly = sp.factor(
        16 * (r + x**2) * (r + y**2) * (r + A) * (r + B)
        - 81 * x**2 * y**2 * (x + y) ** 4
    )
    assert sp.simplify(c_numerator - sigma**4 * x**2 * y**2 * coupling_poly) == 0
    at_zero = sp.factor(coupling_poly.subs(r, 0))
    assert sp.simplify(at_zero + x**2 * y**2 * (33 * (x + y) ** 4 - 16 * x**2 * y**2)) == 0

    # Martin (2017), Eqs. (3.6)-(3.8), with r=g/sigma and gamma_M=-gamma_here.
    e_m = x**3 + y**3 - k3**3
    a_m = 4 * x * y * r * (r + x**2 + y**2)
    zeta2_m = sp.factor(
        (e_m**2 - 4 * x**3 * y**3 - a_m) ** 2
        / (
            8
            * e_m
            * (
                e_m**2
                - 4 * x**3 * y**3
                + 2 * e_m * k3**3
                + 2 * k3 * r * e_m
                - a_m
            )
        )
    )
    assert sp.simplify(n**2 / d2 - 4 * sigma * zeta2_m) == 0

    print(f"python={sys.version.split()[0]}; sympy={sp.__version__}; mpmath={mp.__version__}")
    print(f"ell_factor={ell}")
    print(f"N_factor={n}")
    print(f"D2_factor={d2}")
    print("eliminated_polynomial=D*gamma**2-N**2")
    print("positive_frequency_sheet:epsilon=+1,gamma=-N/sqrt(D)")
    print("negative_frequency_sheet:epsilon=-1,gamma=+N/sqrt(D)")
    print("complete_two_sheet_frequency_formula_verified=True")
    print("C_on_resonance_numerator=16*a*b*(c-a)*(c-b)-ell**4")
    print("coupling_zero_polynomial=16*(r+k1**2)*(r+k2**2)*(r+3*k1**2+3*k1*k2+k2**2)*(r+k1**2+3*k1*k2+3*k2**2)-81*k1**2*k2**2*(k1+k2)**4")
    print(f"coupling_polynomial_at_r_zero={at_zero}")
    print(f"coupling_polynomial_dr={sp.factor(sp.diff(coupling_poly, r))}")
    print("martin_2017_squared_formula_difference=0")

    # Exact back-substitution for the diagnostic pair from the intake.
    av = a.subs({x: 1, y: 3, r: 1, sigma: 1})
    bv = b.subs({x: 1, y: 3, r: 1, sigma: 1})
    cv = c.subs({x: 1, y: 3, r: 1, sigma: 1})
    lv = ell.subs({x: 1, y: 3, r: 1, sigma: 1})
    nv = n.subs({x: 1, y: 3, r: 1, sigma: 1})
    d2v = d2.subs({x: 1, y: 3, r: 1, sigma: 1})
    gv = sp.simplify(-nv / sp.sqrt(d2v))
    ws = [sp.simplify((-gv + sp.sqrt(gv**2 + 4 * q)) / 2) for q in (av, bv, cv)]
    exact_residual = sp.simplify(ws[0] + ws[1] - ws[2])
    exact_dispersion = [sp.simplify(w**2 + gv * w - q) for w, q in zip(ws, (av, bv, cv))]
    exact_c = sp.simplify(gv**2 + 2 * gv * ws[2] + 2 * ws[0] * ws[1])
    gmirror = -gv
    wnegative = tuple(-w for w in ws)
    negative_dispersion = [
        sp.simplify(w**2 + gmirror * w - q)
        for w, q in zip(wnegative, (av, bv, cv))
    ]
    negative_residual = sp.simplify(wnegative[0] + wnegative[1] - wnegative[2])
    negative_c = sp.simplify(
        gmirror**2 + 2 * gmirror * wnegative[2] + 2 * wnegative[0] * wnegative[1]
    )
    positive_at_companion = [
        sp.simplify((-gmirror + sp.sqrt(gmirror**2 + 4 * q)) / 2)
        for q in (av, bv, cv)
    ]
    positive_at_companion_residual = sp.simplify(
        positive_at_companion[0] + positive_at_companion[1] - positive_at_companion[2]
    )
    w1s, w2s, gs = sp.symbols("omega1 omega2 gamma")
    groebner = sp.groebner(
        [
            w1s**2 + gs * w1s - av,
            w2s**2 + gs * w2s - bv,
            (w1s + w2s) ** 2 + gs * (w1s + w2s) - cv,
        ],
        w1s,
        w2s,
        gs,
        order="lex",
    )
    groebner_basis = tuple(sp.factor(poly.as_expr()) for poly in groebner.polys)
    print(f"exact_case_q={(av, bv, cv)}; ell={lv}; N={nv}; D2={d2v}")
    print(f"exact_case_gamma={gv}")
    print(f"exact_case_frequencies={tuple(ws)}")
    print(f"exact_case_dispersion_residuals={tuple(exact_dispersion)}")
    print(f"exact_case_resonance_residual={exact_residual}")
    print(f"exact_case_C={exact_c}")
    print(f"exact_case_denominators={tuple(sp.simplify(2*w+gv) for w in ws)}")
    print(f"sign_reversed_case_gamma={gmirror}")
    print(f"sign_reversed_case_frequencies={wnegative}")
    print(f"sign_reversed_case_dispersion_residuals={tuple(negative_dispersion)}")
    print(f"sign_reversed_case_resonance_residual={negative_residual}")
    print(f"sign_reversed_case_C={negative_c}")
    print(f"exact_case_groebner_basis={groebner_basis}")
    print(f"positive_roots_at_companion_gamma_residual={positive_at_companion_residual}")

    # Independent high-precision evaluation for the unique coupling-zero ratio.
    mp.mp.dps = 80
    for k1v, k2v in ((mp.mpf(1), mp.mpf(3)), (mp.mpf(2), mp.mpf(5)), (mp.mpf(3) / 2, mp.mpf(7) / 3)):
        A_v = 3 * k1v**2 + 3 * k1v * k2v + k2v**2
        B_v = k1v**2 + 3 * k1v * k2v + 3 * k2v**2

        def p_couple(rv: mp.mpf) -> mp.mpf:
            return (
                16
                * (rv + k1v**2)
                * (rv + k2v**2)
                * (rv + A_v)
                * (rv + B_v)
                - 81 * k1v**2 * k2v**2 * (k1v + k2v) ** 4
            )

        lo = mp.mpf(0)
        hi = (k1v + k2v) ** 2
        while p_couple(hi) <= 0:
            hi *= 2
        for _ in range(400):
            mid = (lo + hi) / 2
            if p_couple(mid) < 0:
                lo = mid
            else:
                hi = mid
        rv = (lo + hi) / 2
        gravity = rv
        tension = mp.mpf(1)
        q1v = k1v * (gravity + tension * k1v**2)
        q2v = k2v * (gravity + tension * k2v**2)
        q3v = (k1v + k2v) * (gravity + tension * (k1v + k2v) ** 2)
        ellv = q3v - q1v - q2v
        nv = ellv**2 - 4 * q1v * q2v
        d2v = 2 * ellv * (q3v**2 - (q1v - q2v) ** 2)
        gammav = -nv / mp.sqrt(d2v)
        w1v = positive_frequency(k1v, gravity, tension, gammav)
        w2v = positive_frequency(k2v, gravity, tension, gammav)
        w3v = positive_frequency(k1v + k2v, gravity, tension, gammav)
        residual = w1v + w2v - w3v
        cvv = gammav**2 + 2 * gammav * w3v + 2 * w1v * w2v
        dispersions = (
            w1v**2 + gammav * w1v - q1v,
            w2v**2 + gammav * w2v - q2v,
            w3v**2 + gammav * w3v - q3v,
        )
        print(
            "holdout="
            f"k1:{mp.nstr(k1v, 20)},k2:{mp.nstr(k2v, 20)},"
            f"r_interval:[{mp.nstr(lo, 28)},{mp.nstr(hi, 28)}],"
            f"gamma:{mp.nstr(gammav, 28)},R:{mp.nstr(residual, 8)},"
            f"C:{mp.nstr(cvv, 8)},disp:{tuple(mp.nstr(z, 8) for z in dispersions)},"
            f"min_omega:{mp.nstr(min(w1v,w2v,w3v), 20)},"
            f"min_denom:{mp.nstr(min(2*w1v+gammav,2*w2v+gammav,2*w3v+gammav),20)}"
        )

    print("EXACT_TWO_SHEET_IDENTITIES_AND_BACKSUBSTITUTION_PASS")


if __name__ == "__main__":
    main()
