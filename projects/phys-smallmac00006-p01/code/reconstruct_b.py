#!/usr/bin/env python3
"""B: Gray-coded bond weights and synchronous edge flux; imports no A code/data."""
from pathlib import Path
from datetime import datetime, timezone
import json
import platform
import resource
import time
import sympy as S


def main():
    start = time.perf_counter()
    root = Path(__file__).resolve().parents[1]
    L = 4
    codes = [n ^ (n >> 1) for n in range(1 << L)]
    index = {g: i for i, g in enumerate(codes)}
    bits = [[(g >> a) & 1 for a in range(L)] for g in codes]
    aligned = [sum(b[a] == b[(a + 1) % L] for a in range(L)) for b in bits]
    edges = sorted({tuple(sorted((i, index[g ^ (1 << a)])))
                    for i, g in enumerate(codes) for a in range(L)})
    n = len(codes)
    assert len(edges) == n * L // 2

    def step(p, w):
        delta = [S.Integer(0) for _ in codes]
        activity = S.Integer(0)
        contrast = S.Integer(0)
        for u, v in edges:
            denominator = L * (w[u] + w[v])
            flux = (w[u] * p[v] - w[v] * p[u]) / denominator
            delta[u] += flux
            delta[v] -= flux
            activity += (w[u] * p[v] + w[v] * p[u]) / denominator
            contrast += (w[u] - w[v]) * (p[u] - p[v]) / denominator
        return [p[i] + delta[i] for i in range(n)], activity, S.Rational(1, 2) - contrast / 2

    def make_case(x):
        weights = [x ** (m - L // 2) for m in aligned]
        Z = sum(weights)
        gamma = [w / Z for w in weights]
        K = []
        basis_activities = []
        basis_activities_eq40 = []
        for j in range(n):
            impulse = [S.Integer(int(i == j)) for i in range(n)]
            new, activity, activity40 = step(impulse, weights)
            K.append(new)
            basis_activities.append(activity)
            basis_activities_eq40.append(activity40)
        after, R, R40 = step(gamma, weights)
        transfer = S.Matrix([[x, 1], [1, x]])
        Ztransfer = S.trace(transfer ** L) * x ** (-L // 2)
        return {'x': x, 'weights': weights, 'partition_function': Z,
                'transfer_partition_function': Ztransfer, 'gibbs': gamma,
                'row_kernel': K, 'basis_activities': basis_activities,
                'basis_activities_eq40': basis_activities_eq40,
                'equilibrium_after_step': after,
                'equilibrium_activity': R, 'equilibrium_activity_eq40': R40}

    cases = [make_case(x) for x in (S.Rational(1), S.Rational(3, 2), S.Rational(2), S.Rational(3))]
    by_x = {c['x']: c for c in cases}
    protocol = [S.Rational(3, 2), S.Rational(2), S.Rational(2), S.Rational(3)]
    p = by_x[protocol[0]]['gibbs'][:]
    initial = p[:]
    steps = []
    for k, x in enumerate(protocol[1:]):
        new, R, R40 = step(p, by_x[x]['weights'])
        steps.append({'k': k, 'bath_x': x, 'before': p, 'after': new,
                      'activity': R, 'activity_eq40': R40})
        p = new

    x = S.Symbol('x', positive=True)
    symbolic_weights = [x ** (m - L // 2) for m in aligned]
    symbolic_Z = sum(symbolic_weights)
    symbolic_p = [w / symbolic_Z for w in symbolic_weights]
    _, symbolic_R, _ = step(symbolic_p, symbolic_weights)
    symbolic_R = S.factor(symbolic_R)
    symbolic_Z = S.factor(symbolic_Z)
    symbolic_transfer = S.factor(S.trace(S.Matrix([[x, 1], [1, x]]) ** L) * x ** (-L // 2))
    data = {'schema': 1, 'job_id': 'phys-smallmac00006-p01-reproduce-8cc0c1fb7af6',
            'construction': 'Independent derivation from bond counts and complementary edge acceptance; synchronous unit-impulse replay.',
            'source_derivation': 'evidence/independent-derivation-b.md',
            'implementation': 'code/reconstruct_b.py',
            'conventions': 'Gray-coded little-endian spin bits; row kernel K; delta buffer reads unchanged old p on all edges.',
            'L': L, 'N': n, 'z': L,
            'states': [{'index': i, 'gray_code': g, 'spin_bits_little_endian': bits[i],
                        'aligned_bonds': aligned[i], 'energy_J': L - 2 * aligned[i]}
                       for i, g in enumerate(codes)],
            'undirected_edges': edges, 'cases': cases,
            'protocol': {'x_schedule': protocol, 'initial': initial, 'steps': steps},
            'symbolic': {'variable': 'x>0; physical positive beta requires x>1',
                         'partition_function': str(symbolic_Z),
                         'transfer_partition_function': str(symbolic_transfer),
                         'equilibrium_activity': str(symbolic_R)},
            'arithmetic': 'SymPy Rational and exact symbolic rational functions; no A data/code read'}

    def encode(v):
        if isinstance(v, S.Basic):
            return str(v)
        if isinstance(v, dict):
            return {k: encode(w) for k, w in v.items()}
        if isinstance(v, (list, tuple)):
            return [encode(w) for w in v]
        return v

    (root / 'evidence/input-b.json').write_text(json.dumps(encode(data), indent=2) + '\n')
    print('B generated independently; no A script, matrix, JSON or cached result read.')
    print('Gray basis; {} unique synchronous edges; row kernel from all unit impulses.'.format(len(edges)))
    for c in cases:
        print('L=4 x={} Z={} Z_transfer={} R_edge={} R_eq40={}'.format(
            c['x'], c['partition_function'], c['transfer_partition_function'],
            c['equilibrium_activity'], c['equilibrium_activity_eq40']))
    print('Independent symbolic Z4:', symbolic_Z)
    print('Independent symbolic R4:', symbolic_R)
    print(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
                      'wall_seconds': time.perf_counter() - start,
                      'maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'maxrss_unit': 'bytes on macOS; KiB on Linux',
                      'python': platform.python_version(), 'sympy': S.__version__,
                      'platform': platform.system()}))


if __name__ == '__main__':
    main()
