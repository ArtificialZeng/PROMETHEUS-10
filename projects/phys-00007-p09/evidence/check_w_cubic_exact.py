"""Separate operator-commutator check of the decisive one-dimensional jet.
Does not import w_cubic or read its outputs. Shares radical arithmetic and source q.
"""
from radical_algebra import *
def comm(A,B):return add(mul(A,B),scale(-1,mul(B,A)))
def mv(M,v):return [sum(x*y for x,y in zip(row,v)) for row in M]
def expectation(T):return sum(w[j].conj()*x for j,x in enumerate(mv(T,w)))*Q(1,3)
w=[one if k in [1,2,4] else zero for k in range(8)]
V=tensor([q,q,q])
K=[tensor([X if k==j else Z for k in range(3)]) for j in range(3)]
S=K+[mul(K[0],K[1]),mul(K[0],K[2]),mul(K[1],K[2])]
O=add(mul(S[3],K[2]),scale(-2,add(add(K[0],K[1]),K[2])))
Cs=[tensor([p if k==j else I for k in range(3)]) for j in range(3) for p in [X,Y,Z]]
def g(t):
 M=[[zero for _ in range(8)] for _ in range(8)]
 for x,C in zip(t,Cs):M=add(M,scale(x*Q(1,2),C))
 return mul(dag(V),mul(M,V))
H=g([zero,2*r*a*b,F(-3),zero,zero,F(2),zero,zero,F(2)])
L=g([13*r*a*b,zero,zero,-4*r*a*b,zero,zero,-4*r*a*b,zero,zero])
S=[mul(dag(V),mul(T,V)) for T in S]
O=mul(dag(V),mul(O,V))
checks=[]
for T in S+[O]:
 baseline=expectation(T)
 first=i*expectation(comm(H,T))
 second=i*expectation(comm(L,T))-Q(1,2)*expectation(comm(H,comm(H,T)))
 assert baseline==first==second==0
 checks.append({'baseline':baseline.record(),'first':first.record(),'second':second.record()})
cubic=-i*Q(1,6)*expectation(comm(H,comm(H,comm(H,O))))-Q(1,2)*expectation(add(comm(H,comm(L,O)),comm(L,comm(H,O))))
assert cubic==-Q(80,3)*a*b
delta=mv(O,w)
norm=sum(x.conj()*x for x in delta)*Q(1,3)
overlap=sum(x.conj()*y for x,y in zip(w,delta))*Q(1,3)
source_linear=sum(x.conj()*y+y.conj()*x for x,y in zip(mv(O,w),delta))*Q(1,3)
assert norm==13 and overlap==0 and source_linear==26
out={'status':'pass','representation':'operator conjugation in original W basis; nested commutators',
 'independence':'Separately coded, no w_cubic import or cached jet input; shared radical algebra and primary q',
 'jet_checks':checks,'cubic_exact':cubic.record(),'cubic_numeric':cubic.val().real,
 'source_path_norm_squared':13,'source_path_missing_derivative':26,
 'limitations':'Proposer cross-check, not fresh referee acceptance; full cubic checked in separate vector expansion'}
print(json.dumps(out,indent=2))
