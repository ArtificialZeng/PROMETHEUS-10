"""Exact reduction and marginal-map checks for the full qutrit extension cone."""
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'evidence'

def ket(a,b,c):
    v=s.zeros(27,1); v[9*a+3*b+c]=1; return v

def swapket(a,b,c,sign=1):
    return ket(a,b,c) if b==c else (ket(a,b,c)+sign*ket(a,c,b))/s.sqrt(2)

def partial(M,which=2):
    if which==2:
        return s.Matrix(9,9,lambda i,j:sum(M[9*(i//3)+3*(i%3)+c,9*(j//3)+3*(j%3)+c] for c in range(3)))
    return s.Matrix(9,9,lambda i,j:sum(M[9*(i//3)+3*b+(i%3),9*(j//3)+3*b+(j%3)] for b in range(3)))

def basis_blocks():
    plus={}; minus={}; labels={}
    for a in range(3):
        for b in range(a+1):
            for c in range(b,a+1):
                q=b+c-a
                plus.setdefault(q,[]).append(swapket(a,b,c))
                labels.setdefault(('plus',q),[]).append((a,b,c))
                if b<c:
                    minus.setdefault(q,[]).append(swapket(a,b,c,-1))
                    labels.setdefault(('minus',q),[]).append((a,b,c))
    return {q:s.Matrix.hstack(*vs) for q,vs in plus.items()}, {q:s.Matrix.hstack(*vs) for q,vs in minus.items()}, labels

def symmetric_variables(n,prefix):
    M=s.zeros(n); variables=[]
    for i in range(n):
        for j in range(i,n):
            v=s.Symbol(f'{prefix}_{i}{j}',real=True); M[i,j]=M[j,i]=v; variables.append(v)
    return M,variables

def main():
    plus,minus,labels=basis_blocks()
    S=s.zeros(27)
    for a in range(3):
        for b in range(3):
            for c in range(3): S[9*a+3*c+b,9*a+3*b+c]=1
    U=s.Matrix.hstack(*(plus[q] for q in sorted(plus)),*(minus[q] for q in sorted(minus)))
    assert U.T*U==s.eye(14)
    assert all(S*B==B for B in plus.values())
    assert all(S*B==-B for B in minus.values())
    charge=s.diag(*[b+c-a for a in range(3) for b in range(3) for c in range(3)])
    assert all(charge*B==q*B for q,B in list(plus.items())+list(minus.items()))
    print('PASS: support dimension14, complete orthonormal swap/charge decomposition')
    print('Plus blocks:',{q:B.cols for q,B in sorted(plus.items())})
    print('Minus blocks:',{q:B.cols for q,B in sorted(minus.items())})
    # Test marginal-preserving transfer of every matrix unit, including complex ones.
    transfers=[]
    for q,B in sorted(minus.items()):
        indices=[labels[('plus',q)].index(t) for t in labels[('minus',q)]]
        C=plus[q][:,indices]
        for i in range(B.cols):
            for j in range(B.cols):
                assert partial(B[:,i]*B[:,j].T)==partial(C[:,i]*C[:,j].T)
        transfers.append({'charge':q,'plus_indices':indices,'matrix_units_checked':B.cols**2})
    print('PASS: all6 complex antisymmetric matrix units have exactly the same marginal after plus-sector transfer')
    names={-2:'z',-1:'R',0:'T',1:'V',2:'w'}
    X=s.zeros(27); blocks={}; variables=[]
    for q,B in sorted(plus.items()):
        M,vs=symmetric_variables(B.cols,names[q]); blocks[q]=M; variables+=vs; X+=B*M*B.T
    marg=partial(X).applyfunc(s.simplify)
    assert marg==partial(X,1).applyfunc(s.simplify)
    lam=s.Symbol('lam',nonnegative=True)
    J=s.zeros(9)
    # Fresh channel transcription, independent of reduction-variable construction.
    for m in range(3):
        for n in range(3):
            for ell in range(min(m,n)+1):
                J[3*m+m-ell,3*n+n-ell]+=2**(-s.Rational((m-n)**2,2))*s.sqrt(s.binomial(m,ell)*s.binomial(n,ell))*(1-lam)**ell*lam**(s.Rational(m+n,2)-ell)
    saved=json.loads((OUT/'input-a.json').read_text())
    savedJ=s.Matrix([[s.sympify(x,locals={'lam':lam}) for x in row] for row in saved['choi_ab']])
    assert (J/3-savedJ).applyfunc(s.simplify)==s.zeros(9)
    eqs=[]; locations=[]
    for i in range(9):
        for j in range(i,9):
            if marg[i,j]!=0 or J[i,j]!=0:
                eqs.append(marg[i,j]-J[i,j]);locations.append((i,j))
                print(f'marginal[{i},{j}]: {marg[i,j]} = {s.simplify(J[i,j])}')
    A,b=s.linear_eq_to_matrix(eqs,variables)
    assert A.rank()==10 and len(variables)==18
    print('PASS: 18 real variables, 10 independent constraints; exact comparison to all81 reconstructed Choi entries')
    data={'normalization':'X here is3 times normalized extension; marginal=3J; divide X by3 for trace1',
          'support_dimension':14,'plus_dimensions':{str(q):B.cols for q,B in sorted(plus.items())},
          'minus_dimensions':{str(q):B.cols for q,B in sorted(minus.items())},
          'plus_basis':{str(q):labels[('plus',q)] for q in sorted(plus)},
          'minus_basis':{str(q):labels[('minus',q)] for q in sorted(minus)},
          'antisymmetric_transfer':transfers,'real_variables':[str(v) for v in variables],
          'blocks':{str(q):[[str(x) for x in M.row(i)] for i in range(M.rows)] for q,M in blocks.items()},
          'marginal_locations':locations,'constraint_matrix':[[str(x) for x in A.row(i)] for i in range(A.rows)],
          'constraint_rhs':[str(s.simplify(x)) for x in b],
          'nullity':8,'constraint_rank':10,'checks':'exact SymPy identities; proof of necessity in research-reduction.md'}
    (OUT/'qutrit-reduction.json').write_text(json.dumps(data,indent=2)+'\n')

if __name__=='__main__': main()
