#!/usr/bin/env python3
"""Portable exact algebra for the subdivided two-star endpoint gap.

Run with SymPy 1.14.0. No external files, proposer caches or network are read.
The generated data supplement the full-sector analytic proof in the paper.
"""
import argparse
import itertools
import json
from pathlib import Path
import time
import sympy as S

k, q, x, e, t, h = S.symbols('k q x e theta h')


def choose(p):
    return S.prod((k-j)/S.Integer(j+1) for j in range(p))


def quotient(number):
    states = sorted((a, b, c, p, number-a-b-c-p)
                    for a, b, c in itertools.product([0, 1], repeat=3)
                    for p in range(number+1)
                    if 0 <= number-a-b-c-p <= number)
    index = {v: i for i, v in enumerate(states)}
    weights = [choose(p)*choose(r)*q**(a+b) for a, b, c, p, r in states]
    A = S.zeros(len(states))
    for i, (a, b, c, p, r) in enumerate(states):
        za, zb, zc = 2*a-1, 2*b-1, 1-2*c
        for zh, count in [(za, p), (zb, r)]:
            zsum = k-2*count
            A[i, i] += (1+q)*(k+zh*zsum)/4+(1-q)*(k*zh+zsum)/4
            A[i, i] += (1+q)*(1+zh*zc)/4+(1-q)*(zh+zc)/4
        for hub, site, count, column in [(a, 0, p, 3), (b, 1, r, 4)]:
            new_count = count+1 if hub else count-1
            if not 0 <= new_count <= number:
                continue
            target = list(states[i]); target[site] = 1-hub; target[column] = new_count
            j = index[tuple(target)]
            ladder = (k-count)*(count+1) if hub else count*(k-count+1)
            value = k-count if hub else q*count
            assert S.cancel(q*ladder*weights[j]/weights[i]-value**2) == 0
            A[i, j] += value
        for hub, site in [(a, 0), (b, 1)]:
            if hub == c:
                continue
            target = list(states[i]); target[site] = 1-hub; target[2] = 1-c
            j = index[tuple(target)]
            value = S.Integer(1) if hub else q
            assert S.cancel(q*weights[j]/weights[i]-value**2) == 0
            A[i, j] += value
    A = S.simplify(A)
    W = S.diag(*weights)
    assert S.simplify(W*A-A.T*W) == S.zeros(A.rows)
    groups, seen = [], set()
    for v in states:
        if v in seen:
            continue
        a, b, c, p, r = v
        rv = (b, a, c, r, p)
        group = [v] if rv == v else [v, rv]
        groups.append(group); seen.update(group)
    folded = {v: i for i, group in enumerate(groups) for v in group}
    Q = S.zeros(len(groups))
    for i, group in enumerate(groups):
        for v in group:
            row = [S.Integer(0)]*len(groups)
            for j, w in enumerate(states):
                row[folded[w]] += A[index[v], j]
            if v == group[0]:
                for j, value in enumerate(row):
                    Q[i, j] = S.expand(value)
            else:
                assert all(S.expand(row[j]-Q[i, j]) == 0 for j in range(Q.cols))
    wf = [len(group)*weights[index[group[0]]] for group in groups]
    assert S.simplify(S.diag(*wf)*Q-Q.T*S.diag(*wf)) == S.zeros(Q.rows)
    return Q, groups, len(states)


def box_norm(poly, variables, bounds):
    return sum(abs(c)*S.prod(b**power for b, power in zip(bounds, powers))
               for powers, c in S.Poly(S.expand(poly), *variables).terms())


def enclose(poly, number):
    lead = 8 if number == 2 else 32
    a = -S.Integer(2) if number == 2 else -(t+4)/2
    b = 2*t+10 if number == 2 else (t*t+7*t+40)/4
    substituted = S.expand(poly.subs({k: 1/e, q: 1-t*e,
                                     x: 2/e+4+e*(h-number*t)}))
    power = min(v.as_powers_dict().get(e, 0) for v in S.Add.make_args(substituted))
    P = S.expand(substituted/e**power)
    assert S.expand(P.subs(e, 0)-lead*h) == 0
    dev = box_norm(S.diff(P, h)-lead, [e, t, h], [S.Rational(1, 100), 2, 1])
    lower = lead-dev
    residual = S.expand(P.subs(h, e*a+e**2*b))
    assert all(residual.coeff(e, j) == 0 for j in range(3))
    residual_bound = box_norm(S.cancel(residual/e**3), [e, t], [S.Rational(1, 100), 2])
    C = S.cancel(residual_bound/lower)
    ceiling = 81 if number == 2 else 101
    dev_ceiling = S.Rational(187, 200) if number == 2 else S.Rational(1541, 250)
    residual_ceiling = S.Integer(572) if number == 2 else S.Integer(2597)
    assert 0 < dev < dev_ceiling and 0 < residual_bound < residual_ceiling
    assert lower > 0 and C < ceiling
    trunc_bound = box_norm(e*a+e**2*b, [e, t], [S.Rational(1, 100), 2])
    assert trunc_bound+ceiling/S.Integer(100)**3 < 1
    return {'N': number, 'dimension': int(S.degree(poly, x)),
            'characteristic_polynomial': str(poly),
            'normalization_exponent': int(power), 'normalized_polynomial': str(P),
            'derivative_deviation': str(dev), 'derivative_lower': str(lower),
            'residual_over_e3_bound': str(residual_bound),
            'h_error_over_e3_bound': str(C), 'lambda_error_constant': ceiling,
            'truncation_box_bound': str(trunc_bound),
            'lambda_approximation': str(2/e+4-number*t*e+e**2*a+e**3*b)}


def physical_lift(Q, groups, number):
    K, s = 3, S.Rational(3, 5)
    n = 2*K+3
    edges = [(0, 2), (1, 2)]+[(0, j) for j in range(3, 3+K)]+[(1, j) for j in range(3+K, n)]
    basis = sorted(sum(1 << j for j in sites) for sites in itertools.combinations(range(n), number))
    index = {v: i for i, v in enumerate(basis)}
    B = S.zeros(len(basis))
    lift = S.zeros(len(basis), Q.rows)
    gindex = {v: i for i, g in enumerate(groups) for v in g}
    for i, bits in enumerate(basis):
        a, b, c = [(bits >> j) & 1 for j in range(3)]
        p = sum((bits >> j) & 1 for j in range(3, 3+K))
        r = sum((bits >> j) & 1 for j in range(3+K, n))
        lift[i, gindex[(a, b, c, p, r)]] = s**(a+b)
        for hub, site in edges:
            ah, bs = (bits >> hub) & 1, (bits >> site) & 1
            if ah == bs:
                continue
            B[i, i] += 1 if ah else s*s
            B[i, index[bits ^ (1 << hub) ^ (1 << site)]] += s
    assert B == B.T
    assert B*lift == lift*Q.subs({k: K, q: s*s})
    return {'k': K, 's': str(s), 'N': number, 'full_number_dimension': len(basis),
            'quotient_dimension': Q.rows, 'exact_intertwining': True}


def baseline_and_envelope():
    s = S.Rational(1, 2)
    phi = S.Matrix([1, 0, 0, s]); local = phi*phi.T
    X = S.Matrix([[0, 1], [1, 0]]); Y = S.Matrix([[0, -S.I], [S.I, 0]])
    Z = S.diag(1, -1); I = S.eye(2)
    pauli = (1+s*s)*(S.eye(4)+S.kronecker_product(Z, Z))/4
    pauli += (1-s*s)*(S.kronecker_product(Z, I)+S.kronecker_product(I, Z))/4
    pauli += s*(S.kronecker_product(X, X)-S.kronecker_product(Y, Y))/2
    assert local == pauli
    H = S.zeros(16)
    for bits in range(16):
        for leaf in [1, 2, 3]:
            a, b = (bits >> 0) & 1, (bits >> leaf) & 1
            if a != b:
                continue
            H[bits, bits] -= 1 if a == 0 else s*s
            H[bits, bits ^ 1 ^ (1 << leaf)] -= s
    eigen = H.eigenvals()
    ordered = sorted(v for value, count in eigen.items() for v in [value]*count)
    assert len(ordered) == 16 and ordered[:2] == [-S.Rational(13, 4), -S.Rational(5, 2)]
    L, N, d = S.symbols('L N d', integer=True)
    determinant = S.expand((L-N+1)*q*N-q*(N-d)*(L-d-N+1))
    assert S.expand(determinant-q*d*(L+1-d)) == 0
    c_spectra = {}
    for number in [1, 2]:
        basis = sorted(sum(1 << j for j in sites) for sites in itertools.combinations(range(3), number))
        idx = {v: i for i, v in enumerate(basis)}; C = S.zeros(3)
        for i, bits in enumerate(basis):
            for hub in [0, 1]:
                a, b = (bits >> hub) & 1, (bits >> 2) & 1
                if a != b:
                    C[i, i] += 1 if a else q
                    C[i, idx[bits ^ (1 << hub) ^ 4]] += S.sqrt(q)
        expected = x*(x-1)*(x-1-2*q) if number == 1 else x*(x-q)*(x-2-q)
        actual = S.expand(C.charpoly(x).as_expr())
        assert S.expand(actual-expected) == 0
        c_spectra[str(number)] = str(S.factor(actual))
    return {'star_s': str(s), 'full_star_spectrum': [[str(v), int(m)] for v, m in sorted(eigen.items())],
            'star_ground': '-13/4', 'star_first_excited': '-5/2', 'star_gap': '3/4',
            'local_ket_matches_pauli': True, 'symbolic_star_block_determinant': str(determinant),
            'auxiliary_C_characteristic_polynomials': c_spectra}


def root_anchors(records):
    anchors = []
    for theta in [S.Rational(1, 2), S.Integer(2)]:
        K = S.Integer(100); roots = {}; details = []
        for rec in records:
            number = rec['N']
            p = S.Poly(S.sympify(rec['characteristic_polynomial'], locals={'k': k, 'q': q, 'x': x})
                       .subs({k: K, q: 1-theta/K}), x)
            intervals = p.intervals(eps=S.Rational(1, 10**24))
            assert sum(m for _, m in intervals) == p.degree()
            (lo, hi), mult = intervals[-1]
            assert mult == 1
            approx = 2*K+4-number*theta/K
            approx += -2/K**2+(2*theta+10)/K**3 if number == 2 else -(theta+4)/(2*K**2)+(theta**2+7*theta+40)/(4*K**3)
            err = S.Rational(rec['lambda_error_constant'])/K**4
            assert approx-err < lo <= hi < approx+err
            assert 2*K+4+(-number*theta-1)/K < lo <= hi < 2*K+4+(-number*theta+1)/K
            roots[number] = lo, hi
            details.append({'N': number, 'complete_root_count': int(p.degree()),
                            'all_intervals': [[[str(a), str(b)], int(m)] for (a, b), m in intervals]})
        lo = roots[2][0]-roots[3][1]; hi = roots[2][1]-roots[3][0]; eta = theta/K
        assert lo > eta and roots[3][0] > K+5
        assert roots[3][0] > 2*K+4-4*eta+eta/2
        anchors.append({'k': int(K), 'theta': str(theta), 'eta': str(eta), 'root_checks': details,
                        'full_gap_interval': [str(lo), str(hi)],
                        'gap_ratio_interval': [str(lo/eta), str(hi/eta)]})
    return anchors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='endpoint-certificate.json')
    args = parser.parse_args(); started = time.monotonic()
    controls = baseline_and_envelope(); records = []; lifts = []
    for number in [2, 3]:
        Q, groups, orbit_dimension = quotient(number)
        lifts.append(physical_lift(Q, groups, number))
        poly = S.expand(Q.charpoly(x).as_expr())
        rec = enclose(poly, number)
        rec.update({'unfolded_dimension': orbit_dimension, 'reflection_orbits': groups,
                    'matrix': [[str(v) for v in row] for row in Q.tolist()]})
        records.append(rec)
        print('Exact low-sector construction completed:', number, flush=True)
    anchors = root_anchors(records)
    tail = S.Rational(1, 4)-S.Rational(3, 100)-S.Rational(101, 100**3)
    excess = S.Rational(1, 2)-S.Rational(1, 400)-S.Rational(364, 100**2)
    low = S.Integer(99)-S.Rational(6, 100)-S.Rational(3, 100**2)-S.Rational(101, 100**4)
    assert tail > 0 and excess > 0 and low > 0
    record = {'sympy_version': S.__version__,
              'domain': 'integer k>=100, real theta in [1/2,2], q=1-theta/k, J=1',
              'controls': controls, 'physical_lifts': lifts, 'records': records, 'anchors': anchors,
              'tail_margin_times_k_lower': str(tail), 'ratio_excess_times_k_lower': str(excess),
              'internal_low_sector_separation_lower': str(low), 'ratio_error_constant': 364,
              'meaning': 'Exact supplementary calculation. Full-space ordering additionally uses the analytic star-envelope and Weyl proof; finite checks alone do not prove the universal domain.'}
    target = Path(args.output); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'output': str(target), 'elapsed_seconds': time.monotonic()-started,
                      'all_assertions_passed': True, 'sympy_version': S.__version__}))


if __name__ == '__main__':
    main()
