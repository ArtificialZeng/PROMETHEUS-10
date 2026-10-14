"""Symbolic row-by-row equality of two source representations, not attainment."""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
c,h,r,lam,C,q=s.symbols('c h r lambda C q',real=True)
nx,ny,nz=s.symbols('nx ny nz',real=True);ns=[nx,ny,nz]
I=s.eye(2)
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.Matrix([[1,0],[0,-1]])]
W=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])

def zeros(m):return [[str(s.simplify(m[i,j])) for j in range(m.cols)] for i in range(m.rows)]
def iszero(rows):return all(z=='0' for row in rows for z in row)

def direction_average(expr):
    p=s.Poly(s.expand(expr),nx,ny,nz);answer=0
    for powers,coef in p.terms():
        degree=sum(powers)
        if degree==0:answer+=coef
        elif any(v%2 for v in powers):pass
        elif degree==2:answer+=coef/s.Integer(3)
        else:raise ValueError('unexpected angular degree')
    return s.expand(answer)

def main():
    # A: matrix-unit Choi, source input-output order; separate symbolic transcription.
    u=c*I-s.I*h*sum((n*p for n,p in zip(ns,pauli)),s.zeros(2))
    ja=s.zeros(4)
    for a in range(2):
        for b in range(2):
            e=s.zeros(2);e[a,b]=1
            ja+=s.kronecker_product(e,(1-lam)*u*e*u.adjoint()+lam*s.trace(e)*I/2)
    # B: separately transcribed source spin columns and Eq.20.
    S=s.Matrix([[1,0,0,1],[0,1,s.I,0],[0,1,-s.I,0],[1,0,0,-1]])/s.sqrt(2)
    vb=S*s.Matrix([c,-s.I*h*nx,-s.I*h*ny,-s.I*h*nz])
    jb=2*(1-lam)*vb*vb.adjoint()+lam*s.eye(4)/2
    pointwise=zeros(ja-jb);orth=zeros(S.adjoint()*S-s.eye(4))
    rho=W*ja*W/2
    angular0=rho.applyfunc(direction_average)
    ga=[angular0.applyfunc(lambda z:s.expand(z).subs(c**2,C).subs(h**2,1-C))]
    for ni in ns:
        gi=(r*ni*rho).applyfunc(direction_average)
        ga.append(gi.applyfunc(lambda z:s.expand(z).subs(c*h*r,3*q)))
    spin0=s.diag((1-lam)*C+lam/4,(1-lam)*(1-C)/3+lam/4,
                 (1-lam)*(1-C)/3+lam/4,(1-lam)*(1-C)/3+lam/4)
    gb=[spin0]
    for i in range(1,4):
        m=s.zeros(4);m[0,i]=s.I*(1-lam)*q;m[i,0]=-s.I*(1-lam)*q;gb.append(m)
    T=W*S
    moment_rows=[zeros(ga[i]-T*gb[i]*T.adjoint()) for i in range(4)]
    aa=s.pi/4;t=s.symbols('t',real=True)
    c_rad=s.integrate(3*t**2*s.cos(t)**2/aa**3,(t,0,aa))
    q_rad=s.integrate(t**3*s.sin(t)*s.cos(t)/aa**3,(t,0,aa))
    radial=[str(s.simplify(c_rad-(s.Rational(1,2)+3/(4*aa)-3/(8*aa**3)))),
            str(s.simplify(q_rad-(3/(8*aa)-3/(16*aa**3))))]
    report={'kind':'exact source-input algebra check only','symbolic_assumptions':'c,h,r,lambda,C,q,nx,ny,nz real; c=cos r,h=sin r,C=E cos^2 r,q=E[r sin r cos r]/3; uniform directions',
            'spin_basis_orthonormality_row_residuals':orth,
            'source_choi_16_entry_residuals':pointwise,
            'four_moment_64_entry_residuals':moment_rows,
            'independent_radial_integral_residuals':radial,
            'all_exact_entries_match':iszero(orth) and iszero(pointwise) and all(iszero(m) for m in moment_rows) and radial==['0','0'],
            'limitations':'These exact identities validate input maps and integral coefficients. They do not evaluate the NH optimum or prove that its moment variables arise from a physical POVM.'}
    (OUT/'exact-input-map.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    assert report['all_exact_entries_match']

if __name__=='__main__':main()
