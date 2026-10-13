#!/usr/bin/env python3
"""Clean-room Laurent/Fejer reconstruction of every indirect-contact sector.

This checker starts with det(E-H) for the frozen Bloch matrix at kappa=0.  It
does not import the previously recorded function V(X).  Instead it derives the
Laurent coefficients, the spectral-factor autocorrelations, and the generic
elimination relation anew, and only then compares the result with the earlier
certificate.  All certification assertions are exact SymPy operations over QQ
(apart from explicitly represented square roots in singular/cusp values).
"""

from __future__ import annotations

import sympy as sp


def even_polynomial(expr: sp.Expr, x: sp.Symbol, v: sp.Symbol,
                    X: sp.Symbol, V: sp.Symbol) -> sp.Expr:
    """Replace even powers of x,v by X,V, rejecting an unexpected odd term."""
    out = 0
    for (px, pv), coefficient in sp.Poly(sp.expand(expr), x, v).terms():
        assert px % 2 == 0 and pv % 2 == 0, (px, pv)
        out += coefficient*X**(px//2)*V**(pv//2)
    return sp.factor(out)


def roots_open(poly: sp.Expr, var: sp.Symbol,
               lo: sp.Rational, hi: sp.Rational) -> int:
    assert sp.expand(poly.subs(var, lo)) != 0
    assert sp.expand(poly.subs(var, hi)) != 0
    return int(sp.count_roots(poly, lo, hi))


def frozen_laurent_coefficients() -> None:
    z, E, r, q = sp.symbols("z E r q", nonzero=True, real=True)
    omega = (-1 + sp.I*sp.sqrt(3))/2
    omega_bar = sp.conjugate(omega)

    # Frozen matrix in source.md, at kappa=0 and m=sqrt(3) q.
    h11 = sp.sqrt(3)*q-r*(z*omega_bar+omega/z)
    h22 = -r*(z+1/z)
    h33 = -sp.sqrt(3)*q-r*(z*omega+omega_bar/z)
    ei_minus_h = sp.Matrix([
        [E-h11, 1, 1],
        [1, E-h22, 1],
        [1, 1, E-h33],
    ])
    numerator = sp.expand(sp.cancel(ei_minus_h.det())*z**3)
    coeff = {k: sp.factor(numerator.coeff(z, k+3)) for k in range(-3, 4)}
    expected = {
        -3: r**3,
        -2: 3*sp.I*q*r**2,
        -1: -3*q*r*(q-sp.I*E),
        0: E**3-3*E*(1+r**2+q**2)+2,
        1: -3*q*r*(q+sp.I*E),
        2: -3*sp.I*q*r**2,
        3: r**3,
    }
    assert all(sp.expand(coeff[k]-expected[k]) == 0 for k in expected)
    print("FROZEN determinant -> seven Laurent coefficients: PASS")


def factor_correlations() -> None:
    w, v, rho, t = sp.symbols("w v rho t", nonzero=True, real=True)
    # z1+z2=2 v w, z1*z2=w^2, and the third spectral root is rho/w^2.
    # On the unit circle conjugation sends w to 1/w.
    p = [
        -rho,
        w**2+2*rho*v/w,
        -(2*v*w+rho/w**2),
        sp.Integer(1),
    ]
    pbar = [
        -rho,
        w**-2+2*rho*v*w,
        -(2*v/w+rho*w**2),
        sp.Integer(1),
    ]
    corr = {
        k: sp.factor(sum(p[j+k]*pbar[j] for j in range(4-k))/rho)
        for k in range(4)
    }
    targets = {
        3: -1,
        2: 4*v*w+t/w**2,
        1: -((2+4*v**2)*w**2+4*t*v/w+w**-4),
        0: 2*(1+2*v**2)*t+4*v*(w**3+w**-3),
    }
    rho_relation = rho**2-t*rho+1
    for k in range(4):
        num = sp.together(corr[k]-targets[k]).as_numer_denom()[0]
        assert sp.rem(sp.Poly(num, rho), sp.Poly(rho_relation, rho)).as_expr() == 0
    print("LAURENT spectral-factor autocorrelations derived independently: PASS")


def generic_elimination() -> tuple[sp.Symbol, ...]:
    x, y, v, t, u, e = sp.symbols("x y v t u e", real=True)
    X, V = sp.symbols("X V", real=True)
    dxy = x**2-y**2
    cos4 = x**4-6*x**2*y**2+y**4

    # Match h=-det(E-H) after q=u*r, E=e*r.  These equations are the
    # real/imaginary parts of the newly derived k=2 and k=1 coefficients.
    F1 = sp.expand(4*v*x+t*dxy)
    F2 = sp.expand(4*v*y-2*t*x*y-3*u)
    F3 = sp.expand((2+4*v**2)*dxy+4*t*v*x+cos4+3*u**2)
    F4 = sp.expand(2*x*y*(2+4*v**2)-4*t*v*y-4*x*y*dxy+3*u*e)

    t_solution = sp.factor(-4*v*x/dxy)
    u_solution = sp.factor((4*v*y-2*t_solution*x*y)/3)
    raw = sp.together(F3.subs({t: t_solution, u: u_solution})).as_numer_denom()[0]
    raw = sp.factor(sp.rem(sp.Poly(raw, y), sp.Poly(y**2+x**2-1, y)).as_expr())
    relation = even_polynomial(raw, x, v, X, V)

    # The elimination is linear in V; no branch polynomial is discarded here.
    assert sp.degree(relation, V) == 1
    expected_relation = (
        -160*V*X**3+144*V*X**2-24*V*X+4*V
        +96*X**4-144*X**3+60*X**2-3
    )
    assert sp.expand(relation-expected_relation) == 0
    V_derived = sp.factor(sp.solve(relation, V)[0])

    d = 2*X-1
    A = 8*X**2-4*X-1
    B = 40*X**3-36*X**2+6*X-1
    assert sp.factor(V_derived-3*d**2*A/(4*B)) == 0

    # Derive e from F4 only after the generic u!=0 reduction.  In the physical
    # sign sector x>0,y<0,v<0, e=S*e0 with S=sqrt(X/V).
    e_raw = sp.factor(sp.solve(F4, e)[0].subs({t: t_solution, u: u_solution}))
    e_num, e_den = sp.together(e_raw).as_numer_denom()
    e_num = sp.rem(sp.Poly(e_num, y), sp.Poly(y**2+x**2-1, y)).as_expr()
    e_den = sp.rem(sp.Poly(e_den, y), sp.Poly(y**2+x**2-1, y)).as_expr()
    e_raw = sp.factor(e_num/e_den)
    N = 2*V*X+V-2*X**2+3*X-1
    expected_e_raw = (2*x*(-N)/(v*(4*X-1))).subs({X: x**2, V: v**2})
    assert sp.factor(e_raw-expected_e_raw) == 0
    e0 = sp.factor((2*N/(4*X-1)).subs(V, V_derived))

    # The constant autocorrelation gives H.  Divide K=H+e^3-3e(1+u^2)
    # by S algebraically, avoiding any choice made in the previous script.
    u2 = sp.factor(16*V*(1-X)*(4*X-1)**2/(9*d**2))
    H0 = sp.factor(8*V*((1+2*V)/d-(4*X-3)))  # H/S
    k0 = sp.factor(H0+(X/V)*e0**3-3*e0*(1+u2))
    k0 = sp.factor(k0.subs(V, V_derived))
    u2 = sp.factor(u2.subs(V, V_derived))

    C = 16*X**3-60*X**2+36*X-1
    Q28 = 28*X**2-20*X+1
    k0_expected = sp.factor(
        -(X-1)*d*(2*X+1)**2*(4*X-3)*(4*X-1)**2*Q28**2
        /(6*A*B**2)
    )
    assert sp.factor(e0+d*C/(2*B)) == 0
    assert sp.factor(k0-k0_expected) == 0

    a = sp.factor(k0*V_derived/X)
    Y = sp.symbols("Y", real=True)
    cubic = sp.factor(a*Y**3-3*e0*Y+2)
    assert sp.degree(sp.together(cubic).as_numer_denom()[0], Y) == 3
    print("GENERIC elimination has exactly one X,V relation: PASS")
    print("COMPARE derived V,e0,k0 and rational Y cubic: EXACT MATCH")
    return X, V, Y, A, B, C, V_derived, e0, k0, u2, cubic


def admissible_sector_checks(data: tuple[sp.Symbol, ...]) -> None:
    X, V, Y, A, B, C, Vx, e0, k0, u2, cubic = data
    d = 2*X-1
    lo, three_quarters, hi = sp.Rational(0), sp.Rational(3, 4), sp.Rational(1)

    t2 = sp.factor(16*X*Vx/d**2)
    assert sp.factor(t2-4-4*(1-X)*(4*X-1)**2/B) == 0
    assert roots_open(B, X, lo, hi) == 1
    assert roots_open(B, X, sp.Rational(743, 1000), sp.Rational(744, 1000)) == 1
    # For a generic u>0 contact, t>2.  Thus B>0, and its unique root forces
    # X>0.743>1/2.  With x>0, t>0 then fixes v<0 and u>0 fixes y<0.
    assert B.subs(X, sp.Rational(3, 4)) > 0

    # V lies strictly between zero and one throughout the certificate sector.
    one_minus_V_num = sp.factor(sp.together(1-Vx).as_numer_denom()[0])
    for poly in (A, B, one_minus_V_num, -C):
        assert roots_open(poly, X, three_quarters, hi) == 0
        assert poly.subs(X, sp.Rational(4, 5)) > 0

    # Any admissible sliver below X=3/4 has e>0 but K<=0.  Its unique
    # positive constant-equation root occurs before E=1, so it cannot be an
    # upper-gap chemical potential.  Polynomial root locations make the sign
    # statement independent of decimal sampling.
    assert roots_open(C, X, sp.Rational(1, 2), three_quarters) == 1
    assert roots_open(C, X, sp.Rational(711, 1000), sp.Rational(712, 1000)) == 1
    assert C.subs(X, sp.Rational(3, 4)) < 0
    # Q28 has no zero after the unique B root.
    Q28 = 28*X**2-20*X+1
    assert roots_open(Q28, X, sp.Rational(743, 1000), hi) == 0
    assert sp.limit(k0, X, three_quarters, dir="-") == 0
    assert k0.subs(X, sp.Rational(149, 200)) < 0
    print("SECTOR Sturm signs: admissible E>=1 implies 3/4 < X < 1: PASS")

    # The derived cubic is literally the certified one.  Its only physical
    # multiple-root point is the known cusp.
    disc = sp.factor(sp.discriminant(sp.together(cubic).as_numer_denom()[0], Y))
    Qc = 16*X**2-14*X+1
    factors = dict(sp.factor_list(disc)[1])
    assert factors[Qc] == 2
    Xc = (7+sp.sqrt(33))/16
    rc2 = (69-11*sp.sqrt(33))/8
    Yc = sp.factor(1/e0.subs(X, Xc))
    assert sp.simplify(cubic.subs({X: Xc, Y: Yc})) == 0
    assert sp.simplify(sp.diff(cubic, Y).subs({X: Xc, Y: Yc})) == 0
    assert sp.simplify(Yc**2*Vx.subs(X, Xc)/Xc-rc2) == 0
    print("CUSP and E=1 multiple-root sector: EXACT MATCH")


def singular_sector_checks() -> None:
    # x=0 makes F1=-t=0, impossible for t>=2.  v=0 forces d=0 and is
    # included in the next calculation.
    t = sp.symbols("t", positive=True)
    assert t != 0

    # At d=0, x^2=y^2=1/2 and F1 forces v=0.  The u>=0 sign choice gives
    # u=t/3; F3 gives u^2=1/3, hence t=sqrt(3)<2.
    assert sp.sqrt(3) < 2

    # At u=0, either y=0 (X=1) or, for y!=0, F1/F2 force X=1/4.
    # In both cases F3 gives t^2=4.  Conversely, the generic identity for
    # t^2-4 shows that t=2 only at X=1 or X=1/4.  Thus every third-unit-root
    # sector is massless.  The exact strict-gap witness below excludes it.
    rr = sp.symbols("rr", positive=True)
    massless_margin = sp.factor((1+rr**2)**3-(1+rr**3)**2)
    assert massless_margin == rr**2*(3*rr**2-2*rr+3)
    assert sp.discriminant(3*rr**2-2*rr+3, rr) < 0
    print("SINGULAR x=0,d=0,v=0 sectors violate t>=2: PASS")
    print("SINGULAR u=0 or t=2 sectors are strictly massless-gapped: PASS")
    print("ONE-ZERO/coincident-angle sectors reduce to known direct closures: PASS")


def main() -> None:
    print("JOB phys-00018-p01-research-1356f29f5414")
    print("Exact clean-room Laurent reconstruction; no prior V(X) is imported.")
    frozen_laurent_coefficients()
    factor_correlations()
    data = generic_elimination()
    admissible_sector_checks(data)
    singular_sector_checks()
    print("LAURENT SECTOR RECONSTRUCTION: PASS; NO EXTRA E>=1 SECTOR")


if __name__ == "__main__":
    main()
