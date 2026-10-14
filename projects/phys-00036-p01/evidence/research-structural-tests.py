#!/usr/bin/env python3
"""Adversarial exact tests of the candidate's transfer and product lemmas.
Generic inputs test algebraic lemmas only, not an admissible physical counterexample.
The gauge input is an admissible non-difference XXX Yang--Baxter input.
"""
import datetime, importlib.util, json, math, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def loadmodule(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
A=loadmodule('transfer_A','evidence/reproduce-input-a.py')
B=loadmodule('binary_B','evidence/reproduce-input-b.py')
K=loadmodule('checker_K','evidence/reproduce-compare.py')
def emit(x):print(json.dumps(x),flush=True)
def save(x):(ROOT/'evidence/research-structural-comparison.json').write_text(json.dumps(x,indent=2)+'\n')
def lift(M,n,i,j):
    out={};bycol={}
    for (r,c),v in M.items():bycol.setdefault(c,[]).append((r,v))
    for c in range(2**n):
        b=B.bits(c,n);small=2*b[i]+b[j]
        for r,v in bycol.get(small,[]):
            dst=b.copy();dst[i]=r//2;dst[j]=r%2
            out[B.integer(dst),c]=v
    return out
def coeffs(M,N):return [M[r] if r<len(M) else {} for r in range(N+1)]
def sminv(X,N):
    assert X[0]==B.eye(max(r for r,c in X[0])+1)
    Y=[X[0]]
    for n in range(1,N+1):Y.append(B.scale(B.add(*(B.mm(Y[n-j],X[j]) for j in range(1,n+1))),-1))
    return Y
def forms(X,N):
    Y=sminv(X,N);D=[B.scale(X[n+1],n+1) for n in range(N)]+[{}]
    return B.series_multiply(Y,D,N)[:N],B.series_multiply(D,Y,N)[:N]
def circuit(Cseries,n,edges,N):
    S=[B.eye(2**n)]+[{} for _ in range(N)]
    for i,j in edges:
        R=[lift(M,n,i,j) for M in coeffs(Cseries,N)]
        S=B.series_multiply(R,S,N)
    return S
def transfer(Cseries,L,N,active=None,weights=None):
    if active is None:active=set(range(L))
    if weights is None:weights=[1]*L
    S=[B.eye(2**(L+1))]+[{} for _ in range(N)]
    P=B.spin_swap(2,0,1);Rtwo=[B.mm(P,M) for M in coeffs(Cseries,N)]
    for j in range(L):
        R=[B.scale(lift(M,L+1,0,j+1),weights[j]**r) if (j in active or r==0) else {} for r,M in enumerate(Rtwo)]
        S=B.series_multiply(R,S,N)
    d=2**L;tr=[]
    for M in S:
        T={}
        for (r,c),v in M.items():
            if r//d==c//d:T[r%d,c%d]=T.get((r%d,c%d),0)+v
        tr.append({p:v for p,v in T.items() if v})
    U=tr[0];assert B.mm(B.transpose(U),U)==B.eye(d)
    return [B.mm(B.transpose(U),T) for T in tr]
def starforms(Cseries,n,N):
    Cs=coeffs(Cseries,N);Di=sminv(Cs,N);I=B.eye(2**n)
    left=[I]+[{} for _ in range(N)];right=[I]+[{} for _ in range(N)]
    for j in reversed(range(1,n)):
        P=B.spin_swap(n,0,j);R=[B.mm(P,lift(M,n,0,j)) for M in Cs]
        left=B.series_multiply(left,R,N)
    for i in range(n-1):
        P=B.spin_swap(n,i,n-1);R=[B.mm(P,lift(M,n,i,n-1)) for M in Di]
        right=B.series_multiply(right,R,N)
    XL=[B.mm(B.transpose(left[0]),M) for M in left]
    XR=[B.mm(B.transpose(right[0]),M) for M in right]
    FL,_=forms(XL,N);FR,_=forms(XR,N)
    return XL,XR,FL,[B.scale(M,-1) for M in FR]
def endpoints(Cseries,k):
    N=k-1
    G=circuit(Cseries,k,[(i,i+1) for i in range(k-1)],N)
    GSright=circuit(Cseries,k,[(i,i+1) for i in range(1,k-1)],N)
    GSleft=circuit(Cseries,k,[(i,i+1) for i in range(k-2)],N)
    F,Bf=forms(G,N);FS,_=forms(GSright,N);_,BS=forms(GSleft,N)
    return {'left':B.scale(B.add(F[k-2],B.scale(FS[k-2],-1)),math.factorial(k-2)),
            'right':B.scale(B.add(Bf[k-2],B.scale(BS[k-2],-1)),math.factorial(k-2))}
def main():
    start=time.monotonic();out={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'arithmetic':'exact integer complete matrices; rational exact gradient solves',
        'generic_domain':'C=I+uH+u^2K, arbitrary nonsymmetric two-site matrices. No YB, Hermiticity, or physical admissibility is asserted; these attack proof lemmas only.',
        'unfolding_checks':[],'star_checks':[],'generic_endpoint_checks':[],'gauge_checks':[]}
    H={(r,c):(3*r+2*c+1)%5-2 for r in range(4) for c in range(4)}
    J={(r,c):(r*r+3*c+2)%7-3 for r in range(4) for c in range(4)}
    H={p:v for p,v in H.items() if v};J={p:v for p,v in J.items() if v}
    generic=[B.eye(4),H,J]
    out['generic_coefficients']={'H':B.encode(H),'K':B.encode(J),'H_K_commutator_nonzero_entries':len(B.add(B.mm(H,J),B.scale(B.mm(J,H),-1)))}
    for L in [3,4]:
        N=2*(L-1);weights=[2,3,5,7][:L]
        for mask in range((1<<L)-1):
            active={j for j in range(L) if mask>>j&1};cut=next(j for j in range(L) if j not in active)
            X=transfer(generic,L,N,active,weights)
            G=[B.eye(2**L)]+[{} for _ in range(N)]
            for step in range(1,L):
                j=(cut+step)%L
                if j not in active:continue
                Cj=[B.scale(lift(M,L,(j-1)%L,j),weights[j]**r) for r,M in enumerate(coeffs(generic,N))]
                G=B.series_multiply(Cj,G,N)
            residual=sum(len(B.add(x,B.scale(g,-1))) for x,g in zip(X,G));assert not residual
            row={'L':L,'active_sites_zero_based':sorted(active),'cut':cut,'weights':weights,
                'all_exact_polynomial_degrees_checked':N,'residual_entries_all_degrees':residual}
            out['unfolding_checks'].append(row)
        emit({'test':'generic_exact_unfolding','L':L,'proper_subsets_checked':(1<<L)-1,'degree_bound':N,'all_residuals':0})
    for n in [3,4,5]:
        N=4;XL,XR,FL,BR=starforms(generic,n,N)
        G=circuit(generic,n,[(i,i+1) for i in range(n-1)],N);Gi=sminv(G,N);FG,BG=forms(G,N)
        errors=[sum(len(B.add(x,B.scale(y,-1))) for x,y in zip(P,Q)) for P,Q in [(XL,G),(XR,Gi),(FL,FG),(BR,BG)]]
        assert not any(errors)
        row={'n':n,'series_degree':N,'left_normalized_star_minus_G':errors[0],'right_normalized_star_minus_G_inverse':errors[1],
            'left_form_residual':errors[2],'right_minus_form_residual':errors[3]}
        out['star_checks'].append(row);emit(row)
    for L in [5,6]:
        N=4;X=transfer(generic,L,N);F,BR=forms(X,N)
        for k in [2,3,4,5]:
            E=endpoints(generic,k)
            qL=B.scale(F[k-2],math.factorial(k-2));qR=B.scale(BR[k-2],math.factorial(k-2))
            errors={side:len(B.add(K.cyclic_sum(E[side],k,L),B.scale(qL if side=='left' else qR,-1))) for side in E}
            assert not any(errors.values())
            row={'L':L,'k':k,'left_endpoint_minus_left_transfer_entries':errors['left'],
                'right_endpoint_minus_right_transfer_entries':errors['right'],
                'left_minus_right_transfer_entries':len(B.add(qL,B.scale(qR,-1))),
                'last_quantity_is_a_control':'Generic input need not have commuting transfers; a nonzero value is not a conjecture counterexample'}
            out['generic_endpoint_checks'].append(row);emit(row)
    # Legal non-difference gauge. G(u)=I+uN, N^2=0; G(0)=I.
    P=B.spin_swap(2,0,1);T=B.add(P,B.scale(B.eye(4),-1));Ng={(0,2):1,(1,3):1}
    gaugeR=[]
    for r in range(6):
        rr=P if r==0 else T;rm=P if r==1 else T if r>=2 else {};rmm=P if r==2 else T if r>=3 else {}
        gaugeR.append(B.add(rr,B.mm(Ng,rm),B.scale(B.mm(rm,Ng),-1),B.scale(B.mm(B.mm(Ng,rmm),Ng),-1)))
    gaugeC=[B.mm(P,R) for R in gaugeR];plainC=[B.eye(4)]+[B.mm(P,T) for _ in range(5)]
    out['gauge_definition']='R_g(u,v)=(G(u) tensor G(v)) R_XXX(u-v) (G(u)^(-1) tensor G(v)^(-1)), G(u)=I+uN, N=[[0,1],[0,0]], N^2=0'
    out['gauge_admissibility']='YB is global three-leg conjugation; regularity uses equal G on both legs commuting with P; braiding normalization is conjugation of the parent identity. All matrices are analytic and invertible as formal series. Physical t_g(u)=t_XXX(u) because physical G(0)=I and auxiliary factors telescope under trace.'
    for L in [6,7]:
        N=5;Xg=transfer(gaugeC,L,N);Fg,_=forms(Xg,N)
        _,_,QA=A.transfer(L,N)
        for k in [4,5,6]:
            target=B.add(*(B.scale(K.perm_matrix(p),v) for p,v in QA[k].items()))
            qg=B.scale(Fg[k-2],math.factorial(k-2));transfer_error=len(B.add(qg,B.scale(target,-1)));assert not transfer_error
            E=endpoints(gaugeC,k);E0=endpoints(plainC,k)
            for side in E:
                glob=len(B.add(K.cyclic_sum(E[side],k,L),B.scale(target,-1)));assert not glob
                D=B.add(E[side],B.scale(E0['left'],-1));m,info=K.solve_gradient(D,k)
                assert m is not None and info['residual_nonzero_entries']==0
                row={'input':'legal_nondifference_gauge_XXX','L':L,'k':k,'side':side,
                    'gauge_transfer_minus_independent_XXX_transfer_entries':transfer_error,
                    'endpoint_sum_minus_independent_transfer_entries':glob,
                    'local_gradient':info,'witness_sparse_entries':K.encode(m)}
                out['gauge_checks'].append(row);emit({j:v for j,v in row.items() if j!='witness_sparse_entries'})
            save(out)
    out['elapsed_seconds']=time.monotonic()-start
    out['limits']='Finite exact adversarial checks, not all-R/all-k certification. The stable structural proof supplies the universal argument. Same-agent checking is not fresh referee acceptance.'
    save(out);emit({'completed':True,'elapsed_seconds':out['elapsed_seconds']})
if __name__=='__main__':main()
