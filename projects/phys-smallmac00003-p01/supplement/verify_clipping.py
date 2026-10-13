#!/usr/bin/env python3
"""Exact rational clipping cross-check for the two-qutrit purity certificate.

Mathematical functions preserve the separate pre-manuscript verification.
Only descriptive metadata and output routing are adapted for this package.
No previously stored vertex list is read by this program.
"""
from argparse import ArgumentParser
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import datetime
import hashlib
import json
import platform
import resource
import time

N = 9
TARGET = F(17, 121)

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def rank(rows):
    a = [list(map(F, r)) for r in rows]
    pivot = 0
    for col in range(N):
        k = next((k for k in range(pivot, len(a)) if a[k][col]), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        q = a[pivot][col]
        a[pivot] = [v/q for v in a[pivot]]
        for k in range(pivot+1, len(a)):
            if a[k][col]:
                q = a[k][col]
                a[k] = [v-q*w for v, w in zip(a[k], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot

def schmidt_pt_spectrum(s):
    # The 9x9 partial transpose has three scalar diagonal blocks and three
    # [[0, s_i*s_j], [s_i*s_j, 0]] blocks (Hildebrand v1, Lemma 1).
    mu = [F(x*x) for x in s]
    for i, j in combinations(range(3), 2):
        mu.extend([F(s[i]*s[j]), F(-s[i]*s[j])])
    return tuple(sorted(mu))

def source_lmis(l):
    # Direct, fresh transcription of Hildebrand v1 p.6 Eq.(5), n=3.
    return (
        ((2*l[8], l[7]-l[0], l[5]-l[1]),
         (l[7]-l[0], 2*l[6], l[4]-l[2]),
         (l[5]-l[1], l[4]-l[2], 2*l[3])),
        ((2*l[8], l[7]-l[0], l[6]-l[1]),
         (l[7]-l[0], 2*l[5], l[4]-l[2]),
         (l[6]-l[1], l[4]-l[2], 2*l[3]))
    )

def schmidt_hessians():
    # Symbolic monomials encoded as (i,j,sign); order chosen by two generic
    # interior examples, whose completeness is proved in source-review.md.
    out = []
    for s in ((4, 3, 1), (5, 2, 1)):
        terms = [(i, i, 1) for i in range(3)]
        terms += [(i, j, sign) for i, j in combinations(range(3), 2) for sign in (-1, 1)]
        terms.sort(key=lambda t: t[2]*s[t[0]]*s[t[1]])
        h = [[[F(0) for _ in range(N)] for _ in range(3)] for _ in range(3)]
        for k, (i, j, sign) in enumerate(terms):
            if i == j:
                h[i][j][k] += 2*sign
            else:
                h[i][j][k] += sign
                h[j][i][k] += sign
        out.append(h)
    # Compare all 18 linear-form entries on a basis, not a random spectrum.
    for k in range(N):
        e = tuple(F(i == k) for i in range(N))
        source = source_lmis(e)
        for c in range(2):
            for i in range(3):
                for j in range(3):
                    assert out[c][i][j][k] == source[c][i][j]
    return out

def determinant(a):
    n = len(a)
    ans = F(0)
    for p in permutations(range(n)):
        v = F(-1 if sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2 else 1)
        for i in range(n):
            v *= a[i][p[i]]
        ans += v
    return ans

def all_minors(a):
    return [determinant([[a[i][j] for j in s] for i in s])
            for k in range(1, 4) for s in combinations(range(3), k)]

def constraints():
    rows = []
    for i in range(N):
        r = [F(0)]*N
        r[i] = F(1)
        if i+1 < N:
            r[i+1] = F(-1)
        rows.append(tuple(r))
    return rows

def clip(vertices, row, prior_rows):
    value = {v: dot(row, v) for v in vertices}
    positive = [v for v in vertices if value[v] > 0]
    negative = [v for v in vertices if value[v] < 0]
    candidates = {v for v in vertices if value[v] >= 0}
    for p in positive:
        for n in negative:
            t = value[p]/(value[p]-value[n])
            v = tuple((1-t)*x+t*y for x, y in zip(p, n))
            assert dot(row, v) == 0
            candidates.add(v)
    all_rows = prior_rows+[row]
    kept = set()
    rejected_ranks = {}
    for v in candidates:
        assert sum(v) == 1 and all(dot(r, v) >= 0 for r in all_rows)
        active = [(F(1),)*N]+[r for r in all_rows if dot(r, v) == 0]
        rnk = rank(active)
        if rnk == N:
            kept.add(v)
        else:
            rejected_ranks[rnk] = rejected_ranks.get(rnk, 0)+1
    return kept, all_rows, {
        'input_vertices': len(vertices), 'positive': len(positive),
        'negative': len(negative), 'zero': len(vertices)-len(positive)-len(negative),
        'crossing_pairs': len(positive)*len(negative),
        'unique_feasible_generators': len(candidates),
        'output_vertices': len(kept), 'nonvertex_active_ranks': rejected_ranks,
        'maximum_purity': str(max(dot(v, v) for v in kept))
    }

def serialize_vertex(v, rows):
    gaps = tuple((i+1)*(v[i]-(v[i+1] if i+1 < N else 0)) for i in range(N))
    return {'lambda': list(map(str, v)), 'gap_support_size': sum(x > 0 for x in gaps),
            'cut_slacks': list(map(str, [dot(r, v) for r in rows[-3:]])),
            'purity': str(dot(v, v)), 'deficit': str(TARGET-dot(v, v))}

def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.perf_counter()
    schmidt_hessians()
    witnesses = ((1, 1, 0), (1, 1, 1), (2, 1, 0))
    cuts = [schmidt_pt_spectrum(s) for s in witnesses]
    for s, c in zip(witnesses, cuts):
        for k in range(N):
            e = tuple(F(i == k) for i in range(N))
            a = source_lmis(e)[0]
            q = sum(s[i]*a[i][j]*s[j] for i in range(3) for j in range(3))/2
            assert q == c[k]
    rows = constraints()
    vertices = {tuple(F(1, k) if i < k else F(0) for i in range(N)) for k in range(1, N+1)}
    steps = []
    for cut in cuts:
        vertices, rows, result = clip(vertices, cut, rows)
        steps.append(result)
        print('CLIP', len(steps), json.dumps(result, sort_keys=True), flush=True)
    ordered = sorted(vertices, key=lambda v: (dot(v, v), v), reverse=True)
    top = dot(ordered[0], ordered[0])
    maximizers = [v for v in ordered if dot(v, v) == top]
    expected = (F(3, 11),)+(F(1, 11),)*8
    assert top == TARGET and maximizers == [expected]
    assert all(dot(v, v) <= TARGET for v in vertices)
    groups = {}
    for v in vertices:
        count = sum(v[i] != (v[i+1] if i+1 < N else 0) for i in range(N))
        groups.setdefault(count, []).append(dot(v, v))
    baselines = []
    for name, l in [('zeta1', expected), ('mixed', (F(1, 9),)*9),
                    ('rank8', (F(1, 8),)*8+(F(0),)),
                    ('pure_control', (F(1),)+(F(0),)*8)]:
        minors = [all_minors(a) for a in source_lmis(l)]
        admissible = all(x >= 0 for m in minors for x in m)
        assert admissible == (name != 'pure_control')
        baselines.append({'name': name, 'lambda': list(map(str, l)),
            'purity': str(dot(l, l)), 'all_principal_minors': [list(map(str, m)) for m in minors],
            'both_lmis_psd': admissible})
    data = {
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'method': 'Exact incremental clipping in spectrum coordinates; all crossing pairs; exact active-rank filtering',
        'input_files_read': [], 'candidate_code_or_cache_imported': False,
        'source_hessian_linear_coefficient_checks': 162,
        'cuts_derived_from_schmidt_pt_eigenvalues': [list(map(str, r)) for r in cuts],
        'clipping_steps': steps, 'vertex_count': len(vertices),
        'maximum': str(top), 'maximizer_count': len(maximizers),
        'runner_up': str(dot(ordered[1], ordered[1])),
        'runner_up_gap': str(top-dot(ordered[1], ordered[1])),
        'support_groups': {str(s): {'count': len(ps), 'max_purity': str(max(ps))} for s, ps in sorted(groups.items())},
        'vertices': [serialize_vertex(v, rows) for v in ordered],
        'baselines': baselines, 'hs_radius_squared': str(TARGET-F(1, 9)),
        'purity_bound_improvement': str(F(25, 169)-TARGET),
        'python_version': platform.python_version(), 'platform': platform.platform(),
        'wall_seconds': time.perf_counter()-began,
        'maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'maxrss_units': 'bytes on macOS; KiB on Linux',
        'threads_or_workers_spawned': 0,
        'arithmetic': 'Unbounded exact Python integers and fractions.Fraction; no tolerance or numerical eigenvalues'
    }
    out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
    summary = {k: data[k] for k in ['method', 'source_hessian_linear_coefficient_checks',
        'cuts_derived_from_schmidt_pt_eigenvalues', 'vertex_count', 'maximum',
        'maximizer_count', 'runner_up', 'runner_up_gap', 'support_groups',
        'hs_radius_squared', 'purity_bound_improvement', 'wall_seconds', 'maxrss_native']}
    print(json.dumps(summary, indent=2))
    print('RESULT_SHA256', hashlib.sha256(out.read_bytes()).hexdigest())
    print('ALL_ASSERTIONS_PASSED')

if __name__ == '__main__':
    main()
