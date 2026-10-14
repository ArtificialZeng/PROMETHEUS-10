"""Exact proposer checks. No solver output is used to prove a PSD assertion.
All zero tests are symbolic with A=1-3B. PSD is established by explicit
projectors/factorizations and the physical 2x2 principal minors.
"""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
B,Q,r=s.symbols('B Q r', real=True)
A=1-3*B
I4=s.eye(4)
def E(a,b):
    m=s.zeros(4);m[a,b]=1;return m
P0=E(0,0);P1=I4-P0
F=[E(0,i)+E(i,0) for i in range(1,4)]
g0=A*P0+B*P1;g=[Q*f for f in F]
records=[]
def zero(name,m):
    m=s.Matrix(m)
    residuals=[s.simplify(v) for v in m]
    failures=[{'index':k,'residual':str(v)} for k,v in enumerate(residuals) if v!=0]
    rec={'check':name,'entries':len(residuals),'zero_entries':len(residuals)-len(failures),'failures':failures}
    records.append(rec)
    assert not failures, rec
    print(json.dumps({k:v for k,v in rec.items() if k!='failures'}),flush=True)

# Independent physical construction from the Pauli matrices, no source spin columns.
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
bell=s.Matrix([1,0,0,1])/s.sqrt(2)
T=s.Matrix.hstack(bell,*[-s.I*s.kronecker_product(p,s.eye(2))*bell for p in pauli])
zero('Pauli-built real-star basis orthonormality',T.H*T-I4)
signs=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
e=[s.Matrix([1,*v])/2 for v in signs]
physical=[]
unitaries=[]
for j,v in enumerate(signs):
    u=(s.eye(2)-s.I*sum((v[i]*pauli[i] for i in range(3)),s.zeros(2)))/2
    unitaries.append(u)
    zero(f'tetrahedral physical unitary {j}',u.H*u-s.eye(2))
    physical.append(s.kronecker_product(u,s.eye(2))*bell)
    zero(f'computational measurement-vector map {j}',physical[-1]-T*e[j])
measurement_basis=s.Matrix.hstack(*physical)
for j,target in enumerate([s.eye(2),s.I*pauli[1],s.I*pauli[2],s.I*pauli[0]]):
    zero(f'fixed rotation then Bell measurement identity {j}',unitaries[0].H*unitaries[j]-target)
zero('computational PVM basis orthonormality',measurement_basis.H*measurement_basis-I4)
M=[v*v.T for v in e]
zero('PVM normalization',sum(M,s.zeros(4))-I4)
for j,v in enumerate(signs):
    zero(f'outcome {j} probability',[s.trace(g0*M[j])-s.Rational(1,4)])
    for i in range(3):
        zero(f'outcome {j} first moment {i}',[s.trace(g[i]*M[j])-Q*v[i]/2])

# Physical risk certificate over all real estimates, not a grid.
D=-12*B*Q**2*P0-s.Rational(4,3)*A*Q**2*P1
slack=(r**2*g0-2*r*g[2])/3-D
block=slack.extract([0,3],[0,3])
zero('physical dual determinant factorization',[block.det()-A*B*(r**2-12*Q**2)**2/9])
zero('physical dual trace',[(s.trace(D)+4*Q**2)])
for j,v in enumerate(signs):
    t=s.Matrix(v)*2*Q
    sj=(s.expand(t.dot(t))*g0-2*sum((t[i]*g[i] for i in range(3)),s.zeros(4)))/3-D
    zero(f'physical complementary slackness {j}',sj*e[j])

# Parameter tensor spin-one projectors (ordering i,a).
omega=s.zeros(9,1)
swap=s.zeros(9)
for i in range(3):
    omega[3*i+i]=1
    for a in range(3):swap[3*i+a,3*a+i]=1
Ptr=omega*omega.T/3
Pas=(s.eye(9)-swap)/2
Pst=(s.eye(9)+swap)/2-Ptr
for name,p in [('trace',Ptr),('antisymmetric',Pas),('symmetric_traceless',Pst)]:
    zero(f'{name} projector idempotence',p*p-p)
    zero(f'{name} projector symmetry',p.T-p)
zero('projector orthogonality',Ptr*Pas+Ptr*Pst+Pas*Pst)
zero('projector completeness',Ptr+Pas+Pst-s.eye(9))
embed=s.zeros(12,9)
for i in range(3):
    for a in range(3):embed[4*i+a+1,3*i+a]=1
scalar=s.kronecker_product(s.eye(3),P0)
K=s.BlockMatrix([[(A*s.KroneckerDelta(i,j)*P0+B*(s.KroneckerDelta(i,j)*P1+E(i,j)-E(j,i)))/3 for j in range(1,4)] for i in range(1,4)]).as_explicit()
Kfac=A*scalar/3+embed*(B*Ptr+2*B*Pas/3)*embed.T
zero('NH K positive-projector decomposition',K-Kfac)
X=[2*Q*f for f in F]
stack=s.Matrix.vstack(*X)
factor=s.Matrix.vstack(s.eye(12),-stack.T)
Z=factor*K*factor.T
for i in range(3):
    si=slice(4*i,4*i+4)
    zero(f'NH dual diagonal {i}',Z[si,si]-g0/3)
    zero(f'NH dual first-moment equality {i}',Z[si,12:16]+Z[12:16,si]+2*g[i]/3)
    for j in range(i+1,3):
        sj=slice(4*j,4*j+4)
        zero(f'NH dual off-diagonal Hermitian-sum {i},{j}',Z[si,sj]+Z[sj,si])
zero('NH dual objective',[s.trace(Z[12:16,12:16])-4*Q**2])
zero('NH dual bottom formula',Z[12:16,12:16]-4*Q**2*(3*B*P0+A*P1/3))

# Sphere primal and its exact PSD complement.
L=[[(4*Q**2*s.KroneckerDelta(i,j)*P0+s.Rational(12,5)*Q**2*(s.KroneckerDelta(i,j)*P1+E(i,j)+E(j,i))) for j in range(1,4)] for i in range(1,4)]
Lb=s.BlockMatrix(L).as_explicit()
zero('NH sphere Schur PSD projector factorization',Lb-stack*stack.T-s.Rational(24,5)*Q**2*embed*Pst*embed.T)
objective=sum((s.trace(g0*L[i][i])-2*s.trace(g[i]*X[i]) for i in range(3)),s.S.Zero)/3
zero('NH sphere primal objective',[objective+4*Q**2])
schur=s.BlockMatrix([[Lb,stack],[stack.T,I4]]).as_explicit()
zero('NH primal-dual complementarity',Z*schur)

# The finite PVM's moment pair is separately checked; its second moments
# need not equal the rotationally averaged second moments.
tx=[sum((2*Q*signs[j][i]*M[j] for j in range(4)),s.zeros(4)) for i in range(3)]
for i in range(3):
    other=[j for j in range(1,4) if j!=i+1]
    zero(f'finite first-moment commuting completion {i}',tx[i]-2*Q*(F[i]+E(*other)+E(*reversed(other))))
    zero(f'finite first-moment square {i}',tx[i]*tx[i]-4*Q**2*I4)
    for j in range(i+1,3):zero(f'finite first-moment commutator {i},{j}',tx[i]*tx[j]-tx[j]*tx[i])
tl=[[sum((4*Q**2*signs[k][i]*signs[k][j]*M[k] for k in range(4)),s.zeros(4)) for j in range(3)] for i in range(3)]
ts=s.Matrix.vstack(*tx)
tb=s.BlockMatrix([[s.BlockMatrix(tl).as_explicit(),ts],[ts.T,I4]]).as_explicit()
gram=s.zeros(16)
for j in range(4):
    v=s.Matrix.vstack(*[2*Q*signs[j][i]*I4 for i in range(3)],I4)
    gram+=v*M[j]*v.T
zero('finite PVM NH Schur Gram factorization',tb-gram)
zero('finite PVM NH objective',[sum((s.trace(g0*tl[i][i])-2*s.trace(g[i]*tx[i]) for i in range(3)),s.S.Zero)/3+4*Q**2])
zero('finite PVM NH complementarity',Z*tb)

rec={'job_id':'phys-00014-p01-research-f15bfc274f9b','mode':'exact','symbols':'B,Q,r real; A=1-3B; physical inputs require A>0,B>0. All checks include Q=0.','zero_checks':records,'checked_entries':sum(v['entries'] for v in records),'failure_count':sum(len(v['failures']) for v in records),'psd_argument':'NH dual has Z=F K F^T and K is a nonnegative combination of orthogonal projectors for A,B>0. Sphere primal Schur complement is (24Q^2/5) times a projector. Finite primal is a sum of Gram matrices. Physical dual slack has nonnegative diagonal entries and determinant AB(r^2-12Q^2)^2/9 for all r>=0. These algebraic arguments, not sampled eigenvalues, establish PSD.','scope':'Proposer exact checks for k=1 star moments; no independent referee or k>1 conclusion.'}
(OUT/'exact-certificates.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps({k:v for k,v in rec.items() if k!='zero_checks'},indent=2))
