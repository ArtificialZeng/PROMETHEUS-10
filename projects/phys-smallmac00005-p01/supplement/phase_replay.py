"""Fresh referee calculation. No imports of submitted code or cached operators.

Haar reconstruction uses u=|alpha|^2 uniform on [0,1] and a uniform relative
phase. Phase balance removes radicals; the remaining polynomial is integrated
term by term with exact rationals. This differs from both submitted input routes.
"""
from pathlib import Path
from itertools import product, permutations, combinations
from functools import lru_cache
import json, hashlib, datetime, platform, sys, time
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
t, u, s = S.symbols('t u s', real=True)
I = S.eye(2)
X = S.Matrix([[0,1],[1,0]])
Y = S.Matrix([[0,-S.I],[S.I,0]])
Z = S.diag(1,-1)
PAULI = [X,Y,Z]
records = []

def record(name, **data):
    entry = {'check':name, **data}
    records.append(entry)
    print(json.dumps(entry, ensure_ascii=False), flush=True)

def bits(i,n):
    return tuple((i >> (n-1-k)) & 1 for k in range(n))

def number(b):
    return sum(x << (len(b)-1-k) for k,x in enumerate(b))

def kron(items):
    out=S.ones(1)
    for a in items: out=S.kronecker_product(out,a)
    return out

def zero(M):
    return all(S.expand(x)==0 for x in M)

@lru_cache(None)
def phase_integral(noisy_00,noisy_11,noisy_off,clean_00,clean_11,clean_off,phase):
    if phase: return S.Integer(0)
    off = noisy_off+clean_off
    assert off%2==0
    expr = ((1-t)/2+t*u)**noisy_00 * ((1+t)/2-t*u)**noisy_11
    expr *= t**noisy_off * u**clean_00 * (1-u)**clean_11
    expr *= (u*(1-u))**(off//2)
    p = S.Poly(S.expand(expr),u)
    return S.expand(sum(c/S.Integer(e[0]+1) for e,c in p.terms()))

def haar(n, fidelity, transpose):
    dim=2**(n+1)
    result=S.zeros(dim)
    for row,col in product(range(dim),repeat=2):
        br,bc=bits(row,n+1),bits(col,n+1)
        if not fidelity and br[-1]!=bc[-1]: continue
        c=[0]*6
        phase=0
        for k in range(n+int(fidelity)):
            a,b=br[k],bc[k]
            if k<n and transpose: a,b=b,a
            offset=0 if k<n else 3
            if a==b: c[offset+a]+=1
            else:
                c[offset+2]+=1
                phase+=a-b
        result[row,col]=phase_integral(*c,phase)
    return result

def symmetrizer(m):
    out=S.zeros(2**m)
    for p in permutations(range(m)):
        for col in range(2**m):
            b=bits(col,m)
            out[number(tuple(b[k] for k in p)),col]+=1
    return out/S.factorial(m)

def depolarize(M,qubit,m):
    out=S.zeros(2**m)
    for row,col in product(range(2**m),repeat=2):
        br,bc=list(bits(row,m)),list(bits(col,m))
        replacement=0
        if br[qubit]==bc[qubit]:
            for b in range(2):
                rr,cc=br.copy(),bc.copy()
                rr[qubit]=cc[qubit]=b
                replacement+=M[number(rr),number(cc)]/2
        out[row,col]=S.expand(t*M[row,col]+(1-t)*replacement)
    return out

def partial_transpose(M,n):
    return S.Matrix(2**(n+1),2**(n+1),
        lambda r,c: M[2*(c//2)+(r%2),2*(r//2)+(c%2)])

def star(n):
    ops=[]
    for edge in range(n):
        for axis,P in enumerate(PAULI):
            f=[I]*(n+1)
            f[edge]=P; f[-1]=P
            ops.append((edge,axis,kron(f)))
    B=S.zeros(2**(n+1))
    for edge,axis,P in ops: B+=(-1 if axis==1 else 1)*P
    return B,ops

def retain_first_choi(n):
    # Direct Kraus outer products of K_(a2,...,an), with the retained input
    # identified with output. Coefficient s, not a Haar trace normalization.
    J=S.zeros(2**(n+1))
    for rest in product(range(2),repeat=n-1):
        v=S.zeros(2**(n+1),1)
        for a in range(2): v[number((a,)+rest+(a,)),0]=1
        J+=s*v*v.T
    return J

def partial_trace_output(M,n):
    return S.Matrix(2**n,2**n,lambda r,c: sum(M[2*r+b,2*c+b] for b in range(2)))

def matrix_strings(M): return [[str(v) for v in row] for row in M.tolist()]

start=time.monotonic()
record('environment',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
       python=platform.python_version(),sympy=S.__version__,
       independence='Reconstruction uses no submitted code or cache. Frozen operators are read only for a subsequent comparison.',
       precision='Exact SymPy integers/rationals; at most 16 by 16 matrices.')
computed={}
for n in (2,3):
    Q=haar(n,True,True); R=haar(n,False,True)
    q0=symmetrizer(n+1)/(n+2)
    r0=kron([symmetrizer(n)/(n+1),I])
    for k in range(n):
        q0=depolarize(q0,k,n+1)
        r0=depolarize(r0,k,n+1)
    assert zero(Q-partial_transpose(q0,n))
    assert zero(R-partial_transpose(r0,n))
    assert S.expand(S.trace(Q)-1)==0 and S.expand(S.trace(R)-2)==0
    assert zero(Q-Q.H) and zero(R-R.H)
    record('source_reconstruction',n=n,entries_each=Q.rows**2,
           comparison='phase/u integration equals local-depolarized permutation symmetrizer after explicit input transpose',
           trace_Q='1',trace_R='2',status='pass')
    J=retain_first_choi(n)
    success=S.expand(S.trace(J*R)); numerator=S.expand(S.trace(J*Q))
    assert success==s and S.expand(numerator-s*(1+t)/2)==0
    assert partial_trace_output(J,n)==s*S.eye(2**n)
    record('attainment',n=n,success=str(success),numerator=str(numerator),
           choi_output_partial_trace='s I_'+str(2**n),status='pass')
    computed[n]=(Q,R,J)

Q,R,J=computed[3]
B,ops=star(3)
H=(Q-(1+t)*R/2).applyfunc(S.expand)
P=kron([S.eye(8),Y])*symmetrizer(4)*kron([S.eye(8),Y])
assert zero(P-P.H) and P*P==P and S.trace(P)==5
residual=H-t*(1-t*t)*(B-3*S.eye(16))/48+t**3*P/5
assert zero(residual)
assert zero(H.subs(t,1)+P/5)
assert zero(H.subs(t,0))
assert zero(H.applyfunc(lambda x:S.expand(x).coeff(t,1))-(B-3*S.eye(16))/48)
record('full_polynomial_certificate',zero_residual_entries=256,projector_trace=5,
       projector_idempotent=True,projector_hermitian=True,
       identity='H=t(1-t^2)(B-3I)/48-t^3 P/5',status='pass')

# Direct matrix anticommutation table, followed by every subset of nine terms.
commute={}
for i,j in combinations(range(9),2): commute[i,j]=ops[i][2]*ops[j][2]==ops[j][2]*ops[i][2]
maxsize=0; maximal=[]; hist={}
for mask in range(512):
    selected=[i for i in range(9) if (mask>>i)&1]
    if all(commute[i,j] for i,j in combinations(selected,2)):
        size=len(selected); hist[size]=hist.get(size,0)+1
        if size>maxsize: maxsize=size; maximal=[selected]
        elif size==maxsize: maximal.append(selected)
assert maxsize==3
record('stabilizer_star_bound',subsets_tested=512,max_commuting_subset=3,
       commuting_subset_histogram=hist,maximal_triples=maximal,
       reason='A stabilizer projector has nonzero Pauli expectations only in its Abelian stabilizer group; each is plus or minus one.',status='pass')

# Source Appendix D two-copy benchmark, independently transcribed permutation
# witness, at delta=s=1/2. This is an upper certificate plus an attainable value.
Q2,R2,J2=computed[2]
def perm_matrix(p):
    m=len(p); out=S.zeros(2**m)
    for col in range(2**m):
        b=bits(col,m);out[number(tuple(b[k] for k in p)),col]=1
    return out
beta=-S.Rational(1,64)
D=beta*(2*S.eye(8)-perm_matrix((1,2,0))-perm_matrix((2,0,1)))
W=partial_transpose(D,2)
rem=Q2.subs(t,S.Rational(1,2))-S.Rational(3,4)*R2.subs(t,S.Rational(1,2))-W
assert rem.eigenvals()=={-S.Rational(5,64):4,S.Integer(0):4}
B2,ops2=star(2)
A2=sum((kron([P0,P0,I]) for P0 in PAULI),S.zeros(8))
assert zero(W-beta*(3*S.eye(8)-A2-B2)/2)
# At most three terms in A2+B2 have nonzero stabilizer expectations: the
# nine Paulis live on the three edges of a triangle, with the same axis
# on both ends; on different edges only equal axes commute.
triangle=[kron([P0,P0,I]) for P0 in PAULI]+[entry[2] for entry in ops2]
triangle_max=0
for mask in range(512):
    ids=[k for k in range(9) if mask>>k&1]
    if all(triangle[i]*triangle[j]==triangle[j]*triangle[i] for i,j in combinations(ids,2)):
        triangle_max=max(triangle_max,len(ids))
assert triangle_max==3
bn=S.expand(S.trace(J2*Q2).subs({t:S.Rational(1,2),s:S.Rational(1,2)}))
bs=S.expand(S.trace(J2*R2).subs({t:S.Rational(1,2),s:S.Rational(1,2)}))
assert (bn,bs,bn/bs)==(S.Rational(3,8),S.Rational(1,2),S.Rational(3,4))
record('published_two_copy_benchmark',delta='1/2',s='1/2',beta=str(beta),
       residual_spectrum={'-5/64':4,'0':4},triangle_max_commuting=triangle_max,
       success=str(bs),numerator=str(bn),fidelity=str(bn/bs),
       source='arXiv:2504.10516v2 Appendix D PDF pp.16-17',status='pass')

# Physical discrimination: general positive Choi matrices need not obey the
# stabilizer star bound. The candidate does not accidentally prove a CP-only
# no-go. A positive eigenvalue is a useful omitted-resource control.
ev=H.subs(t,S.Rational(1,2)).eigenvals()
positive=[str(e) for e in ev if e.is_positive]
assert positive
record('resource_restriction_control',t='1/2',positive_H_eigenvalues=positive,
       interpretation='PSD alone is insufficient; the stabilizer-cone condition is essential.',status='pass')

# A target-dependent Bell filter retaining the untouched third copy checks that
# Haar success must not be replaced by Tr(J)/8. This is an admissible branch.
bell=S.Matrix([1,0,0,1])*S.Matrix([1,0,0,1]).T/2
Jfilter=2*kron([bell,bell])
filter_success=S.expand(S.trace(Jfilter*R))
filter_num=S.expand(S.trace(Jfilter*Q))
assert filter_success==(t*t+3)/12
assert S.expand(filter_num-(1+t)*filter_success/2)==0
assert partial_trace_output(Jfilter,3)==kron([bell,I])
assert filter_success.subs(t,S.Rational(1,2))==S.Rational(13,48)
assert S.trace(Jfilter)/8==S.Rational(1,4)
record('target_dependent_success_control',success=str(filter_success),
       success_at_t_half='13/48',choi_trace_over_8='1/4',
       fidelity='(1+t)/2',status='pass')

# The independent operators above are already complete. Read the submitted
# numerical data only now, to compare their variable/basis conventions.
comparison_count=0
for filename,which in [('evidence/input-a.json','A'),('evidence/input-b.json','B')]:
    cache=json.loads((ROOT/filename).read_text())
    for n in (2,3):
        q,r,j=computed[n]
        ours={'Q':partial_transpose(q,n),'R':partial_transpose(r,n),'QT':q,'RT':r}
        for name,expected in ours.items():
            rows=cache['cases'][str(n)][name]['rows']
            variable=(1-t) if which=='A' else t
            given=S.Matrix([[sum(S.Rational(c)*variable**k for k,c in enumerate(coeff))
                              for coeff in row] for row in rows])
            if which=='B':
                mapping=[(v%2)*2**n+v//2 for v in range(2**(n+1))]
                given=S.Matrix(given.rows,given.cols,lambda r,c:given[mapping[r],mapping[c]])
            assert zero(expected-given)
            comparison_count+=given.rows*given.cols
record('frozen_operator_comparison',entries_compared=comparison_count,
       cases=[2,3],operators=['Q','R','QT','RT'],
       inputs=['A(delta,input-first)','B(t,output-first)'],status='pass')

data={'replay_kind':'independent phase-integral representation','records':records,
      'H_coefficients':{str(k):matrix_strings(H.applyfunc(lambda x:S.expand(x).coeff(t,k))) for k in (1,3)},
      'duration_seconds':time.monotonic()-start}
(ROOT/'generated/phase-replay-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
record('completed',status='pass',elapsed_seconds=time.monotonic()-start)
