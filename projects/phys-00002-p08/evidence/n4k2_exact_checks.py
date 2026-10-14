"""Same-worker exact checks of curvature, normal form and replacement POVMs.

Independent algebraic representation of the analytic argument: explicit 2x2
matrices, with no cached Jacobian/nullspace read. This is proposer verification,
not a fresh scientific referee audit. The universal statement is proved in the
accompanying stable proof; finite examples alone do not establish it.
"""
from itertools import combinations
import json
from pathlib import Path
import sys
import sympy as s

I=s.eye(2)
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
def op(v):
    return sum((v[k]*pauli[k] for k in range(3)),s.zeros(2))
def pure(r):
    return (I+op(r))/2
def effect(alpha,n):
    return alpha*(I+op(n))
def zero(A):
    return A.applyfunc(s.simplify)==s.zeros(A.rows,A.cols)
def real_linear_equations(A):
    return [s.simplify(part) for x in A for part in [s.re(x),s.im(x)] if part!=0]

S=s.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
rT=[S.row(i).T/s.sqrt(3) for i in range(4)]
rU=[s.Matrix([-1,0,0]),s.Matrix([0,-1,0]),s.Matrix([0,0,-1]),s.Matrix([2,3,6])/7]
models=[('tetrahedral',rT,[s.Rational(1,4)]*4),
        ('unequal_weight_extremal',rU,[s.Rational(2,18),s.Rational(3,18),s.Rational(6,18),s.Rational(7,18)])]
summary=[]
print('Python',sys.version.replace('\n',' '),'SymPy',s.__version__)
for name,r,alpha in models:
    rho=[pure(v) for v in r]
    E=[effect(alpha[i],-r[i]) for i in range(4)]
    affine=s.Matrix([[1,*list(v)] for v in r])
    assert s.simplify(affine.det())!=0
    assert zero(sum(E,s.zeros(2))-I)
    assert all(zero(R*R-R) and s.trace(R)==1 for R in rho)
    assert all(s.simplify(s.trace(rho[i]*E[i]))==0 for i in range(4))
    assert all(s.Matrix.hstack(*(r[i] for i in inds)).det()!=0 for inds in combinations(range(4),3))
    print('\nMODEL',name,'affine determinant',s.simplify(affine.det()),'positive weights',alpha)
    # Derive the ENTIRE Hermitian complementary-slackness linear solution space
    # from (Lambda-H_j)E_j=0, without assuming the asserted coefficient form.
    cs=s.symbols('c0:16',real=True)
    la=s.symbols('L0:4',real=True)
    Lam=la[0]*I+sum((la[k+1]*pauli[k] for k in range(3)),s.zeros(2))
    eq=[]
    for j in range(4):
        Hj=sum((cs[4*i+j]*rho[i] for i in range(4)),s.zeros(2))
        eq+=real_linear_equations((Lam-Hj)*E[j])
    unknowns=[*cs,*la]
    C=s.Matrix(eq).jacobian(unknowns)
    kern=s.Matrix.hstack(*C.nullspace())
    assert kern.cols==8
    # Explicit expected eight-dimensional space: 4 common row shifts and
    # 4 diagonal penalties. Lambda=sum l_i rho_i.
    expected=[]
    for i in range(4):
        row=[s.Integer(1) if ii==i else s.Integer(0) for ii in range(4) for j in range(4)]
        row+=[s.Rational(1,2),*list(r[i]/2)]
        expected.append(s.Matrix(row))
    for j in range(4):
        row=[-s.Integer(1) if ii==j and jj==j else s.Integer(0) for ii in range(4) for jj in range(4)]
        expected.append(s.Matrix([*row,0,0,0,0]))
    N=s.Matrix.hstack(*expected)
    assert zero(C*N) and N.rank()==8 and N.row_join(kern).rank()==8
    print('PASS complementary-slackness solution space EXACTLY c_ij=l_i-k_j delta_ij (dimension8).')
    # Adversarial active-index sets: all pairs, each singleton and the empty set.
    # A plane through any selected pair is physically attainable by2 projectors.
    for active in [(),*((i,) for i in range(4)),*combinations(range(4),2)]:
        alt=[s.zeros(2) for i in range(4)]
        rr=list(r)
        if len(active)==2:
            a,b=active
            c=next(i for i in range(4) if i not in active)
            R=r[a]+r[b]
            length=s.sqrt(s.simplify(R.dot(R)))
            assert length!=0
            q=R/length
            A=1/(2+length)
            alt[a]=effect(A,-r[a]);alt[b]=effect(A,-r[b]);alt[c]=effect(A*length,q)
            rr[c]=-q
        else:
            a=active[0] if active else 0
            c=next(i for i in range(4) if i!=a)
            alt[a]=effect(s.Rational(1,2),-r[a]);alt[c]=effect(s.Rational(1,2),r[a])
            rr[c]=-r[a]
        assert zero(sum(alt,s.zeros(2))-I)
        assert all(s.simplify(s.trace(pure(rr[i])*alt[i]))==0 for i in range(4))
        assert all(rr[i]==r[i] for i in active)
        assert sum(A!=s.zeros(2) for A in alt)<=3
        assert all(s.simplify(A.det())==0 and s.simplify(s.trace(A)).is_nonnegative for A in alt)
        # Score with arbitrary common-row shifts, nonnegative penalties, and
        # arbitrary signed auxiliary contribution u_i=eta_i*r_i on active rows.
        li=s.symbols('l1:5',real=True);ki=s.symbols('k1:5',nonnegative=True)
        eta=s.symbols('e1:5',real=True)
        original=s.Integer(0);replacement=s.Integer(0)
        for i in range(4):
            u=eta[i]*r[i] if i in active else s.zeros(3,1)
            original+=r[i].dot(u);replacement+=rr[i].dot(u)
            for j in range(4):
                coefficient=li[i]-(ki[j] if i==j else 0)
                original+=coefficient*s.trace(rho[i]*E[j])
                replacement+=coefficient*s.trace(pure(rr[i])*alt[j])
        assert s.simplify(original-replacement)==0
        print('PASS active labels',tuple(i+1 for i in active),'replacement positivity/completeness/diagonal zeros/same SYMBOLIC score; <=3 nonzero effects.')
    summary.append({'model':name,'normal_form_space_dimension':8,'active_sets_checked':11,'replacement_score_difference':'0 exact'})

# Physical two-sided curve through the non-gauge tetrahedral null direction.
# No cached output from n4k2_linearization.py is used.
t=s.symbols('t',real=True)
A=s.Matrix([[0,-1,1],[0,-1,1],[0,1,1],[0,1,1]])
D=s.Matrix([[-1,0,0],[1,0,0],[-1,0,0],[1,0,0]])
z=s.Matrix([s.Rational(1,3),-s.Rational(1,3),-s.Rational(1,3),s.Rational(1,3)])
K=s.Matrix.vstack(*(D.row(j)+z[j]*S.row(j) for j in range(4)))
rc=[(S.row(i).T+t*A.row(i).T)/s.sqrt(3+2*t*t) for i in range(4)]
nc=[(-S.row(j).T+t*K.row(j).T)/s.sqrt(3+s.Rational(2,3)*t*t) for j in range(4)]
ac=[(1+t*z[j])/4 for j in range(4)]
vc=[s.Matrix([1,0,0]),s.Matrix([t,1,0])/s.sqrt(1+t*t)]
assert all(s.simplify(v.dot(v))==1 for v in [*rc,*nc,*vc])
assert s.simplify(sum(ac))==1
assert zero(sum((ac[j]*nc[j] for j in range(4)),s.zeros(3,1)))
P=s.Matrix(4,4,lambda i,j:ac[j]*(1+rc[i].dot(nc[j])))
Q=s.Matrix(4,2,lambda i,y:(1+rc[i].dot(vc[y]))/2)
assert all(s.simplify(s.diff(p,t).subs(t,0))==0 for p in [*P,*Q])
diag2=[s.simplify(s.diff(P[i,i],t,2).subs(t,0)/2) for i in range(4)]
assert diag2==[s.Rational(1,9)]*4
target_affine=s.Matrix([[1,*list(v)] for v in nc])
det=s.factor(target_affine.det())
print('\nPASS physical curve: all24 probability first derivatives zero; pure states, projective auxiliaries, rank-one complete target exactly.')
print('Curve weights positive for |t|<3; target affine determinant=',det)
print('Diagonal probabilities p(i|i)=alpha_i(t)*(1-3/sqrt((3+2t^2)*(3+2t^2/3)))>0 for 0<|t|<3.')
print('Quadratic coefficients p(i|i)/t^2 ->',diag2)

# Shared-randomness target-only spoof, deliberately NOT a full N4/K2 spoof.
spoof=s.zeros(4,4)
for a,b in combinations(range(4),2):
    for i in range(4):
        if i==a:spoof[i,b]+=s.Rational(1,6)
        elif i==b:spoof[i,a]+=s.Rational(1,6)
        else:
            spoof[i,a]+=s.Rational(1,12);spoof[i,b]+=s.Rational(1,12)
assert spoof==s.Matrix(4,4,lambda i,j:0 if i==j else s.Rational(1,3))
print('PASS six-branch two-outcome-projective target-only spoof:',spoof.tolist())
print('Universal result rests on the analytic proof, not these finite checks. No referee acceptance; original general resource problem unresolved.')
Path('evidence/n4k2-exact-check-summary.json').write_text(json.dumps({'job_id':'phys-00002-p08-research-babca3f8ba11','mode':'exact','purpose':'Same-worker proposer checks of universal proof building blocks; not independent referee','models':summary,'curve_diagonal_quadratic_coefficient':'1/9','all_probability_first_derivatives':'0 exact','target_only_spoof':'0 diagonal,1/3 offdiagonal exact','original_status':'unresolved'},indent=2)+'\n')
