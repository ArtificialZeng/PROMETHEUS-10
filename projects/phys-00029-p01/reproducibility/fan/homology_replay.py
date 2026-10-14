#!/usr/bin/env python3
"""Portable arithmetic adaptation of the accepted original-edge referee replay.

This does not constitute a new independent review. It computes first, and only
then compares with the separately supplied accepted arithmetic values. All writes
go to the script's copied working directory, never the frozen scientific packet.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from math import isqrt
import json
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(20000)
HERE = Path(__file__).resolve().parent


def original_sectors(n, p, q):
    states = {(0, 0, 0): 1}
    for h in (1, 2, 3):
        out = {}
        for (hp, cp, winding), value in states.items():
            for use in (0, 1):
                key = (hp, cp, winding ^ (h if use else 0))
                out[key] = out.get(key, 0) + value * (p if use else q)
        states = out
    for j in range(1, n + 1):
        for h in ([0, 1, 2] if j == 1 else [0, 1]):
            out = {}
            for (hp, cp, winding), value in states.items():
                for use in (0, 1):
                    key = (hp ^ use, cp ^ use, winding ^ (h if use else 0))
                    out[key] = out.get(key, 0) + value * (p if use else q)
            states = out
        if j < n:
            out = {}
            for (hp, cp, winding), value in states.items():
                key = (hp, cp, winding)
                out[key] = out.get(key, 0) + value * (p if cp else q)
            states = out
    return [states.get((0, 0, h), 0) for h in range(4)], q ** (3 * n + 3)


def brute_sectors(n, p, q):
    edges = [(0, 0, 1), (0, 0, 2), (0, 0, 3)]
    for j in range(1, n + 1):
        edges.extend([(0, j, 0), (0, j, 1)])
        if j == 1:
            edges.append((0, j, 2))
        if j > 1:
            edges.append((j - 1, j, 0))
    sector = [0] * 4
    for mask in range(1 << len(edges)):
        parity = [0] * (n + 1)
        winding = 0
        count = 0
        for k, (u, v, h) in enumerate(edges):
            if (mask >> k) & 1:
                parity[u] ^= 1
                parity[v] ^= 1
                winding ^= h
                count += 1
        if not any(parity):
            sector[winding] += p ** count * q ** (len(edges) - count)
    return sector, q ** len(edges)


def sqrt_interval(x, scale=2 ** 96):
    k = isqrt(x.numerator * scale * scale // x.denominator)
    lo, hi = Q(k, scale), Q(k + 1, scale)
    assert lo * lo <= x < hi * hi
    return lo, hi


def artanh_interval(x, terms=72):
    low = sum((x ** (2*k + 1) / (2*k + 1) for k in range(terms)), Q(0))
    high = low + x ** (2*terms + 1) / ((2*terms + 1)*(1 - x*x))
    return low, high


def calibration_intervals():
    sl, sh = sqrt_interval(Q(3))
    tl, th = 2-sh, 2-sl
    assert tl > 0
    # One complete face-triangulation step: monotone g(t).
    _, ru = sqrt_interval(1 + 6*tl - 7*tl*tl)
    rl, _ = sqrt_interval(1 + 6*th - 7*th*th)
    gl, gh = 2*tl/(1+tl+ru), 2*th/(1+th+rl)
    ll, _ = artanh_interval(gl)
    _, lh = artanh_interval(gh)
    laves = (1/lh, 1/ll)
    assert Q(50065,10000) < laves[0] < laves[1] < Q(50075,10000)
    lo, hi = Q(1), Q(2)
    for _ in range(96):
        mid = (lo+hi)/2
        if mid**3-mid**2+mid-3 < 0:
            lo = mid
        else:
            hi = mid
    assert lo**3-lo**2+lo-3 < 0 < hi**3-hi**2+hi-3
    ll, _ = artanh_interval((lo-1)/(lo+1))
    _, lh = artanh_interval((hi-1)/(hi+1))
    half = (1/lh, 1/ll)
    assert Q(44035,10000) < half[0] < half[1] < Q(44045,10000)
    return {
        "laves_star_Tc_over_J": [str(x) for x in laves],
        "half_interpolated_Tc_over_J": [str(x) for x in half],
        "laves_star_display": [float(x) for x in laves],
        "half_interpolated_display": [float(x) for x in half],
        "logarithm_tail": "positive artanh series; 72 terms with exact geometric remainder",
    }


def main():
    small = []
    for n, (p,q) in product(range(1,4), [(1,21),(1,5),(1,3)]):
        assert original_sectors(n,p,q) == brute_sectors(n,p,q)
        small.append({"N":n,"t":str(Q(p,q)),"all_four_sectors_match":True})
    n = 1024
    sectors, denominator = original_sectors(n,1,21)
    signed = sectors[0] - sum(sectors[1:])
    assert signed < 0
    F = Q(signed, denominator)
    w1,w2 = 11,10
    for _ in range(1023):
        w1,w2 = 121*w1+100*w2, 100*w1+100*w2
    D = 21*210**1023
    up,um = Q(121*w1+100*w2,110*D), Q(w1+w2,D)
    margin = Q(121,100)*up-um-2
    assert margin > 1
    assert 3641*w1+1100*w2 > 33000*D
    r = Q(11,10)
    assert F == Q(2**(2*n+2))*r**(n+1)/(r+1)**(2*n+3)*(2-r*r*up+um)
    calibration = calibration_intervals()
    # Expected data enter only after the calculations above.
    expected = json.loads((HERE/"expected-referee-arithmetic.json").read_text())
    old = expected["large_original_homology"]
    assert list(map(int,old["sector_numerators"])) == sectors
    assert int(old["common_denominator"]) == denominator
    assert int(old["signed_numerator"]) == signed
    assert Q(old["signed_F"]) == F
    assert Q(expected["large_trace"]["U_plus"]) == up
    assert Q(expected["large_trace"]["U_minus"]) == um
    assert Q(expected["large_trace"]["ordering_margin"]) == margin
    result = {
        "method":"portable adaptation of accepted original-edge homology elimination",
        "small_all_sector_checks":small,
        "large_original_homology":{
            "N":n,"t":"1/21","sector_numerators":[str(x) for x in sectors],
            "common_denominator":str(denominator),"signed_numerator":str(signed),
            "signed_F":str(F),"strictly_negative":True},
        "integer_margin_greater_than_one":True,
        "ordering_margin":str(margin),
        "formula_6_exact_match":True,
        "accepted_original_sector_certificate_exact_match":True,
        "calibrations":calibration,
        "limitations":"Arithmetic regeneration of the unchanged accepted result, not a fresh scientific referee or human review.",
    }
    (HERE/"homology-replay-results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
        "large_original_signed_F_negative":True,
        "integer_margin_greater_than_one":True,
        "accepted_certificate_exact_match":True,
        "small_all_sector_checks":len(small),
        "calibrations":calibration,
    },indent=2))


if __name__ == "__main__":
    main()
