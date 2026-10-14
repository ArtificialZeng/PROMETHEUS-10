#!/usr/bin/env python3
"""B: independent two-spin spectral-projector construction and sparse tensor matrices.
Reads no A artifacts and imports no A functions. Only the primary formula is shared.
"""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

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
def eye(n):return {(i,i):1 for i in range(n)}
def transpose(a):return {(c,r):v for (r,c),v in a.items()}
def bits(s,n):return [(s>>(n-1-i))&1 for i in range(n)]
def integer(b):
    s=0
    for v in b:s=2*s+v
    return s
def spin_swap(n,i,j):
    out={}
    for column in range(2**n):
        b=bits(column,n);b[i],b[j]=b[j],b[i];out[integer(b),column]=1
    return out
def series_multiply(A,B,order):return [add(*(mm(A[j],B[n-j]) for j in range(n+1))) for n in range(order+1)]
def block_log(n,pairs,sign,order):
    """All chosen spectral differences equal sign*s; derivative is in s."""
    I=eye(2**n);S=[I]+[{} for _ in range(order)]
    for i,j in pairs:
        P=spin_swap(n,i,j);T=add(P,scale(I,-1))
        # Re-derived from eigenvalues r_triplet=1, r_singlet=-(1+x)/(1-x).
        R=[P]+[scale(T,sign**r) for r in range(1,order+1)]
        S=series_multiply(S,R,order)
    X=[mm(transpose(S[0]),s) for s in S];assert X[0]==I
    Y=[I]
    for norder in range(1,order):
        Y.append(scale(add(*(mm(X[j],Y[norder-j]) for j in range(1,norder+1))),-1))
    return [add(*(scale(mm(Y[j],X[r-j+1]),r-j+1) for j in range(r+1))) for r in range(order)]
def encode(a):return [[r,c,v] for (r,c),v in sorted(a.items())]
def direct_transfer(L,order):
    """Binary auxiliary tensor contraction, not permutation-cycle elimination."""
    I=eye(2**(L+1));S=[I]+[{} for _ in range(order)]
    for j in range(1,L+1):
        P=spin_swap(L+1,0,j);T=add(P,scale(I,-1))
        S=series_multiply([P]+[T for _ in range(order)],S,order)
    d=2**L;traced=[]
    for M in S:
        out={}
        for (r,c),v in M.items():
            if r//d==c//d:out[r%d,c%d]=out.get((r%d,c%d),0)+v
        traced.append({p:c for p,c in out.items() if c})
    assert mm(transpose(traced[0]),traced[0])==eye(d)
    X=[mm(transpose(traced[0]),t) for t in traced];Y=[eye(d)]
    for n in range(1,order):Y.append(scale(add(*(mm(X[j],Y[n-j]) for j in range(1,n+1))),-1))
    return {k:scale(add(*(scale(mm(Y[j],X[k-1-j]),k-1-j) for j in range(k-1))),math.factorial(k-2)) for k in range(2,order+2)}
def main():
    # Symmetric/antisymmetric projectors independently give P=Pi_plus-Pi_minus.
    P=spin_swap(2,0,1);I=eye(4)
    rows=lambda a:[[a.get((r,c),0) for c in range(4)] for r in range(4)]
    input_data={'source_id':'S1','locator':'Eq.(3.56), independently read primary rendering PDF p.43',
      'method':'Independent singlet/triplet derivation: R=Pi_triplet-(1+x)/(1-x) Pi_singlet',
      'projector_definitions':'2 Pi_triplet=I+P; 2 Pi_singlet=I-P; spin swap built by binary tensor basis actions',
      'basis':['00','01','10','11'],'spectral_variable':'x=u-v',
      'eigenvalues':{'symmetric':'1','antisymmetric':'-(1+x)/(1-x)'},
      'R_taylor_coefficients':{'0':rows(P),**{str(n):rows(add(P,scale(I,-1))) for n in range(1,4)}},
      'source_product_order':'R1k ... R12 on left; R1k R2k ... R_(k-1)k on right',
      'derivative_map':'D_A=s derivative with x=+s; D_B=s derivative with x=-s; retain ONE overall minus on tilde',
      'index_convention':'Zero-based internal site labels; source labels are index+1',
      'independence':'Same-agent rederivation from primary formula; no reading input A or its generated matrices'}
    (ROOT/'evidence/reproduce-input-b.json').write_text(json.dumps(input_data,indent=2)+'\n')
    output={}
    for k in [2,3,4]:
        order=k-1;factor=math.factorial(k-2)
        left_big=block_log(k,[(0,j) for j in reversed(range(1,k))],1,order)[k-2]
        left_small=block_log(k,[(1,j) for j in reversed(range(2,k))],1,order)[k-2]
        right_big=block_log(k,[(i,k-1) for i in range(k-1)],-1,order)[k-2]
        right_small=block_log(k,[(i,k-2) for i in range(k-2)],-1,order)[k-2]
        left=scale(add(left_big,scale(left_small,-1)),factor)
        right=scale(add(right_big,scale(right_small,-1)),-factor)
        output[str(k)]={'shape':[2**k,2**k],'left_density':encode(left),'right_density':encode(right),
          'left_big_pairs':[[i+1,j+1] for i,j in [(0,j) for j in reversed(range(1,k))]],
          'right_big_pairs':[[i+1,k] for i in range(k-1)],'arithmetic':'exact integer Taylor coefficients; factorial restored'}
        if k==2:expected=add(eye(4),scale(spin_swap(2,0,1),-1))
        elif k==3:
            P12=spin_swap(3,0,1);P23=spin_swap(3,1,2)
            expected=add(mm(P23,P12),scale(mm(P12,P23),-1))
        else:expected=None
        if expected is not None:
            rl=add(left,scale(expected,-1));rr=add(right,scale(expected,-1))
            print(json.dumps({'route':'B','k':k,'left_source_low_order_residual_entries':len(rl),'right_source_low_order_residual_entries':len(rr)}),flush=True)
            assert not rl and not rr
        else:print(json.dumps({'route':'B','k':k,'left_entries':len(left),'right_entries':len(right),'left_minus_right_entries':len(add(left,scale(right,-1)))}),flush=True)
    (ROOT/'evidence/reproduce-block-b.json').write_text(json.dumps(output,indent=2)+'\n')
    transfer_output={}
    for L in [4,5,6]:
        Q=direct_transfer(L,3)
        transfer_output[str(L)]={'method':'Direct binary tensor monodromy and auxiliary partial trace; sparse exact matrices',
            'shape':[2**L,2**L],'series_order':3,'raw_charges':{str(k):encode(q) for k,q in Q.items()}}
        print(json.dumps({'route':'B-direct-transfer','L':L,'charge_nonzero_entries':{str(k):len(q) for k,q in Q.items()},'arithmetic':'exact integers'}),flush=True)
    (ROOT/'evidence/reproduce-transfer-b.json').write_text(json.dumps(transfer_output,indent=2)+'\n')
if __name__=='__main__':main()
