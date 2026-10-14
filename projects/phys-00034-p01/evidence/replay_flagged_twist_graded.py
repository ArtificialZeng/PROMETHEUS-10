#!/usr/bin/env python3
"""Independent full two-register graded-rotation replay at N=6 and N=10.

This file does not import the string checker or its saved answers. It builds
the physical Fock vector, applies every graded replica rotation factor, and
retains both measured outcomes. Floating checks are diagnostics only; the
strict N=34 certificate is exact in verify_flagged_twist_exact.py.
"""

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def state_vector(m, q, phase=1):
    n = 4*m+2
    state = np.zeros(1 << n, dtype=complex)
    state[0] = math.sqrt(1-q)
    for word in range(1 << m):
        index = 3 << (4*m)
        for block in range(m):
            if word & (1 << block):
                index |= 15 << (4*block)
        assert index.bit_count() % 2 == 0
        state[index] = phase*math.sqrt(q/(1 << m))
    assert abs(np.vdot(state,state).real-1) < 2e-15
    return state


def rotation_overlap(state, n, alpha):
    d = 1 << n
    indices = np.arange(d, dtype=np.int64)
    parity = np.array([(-1)**i.bit_count() for i in range(d)])
    doubled = np.kron(state, state)
    rotated = doubled.copy()
    c, s = math.cos(alpha/2), math.sin(alpha/2)
    big_indices = np.arange(d*d, dtype=np.int64)
    for mode in range(n):
        bit = 1 << (n-1-mode)
        prefix_sign = np.array([(-1)**int(i >> (n-mode)).bit_count() for i in indices])
        for kind in ('X','Y'):
            gamma_phase = prefix_sign.astype(complex)
            if kind == 'Y':
                gamma_phase *= 1j*(1-2*((indices & bit) != 0))
            # A_j=(gamma_j Pi) tensor gamma_j, rather than gamma_j tensor gamma_j.
            column_phase = np.kron(gamma_phase*parity, gamma_phase)
            destination = big_indices ^ ((bit << n) | bit)
            acted = np.empty_like(rotated)
            acted[destination] = column_phase*rotated
            rotated = c*rotated+s*acted
    return np.vdot(doubled, rotated)


def family_formula(m,q,alpha):
    c,s=math.cos(alpha),math.sin(alpha)
    block=1-(math.sin(2*alpha)**2)/4
    cross=c*c*((1+c**4)/2)**m+s*s*((1+s**4)/2)**m
    return (1-q)**2+q*q*block**m+2*q*(1-q)*cross


def main():
    records=[]
    for m in (1,2):
        n=4*m+2
        for alpha,q,phase in (
            (math.pi/4, .25, 1),
            (.19, .05, 1j),
            (1.17, .6, -1),
        ):
            state=state_vector(m,q,phase)
            direct=rotation_overlap(state,n,alpha)
            target=family_formula(m,q,alpha)
            assert abs(direct-target)<1e-12
            branches=state.reshape(2,-1)
            probs=np.sum(np.abs(branches)**2,axis=1).real
            fs=[]
            for branch,prob in zip(branches,probs):
                value=rotation_overlap(branch/math.sqrt(prob),n-1,alpha)
                assert abs(value.imag)<1e-12
                fs.append(float(value.real))
            expected_branch=[1,(1-math.sin(2*alpha)**2/4)**m]
            assert np.max(np.abs(np.array(fs)-expected_branch))<1e-12
            delta=math.log(direct.real)-sum(p*math.log(f) for p,f in zip(probs,fs))
            records.append({'m':m,'N':n,'alpha':alpha,'q':q,'relative_phase':str(phase),
                'graded_F_real':float(direct.real),'graded_F_imag':float(direct.imag),
                'formula_F':target,'absolute_difference':float(abs(direct-target)),
                'probabilities':probs.tolist(),'branch_F':fs,'Delta_diagnostic':delta})
    report={'method':'full graded two-register factor product, no string-oracle import',
        'coverage':'m=1,2; alpha=pi/4,0.19,1.17; q=0.25,0.05,0.6; phases=1,i,-1; both branches',
        'records':records,
        'maximum_parent_abs_difference':max(r['absolute_difference'] for r in records),
        'limitations':'Finite floating diagnostics support convention checks; exact N=34 proof uses stable derivation and the separate exact local-string kernel contraction.'}
    (ROOT/'evidence/flagged-twist-graded-replay.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['Full graded-rotation replay passed all six parent and twelve branch comparisons.',
        f"Maximum parent absolute difference: {report['maximum_parent_abs_difference']:.3e}.",
        'N=6,10; three angles, probabilities and relative phases; both outcomes retained.',
        'Floating values are diagnostics, not a strict N=34 violation certificate.']
    (ROOT/'evidence/flagged-twist-graded-replay.log').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':
    main()
