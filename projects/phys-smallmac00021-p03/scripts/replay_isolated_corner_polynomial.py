#!/usr/bin/env python3
"""Independent exact replay of the 15-site t=0 corner certificate.

This checker does not import SymPy or the reconstruction script.  It uses a
direct core adjacency, exact Faddeev-LeVerrier characteristic polynomials at
16 integer interpolation points, and rational Newton interpolation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
N = 15
ON = [(0, 1), (0, 2), (1, 2), (3, 4), (5, 7), (6, 8), (11, 13)]
OFF = [(1, 3), (2, 5), (4, 6), (7, 11), (8, 9), (8, 12), (10, 13), (13, 14)]
FIXED = [(9, 12), (10, 14)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matmul(a, b):
    n = len(a)
    out = [[Q(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                aik = a[i][k]
                for j in range(n):
                    if b[k][j]:
                        out[i][j] += aik * b[k][j]
    return out


def hamiltonian(lam):
    h = [[Q(0) for _ in range(N)] for _ in range(N)]
    for edges, weight in ((ON, lam), (OFF, 1 - lam), (FIXED, Q(1))):
        for i, j in edges:
            h[i][j] = h[j][i] = -weight
    return h


def charpoly_coefficients(lam):
    """Descending coefficients of det(EI-H), exact Faddeev-LeVerrier."""
    a = hamiltonian(lam)
    b = [[Q(int(i == j)) for j in range(N)] for i in range(N)]
    result = [Q(1)]
    for k in range(1, N + 1):
        ab = matmul(a, b)
        ck = -sum(ab[i][i] for i in range(N)) / k
        result.append(ck)
        b = ab
        for i in range(N):
            b[i][i] += ck
    return result


def poly_add(a, b):
    out = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] += x
    while len(out) > 1 and out[-1] == 0: out.pop()
    return out


def poly_mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i + j] += x * y
    while len(out) > 1 and out[-1] == 0: out.pop()
    return out


def poly_scale(a, q):
    return [q * x for x in a]


def interpolate_at_consecutive_integers(values):
    """Power-basis polynomial through p(0),...,p(15), via Newton differences."""
    first = []
    row = list(values)
    while row:
        first.append(row[0])
        row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    answer = [Q(0)]
    binomial_basis = [Q(1)]
    for k, delta in enumerate(first):
        answer = poly_add(answer, poly_scale(binomial_basis, delta))
        binomial_basis = poly_scale(poly_mul(binomial_basis, [Q(-k), Q(1)]), Q(1, k + 1))
    return answer


def polyval(a, x):
    y = Q(0)
    for coefficient in reversed(a): y = y * x + coefficient
    return y


def poly_divmod(a, b):
    a = list(a)
    while len(a) > 1 and a[-1] == 0: a.pop()
    while len(b) > 1 and b[-1] == 0: b.pop()
    if b == [0]: raise ZeroDivisionError
    q = [Q(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and a != [0]:
        k = len(a) - len(b)
        c = a[-1] / b[-1]
        q[k] += c
        for j, x in enumerate(b): a[k + j] -= c * x
        while len(a) > 1 and a[-1] == 0: a.pop()
    return q, a


def monic_gcd(a, b):
    while any(b):
        _, r = poly_divmod(a, b)
        a, b = b, r
    return poly_scale(a, 1 / a[-1])


def factor_poly(factors):
    out = [Q(1)]
    for root, multiplicity in factors:
        for _ in range(multiplicity): out = poly_mul(out, [-Q(root), Q(1)])
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--log", required=True)
    args = parser.parse_args()
    certificate_path = ROOT / args.certificate
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))

    samples = [charpoly_coefficients(Q(k)) for k in range(16)]
    # Table key is (E power, lambda power).
    reconstructed = {}
    for coefficient_index in range(N + 1):
        values = [sample[coefficient_index] for sample in samples]
        lam_poly = interpolate_at_consecutive_integers(values)
        e_power = N - coefficient_index
        for lam_power, value in enumerate(lam_poly):
            if value:
                assert value.denominator == 1
                reconstructed[(e_power, lam_power)] = value.numerator

    expected = {
        (row["E_power"], row["lambda_power"]): row["coefficient"]
        for row in certificate["expanded_coefficients"]
    }
    assert reconstructed == expected

    # Two rational holdouts were not used in interpolation.
    for lam in (Q(1, 2), Q(-2, 3)):
        direct = charpoly_coefficients(lam)
        for coefficient_index, actual in enumerate(direct):
            e_power = N - coefficient_index
            lam_poly = [Q(reconstructed.get((e_power, k), 0)) for k in range(16)]
            assert polyval(lam_poly, lam) == actual

    # Prove every lambda coefficient contains (E-1)^2 and that no larger
    # common factor exists: quotient coefficients at lambda^11 and ^12 are coprime.
    quotient_by_lambda = {}
    divisor = [Q(1), Q(-2), Q(1)]
    max_lam = max(k[1] for k in reconstructed)
    for lp in range(max_lam + 1):
        epoly = [Q(reconstructed.get((ep, lp), 0)) for ep in range(N + 1)]
        while len(epoly) > 1 and epoly[-1] == 0: epoly.pop()
        quotient, remainder = poly_divmod(epoly, divisor)
        assert all(x == 0 for x in remainder)
        quotient_by_lambda[lp] = quotient
    assert monic_gcd(quotient_by_lambda[11], quotient_by_lambda[12]) == [Q(1)]
    assert quotient_by_lambda[11] == [Q(-22), Q(-196), Q(50)]
    assert quotient_by_lambda[12] == [Q(4), Q(24)]

    endpoint0 = charpoly_coefficients(Q(0))
    endpoint1 = charpoly_coefficients(Q(1))
    target0 = list(reversed(factor_poly([(0, 1), (1, 8), (-1, 4), (-2, 2)])))
    target1 = list(reversed(factor_poly([(1, 8), (-1, 6), (-2, 1)])))
    assert endpoint0 == target0 and endpoint1 == target1

    lines = [
        "Independent exact isolated-corner replay (no SymPy)",
        "method=direct 15-vertex adjacency + exact Fraction Faddeev-LeVerrier + 16-point Newton interpolation",
        f"certificate={args.certificate}",
        f"certificate_sha256={sha256(certificate_path)}",
        f"terms={len(reconstructed)} max_lambda_degree={max_lam}",
        "unused_holdouts=lambda=1/2,-2/3: pass",
        "all coefficient polynomials divisible by (E-1)^2: pass",
        "quotient lambda^11=50 E^2-196 E-22",
        "quotient lambda^12=24 E+4",
        "gcd of those quotient coefficients=1",
        "lambda=0 endpoint identity: pass",
        "lambda=1 endpoint identity: pass",
        "conclusion=maximal lambda-independent factor degree 2; nonconstant root degree 13 per corner",
    ]
    log_path = ROOT / args.log
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "log": args.log, "log_sha256": sha256(log_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
