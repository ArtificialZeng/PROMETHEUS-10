#!/usr/bin/env python3
"""Exact rational interval certificate. Standard library only; no floating arithmetic.

All I(a,b) intervals mean [a/10**90,b/10**90]. Every rounded operation is outward.
Machin arctan series encloses pi; Taylor with explicit remainder encloses sine.
Residuals of rational vector proposals isolate each Hermitian eigenvalue.
Endpoint order statistics then enclose complete unrestricted/restricted sorts.
"""
from pathlib import Path
from fractions import Fraction as F
import json, math, hashlib, time

OUT=Path(__file__).resolve().parent
S=10**90
def ceildiv(a,b):return -((-a)//b)
class I:
    def __init__(self,a,b=None):
        self.a=int(a);self.b=int(a if b is None else b)
        assert self.a<=self.b
    @classmethod
    def frac(cls,x):
        x=F(x);return cls(x.numerator*S//x.denominator,ceildiv(x.numerator*S,x.denominator))
    @classmethod
    def point(cls,x):return cls(F(x).numerator*S//F(x).denominator)
    def __add__(self,y):
        if not isinstance(y,I):y=I.frac(y)
        return I(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,y):return self+-y if isinstance(y,I) else self+-I.frac(y)
    def __mul__(self,y):
        if not isinstance(y,I):y=I.frac(y)
        q=[self.a*y.a,self.a*y.b,self.b*y.a,self.b*y.b]
        return I(min(q)//S,ceildiv(max(q),S))
    __rmul__=__mul__
    def divint(self,d):
        assert d>0
        return I(self.a//d,ceildiv(self.b,d))
    def bound(self):return max(abs(self.a),abs(self.b))
    def save(self):return [str(self.a),str(self.b)]
    def show(self,digits=18):
        scale=10**digits
        def fmt(v):
            sign='-' if v<0 else '';v=abs(v)
            return sign+str(v//scale)+'.'+str(v%scale).zfill(digits)
        return [fmt(self.a*scale//S),fmt(ceildiv(self.b*scale,S))]

def atan_inv(d,K):
    total=I(0)
    for k in range(K):
        term=I.frac(F((-1)**k,(2*k+1)*d**(2*k+1)))
        total=total+term
    tail=ceildiv(S,(2*K+1)*d**(2*K+1))
    return total+I(-tail,tail)

PI=16*atan_inv(5,120)-4*atan_inv(239,40)
assert PI.a>3*S and PI.b<4*S

def sin_pi(t):
    t=F(t);sign=1
    if t<0:t=-t;sign=-sign
    t=t%2
    if t>1:t=t-1;sign=-sign
    if t>F(1,2):t=1-t
    if t==0:return I(0)
    x=PI*I.frac(t);x2=x*x
    term=x;total=I(0);M=100
    for k in range(M):
        total=total+term
        term=-(term*x2).divint((2*k+2)*(2*k+3))
    # Taylor polynomial degree 2M-1. Remainder <= |x|^(2M+1)/(2M+1)!:
    # order-2M Taylor coefficient is zero. x<=pi/2<2, so bound 2^(2M+1).
    remainder=ceildiv(S*2**(2*M+1),math.factorial(2*M+1))
    out=total+I(-remainder,remainder)
    return out if sign==1 else -out

def correlation(N):
    l=N//2
    waves=[[sin_pi(F(j*k,N+1)) for k in range(1,l+1)] for j in range(1,l+1)]
    return [[sum((2*waves[i][k]*waves[j][k] for k in range(l)),I(0)).divint(N+1) for j in range(l)] for i in range(l)]

def eigen_enclosures(C,proposal):
    l=len(C);r=S//10**45;answer=[];proofs=[]
    for lam,vec in zip(proposal['eigenvalues_desc'],proposal['eigenvectors_desc']):
        lam=I.point(lam);v=[I.point(x) for x in vec]
        norm2=sum(x.a*x.a for x in v);assert norm2>0
        residual=[sum((C[i][j]*v[j] for j in range(l)),I(0))-lam*v[i] for i in range(l)]
        res2=sum(x.bound()**2 for x in residual)
        # Exact comparison of ||(C-lambda)v||^2 <= (10^-45)^2 ||v||^2.
        assert res2*S*S < r*r*norm2
        box=I(lam.a-r,lam.a+r)
        assert 0<box.a<box.b<S
        answer.append(box)
        proofs.append({'center_scaled':str(lam.a),'radius_scaled':str(r),'vector_norm_squared_numerator':str(norm2),
                       'residual_norm_squared_upper_numerator':str(res2),
                       'exact_residual_inequality':True})
    assert len(answer)==l
    assert all(answer[j].a>answer[j+1].b for j in range(l-1))
    # Disjoint residual intervals each contain an eigenvalue; l such intervals
    # of an l-dimensional Hermitian matrix isolate all eigenvalues in order.
    return answer,proofs

def products(nu,eps):
    p=[I(S)];E=[I(0)]
    for v,e in zip(nu,eps):
        p=[x*(I(S)-v) for x in p]+[x*v for x in p]
        E=E+[x+e for x in E]
    return p,E

def passive_interval(p,E,masks):
    # Componentwise bounds survive sorting. Do not need to separate degeneracies.
    pl=sorted((p[m].a for m in masks),reverse=True)
    pu=sorted((p[m].b for m in masks),reverse=True)
    el=sorted(E[m].a for m in masks)
    eu=sorted(E[m].b for m in masks)
    return sum((I(a,b)*I(c,d) for a,b,c,d in zip(pl,pu,el,eu)),I(0))

def witness(p,E,a,b):
    dg=E[b]-E[a];dp=p[b]-p[a];w=dg*dp
    assert dg.a>0 and dp.a>0 and w.a>0
    assert a.bit_count()==b.bit_count()
    return {'lower_energy_mask':a,'higher_energy_mask':b,'particle_number':a.bit_count(),
            'energy_gap':dg.save(),'probability_gap':dp.save(),'swap_work_gain':w.save(),
            'energy_gap_decimal':dg.show(),'probability_gap_decimal':dp.show(),'swap_work_gain_decimal':w.show()}

proposals=json.loads((OUT/'eigenvector-proposals.json').read_text())
results=[]
for prop in proposals['cases']:
    t=time.monotonic();N=prop['N'];l=N//2
    C=correlation(N);nu,eigproof=eigen_enclosures(C,prop)
    eps=[-2*sin_pi(F(1,2)-F(j,l+1)) for j in range(1,l+1)]
    assert all(eps[j].b<eps[j+1].a for j in range(l-1))
    p,E=products(nu,eps);masks=list(range(1<<l))
    align=sum((a*b for a,b in zip(nu,eps)),I(0))
    passive=passive_interval(p,E,masks)
    bynumber=sum((passive_interval(p,E,[m for m in masks if m.bit_count()==k]) for k in range(l+1)),I(0))
    byparity=sum((passive_interval(p,E,[m for m in masks if m.bit_count()%2==k]) for k in range(2)),I(0))
    gain=align-passive;numgain=align-bynumber;pargain=align-byparity
    E0=sum(eps[:l//2],I(0));initial=sum((-2*C[j][j+1] for j in range(l-1)),I(0))
    case={'N':N,'l':l,'C_A_intervals':[[x.save() for x in row] for row in C],
          'nu_desc_intervals':[x.save() for x in nu],'epsilon_intervals':[x.save() for x in eps],
          'eigenvalue_isolation_checks':eigproof,'E_align':align.save(),'E_passive':passive.save(),
          'E_initial':initial.save(),'E_A0':E0.save(),'extra_work_full':gain.save(),
          'extra_work_number':numgain.save(),'extra_work_parity':pargain.save(),
          'extra_work_full_decimal':gain.show(),'extra_work_number_decimal':numgain.show(),
          'bound_energy_align':(align-E0).save(),'bound_energy_full':(passive-E0).save(),
          'complete_probability_intervals':[x.save() for x in p],
          'complete_energy_intervals':[x.save() for x in E]}
    if N>=12:
        assert gain.a>0 and numgain.a>0 and pargain.a>0
        # These masks are exploratory proposals. Every required sign is checked.
        pair={12:(6,9),16:(13,19),20:(27,39),24:(55,79)}[N]
        case['same_number_witness']=witness(p,E,*pair)
    if N==12:
        first=case['same_number_witness']
        second=witness(p,E,39,27)
        case['second_disjoint_witness']=second
        double=I(*first['swap_work_gain'])+I(*second['swap_work_gain'])
        case['two_disjoint_swaps_gain']=double.save()
        case['two_disjoint_swaps_gain_decimal']=double.show()
        four14=nu[0]*(I(S)-nu[1])*(I(S)-nu[2])*nu[3]
        four23=(I(S)-nu[0])*nu[1]*nu[2]*(I(S)-nu[3])
        quartic=(eps[0]+eps[3]-eps[1]-eps[2])*(four14-four23)
        assert quartic.a>0
        case['quartic_gate_gain']=quartic.save()
        case['quartic_gate_gain_decimal']=quartic.show()
    if N==8:
        # All negative-energy excitations have two alpha and two beta modes.
        # alpha>2 beta and entanglement alpha-cost>2 beta-cost give lex order.
        energy_order=-eps[0]+2*eps[1]
        assert energy_order.a>0
        # r1<r2^2, without logarithms or division: (1-nu1)*nu2^2 < nu1*(1-nu2)^2.
        order=nu[0]*(I(S)-nu[1])*(I(S)-nu[1])-(I(S)-nu[0])*nu[1]*nu[1]
        assert order.a>0
        case['N8_lexicographic_passivity_check']=order.save()
        case['N8_alpha_minus_twice_beta']=energy_order.save()
    results.append(case)
    print(f'N={N}: all {l} eigenvalues isolated; full extra work interval {gain.show()}; number {numgain.show()}',flush=True)
    if 'same_number_witness' in case:print('certified number/parity swap',case['same_number_witness'],flush=True)
    print('seconds',time.monotonic()-t,flush=True)
record={'arithmetic':'exact scaled-integer rational intervals; outward rounding on every operation','scale':str(S),
        'pi_interval':PI.save(),'pi_decimal':PI.show(30),'pi_formula':'16 atan(1/5)-4 atan(1/239); alternating-series truncation bounds',
        'trigonometric_bound':'100 sine terms on reduced rational multiple of pi in [0,pi/2]; remainder <=2^201/201!',
        'eigen_bound':'Hermitian residual plus disjoint l intervals; radius 10^-45',
        'proposal_sha256':hashlib.sha256((OUT/'eigenvector-proposals.json').read_bytes()).hexdigest(),
        'cases':results,'all_checks_completed':True,'scope':'same-worker proposer computer-assisted certificate; no fresh referee acceptance'}
(OUT/'certificate.json').write_text(json.dumps(record,indent=2)+'\n')
print('All exact certificate checks completed. This is proposer verification only.')
