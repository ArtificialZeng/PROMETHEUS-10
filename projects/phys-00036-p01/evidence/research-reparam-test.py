#!/usr/bin/env python3
"""Exact new stress test, with separate permutation-transfer and binary block routes.
No old artifacts are overwritten. No checkpoint/state input is read.
"""
import datetime, importlib.util, json, math, time
from fractions import Fraction
from itertools import permutations
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
A=module('permutation_transfer','evidence/reproduce-input-a.py')
B=module('binary_blocks','evidence/reproduce-input-b.py')
C=module('checker','evidence/reproduce-compare.py')
def save(name,obj):(ROOT/'evidence'/name).write_text(json.dumps(obj,indent=2)+'\n')
def record(obj):print(json.dumps(obj),flush=True)
def conv(a,b,N):return [sum(a[j]*b[n-j] for j in range(n+1)) for n in range(N+1)]
def scalar_powers(f,N):
    powers=[[1]+[0]*N]
    for j in range(N):powers.append(conv(powers[-1],f,N))
    return powers
def matrix_compose(coeff,f,N):
    powers=scalar_powers(f,N)
    return [B.add(*(B.scale(coeff[j],powers[j][n]) for j in range(N+1))) for n in range(N+1)]
def transfer_chain_rule(L,N):
    # Route A derives undeformed transfer using auxiliary permutation tracing.
    _,X,Q=A.transfer(L,N)
    f=[0,1,1]+[0]*(N-2);powers=scalar_powers(f,N)
    Xf=[A.add(*(A.scale(X[j],powers[j][n]) for j in range(N+1))) for n in range(N+1)]
    I={tuple(range(L)):1};Y=[I]
    for n in range(1,N):Y.append(A.scale(A.add(*(A.mul(Xf[j],Y[n-j]) for j in range(1,n+1))),-1))
    Qf={k:A.scale(A.add(*(A.scale(A.mul(Y[j],Xf[k-1-j]),k-1-j) for j in range(k-1))),math.factorial(k-2)) for k in range(2,N+2)}
    return Q,Qf
def binary_transfer_reparam(L,N):
    # Route B directly composes two-spin projector Taylor series before monodromy.
    I=B.eye(2**(L+1));S=[I]+[{} for _ in range(N)]
    f=[0,1,1]+[0]*(N-2)
    for j in range(1,L+1):
        P=B.spin_swap(L+1,0,j);T=B.add(P,B.scale(I,-1))
        R=matrix_compose([P]+[T for _ in range(N)],f,N)
        S=B.series_multiply(R,S,N)
    d=2**L;tr=[]
    for M in S:
        out={}
        for (r,c),v in M.items():
            if r//d==c//d:out[r%d,c%d]=out.get((r%d,c%d),0)+v
        tr.append({p:v for p,v in out.items() if v})
    X=[B.mm(B.transpose(tr[0]),t) for t in tr];assert X[0]==B.eye(d)
    Y=[B.eye(d)]
    for n in range(1,N):Y.append(B.scale(B.add(*(B.mm(X[j],Y[n-j]) for j in range(1,n+1))),-1))
    return {k:B.scale(B.add(*(B.scale(B.mm(Y[j],X[k-1-j]),k-1-j) for j in range(k-1))),math.factorial(k-2)) for k in range(2,N+2)}
def binary_block(n,pairs,sign,N,f):
    I=B.eye(2**n);S=[I]+[{} for _ in range(N)]
    for i,j in pairs:
        P=B.spin_swap(n,i,j);T=B.add(P,B.scale(I,-1))
        R=matrix_compose([P]+[B.scale(T,sign**r) for r in range(1,N+1)],f,N)
        S=B.series_multiply(S,R,N)
    X=[B.mm(B.transpose(S[0]),s) for s in S];assert X[0]==I
    Y=[I]
    for norder in range(1,N):Y.append(B.scale(B.add(*(B.mm(X[j],Y[norder-j]) for j in range(1,norder+1))),-1))
    return [B.add(*(B.scale(B.mm(Y[j],X[r-j+1]),r-j+1) for j in range(r+1))) for r in range(N)]
def endpoints(k,f):
    N=k-1
    left_big=binary_block(k,[(0,j) for j in reversed(range(1,k))],1,N,f)
    left_small=binary_block(k,[(1,j) for j in reversed(range(2,k))],1,N,f)
    right_big=binary_block(k,[(i,k-1) for i in range(k-1)],-1,N,f)
    right_small=binary_block(k,[(i,k-2) for i in range(k-2)],-1,N,f)
    return {'left':B.scale(B.add(left_big[k-2],B.scale(left_small[k-2],-1)),math.factorial(k-2)),
            'right':B.scale(B.add(right_big[k-2],B.scale(right_small[k-2],-1)),-math.factorial(k-2))}
def cyclic_permutation(L,p):
    ans={};k=len(p)
    for start in range(L):
        sites=[(start+i)%L for i in range(k)];q=list(range(L))
        for i,j in enumerate(p):q[sites[i]]=sites[j]
        q=tuple(q);ans[q]=ans.get(q,0)+1
    return ans
def solve_sparse(rows,n):
    piv={}
    for row,rhs in rows:
        row={i:Fraction(v) for i,v in row.items() if v};rhs=Fraction(rhs)
        while row:
            j=min(row);v=row[j]
            if j in piv:
                old,b=piv[j]
                for t,w in old.items():row[t]=row.get(t,Fraction(0))-v*w
                row={t:w for t,w in row.items() if w};rhs-=v*b
            else:
                piv[j]=({t:w/v for t,w in row.items()},rhs/v);break
        if not row and rhs:raise ValueError('inconsistent exact locality equation')
    x={}
    for j in sorted(piv,reverse=True):
        row,rhs=piv[j];x[j]=rhs-sum(v*x.get(t,0) for t,v in row.items() if t!=j)
    return x,{'rank':len(piv),'unknowns':n,'free_variables_set_zero':n-len(piv)}
def density_from_transfer(Q,k,L):
    # Independent local representative solved in the full S_k algebra, not from endpoints.
    basis=list(permutations(range(k)));rows={}
    for j,p in enumerate(basis):
        for globalp,v in cyclic_permutation(L,p).items():rows.setdefault(globalp,{})[j]=v
    equations=[(rows.get(p,{}),Q.get(p,0)) for p in sorted(set(rows)|set(Q))]
    x,info=solve_sparse(equations,len(basis));q={basis[j]:v for j,v in x.items() if v}
    residual=A.add(A.add(*(A.scale(cyclic_permutation(L,p),v) for p,v in q.items())),A.scale(Q,-1));assert not residual
    info.update({'derivation':'Exact locality inversion of route-A Q5 at L=6 in formal S5/S6 permutation algebra; no block endpoint used',
        'all_global_permutations_checked':len(equations),'residual_terms':len(residual),
        'coefficients':[{'permutation':[i+1 for i in p],'coefficient':str(v)} for p,v in sorted(q.items())]})
    return B.add(*(B.scale(C.perm_matrix(p),v) for p,v in q.items())),info
def pad(M,j,k):
    out={}
    for (r,c),v in M.items():
        for rest in range(2**(k-j)):out[r*2**(k-j)+rest,c*2**(k-j)+rest]=v
    return out
def main():
    start=time.monotonic();data={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'input':'R_f(u,v)=(P-(f(u)-f(v))I)/(1-f(u)+f(v)), f(u)=u+u^2',
        'scope':'Exact finite k=4,5 stress test, not a resolution or novelty assertion',
        'arithmetic':'Python integers and fractions.Fraction; no numeric tolerance',
        'transfer_checks':[],'local_gradient_checks':[]}
    qa={};qfa={}
    for L in [4,5,6]:
        N=3 if L==4 else 4
        Q,Qf=transfer_chain_rule(L,N);qa[L]=Q;qfa[L]=Qf
        QB=binary_transfer_reparam(L,N)
        for k in range(2,N+2):
            AM=B.add(*(B.scale(C.perm_matrix(p),v) for p,v in Qf[k].items()))
            res=B.add(AM,B.scale(QB[k],-1));assert not res
            mix={2:{2:1},3:{3:1,2:2},4:{4:1,3:6},5:{5:1,4:12,3:12}}[k]
            mixres=A.add(Qf[k],A.scale(A.add(*(A.scale(Q[j],c) for j,c in mix.items())),-1));assert not mixres
            row={'L':L,'k':k,'full_matrix_entries_checked':2**(2*L),'independent_transfer_residual_entries':len(res),
                'chain_rule_mixing':mix,'mixing_residual_permutation_terms':len(mixres)}
            data['transfer_checks'].append(row);record(row)
    q5,q5info=density_from_transfer(qa[6][5],5,6);data['q5_derivation']=q5info
    # Independently transcribed published XXX q2/q3/q4, with normalization already reproduced.
    q2=B.add(B.eye(4),B.scale(B.spin_swap(2,0,1),-1))
    q3=B.add(C.local_symbol(3,[3,1,2]),B.scale(C.local_symbol(3,[2,3,1]),-1))
    terms=[(-1,[1]),(2,[2,1]),(-1,[3,2,1]),(1,[2,3,4,1]),(-1,[2,4,1,3]),(-1,[3,1,4,2]),(1,[4,1,2,3])]
    q4=B.scale(B.add(*(B.scale(C.local_symbol(4,p),c) for c,p in terms)),-2)
    densities={2:q2,3:q3,4:q4,5:q5}
    for k in [4,5]:
        f=[0,1,1]+[0]*(k-3);plain=[0,1]+[0]*(k-2)
        mix={4:{4:1,3:6},5:{5:1,4:12,3:12}}[k]
        qf=B.add(*(B.scale(pad(densities[j],j,k),c) for j,c in mix.items()))
        for model,fcoeff,expected in [('XXX',plain,densities[k]),('nonlinear_reparam',f,qf)]:
            E=endpoints(k,fcoeff)
            for side,M in E.items():
                D=B.add(M,B.scale(expected,-1));m,info=C.solve_gradient(D,k)
                row={'model':model,'k':k,'side':side,'difference_entries':len(D),**info,
                    'equation':'endpoint_density - independently derived q = I tensor m - m tensor I'}
                if m is not None:row['witness_sparse_entries']=C.encode(m)
                data['local_gradient_checks'].append(row);record({j:v for j,v in row.items() if j!='witness_sparse_entries'})
                assert m is not None and not info['residual_nonzero_entries']
                for L in [k,6]:
                    residual=B.add(C.cyclic_sum(M,k,L),B.scale(B.add(*(B.scale(C.perm_matrix(p),v) for p,v in (qa if model=='XXX' else qfa)[L][k].items())),-1))
                    assert not residual
                    record({'model':model,'k':k,'side':side,'L':L,'endpoint_sum_minus_transfer_residual_entries':len(residual)})
        save('research-reparam-comparison.json',data)
    data['elapsed_seconds']=time.monotonic()-start
    data['limitations']='Known-input stress test only. Local q5 obtained from one formal periodic transfer and checked against exact endpoints and L=5,6, not a universal general-R/all-k proof. Same-agent route independence is weaker than a fresh referee.'
    save('research-reparam-comparison.json',data);record({'completed':True,'elapsed_seconds':data['elapsed_seconds']})
if __name__=='__main__':main()
