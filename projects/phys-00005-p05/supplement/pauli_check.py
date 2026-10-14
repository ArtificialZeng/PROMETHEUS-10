"""Portable Pauli reconstruction derived from the separate referee implementation.
This rerun is reproduction, not a new independent review.
"""
from itertools import combinations
import sympy as S

I=S.eye(2); X=S.Matrix([[0,1],[1,0]]); Y=S.Matrix([[0,-S.I],[S.I,0]]); Z=S.diag(1,-1)
def embed(n,ops):
    return S.kronecker_product(*[ops.get(k,I) for k in range(n)])
def model(n,edges,s,phases):
    H=S.zeros(2**n)
    for i,j in edges:
        u=phases.get((i,j),S.Integer(1))
        H-=(1+s*s)/4*(S.eye(2**n)+embed(n,{i:Z,j:Z}))
        H-=(1-s*s)/4*(embed(n,{i:Z})+embed(n,{j:Z}))
        H-=s/2*(S.re(u)*(embed(n,{i:X,j:X})-embed(n,{i:Y,j:Y}))+S.im(u)*(embed(n,{i:X,j:Y})+embed(n,{i:Y,j:X})))
    assert H==H.conjugate().T
    assert H*embed(n,{k:Z for k in range(n)})==embed(n,{k:Z for k in range(n)})*H
    return H
def sectors(H,n):
    return [H.extract([b for b in range(2**n) if b.bit_count()%2==p],[b for b in range(2**n) if b.bit_count()%2==p]) for p in (0,1)]
x=S.symbols('x'); s=S.Rational(3,4)
# Complex source h(z) reconstruction tests phase orientation, not only real signs.
u=(3+4*S.I)/5
local=model(2,[(0,1)],s,{(0,1):u})
ket=S.Matrix([1,0,0,s*u])
assert (local+ket*ket.conjugate().T).applyfunc(S.simplify)==S.zeros(4)
print('Source Eq77 complex local operator PASS',local.tolist())
H=model(4,list(combinations(range(4),2)),s,{(1,3):-1,(2,3):-1})
E,O=sectors(H,4)
pe=S.Poly(E.charpoly(x).as_expr(),x); po=S.Poly(O.charpoly(x).as_expr(),x)
print('Independent even characteristic polynomial',S.factor(pe.as_expr()))
print('Independent odd characteristic polynomial',S.factor(po.as_expr()))
intervals=[(S.Rational(-669,100),S.Rational(-667,100)),(S.Rational(-449,100),S.Rational(-447,100)),(S.Rational(-51,50),S.Integer(-1)),(S.Rational(-17,50),S.Rational(-33,100))]
counts=[pe.count_roots(a,b) for a,b in intervals]
assert counts==[1,1,1,1]
assert pe.count_roots(-S.oo,S.Rational(-89,20))==2
assert po.count_roots(-S.oo,S.Rational(-83,20))==0
assert po.eval(S.Rational(-83,20))!=0
assert S.Rational(3321)<S.Rational(289,5)**2
assert S.factor(pe.as_expr()).subs(x,-S.Rational(25,16))==0
assert pe.count_roots(-S.oo,-6)==1
print('Exact sector root counts PASS',counts,'even below -89/20 = 2; odd <= -83/20 = 0; unique even ground below -6')
# Alternative to root isolation: exact LDL congruence on freshly assembled sectors.
for label,M,t,negative in [('even',E,S.Rational(89,20),2),('odd',O,S.Rational(83,20),0)]:
    A=M+t*S.eye(8); L,D=A.LDLdecomposition(hermitian=False)
    assert L*D*L.T==A
    diag=list(D.diagonal()); assert all(v!=0 for v in diag)
    assert sum(int(bool(v<0)) for v in diag)==negative
    print('Exact LDL',label,'pivots',[str(v) for v in diag],'negative',negative)
# Reconstruct published parent star and interior star baseline independently.
for amp in [S.Integer(1),S.Rational(1,2)]:
    star=model(4,[(0,1),(0,2),(0,3)],amp,{})
    even,odd=sectors(star,4)
    ev=even.eigenvals(); ov=odd.eigenvals()
    print('Star baseline',amp,'even',ev,'odd',ov)
    if amp==1:
        assert min(ev)==-4 and min(ov)==-4
        v=S.zeros(16,1);v[0]=S.sqrt(3)/2
        for b in [12,10,9]:v[b]=1/(2*S.sqrt(3))
        assert star*v==-4*v and (v.T*v)[0]==1
    else:
        assert min(ev)==-S.Rational(13,4) and min(ov)==-S.Rational(5,2)
        assert min(ov)-min(ev)==1-amp**2
print('Published parent bound saturation and interior source Lemma13 PASS')
# Domain and analytic robustness arithmetic. Operator inequality is audited in science.md.
margin=S.Rational(3,10); perturb=6*(3*S.Rational(1,1000)+S.Rational(1,1000))
assert margin-2*perturb==S.Rational(252,1000)
assert S.Rational(3,4)-S.Rational(1,1000)>0 and S.Rational(3,4)+S.Rational(1,1000)<1
assert 4*S.Rational(1,1000)<S.pi
print('Weyl neighborhood arithmetic PASS',perturb,margin-2*perturb)
print('INDEPENDENT REPLAY PASS; no discovery modules, matrices, or logs imported')
