"""Read accepted data and verify manuscript tables exactly, without mutating it.

This is an algebra/table check, not a fresh source reconstruction or referee.
"""
from pathlib import Path
from fractions import Fraction
import json
import math
import platform
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]


def main():
    result = {
        "purpose": "Read-only checks of accepted data used by the manuscript",
        "python": sys.version,
        "platform": platform.platform(),
        "sympy": sp.__version__,
        "finite_checks": [],
    }
    for k in [7, 8]:
        a = json.loads((ROOT / f"evidence/research/sym{k}-input-a.json").read_text())
        b = json.loads((ROOT / f"evidence/research/sym{k}-input-b.json").read_text())
        assert a["ranks"] == b["ranks"]
        assert a["cross_gram"] == b["cross_gram"]
        d = math.comb(k + 7, 7)
        assert a["dimension"] == b["dimension"] == d == sum(a["ranks"])
        gram = sp.diag(*a["ranks"])
        cross = sp.Matrix(a["cross_gram"])
        overlap = gram.inv() * cross
        assert cross == cross.T
        one = sp.ones(len(a["ranks"]), 1)
        global_projection = one * (one.T * gram) / d
        assert global_projection**2 == global_projection
        assert overlap * global_projection == global_projection * overlap == global_projection
        expected = {sp.Rational(6, (r + 2) * (2 * r + 3)): 1
                    for r in range(k//2 + 1)}
        assert overlap.eigenvals() == expected
        assert (overlap-global_projection).eigenvals() == {
            sp.Integer(0): 1, **{c: n for c, n in expected.items() if c != 1}}
        result["finite_checks"].append({
            "k": k, "dimension": d, "ranks": a["ranks"],
            "nonfixed_angles": [str(c) for c in sorted(expected, reverse=True) if c != 1],
            "complete_identity_subtraction": True,
        })
    x = sp.Symbol("x", nonnegative=True)
    weight = sp.Rational(105, 16) * sp.sqrt(x) * (1-x)**2
    assert sp.integrate(weight, (x, 0, 1)) == 1
    assert sp.integrate(x * weight, (x, 0, 1)) == sp.Rational(1, 3)
    p = [sp.jacobi(r, 2, sp.Rational(1, 2), 2*x-1) for r in range(3)]
    conditional = [sp.Integer(1), sp.Rational(1, 5)+sp.Rational(2, 5)*x,
                   sp.Rational(1, 14)+x/7+sp.Rational(3, 14)*x**2]
    for r, poly in enumerate(p):
        transformed = sum(sp.Poly(poly, x).nth(j)*conditional[j] for j in range(r+1))
        assert sp.expand(transformed-sp.Rational(6, (r+2)*(2*r+3))*poly) == 0
        for s in range(r):
            assert sp.integrate(sp.expand(poly*p[s])*weight, (x, 0, 1)) == 0
    R = sp.Symbol("R", nonnegative=True)
    n = sp.Symbol("n", integer=True, nonnegative=True)
    moment = sp.integrate(12*R**(2*n+2)*(1-R), (R, 0, 1))
    assert sp.simplify(moment-6/((n+2)*(2*n+3))) == 0
    result.update({"weight_normalized": True, "purity_mean_t": "1/3",
                   "conditional_formulas_checked": True,
                   "general_radial_moment_identity": True,
                   "limitation": "Reads saved A/B data and checks algebra; does not reconstruct Haar inputs or certify novelty/independence."})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
