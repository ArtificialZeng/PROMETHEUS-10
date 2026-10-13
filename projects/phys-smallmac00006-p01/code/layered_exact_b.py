"""Witness B: independent labeled undirected-edge synchronous flux, SymPy Rational.

Reads neither A's code/data nor generated matrices or cached answers.
The graph and parameter transcription are shared scientific premises.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations
import hashlib
import json
import resource
import time
from sympy import Rational as R

ROOT = Path(__file__).resolve().parents[1]


def main():
    started = datetime.now(timezone.utc).isoformat()
    begin = time.perf_counter()
    labels = ['c3', 'c2', 'c1', 'c0', 'b3', 'b2', 'b1', 'b0', 'a2', 'a1', 'a0']
    edges = [(f'a{i}', f'b{j}') for j in range(4) for i in range(3)]
    edges += [(f'c{j}', f'b{j}') for j in range(4)]
    edges += list(combinations([f'c{i}' for i in range(4)], 2))
    energies = {s: {'a': 0, 'b': 1, 'c': 64}[s[0]] for s in labels}
    qs = [R(10001, 10000), R(33, 32), R(64)]
    degree = {s: sum(s in edge for edge in edges) for s in labels}
    assert set(degree.values()) == {4} and len(set(map(frozenset, edges))) == 22
    mapping = {s: int(s[1:]) + {'a': 0, 'b': 3, 'c': 7}[s[0]] for s in labels}

    def evolve(old, q):
        weights = {s: q ** (-energies[s]) for s in labels}
        delta = {s: R(0) for s in labels}
        activity = R(0)
        per_edge = []
        pi = {s: R(0) for s in labels}
        for i, j in edges:
            denominator = 4 * (weights[i] + weights[j])
            forward = old[i] * weights[j] / denominator
            backward = old[j] * weights[i] / denominator
            delta[i] += backward - forward
            delta[j] += forward - backward
            activity += forward + backward
            term = (weights[i] - weights[j]) / (weights[i] + weights[j]) * (old[i] - old[j])
            pi[i] += term
            pi[j] += term
            per_edge.append({'edge': [i, j], 'i_to_j': str(forward), 'j_to_i': str(backward), 'passivity_term': str(term)})
        new = {s: old[s] + delta[s] for s in labels}
        assert sum(new.values()) == sum(old.values())
        assert activity == sum(old.values()) / 2 - sum(pi.values()) / 16
        return new, activity, pi, per_edge

    row_kernels = []
    for q in qs:
        rows = []
        weights = {s: q ** (-energies[s]) for s in labels}
        equilibrium = {s: v / sum(weights.values()) for s, v in weights.items()}
        stationary, _, _, _ = evolve(equilibrium, q)
        assert stationary == equilibrium
        for source in labels:
            new, activity, _, _ = evolve({s: R(s == source) for s in labels}, q)
            assert min(new.values()) >= 0 and sum(new.values()) == 1
            assert activity == 1 - new[source]
            rows.append([str(new[s]) for s in labels])
        row_kernels.append(rows)
    weight0 = {s: qs[0] ** (-energies[s]) for s in labels}
    p = {s: w / sum(weight0.values()) for s, w in weight0.items()}
    records = []
    distributions = [{s: str(v) for s, v in p.items()}]
    activities = []
    for k, q in enumerate(qs[1:]):
        new, act, pi, edges_record = evolve(p, q)
        assert min(new.values()) > 0
        records.append({'k': k, 'q': str(q), 'activity': str(act),
                        'neighborhood_passivity': {s: str(v) for s, v in pi.items()},
                        'edge_fluxes': edges_record})
        activities.append(act)
        p = new
        distributions.append({s: str(v) for s, v in p.items()})
    assert activities[1] > R(63, 125)
    assert sum(activities) / 2 > R(251, 500)

    # Independent analytic three-class lumped equations, including intra-C jumps in activity.
    r, s = R(10000, 10001), R(10000, 10001) ** 64
    z0 = 3 + 4 * r + 4 * s
    initial = [1 / z0, r / z0, s / z0]
    h = R(33, 65)
    ell = R(33) ** 63 / (R(33) ** 63 + R(32) ** 63)
    jab = (h * initial[1] - (1 - h) * initial[0]) / 4
    jbc = (ell * initial[2] - (1 - ell) * initial[1]) / 4
    class_p1 = [initial[0] + 4 * jab, initial[1] - 3 * jab + jbc, initial[2] - jbc]
    assert all(class_p1[i] == R(distributions[1][name]) for i, name in enumerate(['a0', 'b0', 'c0']))
    rho = R(1, 1 + 64 ** 63)
    rates1 = [R(1, 65), R(48, 65) + rho / 4, R(5, 8) - rho / 4]
    lumped_activity1 = sum(m * prob * rate for m, prob, rate in zip([3, 4, 4], class_p1, rates1))
    assert lumped_activity1 == activities[1]

    def enclosure(x, digits=12):
        denominator = 10 ** digits
        lo = int(x * denominator)
        assert R(lo, denominator) <= x < R(lo + 1, denominator)
        return {'lower_numerator': lo, 'upper_numerator': lo + 1, 'denominator': denominator}

    result = {'method': 'SymPy Rational; complementary detailed-balance acceptance from Gibbs weights, synchronous undirected edge flux; reversed labeled basis.',
              'started_at': started, 'finished_at': datetime.now(timezone.utc).isoformat(),
              'labels': labels, 'mapping_to_a': mapping, 'edges': edges,
              'energies': energies, 'q_protocol': list(map(str, qs)), 'row_kernels': row_kernels,
              'distributions': distributions, 'steps': records, 'activities': list(map(str, activities)),
              'mean_activity': str(sum(activities) / 2),
              'lumped_equations': {'initial_per_vertex': list(map(str, initial)),
                                   'AB_flux_per_edge': str(jab), 'BC_flux_per_edge': str(jbc),
                                   'p1_per_vertex': list(map(str, class_p1)),
                                   'next_bath_escape_per_vertex': list(map(str, rates1)),
                                   'A1': str(lumped_activity1)},
              'rational_enclosures': {'A0': enclosure(activities[0]), 'A1': enclosure(activities[1]),
                                      'mean': enclosure(sum(activities) / 2),
                                      'p1_A': enclosure(class_p1[0]), 'p1_B': enclosure(class_p1[1]),
                                      'p1_C': enclosure(class_p1[2])},
              'elapsed_seconds': time.perf_counter() - begin,
              'peak_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'independence': 'Same worker; literal graph/parameter transcription from frozen witness, no A code or data read. Distinct arithmetic, basis, flux representation and lumped analytic check. Not a fresh referee.'}
    (ROOT / 'evidence/layered-exact-b.json').write_text(json.dumps(result, indent=2) + '\n')
    log = ['Independent edge reconstruction B; all arithmetic SymPy Rational.',
           '22 labeled edges, every vertex degree four PASS',
           'Three baths x eleven unit-impulse distributions: synchronous edge conservation, positivity, source Eq.(40) and activity=1-stay PASS',
           'Stationarity at all three baths PASS',
           'Two-step trajectory; all edge fluxes retained, normalization and exact Eq.(40) PASS',
           'Three-class analytic reduction equals full edge trajectory exactly PASS',
           'A1 > 63/125 and mean > 251/500, exact rational comparison PASS',
           'Decimal interval endpoints below are rationals with denominator 10^12, not floating tolerances:',
           json.dumps(result['rational_enclosures']),
           f'elapsed_seconds={result["elapsed_seconds"]:.6f}; peak_rss_bytes_macos={result["peak_rss_bytes_macos"]}',
           'B did not read A. Same worker; independent implementation, not an independent referee.']
    (ROOT / 'evidence/layered-exact-b.log').write_text('\n'.join(log) + '\n')
    print('\n'.join(log))


if __name__ == '__main__':
    main()
