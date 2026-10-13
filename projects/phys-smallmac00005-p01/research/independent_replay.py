"""Same-researcher replay using a Clifford orbit and independent input B.

No import of the isotropic enumerator or its multiplication-phase table. The
orbit is generated without reading its ray corpus; comparison occurs afterwards.
This is not the fresh referee audit required by the workflow.
"""
from collections import deque, Counter
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import json
import time
import sympy as S

START=time.monotonic()
N=4
digits=[tuple((v//(4**(3-k)))%4 for k in range(4)) for v in range(256)]


def encode(ds):
    return sum(v*4**(3-k) for k,v in enumerate(ds))


I=S.eye(2); X=S.Matrix([[0,1],[1,0]]); Z=S.diag(1,-1); Y=S.Matrix([[0,-S.I],[S.I,0]])
p=[I,X,Z,Y]
# Construct the 2-qubit controlled-X as an actual computational-basis matrix.
cx=S.zeros(4)
for c,b in product([0,1],repeat=2):
    cx[2*c+(b^c),2*c+b]=1
twopauli=[S.kronecker_product(a,b) for a in p for b in p]
cxtable={}
for a,b in product(range(4),repeat=2):
    transformed=cx*S.kronecker_product(p[a],p[b])*cx.T
    matches=[(v//4,v%4,sgn) for v,mat in enumerate(twopauli)
             for sgn in [1,-1] if transformed==sgn*mat]
    assert len(matches)==1
    cxtable[a,b]=matches[0]

# Each state is the sorted list of its 15 nonidentity signed Pauli elements.
# An element is encoded as 2*v+(sign<0). Identity is omitted.
tables=[]
for gate in ['H','S']:
    for pos in range(4):
        table=[]
        for v,negative in product(range(256),[0,1]):
            ds=list(digits[v]); old=ds[pos]
            if gate=='H':
                ds[pos]=[0,2,1,3][old]; flip=(old==3)
            else:
                ds[pos]=[0,3,2,1][old]; flip=(old==3)
            table.append(2*encode(ds)+(negative^flip))
        tables.append(table)
for control,target in [(0,1),(1,0),(1,2),(2,1),(2,3),(3,2)]:
    table=[]
    for v,negative in product(range(256),[0,1]):
        ds=list(digits[v])
        a,b,sgn=cxtable[ds[control],ds[target]]
        ds[control],ds[target]=a,b
        table.append(2*encode(ds)+(negative^(sgn==-1)))
    tables.append(table)

initial=tuple(sorted(2*encode(ds) for ds in product([0,2],repeat=4) if any(ds)))
orbit={initial}; queue=deque([initial])
while queue:
    state=queue.popleft()
    for table in tables:
        new=tuple(sorted(table[x] for x in state))
        if new not in orbit:
            orbit.add(new); queue.append(new)
assert len(orbit)==36720
print('Independent Clifford orbit: 36720 states from |0000>, H/S and adjacent directed CNOT.',flush=True)

# Polynomial coefficients from separately derived Bloch-moment input B, in its
# own output-first basis. This stage never uses the matrix input A.
b=json.loads(Path('evidence/input-b.json').read_text())['cases']['3']['pauli_terms']
coefficients={}
alphabet={'I':0,'X':1,'Z':2,'Y':3}
for kind in ['Q','R']:
    for term in b[kind]:
        labels=term['labels']; a_labels=labels[1:]+labels[0]
        v=encode([alphabet[x] for x in a_labels])
        coeff=Fraction(term['coefficient'])*(-1)**labels[1:].count('Y')
        k=term['t_degree']
        arr=coefficients.setdefault(v,[Fraction(0)]*4)
        if kind=='Q':
            arr[k]+=coeff
        else:
            arr[k]-=coeff/2; arr[k+1]-=coeff/2
scaled={v:tuple(c*240 for c in arr) for v,arr in coefficients.items()}
assert all(c.denominator==1 for arr in scaled.values() for c in arr)
scaled={v:tuple(int(c) for c in arr) for v,arr in scaled.items()}
assert all(arr[0]==arr[2]==0 for arr in scaled.values())

corpus=set(); classes=Counter(); equality=0
for line in Path('evidence/stabilizer4-rays.jsonl').read_text().splitlines():
    ray=json.loads(line)
    support=ray['signed_pauli_support']
    state=tuple(2*v+(sgn<0) for v,sgn in support if v)
    assert state not in corpus
    corpus.add(state)
    value=[sum(sgn*scaled.get(v,(0,0,0,0))[k] for v,sgn in support) for k in range(4)]
    assert value==ray['g_t_coefficients_over_240']
    assert value[1]<=0 and value[1]+value[3]<=0
    classes[value[1],value[3]]+=1
    equality+=not any(value)
assert corpus==orbit

# An independent finite verification of the elementary star-correlation lemma:
# check commutators directly, then every subset of the nine operators.
star=[]
for i in range(3):
    for a,sgn in [(1,1),(2,1),(3,-1)]:
        ds=[0]*4; ds[i]=ds[3]=a
        star.append(sgn*S.kronecker_product(*(p[k] for k in ds)))
commute=[[star[i]*star[j]==star[j]*star[i] for j in range(9)] for i in range(9)]
cliques=[]
for mask in range(512):
    indices=[i for i in range(9) if (mask>>i)&1]
    if all(commute[i][j] for i,j in combinations(indices,2)):
        cliques.append(indices)
assert max(map(len,cliques))==3

# Independent unnormalized Choi primal with arbitrary success scale s.
t,s=S.symbols('t s',real=True)
bb=json.loads(Path('evidence/input-b.json').read_text())['cases']['3']


def unpack_outfirst(record):
    raw=S.Matrix([[sum(S.Rational(c)*t**k for k,c in enumerate(cell)) for cell in row]
                  for row in record['rows']])
    return S.Matrix(16,16,lambda i,j:raw[(i%2)*8+i//2,(j%2)*8+j//2])


q,r=unpack_outfirst(bb['QT']),unpack_outfirst(bb['RT'])
# The symmetric projector is reconstructed by Dicke-weight blocks, not by
# permutation summation or the cached source matrices.
weight=[bin(i).count('1') for i in range(16)]
pi=S.Matrix(16,16,lambda i,j:S.Rational(1,S.binomial(4,weight[i])) if weight[i]==weight[j] else 0)
assert pi*pi==pi and S.trace(pi)==5
uy=S.kronecker_product(S.eye(8),Y)
projector=uy*pi*uy
h=(q-(1+t)*r/2).applyfunc(S.expand)
star_matrix=sum(star,S.zeros(16))
closed=t*(1-t*t)*(star_matrix-3*S.eye(16))/48-t**3*projector/5
assert all(S.expand(x)==0 for x in h-closed)
assert h.subs(t,1)==-projector/5
Path('evidence/analytic-operator-certificate.json').write_text(json.dumps({
    'identity':'H(t)=t(1-t^2)(B-3I)/48-t^3 P/5',
    'P':'(I8 tensor Y) Pi_sym,4 (I8 tensor Y)',
    'reconstruction':'Pi_sym,4[i,j]=1/binomial(4,wt(i)) when wt(i)=wt(j), else zero',
    'B':[[str(x) for x in star_matrix.row(i)] for i in range(16)],
    'projector':[[str(x) for x in projector.row(i)] for i in range(16)],
    'projector_rank':5,'exact_matrix_identity_entries':256,
    'source_input':'evidence/input-b.json','proof':'research/proof.md'
},indent=2)+'\n')
choi=S.zeros(16)
for a,b,x,y in product([0,1],repeat=4):
    choi[8*a+4*x+2*y+a,8*b+4*x+2*y+b]=s
ptr=S.Matrix(8,8,lambda i,j:choi[2*i,2*j]+choi[2*i+1,2*j+1])
assert ptr==s*S.eye(8)
success=S.expand(S.trace(choi*r))
numerator=S.expand(S.trace(choi*q))
print(f'Primal success={success}; numerator={numerator}; expanded residual='+str(S.expand(numerator-s*(1+t)/2)),flush=True)
assert S.expand(success-s)==0 and S.expand(numerator-s*(1+t)/2)==0
assert choi.subs(s,1).eigenvals()=={S.Integer(2):4,S.Integer(0):12}
record={'method':'Independent Clifford orbit from |0000>; actual 4x4 CNOT conjugation; Bloch-input B ray polynomials; direct nine-star commutators; symbolic discard-two primal.',
    'independence':'Same researcher; no imported enumerator, input A, phase table, isotropic spaces or generator eigenvalue construction. Raw corpus is read only after orbit generation. Input B was independently derived in the reproduction phase. A fresh referee remains required.',
    'orbit_rays':len(orbit),'corpus_exact_set_equality':True,'polynomial_matches':len(corpus),
    'polynomial_classes':len(classes),'zero_polynomials':equality,'maximum_commuting_star_subset':max(map(len,cliques)),
    'closed_operator_certificate':'H(t)=t(1-t^2)(B-3I)/48-t^3*(I8 tensor Y)*Pi_sym,4*(I8 tensor Y)/5; all 256 entries agree with input B; projector has rank 5.',
    'primal_success':str(success),'primal_numerator':str(numerator),'primal_TrB':'s I8',
    'primal_Choi_eigenvalues_at_s1':{'2':4,'0':12},
    'coverage':'All 36720 rays, entire real interval 0<=t<=1 via endpoint coefficients, arbitrary 0<s<=1 by symbolic primal.',
    'error_control':'Exact rational and Python-integer arithmetic only; no tolerance, floating point fit, solver or probabilistic test.',
    'elapsed_seconds':time.monotonic()-START,'limitations':'Research replay, not independent job or scientific acceptance. Literature novelty is separately pending fresh review.'}
Path('evidence/research-independent-replay.json').write_text(json.dumps(record,indent=2)+'\n')
log='\n'.join(f'{key}: {value}' for key,value in record.items())+'\n'
Path('evidence/research-independent-replay.log').write_text(log)
print(log)
