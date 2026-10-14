"""Input A: direct transcription of primary SIP generator (2.1), measure (2.2).

Does not import or read reconstruction B or any computed cache. Standard library only.
"""
import json
from fractions import Fraction as F
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent


def compositions(total, sites):
    if sites == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, sites - 1):
            yield (first,) + tail


def rising(a, m):
    answer = F(1)
    for r in range(m):
        answer *= a + r
    return answer


def reconstruct(spec, k):
    n = spec['n']
    alpha = list(map(F, spec['alpha']))
    c = [[F(0) for _ in range(n)] for _ in range(n)]
    for x, y, rate in spec['edges']:
        c[x][y] = c[y][x] = F(rate)
    states = list(compositions(k, n))
    index = {state: i for i, state in enumerate(states)}
    dim = len(states)
    generator = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for i, eta in enumerate(states):
        for x in range(n):
            if eta[x] == 0:
                continue
            for y in range(n):
                if x == y or not c[x][y]:
                    continue
                target = list(eta)
                target[x] -= 1
                target[y] += 1
                j = index[tuple(target)]
                rate = c[x][y] * eta[x] * (alpha[y] + eta[y])
                generator[i][j] += rate
                generator[i][i] -= rate
    normalization = rising(sum(alpha), k) / factorial(k)
    probabilities = []
    for eta in states:
        weight = F(1)
        for x, m in enumerate(eta):
            weight *= rising(alpha[x], m) / factorial(m)
        probabilities.append(weight / normalization)
    return {
        'id': spec['id'] + '-k' + str(k), 'family': spec['id'], 'k': k,
        'n': n, 'alpha': spec['alpha'], 'edges': spec['edges'],
        'state_order': [list(state) for state in states],
        'L_backward': [[str(entry) for entry in row] for row in generator],
        'mu': list(map(str, probabilities)), 'Z_closed': str(normalization),
    }


if __name__ == '__main__':
    specs = json.loads((HERE / 'reproduction-cases.json').read_text())['families']
    cases = [reconstruct(spec, k) for spec in specs for k in spec['particle_numbers']]
    output = {
        'representation': 'Direct ordered-pair jump generator on function column vectors; rows indexed by source state.',
        'primary_inputs': 'Kim-Sau journal Eqs. (2.1), (2.2).',
        'source_evidence': 'evidence/reproduce-model-dirichlet-tool-return.json',
        'construction_code': 'evidence/reconstruct_a.py',
        'case_specification': 'evidence/reproduction-cases.json',
        'arithmetic': 'Exact fractions.Fraction; rational strings.',
        'cases': cases,
    }
    (HERE / 'input-a.json').write_text(json.dumps(output, indent=2) + '\n')
    print('Input A wrote', len(cases), 'cases from independent direct jump assembly.')

