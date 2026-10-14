#!/usr/bin/env python3
"""Outward Decimal box enclosure for benchmark integrals, not novel physics.
Decimal sqrt/exp are correctly rounded; expand by an adjacent representable value.
All arithmetic bounds use directed rounding. Tail expression from stable derivation.
"""
import decimal as d, json, time, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
d.getcontext().prec=40
DOWN=d.Context(prec=40,rounding=d.ROUND_FLOOR)
UP=d.Context(prec=40,rounding=d.ROUND_CEILING)
D=d.Decimal
def add(a,b): return (DOWN.add(a[0],b[0]),UP.add(a[1],b[1]))
def neg(a): return (-a[1],-a[0])
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    pairs=[(x,y) for x in a for y in b]
    return (min(DOWN.multiply(x,y) for x,y in pairs),max(UP.multiply(x,y) for x,y in pairs))
def sqrt(a):
    assert a[0]>=0
    return (max(D(0),a[0].sqrt().next_minus()),a[1].sqrt().next_plus())
def exp(a): return (a[0].exp().next_minus(),a[1].exp().next_plus())
def point(x): return (D(x),D(x))
def rat(n,m): return (DOWN.divide(D(n),D(m)),UP.divide(D(n),D(m)))
def sq(a):
    lo=D(0) if a[0]<=0<=a[1] else min(DOWN.multiply(x,x) for x in a)
    return (lo,max(UP.multiply(x,x) for x in a))
def absolute(a):
    if a[0]>=0: return a
    if a[1]<=0: return neg(a)
    return (D(0),max(-a[0],a[1]))
def atan_inv(k,N):
    # Alternating series, each operation directed; exact remainder <= next term.
    v=point(0)
    for j in range(N):
        term=rat(1,(2*j+1)*k**(2*j+1))
        v=add(v,term) if j%2==0 else sub(v,term)
    remainder=rat(1,(2*N+1)*k**(2*N+1))
    return add(v,(-remainder[1],remainder[1]))
PI=sub(mul(point(16),atan_inv(5,80)),mul(point(4),atan_inv(239,24)))
S2=sqrt(point(2))
PIQ=sqrt(sqrt(PI))
PREF=(DOWN.divide(D(1),PIQ[1]),UP.divide(D(1),PIQ[0]))
VAC=mul(point(4),mul(PI,PREF))
def Q(case,x,p):
    R=add(sq(x),sq(p))
    if case=='one_photon': return sub(R,point(1))
    # Exact Figure4 polynomial at z/sqrt(2), rearranged in R=x²+p².
    return add(add(add(add(add(rat(1,3),mul(rat(-2,3),x)),mul(mul(rat(2,3),S2),p)),mul(rat(-1,3),R)),mul(mul(rat(2,3),S2),mul(x,p))),add(mul(mul(rat(-1,3),S2),mul(p,R)),mul(rat(1,6),sq(R))))
def box(case,L,N):
    step=rat(2*L,N); total=point(0); area=mul(step,step)
    # Endpoints are exact rationals here: N is power of two, L integral.
    for i in range(N):
        x=(D(-L)+D(2*L)*i/N,D(-L)+D(2*L)*(i+1)/N)
        for j in range(N):
            p=(D(-L)+D(2*L)*j/N,D(-L)+D(2*L)*(j+1)/N)
            R=add(sq(x),sq(p)); g=exp(mul(rat(-1,4),R))
            f=mul(g,sqrt(absolute(Q(case,x,p))))
            total=add(total,mul(area,f))
    return mul(PREF,total)
def tail(case,L):
    # Outside square is subset of outside disk of radius L; L>=1.
    if case=='one_photon': factor=point(1)
    else:
        C=add(add(add(add(rat(1,3),mul(rat(2,3),add(S2,point(1)))),mul(rat(1,3),add(point(1),S2))),mul(rat(1,3),S2)),rat(1,6))
        factor=sqrt(C)
    u=rat(L*L,4)
    return mul(mul(mul(mul(point(16),PI),PREF),factor),mul(add(u,point(1)),exp(neg(u))))
def main():
    start=time.monotonic(); rows=[]
    for case in ['one_photon','figure4']:
        for N in [32,64,128,256]:
            I=box(case,10,N); t=tail(case,10)
            full=(I[0],UP.add(I[1],t[1]))
            row={'case':case,'square_half_width':10,'cells_per_side':N,'interior_enclosure':[str(x) for x in I],'full_plane_enclosure':[str(x) for x in full],'tail_upper':str(t[1]),'vacuum_upper':str(VAC[1]),'strictly_above_vacuum':full[0]>VAC[1]}
            rows.append(row); print(json.dumps(row),flush=True)
            if N==256: assert row['strictly_above_vacuum']
    record={'precision_decimal_digits':40,'pi_enclosure':[str(x) for x in PI],'vacuum_integral_enclosure':[str(x) for x in VAC],'rows':rows,'elapsed_seconds':time.monotonic()-start,'scope':'Only two fixed benchmark states at alpha=1/4; conservative numerical interval enclosure, proposer calculation requiring fresh replay.'}
    (ROOT/'evidence/alpha-quarter-enclosures.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
if __name__=='__main__': main()
