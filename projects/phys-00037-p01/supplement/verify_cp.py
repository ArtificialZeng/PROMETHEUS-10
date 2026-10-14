"""CP-factor replay of the three-mode entropy certificate.

Portable adaptation of the previously audited calculation, not a new referee
acceptance. Rebuilds matrix entries and rational coefficients before comparing
with the supplied witness. Numerical diagnostics are not the sign proof.
"""
from __future__ import annotations
import hashlib
import itertools as it
import json
import math
import platform
import time
from fractions import Fraction
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
import sympy as s

BEGIN = time.monotonic()
PREFIX = _OUTPUT / 'cp-check'
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
def tensor(matrices):
    out=s.ones(1,1)
    for matrix in matrices: out=s.kronecker_product(out,matrix)
    return out

def reconstruct(n):
    majoranas=[]
    for j in range(n):
        majoranas += [tensor([Z]*j+[M]+[I]*(n-j-1)) for M in (X,Y)]
    parity=(-s.I)**n*s.prod(majoranas)
    assert parity==tensor([Z]*n)
    kraus=[s.I*parity*c for c in majoranas]
    for k in kraus: assert k==k.conjugate().T and k*k==s.eye(2**n)
    for p,c in enumerate(majoranas):
        for q,k in enumerate(kraus):
            assert k*c*k == (-1 if p==q else 1)*c
    return majoranas,kraus

cs,ks=reconstruct(3)
U=tensor([X+Z]*3)/s.sqrt(8)
ksx=[s.simplify(U*k*U) for k in ks]
atten=s.symbols('a:6',real=True)
def exact_map(M):
    out=M
    for b,k in zip(atten,ksx):
        out=((1+b)*out+(1-b)*k*out*k)/2
        out=out.applyfunc(s.expand)
    return out

e0=s.eye(8)[:,0]; en=s.eye(8)[:,5]
out0=exact_map(e0*e0.T)
outn=exact_map(en*en.T)
outcoh=exact_map(en*e0.T)
forms=[]
for j in range(8):
    ss=tuple(1-2*((j>>(2-k))&1) for k in range(3))
    t=(ss[0],ss[0]*ss[1],ss[1]*ss[2])
    a,b,c,d,e,f=atten
    lam=s.prod(1+v*sign for v,sign in zip((a,b*c,d*e),t))/8
    amp=t[2]*f*(a+t[0])*(b+t[1]*c)*(d+t[2]*e)/8
    for i in range(8):
        assert s.expand(out0[i,j]-(lam if i==j else 0))==0
        assert s.expand(outn[i,j]-(lam.subs({a:-a,b:-b,d:-d},simultaneous=True) if i==j else 0))==0
        assert s.expand(outcoh[i,j]-(amp if i==j^5 else 0))==0
    forms.append({'X_basis_index':j,'t':t,'lambda':str(s.factor(lam)),'normal_coherence':str(s.factor(amp))})
print('Exact CP-factor output and coherence identities: 192 entries passed.',flush=True)

# Phase ordering and the common pair product, checked as exact identities from
# the independently reconstructed channel matrices.
a,b,c,d,e,f=atten
pair_product=(1-a*a)*(1-b*b*c*c)*(1-d*d*e*e)/64
coherence_product=f*f*(1-a*a)*(b*b-c*c)*(d*d-e*e)/64
for j in range(8):
    k=j^5
    assert s.expand(out0[j,j]*out0[k,k]-pair_product)==0
    assert s.expand(outcoh[k,j]*outcoh[j,k]-coherence_product)==0
print('Exact common spectral product and real/imaginary phase-ordering products: 16 identities passed.',flush=True)

# Each Gaussian generator produces one X-flip pattern (or a phase).
generators=cs+[s.I*cs[p]*cs[q] for p in range(6) for q in range(p+1,6)]
columns=[]; supports=set()
for G in generators:
    v=s.Matrix(U*s.I*G*U*e0)
    v[0]=0
    positions=[q for q in range(1,8) if v[q]!=0]
    assert len(positions)<=1
    supports.update(positions)
    columns.append(s.Matrix([s.re(z) for z in v[1:]]+[s.im(z) for z in v[1:]]))
rank=s.Matrix.hstack(*columns).rank()
assert rank==12 and supports=={1,2,3,4,6,7}

# Verify Pauli flip-support selection for every matrix unit, exactly and for all b.
selection=0
for k in ksx:
    permutation=[]
    for q in range(8):
        positions=[p for p in range(8) if k[p,q]!=0]
        assert len(positions)==1
        permutation.append(positions[0])
    for p,q in it.product(range(8),repeat=2):
        assert permutation[p]^permutation[q]==p^q
        selection+=1
print('Gaussian tangent rank 12; missing pattern 101; 384 support identities passed.',flush=True)

# Build the four resolvent summands from CP-derived matrix entries, rather than
# transcribing W,D,V. F is included in the squared coherence amplitude.
pairs=[(j,j^5) for j in range(4)]
W=[]; energy=[]
for j,k in pairs:
    W.append(s.expand(4*(out0[j,j]+out0[k,k])))
    gap=4*(out0[j,j]-out0[k,k])
    coh=4*(outcoh[j,k]+outcoh[k,j])
    energy.append(s.expand(gap*gap-coh*coh))
z=s.Symbol('z')
numerator=s.Poly(s.expand(sum(energy[i]*s.prod(1+z*W[j] for j in range(4) if j!=i) for i in range(4))),z)
assert numerator.degree()==3

certificate=json.loads((_HERE / 'certificate.json').read_text())
cert_by_k={r['k']:r for r in certificate['records']}
assert set(cert_by_k)==set(range(4))
certificate_results=[]
for order in range(4):
    original=s.Poly(numerator.nth(order),*atten)
    assert all(all(e%2==0 for e in powers) for powers in original.monoms())
    power={}
    for powers,co in original.terms():
        half=[v//2 for v in powers]
        half[4]+=half.pop()  # f^2=e^2 worst-case boundary
        exponents=tuple(sum(half[q:]) for q in range(5))
        power[exponents]=power.get(exponents,0)+int(co)
    power={e:c for e,c in power.items() if c}
    degrees=tuple(max(e[q] for e in power) for q in range(5))
    shape=tuple(n+1 for n in degrees)
    # Exact Fraction basis conversion by univariate line prefix summation.
    # beta_i=sum_{j<=i} binom(i,j)/binom(n,j) power_j.
    values={e:Fraction(c) for e,c in power.items()}
    for axis,n in enumerate(degrees):
        new={}
        for index in it.product(*(range(x) for x in shape)):
            total=Fraction(0)
            for j in range(index[axis]+1):
                source=list(index);source[axis]=j
                total += values.get(tuple(source),0)*Fraction(math.comb(index[axis],j),math.comb(n,j))
            if total: new[index]=total
        values=new
    rec=cert_by_k[order]
    assert tuple(rec['ratio_degrees'])==degrees
    proposed=[Fraction(int(v),int(rec['common_denominator'])) for v in rec['all_scaled_coefficients']]
    fresh=[values.get(index,Fraction(0)) for index in it.product(*(range(x) for x in shape))]
    assert len(proposed)==math.prod(shape)==len(fresh)
    assert fresh==proposed and min(fresh)>=0
    if order==0:
        strict_values=[v for index,v in values.items() if index[0]==1]
        assert len(strict_values)==math.prod(shape[1:]) and set(strict_values)=={Fraction(4,5)}
    certificate_results.append({'order':order,'degrees':degrees,'coefficients':len(fresh),'nonnegative':True,
        'zero_count':fresh.count(0),'matches_frozen_certificate':True,'fresh_power_terms':len(power)})
    print('Fresh rational Bernstein expansion',certificate_results[-1],flush=True)

# Independent finite-point diagnostics: monomial action, not the CP-factor route.
# The all-parameter proof above is exact; these are deliberately just diagnostics.
csn=[np.array(c,dtype=complex) for c in cs]
un=np.array(U,dtype=complex)
monomials=[]
for mask in range(64):
    M=np.eye(8,dtype=complex)
    for q in range(6):
        if mask>>q&1:M=M@csn[q]
    monomials.append(M)
def nmap(M,bs):
    out=np.zeros((8,8),complex)
    for mask,Q in enumerate(monomials):
        weight=math.prod(bs[p] for p in range(6) if mask>>p&1)
        out+=weight*np.vdot(Q,M)/8*Q
    return out
def divided_log(x,y):
    if x==y:return 1/x
    return math.log1p((x-y)/y)/(x-y) if abs(x-y)<.5*y else (math.log(x)-math.log(y))/(x-y)
g=un[:,0]; rho=np.outer(g,g)
directions=[phase*un[:,q] for q in range(1,8) for phase in (1,1j)]
rng=np.random.default_rng(590417)
points=[[0]*6,[.35,0,0,0,0,0],[.61]*6,[.92,.92,.5,.5,0,0],[.9999,.999,.97,.8,.7,.6]]
points += [sorted(rng.uniform(.001,.995,6),reverse=True) for _ in range(24)]
diagnostics=[]
for bs in points:
    output=un.conj().T@nmap(rho,bs)@un
    lam=np.diag(output).real
    assert min(lam)>0 and np.max(np.abs(output-np.diag(lam)))<1e-12
    L=np.array([[divided_log(x,y) for y in lam] for x in lam])
    first=[]; grad=[]
    for v in directions:
        M=un.conj().T@nmap(np.outer(v,g.conj())+np.outer(g,v.conj()),bs)@un
        first.append(M); grad.append(-np.dot(np.diag(M).real,np.log(lam))/math.log(2))
    H=np.empty((14,14))
    for p,v in enumerate(directions):
        for q,w in enumerate(directions):
            mixed=np.outer(v,w.conj())+np.outer(w,v.conj())-2*np.vdot(v,w).real*rho
            density2=un.conj().T@nmap(mixed,bs)@un
            H[p,q]=(-np.dot(np.diag(density2).real,np.log(lam))-np.sum(first[p].conj()*first[q]*L).real)/math.log(2)
    normal=np.diag(H)[8:10]
    lower=2*bs[0]**2*(1-bs[0]**2)**4/(65*math.log(2))
    gauss=[q for q in range(14) if q not in (8,9)]
    minimum=float(np.linalg.eigvalsh((H+H.T)/2)[0])
    cross=float(np.max(np.abs(H[np.ix_([8,9],gauss)])))
    assert minimum>=-1e-9 and normal[0]>=lower-1e-9 and normal[1]>=normal[0]-1e-9
    assert max(map(abs,grad))<1e-10 and cross<1e-10
    diagnostics.append({'b':bs,'minimum_output_eigenvalue':float(min(lam)),'minimum_hessian_eigenvalue':minimum,
        'normal_eigenvalues':normal.tolist(),'lower_bound':lower,'max_gradient':max(map(abs,grad)),'max_cross':cross})

# Known source n=1/2 spectra reconstructed again from CP factors.
baselines=[]
for n,bs,expected in [(1,[s.Rational(4,5),s.Rational(3,5)],[s.Rational(1,10),s.Rational(9,10)]),
    (2,[s.Rational(4,5),s.Rational(3,5),s.Rational(2,5),s.Rational(1,5)],
     [s.Rational(v,500) for v in (19,31,171,279)])]:
    _,klist=reconstruct(n)
    v=s.ones(2**n,1)/s.sqrt(2**n); out=v*v.T
    for bp,k in zip(bs,klist): out=((1+bp)*out+(1-bp)*k*out*k)/2
    spectrum=sorted([ev for ev,count in out.eigenvals().items() for _ in range(count)])
    assert spectrum==expected
    baselines.append({'n':n,'spectrum':[str(v) for v in spectrum]})

record={'implementation':'CP-factor replay','status':'pass',
    'exact_source_matrix_identities':192,'spectral_and_phase_product_identities':16,'Gaussian_tangent_real_rank':rank,'Gaussian_patterns':sorted(supports),
    'flip_support_identities':selection,'certificate':certificate_results,'baselines':baselines,
    'numerical_diagnostics':diagnostics,'output_forms':forms,
    'independence':'Fresh CP-factor symbolic reconstruction from primary Eqs.(3),(9),(10); polynomial assembled from resulting matrix entries; new Fraction Bernstein expansion. Numeric Hessian uses the other, full Clifford-monomial channel. No proposer module or polynomial cache loaded; only frozen Bernstein witness compared after recomputation.',
    'limitations':'Numeric diagnostics do not replace exact proof. Global minimum, higher modes, b1=1 and priority are not certified by this replay.',
    'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':s.__version__},'elapsed_seconds':time.monotonic()-BEGIN}
PREFIX.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('numerical_diagnostics','output_forms')},indent=2))
