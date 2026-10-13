#!/usr/bin/env python3
"""Exact circuit and entropy replay accompanying the graph-state manuscript.

Standard library only. Reconstructs the full phase-error ensemble, takes exact
partial traces, verifies Walsh eigenvector equations, and encloses logarithms
using a 96-term Mercator series with a rational remainder bound.
Writes JSON to stdout only; no external input files are loaded.
"""
from collections import Counter
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from functools import lru_cache
import datetime
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time

TERMS = 96

def parity(x):
    return bin(x).count('1') & 1

def fwht(v):
    v = list(v)
    step = 1
    while step < len(v):
        for i in range(0, len(v), 2 * step):
            for j in range(i, i + step):
                a, b = v[j], v[j + step]
                v[j], v[j + step] = a + b, a - b
        step *= 2
    return v

def graph_checks(na, nb, edges):
    assert len(edges) == len(set(edges))
    assert all(0 <= a < na <= b < na + nb for a, b in edges)
    adjacency = [set() for _ in range(na + nb)]
    rowmasks = [0] * na
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
        rowmasks[a] |= 1 << (b - na)
    seen, todo = {0}, [0]
    while todo:
        for x in adjacency[todo.pop()]:
            if x not in seen:
                seen.add(x)
                todo.append(x)
    # Rank via size of the image, with no RREF or submitted kernel basis.
    image = {0}
    for row in rowmasks:
        image |= {x ^ row for x in tuple(image)}
    rank = len(image).bit_length() - 1
    assert len(image) == 2 ** rank
    return dict(n_A=na, n_B=nb, rank=rank,
                connected=len(seen) == na + nb,
                no_zero_rows_columns=all(adjacency), edges=len(edges))

def direct_circuit(na, nb, edges, P):
    N, den, pnum = na + nb, P.denominator, P.numerator
    qnum = den - pnum
    size = 1 << N
    signs = [(-1) ** sum(((x >> a) & 1) * ((x >> b) & 1)
                         for a, b in edges) for x in range(size)]
    weights = [pnum ** (N - bin(e).count('1')) * qnum ** bin(e).count('1')
               for e in range(size)]
    assert sum(weights) == den ** N
    # Explicit full error ensemble transformed independently; no assumed t^weight.
    characteristic = [sum(w * (-1) ** parity(e & d)
                          for e, w in enumerate(weights)) for d in range(size)]
    assert characteristic == fwht(weights)
    common = size * den ** N
    matrices = []
    spectra = []
    for side, nlocal, ntraced in [('A', na, nb), ('B', nb, na)]:
        mat = []
        for i in range(1 << nlocal):
            row = []
            for j in range(1 << nlocal):
                total = 0
                for k in range(1 << ntraced):
                    x = i | (k << na) if side == 'A' else k | (i << na)
                    y = j | (k << na) if side == 'A' else k | (j << na)
                    total += signs[x] * signs[y] * characteristic[x ^ y]
                row.append(total)
            mat.append(row)
        dim = len(mat)
        assert all(mat[i][j] == mat[j][i] == mat[0][i ^ j]
                   for i in range(dim) for j in range(dim))
        assert sum(mat[i][i] for i in range(dim)) == common
        # A Walsh character is an exact eigenvector: prove each row equation.
        eigen_numerators = fwht(mat[0])
        for s, lam in enumerate(eigen_numerators):
            assert all(sum(mat[i][j] * (-1) ** parity(s & j)
                           for j in range(dim)) == lam * (-1) ** parity(s & i)
                       for i in range(dim))
        spectrum = [F(v, common) for v in eigen_numerators]
        assert min(spectrum) >= 0 and sum(spectrum) == 1
        spectra.append(spectrum)
        matrices.append(mat)
    return spectra, sum(len(m) ** 2 for m in matrices)

@lru_cache(maxsize=None)
def minus_ln_range(y):
    """For 1/2<=y<=1: -ln y=sum_(j>=1) (1-y)^j/j.

    Remaining terms lie in [0,z^(M+1)/((M+1)(1-z))].
    """
    assert F(1, 2) <= y <= 1
    z, power, lower = 1 - y, 1 - y, F(0)
    for j in range(1, TERMS + 1):
        lower += power / j
        power *= z
    return lower, lower + power / ((TERMS + 1) * (1 - z))

@lru_cache(maxsize=None)
def surprisal(p):
    assert 0 < p <= 1
    y, k = p, 0
    while y < F(1, 2):
        y *= 2
        k += 1
    lo, hi = minus_ln_range(y)
    l2lo, l2hi = minus_ln_range(F(1, 2))
    return F(k) + lo / l2hi, F(k) + hi / l2lo

def entropy(probabilities):
    assert all(p >= 0 for p in probabilities) and sum(probabilities) == 1
    lo = hi = F(0)
    for p, multiplicity in Counter(probabilities).items():
        if p:
            a, b = surprisal(p)
            lo += multiplicity * p * a
            hi += multiplicity * p * b
    return lo, hi

def subtract(x, y):
    return x[0] - y[1], x[1] - y[0]

def scaled(x, n):
    assert n >= 0
    return n * x[0], n * x[1]

def bounds(x):
    out = []
    for value, rounding in zip(x, [ROUND_FLOOR, ROUND_CEILING]):
        with localcontext() as ctx:
            ctx.prec = 50
            ctx.rounding = rounding
            d = Decimal(value.numerator) / Decimal(value.denominator)
            out.append(str(d.quantize(Decimal('1e-22'), rounding=rounding)))
    return out

def spectral_counts(s):
    return {str(p): n for p, n in sorted(Counter(s).items())}

def run_case(name, na, nb, edges, P, expected=None):
    checks = graph_checks(na, nb, edges)
    assert checks['connected'] and checks['no_zero_rows_columns']
    spectra, entries = direct_circuit(na, nb, edges, P)
    if expected is not None:
        assert all(Counter(got) == Counter(want)
                   for got, want in zip(spectra, expected))
    SA, SB = map(entropy, spectra)
    h = entropy([P, 1-P])
    SAB = scaled(h, na + nb)
    delta, IA, IB = subtract(SA, SB), subtract(SA, SAB), subtract(SB, SAB)
    if name == 'witness' and P == F(199, 200):
        assert checks['rank'] == 3 and na > nb >= 3
        assert F(-43, 10000) < delta[0] < delta[1] < F(-42, 10000)
        assert IA[0] > F(27, 10) and IB[0] > F(27, 10)
        assert h[1] < F(1, 2)
    return dict(name=name, P=str(P), graph=checks, exact_matrix_entries=entries,
                spectrum_A=spectral_counts(spectra[0]),
                spectrum_B=spectral_counts(spectra[1]),
                S_A=bounds(SA), S_B=bounds(SB), S_AB=bounds(SAB),
                delta=bounds(delta), I_A=bounds(IA), I_B=bounds(IB), h_P=bounds(h))

def main():
    start = time.monotonic()
    cases = []
    # Primary S1 rank-one baseline, independent physical edge transcription.
    cases.append(run_case('K21', 2, 1, [(0,2),(1,2)], F(3,4),
                          [[F(5,16)]*2+[F(3,16)]*2, [F(1,2)]*2]))
    # S1 PDF p11 Eq28, directly transcribed as edges (zero-based labels).
    eq28 = [(0,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)]
    cases.append(run_case('Eq28', 4, 3, eq28, F(3,4),
                          [[F(3,32)]*4+[F(1,16)]*4+[F(3,64)]*8,
                           [F(5,32)]*4+[F(3,32)]*4]))
    witness = [(0,5),(0,8),(1,5),(1,8),(2,5),(2,8),(3,6),(3,8),(4,7),(4,8)]
    for P in [F(1,2), F(1), F(199,200), F(99,100), F(999,1000)]:
        t = 2*P-1
        a, b, c = (1+3*t*t)/4, (1-t*t)/4, (1-t**4)/2
        cases.append(run_case('witness', 5, 4, witness, P,
                              [[a/8]*8+[b/8]*24, [(1-c)/8]*8+[c/8]*8]))
    # This finite check only attacks the analytic all-r argument, never proves it.
    family = []
    for r in range(3, 10):
        na, nb = r+2, r+1
        edges = [(i,na) for i in range(3)]
        edges += [(i+2,na+i) for i in range(1,r)]
        edges += [(i,na+r) for i in range(na)]
        check = graph_checks(na,nb,edges)
        assert check['rank'] == r and check['connected'] and check['no_zero_rows_columns']
        t = F(99,100)
        a,b,c = (1+3*t*t)/4,(1-t*t)/4,(1-t**(r+1))/2
        A, B, h = entropy([a,b,b,b]), entropy([1-c,c]), entropy([F(199,200),F(1,200)])
        delta = subtract(A,B)
        IA = subtract((A[0]+r,A[1]+r),scaled(h,2*r+3))
        assert delta[1] < F(-42,10000) and IA[0] > F(27,10)
        family.append(dict(r=r,graph=check,delta=bounds(delta),I_A=bounds(IA)))
    result = dict(checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  status='all_assertions_passed',
                  implementation='Explicit circuit and phase-error ensemble; standard library only; no input caches.',
                  exact_log_series='96-term positive Mercator with rational remainder and base-2 range reduction',
                  cases=cases,family_finite_checks=family,
                  finite_family_limit='r=3..9 is diagnostic only; all-r proof is in the manuscript proposition.',
                  python=sys.version, platform=platform.platform(),
                  elapsed_seconds=time.monotonic()-start,
                  peak_rss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  peak_rss_units='bytes on macOS, KiB on Linux',
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
