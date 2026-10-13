"""Direct 27-dimensional endpoint and dual replay, without cached marginal maps.

Radical-square relations are imposed exactly; the only unsatisfied formal marginal
is reported explicitly and proved zero by the separate Sturm/branch certificate.
"""
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
l,t,e,z,b,c=s.symbols('l t e z b c',positive=True)
radicals=(t,e,z,b,c)
squares=[l,2-3*l,2*(1-l)**2-l*l/8,2*l-1,2*l*(1-l)]

def canonical(expr):
    p=s.Poly(s.expand(expr),*radicals)
    total=0
    for powers,coeff in p.terms():
        term=coeff
        for var,power,square in zip(radicals,powers,squares):term*=var**(power%2)*square**(power//2)
        total+=term
    return s.expand(total)

def ket(a,bb,cc):
    v=s.zeros(27,1);v[9*a+3*bb+cc]=1;return v

def symmetric(a,bb,cc,minus=False):
    return ket(a,bb,cc) if bb==cc else (ket(a,bb,cc)+(-1 if minus else 1)*ket(a,cc,bb))/s.sqrt(2)

def trace_output(M,leg):
    return s.Matrix(9,9,lambda i,j:sum(M[9*(i//3)+(3*(i%3)+q if leg==2 else 3*q+i%3),9*(j//3)+(3*(j%3)+q if leg==2 else 3*q+j%3)] for q in range(3)))

def main():
    k=t/s.sqrt(2);p=l/(2*s.sqrt(2));w=l*l+l-1
    g0=ket(0,0,0)+t*symmetric(1,0,1)+p*symmetric(2,0,2)+k*t*ket(2,1,1)
    g1=e*symmetric(1,0,1)+z*symmetric(2,0,2)+k*e*ket(2,1,1)
    g2=b*ket(1,1,1)+c*symmetric(2,1,2)
    Y=g0*g0.T+g1*g1.T+g2*g2.T+w*ket(2,2,2)*ket(2,2,2).T
    triples=[(aa,bb,cc) for aa in range(3) for bb in range(3) for cc in range(3)]
    for g in [g0,g1,g2]:assert all(s.expand(g[i]-g[9*aa+3*cc+bb])==0 for i,(aa,bb,cc) in enumerate(triples))
    assert canonical(s.trace(Y)-3)==0
    J3=s.zeros(9)
    for m in range(3):
        for n in range(3):
            for loss in range(min(m,n)+1):
                J3[3*m+m-loss,3*n+n-loss]+=2**(-s.Rational((m-n)**2,2))*s.sqrt(s.binomial(m,loss)*s.binomial(n,loss))*(1-l)**loss*t**(m+n-2*loss)
    J3=J3.applyfunc(canonical)
    saved=json.loads((ROOT/'evidence/input-a.json').read_text())
    lam=s.Symbol('lam',nonnegative=True)
    A=s.Matrix([[s.sympify(x,locals={'lam':lam}).subs(lam,t*t) for x in row] for row in saved['choi_ab']])
    assert (3*A-J3).applyfunc(canonical)==s.zeros(9)
    f=e*z+s.sqrt(2)*b*c-3*l*t/(2*s.sqrt(2))
    for leg in [1,2]:
        residual=(trace_output(Y,leg)-J3).applyfunc(canonical)
        expected=s.zeros(9);expected[4,8]=expected[8,4]=f/2
        assert (residual-expected).applyfunc(canonical)==s.zeros(9)
    print('PASS: four pure-state endpoint components directly embedded in27 dimensions')
    print('PASS: swap invariance, trace3, both81-entry marginal residuals exactly zero except f/2 at(4,8),(8,4)')
    print('PASS: direct source transcription exactly matches all81 saved A Choi entries')
    print('The independent exact root/branch certificate proves f=0 at the isolated endpoint.')
    # New direct dual construction, with no import of reduction arrays.
    u,v=s.symbols('u v',positive=True);tt=s.symbols('tt',positive=True)
    rr=tt*tt;pp=rr/(2*s.sqrt(2));kk=tt/s.sqrt(2);eta=s.sqrt(2)*u/v;beta=2*eta;cc=tt*u-pp
    y=[cc*cc,-2*s.sqrt(2)*u*cc,2*s.sqrt(2)*cc,2*u*u+eta*(2*rr-v*v),-2*beta*tt,eta*v*v,-4*u,2,beta,0]
    H=s.zeros(9)
    for i,j in zip([0,3,4,6,7,8],[0,3,5,7,8,9]):H[i,i]=y[j]
    for (i,j),q in zip([(0,4),(0,8),(3,7),(4,8)],[1,2,4,6]):H[i,j]=H[j,i]=y[q]/2
    W=s.Matrix(27,27,lambda i,j:(H[3*triples[i][0]+triples[i][1],3*triples[j][0]+triples[j][1]]*int(triples[i][2]==triples[j][2])+H[3*triples[i][0]+triples[i][2],3*triples[j][0]+triples[j][2]]*int(triples[i][1]==triples[j][1]))/2)
    assert all(W[i,j]==0 for i,(aa,bb,ccc) in enumerate(triples) for j,(aaa,bbb,cccc) in enumerate(triples) if bb+ccc-aa!=bbb+cccc-aaa)
    assert all(W[i,j]==W[9*aa+3*ccc+bb,9*aaa+3*cccc+bbb] for i,(aa,bb,ccc) in enumerate(triples) for j,(aaa,bbb,cccc) in enumerate(triples))
    n=s.Matrix([cc,-u,1,0]);m=s.Matrix([0,-kk,0,1]);j=s.Matrix([v,-1])
    expected={-2:s.Matrix([[2]]),-1:s.Matrix([[y[3],-beta*kk],[-beta*kk,1+eta]]),0:n*n.T+beta*m*m.T,1:eta*j*j.T,2:s.zeros(1)}
    plus={};minus={};labels={}
    for aa in range(3):
        for bb in range(aa+1):
            for ccc in range(bb,aa+1):
                q=bb+ccc-aa;plus.setdefault(q,[]).append(symmetric(aa,bb,ccc));labels.setdefault(q,[]).append((aa,bb,ccc))
                if bb<ccc:minus.setdefault(q,[]).append((symmetric(aa,bb,ccc,True),(aa,bb,ccc)))
    for q,columns in plus.items():
        B=s.Matrix.hstack(*columns);C=B.T*W*B
        assert (C-expected[q]).applyfunc(s.simplify)==s.zeros(C.rows)
    for q,columns in minus.items():
        B=s.Matrix.hstack(*[x[0] for x in columns]);indices=[labels[q].index(x[1]) for x in columns];C=B.T*W*B
        assert (C-expected[q].extract(indices,indices)).applyfunc(s.simplify)==s.zeros(C.rows)
    print('PASS: all five plus and all three minus face dual blocks exactly equal advertised Gram/principal blocks')
    print('PASS: no off-charge dual entries, exact full swap invariance; no sector omitted')
    (ROOT/'evidence/qutrit-symbolic-replay.json').write_text(json.dumps({'status':'pass','full_dimension':27,'marginals_checked':2,'entries_each':81,'source_entries_checked':81,'trace':'TrY=3 exactly; X=Y/3','swap':'all component amplitudes exactly invariant','remaining_formal_residual':'f/2 only at(4,8),(8,4); exact Sturm/branch proof establishes f(r)=0','dual_blocks_checked':{'plus':5,'minus':3},'independence':'Separate direct pure-component embedding and full computational W entries; no cached marginal/constraint maps. Same worker and SymPy shared, not a fresh referee.','root_certificate':'evidence/qutrit-exact-certificate.json'},indent=2)+'\n')

if __name__=='__main__':main()
