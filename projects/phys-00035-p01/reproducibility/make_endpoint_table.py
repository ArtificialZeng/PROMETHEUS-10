#!/usr/bin/env python3
"""Round saved exact anchor enclosures outward; no floating-point rounding."""
import argparse
from fractions import Fraction
import json
from pathlib import Path


def fixed(value, up=False, digits=12):
    value = Fraction(value)
    scale = 10**digits
    a = value.numerator*scale
    n = -(-a//value.denominator) if up else a//value.denominator
    return str(n//scale)+'.'+str(n % scale).zfill(digits)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='reproducibility/endpoint-certificate.json')
    p.add_argument('--output', default='manuscript/endpoint-anchors.tex')
    args = p.parse_args()
    d = json.loads(Path(args.input).read_text())
    lines = [r'\begin{tabular}{@{}cccc@{}}', r'\toprule',
             r'$\theta$ & $\eta$ & Complete root counts $(N=2,3)$ & $\Delta/\eta$ enclosure\\',
             r'\midrule']
    for a in d['anchors']:
        counts = tuple(c['complete_root_count'] for c in a['root_checks'])
        assert counts == (7, 11)
        theta = r'1/2' if a['theta'] == '1/2' else '2'
        eta = '1/200' if a['eta'] == '1/200' else '1/50'
        lo, hi = a['gap_ratio_interval']
        lines.append('$'+theta+'$ & $'+eta+'$ & $(7,11)$ & $['+fixed(lo)+', '+fixed(hi, True)+r']$\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('\n'.join(lines)+'\n')
    print('Generated outward rational anchor table:', output)


if __name__ == '__main__':
    main()
