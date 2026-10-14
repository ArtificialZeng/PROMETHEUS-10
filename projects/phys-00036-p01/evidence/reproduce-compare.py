#!/usr/bin/env python3
"""Exact comparison of independently generated artifacts, published baselines and input legality."""
import json,math,datetime,hashlib
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def load(name):return json.loads((ROOT/name).read_text())
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2)+'\n')
def add(*args):
    out={}
    for a in args:
        for p,c in a.items():out[p]=out.get(p,0)+c
    return {p:c for p,c in out.items() if c}
def scale(a,n):return {p:c*n for p,c in a.items() if c*n}
def mm(a,b):
    byrow={}
    for (r,c),v in b.items():byrow.setdefault(r,[]).append((c,v))
    out={}
    for (r,k),u in a.items():
        for c,v in byrow.get(k,[]):out[r,c]=out.get((r,c),0)+u*v
    return {p:c for p,c in out.items() if c}
def decode(a):return {(r,c):v for r,c,v in a}
def encode(a):return [[r,c,str(v)] for (r,c),v in sorted(a.items())]
def perm_matrix(p):
    # Independent checker action: each source tensor factor i moves to target p[i].
    n=len(p);out={}
    for c in range(2**n):
        dest=0
        for i,j in enumerate(p):dest|=((c>>(n-1-i))&1)<<(n-1-j)
        out[dest,c]=1
    return out
def perm_sum_to_matrix(terms):return add(*(scale(perm_matrix([i-1 for i in t['permutation']]),t['coefficient']) for t in terms))
def local_symbol(k,p):return perm_matrix([i-1 for i in p]+list(range(len(p),k)))
def cyclic_sum(M,k,L):
    columns={}
    for (r,c),v in M.items():columns.setdefault(c,[]).append((r,v))
    out={}
    for start in range(L):
        sites=[(start+i)%L for i in range(k)]
        for c in range(2**L):
            smallc=0
            for site in sites:smallc=2*smallc+((c>>(L-1-site))&1)
            for smallr,v in columns.get(smallc,[]):
                r=c
                for j,site in enumerate(sites):
                    mask=1<<(L-1-site);r=(r&~mask)|(((smallr>>(k-1-j))&1)<<(L-1-site))
                out[r,c]=out.get((r,c),0)+v
    return {p:c for p,c in out.items() if c}
def gradient(m,k):
    out={}
    for (r,c),v in m.items():
        for i in range(2):
            out[(i*2**(k-1)+r,i*2**(k-1)+c)]=out.get((i*2**(k-1)+r,i*2**(k-1)+c),0)+v
            out[(2*r+i,2*c+i)]=out.get((2*r+i,2*c+i),0)-v
    return {p:c for p,c in out.items() if c}
def solve_gradient(D,k):
    d=2**(k-1);pivots={};inconsistent=[]
    for r in range(2*d):
        for c in range(2*d):
            eq={};rhs=Fraction(D.get((r,c),0))
            if r//d==c//d:eq[(r%d)*d+c%d]=Fraction(1)
            if r%2==c%2:
                j=(r//2)*d+c//2;eq[j]=eq.get(j,Fraction(0))-1
            eq={j:v for j,v in eq.items() if v}
            while eq:
                j=min(eq);v=eq[j]
                if j in pivots:
                    old,oldrhs=pivots[j]
                    for t,w in old.items():eq[t]=eq.get(t,Fraction(0))-v*w
                    eq={t:w for t,w in eq.items() if w};rhs-=v*oldrhs
                else:
                    pivots[j]=({t:w/v for t,w in eq.items()},rhs/v);break
            if not eq and rhs:inconsistent.append([r,c,str(rhs)])
    if inconsistent:return None,{'inconsistent_equations':inconsistent}
    x={}
    for j in sorted(pivots,reverse=True):
        row,rhs=pivots[j];x[j]=rhs-sum(v*x.get(t,0) for t,v in row.items() if t!=j)
    m={(j//d,j%d):v for j,v in x.items() if v}
    residual=add(D,scale(gradient(m,k),-1))
    return m,{'rank':len(pivots),'unknowns':d*d,'free_variables_set_zero':d*d-len(pivots),'residual_nonzero_entries':len(residual)}
def yb_polynomial_check():
    n=3;identity=tuple(range(n))
    def swap(i,j):
        p=list(identity);p[i],p[j]=p[j],p[i];return tuple(p)
    def pm(A,B):
        out={}
        for (p,a,b),v in A.items():
            for (q,c,d),w in B.items():
                key=(tuple(p[q[i]] for i in range(n)),a+c,b+d);out[key]=out.get(key,0)+v*w
        return {k:v for k,v in out.items() if v}
    def pa(A,B):
        out=A.copy()
        for k,v in B.items():out[k]=out.get(k,0)+v
        return {k:v for k,v in out.items() if v}
    X={(swap(0,1),0,0):1,(identity,1,0):-1}
    Z={(swap(0,2),0,0):1,(identity,1,0):-1,(identity,0,1):-1}
    Y={(swap(1,2),0,0):1,(identity,0,1):-1}
    left=pm(pm(X,Z),Y);right=pm(pm(Y,Z),X)
    residual=pa(left,{k:-v for k,v in right.items()})
    assert not residual
    return {'identity':'(P12-xI)(P13-(x+y)I)(P23-yI)=(P23-yI)(P13-(x+y)I)(P12-xI)',
        'variables':'x=u1-u2; y=u2-u3; u1-u3=x+y',
        'common_denominator':'(1-x)(1-x-y)(1-y)',
        'exact_polynomial_residual_terms':len(residual),'basis':'Formal S3 permutation algebra, not a sample-point or projected-sector check'}
def main():
    A=load('evidence/reproduce-input-a.json');B=load('evidence/reproduce-input-b.json')
    rowchecks=[]
    for degree in range(4):
        for row in range(4):
            equal=A['R_taylor_coefficients'][str(degree)][row]==B['R_taylor_coefficients'][str(degree)][row]
            rowchecks.append({'degree':degree,'row':row,'equal':equal});assert equal
    TA=load('evidence/reproduce-transfer-a.json');TB=load('evidence/reproduce-transfer-b.json');BB=load('evidence/reproduce-block-b.json')
    result={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'row_by_row_input_checks':rowchecks,'basis_map':'A and B both use column vectors in |00>,|01>,|10>,|11>; map is the identity. A site permutation sends factor i to p(i); B binary matrices implement the same action.',
        'full_R_map':'R=Pi_plus-(1+x)/(1-x)Pi_minus=(P-xI)/(1-x), Pi_plus=(I+P)/2, Pi_minus=(I-P)/2. This proves all-x equality, not only four Taylor coefficients.',
        'derivative_map':'Taylor coefficients carry no factorial; raw Q_k restores (k-2)!. Right-leg x=-s and one outer minus are retained, never equated with left at all k.',
        'transfer_comparisons':[],'local_and_global_baselines':[],'local_gradients':[]}
    baseline_terms=[(-1,[1]),(2,[2,1]),(-1,[3,2,1]),(1,[2,3,4,1]),(-1,[2,4,1,3]),(-1,[3,1,4,2]),(1,[4,1,2,3])]
    q={2:add(local_symbol(2,[1]),scale(local_symbol(2,[2,1]),-1)),
       3:add(local_symbol(3,[3,1,2]),scale(local_symbol(3,[2,3,1]),-1)),
       4:scale(add(*(scale(local_symbol(4,p),c) for c,p in baseline_terms)),-2)}
    for L in [4,5,6]:
        for k in [2,3,4]:
            a=perm_sum_to_matrix(TA[str(L)]['raw_charges'][str(k)]);b=decode(TB[str(L)]['raw_charges'][str(k)])
            residual=add(a,scale(b,-1));assert not residual
            result['transfer_comparisons'].append({'L':L,'k':k,'nonzero_residual_entries':len(residual),'all_entries_checked':2**(2*L)})
            left=cyclic_sum(decode(BB[str(k)]['left_density']),k,L);right=cyclic_sum(decode(BB[str(k)]['right_density']),k,L)
            published=cyclic_sum(q[k],k,L)
            rleft=add(left,scale(a,-1));rright=add(right,scale(a,-1));rpub=add(published,scale(a,-1))
            result['local_and_global_baselines'].append({'L':L,'k':k,'left_density_sum_residual_entries':len(rleft),'right_density_sum_residual_entries':len(rright),'published_charge_after_convention_map_residual_entries':len(rpub)})
            print(json.dumps({'L':L,'k':k,'A_minus_B_entries':len(residual),'left_minus_transfer_entries':len(rleft),'right_minus_transfer_entries':len(rright),'published_minus_transfer_entries':len(rpub)}),flush=True)
            assert not rleft and not rright and not rpub
            for pair in [('Q2_Q3',2,3),('Q2_Q4',2,4),('Q3_Q4',3,4)]:
                if k!=4:continue
                c=decode(TB[str(L)]['raw_charges'][str(pair[1])]);d=decode(TB[str(L)]['raw_charges'][str(pair[2])])
                assert not add(mm(c,d),scale(mm(d,c),-1))
    for k in [2,3,4]:
        for side in ['left','right']:
            D=add(decode(BB[str(k)][side+'_density']),scale(q[k],-1));m,info=solve_gradient(D,k)
            record={'k':k,'side':side,'equation':side+'_density - q_raw_BBL = I tensor m - m tensor I','difference_nonzero_entries':len(D),**info}
            if m is not None:record['witness_m_shape']=[2**(k-1),2**(k-1)];record['witness_m_sparse_entries']=encode(m)
            if k==4 and m is not None:
                I=local_symbol(3,[1]);h12=add(I,scale(local_symbol(3,[2,1]),-1));h23=add(I,scale(local_symbol(3,[1,3,2]),-1));h13=add(I,scale(local_symbol(3,[3,2,1]),-1))
                named=scale(h12,2) if side=='left' else add(scale(h12,4),scale(h23,2),scale(h13,-2))
                named_residual=add(m,scale(named,-1));assert not named_residual
                record['named_witness']='2(I-P12)' if side=='left' else '4(I-P12)+2(I-P23)-2(I-P13)'
                record['named_witness_matrix_residual_entries']=len(named_residual)
            result['local_gradients'].append(record);print(json.dumps({key:val for key,val in record.items() if key!='witness_m_sparse_entries'}),flush=True)
            assert m is not None and info['residual_nonzero_entries']==0
    result['published_map']={'Q2_BBL':'Q2_raw','Q3_BBL':'(i/2) Q3_raw','Q4_BBL':'-(1/6) Q4_raw',
        'derivation':'Primary Eq.(2.9) fixes site permutation direction. Exact transfer coefficient expansion gives Q2= [1]-[2,1], Q3=[3,1,2]-[2,3,1], Q4=-2 times the seven-term bracket of published Eq.(2.16). The displayed i/2 and 1/3 coefficients give these maps without dropping scalar or lower charges.'}
    write('evidence/reproduce-comparison.json',result)
    legality={'model':'XXX spin 1/2 input only','yb':yb_polynomial_check(),
        'regularity':'At x=0, R=P; every diagonal spectral evaluation u=v has x=0.',
        'braiding_normalization':'R12(x)R21(-x)=(P-xI)(P+xI)/((1-x)(1+x))=(I-x^2 I)/(1-x^2)=I, since P21=P12 and P^2=I.',
        'analyticity':'Analytic at x=0, nearest poles at x=1; inverse has pole at x=-1. Formal series checks require no continuation across either pole.',
        'transfer_zero':'Auxiliary trace of P_aL...P_a1 is right translation U; A and B agree and B verifies U transpose U=I at each tested L.',
        'hermiticity':'At zero h=I-P is real symmetric. Q3raw is real antisymmetric, so i Q3raw/2 is Hermitian; Q4raw is real symmetric.',
        'physical_units':'All algebraic quantities and spectral variables dimensionless; H=J Q2 with real J is the physical energy operator.',
        'boundary':'Periodic homogeneous untwisted L=4,5,6; all support k<=4. No weighted boost or thermodynamic limit has been used.',
        'coverage':'Full tensor Hilbert space and all spin sectors; no projection or numerical tolerance. Independent transfer matrices agree at every entry.',
        'commutators':'Q2,Q3,Q4 pairwise matrix commutators vanish exactly at L=4,5,6.',
        'universal_target_not_proved':'All-R/all-k identities and non-difference R have not been established by this reproduction.'}
    for L in [4,5,6]:
        for k in [2,3,4]:
            M=decode(TB[str(L)]['raw_charges'][str(k)]);Mt={(c,r):v for (r,c),v in M.items()}
            expected_sign=-1 if k==3 else 1;assert not add(M,scale(Mt,-expected_sign))
    write('evidence/reproduce-input-admissibility.json',legality)
    print(json.dumps({'input_row_checks':len(rowchecks),'YB_exact_polynomial_residual_terms':0,'pairwise_charge_commutators':'all zero','published_maps':result['published_map'],'scope':'Known reproduction only; no all-R or all-k claim'}),flush=True)
if __name__=='__main__':main()
