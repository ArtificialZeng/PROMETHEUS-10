#!/usr/bin/env python3
"""Export displayed inputs and one comparison table from the retained data.

No root finding or propagation is performed. The exact witness is the enclosed
zero, not these displayed couplings or the decimal box center.
"""
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scientific(value, places=5):
    mantissa, exponent = format(Decimal(value), f'.{places}E').split('E')
    return rf'${mantissa}\times10^{{{int(exponent)}}}$'


def main():
    cert = json.loads((ROOT / 'evidence/research-root-certificate.json').read_text())
    center = cert['center_exact_decimal']
    lines = [r'\begin{equation}', r'\begin{aligned}']
    for index, (name, value) in enumerate(zip(('v_0', 'c_0', 'd_0'), center)):
        suffix = r'\\' if index < 2 else ''
        lines.append(rf'{name}&=\texttt{{{value}}}{suffix}')
    lines.extend([r'\end{aligned}', r'\label{eq:center}', r'\end{equation}'])
    (ROOT / 'manuscript/certificate-center.tex').write_text('\n'.join(lines) + '\n')
    lines = [r'\begingroup\small', r'\begin{verbatim}']
    for j, row in enumerate(cert['preconditioner_exact_decimal'], 1):
        for k, value in enumerate(row, 1):
            lines.append(f'Y{j}{k} = {value}')
    lines.extend([r'\end{verbatim}', r'\endgroup'])
    (ROOT / 'manuscript/certificate-preconditioner.tex').write_text('\n'.join(lines) + '\n')
    data = json.loads((ROOT / 'evidence/research-independent-replay.json').read_text())
    point = next(p for p in data['points'] if p['phase_index_k'] == 100)
    rows = []
    for name, prefix in [('Fixed-spectrum reference', 'reference'), ('Certified-root design', 'candidate')]:
        error = scientific(point[f'{prefix}_abs_error'])
        success = scientific(point[f'{prefix}_success_probability_scalar'])
        cost = format(Decimal(point[f'{prefix}_norm_H_times_t_scalar']), '.5f')
        rows.append(f'{name} & {error} & {success} & ${cost}$ ' + r'\\')
    table = [r'\begin{table}[htbp]', r'\centering', r'\small',
             r'\begin{tabular}{lccc}', r'\toprule',
             r'Design & $|a_4-\mathrm{i}\ell x|$ & $|a_4|^2$ & $\|T_4\|\tau$ \\',
             r'\midrule', *rows, r'\bottomrule', r'\end{tabular}',
             r'\caption{Complete scalar-channel propagation at $x=4/401$ and $\tau=2\pi$.',
             r'The fixed-spectrum reference is reconstructed from the $R=4$ design in',
             r'Kay and Tamon, \emph{Matrix Inversion by Quantum Walk}',
             r'(arXiv:2508.06611v1), Table~I. Each error is measured relative to that',
             r"design's own linear coefficient. Displayed digits are numerical diagnostics;",
             r'the uniform bound follows from the root certificate and analytic estimates.}',
             r'\label{tab:comparison}', r'\end{table}']
    (ROOT / 'manuscript/comparison-table.tex').write_text('\n'.join(table) + '\n')
    print(json.dumps({'exported': ['manuscript/certificate-center.tex',
                                   'manuscript/certificate-preconditioner.tex',
                                   'manuscript/comparison-table.tex'],
                      'data_source': 'evidence/research-independent-replay.json',
                      'phase_index_k': point['phase_index_k'],
                      'certificate_source': 'evidence/research-root-certificate.json'}))


if __name__ == '__main__':
    main()
