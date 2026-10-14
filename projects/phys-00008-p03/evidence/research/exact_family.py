"""Exact independent tangent-generator representation of a known n=4 QLS family.

Uses SymPy rational functions, no SVD, no numerical Jacobian or cached spectrum.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import time
import sympy as sp

OUT = Path(__file__).resolve().parent
t = sp.Symbol('t', real=True)
z = sp.Symbol('z')
c = (1 - t ** 2) / (1 + t ** 2)
s = 2 * t / (1 + t ** 2)


def reduce_matrix(m):
    return m.applyfunc(sp.cancel)


def family():
    e = [sp.eye(4)[:, j] for j in range(4)]
    u, v = c * e[0] + s * e[1], -s * e[0] + c * e[1]
    return [[e[0], e[1], e[2], e[3]], [e[1], e[0], e[3], e[2]],
            [e[2], e[3], u, v], [e[3], e[2], v, u]]


def tangent_representation(q, imaginary):
    rows = [sp.Matrix.hstack(*q[i]) for i in range(4)]
    cols = [sp.Matrix.hstack(*[q[i][j] for i in range(4)]) for j in range(4)]
    pairs = [(a, b) for a in range(4) for b in range(a if imaginary else a + 1, 4)]
    labels = [(j, a, b) for j in range(4) for a, b in pairs]
    matrix = sp.zeros(len(labels))
    sign = 1 if imaginary else -1
    for k, (j, a, b) in enumerate(labels):
        generator = sp.zeros(4)
        generator[a, b] = 1
        if a != b:
            generator[b, a] = sign
        col = cols[j] * generator
        delta = [[sp.zeros(4, 1) for _ in range(4)] for _ in range(4)]
        for i in range(4):
            delta[i][j] = col[:, i]
        after_rows = []
        for i in range(4):
            e = sp.Matrix.hstack(*delta[i])
            after_rows.append(reduce_matrix((e + sign * rows[i] * e.T * rows[i]) / 2))
        after_cols = []
        for jj in range(4):
            e = sp.Matrix.hstack(*[after_rows[i][:, jj] for i in range(4)])
            p = reduce_matrix((e + sign * cols[jj] * e.T * cols[jj]) / 2)
            after_cols.append(reduce_matrix(cols[jj].T * p))
        for kk, (jj, aa, bb) in enumerate(labels):
            matrix[kk, k] = sp.cancel(after_cols[jj][aa, bb])
    return matrix, labels


def connected_blocks(m):
    unseen = set(range(m.rows))
    blocks = []
    while unseen:
        pending = [min(unseen)]
        found = set()
        while pending:
            i = pending.pop()
            if i in found:
                continue
            found.add(i)
            for j in unseen:
                if (m[i, j] != 0 or m[j, i] != 0) and j not in found:
                    pending.append(j)
        unseen -= found
        ids = sorted(found)
        blocks.append((ids, m.extract(ids, ids)))
    return blocks


def main():
    start = time.monotonic()
    q = family()
    rows = [sp.Matrix.hstack(*q[i]) for i in range(4)]
    cols = [sp.Matrix.hstack(*[q[i][j] for i in range(4)]) for j in range(4)]
    assert all(reduce_matrix(a.T * a - sp.eye(4)) == sp.zeros(4) for a in rows + cols)
    record = {'started_at': datetime.now(timezone.utc).isoformat(), 'sympy': sp.__version__,
              'parameter': 't=tan(theta/2), c=(1-t^2)/(1+t^2), s=2t/(1+t^2)',
              'QLS_row_column_orthogonality': 'exact identity for all real t', 'parts': []}
    products = []
    for imaginary in (False, True):
        matrix, labels = tangent_representation(q, imaginary)
        blocks = connected_blocks(matrix)
        part = {'sector': 'imaginary symmetric generators' if imaginary else 'real skew generators',
                'dimension': matrix.rows, 'blocks': []}
        product = sp.Integer(1)
        for ids, block in blocks:
            polynomial = sp.factor(block.charpoly(z).as_expr())
            product *= polynomial
            part['blocks'].append({'indices': ids, 'generator_labels': [labels[i] for i in ids],
                                   'matrix': [[str(block[i, j]) for j in range(block.cols)] for i in range(block.rows)],
                                   'characteristic_polynomial': str(polynomial)})
        product = sp.factor(product)
        part['characteristic_polynomial'] = str(product)
        products.append(product)
        record['parts'].append(part)
        print(json.dumps({'sector': part['sector'], 'dimension': matrix.rows,
                          'block_sizes': [len(ids) for ids, _ in blocks], 'characteristic_polynomial': str(product)}), flush=True)
    combined = sp.factor(products[0] * products[1])
    expected = z ** 16 * (z - 1) ** 32 * (z - 1 / (1 + t ** 2)) ** 8 * (z - t ** 2 / (1 + t ** 2)) ** 8
    difference = sp.cancel(combined - expected)
    assert difference == 0
    record.update({'completed_at': datetime.now(timezone.utc).isoformat(), 'combined_characteristic_polynomial': str(combined),
                   'expected_polynomial': str(sp.factor(expected)), 'exact_difference': str(difference),
                   'runtime_seconds': time.monotonic() - start,
                   'scope': 'Derivative on the column-unitary tangent space only. No nonlinear convergence, basin, almost-sure claim or global classification.'})
    (OUT / 'exact-family-spectrum.json').write_text(json.dumps(record, indent=2) + '\n')
    print('FINAL ' + json.dumps({key: value for key, value in record.items() if key != 'parts'}), flush=True)


if __name__ == '__main__':
    main()
