#!/usr/bin/env python3
"""A: direct spin energies and column kernel. Reads no generated scientific data."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json
import platform
import resource
import time


def main():
    start = time.perf_counter()
    root = Path(__file__).resolve().parents[1]
    L = 4
    spins = list(product((-1, 1), repeat=L))
    energy = [-sum(s[a] * s[(a + 1) % L] for a in range(L)) for s in spins]
    n = len(spins)

    def make_case(x):
        weights = [x ** (-(e // 2)) for e in energy]
        Z = sum(weights, F(0))
        gamma = [w / Z for w in weights]
        P = [[F(0) for _ in range(n)] for _ in range(n)]
        for j in range(n):
            for i in range(n):
                if sum(a != b for a, b in zip(spins[i], spins[j])) == 1:
                    de = energy[i] - energy[j]
                    assert de % 2 == 0
                    P[i][j] = 1 / (L * (1 + x ** (de // 2)))
            P[j][j] = 1 - sum(P[i][j] for i in range(n) if i != j)
        escape = [sum(P[i][j] for i in range(n) if i != j) for j in range(n)]
        R = sum(gamma[j] * escape[j] for j in range(n))
        return {'x': x, 'weights': weights, 'partition_function': Z,
                'gibbs': gamma, 'column_kernel': P, 'escape_probability': escape,
                'equilibrium_activity': R}

    cases = [make_case(x) for x in (F(1), F(3, 2), F(2), F(3))]
    by_x = {c['x']: c for c in cases}
    protocol = (F(3, 2), F(2), F(2), F(3))
    p = by_x[protocol[0]]['gibbs'][:]
    initial = p[:]
    steps = []
    for k, x in enumerate(protocol[1:]):
        c = by_x[x]
        P = c['column_kernel']
        new = [sum(P[i][j] * p[j] for j in range(n)) for i in range(n)]
        activity = sum(c['escape_probability'][j] * p[j] for j in range(n))
        steps.append({'k': k, 'bath_x': x, 'before': p, 'after': new,
                      'activity': activity})
        p = new

    data = {'schema': 1, 'job_id': 'phys-smallmac00006-p01-reproduce-8cc0c1fb7af6',
            'construction': 'Direct source transcription; lexicographic spins; full destination/source pair loop.',
            'source_transcription': 'evidence/source-transcription-a.md',
            'implementation': 'code/reconstruct_a.py',
            'conventions': 'J sets the energy unit; x=exp(2 beta J); one uniformly proposed spin; column kernel.',
            'L': L, 'N': n, 'z': L,
            'states': [{'index': i, 'spins': list(s), 'energy_J': energy[i]} for i, s in enumerate(spins)],
            'cases': cases,
            'protocol': {'x_schedule': list(protocol), 'initial': initial, 'steps': steps},
            'arithmetic': 'Python fractions.Fraction, exact unbounded integer arithmetic'}

    def encode(v):
        if isinstance(v, F):
            return str(v)
        if isinstance(v, dict):
            return {k: encode(w) for k, w in v.items()}
        if isinstance(v, (list, tuple)):
            return [encode(w) for w in v]
        return v

    (root / 'evidence/input-a.json').write_text(json.dumps(encode(data), indent=2) + '\n')
    print('A generated independently from source-transcription-a.md; no input-b or cached data read.')
    for c in cases:
        print('L=4 x={} Z={} R={}'.format(c['x'], c['partition_function'], c['equilibrium_activity']))
    print('Protocol activities:', ', '.join(str(s['activity']) for s in steps))
    print(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
                      'wall_seconds': time.perf_counter() - start,
                      'maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'maxrss_unit': 'bytes on macOS; KiB on Linux',
                      'python': platform.python_version(), 'platform': platform.system()}))


if __name__ == '__main__':
    main()
