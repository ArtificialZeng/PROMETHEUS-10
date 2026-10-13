"""Regenerate the manuscript table from saved interval-evaluated points.

No optimization or branch extension is performed. The printed rounding is checked
against the saved interval, while the analytic reference is evaluated exactly.
"""
import json
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
records = json.loads((ROOT / 'data/table-points.json').read_text())['records']
lines = [r'\begin{table}[t]',
         r'\caption{Variance at three prescribed means. The reference values are exact for Eq.~\eqref{eq:baseline}; branch values are rounded to six decimal places from the saved interval evaluations. The last column gives the branch cost. The smaller variance of the larger ansatz is a known numerical feature; the present contribution is the full-domain local certificate.}',
         r'\label{tab:values}', r'\begin{ruledtabular}', r'\begin{tabular}{rccc}',
         r'$m$ & Reference $\sigma^2$ & Branch $\sigma^2$ & Branch $\CF$\\']
rounding_checks = []
with localcontext() as ctx:
    ctx.prec = 70
    for rec in records:
        m = Fraction(rec['mean'])
        assert m.denominator == 1
        n = m.numerator
        value, radius = rec['cost_enclosure'].strip('[]').split(' +/- ')
        center, radius = Decimal(value), Decimal(radius)
        assert abs(Decimal(rec['CF2']) - center) <= radius
        variance = (center + Decimal(n * (n - 2))) / 2
        rounded_variance = variance.quantize(Decimal('0.000001'))
        rounded_cost = center.quantize(Decimal('0.000001'))
        assert abs(rounded_variance - variance) + radius / 2 < Decimal('0.0000005')
        assert abs(rounded_cost - center) + radius < Decimal('0.0000005')
        ref_cost = -Fraction(n * n * (n - 2)**2, 2 * (n - 1)**2)
        ref_var = (ref_cost + n * (n - 2)) / 2
        ref_tex = r'$%d/%d$' % (ref_var.numerator, ref_var.denominator)
        lines.append(f'{n} & {ref_tex} & ${rounded_variance}$ & ${rounded_cost}$' + r'\\')
        rounding_checks.append({'mean': n, 'reference_variance': str(ref_var),
                                'branch_variance_printed': str(rounded_variance),
                                'branch_cost_printed': str(rounded_cost),
                                'rounding_enclosure_checked': True})
lines += [r'\end{tabular}', r'\end{ruledtabular}', r'\end{table}']
(PROJECT / 'manuscript/values.tex').write_text('\n'.join(lines) + '\n')
(ROOT / 'results').mkdir(exist_ok=True)
(ROOT / 'results/table-check.json').write_text(json.dumps(rounding_checks, indent=2) + '\n')
print(json.dumps(rounding_checks))
