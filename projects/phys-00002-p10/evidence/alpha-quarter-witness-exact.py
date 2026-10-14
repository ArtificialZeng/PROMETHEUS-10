#!/usr/bin/env python3
"""Exact Q(sqrt2) checks: output Laguerre vs independent Hermite Fourier Q.
No old numerical coefficients are read. All arithmetic uses fractions.
"""
from fractions import Fraction as F
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def c(a=0,b=0):return F(a),F(b)
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def times(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def P(v):return {(0,0):c(v)}
def add(*ps):
 d={}
 for p in ps:
  for k,v in p.items():d[k]=plus(d.get(k,c()),v)
 return {k:v for k,v in d.items() if v!=c()}
def scalar(p,a):return {k:times(v,a) for k,v in p.items() if times(v,a)!=c()}
def mul(a,b):
 d={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():d[i+k,j+l]=plus(d.get((i+k,j+l),c()),times(v,w))
 return {k:v for k,v in d.items() if v!=c()}
def power(p,n):
 out=P(1)
 for _ in range(n):out=mul(out,p)
 return out
x2={(2,0):c(1)};p2={(0,2):c(1)};R=add(x2,p2);DELTA=add(x2,scalar(p2,c(-1)))
# A: exact creation amplitudes yield partial-trace entries in denominator 401².
# Diagonal numerators rho00=160400+3/8, rho22=1601/4, rho44=3/8.
# Off diagonals rho02=7990, rho04=100sqrt6, rho24=5sqrt6.
def laguerre(n):
 return add(*(scalar(power(R,k),c((-2)**k*F(math.comb(n,k),math.factorial(k)))) for k in range(n+1)))
A=add(scalar(P(1),c(F(1283203,8))),scalar(laguerre(2),c(F(1601,4))),scalar(laguerre(4),c(F(3,8))),
      scalar(DELTA,c(0,15980)),scalar({(4,0):c(1),(2,2):c(-6),(0,4):c(1)},c(400)),
      scalar(mul(DELTA,add(P(6),scalar(R,c(-8)),scalar(power(R,2),c(2)))),c(0,10)))
A=scalar(A,c(F(1,401**2)))
# B: wavefunction f(q)=20-sqrt2/2+sqrt2*q², normalized by sqrt401.
# E[y²]=1/2-p²/2, E[y⁴]=3/4-3p²/2+p⁴/4 after z/sqrt2.
u=c(20,F(-1,2));v=c(0,1)
EX2=scalar(x2,c(F(1,2)));EY2=add(P(F(1,2)),scalar(p2,c(F(-1,2))))
EY4=add(P(F(3,4)),scalar(p2,c(F(-3,2))),scalar(power(p2,2),c(F(1,4))))
B=add({(0,0):times(u,u)},scalar(add(EX2,EY2),times(c(2),times(u,v))),
      scalar(add(power(EX2,2),scalar(mul(EX2,EY2),c(-2)),EY4),times(v,v)))
B=scalar(B,c(F(1,401)))
expected=scalar(add(P(401),scalar(R,c(-2)),scalar(power(R,2),c(F(1,2))),scalar(DELTA,c(0,20))),c(F(1,401)))
assert B==expected
assert A==mul(B,B)
# Exact normalization with Gaussian moments E[x^(2k)]=(2k-1)!!/2^k.
def gm(n):return F(math.prod(range(1,n,2)),2**(n//2)) if n%2==0 else F(0)
norm=c()
for (i,j),z in A.items():norm=plus(norm,times(z,c(gm(i)*gm(j))))
assert norm==c(1)
assert F(400**2+2*20**2,401**2)+F(2*6,16*401**2)+F(1,4*401**2)==1
out={'state':'(20|0>+|2>)/sqrt401, independently prepared on both inputs','A':'creation map, partial trace and even Laguerre Weyl matrix elements','B':'Hermite wavefunctions and Gaussian Fourier moments','independence':'same proposer, distinct exact physical representations; shared generic rational polynomial helpers; fresh referee still required','coefficient_equality':'exact Q(sqrt2), A=B²','full_plane_normalization':'exactly one','Q':[{'x':i,'p':j,'rational':str(a),'sqrt2':str(b)} for (i,j),(a,b) in sorted(B.items())],'Wout_polynomial':[{'x':i,'p':j,'rational':str(a),'sqrt2':str(b)} for (i,j),(a,b) in sorted(A.items())]}
(ROOT/'evidence/alpha-quarter-witness-exact.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
