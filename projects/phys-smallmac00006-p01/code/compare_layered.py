"""Compare already-completed independent witness representations and sign bounds."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
a = json.loads((ROOT / 'evidence/layered-exact-a.json').read_text())
b = json.loads((ROOT / 'evidence/layered-exact-b.json').read_text())
labels = b['labels']
mapping = b['mapping_to_a']
assert sorted(mapping.values()) == list(range(11))
assert sorted(tuple(sorted((mapping[i], mapping[j]))) for i, j in b['edges']) == [tuple(e) for e in a['edges']]
assert all(a['energies'][mapping[s]] == b['energies'][s] for s in labels)
assert a['q_protocol'] == b['q_protocol']
entries = 0
for t in range(3):
    for i, target in enumerate(labels):
        for j, source in enumerate(labels):
            assert F(a['kernels'][t][mapping[target]][mapping[source]]) == F(b['row_kernels'][t][j][i])
            entries += 1
for k in range(3):
    for s in labels:
        assert F(a['distributions'][k][mapping[s]]) == F(b['distributions'][k][s])
for k in range(2):
    assert F(a['activities'][k]) == F(b['activities'][k])
    pi_sum = sum(map(F, b['steps'][k]['neighborhood_passivity'].values()))
    assert F(a['activities'][k]) == F(1, 2) - pi_sum / 16
assert F(a['mean_activity']) == F(b['mean_activity'])
assert F(a['activities'][1]) > F(63, 125)
assert F(a['mean_activity']) > F(251, 500)
for name, value in [('A0', F(a['activities'][0])), ('A1', F(a['activities'][1])), ('mean', F(a['mean_activity']))]:
    enc = b['rational_enclosures'][name]
    assert F(enc['lower_numerator'], enc['denominator']) <= value < F(enc['upper_numerator'], enc['denominator'])

# Bound used for the explicit optional energy-perturbation robustness corollary.
# |delta(E_i/epsilon)| <= 1/1000; beta_k epsilon unchanged.
# beta0<1/10000, beta1<1/32, beta2<21/5; Gibbs L1 change <1/4000000.
delta = F(1, 1000)
initial_bound = F(1, 4000000)
step_bound = initial_bound + F(1, 32) * delta + F(21, 5) * delta / 2
mean_bound = initial_bound + 3 * F(1, 32) * delta / 4 + F(21, 5) * delta / 4
assert F(63, 125) - step_bound > F(1, 2)
assert F(251, 500) - mean_bound > F(1, 2)

record = {'checked_at': datetime.now(timezone.utc).isoformat(), 'result': 'pass',
          'matrix_entries_compared': entries, 'distributions_compared': 3, 'probability_entries_compared': 33,
          'activities_compared': 2, 'mean_compared': True, 'tolerance': 'exact equality; zero',
          'convention': 'A column kernel equals permuted transpose of B row kernel. B starts from literal label/energy/temperature transcription and reads no A generated data.',
          'rational_activity_enclosures': {k: b['rational_enclosures'][k] for k in ['A0', 'A1', 'mean']},
          'robustness_arithmetic': {'delta_energy_dimensionless': str(delta), 'A1_change_upper_bound': str(step_bound),
                                    'mean_change_upper_bound': str(mean_bound),
                                    'A1_lower_bound': str(F(63, 125) - step_bound),
                                    'mean_lower_bound': str(F(251, 500) - mean_bound)},
          'files_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in
                           ['code/layered_exact_a.py', 'code/layered_exact_b.py', 'evidence/layered-witness-spec.json',
                            'evidence/layered-exact-a.json', 'evidence/layered-exact-b.json']},
          'limitation': 'Same-worker implementation comparison. Scientific acceptance requires the assigned fresh referee.'}
(ROOT / 'evidence/layered-comparison.json').write_text(json.dumps(record, indent=2) + '\n')
log = ['Comparison of independently completed A and B',
       'Labeled graph, degrees, energies and temperatures agree exactly after explicit permutation PASS',
       f'All {entries} kernel entries agree under permutation and transpose PASS',
       'All 33 probabilities, both activities, mean and source Eq.(40) agree exactly PASS',
       'A1 > 63/125 > 1/2; mean > 251/500 > 1/2 PASS',
       'All rational enclosures independently checked by cross multiplication PASS',
       'Perturbation-error rational arithmetic PASS (analytic Lipschitz proof is in layered-proof.md)',
       json.dumps(record['robustness_arithmetic']),
       'Exact finite-domain witness; no precision error or asymptotic substitution. No referee acceptance claimed.']
(ROOT / 'evidence/layered-comparison.log').write_text('\n'.join(log) + '\n')
print('\n'.join(log))
