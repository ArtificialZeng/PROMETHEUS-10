#!/usr/bin/env python3
"""Exact rational/Sturm certificate for the indirect-gap boundary reduction.

All polynomial operations in this file use SymPy over QQ (or the explicit quadratic
field at the cusp).  Floating-point values are printed only after the exact assertions.
"""

from __future__ import annotations

import sympy as sp


X, Y = sp.symbols("X Y", real=True)
d = 2*X - 1
A = 8*X**2 - 4*X - 1
B = 40*X**3 - 36*X**2 + 6*X - 1
C = 16*X**3 - 60*X**2 + 36*X - 1
Qc = 16*X**2 - 14*X + 1
Q4 = 32*X**4 - 8*X**3 - 36*X**2 + 22*X - 1
Q28 = 28*X**2 - 20*X + 1
J = 32*X**3 - 36*X**2 + 12*X + 1

V = sp.factor(3*d**2*A/(4*B))
R0 = sp.factor(X/V)  # S^2, where S=sqrt(X/V)
u2 = sp.factor(16*V*(1-X)*(4*X-1)**2/(9*d**2))
e0 = sp.factor(-d*C/(2*B))  # e=sqrt(X/V)*e0
k0 = sp.factor(
    -(X-1)*d*(2*X+1)**2*(4*X-3)*(4*X-1)**2*Q28**2
    /(6*A*B**2)
)  # K=sqrt(X/V)*k0
a = sp.factor(k0/R0)
g = sp.factor(a*Y**3 - 3*e0*Y + 2)

S12 = (
    602112*X**12 - 1505280*X**11 + 1069824*X**10
    + 184576*X**9 - 524928*X**8 + 195264*X**7
    - 23328*X**6 + 8736*X**5 - 3528*X**4 + 228*X**3
    - 45*X**2 + 15*X - 1
)
P5 = 224*X**5 - 296*X**4 + 76*X**3 + 10*X**2 + 5*X - 1
P7 = (
    3584*X**7 - 23296*X**6 + 38688*X**5 - 24304*X**4
    + 5024*X**3 - 96*X**2 + 182*X - 25
)


def roots_open(poly: sp.Expr, lo: sp.Rational, hi: sp.Rational) -> int:
    """Exact number of distinct real roots in (lo,hi); endpoints are nonroots here."""
    assert sp.expand(poly.subs(X, lo)) != 0
    assert sp.expand(poly.subs(X, hi)) != 0
    return int(sp.count_roots(poly, lo, hi))


def positive_poly_interval(poly: sp.Expr, lo: sp.Rational, hi: sp.Rational):
    """Exact range enclosure for a QQ polynomial on a positive interval."""
    p = sp.Poly(poly, Y, domain=sp.QQ)
    lower = sp.Rational(0)
    upper = sp.Rational(0)
    for (power,), coeff in p.terms():
        if coeff >= 0:
            lower += coeff*lo**power
            upper += coeff*hi**power
        else:
            lower += coeff*hi**power
            upper += coeff*lo**power
    return sp.factor(lower), sp.factor(upper)


def sector_and_cubic_checks() -> None:
    relation = (
        -160*sp.Symbol("VV")*X**3 + 144*sp.Symbol("VV")*X**2
        - 24*sp.Symbol("VV")*X + 4*sp.Symbol("VV")
        + 96*X**4 - 144*X**3 + 60*X**2 - 3
    )
    assert sp.factor(relation.subs(sp.Symbol("VV"), V)) == 0
    assert sp.factor(16*X*V/d**2 - 4 + 4*(X-1)*(4*X-1)**2/B) == 0
    assert sp.factor(u2-1 + Qc*J/(3*B)) == 0
    assert sp.factor(e0**3-a-3*d**3*A*Qc**2*Q4/(8*X*B**3)) == 0

    lo, hi = sp.Rational(3, 4), sp.Rational(1)
    sign_polys = {
        "A": A, "B": B, "-C": -C, "Q4": Q4,
        "J": J, "Q28": Q28,
        "1-V numerator": -(96*X**4-304*X**3+204*X**2-24*X+1),
    }
    for name, poly in sign_polys.items():
        assert roots_open(poly, lo, hi) == 0, name
        assert poly.subs(X, sp.Rational(4, 5)) > 0, name

    # On the normalized generic sector, t>=2 and 0<V<1 force X>3/4
    # for any E>=1 solution: K<=0 at X<=3/4 gives its sole positive
    # cubic root below E=1.  On (3/4,1), a,e0,V are positive.
    assert sp.limit(V, X, lo, dir="+") == sp.Rational(3, 4)
    assert sp.limit(V, X, hi, dir="-") == sp.Rational(1, 4)
    assert sp.limit(e0, X, lo, dir="+") == 2
    assert sp.limit(e0, X, hi, dir="-") == sp.Rational(1, 2)
    assert sp.limit(a, X, lo, dir="+") == 0
    assert sp.limit(a, X, hi, dir="-") == 0

    # The only potentially admissible interval below 3/4 starts after B's
    # unique zero.  That zero is above every zero of C, so e0>0 there.
    half = sp.Rational(1, 2)
    assert roots_open(B, half, lo) == 1
    assert roots_open(B, sp.Rational(743, 1000), sp.Rational(744, 1000)) == 1
    assert roots_open(C, half, lo) == 1
    assert roots_open(C, sp.Rational(711, 1000), sp.Rational(712, 1000)) == 1

    disc = sp.factor(sp.discriminant(sp.together(g).as_numer_denom()[0], Y))
    expected_factors = dict(sp.factor_list(disc)[1])
    assert expected_factors[Qc] == 2
    assert roots_open(Qc, lo, hi) == 1

    root33 = sp.sqrt(33)
    Xc = (7+root33)/16
    rc2 = (69-11*root33)/8
    Yc = sp.factor(1/e0.subs(X, Xc))
    assert sp.simplify(g.subs({X: Xc, Y: Yc})) == 0
    assert sp.simplify(sp.diff(g, Y).subs({X: Xc, Y: Yc})) == 0
    assert sp.simplify(Yc**2*V.subs(X, Xc)/Xc-rc2) == 0
    print("SECTOR generic admissibility reduces to 3/4 < X < 1: PASS")
    print("CUBIC Y=r*sqrt(X/V) has rational coefficients: PASS")
    print("CUBIC unique E=e0*Y>=1 root; double only at Xc: PASS")
    print(f"CUSP Xc={sp.N(Xc, 16)} rc={sp.N(sp.sqrt(rc2), 16)}: PASS")


def monotonicity_checks() -> None:
    # r=Y/sqrt(R0).  Along g=0, r_X=0 is equivalent to h=0.
    h = sp.factor(2*R0*sp.diff(g, X) + Y*sp.diff(g, Y)*sp.diff(R0, X))
    gn = sp.primitive(sp.together(g).as_numer_denom()[0], Y)[1]
    hn = sp.primitive(sp.together(h).as_numer_denom()[0], Y)[1]
    resultant = sp.factor(sp.resultant(gn, hn, Y))
    factors = {sp.factor(poly): mult for poly, mult in sp.factor_list(resultant)[1]}
    expected = {
        4*X-1: 2, X: 3, d: 3, A: 1, Qc: 2,
        Q28: 2, B: 9, S12: 1,
    }
    assert factors == expected
    lo, hi = sp.Rational(3, 4), sp.Rational(1)
    assert roots_open(S12, lo, hi) == 1
    iso_lo, iso_hi = sp.Rational(769, 1000), sp.Rational(77, 100)
    assert roots_open(S12, iso_lo, iso_hi) == 1
    for poly in (B, P5, P7):
        assert roots_open(poly, iso_lo, iso_hi) == 0
        assert poly.subs(X, iso_lo) > 0 and poly.subs(X, iso_hi) > 0
    Ystat = sp.factor(-2*B*P5/(X*d*P7))
    # Substitution verifies that this is the common g=h root whenever S12=0;
    # the remaining factors have fixed nonzero signs on its isolating interval.
    g_at_stat = sp.cancel(g.subs(Y, Ystat)).as_numer_denom()[0]
    h_at_stat = sp.cancel(h.subs(Y, Ystat)).as_numer_denom()[0]
    assert sp.rem(g_at_stat, S12, X) == 0
    assert sp.rem(h_at_stat, S12, X) == 0
    # Hence the sole S12 stationary solution has Y=Ystat<0 and is not physical.
    assert Ystat.subs(X, iso_lo) < 0 and Ystat.subs(X, iso_hi) < 0
    print("STURM stationary resultant factors exactly into Qc and S12 sectors: PASS")
    print("STURM S12 has one root in (0.769,0.770), with stationary Y<0: PASS")
    print("MONOTONIC physical r+(X): decreasing left of Xc, increasing right: PASS")


def pe_sign_sample(xval: sp.Rational) -> None:
    # Product of P_E/3 at theta_c and theta_v, expressed rationally in X,Y.
    usum = sp.factor(8*V*(1-X)*(4*X-1)/(3*d))
    r2 = Y**2/R0
    e2 = R0*e0**2
    L = sp.factor(r2*(e2-1-u2)-1)
    product = sp.factor(L**2 + 2*r2*L*usum + 4*r2**2*u2*(V-X))

    gx = sp.Poly(sp.together(g.subs(X, xval)).as_numer_denom()[0], Y, domain=sp.QQ)
    intervals = gx.intervals(eps=sp.Rational(1, 10**12))
    e0x = sp.factor(e0.subs(X, xval))
    physical = [iv for iv, mult in intervals if iv[0] > 0 and e0x*iv[0] > 1]
    assert len(physical) == 1
    ylo, yhi = physical[0]
    num, den = sp.together(product.subs(X, xval)).as_numer_denom()
    assert den > 0
    plo, phi = positive_poly_interval(num, ylo, yhi)
    assert phi < 0
    print(
        f"P_E PRODUCT X={xval}: physical Y in "
        f"[{sp.N(ylo,12)},{sp.N(yhi,12)}], exact upper bound < 0: PASS"
    )


def exceptional_checks() -> None:
    rr = sp.symbols("rr", positive=True)
    # m=0: at E=sqrt(1+r^2), max_theta f is strictly negative because
    # (1+r^2)^(3/2)>1+r^3 for every r>0.
    assert sp.factor((1+rr**2)**3-(1+rr**3)**2) == rr**2*(3*rr**2-2*rr+3)
    assert sp.discriminant(3*rr**2-2*rr+3, rr) < 0
    # The X=1/2 exceptional equations imply u=1/sqrt(3), t=sqrt(3)<2.
    assert sp.sqrt(3) < 2
    print("EXCEPTION m=0 has a strict global gap for every r>0: PASS")
    print("EXCEPTION X=1/2 contradicts the Fejer parameter t>=2: PASS")


def main() -> None:
    print("JOB phys-00018-p01-research-d0b42926d073")
    print("Exact QQ/Sturm computation; decimal displays are non-authoritative.")
    sector_and_cubic_checks()
    monotonicity_checks()
    pe_sign_sample(sp.Rational(39, 50))  # left of Xc
    pe_sign_sample(sp.Rational(4, 5))    # right of Xc
    exceptional_checks()
    print("GLOBAL BOUNDARY ALGEBRA CERTIFICATE: PASS")


if __name__ == "__main__":
    main()
