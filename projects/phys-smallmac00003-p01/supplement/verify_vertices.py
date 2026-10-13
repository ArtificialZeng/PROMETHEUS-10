#!/usr/bin/env python3
"""Exact two-qutrit APPT outer-polytope certificate; Python standard library.

This submission-facing program implements the accepted raw-spectrum active-basis
calculation. It generates every vertex before opening the distributed data file.
The analytic completeness proof is in the manuscript. This repackaging is not a
new independent scientific review. No floating-point feasibility test is used.
"""
from argparse import ArgumentParser
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import platform


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def solve(rows, rhs):
    a = [[F(x) for x in row] + [F(b)] for row, b in zip(rows, rhs)]
    n = len(a)
    for c in range(n):
        p = next((r for r in range(c, n) if a[r][c]), None)
        if p is None:
            return None
        a[c], a[p] = a[p], a[c]
        scale = a[c][c]
        a[c] = [x / scale for x in a[c]]
        for r in range(n):
            if r != c and a[r][c]:
                scale = a[r][c]
                a[r] = [x - scale * y for x, y in zip(a[r], a[c])]
    return tuple(row[-1] for row in a)


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    return sum(((-1) ** j * a[0][j] * determinant(
        [[row[k] for k in range(len(a)) if k != j] for row in a[1:]])
        for j in range(len(a))), F(0))


def lmis(x):
    a, b, c, d, e, f, g, h, i = x
    return ([[2*i, h-a, f-b], [h-a, 2*g, e-c], [f-b, e-c, 2*d]],
            [[2*i, h-a, g-b], [h-a, 2*f, e-c], [g-b, e-c, 2*d]])


def enumerate_vertices():
    rows = []
    for k in range(8):
        row = [0] * 9
        row[k], row[k+1] = 1, -1
        rows.append(row)
    rows.append([0] * 8 + [1])
    rows.extend([[-1,0,0,0,0,0,1,1,1],
                 [-1,-1,-1,1,1,1,1,1,1],
                 [-2,0,0,0,0,0,1,2,4]])
    vertices = set()
    attempts = singular = feasible = 0
    for active in combinations(range(12), 8):
        attempts += 1
        x = solve([[1]*9] + [rows[k] for k in active], [1] + [0]*8)
        if x is None:
            singular += 1
            continue
        if any(dot(row, x) < 0 for row in rows):
            continue
        feasible += 1
        vertices.add(x)
    ordered = sorted(vertices, key=lambda x: (-dot(x, x), x))
    records = []
    groups = {}
    for x in ordered:
        y = tuple((k+1)*(x[k]-(x[k+1] if k < 8 else 0)) for k in range(9))
        assert sum(y) == 1 and min(y) >= 0
        p = dot(x, x)
        assert p == sum((y[k]*y[l]/max(k+1,l+1)
                         for k in range(9) for l in range(9)), F(0))
        assert p <= F(17,121)
        support = [k+1 for k, value in enumerate(y) if value]
        group = groups.setdefault(str(len(support)), {'count': 0, 'maximum': F(0)})
        group['count'] += 1
        group['maximum'] = max(group['maximum'], p)
        records.append({'lambda': list(map(str,x)), 'gap_weights': list(map(str,y)),
                        'positive_support_1based': support,
                        'cut_slacks': [str(dot(row,x)) for row in rows[-3:]],
                        'purity': str(p), 'target_minus_purity': str(F(17,121)-p)})
    star = tuple([F(3,11)] + [F(1,11)]*8)
    assert len(vertices) == 49 and ordered[0] == star
    assert sum(dot(x,x) == F(17,121) for x in vertices) == 1
    assert dot(ordered[1],ordered[1]) == F(5,36)
    minors = []
    for matrix in lmis(star):
        values = [determinant([[matrix[i][j] for j in inds] for i in inds])
                  for size in range(1,4) for inds in combinations(range(3),size)]
        assert min(values) >= 0
        assert values == [F(2,11)]*3 + [F(0),F(4,121),F(4,121),F(0)]
        minors.append(list(map(str,values)))
    for group in groups.values():
        group['maximum'] = str(group['maximum'])
    return {'schema': 'appt-three-cut-vertices-v1', 'arithmetic': 'exact rational',
            'attempted_bases': attempts, 'singular_bases': singular,
            'feasible_bases': feasible, 'vertex_count': len(vertices),
            'maximum_purity': '17/121', 'runner_up': '5/36',
            'positive_support_groups': groups, 'equality_principal_minors': minors,
            'vertices': records}


def table_text(records):
    lines = [r'\begingroup', r'\small', r'\setlength{\tabcolsep}{10pt}',
             r'\begin{longtable}{rll}',
             r'\caption{All 49 vertices of the three-cut outer polytope, in gap weights.}',
             r'\label{tab:vertices}\\', r'\toprule',
             r'No. & Positive gap weights $k:y_k$ & $P$\\', r'\midrule',
             r'\endfirsthead', r'\multicolumn{3}{c}{Table \thetable\ continued}\\',
             r'\toprule', r'No. & Positive gap weights $k:y_k$ & $P$\\',
             r'\midrule', r'\endhead', r'\midrule',
             r'\multicolumn{3}{r}{Continued on next page}\\', r'\endfoot',
             r'\bottomrule', r'\endlastfoot']
    for n, row in enumerate(records, 1):
        weights = r',\; '.join(str(k+1)+':'+value
                              for k,value in enumerate(row['gap_weights']) if F(value))
        lines.append(str(n)+' & $'+weights+'$ & $'+row['purity']+r'$\\')
    lines.extend([r'\end{longtable}', r'\endgroup', ''])
    return '\n'.join(lines)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--compare', type=Path)
    parser.add_argument('--table', type=Path)
    args = parser.parse_args()
    result = enumerate_vertices()
    # No stored vertices are read before the complete calculation above.
    if args.compare:
        expected = json.loads(args.compare.read_text())
        a = {tuple(row['lambda']): row for row in result['vertices']}
        b = {tuple(row['lambda']): row for row in expected['vertices']}
        assert set(a) == set(b), 'Vertex sets differ'
        for key in a:
            for field in ('gap_weights','cut_slacks','purity','target_minus_purity'):
                assert a[key][field] == b[key][field], (key,field)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    if args.table:
        args.table.parent.mkdir(parents=True, exist_ok=True)
        args.table.write_text(table_text(result['vertices']))
    summary = {k:v for k,v in result.items() if k != 'vertices'}
    summary['python_version'] = platform.python_version()
    summary['comparison'] = 'all records agree' if args.compare else 'not requested'
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
