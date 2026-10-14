"""Bounded exact thermal search; standard library only. No universal conclusion.
E integer in epsilon; beta_a=2 ln(b_a)/epsilon, b_a rational >1.
k^a_ij=g^a_{ij} b_a**(E_j-E_i), symmetric g>=0, in tau^-1.
"""
from fractions import Fraction as F
from math import comb
from itertools import combinations
from pathlib import Path
import json, random, time

def solve(a,b):
    n=len(b); a=[list(row)+[b[i]] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if a[i][j])
        a[j],a[pivot]=a[pivot],a[j]
        x=a[j][j]; a[j]=[v/x for v in a[j]]
        for i in range(n):
            if i!=j:
                x=a[i][j]; a[i]=[v-x*w for v,w in zip(a[i],a[j])]
    return [row[-1] for row in a]

def calculate(spec,selected=0):
    e=spec['energies']; n=len(e); bases=list(map(F,spec['bases']))
    g=[[F(v) for v in row] for row in spec['couplings']]
    ds=[[[F(0) for j in e] for i in e] for m in range(5)]
    edges=[]
    for z,(i,j) in enumerate(combinations(range(n),2)):
        for a,b in enumerate(bases):
            for dest,dep in [(i,j),(j,i)]:
                rate=g[a][z]*b**(e[dep]-e[dest]); q=e[dep]-e[dest]
                edges.append((dest,dep,a,rate,q))
                ds[0][dest][dep]+=rate; ds[0][dep][dep]-=rate
                if a==selected:
                    for m in range(1,5): ds[m][dest][dep]+=rate*q**m
    w=ds[0]; mat=[row[:] for row in w]; mat[-1]=[F(1)]*n
    p=solve(mat,[F(0)]*(n-1)+[F(1)])
    assert min(p)>0 and sum(p)==1
    assert all(sum(w[i][j] for i in range(n))==0 for j in range(n))
    def mv(a,v): return [sum(a[i][j]*v[j] for j in range(n)) for i in range(n)]
    assert mv(w,p)==[0]*n
    v=[p]; c=[F(0)]
    for m in range(1,5):
        forcing=[F(0)]*n
        for k in range(1,m+1):
            t=mv(ds[k],v[m-k])
            forcing=[x+comb(m,k)*y for x,y in zip(forcing,t)]
        c.append(sum(forcing))
        rhs=[c[m]*p[i]-forcing[i] for i in range(n)]
        for k in range(1,m):
            rhs=[x+comb(m,k)*c[k]*y for x,y in zip(rhs,v[m-k])]
        vn=solve(mat,rhs[:-1]+[F(0)])
        assert sum(vn)==0 and mv(w,vn)==rhs
        v.append(vn)
    return c[1:],p,edges,ds

def encode(x):
    if isinstance(x,F): return str(x)
    raise TypeError(type(x))

def main():
    rng=random.Random(2026101204); start=time.monotonic()
    rows=[]; best=None; negative=[]; zero=0; singular=0
    for z in range(1800):
        e=[0,1,rng.choice([2,3,4,6])]
        bases=rng.choice([['5/4','2'],['2','3'],['9/8','8'],['2','16'],['2','2']])
        # One bath may omit a paired edge; total complete graph retained.
        g=[[str(F(2)**rng.randint(-8,8)) for k in range(3)] for a in range(2)]
        if z%3==0:
            for k in range(3): g[rng.randrange(2)][k]='0'
        spec={'energies':e,'bases':bases,'couplings':g}
        try: c,p,edges,ds=calculate(spec)
        except (StopIteration,AssertionError): singular+=1; continue
        ratio=c[3]/c[1] if c[1] else None
        row={'index':z,'spec':spec,'cumulants':c,'ratio':ratio}
        rows.append(row)
        if ratio is None: zero+=1
        elif best is None or ratio<best['ratio']: best=row
        if c[3]<0:
            negative.append(row)
            break
        if z%100==0:
            print(z,'best ratio',float(best['ratio']) if best else None,flush=True)
            Path('evidence/search-progress.json').write_text(json.dumps({'completed':len(rows),'best':best},default=encode,indent=2)+'\n')
    out={'seed':2026101204,'planned':1800,'completed':len(rows),'singular':singular,'zero_variance':zero,'negative':negative,'best':best,'elapsed_seconds':time.monotonic()-start,'arithmetic':'exact Fraction; normalized Poisson recursion','samples':rows}
    Path('evidence/three-state-search.json').write_text(json.dumps(out,default=encode,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='samples'},default=encode,indent=2))

if __name__=='__main__': main()
