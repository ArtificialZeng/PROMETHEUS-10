"""Compare separate source reconstructions and certify known SDP benchmarks.
All matrix operations, PSD tests and objectives use Fraction, not float.
"""
import json, hashlib, math
from fractions import Fraction as F
from pathlib import Path

def parse(rows): return [[F(z) for z in row] for row in rows]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def scale(a,c): return [[c*z for z in row] for row in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def trace(a): return sum(a[i][i] for i in range(len(a)))
def kron(a,b): return [[x*y for x in r for y in s] for r in a for s in b]
def ptr_x(a): return [[sum(a[4*x+i][4*x+j] for x in range(4)) for j in range(4)] for i in range(4)]
def ptr_qubit(a,which):
    if which=='B': return [[sum(a[2*i+b][2*j+b] for b in range(2)) for j in range(2)] for i in range(2)]
    return [[sum(a[2*b+i][2*b+j] for b in range(2)) for j in range(2)] for i in range(2)]
def psd(a):
    # Exact Schur-complement elimination; a zero pivot must have zero row/column.
    a=[row[:] for row in a]
    n=len(a)
    assert a==list(map(list,zip(*a)))
    for k in range(n):
        pivot=a[k][k]
        if pivot<0: return False
        if pivot==0:
            if any(a[k][j]!=0 for j in range(k+1,n)): return False
        else:
            for i in range(k+1,n):
                for j in range(k+1,n): a[i][j]-=a[i][k]*a[k][j]/pivot
    return True

A=json.loads(Path('evidence/input-a.json').read_text())
B=json.loads(Path('evidence/input-b.json').read_text())
# New grouped index maps to old RA,RB,A,B index by swapping positions 2 and 3.
perm=[8*ra+4*rb+2*a+b for ra in (0,1) for a in (0,1) for rb in (0,1) for b in (0,1)]
comparison=['Exact basis permutation: new[RA,A,RB,B] -> old[RA,RB,A,B]',str(perm)]
baseline=[]
pure={}
for ca,cb in zip(A['cases'],B['cases']):
    assert (ca['gate'],ca['p'])==(cb['gate'],cb['p'])
    old=parse(ca['omega']); rho=parse(cb['omega'])
    assert all(rho[i][j]==old[perm[i]][perm[j]] for i in range(16) for j in range(16))
    assert trace(rho)==1 and psd(rho)
    # Full reference and full output marginals in original ordering.
    assert [[sum(old[4*r+o][4*s+o] for o in range(4)) for s in range(4)] for r in range(4)]==scale(eye(4),F(1,4))
    assert [[sum(old[4*r+o][4*r+v] for r in range(4)) for v in range(4)] for o in range(4)]==scale(eye(4),F(1,4))
    red=ptr_x(rho)
    assert ptr_qubit(red,'B')==scale(eye(2),F(1,2))
    assert ptr_qubit(red,'RB')==scale(eye(2),F(1,2))
    comparison.append(f"{ca['gate']} p={ca['p']}: 256/256 entries equal; PSD, trace, TP, unitality, both Y marginals PASS")
    if ca['p']=='0': pure[ca['gate']]=rho

for gate,k in (('identity',1),('CNOT',2),('SWAP',4)):
    P=pure[gate]; Pi=scale(ptr_x(P),F(k))
    assert mul(P,P)==P and mul(Pi,Pi)==Pi and trace(Pi)==k
    assert ptr_qubit(Pi,'B')==scale(eye(2),F(k,2))
    complement=add(eye(4),scale(Pi,F(-1)))
    # Dual trace constraint is exactly I_Y.
    W=add(scale(P,F(k)),kron(scale(eye(4),F(1,4)),complement))
    assert psd(W) and ptr_x(W)==eye(4)
    for p in (F(0),F(1,2),F(1)):
        rho=next(parse(c['omega']) for c in B['cases'] if c['gate']==gate and F(c['p'])==p)
        Q=add(scale(Pi,1-p),scale(eye(4),p/16))
        slack=add(kron(eye(4),Q),scale(rho,F(-1)))
        assert psd(Q) and psd(slack)
        assert ptr_qubit(Q,'B')==scale(eye(2),trace(Q)/2)
        primal=trace(Q); dual=trace(mul(rho,W))
        assert primal==dual==k*(1-p)+p/4
        # Eq.87: Gamma=4rho, M=4Q, objective Tr M/2 = 2t.
        M=scale(Q,F(4)); Gamma=scale(rho,F(4))
        assert psd(add(kron(eye(4),M),scale(Gamma,F(-1))))
        assert trace(M)/2==2*primal
        baseline.append({'gate':gate,'p':str(p),'rank':k,'s':str(primal),'t':str(primal),
            'state_bits':-math.log2(float(primal)),'channel_bits':-math.log2(float(primal))-1,
            'certificate':'exact primal/dual equality; Q obeys TP marginal; Eq87 normalization verified'})

# KRS2009 d=4 standard maximally entangled state, separate from SWAP conventions.
v=[F(i//4==i%4,2) for i in range(16)]
Phi=[[x*y for y in v] for x in v]
Q=eye(4); W=scale(Phi,F(4))
assert psd(add(kron(eye(4),Q),scale(Phi,F(-1))))
assert psd(W) and ptr_x(W)==eye(4) and trace(mul(Phi,W))==trace(Q)==4
mixed=scale(eye(16),F(1,16)); Q=scale(eye(4),F(1,16)); W=scale(eye(16),F(1,4))
assert kron(eye(4),Q)==mixed and ptr_x(W)==eye(4) and trace(mul(mixed,W))==trace(Q)==F(1,4)
baseline.extend([{'KRS2009':'Phi_4','s':'4','state_bits':-2},
                 {'KRS2009':'I_16/16','s':'1/4','state_bits':2}])
Path('evidence/input-comparison.log').write_text('\n'.join(comparison)+'\n')
Path('evidence/baseline.log').write_text(json.dumps({'arithmetic':'exact rational; logs in bits are display-only floats',
    'benchmarks':baseline,'scope':'Known three-gate benchmarks only; no all-U result'},indent=2)+'\n')
expected=json.loads(Path('input-manifest.json').read_text())['source_sha256']
actual=hashlib.sha256(Path('source.md').read_bytes()).hexdigest()
assert expected==actual
print('PASS: 3072 exact entry comparisons across 12 cases; all input marginals and positivity pass.')
print('PASS: 9 noisy gate primal/dual certificates and 2 KRS2009 published limit certificates.')
print('PASS: source.md SHA256 unchanged: '+actual)
