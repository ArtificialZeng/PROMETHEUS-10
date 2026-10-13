"""Exact n=3 no-purification witness on all four-qubit stabilizer rays.

Run from PROJECT_DIR: python3 research/exhaustive_certificate.py
No optimizer, sampling, subprocesses, or approximate arithmetic.
"""
from collections import Counter
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import platform
import time
import numpy as np
import sympy as S

START = time.monotonic()
t = S.Symbol('t', real=True)
N, D = 4, 16
alphabet = 'IXZY'
digits = [tuple((v >> (2*(N-1-k))) & 3 for k in range(N)) for v in range(256)]
local_phase = {(1,2):3,(2,1):1,(1,3):1,(3,1):3,(3,2):1,(2,3):3}


def commute(v, w):
    return sum((a&1)*(b>>1)+(a>>1)*(b&1)
               for a,b in zip(digits[v],digits[w])) % 2 == 0


def phase(v, w):
    return sum(local_phase.get((a,b),0) for a,b in zip(digits[v],digits[w])) % 4


def code(labels):
    out = 0
    for k in labels:
        out = (out << 2) | k
    return out


def unpack(record):
    return S.Matrix([[S.expand(sum(S.Rational(c)*(1-t)**k for k,c in enumerate(cell)))
                      for cell in row] for row in record['rows']])


def canonical_basis(space):
    basis, span = [], {0}
    for v in space:
        if v not in span:
            basis.append(v)
            span |= {v^w for w in tuple(span)}
    assert span == set(space)
    return basis


I = np.eye(2,dtype=np.int64)
X = np.array([[0,1],[1,0]],dtype=np.int64)
Z = np.diag(np.array([1,-1],dtype=np.int64))
zero = np.zeros((2,2),dtype=np.int64)
local = [(I,zero),(X,zero),(Z,zero),(zero,np.array([[0,-1],[1,0]],dtype=np.int64))]
paulis = []
for ds in digits:
    re, im = np.ones((1,1),dtype=np.int64), np.zeros((1,1),dtype=np.int64)
    for k in ds:
        r,j = local[k]
        re,im = np.kron(re,r)-np.kron(im,j),np.kron(re,j)+np.kron(im,r)
    paulis.append((re,im))

# A: input-input same-axis correlations. B: signed input-output correlations.
# C: fourth Bloch moment, with integer weights 3 (one axis) or 1 (two axes).
A, B, C = {}, {}, {}
for i,j in combinations(range(3),2):
    for a in [1,2,3]:
        ds=[0]*4; ds[i]=ds[j]=a
        A[code(ds)]=1
for i in range(3):
    for a in [1,2,3]:
        ds=[0]*4; ds[i]=ds[3]=a
        B[code(ds)]=-1 if a==3 else 1
for ds in product([1,2,3],repeat=4):
    ns=[ds.count(a) for a in [1,2,3]]
    if any(k%2 for k in ns):
        continue
    C[code(ds)]=(3 if 4 in ns else 1)*(-1)**ds[:3].count(3)


def matrix(terms):
    return sum((c*(S.Matrix(paulis[v][0])+S.I*S.Matrix(paulis[v][1]))
                for v,c in terms.items()),S.zeros(16))


am,bm,cm=matrix(A),matrix(B),matrix(C)
data=json.loads(Path('evidence/input-a.json').read_text())['cases']['3']
qt,rt=unpack(data['QT']),unpack(data['RT'])
h=(qt-(1+t)*rt/2).applyfunc(S.expand)
expected=t*(-15*S.eye(16)+5*bm+t*t*(cm-5*am))/240
assert all(S.expand(x)==0 for x in h-expected)
h1=h.subs(t,1)
linear=(bm-3*S.eye(16))/48
assert all(S.expand(x)==0 for x in h-t*((1-t*t)*linear+t*t*h1))
spectrum=h1.eigenvals()
assert all(v<=0 for v in spectrum)
print('Exact matrix identity H(t)=t[(1-t^2)(B-3I)/48+t^2 H(1)] verified in all 256 entries.',flush=True)
print('Exact H(1) spectrum: '+str(spectrum),flush=True)

# The zero subspace is extended by every commuting vector, one representative
# per coset. Induction proves every isotropic subspace occurs. Deduplication is
# by the entire vector space, not an arbitrary generator choice.
commuting=[sum(1<<w for w in range(256) if commute(v,w)) for v in range(256)]
spaces={(0,)}
levels=[1]
for dim in range(1,5):
    next_spaces=set()
    for space in sorted(spaces):
        mask=(1<<256)-1
        for v in canonical_basis(space):
            mask &= commuting[v]
        for v in space:
            mask &= ~(1<<v)
        while mask:
            bit=mask & -mask
            v=bit.bit_length()-1
            coset=tuple(v^w for w in space)
            next_spaces.add(tuple(sorted(space+coset)))
            for w in coset:
                mask &= ~(1<<w)
    spaces=next_spaces
    levels.append(len(spaces))
    print(f'Isotropic dimension {dim}: {len(spaces)} distinct complete spaces.',flush=True)
assert levels==[1,255,5355,11475,2295]

classes=Counter()
triples=Counter()
seen=set()
state_count=0
max_entry=0
outfile=Path('evidence/stabilizer4-rays.jsonl')
with outfile.open('w') as output:
    for space in sorted(spaces):
        basis=canonical_basis(space)
        assert len(basis)==4
        for signs in product([1,-1],repeat=4):
            group={0:1}
            for generator,sgn in zip(basis,signs):
                extra={}
                for v,sv in group.items():
                    p=phase(v,generator)
                    assert p in [0,2]
                    extra[v^generator]=sv*sgn*(-1 if p==2 else 1)
                assert not set(group)&set(extra)
                group.update(extra)
            support=tuple(sorted(group.items()))
            assert tuple(v for v,_ in support)==space
            assert support not in seen
            seen.add(support)
            # Exact rank-one checks with Gaussian integers M=16 phi.
            real=sum(sv*paulis[v][0] for v,sv in support)
            imag=sum(sv*paulis[v][1] for v,sv in support)
            assert np.array_equal(real,real.T) and np.array_equal(imag,-imag.T)
            assert np.trace(real)==16 and np.trace(imag)==0
            assert np.array_equal(real@real-imag@imag,16*real)
            assert np.array_equal(real@imag+imag@real,16*imag)
            max_entry=max(max_entry,int(np.max(np.abs(real))),int(np.max(np.abs(imag))))
            av=sum(c*group.get(v,0) for v,c in A.items())
            bv=sum(c*group.get(v,0) for v,c in B.items())
            cv=sum(c*group.get(v,0) for v,c in C.items())
            alpha,beta=5*bv-15,cv-5*av
            assert alpha<=0 and alpha+beta<=0
            classes[(alpha,beta)]+=1
            triples[(av,bv,cv)]+=1
            state_count+=1
            output.write(json.dumps({'id':state_count,'generators':basis,'eigenvalues':signs,
                'signed_pauli_support':support,'ABC':[av,bv,cv],
                'g_t_coefficients_over_240':[0,alpha,0,beta]},separators=(',',':'))+'\n')
assert state_count==36720

summary={
    'qubits':4,'source_input':'evidence/input-a.json','basis':'input1,input2,input3,output',
    'pauli_alphabet':alphabet,'pauli_integer_encoding':'big-endian 2 bits per qubit, I=0 X=1 Z=2 Y=3',
    'isotropic_subspace_counts':levels,'pure_stabilizer_rays':state_count,
    'enumeration_method':'All isotropic spaces by commuting-vector coset extension; all 16 eigenvalue choices per Lagrangian. Completeness is proved in research/proof.md.',
    'operator_identity':'H(t)=t*((1-t^2)*(B-3I)/48+t^2*H(1)), t=1-delta',
    'H1_spectrum':{str(k):int(v) for k,v in spectrum.items()},
    'ray_polynomial':'g_phi(t)=t*(alpha+beta*t^2)/240',
    'sign_certificate':'Every alpha<=0 and alpha+beta<=0; alpha+beta*t^2=(1-t^2)*alpha+t^2*(alpha+beta).',
    'classes':[{'alpha':a,'beta':b,'alpha_plus_beta':a+b,'count':count} for (a,b),count in sorted(classes.items())],
    'ABC_classes':[{'A':a,'B':b,'C':c,'count':count} for (a,b,c),count in sorted(triples.items())],
    'projector_checks':'All 36720 M=16phi satisfy exact Hermiticity, trace=16, M^2=16M, and unique signed Pauli support.',
    'arithmetic':'Python integers and rational polynomials; NumPy int64 only for 16x16 Gaussian integer projector checks.',
    'integer_bound':'Each M entry <=16. Each real or imaginary M^2 entry <=2*16*16^2=8192, safely below int64 range.',
    'maximum_observed_abs_real_or_imag_entry':max_entry,
    'raw_rays':str(outfile),'raw_rays_sha256':hashlib.sha256(outfile.read_bytes()).hexdigest(),
    'environment':{'python':platform.python_version(),'sympy':S.__version__,'numpy':np.__version__},
    'elapsed_seconds':time.monotonic()-START,
    'limitations':'Researcher-generated evidence, not fresh scientific review. No n>=4-input claim, Clifford implementation, or free failure completion.',
}
Path('evidence/stabilizer4-certificate.json').write_text(json.dumps(summary,indent=2)+'\n')
log=[f'Isotropic counts {levels}; complete rays {state_count}.',
     f'All 36720 exact Gaussian integer projector and sign checks passed; {len(classes)} different g polynomials.',
     f'Maximum B expectation {max(b for a,b,c in triples)}; zero polynomials {classes.get((0,0),0)}.',
     f'H(1) spectrum {spectrum}; exact polynomial identity checked.',
     f'Max absolute matrix entry {max_entry}; no tolerance or sampling.',
     f'Elapsed {summary["elapsed_seconds"]:.6f} seconds; Python {platform.python_version()}, SymPy {S.__version__}, NumPy {np.__version__}.']
Path('evidence/stabilizer4-certificate.log').write_text('\n'.join(log)+'\n')
print('\n'.join(log))
