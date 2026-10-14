"""Same-worker independent exact n=6 replay from differentiated full equations.

Does not import the Fourier perturbation generator or its cached eigenvalues.
Differentiates original defining rates, then solves a bordered eigenvector system.
The closed generic formula is read only after this reconstruction for comparison.
"""
import json,time
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix

def simplify(z):return s.simplify(s.expand_complex(z))

def exact_second(h,p):
    n=6;e=s.symbols('e',real=True);g=(s.sqrt(3)-1)/2
    # Coefficients are obtained by differentiation of the defining equations.
    normalizer=sum(s.exp(e*pj) for pj in p)
    Q=s.zeros(n)
    for i in range(n):
        invpi=normalizer*s.exp(-e*p[i])
        up=(1+g*s.exp(e*h[i]))*invpi
        down=g*s.exp(e*h[(i-1)%n])*invpi
        Q[i,(i+1)%n]=up;Q[i,(i-1)%n]=down;Q[i,i]=-up-down
    Q0=Q.subs(e,0).applyfunc(simplify)
    Q1=Q.diff(e).subs(e,0).applyfunc(simplify)
    Q2=Q.diff(e,2).subs(e,0).applyfunc(simplify)
    phase=[s.simplify(s.cos(s.pi*i/3)+s.I*s.sin(s.pi*i/3)) for i in range(n)]
    right=s.Matrix(phase);left=(s.conjugate(right).T)/n
    lam=3*s.sqrt(3)*(-1+s.I)
    assert (Q0*right-lam*right).applyfunc(simplify)==s.zeros(n,1)
    assert (left*Q0-lam*left).applyfunc(simplify)==s.zeros(1,n)
    bordered=(Q0-lam*s.eye(n)).row_join(-right).col_join(left.row_join(s.zeros(1,1)))
    rhs=(-Q1*right).col_join(s.zeros(1,1))
    # Algebraic-domain inversion avoids approximate eigensolvers.
    field=s.QQ.algebraic_field(s.sqrt(3),s.I)
    domain_matrix=DomainMatrix.from_Matrix(bordered).convert_to(field)
    domain_rhs=DomainMatrix.from_Matrix(rhs).convert_to(field)
    answer=domain_matrix.inv().matmul(domain_rhs).to_Matrix()
    first=simplify(answer[-1]);assert first==0
    second=simplify((left*Q2*right+2*left*Q1*answer[:n,0])[0])
    lg=-6*(s.sqrt(3)-1)*(1-s.Rational(1,2));b=3*s.sqrt(3)
    shift=simplify(-(s.re(second)+s.im(second))/lg)
    A0=6*s.log((g+1)/g)
    A2=simplify(g/(g+1)**2*sum(hi*hi for hi in h)-shift*6/(g+1))
    Y0=A0/b
    Y2=simplify(Y0*(A2/A0-s.im(second)/b))
    return first,second,shift,Y2

def main():
    start=time.monotonic();rec=json.loads(Path('evidence/research-symbolic-curvature.json').read_text())
    t,v,L=s.symbols('t v L',positive=True,real=True);env={'t':t,'v':v,'L':L}
    expr={k:s.sympify(rec[k],locals=env) for k in ['hh','pp','hc','hs']}
    tval=1/s.sqrt(3);Lval=s.log((1+tval)/(1-tval));reports=[]
    for k,H,P,S in [(1,1,0,0),(1,0,1,0),(1,1,1,0),(1,1,0,1),(2,1,0,0),(3,1,0,0),(3,0,1,0),(3,1,1,0)]:
        h=[simplify(H*s.cos(s.pi*k*i/3)) for i in range(6)]
        p=[simplify(P*s.cos(s.pi*k*i/3)+S*s.sin(s.pi*k*i/3)) for i in range(6)]
        first,second,shift,y2=exact_second(h,p)
        if k==3:
            closed=2*s.limit(expr['hh']*H*H+expr['pp']*P*P,v,s.oo)
        else:
            closed=expr['hh']*H*H+expr['pp']*(P*P+S*S)+2*expr['hc']*H*P+2*expr['hs']*H*S
            closed=closed.subs(v,s.tan(s.pi*k/6))
        closed=s.simplify(closed.subs({t:tval,L:Lval}))
        error=s.simplify(s.expand_log(y2-closed,force=True))
        passed=error==0
        reports.append({'n':6,'k':k,'H':H,'P':P,'S':S,'lambda_first':str(first),
                        'lambda_second':str(second),'log_g_shift_second':str(shift),
                        'Y_second':str(y2),'closed_formula_difference':str(error),'pass':passed})
        print(json.dumps(reports[-1]),flush=True)
    out={'method':'direct differentiation and exact bordered full-matrix eigenderivative; algebraic sqrt(3) arithmetic',
         'independence':'same worker; code reads no discovery matrices or eigenvalues; closed formula used only for post-computation comparison',
         'checks':reports,'elapsed_seconds':time.monotonic()-start,'status':'pass' if all(r['pass'] for r in reports) else 'fail'}
    Path('evidence/research-exact-local-replay.json').write_text(json.dumps(out,indent=2)+'\n')
    if out['status']!='pass':raise SystemExit(1)

if __name__=='__main__':main()
