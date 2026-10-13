#!/usr/bin/env python3
"""Exact composition check using only the Python standard library.

Constructs the two-generation numerator directly from the 27 Hamiltonian
weights and verifies a hand-entered certificate by sparse polynomial
arithmetic over integers. It imports no CAS and reads no cached input,
quotient, certificate, or prior log. The certificate is checked coefficient by coefficient.
"""
import argparse
import sys
import json
from pathlib import Path
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', default='reproducibility/outputs')
args = parser.parse_args()
OUT = (ROOT / args.output_dir).resolve()
if not OUT.is_relative_to(ROOT) or OUT == ROOT:
    raise SystemExit('Output must be a subdirectory of the project.')
if sys.flags.optimize:
    raise SystemExit('Assertions are required; do not run Python with -O.')
OUT.mkdir(parents=True, exist_ok=True)
# Polynomials are dicts (exponent of t, exponent of h, exponent of u) -> int.
def clean(p):
    return {e:c for e,c in p.items() if c}

def add(*ps):
    ans={}
    for p in ps:
        for e,c in p.items(): ans[e]=ans.get(e,0)+c
    return clean(ans)

def scale(p,c):
    return clean({e:c*a for e,a in p.items()})

def mul(p,q):
    ans={}
    for e,a in p.items():
        for f,b in q.items():
            g=tuple(i+j for i,j in zip(e,f))
            ans[g]=ans.get(g,0)+a*b
    return clean(ans)

def power(p,n):
    ans={(0,0,0):1}
    for _ in range(n): ans=mul(ans,p)
    return ans

def poly(terms):
    # Terms are (integer coefficient, t exponent, h exponent, u exponent).
    return add(*[{(i,j,k):c} for c,i,j,k in terms])

ONE={(0,0,0):1}
U={(0,0,1):1}
T={(1,0,0):1}
weights={}
for i,j,k in product(range(3),repeat=3):
    weights[i,j,k]={(abs(i-j)+abs(i-k),abs(j-k),0):1}

def update(messages):
    return [add(*(mul(weights[i,j,k],mul(messages[j],messages[k]))
                  for j,k in product(range(3),repeat=2))) for i in range(3)]

log=[]
M=update([ONE,U,ONE])
assert M[2]==M[0]
N=poly([(1,0,0,2),(4,1,1,1),(2,2,2,0),(2,2,0,0)])
D=poly([(1,2,0,2),(2,3,1,1),(2,1,1,1),(1,4,0,0),(2,2,2,0),(1,0,0,0)])
assert M[1]==N and M[0]==D
log.append('27 Hamiltonian weights enumerate to the transcribed scalar N,D; reflection invariant: exact integer equality.')
MM=update(M)
H=add(MM[1],scale(mul(U,MM[0]),-1))
P=add(N,scale(mul(U,D),-1))

# Independently transcribed Q coefficients; no read of reproduced-algebra.
A=poly([(1,6,0,0),(2,4,2,0),(2,3,1,0),(1,2,0,0),(2,1,1,0),(1,0,0,0)])
B=poly([(2,7,1,0),(4,5,3,0),(2,5,1,0),(6,4,2,0),
        (4,3,3,0),(-1,4,0,0),(2,3,1,0),(10,2,2,0),(6,1,1,0),(1,0,0,0)])
C=poly([(1,8,0,0),(4,6,2,0),(4,4,4,0),(4,5,1,0),(8,3,3,0),
        (2,4,0,0),(6,2,2,0),(2,2,0,0),(4,1,1,0),(1,0,0,0)])
Q=add(mul(A,power(U,2)),mul(B,U),C)
assert H==mul(P,Q)
log.append(f'Full two-generation numerator H=P*Q: exact equality of all {len(H)} nonzero integer coefficients; no division by fixed-point P.')
assert all(c>0 for c in MM[0].values())
log.append(f'Actual two-generation denominator has {len(MM[0])} positive monomials; no pole on t,h,u>0.')

# Clear factor 4 to perform square verification wholly over integers:
# 4Q = t^2(2t^2u-1)^2 + positive remainder.
inner=add(scale(mul(power(T,2),U),2),scale(ONE,-1))
sq=mul(power(T,2),power(inner,2))
fourR=add(scale(Q,4),scale(sq,-1))
assert len(fourR)==24 and fourR[(0,0,0)]==4
assert all(c>0 for c in fourR.values())
log.append('4Q-t^2(2t^2*u-1)^2: 24 positive integer coefficients, constant 4. Hence Q>1 for all t,h,u>0.')
for name,p in [('A-t^6',add(A,scale(power(T,6),-1))),
               ('C-t^8',add(C,scale(power(T,8),-1))),
               ('B-1+t^4',add(B,scale(ONE,-1),power(T,4)))]:
    assert all(c>0 for c in p.values())
    log.append(name+': all coefficients positive, supporting the strict B<0 discriminant bounds.')
log.append('Coverage: every coefficient in Z[t,h,u]; no sampling, truncated expansion, numerical tolerance, or CAS is used.')
log.append('Method: raw Hamiltonian reconstruction and integer sparse-polynomial arithmetic; no cached scientific files are read.')
(OUT/'integer-check.log').write_text('\n'.join(log)+'\n')
record={'status':'pass','arithmetic':'Python integer sparse-polynomial arithmetic',
        'weights':len(weights),'two_generation_numerator_terms':len(H),
        'positive_denominator_terms':len(MM[0]),'positive_remainder_terms':len(fourR),
        'four_times_remainder':[{'exponents_t_h_u':list(e),'coefficient':c} for e,c in sorted(fourR.items())],
        'reads_cached_scientific_files':False,
        'scope':'Exact polynomial identities; no empirical or unrestricted Gibbs-phase claim'}
(OUT/'integer-check.json').write_text(json.dumps(record,indent=2)+'\n')
print('\n'.join(log))
