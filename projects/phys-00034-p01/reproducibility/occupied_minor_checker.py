#!/usr/bin/env python3
"""Portable replay of the accepted independent exterior-power calculation.

This reproduction program is not a new scientific or release audit.

No submitted implementation, input JSON, or cached answer is imported.
The one-particle rotation is derived from the printed graded Majorana
generator. Exact many-particle matrix elements are its occupied minors.
"""
import itertools
import json
import math
import platform
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import sympy as sp

u, v, t = sp.symbols('u v t', real=True)


def one_particle(n, cu, sv):
    eye = sp.eye(n)
    return sp.BlockMatrix([[cu*eye, sv*eye], [-sv*eye, cu*eye]]).as_explicit()


def occ(word):
    return tuple(j for j, bit in enumerate(word) if bit)


def doubled(left, right):
    return occ(left + right)


def even_polynomial(expr):
    """Use u^2=1-t, v^2=t, with no numeric evaluation."""
    expr = sp.expand(expr)
    out = 0
    for (a, b), coefficient in sp.Poly(expr, u, v).terms():
        assert a % 2 == 0 and b % 2 == 0, (expr, a, b)
        out += coefficient*(1-t)**(a//2)*t**(b//2)
    return sp.factor(out)


def symbolic_kernel(n, states):
    rotation = one_particle(n, u, v)

    @lru_cache(None)
    def element(rows, columns):
        if len(rows) != len(columns):
            return sp.Integer(0)
        if not rows:
            return sp.Integer(1)
        return sp.expand(rotation.extract(rows, columns).det())

    result = {}
    for a, b, c, d in itertools.product(range(2), repeat=4):
        val = 0
        for (ra, aa), (ib, ab), (rc, ac), (id_, ad) in itertools.product(
                states[a].items(), states[b].items(), states[c].items(), states[d].items()):
            val += sp.conjugate(aa*ac)*ab*ad*element(doubled(ra, rc), doubled(ib, id_))
        result[a,b,c,d] = even_polynomial(val)
    return result


def family_contraction(flags, resources, m, p, q):
    total = 0
    for indices, entry in flags.items():
        if entry == 0:
            continue
        bcount = sum(indices)
        assert bcount % 2 == 0
        k = bcount//2
        total += p**(2-k)*q**k*entry*resources[indices]**m
    return sp.factor(total)


def integer_det(matrix):
    """Independent exact fraction-free elimination for numeric occupied minors."""
    a = [list(row) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign, previous = 1, 1
    for k in range(n-1):
        if a[k][k] == 0:
            row = next((r for r in range(k+1,n) if a[r][k]), None)
            if row is None:
                return 0
            a[k], a[row] = a[row], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator//previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


@lru_cache(None)
def fixed_angle_element(n, rows, columns):
    if len(rows) != len(columns):
        return F(0)
    k = len(rows)
    assert k % 2 == 0
    # At pi/4, R = [[I,I],[-I,I]]/sqrt(2).
    if any(sum(x % n == j for x in rows) != sum(x % n == j for x in columns)
           for j in range(n)):
        return F(0)
    def entry(i, j):
        if i % n != j % n:
            return 0
        return -1 if i >= n and j < n else 1
    mat = [[entry(i,j) for j in columns] for i in rows]
    return F(integer_det(mat), 2**(k//2))


def haar_replay(n, parity):
    basis = [tuple((word >> (n-1-j)) & 1 for j in range(n))
             for word in range(2**n) if word.bit_count() % 2 == parity]
    direct_trace = F(0)
    swapped_trace = F(0)
    for a,b in itertools.product(basis, repeat=2):
        columns = doubled(a,b)
        direct_trace += fixed_angle_element(n, columns, columns)
        swapped_trace += fixed_angle_element(n, doubled(b,a), columns)
    d = len(basis)
    return (direct_trace+swapped_trace)/(d*(d+1))


def sparse_family_replay(m, q):
    """Global register-first occupied minors; no block contraction here."""
    n = 4*m+2
    words = [(tuple([0]*n), 0)]
    for bits in itertools.product((0,1), repeat=m):
        word = (1,1)+tuple(bit for value in bits for bit in [value]*4)
        words.append((word,1))
    answer = F(0)
    p = 1-q
    for (wa,a),(wb,b),(wc,c),(wd,d) in itertools.product(words, repeat=4):
        value = fixed_angle_element(n, doubled(wa,wc), doubled(wb,wd))
        if not value:
            continue
        assert a+c == b+d  # particle conservation on the first flag mode
        k = a+c
        coefficient = p**(2-k)*(q/F(2**m))**k
        answer += coefficient*value
    return answer


def main():
    report = {'environment':{'python':platform.python_version(),'sympy':sp.__version__},
              'representation':'Occupied minors of R=[[uI,vI],[-vI,uI]], derived from graded source generator'}
    flags = symbolic_kernel(2,[{(0,0):sp.Integer(1)},{(1,1):sp.Integer(1)}])
    resources = symbolic_kernel(4,[{(0,0,0,0):sp.Integer(1)},
                                  {(0,0,0,0):1/sp.sqrt(2),(1,1,1,1):1/sp.sqrt(2)}])
    nonzero = {''.join(map(str,key)):{'flag':str(val),'resource':str(resources[key])}
               for key,val in flags.items() if val != 0}
    expected_flags = {(0,0,0,0):1,(1,1,1,1):1,
                      (0,0,1,1):1-t,(1,1,0,0):1-t,
                      (0,1,1,0):t,(1,0,0,1):t}
    assert all(sp.simplify(flags[key]-expected_flags.get(key,0)) == 0 for key in flags)
    f = 1-t+t*t
    a = (1+(1-t)**2)/2
    b = (1+t*t)/2
    expected_resources = {(0,0,0,0):1,(1,1,1,1):f,
                          (0,0,1,1):a,(1,1,0,0):a,
                          (0,1,1,0):b,(1,0,0,1):b}
    assert all(sp.simplify(resources[key]-val) == 0 for key,val in expected_resources.items())
    report['all_angle_local_kernels'] = {'index_order':'bra-copy1, ket-copy1, bra-copy2, ket-copy2',
                                       't':'sin(alpha)^2','nonzero_flag_entries':nonzero,
                                       'all_16_flag_entries_checked':True,
                                       'formula':'p^2+q^2(1-t+t^2)^m+2pq[(1-t)((1+(1-t)^2)/2)^m+t((1+t^2)/2)^m]'}
    exact_cases=[]
    for m in range(1,10):
        for q in (sp.Rational(1,4),sp.Rational(1,2),sp.Rational(3,4)):
            out=family_contraction(flags,resources,m,1-q,q).subs(t,sp.Rational(1,2))
            independent_closed=(1-q)**2+q*q*sp.Rational(3,4)**m+2*(1-q)*q*sp.Rational(5,8)**m
            assert out == independent_closed
            exact_cases.append({'m':m,'q':str(q),'F':str(out)})
    report['fixed_angle_exact_contractions']=exact_cases
    global_checks=[]
    for m in (1,2,3):
        q=F(1,4)
        got=sparse_family_replay(m,q)
        want=(1-q)**2+q*q*F(3,4)**m+2*(1-q)*q*F(5,8)**m
        assert got == want
        global_checks.append({'N':4*m+2,'m':m,'q':str(q),'F_from_global_minors':str(got),'F_from_closed_formula':str(want)})
    report['global_exact_sign_checks']=global_checks
    haar=[]
    for n in range(2,6):
        for parity in (0,1):
            got=haar_replay(n,parity)
            z=(2+sp.sqrt(2))/4
            published=sp.simplify(sp.Rational(2**n,2**n+2)*2*(z**n+(1-z)**n))
            assert sp.Rational(got.numerator,got.denominator) == published
            haar.append({'N':n,'parity':parity,'mean_F_from_trace_plus_swap':str(got),
                         'published_equation_8':str(published)})
    report['published_nonzero_haar_baseline']=haar
    q=sp.Rational(1,4);p=1-q;m=8
    parent=family_contraction(flags,resources,m,p,q).subs(t,sp.Rational(1,2))
    branch1=sp.Rational(3,4)**m
    ratio=sp.factor(parent/branch1**q)
    assert parent == sp.Rational(77509155,134217728)
    assert ratio == sp.Rational(25836385,25165824) and ratio>1
    x=ratio-1
    report['N34_certificate']={'N':34,'parent_norm_squared':'1','parent_parity':'even',
                 'outcome_probabilities':['3/4','1/4'],'remaining_parities':['even','odd'],
                 'F_parent':str(parent),'F_branch0':'1','F_branch1':str(branch1),
                 'exp_Delta':str(ratio),'Delta':'log('+str(ratio)+')',
                 'strict_integer_difference':int(sp.numer(ratio)-sp.denom(ratio)),
                 'lower_bound_Delta':str(x/(1+x)),'upper_bound_Delta':str(x),
                 'decimal_diagnostic':str(sp.N(sp.log(ratio),45))}
    report['asymptotic_scope']={'premises':'integer m>=1, 0<q<1, 0<alpha<pi/2',
        'f_range':'0<f=1-t(1-t)<1 for 0<t<1',
        'K_nonnegative':True,'parent_lower_bound':'F_parent>=p^2>0',
        'Delta_lower_bound':'q*m*(-log(f))+2*log(p)',
        'limit_parent':'p^2','unbounded_Delta':True,
        'mode_count_limit':'Sequence of finite N=4m+2 states; no infinite-system state assumed'}
    Path('outputs/occupied-minor-results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    print('PASS: all assertions completed; exact certificate and all-angle local identities checked.')


if __name__ == '__main__':
    main()
