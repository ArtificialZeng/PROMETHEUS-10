"""Finite witness A: explicit destination/source matrix, Python Fraction."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib
import json
import resource
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    started = datetime.now(timezone.utc).isoformat()
    begin = time.perf_counter()
    spec = json.loads((ROOT / 'evidence/layered-witness-spec.json').read_text())
    e = spec['energies']
    qs = list(map(F, spec['q_protocol']))
    n, z = spec['n'], spec['degree']
    edges = [(i, j) for i in range(3) for j in range(3, 7)]
    edges += [(j, j + 4) for j in range(3, 7)]
    edges += [(i, j) for i in range(7, 11) for j in range(i + 1, 11)]
    edges = sorted(edges)
    assert len(set(edges)) == len(edges) == 22
    adj = [[int(tuple(sorted((i, j))) in edges) for j in range(n)] for i in range(n)]
    assert all(sum(r) == z for r in adj)
    reached = {0}
    while True:
        new = reached | {j for i in reached for j in range(n) if adj[i][j]}
        if new == reached:
            break
        reached = new
    assert len(reached) == n
    assert F(1) < qs[0] < qs[1] < qs[2]
    kernels, gibbss = [], []
    for q in qs:
        m = [[F(0) for j in range(n)] for i in range(n)]
        for j in range(n):
            for i in range(n):
                if adj[i][j]:
                    m[i][j] = 1 / (z * (1 + q ** (e[i] - e[j])))
            m[j][j] = 1 - sum(m[i][j] for i in range(n))
        g = [q ** (-v) for v in e]
        g = [v / sum(g) for v in g]
        assert all(sum(m[i][j] for i in range(n)) == 1 for j in range(n))
        assert all(v >= 0 for row in m for v in row)
        assert all(m[i][j] * g[j] == m[j][i] * g[i] for i in range(n) for j in range(n))
        assert [sum(m[i][j] * g[j] for j in range(n)) for i in range(n)] == g
        kernels.append(m)
        gibbss.append(g)
    distributions = [gibbss[0]]
    activities = []
    for k in range(2):
        m = kernels[k + 1]
        p = distributions[-1]
        activities.append(sum(p[j] * sum(m[i][j] for i in range(n) if i != j) for j in range(n)))
        new = [sum(m[i][j] * p[j] for j in range(n)) for i in range(n)]
        assert sum(new) == 1 and min(new) > 0
        distributions.append(new)
    mean = sum(activities) / 2
    assert activities[0] < F(1, 2)
    assert activities[1] > F(63, 125) > F(1, 2)
    assert mean > F(251, 500) > F(1, 2)

    def serialize(v):
        if isinstance(v, F):
            return str(v)
        if isinstance(v, list):
            return [serialize(x) for x in v]
        if isinstance(v, dict):
            return {k: serialize(x) for k, x in v.items()}
        return v

    record = {'method': 'Explicit 11x11 column matrices from destination-minus-source energies; Python Fraction.',
              'started_at': started, 'finished_at': datetime.now(timezone.utc).isoformat(),
              'edges': edges, 'energies': e, 'q_protocol': qs, 'kernels': kernels,
              'instantaneous_gibbs': gibbss, 'distributions': distributions,
              'activities': activities, 'mean_activity': mean,
              'step_excess': activities[1] - F(1, 2), 'mean_excess': mean - F(1, 2),
              'strict_rational_checks': {'A1_minus_63_over_125': activities[1] - F(63, 125),
                                         'mean_minus_251_over_500': mean - F(251, 500)},
              'max_probability_rational_bits': max(max(abs(v.numerator).bit_length(), v.denominator.bit_length()) for p in distributions for v in p),
              'elapsed_seconds': time.perf_counter() - begin,
              'peak_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'spec_sha256': hashlib.sha256((ROOT / 'evidence/layered-witness-spec.json').read_bytes()).hexdigest(),
              'independence_limit': 'Same worker as B. A reads only the frozen model specification, no B generated output.'}
    (ROOT / 'evidence/layered-exact-a.json').write_text(json.dumps(serialize(record), indent=2) + '\n')
    log = ['Exact matrix reconstruction A', 'n=11, z=4, edges=22, simple connected regular PASS',
           'q0=10001/10000 < q1=33/32 < q2=64, all >1 PASS',
           'All three 11x11 matrices: support, nonnegativity, column sums, detailed balance and Gibbs stationarity PASS',
           'Gibbs initial; both synchronous updates normalized and strictly positive PASS']
    for k, a in enumerate(activities):
        log += [f'A{k} exact = {a}', f'A{k} decimal display only = {float(a):.16g}']
    log += [f'mean exact = {mean}', f'mean decimal display only = {float(mean):.16g}',
            'A1 > 63/125 > 1/2 and mean > 251/500 > 1/2: exact cross-multiplication PASS',
            f'elapsed_seconds={record["elapsed_seconds"]:.6f}; peak_rss_bytes_macos={record["peak_rss_bytes_macos"]}',
            'Not a fresh referee; candidate verification only.']
    (ROOT / 'evidence/layered-exact-a.log').write_text('\n'.join(log) + '\n')
    print('\n'.join(line for line in log if ' exact = ' not in line))


if __name__ == '__main__':
    main()
