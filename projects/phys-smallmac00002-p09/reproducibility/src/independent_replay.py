#!/usr/bin/env python3
"""Fresh referee replay: no discovery code, input file, or cached result is read.

Primary convention: Harunari arXiv:2406.12792v2 Eqs. (30),(31).
All calculations use t_star=1. Symbolic checks are exact. Numerical replay uses
row-generator Poisson uniformization, with explicitly bounded series omission;
floating-point roundoff and Gauss quadrature are NOT interval certificates.
"""
import argparse
import datetime
import hashlib
import itertools
import json
import math
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np
import scipy
import sympy as sy
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
BEGIN = time.perf_counter()
RECORD = {}


def say(key, value):
    RECORD[key] = value
    print(key + ': ' + json.dumps(value, ensure_ascii=False), flush=True)


def elementary_generator(rates, absorb=False):
    """Derive a row generator by adding six individual jump balance terms.

    Basis is (1,2,3,+,-); visible jumps leave their physical arrival unoccupied
    and enter their own absorber. The escape diagonal is never recalculated
    from the retained hidden jumps.
    """
    q = sy.zeros(5 if absorb else 3)
    for (i, j), rate in rates.items():
        dest = {(0, 1): 3, (1, 0): 4}.get((i, j), j) if absorb else j
        q[i, i] -= rate
        q[i, dest] += rate
    return q


def symmetric_rates(a, b, c):
    return {(0, 1): a, (1, 0): a, (1, 2): b, (2, 1): b,
            (2, 0): c, (0, 2): c}


def exact_checks():
    k12, k21, k23, k32, k31, k13 = sy.symbols('k12 k21 k23 k32 k31 k13', positive=True)
    rates = {(0, 1): k12, (1, 0): k21, (1, 2): k23,
             (2, 1): k32, (2, 0): k31, (0, 2): k13}
    g = elementary_generator(rates, True)
    # New direct transcription of the published column matrix, absorbers (-,+).
    primary = sy.Matrix([[-k12-k13, 0, k31, 0, 0],
                         [0, -k21-k23, k32, 0, 0],
                         [k13, k23, -k31-k32, 0, 0],
                         [0, k21, 0, 0, 0],
                         [k12, 0, 0, 0, 0]])
    perm = sy.eye(5)[[0, 1, 2, 4, 3], :]
    assert primary == perm * g.T * perm.T
    assert g * sy.ones(5, 1) == sy.zeros(5, 1)
    say('primary_matrix_reconstruction', {'entries_checked':25,
        'result':'exact transpose plus absorber permutation agreement',
        'row_basis':['1','2','3','+','-'], 'published_basis':['1','2','3','-','+']})

    # Published stationary-unicycle baseline, independently recomputed.
    base_rates = {(0, 1):2, (1, 0):1, (1, 2):2,
                  (2, 1):1, (2, 0):2, (0, 2):1}
    base_g = elementary_generator(base_rates, True)
    r0, b0 = base_g[:3, :3], base_g[:3, 3:]
    x = sy.symbols('x', positive=True)
    selector = sy.Matrix([[0,1,0],[1,0,0]])
    densities = sy.simplify(selector * sy.exp(x*r0) * b0)
    probabilities = selector * (-r0).inv() * b0
    ratio = sy.simplify(densities[0,0]/densities[1,1])
    estimator = sy.simplify((sy.Rational(2,3)*probabilities[0,0]
                            -sy.Rational(1,3)*probabilities[1,1])*sy.log(ratio))
    sigma = sy.simplify(sum(sy.Rational(1,3)*v*sy.log(sy.Rational(v,base_rates[j,i]))
                            for (i,j),v in base_rates.items()))
    assert probabilities == sy.Matrix([[sy.Rational(8,15),sy.Rational(7,15)],
                                       [sy.Rational(14,15),sy.Rational(1,15)]])
    assert estimator == sigma == sy.log(2)
    say('stationary_baseline', {'joint_probabilities':str(probabilities),
        'same_direction_ratio':str(ratio),'estimator':str(estimator),
        'full_entropy':str(sigma),'eigenvalues':str(r0.eigenvals())})

    r = sy.symbols('r', positive=True)
    triples = [(r,1,1),(1,r,1),(1,1,r)]
    qs = [elementary_generator(symmetric_rates(*z)) for z in triples]
    gs = [elementary_generator(symmetric_rates(*z), True) for z in triples]
    rs = [q[:3,:3] for q in gs]
    for q in qs:
        assert q == q.T
        assert q * sy.ones(3,1) == sy.zeros(3,1)
        assert sy.ones(1,3) * q == sy.zeros(1,3)
    a = [z[0] for z in triples]
    weights = [a[i]*a[(i+1)%3] for i in range(3)]
    coeff = []
    # Row propagation is exp(u R_old) exp((x-u) R_new).
    # The simplex integral of u^m (x-u)^n/(m! n!) is x^(m+n+1)/(m+n+1)!.
    # We enumerate chronological words, not a submitted commutator formula.
    for degree in range(4):
        value = 0
        for i in range(3):
            j = (i+1)%3
            for nleft in range(degree+1):
                word = rs[i]**nleft * rs[j]**(degree-nleft)
                value += weights[i]*(word[1,0]-word[0,1])/sy.factorial(degree+1)
        coeff.append(sy.factor(value/(r+2)))
    expected = [0,0,-(r-1)**2/(6*(r+2))]
    assert all(sy.simplify(v-w)==0 for v,w in zip(coeff[:3],expected))
    switch = [sy.factor(weights[i]*((rs[i]*rs[(i+1)%3])[1,0]
                                   -(rs[i]*rs[(i+1)%3])[0,1])) for i in range(3)]
    say('periodic_exact', {'uniform_periodic_state':'(1,1,1)/3',
        'entropy':'0', 'event_phase_weight':'a(s)/(r+2)',
        'event_flux':'(r+2)/9', 'weighted_switch_terms':list(map(str,switch)),
        'r10_switch_terms':[str(z.subs(r,10)) for z in switch],
        'coefficients_x1_through_x4':list(map(str,coeff))})

    # Alternative direct path enumeration of the degree-two mixed words.
    path_switch=[]
    for i in range(3):
        j=(i+1)%3
        plus=sum(rs[i][1,k]*rs[j][k,0] for k in range(3))
        minus=sum(rs[i][0,k]*rs[j][k,1] for k in range(3))
        path_switch.append(sy.factor(weights[i]*(plus-minus)))
    assert path_switch==switch

    # Explicit r=10 remainder and rational estimator bound.
    norms=[max(sum(abs(v) for v in row) for row in z.subs(r,10).tolist()) for z in rs]
    assert max(norms)==22
    delta=sy.Rational(1,20000)
    remainder=sy.Rational(7,12)*22**3*delta/(1-22*delta)
    assert remainder==sy.Rational(1331,4281) and remainder<sy.Rational(9,16)
    bound=sy.Rational(4,3)*sy.Rational(1,10)*sy.Rational(9,16)**2*delta**7/7
    assert bound==sy.Rational(27,5734400000000000000000000000000000)
    k=sy.Matrix([[2,0,-1],[0,2,-1],[-1,-1,2]])
    shifted=k-sy.eye(3)/2
    minors=[shifted[:j,:j].det() for j in (1,2,3)]
    assert minors==[sy.Rational(3,2),sy.Rational(9,4),sy.Rational(3,8)]
    tail=sy.Rational(80,3)*sy.exp(-40)*(2*sy.log(20)+22*80+44)
    say('sign_and_tail_certificate', {'induced_infinity_norms':list(map(str,norms)),
        'remainder_over_x3_upper':str(remainder),
        'positive_integral_bound':str(bound),'bound_decimal':str(sy.N(bound,18)),
        'K_minus_halfI_leading_minors':list(map(str,minors)),
        'tail_H80':str(sy.N(tail,18)),
        'survival_H80':str(sy.N(sy.sqrt(3)*sy.exp(-40),18)),
        'generic_r_extension':'m=min(1,r)>0; M=max(1,r). -R>=mK; U<=exp(-m*x/2); A,B>=m^3*x^2*exp(-2*M*x)/2 and <=M*exp(-m*x/2). Constants are not uniform at r=0.'})


class UniformizedProtocol:
    def __init__(self, ratio=10, order=(0,1,2), horizon=81):
        triples=[(ratio,1,1),(1,ratio,1),(1,1,ratio)]
        triples=[triples[j] for j in order]
        self.a=np.array([z[0] for z in triples],dtype=float)
        self.phase_denom=ratio+2.
        self.flux=(ratio+2.)/9.
        self.q=[np.array(elementary_generator(symmetric_rates(*z),True),dtype=float) for z in triples]
        self.rate=max(-q.diagonal().min() for q in self.q)
        self.cut=85
        self.powers=[]
        for q in self.q:
            transition=np.eye(5)+q/self.rate
            terms=[np.eye(5)]
            for n in range(self.cut): terms.append(terms[-1]@transition)
            self.powers.append(np.array(terms))
        full=[self.segment(j,1.) for j in range(3)]
        self.products={}
        for j in range(3):
            u=np.eye(5)
            self.products[j,0]=u
            for n in range(1,horizon+3):
                u=u@full[(j+n-1)%3]
                self.products[j,n]=u

    def segment(self, j, h):
        z=self.rate*h
        weights=np.empty(self.cut+1)
        weights[0]=math.exp(-z)
        for n in range(1,len(weights)): weights[n]=weights[n-1]*z/n
        return np.einsum('n,nij->ij',weights,self.powers[j],optimize=False)

    def propagate(self,s,x):
        j=int(math.floor(s))%3
        first=1.-(s-math.floor(s))
        if x<=first:
            return self.segment(j,x),j
        u=self.segment(j,first)
        remaining=x-first
        whole=int(math.floor(remaining))
        frac=remaining-whole
        u=u@self.products[(j+1)%3,whole]
        last=(j+whole+1)%3
        return u@self.segment(last,frac),last

    def law(self,x,phase_order):
        nodes,weights=leggauss(phase_order)
        # Starting and ending phases have all jumps explicitly split.
        breaks=sorted(set([0.,1.,2.,3.]+[float((j-x)%3) for j in range(3)]))
        d=np.zeros((2,2))
        absorption=np.zeros((2,2))
        for lo,hi in zip(breaks[:-1],breaks[1:]):
            if hi-lo<1e-14: continue
            for node,w in zip(nodes,weights):
                s=(lo+hi)/2+(hi-lo)*node/2
                u,last=self.propagate(s,x)
                weight=(hi-lo)*w/2*self.a[int(s)%3]/self.phase_denom
                arrivals=u[[1,0],:]
                d+=weight*(arrivals@self.q[last])[:,[3,4]]
                absorption+=weight*arrivals[:,[3,4]]
        return d,absorption


def numerical_checks(order,horizon):
    model=UniformizedProtocol(horizon=horizon+1)
    samples={}
    for x in [0.005,0.05,0.2,0.75,1.25,2.1,5.4]:
        d,_=model.law(x,order)
        samples[str(x)]={'densities':d.tolist(),'A_minus_B_over_x3':float((d[0,0]-d[1,1])/x**3)}
    say('independent_density_samples',samples)
    # Delay quadrature split at each integer, where the protocol overlap changes.
    nodes,weights=leggauss(order)
    integral=0.
    probs=np.zeros((2,2))
    for block in range(horizon):
        for node,w in zip(nodes,weights):
            x=block+(node+1.)/2
            d,_=model.law(x,order)
            aa,bb=d[0,0],d[1,1]
            assert aa>0 and bb>0
            integral+=w/2*model.flux*(aa-bb)*math.log(aa/bb)
            probs+=w/2*d
    _,absorbed=model.law(float(horizon),order)
    omission=math.exp(-model.rate)*model.rate**(model.cut+1)/math.factorial(model.cut+1)/(1-model.rate/(model.cut+2))
    say('numerical_integral',{'gauss_order_phase_and_delay':order,'horizon':horizon,
        'estimator':float(integral),'integrated_joint_channels':probs.tolist(),
        'integrated_row_sums':probs.sum(axis=1).tolist(),
        'direct_absorption_row_sums':absorbed.sum(axis=1).tolist(),
        'max_integral_vs_absorption_difference':float(np.abs(probs-absorbed).max()),
        'Poisson_series_degree':model.cut,'max_omitted_probability_per_subsegment':omission,
        'limitations':'Poisson omission bound only; no interval enclosure of floating-point arithmetic or Gauss quadrature. Exact sign and infinite integral established separately.'})
    # Deliberate attacks: reverse order, equal-rate degeneration, cyclic phase shift.
    forward=model.law(0.2,order)[0]
    reverse=UniformizedProtocol(order=(2,1,0)).law(0.2,order)[0]
    shift=UniformizedProtocol(order=(1,2,0)).law(0.2,order)[0]
    degenerate=UniformizedProtocol(ratio=1).law(0.2,order)[0]
    say('adversarial_checks',{'x':0.2,
        'reversal_same_channel_exchange_error':float(max(abs(reverse[0,0]-forward[1,1]),abs(reverse[1,1]-forward[0,0]))),
        'phase_origin_change_error':float(np.max(abs(forward-shift))),
        'r1_same_direction_difference':float(degenerate[0,0]-degenerate[1,1])})


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--numeric',action='store_true')
    parser.add_argument('--order',type=int,default=16)
    parser.add_argument('--horizon',type=int,default=80)
    args=parser.parse_args()
    say('environment',{'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'sympy':sy.__version__,'float_dtype':'float64','command':sys.argv,
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'independence':'Only primary formulas and frozen claim/proof were read; no discovery code or cached scientific result imported.'})
    exact_checks()
    if args.numeric: numerical_checks(args.order,args.horizon)
    say('resources',{'elapsed_seconds':time.perf_counter()-BEGIN,
        'maxrss_platform_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'platform':platform.system(),'worker_processes':1})
    suffix=('numeric-q%d-H%d'%(args.order,args.horizon)) if args.numeric else 'exact'
    (HERE/('referee-replay-'+suffix+'.json')).write_text(json.dumps(RECORD,indent=2,ensure_ascii=False)+'\n')
    print('ALL EXECUTED ASSERTIONS PASSED',flush=True)
