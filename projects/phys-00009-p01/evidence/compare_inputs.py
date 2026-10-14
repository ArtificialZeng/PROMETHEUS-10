"""Exact row-by-row source-reconstruction and input admissibility checks."""
import json
from datetime import datetime, timezone
from fractions import Fraction as F
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def matrix(value):
    return [[F(x) for x in row] for row in value]


def connected(rows):
    seen = {0}
    pending = [0]
    while pending:
        i = pending.pop()
        for j, entry in enumerate(rows[i]):
            if j != i and entry > 0 and j not in seen:
                seen.add(j)
                pending.append(j)
    return len(seen) == len(rows)


if __name__ == '__main__':
    with (HERE / 'input-comparison.log').open('w') as log:
        def record(message):
            print(message)
            log.write(message + '\n')
            log.flush()
        record('UTC ' + datetime.now(timezone.utc).isoformat())
        record('Command: python3 evidence/compare_inputs.py')
        record('Arithmetic: exact fractions.Fraction; zero entry tolerance.')
        data_a = json.loads((HERE / 'input-a.json').read_text())
        data_b = json.loads((HERE / 'input-b.json').read_text())
        a = {case['id']: case for case in data_a['cases']}
        b = {case['id']: case for case in data_b['cases']}
        assert set(a) == set(b)
        reports = []
        entry_count = 0
        for name, aa in a.items():
            bb = b[name]
            assert aa['n'] == bb['n'] and aa['k'] == bb['k']
            assert aa['alpha'] == bb['alpha'] and aa['edges'] == bb['edges']
            n, k = aa['n'], aa['k']
            assert all(F(v) > 0 for v in aa['alpha'])
            conductance = [[F(0) for _ in range(n)] for _ in range(n)]
            for x, y, value in aa['edges']:
                assert x < y and F(value) > 0
                conductance[x][y] = conductance[y][x] = F(value)
            assert connected(conductance)
            states_a = [tuple(v) for v in aa['state_order']]
            states_b = [tuple(v) for v in bb['state_order']]
            assert len(set(states_a)) == len(states_a)
            assert len(set(states_b)) == len(states_b)
            assert set(states_a) == set(states_b)
            size = len(states_a)
            assert size == comb(n + k - 1, k)
            assert all(sum(v) == k and min(v) >= 0 for v in states_a)
            pos_b = {state: j for j, state in enumerate(states_b)}
            p = [pos_b[state] for state in states_a]
            la, lb, kb = matrix(aa['L_backward']), matrix(bb['L_backward_from_form']), matrix(bb['K_incidence'])
            ma, mb = list(map(F, aa['mu'])), list(map(F, bb['mu']))
            assert all(m > 0 for m in ma + mb)
            assert sum(ma) == sum(mb) == 1
            assert F(aa['Z_closed']) == F(bb['Z_direct_sum'])
            assert all(ma[i] == mb[p[i]] for i in range(size))
            for i in range(size):
                assert len(la[i]) == size
                assert sum(la[i]) == 0
                assert la[i][i] <= 0
                for j in range(size):
                    assert la[i][j] == lb[p[i]][p[j]], (name, i, j)
                    assert -ma[i] * la[i][j] == kb[p[i]][p[j]]
                    assert kb[p[i]][p[j]] == kb[p[j]][p[i]]
                    assert ma[i] * la[i][j] == ma[j] * la[j][i]
                    if i != j:
                        assert la[i][j] >= 0
                        if la[i][j]:
                            delta = [states_a[j][x] - states_a[i][x] for x in range(n)]
                            assert delta.count(1) == delta.count(-1) == 1
                            assert all(d in (-1, 0, 1) for d in delta)
                assert sum(ma[j] * la[j][i] for j in range(size)) == 0
                record(name + ': row ' + str(i) + ' A->B ' + str(p[i]) + '; ' + str(size) + ' exact entries agree, mass/form map and detailed balance agree.')
            assert connected(la)
            for edge in bb['unoriented_configuration_edges']:
                i, j, q = edge['i'], edge['j'], F(edge['q'])
                assert q > 0 and q == mb[i] * lb[i][j] == mb[j] * lb[j][i]
            record(name + ': PASS positive legal rates; constant row kernel; exact stationary normalization; configuration graph connected; reversible incidence form positive semidefinite.')
            entry_count += size * size
            reports.append({'id': name, 'dimension': size, 'a_to_b_permutation': p,
                            'matrix_entries_compared': size * size,
                            'configuration_edges': len(bb['unoriented_configuration_edges']),
                            'normalization': aa['Z_closed'], 'status': 'pass'})
        summary = {'status': 'pass', 'mode': 'exact', 'case_count': len(reports),
                   'matrix_entries_compared': entry_count, 'cases': reports,
                   'scope': 'Input admissibility and equality of two assemblies only; no universal gap result.'}
        (HERE / 'input-comparison.json').write_text(json.dumps(summary, indent=2) + '\n')
        record('TOTAL PASS: ' + str(len(reports)) + ' cases; ' + str(entry_count) + ' exact matrix entries; no mismatches.')
