"""Exact comparison and published-baseline replay AFTER separate A/B construction."""
import datetime
import hashlib
import json
from pathlib import Path
import sys
import sympy as sp
import input_a as a
import input_b as b

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def zero(m):
    return all(sp.simplify(q) == 0 for q in m)


def read_matrix(v):
    return sp.Matrix([[sp.sympify(q, locals={'x': a.X_WEIGHT, 'y': a.Y_WEIGHT})
                       for q in row] for row in v])


def partial_output(jmat, d):
    return sp.Matrix(d,d,lambda i,j:sum(jmat[i*d+k,j*d+k] for k in range(d)))


def partial_input(jmat, d):
    return sp.Matrix(d,d,lambda i,j:sum(jmat[k*d+i,k*d+j] for k in range(d)))


def main():
    ca, bl = [], []
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    header = [f'Actual replay at {stamp}', 'Job phys-00027-p01-reproduce-e7d47effda86',
              f'Python {sys.version}', f'SymPy {sp.__version__}',
              'Exact symbolic/rational arithmetic; no floating-point tolerance or numerical enclosure used.',
              'Invocation: python3 evidence/reproduce/check_reproduction.py']
    ca += header
    bl += header
    for name in ['input_a.py','input_b.py','input-a.json','input-b.json','check_reproduction.py','input-b.md']:
        ca.append(f'SHA256 {name} {hashlib.sha256((OUT/name).read_bytes()).hexdigest()}')
    ja, jb = [json.loads((OUT/name).read_text()) for name in ['input-a.json','input-b.json']]
    for key in ['symbolic_d3_superoperator','symbolic_d3_choi']:
        ma, mb = read_matrix(ja[key]), read_matrix(jb[key])
        assert zero(ma-mb), key
        ca.append(f'PASS saved input A/B {key}: all {ma.rows*ma.cols} entries identical exactly.')
    ca.append('Map: source 1-based -> local 0-based; J input tensor output; S[a+d*b,i+d*j]=J[i*d+a,j*d+b].')
    ca.append('B does not import/read A; this checker imports both only after separate records were generated.')
    for d in [3,4,5,6]:
        x,y = a.X_WEIGHT,a.Y_WEIGHT
        sa,sb = a.superoperator(d,x,y), b.superoperator(d,x,y)
        j1,j2 = a.choi(d,x,y), b.choi(d,x,y)
        assert zero(sa-sb) and zero(j1-j2)
        assert zero(partial_output(j2,d)-sp.eye(d))
        assert zero(partial_input(j2,d)-sp.eye(d))
        assert zero(j2-j2.H)
        basis = b.weighted_basis(d,x,y)
        gram = sp.Matrix([[sp.trace(f.H*g) for _,_,g in basis] for _,_,f in basis])
        assert zero(gram-sp.eye(d*d))
        ktp = sp.zeros(d)
        for label,w,f in basis:
            ktp += w*f.H*f
        assert zero(ktp-sp.eye(d))
        # Matrix-unit equality of independently reconstructed Kraus action.
        for i in range(d):
            for j in range(d):
                e = a.matrix_unit(d,i,j)
                assert zero(a.direct_map(e,x,y)-b.apply_kraus(e,x,y))
                assert zero(a.direct_map(e.T,x,y)-a.direct_map(e,x,y).H)
        # Known symmetric/antisymmetric operator sectors, not Choi sectors.
        t,beta = 1-x-y,y/(d+1)-x/(d-1)
        for label,w,f in basis:
            eigen = 1 if label == 'omega' else (t-beta if label.startswith('antisymmetric') else t+beta)
            assert zero(a.direct_map(f,x,y)-eigen*f)
        ca.append(f'PASS d={d}, symbolic x,y: A/B superoperator and Choi all {d**4} entries; '
                  f'{d*d} matrix units; Kraus TP; Choi TP/unital/Hermiticity; orthonormal basis; operator sectors.')
    # Legal but degenerate/singular/negative-spectrum inputs test conventions.
    cases = [(3,sp.Rational(1,2),sp.Rational(1,3),'singular symmetric operator sector'),
             (3,sp.Rational(1,2),sp.Rational(1,2),'triangle edge; negative symmetric operator eigenvalue'),
             (4,sp.Rational(1,3),sp.Rational(2,3),'d=4 triangle edge'),
             (5,sp.Rational(1,5),sp.Rational(3,10),'isotropic/depolarizing line')]
    for d,x,y,desc in cases:
        ja1,jb1=a.choi(d,x,y),b.choi(d,x,y)
        weights=[sp.simplify(w) for _,w,_ in b.weighted_basis(d,x,y)]
        assert x>0 and y>0 and x+y<=1 and all(w>0 for w in weights)
        assert zero(ja1-jb1) and ja1.rank()==d*d
        s=sp.simplify(1-x-y+y/(d+1)-x/(d-1))
        anti=sp.simplify(1-x-y-y/(d+1)+x/(d-1))
        ca.append(f'PASS input witness d={d},x={x},y={y}: {desc}; '
                  f'Choi rank {d*d}, positive sector weights; operator s={s},a={anti}. No embedding inference.')
    d,x,y=3,sp.Rational(1,4),sp.Rational(1,4)
    psi=sp.Matrix([sp.I,1,0])/sp.sqrt(2)
    rho=psi*psi.H
    assert (psi.H*psi)[0]==1 and sp.trace(rho)==1 and zero(rho*rho-rho)
    oa,ob=a.direct_map(rho,x,y),b.apply_kraus(rho,x,y)
    assert zero(oa-ob)
    for obj in [ja,jb]:
        assert zero(read_matrix(obj['benchmark']['output'])-oa)
    # Separately transcribed from the inspected primary PDF p6 Eq. (30).
    xd,yd=x/(d-1),y/(d+1)
    expected=[2*yd,1-(d-2)*xd-d*yd]+[xd+yd]*(d-2)
    z=sp.Symbol('z')
    cp=oa.charpoly(z).as_expr()
    published=sp.prod(z-l for l in expected)
    assert sp.expand(cp-published)==0
    eig=oa.eigenvals()
    assert sorted(eig)==sorted(expected) and all(v==1 for v in eig.values())
    assert zero(oa-oa.H) and sp.trace(oa)==1 and all(v>0 for v in eig)
    bl.append('Primary source: literature/2405.11216v3.pdf, PDF p6 Eqs. (28),(30); Eq. (14) p3.')
    bl.append(f'Legal benchmark d={d}, x={x}, y={y}; xd={xd}, yd={yd}; yd<xd verified.')
    assert yd<xd
    bl.append('rho = '+str(rho))
    bl.append('Direct A output = '+str(oa))
    bl.append('Choi/Kraus B output = '+str(ob))
    bl.append('Published Eq. (30) evaluated spectrum (source order) = '+str(expected))
    bl.append('Exact independently computed spectrum A and B = '+str(eig))
    bl.append('Characteristic polynomial = '+str(cp))
    bl.append('Exact factorization = '+str(sp.factor(cp)))
    bl.append('PASS: output Hermitian positive definite, trace one; exact polynomial equality to published spectrum.')
    jmat=b.choi(d,x,y)
    jeig=jmat.eigenvals()
    assert jeig=={sp.Rational(13,8):1,sp.Rational(1,8):5,sp.Rational(1,4):3}
    assert sp.trace(jmat)==d and sp.trace(jmat/d)==1
    bl.append('Unnormalized Choi eigenvalues = '+str(jeig)+'; trace='+str(sp.trace(jmat)))
    bl.append('Normalized Choi eigenvalues = '+str((jmat/d).eigenvals())+'; trace=1')
    bl.append('Superoperator eigenvalues = '+str(a.superoperator(d,x,y).eigenvals()))
    bl.append('PASS known source output spectrum only. No minimum-entropy optimization, generator or novelty result asserted.')
    ca.append('PASS exact general-d correspondence also derived in evidence/reproduce/input-b.md; finite script checks do not alone prove all d.')
    (OUT/'input-comparison.log').write_text('\n'.join(ca)+'\n')
    (OUT/'baseline.log').write_text('\n'.join(bl)+'\n')
    print('\n'.join(ca[-8:]+bl[-10:]))


if __name__=='__main__':
    main()
