"""Direct column generator determinant, exact integer Laurent polynomials.
No dependency on input B or its implementation. Python standard library only.
"""
from itertools import permutations
from fractions import Fraction as F
from math import factorial
import json
from pathlib import Path

# Variables u0,u1,u2,w0,w1,w2,s,r; r exponent may be negative.
ZERO = (0,)*8
def add(*polys):
    out = {}
    for p in polys:
        for e,c in p.items(): out[e] = out.get(e,0)+c
    return {e:c for e,c in out.items() if c}
def scale(p,c): return {e:v*c for e,v in p.items() if v*c}
def mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(a+b for a,b in zip(e,f)); out[g]=out.get(g,0)+c*d
    return {e:c for e,c in out.items() if c}
def var(i,power=1):
    e=list(ZERO); e[i]=power; return {tuple(e):1}
u=[var(i) for i in range(3)]; w=[var(i+3) for i in range(3)]
s=var(6); r=var(7); inv=var(7,-1)
q=var(7,3); qi=var(7,-3)
L=[ [scale(add(u[0],w[2]),-1),w[0],mul(u[2],q)],
    [u[0],scale(add(u[1],w[0]),-1),w[1]],
    [mul(w[2],qi),u[1],scale(add(u[2],w[1]),-1)] ]
M=[[add(s,scale(L[i][j],-1)) if i==j else scale(L[i][j],-1)
    for j in range(3)] for i in range(3)]
det={}
for perm in permutations(range(3)):
    sign=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
    term={ZERO:sign}
    for i in range(3): term=mul(term,M[i][perm[i]])
    det=add(det,term)

def smul(a,b,n=4):
    return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(n+1)]
def logseries(a,n=4):
    assert a[0]==1
    x=a[:]; x[0]=0; out=[F(0)]*(n+1); power=[F(1)]+[F(0)]*n
    for k in range(1,n+1):
        power=smul(power,x,n)
        for i in range(n+1): out[i]+=F((-1)**(k+1),k)*power[i]
    return out
def determinant_cumulants(rates):
    """Compute per-cycle FPT cumulants from Xi(s,rho)=0; no renewal input."""
    U=rates[0]*rates[1]*rates[2]; W=rates[3]*rates[4]*rates[5]
    # Evaluate exact s coefficients at r=1, directly from the full determinant.
    P=[F(0)]*4
    for e,c in det.items():
        term=F(c)
        for i in range(6): term*=rates[i]**e[i]
        P[e[6]]+=term
    assert P[0]==0 and P[3]==1 and U>W
    # y=exp(A*rho). W*y^2-(U+W+P(s))*y+U=0 near y=1.
    y=[F(1)]+[F(0)]*4
    for n in range(1,5):
        nonlinear=W*sum(y[j]*y[n-j] for j in range(1,n))
        forcing=sum(P[j]*y[n-j] for j in range(1,min(n,3)+1))
        y[n]=(nonlinear-forcing)/(U-W)
    g=logseries(y)
    return [(-1)**n*factorial(n)*g[n] for n in range(1,5)]
def serialize(p): return [[list(e),c] for e,c in sorted(p.items())]
if __name__=='__main__':
    out=Path(__file__).parent/'computed-a.json'
    out.write_text(json.dumps({'variables':['u0','u1','u2','w0','w1','w2','s','r'],
        'matrix':[[serialize(p) for p in row] for row in L],
        'determinant':serialize(det)},indent=2)+'\n')
    print('A exact determinant generated:',len(det),'nonzero monomials')
