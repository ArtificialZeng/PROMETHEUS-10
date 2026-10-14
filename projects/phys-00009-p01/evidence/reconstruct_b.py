"""Input B: reversible incidence form derived from primary Eqs. (2.2), (3.7).

This script does not import A or read A's matrices/probabilities. It shares only
fixed graph/alpha/k specifications, independently enumerates states, normalizes
local recurrence weights by an explicit sum, and builds unoriented edge forms
from (k-1)-particle states. The derivation is in reconstruction-map.md.
"""
import itertools
import json
from fractions import Fraction as R
from pathlib import Path

LOCATION = Path(__file__).resolve().parent


def occupancies(m, n):
    # Reverse lexicographic product/filter, different from A's weak compositions.
    return [v for v in itertools.product(range(m, -1, -1), repeat=n) if sum(v) == m]


def distribution(states, parameters):
    m = sum(states[0])
    site = []
    for a in parameters:
        values = [R(1)]
        for count in range(1, m + 1):
            values.append(values[-1] * (a + count - 1) / count)
        site.append(values)
    unnormalized = []
    for v in states:
        entry = R(1)
        for x, count in enumerate(v):
            entry *= site[x][count]
        unnormalized.append(entry)
    total = sum(unnormalized)
    return [entry / total for entry in unnormalized], total


def derive(spec, particles):
    n = spec['n']
    a = [R(s) for s in spec['alpha']]
    states = occupancies(particles, n)
    positions = {v: i for i, v in enumerate(states)}
    mass, direct_z = distribution(states, a)
    residual_states = occupancies(particles - 1, n)
    residual_mass, residual_z = distribution(residual_states, a)
    size = len(states)
    stiffness = [[R(0) for _ in range(size)] for _ in range(size)]
    conductances = []
    scale = R(particles) / (sum(a) + particles - 1)
    for zeta, prob in zip(residual_states, residual_mass):
        for x, y, weight in spec['edges']:
            assert 0 <= x < y < n
            vx, vy = list(zeta), list(zeta)
            vx[x] += 1
            vy[y] += 1
            i, j = positions[tuple(vx)], positions[tuple(vy)]
            q = scale * prob * R(weight) * (a[x] + zeta[x]) * (a[y] + zeta[y])
            stiffness[i][i] += q
            stiffness[j][j] += q
            stiffness[i][j] -= q
            stiffness[j][i] -= q
            conductances.append({'zeta': list(zeta), 'x': x, 'y': y,
                                 'i': i, 'j': j, 'q': str(q)})
    backward = [[-entry / mass[i] for entry in row]
                for i, row in enumerate(stiffness)]
    return {
        'id': spec['id'] + '-k' + str(particles), 'family': spec['id'],
        'k': particles, 'n': n, 'alpha': spec['alpha'], 'edges': spec['edges'],
        'state_order': [list(v) for v in states], 'mu': list(map(str, mass)),
        'Z_direct_sum': str(direct_z), 'Z_residual_direct_sum': str(residual_z),
        'K_incidence': [[str(entry) for entry in row] for row in stiffness],
        'L_backward_from_form': [[str(entry) for entry in row] for row in backward],
        'unoriented_configuration_edges': conductances,
    }


if __name__ == '__main__':
    examples = json.loads((LOCATION / 'reproduction-cases.json').read_text())['families']
    cases = [derive(example, k) for example in examples for k in example['particle_numbers']]
    output = {
        'representation': 'Symmetric unoriented-edge stiffness K; generator L=-diag(mu)^(-1) K in B order.',
        'primary_inputs': 'Kim-Sau journal Eqs. (2.2), (3.7). Conductance formula independently derived in reconstruction-map.md.',
        'source_evidence': 'evidence/reproduce-versions-scope-form-tool-return.json',
        'construction_code': 'evidence/reconstruct_b.py',
        'derivation': 'evidence/reconstruction-map.md',
        'case_specification': 'evidence/reproduction-cases.json',
        'arithmetic': 'Exact fractions.Fraction; rational strings.',
        'cases': cases,
    }
    (LOCATION / 'input-b.json').write_text(json.dumps(output, indent=2) + '\n')
    print('Input B wrote', len(cases), 'cases from independent (k-1)-configuration incidence assembly.')
