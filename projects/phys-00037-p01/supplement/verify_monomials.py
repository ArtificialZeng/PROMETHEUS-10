"""Independent exact replay: source JW matrices and inverse Bernstein transform.

Does not import the proposer generator or read its symbolic-polynomial cache.
The sparse polynomial numerator is rebuilt by integer dictionary convolution.
"""
from __future__ import annotations
import itertools,json,math,platform,time
from pathlib import Path

import argparse
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--output-dir', type=Path, required=True)
_args = _parser.parse_args()
_OUTPUT = _args.output_dir.resolve()
_HERE = Path(__file__).resolve().parent
if _OUTPUT == _HERE or _HERE in _OUTPUT.parents:
    raise ValueError('Select an output directory outside the source supplement directory')
_OUTPUT.mkdir(parents=True, exist_ok=True)
if not __debug__:
    raise RuntimeError('Exact assertions require Python without -O')
import numpy as np
import sympy as sp

START=time.monotonic()
OUT=_OUTPUT / 'monomial-check.json'
a,b,c,d,e,f=sp.symbols('a b c d e f',real=True)
bs=(a,b,c,d,e,f)
I=sp.eye(2);X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1)
def kron(xs):
    out=sp.Matrix([[1]])
    for x in xs:out=sp.kronecker_product(out,x)
    return out
cs=[]
for j in range(3):cs.extend([kron([Z]*j+[X]+[I]*(2-j)),kron([Z]*j+[Y]+[I]*(2-j))])
monos=[]
for mask in range(64):
    M=sp.eye(8);w=sp.Integer(1)
    for j in range(6):
        if mask>>j&1:M=M*cs[j];w*=bs[j]
    monos.append((M,w))
def channel(M):
    out=sp.zeros(8)
    for basis,w in monos:
        coefficient=sp.trace(basis.conjugate().T*M)/8
        if coefficient:out+=coefficient*w*basis
    return out
H=kron([X+Z]*3)/sp.sqrt(8)
g=H[:,0];chi=H[:,5]
sigma=H.T*channel(g*g.T)*H
coherence=H.T*channel(chi*g.T)*H
other=H.T*channel(chi*chi.T)*H
source_checks=0
for q in range(8):
    ss=tuple(1-2*((q>>(2-j))&1) for j in range(3))
    tt=(ss[0],ss[0]*ss[1],ss[1]*ss[2])
    lam=sp.prod(1+ri*ti for ri,ti in zip((a,b*c,d*e),tt))/8
    lamm=sp.prod(1-ri*ti for ri,ti in zip((a,b*c,d*e),tt))/8
    amp=tt[2]*f*(a+tt[0])*(b+tt[1]*c)*(d+tt[2]*e)/8
    for p in range(8):
        assert sp.expand(sigma[p,q]-(lam if p==q else 0))==0
        assert sp.expand(other[p,q]-(lamm if p==q else 0))==0
        assert sp.expand(coherence[p,q]-(amp if p==q^5 else 0))==0
        source_checks+=3
generators=cs+[sp.I*cs[p]*cs[q] for p in range(6) for q in range(p+1,6)]
tangent=[];patterns=set()
for G in generators:
    v=sp.Matrix(H.T*(sp.I*G*g))
    v[0]=0
    support=[q for q in range(1,8) if v[q]!=0]
    assert len(support)<=1
    patterns.update(support)
    tangent.append(sp.Matrix([sp.re(v[q]) for q in range(1,8)]+[sp.im(v[q]) for q in range(1,8)]))
rank=sp.Matrix.hstack(*tangent).rank()
assert rank==12 and patterns=={1,2,3,4,6,7}

# Completely separate sparse-integer polynomial implementation.
ZERO=(0,)*6
def add(p,q):
    ans=dict(p)
    for k,v in q.items():ans[k]=ans.get(k,0)+v
    return {k:v for k,v in ans.items() if v}
def scale(p,n):return {k:n*v for k,v in p.items() if n*v}
def mul(p,q):
    ans={}
    for i,v in p.items():
        for j,w in q.items():
            k=tuple(ii+jj for ii,jj in zip(i,j));ans[k]=ans.get(k,0)+v*w
    return {k:v for k,v in ans.items() if v}
def mono(indices,n=1):
    powers=[0]*6
    for index in indices:powers[index]+=1
    return {tuple(powers):n}
one={ZERO:1}
rows=[]
for t2,t3 in itertools.product((1,-1),repeat=2):
    W=add(add(add(one,mono([0,1,2],t2)),mono([0,3,4],t3)),mono([1,2,3,4],t2*t3))
    Dp=add(add(add(mono([0]),mono([1,2],t2)),mono([3,4],t3)),mono([0,1,2,3,4],t2*t3))
    Fp=add(add(add(mono([5,1,3]),mono([5,2,4],t2*t3)),mono([5,0,2,3],t2)),mono([5,0,1,4],t3))
    rows.append((W,add(mul(Dp,Dp),scale(mul(Fp,Fp),-1))))
cert=json.loads((_HERE / 'certificate.json').read_text())
checks=[]
for rec in cert['records']:
    k=rec['k'];target={}
    for i,(_,Pi) in enumerate(rows):
        for subset in itertools.combinations([j for j in range(4) if j!=i],k):
            term=Pi
            for j in subset:term=mul(term,rows[j][0])
            target=add(target,term)
    ratio={}
    for powers,co in target.items():
        assert all(n%2==0 for n in powers)
        aa,bb,cc,dd,ee,ff=(n//2 for n in powers)
        pp=(aa,bb,cc,dd,ee+ff)
        rr=tuple(sum(pp[j:]) for j in range(5))
        ratio[rr]=ratio.get(rr,0)+co
    ratio={p:co for p,co in ratio.items() if co}
    deg=rec['ratio_degrees'];shape=tuple(n+1 for n in deg)
    assert tuple(deg)==tuple(max(p[j] for p in ratio) for j in range(5))
    assert all(all(p[j]<=deg[j] for j in range(5)) for p in ratio)
    integers=[int(v) for v in rec['all_scaled_coefficients']]
    assert len(integers)==math.prod(shape) and min(integers)>=0
    denom=int(rec['common_denominator'])
    arr=np.array(integers,dtype=object).reshape(shape)
    strict_slice=None
    if k==0:
        strict_slice=[int(v) for v in arr[1].flat]
        assert min(strict_slice)==max(strict_slice)==4*denom//5
    # c_j = binom(n,j) Delta^j beta_0; verify against the fresh numerator.
    for axis,n in enumerate(deg):
        T=np.array([[((-1)**(i-j))*math.comb(i,j)*math.comb(n,i) if j<=i else 0
                     for j in range(n+1)] for i in range(n+1)],dtype=object)
        arr=np.moveaxis(arr,axis,0);sh=arr.shape
        arr=(T@arr.reshape(n+1,-1)).reshape(sh);arr=np.moveaxis(arr,0,axis)
    checked=0
    for p in np.ndindex(shape):
        assert int(arr[p])==denom*ratio.get(p,0)
        checked+=1
    checks.append({'k':k,'identity_coefficients_checked':checked,'all_bernstein_coefficients_nonnegative':True,
                   'denominator':str(denom),'strict_N0_A_index1_value':'4/5' if k==0 else None})
result={'status':'pass','implementation':'full Majorana monomial replay',
        'scope':'exact input identities, tangent split, four all-chamber polynomial positivity certificates; proposer replay, not fresh referee acceptance',
        'source_matrix_identities_checked':source_checks,'gaussian_tangent_real_rank':rank,
        'gaussian_nonzero_X_flip_patterns':[format(q,'03b') for q in sorted(patterns)],
        'normal_X_flip_pattern':'101','certificate_replay':checks,
        'independence':'JW/Clifford symbolic full-matrix source reconstruction plus sparse integer dictionary convolution and inverse finite-difference Bernstein identity; no imports of proposer generator and no reads of symbolic-polynomial cache. Shared source, derived formula and same agent.',
        'environment':{'python':platform.python_version(),'sympy':sp.__version__,'numpy':np.__version__},
        'elapsed_seconds':time.monotonic()-START,
        'limitations':'Finite exact algebra proves this specified certificate when combined with the stable resolvent derivation. It does not establish global minimum output entropy, higher n, rank-singular b1=1 behavior, novelty, or independent referee acceptance.'}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
