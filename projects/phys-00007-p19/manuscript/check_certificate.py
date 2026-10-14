#!/usr/bin/env python3
"""Reproduce the finite coefficient certificate using only rational arithmetic.

This is a manuscript arithmetic check of the accepted result, not a new audit.
All constants below are printed in the manuscript; no cached result is an input.
"""
from fractions import Fraction as Q
from math import comb
import json


def certificate():
    radicals = {
        42: (Q(648074, 100000), Q(648075, 100000)),
        273: (Q(1652271, 100000), Q(1652272, 100000)),
    }
    for n, (lo, hi) in radicals.items():
        assert 0 < lo and lo * lo < n < hi * hi
    # Entries are rational constant, sqrt(42) coefficient, sqrt(273) coefficient.
    coefficients = [
        (Q(16556, 315), -Q(512, 63), Q(0)),
        (-Q(143803, 270), Q(2048, 27), Q(5, 2)),
        (Q(631987, 297), -Q(81920, 297), -Q(225, 11)),
        (-Q(509176, 117), Q(655360, 1287), Q(9000, 143)),
        (Q(6236816, 1287), -Q(655360, 1287), -Q(1200, 13)),
        (-Q(27854144, 9945), Q(524288, 1989), Q(14400, 221)),
        (Q(124497536, 188955), -Q(2097152, 37791), -Q(5760, 323)),
    ]
    enclosures = []
    for c, r, s in coefficients:
        lo = hi = c
        for n, multiplier in ((42, r), (273, s)):
            lower, upper = radicals[n]
            lo += multiplier * (lower if multiplier >= 0 else upper)
            hi += multiplier * (upper if multiplier >= 0 else lower)
        enclosures.append((lo, hi))
    epsilon = Q(1, 100)
    q_upper = enclosures[0][1] + sum(
        max(abs(lo), abs(hi)) * epsilon ** i
        for i, (lo, hi) in enumerate(enclosures[1:], 1)
    )
    assert q_upper == -Q(730364709499556213711, 6820094531250000000000)
    assert q_upper < 0

    def a(t, k):
        if t > k:
            return Q(0)
        return Q(
            4 ** t * (-1) ** (k + t) * comb(18, 2 * k) * comb(k, t)
            * comb(18 - 2 * t, 9 - t),
            (2 * k + 1) * comb(18, 9),
        )

    phi = [Q(0)] * 10
    for k in range(4, 10):
        factor = -Q(4, 5) * (a(4, k) + a(5, k))
        for h in range(10 - k):
            phi[k + h] += factor * comb(9 - k, h) * (-1) ** h
    assert phi[:4] == [Q(0)] * 4
    assert phi[4:] == [
        -Q(129024, 25), Q(2322432, 55), -Q(18579456, 143),
        Q(12386304, 65), -Q(148635648, 1105), Q(297271296, 8075),
    ]
    u_upper = phi[4] + sum(abs(phi[k]) * epsilon ** (k - 4) for k in range(5, 10))
    assert u_upper == -Q(53287797135702528, 11276611328125)
    assert u_upper < 0
    integer_gap = 640 ** 2 * 42 - 4139 ** 2
    assert integer_gap == 71879
    return {
        "check": "manuscript rational coefficient certificate",
        "integer_gap": integer_gap,
        "q_coefficient_enclosures": [[str(lo), str(hi)] for lo, hi in enclosures],
        "q_upper": str(q_upper),
        "phi4_coefficients_ascending": [str(c) for c in phi[4:]],
        "u_upper": str(u_upper),
        "domain": "0<x=sin^2(eta/2)<=1/100",
        "all_assertions_passed": True,
        "scope": "Faithful manuscript arithmetic check; not scientific or release acceptance.",
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
