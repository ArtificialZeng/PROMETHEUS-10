"""Directed-interval certificate for the central two-occupation inequality.

Rational bisection covers the complete central rectangle. Other regions are
handled by the analytic proof in uniform-bound-proof.md. No optimization is
used to certify. Run from project root, one CPU; does not read handoffs.
"""
import json, time, hashlib
from pathlib import Path
from fractions import Fraction as Q
import mpmath as mp

OUT=Path(__file__).parent
mp.iv.dps=45
IV=mp.iv
def rat(q):
    q=Q(q)
    return IV.mpf(q.numerator)/q.denominator
def interval(lo,hi):
    x,y=rat(lo),rat(hi)
    return IV.mpf([x.a,y.b])
def g(q):return q*(1-q)
def gmin(lo,hi):return min(g(lo),g(hi))
def gmax(lo,hi):
    return Q(1,4) if lo<=Q(1,2)<=hi else max(g(lo),g(hi))
def endpoints(x):return [str(x.a),str(x.b)]
def frac(q):return [q.numerator,q.denominator]
def enclosure(box):
    al,ah,bl,bh=box
    a,b=interval(al,ah),interval(bl,bh)
    # Nonzero-current boxes only; the diagonal uses an analytic bound.
    D=b*IV.log(b/a)+(1-b)*IV.log((1-b)/(1-a))
    H=1-IV.sqrt(a*b)-IV.sqrt((1-a)*(1-b))
    dhi=ah-bl
    vlo=gmin(al,ah)+gmin(bl,bh)
    d,v=rat(dhi),rat(vlo)
    # Monotonicity makes this a valid upper bound for Phi on the box.
    Phi=d*IV.log((d+IV.sqrt(d*d+v*v))/v)
    lower=D+H-rat(Q(9,10))*Phi
    return lower

initial=(Q(1,20),Q(999999,1000000),Q(1,1000000),Q(19,20))
stack=[(initial,0)]
leaves=[];visited=0;maxdepth=0;start=time.time()
while stack:
    box,depth=stack.pop();visited+=1;maxdepth=max(maxdepth,depth)
    al,ah,bl,bh=box
    if ah<=bl:
        kind='outside_a_gt_b'
    elif ah-bl<=Q(1,2)*(gmin(al,ah)+gmin(bl,bh)):
        kind='analytic_small_current_ratio'
    elif al>=bh:
        bound=enclosure(box)
        if bool(bound.a>=0):
            kind='interval_positive'
        else:kind=None
    else:kind=None
    if kind:
        leaf={'box':[frac(q) for q in box],'reason':kind,'depth':depth}
        if kind=='interval_positive':leaf['margin_enclosure']=endpoints(bound)
        leaves.append(leaf)
        continue
    if depth>=50 or time.time()-start>180:
        raise RuntimeError('Incomplete certificate; depth or wall budget reached')
    if (ah-al)>=(bh-bl):
        mid=(al+ah)/2
        stack.extend([((al,mid,bl,bh),depth+1),((mid,ah,bl,bh),depth+1)])
    else:
        mid=(bl+bh)/2
        stack.extend([((al,ah,bl,mid),depth+1),((al,ah,mid,bh),depth+1)])
    if visited%5000==0:print(json.dumps({'visited':visited,'pending':len(stack),'seconds':time.time()-start}),flush=True)

# Exact primary psi0 upper witness; this does not enclose its optimal value.
a,b=rat(Q(1,10)),rat(Q(999,1000))
d=a-b;v=a*(1-a)+b*(1-b)
D=b*IV.log(b/a)+(1-b)*IV.log((1-b)/(1-a))
F=d*IV.log((d+IV.sqrt(d*d+v*v))/v)
psi=D/F
assert bool(psi.b<rat(Q(9,10)))
dc=rat(Q(1,1000))
rho=-dc*IV.log(dc)-(1-dc)*IV.log(1-dc)
corner=rat(Q(99,1000))*IV.log(1000)-rho-rat(Q(9,10))*IV.log(rat(Q(2000999,999000)))
assert bool(corner.a>0)
checks={
 'log2_lt_7over10':bool(IV.log(2).b<rat(Q(7,10))),
 'log1000_lt7':bool(IV.log(1000).b<7),
 'log1e6_lt14_gt13':bool(IV.log(1000000).b<14 and IV.log(1000000).a>13),
 'log20_lt3':bool(IV.log(20).b<3),
 'asinh1000_lt8':bool(IV.log(1000+IV.sqrt(1000001)).b<8),
 'tiny_b_error_below_margin':Q(1022,1000000)<Q(143,51200),
 'opposite_corner_margin_positive':bool(corner.a>0),
 'psi0_witness_below_9over10':bool(psi.b<rat(Q(9,10))),
}
assert all(checks.values())
res={'status':'complete_interval_cover','mode':'computer_assisted',
 'scope':'Central a>b rectangle; complete scalar result also requires stated analytic tail/small-ratio arguments. Not referee acceptance.',
 'mpmath_version':mp.__version__,'interval_decimal_precision':IV.dps,
 'initial_box':[frac(q) for q in initial],
 'tested':'D(b||a)+1-sqrt(ab)-sqrt((1-a)(1-b)) >= (9/10) Phi(a-b,g(a)+g(b))',
 'visited':visited,'leaves':len(leaves),'max_depth':maxdepth,
 'leaf_counts':{k:sum(x['reason']==k for x in leaves) for k in ['outside_a_gt_b','analytic_small_current_ratio','interval_positive']},
 'seconds':time.time()-start,'analytic_constants':checks,
 'opposite_corner_margin_enclosure':endpoints(corner),
 'psi0_witness':{'x':[1,10],'y':[999,1000],'ratio_enclosure':endpoints(psi)},
 'cover':leaves}
(OUT/'cycle-certificate.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k!='cover'},indent=2))
