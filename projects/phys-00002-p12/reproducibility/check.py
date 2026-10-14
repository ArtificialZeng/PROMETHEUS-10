"""Portable scientific replay, adapted from the independent local referee check. Standard library only; deterministic inputs generated below. Not a substitute for the proof or human review."""
from fractions import Fraction as F
from math import comb, factorial, sqrt
import hashlib, json, pathlib

def solve(a,b):
    n=len(b); a=[[F(t) for t in row]+[F(v)] for row,v in zip(a,b)]
    for j in range(n):
        h=next(i for i in range(j,n) if a[i][j]); a[j],a[h]=a[h],a[j]
        t=a[j][j]; a[j]=[v/t for v in a[j]]
        for i in range(n):
            if i!=j:
                t=a[i][j]; a[i]=[v-t*w for v,w in zip(a[i],a[j])]
    return [row[-1] for row in a]

def mv(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]
def mul(a,b):
    return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(5)]

def ring(u,w,bond):
    n=len(u); a=[[F(0) for _ in u] for _ in u]
    for i in range(n):
        j=(i+1)%n
        a[j][i]+=u[i]; a[i][j]+=w[i]
        a[i][i]-=u[i]; a[j][j]-=w[i]
    assert all(sum(a[i][j] for i in range(n))==0 for j in range(n))
    aa=[row[:] for row in a]; aa[-1]=[F(1)]*n
    p=solve(aa,[0]*(n-1)+[1]); assert all(v>0 for v in p)
    derivatives=[]
    for k in range(1,5):
        d=[[F(0) for _ in u] for _ in u]; j=(bond+1)%n
        d[j][bond]=u[bond]; d[bond][j]=(-1)**k*w[bond]
        derivatives.append(d)
    vs=[p]; cs=[F(0)]
    for k in range(1,5):
        rhs=[F(0)]*n
        for j in range(1,k+1):
            d=mv(derivatives[j-1],vs[k-j])
            rhs=[x+comb(k,j)*y for x,y in zip(rhs,d)]
        c=sum(rhs); cs.append(c)
        target=[c*x-y for x,y in zip(p,rhs)]
        for j in range(1,k):
            target=[x+comb(k,j)*cs[j]*y for x,y in zip(target,vs[k-j])]
        target[-1]=0
        v=solve(aa,target); assert sum(v)==0
        vs.append(v)
    return cs[1:]

def passage(u,w):
    # Rotate to just AFTER the first irreversible bond. Fresh backward row generator.
    n=len(u); cut=w.index(0); order=[(cut+1+i)%n for i in range(n)]
    h=[[F(0) for _ in u] for _ in u]
    for j,i in enumerate(order):
        h[j][j]=u[i]+w[(i-1)%n]
        if j<n-1: h[j][j+1]=-u[i]
        if j>0: h[j][j-1]=-w[(i-1)%n]
    prev=[F(1)]*n; moments=[F(1)]
    for k in range(1,5):
        prev=solve(h,[k*x for x in prev]); moments.append(prev[0])
    # Solve exp(z)*E exp(-psi(z)*tau)=1 coefficientwise, using RAW moments.
    b=[F(0)]*5
    expz=[F(1,factorial(i)) for i in range(5)]
    for k in range(1,5):
        lap=[F(1)]+[F(0)]*4; power=lap[:]
        for j in range(1,5):
            power=mul(power,b)
            lap=[x+(-1)**j*moments[j]/factorial(j)*y for x,y in zip(lap,power)]
        residue=mul(expz,lap)[k]
        b[k]=residue/moments[1]
    cs=[b[k]*factorial(k) for k in range(1,5)]
    # Trace inverse powers independently recovers the spectral power sums without eigensolving.
    invcols=[solve(h,[int(i==j) for i in range(n)]) for j in range(n)]
    inv=[list(row) for row in zip(*invcols)]
    power=inv; traces=[]
    for k in range(1,5):
        traces.append(sum(power[i][i] for i in range(n)))
        power=[[sum(power[i][l]*inv[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
    m=traces[0]; q,r,s=[traces[k]/m**(k+1) for k in range(1,4)]
    assert cs[2]/cs[0]==3*q*q-2*r
    assert cs[3]/cs[1]==15*q*q-20*r+6*s/q
    assert cs[0]>0 and cs[1]>0
    assert cs[2]/cs[0]>=-F(1,16)
    # Exact comparison to -(1+sqrt(5))/10, without approximate irrational arithmetic.
    t=10*cs[3]/cs[1]+1
    assert t>=0 or t*t<=5
    return cs

def algebra():
    # Exact Q(sqrt(5)) polynomial certificates, encoded as rational pairs.
    def add(a,b): return (a[0]+b[0],a[1]+b[1])
    def times(a,b): return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def pm(a,b):
        c=[(F(0),F(0))]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): c[i+j]=add(c[i+j],times(x,y))
        return c
    def R(a,b=0): return (F(a),F(b))
    skew=pm([R(1),R(-4),R(4)],[R(F(1,16)),R(F(1,4)),R(F(3,4))])
    assert skew==[R(F(1,16)),R(0),R(0),R(-2),R(3)]
    a=R(F(1,2),F(1,10))
    sq=pm([(-a[0],-a[1]),R(1)],[(-a[0],-a[1]),R(1)])
    kurt=pm(sq,[R(-F(1,2),F(1,2)),R(-5,3),R(15)])
    assert kurt==[R(F(1,10),F(1,10)),R(0),R(6),R(-20),R(15)]
    print('Exact scalar skewness and Q(sqrt(5)) kurtosis certificates: PASS')

def main():
    algebra(); total=0
    for n in (3,4,6,8):
        for variant in range(4):
            u=[F((i+2)**2,(i%3)+1) for i in range(n)]
            w=[F((i+1)**3,(i%2)+2) for i in range(n)]
            if variant==0: w=[F(0)]*n
            if variant==1: w[n//2]=F(0)
            if variant==2: w[0]=w[-1]=F(0)
            if variant==3:
                w[-1]=F(0); u[0]=F(1,10**6); w[1]=F(10**6)
            c=passage(u,w)
            for b in range(n): assert ring(u,w,b)==c,(n,variant,b)
            total+=n
            print('boundary case',n,variant,'all counted bonds PASS; S,K=',str(c[2]/c[0]),str(c[3]/c[1]))
    u=[F(1,7)]+[F(1)]*7; w=[F(0)]*8
    c=ring(u,w,0)
    assert passage(u,w)==c
    assert c==[F(1,14),F(1,49),-F(1,1372),-F(1,4802)]
    assert c[2]/c[0]==-F(1,98)
    print('Published N=8 a=1/7 baseline c1..c4=',[str(x) for x in c],'PASS')
    for n in (3,10,100,1000):
        p=[F(1,2)]+[F(1,2*(n-1))]*(n-1)
        q=sum(x*x for x in p); r=sum(x**3 for x in p)
        print('skew sharpness N=',n,'S=',str(3*q*q-2*r))
    print('PASS:',total,'independent exact tilted-generator bond comparisons; 16 passage cases; analytic certificate checks.')

if __name__=='__main__': main()
