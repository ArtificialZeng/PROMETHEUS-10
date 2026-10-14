#!/usr/bin/env python3
"""Exact Eq.(4) verification of a fixed-parity flagged resource family.

Independent of the replica-rotation calculation: enumerate all even local
Hermitian Majorana strings, then contract the exact four-index kernels.
The global state has even parity in every block, so odd local strings vanish.
No global string truncation, fit, stochastic estimate, or dense N=34 vector.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
A = (2 + sp.sqrt(2)) / 4  # cos(pi/8)^2
B = (2 - sp.sqrt(2)) / 4  # sin(pi/8)^2


def majorana_action(n, label, column):
    """Column action of Z-prefix X/Y, with first mode the high Fock bit."""
    mode, y = divmod(label, 2)
    bit = 1 << (n - 1 - mode)
    occupied = bool(column & bit)
    prefix = column >> (n - mode)
    phase = (-1) ** prefix.bit_count()
    if y:
        phase *= sp.I * (-1 if occupied else 1)
    return column ^ bit, phase


def string_element(n, subset, row, column):
    phase = sp.I ** (len(subset) * (len(subset) - 1) // 2)
    destination = column
    for label in reversed(subset):
        destination, factor = majorana_action(n, label, destination)
        phase *= factor
    return phase if destination == row else sp.S.Zero


def local_kernel(n, vectors, c2=A, s2=B):
    keys = list(itertools.product(range(2), repeat=4))
    kernel = dict.fromkeys(keys, sp.S.Zero)
    for length in range(0, 2 * n + 1, 2):
        weight = c2 ** (n - length // 2) * s2 ** (length // 2)
        for subset in itertools.combinations(range(2 * n), length):
            matrix = {}
            for a, b in itertools.product(range(2), repeat=2):
                matrix[a, b] = sum(
                    sp.conjugate(ar) * bc * string_element(n, subset, r, c)
                    for r, ar in vectors[a].items()
                    for c, bc in vectors[b].items()
                )
            for a, b, c, d in keys:
                kernel[a, b, c, d] += (
                    weight * matrix[a, b] * sp.conjugate(matrix[c, d])
                )
    return {key: sp.simplify(value) for key, value in kernel.items()}


def contract(flags, block, m, probability):
    amplitudes = [sp.sqrt(1 - probability), sp.sqrt(probability)]
    return sp.simplify(sum(
        sp.conjugate(amplitudes[a]) * amplitudes[b]
        * amplitudes[c] * sp.conjugate(amplitudes[d])
        * flags[a, b, c, d] * block[a, b, c, d] ** m
        for a, b, c, d in flags
    ))


def main():
    flags = local_kernel(2, [{0: sp.S.One}, {3: sp.S.One}])
    block = local_kernel(4, [
        {0: sp.S.One},
        {0: 1 / sp.sqrt(2), 15: 1 / sp.sqrt(2)},
    ])
    assert flags[0, 0, 0, 0] == flags[1, 1, 1, 1] == 1
    assert block[0, 0, 0, 0] == 1
    assert block[1, 1, 1, 1] == sp.Rational(3, 4)
    # These kernel values are obtained from the complete local string sums.
    assert flags[0, 0, 1, 1] == flags[1, 1, 0, 0] == sp.Rational(1, 2)
    # Independent symbolic all-angle check of the SIX entries that survive
    # the flag contraction. Here z=cos(alpha/2)^2, t=sin(alpha)^2.
    z=sp.symbols('z', real=True)
    t=4*z*(1-z)
    flags_symbolic=local_kernel(2,[{0:sp.S.One},{3:sp.S.One}],z,1-z)
    block_symbolic=local_kernel(4,[
        {0:sp.S.One},{0:1/sp.sqrt(2),15:1/sp.sqrt(2)}],z,1-z)
    targets={
        (0,0,0,0):(sp.S.One,sp.S.One),
        (1,1,1,1):(sp.S.One,1-t*(1-t)),
        (0,0,1,1):(1-t,(1+(1-t)**2)/2),
        (1,1,0,0):(1-t,(1+(1-t)**2)/2),
        (0,1,0,1):(t,(1+t**2)/2),
        (1,0,1,0):(t,(1+t**2)/2),
    }
    for key,value in flags_symbolic.items():
        if key not in targets:
            assert value == 0
        else:
            flag_target,block_target=targets[key]
            assert sp.simplify(value-flag_target)==0
            assert sp.simplify(block_symbolic[key]-block_target)==0
    records = []
    # A symbolic coefficient extraction avoids assumptions about sqrt(1-q).
    # Every nonzero flag entry has an even count of each global branch label.
    for key, value in flags.items():
        if sum(key) % 2:
            assert value == 0
    for m in range(1, 10):
        for q in (sp.Rational(1, 4), sp.Rational(1, 20)):
            measured = contract(flags, block, m, q)
            expected = (1-q)**2 + q**2 * sp.Rational(3, 4)**m \
                + 2*q*(1-q)*sp.Rational(5, 8)**m
            assert sp.simplify(measured - expected) == 0
            records.append({
                'm': m, 'N': 4*m+2, 'q': str(q),
                'F_from_exact_strings': str(measured),
                'formula_difference': '0',
            })
    # Main finite counterexample: m=8, q=1/4, N=34.
    m, q = 8, sp.Rational(1, 4)
    parent = contract(flags, block, m, q)
    branch = sp.Rational(3, 4)**m
    ratio = sp.factor(parent / sp.Rational(3, 4)**(m*q))
    assert ratio.is_Rational and ratio > 1
    delta = sp.log(ratio)
    # Simple rigorous enclosure: for x>0, x/(1+x)<log(1+x)<x.
    x = ratio - 1
    lower, upper = x/(1+x), x
    assert 0 < lower < upper
    result = {
        'method': 'complete local even Hermitian-Majorana string kernels; exact symbolic contraction',
        'arithmetic': 'SymPy exact rationals, Gaussian integers and radicals; no tolerance',
        'block_factorization': 'Each of the 2-mode flag and m four-mode blocks has even local parity; all odd local strings vanish exactly.',
        'flag_kernel': {''.join(map(str,k)): str(v) for k,v in flags.items()},
        'resource_kernel': {''.join(map(str,k)): str(v) for k,v in block.items()},
        'all_angle_symbolic_check': {
            'variable': 'z=cos(alpha/2)^2; t=4z(1-z)=sin(alpha)^2',
            'flag_nonzero_entries': {''.join(map(str,k)):str(v) for k,v in flags_symbolic.items() if v!=0},
            'resource_entries_at_flag_nonzero': {''.join(map(str,k)):str(block_symbolic[k]) for k in targets},
            'result': 'Every surviving kernel equals the claimed polynomial identically; hence the all-m all-angle contraction formula follows algebraically.',
        },
        'formula_checks': records,
        'witness': {
            'N': 34, 'm': 8, 'q': '1/4', 'p': '3/4',
            'state': 'sqrt(3)/2 |00> |0000>^tensor8 + 1/2 |11> [(|0000>+|1111>)/sqrt(2)]^tensor8',
            'measurement': 'first Fock mode occupation; retain outcomes 0 and 1',
            'branch_F': ['1', str(branch)],
            'F_parent': str(parent),
            'exp_Delta': str(ratio),
            'Delta': str(delta),
            'Delta_decimal_diagnostic': str(sp.N(delta, 40)),
            'strict_log_bounds': {'lower': str(lower), 'upper': str(upper)},
            'integer_certificate': {'numerator': str(sp.numer(ratio)), 'denominator': str(sp.denom(ratio)), 'comparison': 'numerator > denominator > 0'},
        },
        'limitations': 'This is proposer-side exact verification, not fresh referee acceptance. N=34 is an explicit witness, not a minimal-dimension assertion.',
    }
    path = ROOT / 'evidence/flagged-twist-exact.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    lines = [
        'Exact local Eq.(4) kernel verification; all assertions passed.',
        'All-angle symbolic kernel identities passed as polynomials in z=cos(alpha/2)^2.',
        '18 exact family comparisons: m=1..9, q=1/4 and 1/20.',
        f'N=34 input F={parent}; branches F=1,{branch}; p=3/4,1/4.',
        f'exp(Delta)={ratio} > 1; Delta~{sp.N(delta, 24)}.',
        f'Rigorous rational log enclosure: {lower} < Delta < {upper}.',
        'No stochastic or numerical criterion used for the strict violation.',
        'No independent-referee verdict is asserted.',
    ]
    (ROOT / 'evidence/flagged-twist-exact.log').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
