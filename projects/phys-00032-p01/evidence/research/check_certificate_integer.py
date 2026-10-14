"""Independent standard-library integer-interval replay of every cover leaf.

Uses fixed-point integer arithmetic, integer square roots, and a proven
atanh-series logarithm remainder. Does not import mpmath or the generator.
"""
import json, math, hashlib, time
from fractions import Fraction as Q
from pathlib import Path
from decimal import Decimal, localcontext

OUT=Path(__file__).parent
S=1<<128
M=40
def ceildiv(a,b):return -((-a)//b)
class I:
    def __init__(self,lo,hi=None):self.lo=lo;self.hi=lo if hi is None else hi
    @staticmethod
    def q(q):
        q=Q(q);n=q.numerator*S;d=q.denominator
        return I(n//d,ceildiv(n,d))
    def __add__(x,y):return I(x.lo+y.lo,x.hi+y.hi)
    def __sub__(x,y):return I(x.lo-y.hi,x.hi-y.lo)
    def __mul__(x,y):
        p=[x.lo*y.lo,x.lo*y.hi,x.hi*y.lo,x.hi*y.hi]
        return I(min(p)//S,ceildiv(max(p),S))
    def __truediv__(x,y):
        assert y.lo>0 or y.hi<0
        vals=[Q(a*S,b) for a in [x.lo,x.hi] for b in [y.lo,y.hi]]
        lo,hi=min(vals),max(vals)
        return I(lo.numerator//lo.denominator,ceildiv(hi.numerator,hi.denominator))
    def sqrt(x):
        assert x.lo>=0
        lo=math.isqrt(x.lo*S);hi=math.isqrt(x.hi*S)
        if hi*hi<x.hi*S:hi+=1
        return I(lo,hi)

one=I.q(1);two=I.q(2)
def series_log(u):
    z=(u-one)/(u+one);assert z.lo>=0 and z.hi<S
    z2=z*z;power=z;total=I.q(0)
    for n in range(M):
        total=total+power/I.q(2*n+1)
        power=power*z2
    total=two*total
    # Remaining positive series terms are bounded geometrically.
    remainder=two*power/(I.q(2*M+1)*(one-z2))
    return I(total.lo,total.hi+remainder.hi)
ln2=series_log(I.q(2))
def log_endpoint(x):
    assert x>0
    k=x.bit_length()-S.bit_length()
    while (x < (S<<k) if k>=0 else (x<<(-k))<S):k-=1
    while (x >= (S<<(k+1)) if k+1>=0 else (x<<(-(k+1)))>=S):k+=1
    u=I(x)/I.q(1<<k) if k>=0 else I(x)*I.q(1<<(-k))
    return I.q(k)*ln2+series_log(u)
def log(x):
    a,b=log_endpoint(x.lo),log_endpoint(x.hi)
    return I(a.lo,b.hi)
def box_interval(lo,hi):return I(I.q(lo).lo,I.q(hi).hi)
def g(q):return q*(1-q)
def gmin(lo,hi):return min(g(lo),g(hi))
def phi(d,v):return d*log((d+(d*d+v*v).sqrt())/v)
def display(x):
    with localcontext() as ctx:
        ctx.prec=45
        # The exact integer endpoints, not displayed decimals, are the certificate.
        return {'lower_integer':str(x.lo),'upper_integer':str(x.hi),
                'scale_integer':str(S),'lower_display':str(Decimal(x.lo)/Decimal(S)),
                'upper_display':str(Decimal(x.hi)/Decimal(S))}
def decode(box):return tuple(Q(*x) for x in box)
def certify_box(box):
    al,ah,bl,bh=box
    a,b=box_interval(al,ah),box_interval(bl,bh)
    D=b*log(b/a)+(one-b)*log((one-b)/(one-a))
    H=one-(a*b).sqrt()-((one-a)*(one-b)).sqrt()
    P=phi(I.q(ah-bl),I.q(gmin(al,ah)+gmin(bl,bh)))
    return D+H-I.q(Q(9,10))*P

started=time.time()
file=OUT/'cycle-certificate.json'
data=json.loads(file.read_text())
leaves={decode(x['box']):x for x in data['cover']}
assert len(leaves)==len(data['cover'])
initial=(Q(1,20),Q(999999,1000000),Q(1,1000000),Q(19,20))
assert decode(data['initial_box'])==initial
used=set();counts={};minmargin=None;visited=0
def replay(box,depth):
    global minmargin,visited
    visited+=1
    if box in leaves:
        x=leaves[box];assert x['depth']==depth;used.add(box)
        why=x['reason'];al,ah,bl,bh=box
        if why=='outside_a_gt_b':assert ah<=bl
        elif why=='analytic_small_current_ratio':
            assert ah-bl<=Q(1,2)*(gmin(al,ah)+gmin(bl,bh))
        elif why=='interval_positive':
            assert al>=bh
            margin=certify_box(box);assert margin.lo>=0,(box,display(margin))
            minmargin=margin.lo if minmargin is None else min(minmargin,margin.lo)
        else:raise AssertionError(why)
        counts[why]=counts.get(why,0)+1
        return
    assert depth<50
    al,ah,bl,bh=box
    if ah-al>=bh-bl:
        mid=(al+ah)/2
        replay((al,mid,bl,bh),depth+1);replay((mid,ah,bl,bh),depth+1)
    else:
        mid=(bl+bh)/2
        replay((al,ah,bl,mid),depth+1);replay((al,ah,mid,bh),depth+1)
replay(initial,0)
assert used==set(leaves)
assert visited==data['visited']

x,y=I.q(Q(1,10)),I.q(Q(999,1000))
D=y*log(y/x)+(one-y)*log((one-y)/(one-x))
P=phi(y-x,x*(one-x)+y*(one-y))
psi=D/P
dc=I.q(Q(1,1000));rho=I.q(0)-dc*log(dc)-(one-dc)*log(one-dc)
corner=I.q(Q(99,1000))*log(I.q(1000))-rho-I.q(Q(9,10))*log(I.q(Q(2000999,999000)))
checks={
 'log2_lt7over10':ln2.hi<I.q(Q(7,10)).lo,
 'log1000_lt7':log(I.q(1000)).hi<7*S,
 'log1e6_between13and14':13*S<log(I.q(1000000)).lo and log(I.q(1000000)).hi<14*S,
 'log20_lt3':log(I.q(20)).hi<3*S,
 'asinh1000_lt8':log(I.q(1000)+I.q(1000001).sqrt()).hi<8*S,
 'tiny_b_error_below_margin':Q(1022,1000000)<Q(143,51200),
 'corner_positive':corner.lo>0,
 'psi0_witness_below9over10':psi.hi<I.q(Q(9,10)).lo,
 'complete_disjoint_rational_cover':used==set(leaves),
}
assert all(checks.values())
res={'status':'pass','scope':'Independent integer-interval replay of scalar certificate and constants; same proposer, not fresh referee acceptance.',
 'representation':'128-bit binary fixed-point intervals; signed integer directed divisions; isqrt; 40-term atanh logarithm with positive geometric tail bound',
 'certificate_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
 'visited':visited,'leaves':len(leaves),'leaf_counts':counts,
 'minimum_interval_leaf_margin_lower':display(I(minmargin)),
 'constant_checks':checks,'psi0_upper_witness_enclosure':display(psi),
 'corner_margin_enclosure':display(corner),'seconds':time.time()-started}
(OUT/'integer-replay-data.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
