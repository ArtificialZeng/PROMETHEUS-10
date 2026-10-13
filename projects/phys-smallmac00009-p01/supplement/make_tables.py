#!/usr/bin/env python3
"""Render the complete rational witness as LaTeX tables; standard library only.

Run from any directory. Output is manuscript/tables/, relative to this package.
This is presentation generation, not an independent scientific verifier.
"""
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = json.loads((ROOT / 'supplement/certificate.json').read_text())
OUT = ROOT / 'manuscript/tables'
OUT.mkdir(parents=True, exist_ok=True)
EDGES = [(i, j) for i in range(4) for j in range(4) if i != j]
trees = []
for root in range(4):
    nodes = [j for j in range(4) if j != root]
    valid = []
    for parents in product(*[[i for i in range(4) if i != j] for j in nodes]):
        parent = dict(zip(nodes, parents))
        good = True
        for start in nodes:
            seen, v = set(), start
            while v != root:
                if v in seen:
                    good = False
                    break
                seen.add(v)
                v = parent[v]
            if not good:
                break
        if good:
            valid.append(tuple(sorted(EDGES.index((parent[j], j)) for j in nodes)))
    trees.append(sorted(valid))
assert list(map(len, trees)) == [16] * 4
lines = [r'\begin{tabular}{rcccc}', r'\toprule',
         r'$t$ & Root $0$ & Root $1$ & Root $2$ & Root $3$ \\', r'\midrule']
for t in range(16):
    cols = [str(t)] + ['$' + ','.join(map(str, trees[r][t])) + '$' for r in range(4)]
    lines.append(' & '.join(cols) + r' \\')
lines += [r'\bottomrule', r'\end{tabular}']
(OUT / 'trees.tex').write_text('\n'.join(lines) + '\n')
names = [r's_{01}', r's_{02}', r's_{03}', r's_{12}', r's_{13}', r's_{23}', 'A', 'B', 'C']
lines = [r'\begingroup', r'\small', r'\setlength{\tabcolsep}{10pt}',
         r'\begin{longtable}{lrrl}',
         r'\caption{Complete coefficient witness. Every listed family receives weight $1/c_m$; unlisted families receive zero. IDs use Eq.~\eqref{eq:family-id}.}\label{tab:witness}\\',
         r'\toprule $x^m$ & $c_m$ & Family IDs & Each weight \\ \midrule',
         r'\endfirsthead',
         r'\multicolumn{4}{c}{Table \thetable\ continued}\\',
         r'\toprule $x^m$ & $c_m$ & Family IDs & Each weight \\ \midrule',
         r'\endhead', r'\midrule\multicolumn{4}{r}{Continued on next page}\\',
         r'\endfoot', r'\bottomrule', r'\endlastfoot']
assert len(CERT['records']) == 93
for record in CERT['records']:
    c = record['coefficient']
    ids = record['unique_family_ids']
    assert len(ids) == c
    assert record['weights'] == [('1' if c == 1 else '1/' + str(c))] * c
    mon = r'\,'.join(name + ('^{' + str(power) + '}' if power != 1 else '')
                     for name, power in zip(names, record['monomial']) if power)
    weight = '1' if c == 1 else r'1/' + str(c)
    lines.append('$' + mon + '$ & ' + str(c) + ' & ' + ', '.join(map(str, ids))
                 + ' & $' + weight + '$' + r' \\')
lines += [r'\end{longtable}', r'\endgroup']
(OUT / 'witness.tex').write_text('\n'.join(lines) + '\n')
print('Generated 16-row rooted-tree table and complete 93-row coefficient table.')
