"""Independent explicit rate transcription and characteristic series checker.
No import of search implementation or construction. Rational arithmetic only.
"""
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path
import json

# Destination row/departure column. State energies [0,1,2].
HOT=[[F(0),F(9,1024),F(81,256)],
     [F(1,144),F(0),F(72)],
     [F(16,81),F(512,9),F(0)]]
COLD=[[F(0),F(1,16),F(4)],
      [F(1,1024),F(0),F(1024)],
      [F(1,1024),F(16),F(0)]]

def add(a,b): return [x+y for x,y in zip(a,b)]
def mul(a,b): return [sum(a[j]*b[k-j] for j in range(k+1)) for k in range(5)]
def det(a):
    ans=[F(0)]*5
    for p in permutations(range(3)):
        sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        term=[F(1)]+[F(0)]*4
        for i in range(3): term=mul(term,a[i][p[i]])
        ans=add(ans,[sign*v for v in term])
    return ans

def characteristic(selected=0,scale=F(1),reverse=False):
    # Separate heat transcription using state labels equal to energies.
    w=[[[F(0)]*5 for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            if i==j:
                w[i][j][0]=-scale*sum(HOT[k][j]+COLD[k][j] for k in range(3))
            else:
                heat=(j-i)*(-1 if reverse else 1)
                rates=[HOT[i][j],COLD[i][j]]
                w[i][j][0]=scale*sum(rates)
                for m in range(1,5): w[i][j][m]=scale*rates[selected]*F(heat**m,factorial(m))
    def residual(lam):
        mat=[[[ -v for v in w[i][j]] for j in range(3)] for i in range(3)]
        for i in range(3): mat[i][i]=add(mat[i][i],lam)
        return det(mat)
    # P(lambda,0)=lambda^3 + A lambda^2 + B lambda, B>0.
    # B is sum of principal 2x2 minors; zero is simple.
    B=sum(w[i][i][0]*w[j][j][0]-w[i][j][0]*w[j][i][0] for i in range(3) for j in range(i+1,3))
    assert B>0
    lam=[F(0)]*5
    assert residual(lam)[0]==0
    for m in range(1,5):
        const=residual(lam)[m]
        trial=lam[:]; trial[m]=1
        slope=residual(trial)[m]-const
        assert slope==B
        lam[m]=-const/B
        assert residual(lam)[:m+1]==[0]*(m+1)
    # Extract P(x,s)=x^3+A*x^2+B(s)*x+C(s) without another solver.
    C=residual([F(0)]*5)
    plus=residual([F(1)]+[F(0)]*4)
    minus=residual([F(-1)]+[F(0)]*4)
    Bs=[(plus[m]-minus[m])/2-(1 if m==0 else 0) for m in range(5)]
    As=[(plus[m]+minus[m])/2-C[m] for m in range(5)]
    assert As[1:]==[0]*4 and Bs[0]==B
    coefficients={'A':As[0], 'B_derivatives':[factorial(m)*Bs[m] for m in range(5)],
                  'C_derivatives':[factorial(m)*C[m] for m in range(5)]}
    return [factorial(m)*lam[m] for m in range(1,5)],B,residual(lam),coefficients

def main():
    for matrix,b in [(HOT,F(9,8)),(COLD,F(8))]:
        for i in range(3):
            for j in range(i+1,3):
                assert matrix[i][j]>0 and matrix[j][i]>0
                assert matrix[i][j]/matrix[j][i]==b**(2*(j-i))
    c,B,res,coefficients=characteristic()
    other,_,_,_=characteristic(selected=1)
    reverse,_,_,_=characteristic(reverse=True)
    scaled,_,_,_=characteristic(scale=F(1,1024))
    assert other==[(-1)**m*c[m-1] for m in range(1,5)]
    assert reverse==other and scaled==[v/1024 for v in c]
    assert c[1]>0 and c[3]<0
    # Hand-reviewable scalar implicit-differentiation recurrences.
    A=coefficients['A']; b=coefficients['B_derivatives']; h=coefficients['C_derivatives']
    d1=-h[1]/b[0]
    d2=-(2*A*d1*d1+2*b[1]*d1+h[2])/b[0]
    d3=-(6*d1**3+6*A*d1*d2+3*b[1]*d2+3*b[2]*d1+h[3])/b[0]
    d4=-(36*d1*d1*d2+A*(8*d1*d3+6*d2*d2)+4*b[1]*d3+6*b[2]*d2+4*b[3]*d1+h[4])/b[0]
    assert [d1,d2,d3,d4]==c
    # Comparison only after independently constructing and solving.
    search=json.loads(Path('evidence/three-state-search.json').read_text())
    assert c==list(map(F,search['negative'][0]['cumulants']))
    out={'method':'explicit thermal matrices; truncated characteristic determinant in Q[s]/(s^5)',
         'hot_rates':HOT,'cold_rates':COLD,'energies':[0,1,2],
         'beta_times_energy_unit':['2 ln(9/8)','2 ln(8)'],
         'stationary_branch_simple_B':B,'determinant_residual_coefficients_0_to_4':res,
         'characteristic_coefficients':coefficients,
         'cumulants':c,'decimal_cumulants':[float(v) for v in c],
         'ratio':c[3]/c[1],'decimal_ratio':float(c[3]/c[1]),
         'checks':{'detailed_balance':'exact pass','all_reverse_rates_positive':'pass',
                   'irreducible':'complete graph, pass','search_poisson_comparison':'exact pass',
                   'both_bath_cumulants':'exact opposite odd/equal even, pass',
                   'scalar_implicit_derivative_recurrences':'exact pass',
                   'heat_reversal':'exact pass','all_rates_at_most_one_rescaling':'exact pass'},
         'rescaled_cumulants':scaled,'independence':'same agent; distinct construction and algorithm, not fresh referee'}
    Path('evidence/witness-check.json').write_text(json.dumps(out,default=str,indent=2)+'\n')
    print(json.dumps(out,default=str,indent=2))

if __name__=='__main__': main()
