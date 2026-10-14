#!/usr/bin/env python3
"""A: primary R transcribed as a permutation polynomial; explicit auxiliary trace.
No imports from input B; all arithmetic is integer in the permutation algebra.
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def clean(a): return {p:c for p,c in a.items() if c}
def add(*args):
    out={}
    for a in args:
        for p,c in a.items(): out[p]=out.get(p,0)+c
    return clean(out)
def scale(a,n): return clean({p:c*n for p,c in a.items()})
def compose(p,q): return tuple(p[i] for i in q)
def mul(a,b):
    out={}
    for p,c in a.items():
        for q,d in b.items():
            pq=compose(p,q);out[pq]=out.get(pq,0)+c*d
    return clean(out)
def transposition(n,i,j):
    p=list(range(n));p[i],p[j]=p[j],p[i];return tuple(p)
def inverse(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def partial_trace_aux(p,dim):
    factor=dim if p[0]==0 else 1
    q=tuple((p[0] if p[i]==0 else p[i])-1 for i in range(1,len(p)))
    return q,factor
def transfer(L,order,dim=2):
    identity=tuple(range(L+1));poly=[{identity:1}]+[{} for _ in range(order)]
    for site in range(1,L+1):
        swap={transposition(L+1,0,site):1}
        poly=[add(mul(swap,poly[n]),scale(poly[n-1],-1) if n else {}) for n in range(order+1)]
    traced=[]
    for a in poly:
        b={}
        for p,c in a.items():
            q,f=partial_trace_aux(p,dim);b[q]=b.get(q,0)+c*f
        traced.append(clean(b))
    assert len(traced[0])==1 and list(traced[0].values())==[1]
    U=next(iter(traced[0]));Ui={inverse(U):1}
    X=[]
    for n in range(order+1):
        tn=add(*(scale(traced[j],math.comb(L+n-j-1,n-j)) for j in range(n+1)))
        X.append(mul(Ui,tn))
    I={tuple(range(L)):1};assert X[0]==I
    Y=[I]
    for n in range(1,order):Y.append(scale(add(*(mul(X[j],Y[n-j]) for j in range(1,n+1))),-1))
    Q={}
    for k in range(2,order+2):
        n=k-2
        Q[k]=scale(add(*(scale(mul(Y[j],X[n-j+1]),n-j+1) for j in range(n+1))),math.factorial(n))
    return U,X,Q
def translated_symbol(L,symbol):
    n=len(symbol);out={}
    for start in range(L):
        sites=[(start+i)%L for i in range(n)];p=list(range(L))
        for i,j in enumerate(symbol):p[sites[i]]=sites[j-1]
        p=tuple(p);out[p]=out.get(p,0)+1
    return out
def encode(a):return [{'permutation':[i+1 for i in p],'coefficient':c} for p,c in sorted(a.items())]
def main():
    rows=[['1','0','0','0'],['0','-x/(1-x)','1/(1-x)','0'],['0','1/(1-x)','-x/(1-x)','0'],['0','0','0','1']]
    I=tuple(range(2));P=transposition(2,0,1)
    # Direct row transcription of Eq.(3.56); x=u-v, column-vector lexicographic basis.
    input_data={'source_id':'S1','locator':'Eq.(3.56), PDF p.43 / printed p.42',
      'method':'Direct operator and row transcription from primary formula and swap definition',
      'basis':['00','01','10','11'],'spectral_variable':'x=u-v','matrix_rows':rows,
      'R_taylor_coefficients':{'0':[[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],
        **{str(n):[[0,0,0,0],[0,-1,1,0],[0,1,-1,0],[0,0,0,0]] for n in range(1,4)}},
      'transfer_order':'R_aL ... R_a1; site permutation maps old site to new site',
      'charge_derivative':'Q_k=(k-2)! [u^(k-2)] (t^-1 t prime)',
      'source_product_order':'R_AB: first block ascending, second block descending',
      'left_derivative':'D_A^(k-2)(R_AB^-1 D_A R_AB)',
      'right_derivative':'-D_B^(k-2)(R_AB^-1 D_B R_AB)',
      'lower_block_embedding':'Original site labels retained, empty block contributes zero'}
    (ROOT/'evidence/reproduce-input-a.json').write_text(json.dumps(input_data,indent=2)+'\n')
    output={};failures=[]
    for L in [4,5,6]:
        U,X,Q=transfer(L,3)
        expected2=add(translated_symbol(L,[1]),scale(translated_symbol(L,[2,1]),-1))
        expected3=add(translated_symbol(L,[3,1,2]),scale(translated_symbol(L,[2,3,1]),-1))
        r2=add(Q[2],scale(expected2,-1));r3=add(Q[3],scale(expected3,-1))
        # BBL's third charge is i/2 times this real antisymmetric raw charge.
        output[str(L)]={'U':list(U),'raw_charges':{str(k):encode(q) for k,q in Q.items()},
          'baseline_Q2_residual_terms':len(r2),'baseline_Q3_after_i_over_2_residual_terms':len(r3),
          'numerator_partial_trace':'Auxiliary permutation cycle eliminated exactly; auxiliary fixed cycle gives local dimension',
          'series_order':3,'full_hilbert_dimension':2**L}
        print(json.dumps({'route':'A','L':L,'Q2_residual_terms':len(r2),'Q3_residual_terms':len(r3),'Q4_terms':len(Q[4]),'arithmetic':'exact integers'}),flush=True)
        if r2 or r3:failures.append(L)
    (ROOT/'evidence/reproduce-transfer-a.json').write_text(json.dumps(output,indent=2)+'\n')
    assert not failures,failures
if __name__=='__main__':main()
