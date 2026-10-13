#!/usr/bin/env python3
"""Compare A/B after separate generation; published baseline is evaluated here."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
from math import comb
import hashlib
import json
import platform
import resource
import time
import sympy as S


def main():
    start = time.perf_counter()
    root = Path(__file__).resolve().parents[1]
    a = json.loads((root / 'evidence/input-a.json').read_text())
    b = json.loads((root / 'evidence/input-b.json').read_text())
    lines = ['Exact independent-input comparison',
             'A: lexicographic spin states, destination/source column kernel.',
             'B: Gray-coded little-endian bit states, source/destination row kernel.',
             'Convention map: P_A = U K_B^T U^T; p_A=U p_B.',
             'Independence: same worker; different derivation/representation/arithmetic; no generated input shared.']
    baseline = ['Published baseline: Burovski arXiv:1907.06776v2 PDF p.8 Appendix B Eqs.(23),(24); p.3 Eq.(11).',
                'Primary target L=4, beta J=log(2)/2, x=2. All arithmetic exact; tolerance 0.',
                'No Monte Carlo, finite precision rounding, truncation or thermodynamic-limit substitution.']

    def check(condition, message):
        if not condition:
            raise AssertionError(message)

    n, L = a['N'], a['L']
    check((n, L, a['z']) == (16, 4, 4) == (b['N'], b['L'], b['z']), 'Model size mismatch')
    spin_index = {tuple(s['spins']): s['index'] for s in a['states']}
    mapping = []
    for sb in b['states']:
        bits = sb['spin_bits_little_endian']
        i = spin_index[tuple(2 * bit - 1 for bit in bits)]
        explicit_i = sum(((sb['gray_code'] >> r) & 1) << (L - 1 - r) for r in range(L))
        check(i == explicit_i, 'Explicit basis map failed')
        check(a['states'][i]['energy_J'] == sb['energy_J'], 'Energy conventions mismatch')
        mapping.append(i)
        lines.append('B index {} (Gray {}) -> A index {}; E/J={}'.format(
            sb['index'], sb['gray_code'], i, sb['energy_J']))
    check(sorted(mapping) == list(range(n)), 'Basis map is not bijective')
    edge_set = {tuple(sorted((mapping[u], mapping[v]))) for u, v in b['undirected_edges']}
    expected_edges = {(i, j) for i in range(n) for j in range(i + 1, n)
                      if sum(u != v for u, v in zip(a['states'][i]['spins'], a['states'][j]['spins'])) == 1}
    check(edge_set == expected_edges and len(edge_set) == 32, 'Proposal graph mismatch')
    degree = [sum(i in edge for edge in edge_set) for i in range(n)]
    check(degree == [4] * n, 'Graph is not 4-regular')
    reached = {0}
    while True:
        new = reached | {v for u, v in edge_set if u in reached} | {u for u, v in edge_set if v in reached}
        if reached == new:
            break
        reached = new
    check(len(reached) == n, 'Graph is not connected')
    lines.append('Graph: exactly 32 unique undirected non-loop edges; connected; every degree=4.')

    results = []
    check([c['x'] for c in a['cases']] == [c['x'] for c in b['cases']], 'Fixture temperatures mismatch')
    for ca, cb in zip(a['cases'], b['cases']):
        x = F(ca['x'])
        P = [[F(v) for v in row] for row in ca['column_kernel']]
        K = [[F(v) for v in row] for row in cb['row_kernel']]
        ga = [F(v) for v in ca['gibbs']]
        gb = [F(v) for v in cb['gibbs']]
        for j in range(n):
            check(ga[mapping[j]] == gb[j], 'Gibbs basis map mismatch')
            check(F(ca['weights'][mapping[j]]) == F(cb['weights'][j]), 'Weight mismatch')
            for i in range(n):
                check(P[mapping[i]][mapping[j]] == K[j][i], 'Kernel entry mismatch')
                check(P[i][j] >= 0, 'Negative transition probability')
                check(P[i][j] * ga[j] == P[j][i] * ga[i], 'Detailed balance mismatch')
                if i != j and tuple(sorted((i, j))) not in edge_set:
                    check(P[i][j] == 0, 'Non-neighbor transition')
            check(sum(P[i][j] for i in range(n)) == 1, 'Column normalization failed')
            check(sum(K[j]) == 1, 'Row normalization failed')
            check(F(cb['basis_activities'][j]) == F(cb['basis_activities_eq40'][j]) ==
                  F(ca['escape_probability'][mapping[j]]), 'Eq.(40) fails on a basis distribution')
        for i in range(n):
            check(sum(P[i][j] * ga[j] for j in range(n)) == ga[i], 'Stationarity mismatch')
            check(F(cb['equilibrium_after_step'][i]) == gb[i], 'Edge stationarity mismatch')
            lines.append('x={} A row {}: all 16 mapped entries equal exactly.'.format(x, i))
        check(sum(ga) == 1 and min(ga) > 0, 'Gibbs positivity/normalization')

        Z11 = x ** (-L // 2) * ((x + 1) ** L + (x - 1) ** L)
        eta = (x - 1) / (x + 1)
        R24 = x / (1 + x * x) * (1 - eta ** L) / (1 + eta ** L)
        R23 = F(0)
        for m in range(0, L + 1, 2):
            conditional = (F(m * (m - 1), L * (L - 1)) / (1 + x * x)
                           + x * x / (1 + x * x) * F((L - m) * (L - m - 1), L * (L - 1))
                           + F((L - m) * m, L * (L - 1)))
            layer = 2 * x ** (-L // 2) * comb(L, m) * x ** m / Z11
            R23 += conditional * layer
        Za, Zb = F(ca['partition_function']), F(cb['partition_function'])
        Ra, Rb = F(ca['equilibrium_activity']), F(cb['equilibrium_activity'])
        check(Za == Zb == F(cb['transfer_partition_function']) == Z11, 'Published partition baseline failed')
        check(Ra == Rb == F(cb['equilibrium_activity_eq40']) == R23 == R24, 'Published activity baseline failed')
        if x == 2:
            check(Za == F(41, 2) and Ra == F(16, 41), 'Chosen baseline failed')
        if x == 1:
            check(Za == 16 and Ra == F(1, 2), 'Infinite-temperature diagnostic failed')
        baseline.append('L=4 x={}: Z_enumA=Z_bondB=Tr(T^4)=Eq.(11)={}; R_A=R_B=Eq.(40)=Eq.(23)=Eq.(24)={}.'.format(x, Za, Ra))
        lines.append('x={}: 256 entries, 256 detailed-balance pairs, 16 column/row sums, 16 stationarity equations and 16 basis-activity identities PASS.'.format(x))
        results.append({'x': str(x), 'Z': str(Za), 'R': str(Ra), 'kernel_entries': n*n,
                        'max_exact_kernel_residual': '0', 'max_exact_detailed_balance_residual': '0',
                        'boundary_diagnostic_only': x == 1})

    pa, pb = a['protocol'], b['protocol']
    check(pa['x_schedule'] == pb['x_schedule'], 'Protocol mismatch')
    schedule = [F(x) for x in pa['x_schedule']]
    check(schedule[0] > 1 and all(u <= v for u, v in zip(schedule, schedule[1:])), 'Protocol inadmissible')
    check(pa['initial'] == a['cases'][1]['gibbs'], 'A initial state is not designated Gibbs state')
    check(pb['initial'] == b['cases'][1]['gibbs'], 'B initial state is not designated Gibbs state')
    for sa, sb in zip(pa['steps'], pb['steps']):
        check(sa['k'] == sb['k'] and sa['bath_x'] == sb['bath_x'], 'Step convention mismatch')
        for name in ('before', 'after'):
            va, vb = [F(v) for v in sa[name]], [F(v) for v in sb[name]]
            check(sum(va) == sum(vb) == 1 and min(va + vb) >= 0, 'Protocol distribution inadmissible')
            check(all(va[mapping[j]] == vb[j] for j in range(n)), 'Protocol replay mismatch')
        check(F(sa['activity']) == F(sb['activity']) == F(sb['activity_eq40']), 'Protocol activity mismatch')
        lines.append('Protocol k={} x={}: both distributions and A^D={} match exactly; activity uses step-before p.'.format(sa['k'], sa['bath_x'], sa['activity']))
    lines.append('Protocol is an implementation cross-check, not a general conjecture scan or proof.')

    x = S.Symbol('x', positive=True)
    eta = (x - 1) / (x + 1)
    R24 = x / (1 + x*x) * (1 - eta**4) / (1 + eta**4)
    Z11 = x**(-2) * ((x + 1)**4 + (x - 1)**4)
    symbolic = b['symbolic']
    rb = S.sympify(symbolic['equilibrium_activity'], locals={'x': x})
    zb = S.sympify(symbolic['partition_function'], locals={'x': x})
    zt = S.sympify(symbolic['transfer_partition_function'], locals={'x': x})
    check(S.cancel(rb - R24) == 0, 'Symbolic finite-temperature R4 baseline failed')
    check(S.cancel(zb - Z11) == S.cancel(zt - Z11) == 0, 'Symbolic partition baseline failed')
    baseline.append('Independent symbolic B: R4={}; Z4={}.'.format(rb, zb))
    baseline.append('Exact rational-function residuals R4-Eq.(24), Z4-Eq.(11), Tr(T^4)-Eq.(11): 0, 0, 0.')
    baseline.append('For x>1 denominators x, 1+x^2, 1+eta^4 are nonzero. No asymptotic or perturbative approximation.')
    baseline.append('Reproduced known formulas only. Original all-regular-graph annealing conjecture remains unresolved.')
    energy_counts = {}
    for state in a['states']:
        e = str(state['energy_J'])
        energy_counts[e] = energy_counts.get(e, 0) + 1
    baseline.append('Energy degeneracies E/J: ' + json.dumps(energy_counts, sort_keys=True))

    def fraction_bits(v):
        if isinstance(v, dict):
            return max([fraction_bits(w) for w in v.values()] + [0])
        if isinstance(v, list):
            return max([fraction_bits(w) for w in v] + [0])
        if isinstance(v, str):
            try:
                f = F(v)
                return max(abs(f.numerator).bit_length(), f.denominator.bit_length())
            except (ValueError, ZeroDivisionError):
                return 0
        return 0

    statistics = {'job_id': a['job_id'], 'finished_at': datetime.now(timezone.utc).isoformat(),
                  'status': 'pass', 'basis_B_to_A': mapping, 'energy_degeneracies': energy_counts,
                  'cases': results, 'symbolic_baseline_residuals': ['0', '0', '0'],
                  'protocol_steps_compared': len(pa['steps']),
                  'maximum_stored_rational_numerator_or_denominator_bits': max(fraction_bits(a), fraction_bits(b)),
                  'wall_seconds': time.perf_counter() - start,
                  'maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  'maxrss_unit': 'bytes on macOS; KiB on Linux',
                  'python': platform.python_version(), 'sympy': S.__version__, 'platform': platform.system(),
                  'input_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                                   for name in ('evidence/input-a.json', 'evidence/input-b.json')},
                  'limitations': 'Same-worker implementation independence; no fresh scientific referee; L=4 baseline only; target unresolved.'}
    (root / 'evidence/input-comparison.log').write_text('\n'.join(lines + ['PASS']) + '\n')
    (root / 'evidence/baseline.log').write_text('\n'.join(baseline + ['PASS']) + '\n')
    (root / 'evidence/reproduction-checks.json').write_text(json.dumps(statistics, indent=2) + '\n')
    print('\n'.join(baseline))
    print('Comparison: PASS; 4 x 256 exact kernel entries and all linked checks.')
    print(json.dumps(statistics, indent=2))


if __name__ == '__main__':
    main()
