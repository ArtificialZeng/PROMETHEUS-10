"""Exact reproduction of two published finite-sector spectral baselines."""
import json
from datetime import datetime, timezone
from math import comb
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
lam = s.symbols('lambda')


def rational_matrix(data):
    return s.Matrix([[s.Rational(v) for v in row] for row in data])


if __name__ == '__main__':
    with (HERE / 'baseline.log').open('w') as log:
        def record(message):
            print(message)
            log.write(message + '\n')
            log.flush()
        record('UTC ' + datetime.now(timezone.utc).isoformat())
        record('Command: python3 evidence/reproduce_baseline.py')
        record('SymPy ' + s.__version__ + '; exact rational characteristic polynomials and real-root isolation.')
        # Independently derived graph Laplacian, not the k=1 input cache.
        path = s.Matrix([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
        for eigenvalue, vector in [(0, [1, 1, 1]), (1, [1, 0, -1]), (3, [1, -2, 1])]:
            v = s.Matrix(vector)
            assert path * v == eigenvalue * v
        expected_rw = s.Poly(lam * (lam - 1) * (lam - 3), lam)
        assert path.charpoly(lam).as_poly() == expected_rw
        record('Independent one-particle path Laplacian: eigenpairs (0,[1,1,1]), (1,[1,0,-1]), (3,[1,-2,1]); gap=1 inverse-time.')
        a = {v['id']: v for v in json.loads((HERE / 'input-a.json').read_text())['cases']}
        b = {v['id']: v for v in json.loads((HERE / 'input-b.json').read_text())['cases']}
        results = []
        for name, aa in a.items():
            if aa['family'] == 'weighted4-input-diagnostic':
                continue
            bb = b[name]
            negative_a = -rational_matrix(aa['L_backward'])
            kb = rational_matrix(bb['K_incidence'])
            mb = s.diag(*[s.Rational(v) for v in bb['mu']])
            negative_b = mb.inv() * kb
            polynomial = negative_a.charpoly(lam).as_poly()
            other = negative_b.charpoly(lam).as_poly()
            assert polynomial == other
            assert negative_a.rank() == negative_a.rows - 1
            entry = {'id': name, 'dimension': negative_a.rows,
                     'characteristic_polynomial': str(polynomial.as_expr()),
                     'factorization': str(s.factor(polynomial.as_expr()))}
            if aa['family'] == 'path3-unit-logconcave':
                intervals = polynomial.intervals(eps=s.Rational(1, 10**12))
                assert sum(m for interval, m in intervals) == negative_a.rows
                zero = [(iv, mult) for iv, mult in intervals if iv == (s.Rational(0), s.Rational(0))]
                assert len(zero) == 1 and zero[0][1] == 1
                positive = [(iv, mult) for iv, mult in intervals if iv[1] > 0]
                assert positive[0] == ((s.Rational(1), s.Rational(1)), 1)
                assert all(iv[0] >= 1 for iv, mult in positive)
                if aa['k'] == 1:
                    assert polynomial == expected_rw
                    # Convert A occupancy order to the independent site order.
                    sites = [aa['state_order'].index([int(x == y) for x in range(3)]) for y in range(3)]
                    assert negative_a.extract(sites, sites) == path
                record(name + ': charpoly=' + entry['factorization'])
                record(name + ': exact rational real-root intervals=' + str(intervals))
                record(name + ': PASS gap=1, simple zero; independent A/B polynomials identical; all other roots >=1. Published Eq. (1.2) reproduced at this k.')
                entry.update({'gap': '1', 'isolating_intervals': [{'bounds': list(map(str, iv)), 'multiplicity': m} for iv, m in intervals],
                              'published_reference': 'Kim-Sau journal Eq. (1.2), Eq. (2.7)', 'status': 'pass'})
            else:
                total = sum(s.Rational(v) for v in aa['alpha'])
                assert total == s.Rational(23, 12)
                expected = s.Integer(1)
                eigenvalues = []
                for degree in range(aa['k'] + 1):
                    value = degree * (total + degree - 1)
                    multiplicity = 1 if degree == 0 else comb(aa['n'] + degree - 2, degree)
                    expected *= (lam - value) ** multiplicity
                    eigenvalues.append({'degree': degree, 'value': str(value), 'multiplicity': multiplicity})
                assert polynomial == s.Poly(s.expand(expected), lam)
                record(name + ': charpoly=' + entry['factorization'])
                record(name + ': PASS expected spectrum=' + str(eigenvalues) + '; gap=23/12 inverse-time. Published Proposition 3.1 spectrum reproduced.')
                entry.update({'gap': '23/12', 'eigenvalues': eigenvalues,
                              'published_reference': 'Kim-Sau journal Eqs. (3.5), (3.8), Proposition 3.1/Eq. (3.9)', 'status': 'pass'})
            results.append(entry)
        assert len(results) == 6
        (HERE / 'baseline-results.json').write_text(json.dumps({
            'status': 'pass', 'mode': 'exact', 'baselines': results,
            'error_control': 'Exact rational coefficients, exact characteristic-polynomial equality, rational real-root isolation (width at most 1e-12 for irrational roots); no floating-point spectral ordering.',
            'scope': 'Six finite published baseline instances only; original arbitrary graph/alpha/k conjecture remains unresolved.'}, indent=2) + '\n')
        record('TOTAL PASS: 6 exact published baseline instances; no new scientific contribution or referee acceptance.')
