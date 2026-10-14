#!/usr/bin/env python3
"""Input A only: explicit 512-component state and ordinary partial traces."""
from pathlib import Path
import json
from math import comb
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'evidence/reproduce-20261012-input-a.json'
OUTPUT = ROOT / 'evidence/reproduce-20261012-output-a.json'
z = s.Symbol('z', nonzero=True)

def star(x):
    return s.conjugate(x).subs(s.conjugate(z), 1/z)

def clean(x):
    return s.simplify(s.expand(x))

def serialized(m):
    return [[str(x) for x in row] for row in m.tolist()]

def main():
    obj = json.loads(INPUT.read_text())
    N = obj['N']
    c = [s.S.Zero]*(N+1)
    for term in obj['spin_terms']:
        k = (term['twice_m']+N)//2
        assert 2*k-N == term['twice_m']
        c[k] = s.sympify(term['coefficient'], locals={'z':z})
    psi = [c[x.bit_count()]/s.sqrt(comb(N,x.bit_count())) for x in range(1<<N)]
    norm = clean(sum(v*star(v) for v in psi))
    assert norm == 1
    # All adjacent swaps generate the permutation group.
    for site in range(N-1):
        for x in range(1<<N):
            a,b=(x>>site)&1,(x>>(site+1))&1
            y=x if a==b else x^(1<<site)^(1<<(site+1))
            assert psi[x] == psi[y]
    results = {}
    for t in range(1,5):
        env = 1<<(N-t)
        rho = s.Matrix(1<<t,1<<t,lambda x,y:clean(sum(
            psi[x*env+e]*star(psi[y*env+e]) for e in range(env))))
        D = s.Matrix(1<<t,t+1,lambda x,r:
            1/s.sqrt(comb(t,int(r))) if int(x).bit_count()==r else 0)
        assert D.T*D == s.eye(t+1)
        reduced = (D.T*rho*D).applyfunc(clean)
        support = (rho-D*reduced*D.T).applyfunc(clean)
        assert support == s.zeros(1<<t)
        assert clean(s.trace(rho)) == 1
        assert (rho-star_matrix(rho).T).applyfunc(clean) == s.zeros(1<<t)
        purity = clean(s.trace(rho*rho))
        A = clean(s.Rational(t+1,t)*(1-purity))
        expected=s.sympify(obj['published_checks'][f'A{t}'],locals={'z':z})
        assert clean(A-expected)==0, (t,A,expected)
        if t<=2:
            assert reduced == s.eye(t+1)/s.Integer(t+1)
        results[str(t)]={'rho_full':serialized(rho),'rho_sym':serialized(reduced),
                         'purity':str(purity),'A':str(A),'source_residual':'0',
                         'support_residual':'0','hermiticity_residual':'0','trace':'1'}
        print(f'A: t={t}; purity={purity}; A_t={A}; exact published residual=0', flush=True)
    # Spin normalization checked as operator identities and on the state.
    j=s.Rational(N,2)
    Jz=s.diag(*[s.Integer(k)-j for k in range(N+1)])
    Jp=s.zeros(N+1)
    for k in range(N): Jp[k+1,k]=s.sqrt((N-k)*(k+1))
    Jm=Jp.T
    Jx=(Jp+Jm)/2
    Jy=(Jp-Jm)/(2*s.I)
    operators=[Jx,Jy,Jz]
    assert (Jx*Jy-Jy*Jx-s.I*Jz).applyfunc(clean)==s.zeros(N+1)
    assert (Jx*Jx+Jy*Jy+Jz*Jz-j*(j+1)*s.eye(N+1)).applyfunc(clean)==s.zeros(N+1)
    ket=s.Matrix(c); bra=star_matrix(ket).T
    means=[clean((bra*J*ket)[0]) for J in operators]
    second=s.Matrix(3,3,lambda a,b:clean((bra*(operators[a]*operators[b]+operators[b]*operators[a])*ket)[0]/2))
    assert means==[0,0,0]
    assert second==s.eye(3)*s.Rational(33,4)
    out={'implementation':'explicit computational bitstring trace; no input B read',
         'input_file':str(INPUT.relative_to(ROOT)),'N':N,'phase_ring':'Laurent expressions in z, star(z)=1/z',
         'norm':str(norm),'permutation_symmetry':'all adjacent swaps verified',
         'coefficients_k':[str(v) for v in c],'marginals':results,
         'spin_checks':{'commutator_residual':'0','casimir_residual':'0',
                        'means':[str(v) for v in means],
                        'symmetrized_second_moment':serialized(second)}}
    OUTPUT.write_text(json.dumps(out,indent=2)+'\n')
    print('A: normalization, permutation symmetry, symmetric support, spin commutator and Casimir checks PASS')

def star_matrix(M):
    return M.applyfunc(star)

if __name__=='__main__': main()
