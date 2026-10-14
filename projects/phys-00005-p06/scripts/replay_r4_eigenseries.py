#!/usr/bin/env python3
"""Independent low-eigenvalue continuant series and complete chain replay.

Does not read cached cancellation coefficients or residue output. The certified
decimal parameter center is an input; all series and propagation are recomputed.
"""
import json
import math
from pathlib import Path

import mpmath as mp

N=9

def add(a,b):
    return [(a[k] if k<len(a) else 0)+(b[k] if k<len(b) else 0) for k in range(max(len(a),len(b)))]

def scale(a,s):return [s*x for x in a]

def pmul(a,b,limit=None):
    L=len(a)+len(b)-1 if limit is None else limit
    o=[mp.mpf(0) for _ in range(L)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<L:o[i+j]+=x*y
    return o

def mul(a,b):return pmul(a,b,N+1)

def padded(a):return a+[mp.mpf(0)]*(N+1-len(a))

def evaluate(poly,z):
    out=padded([mp.mpf(0)])
    for cc in reversed(poly):
        out=mul(out,z);out[0]+=cc
    return out

def inv(a):
    out=padded([1/a[0]])
    for n in range(1,N+1):out[n]=-sum(a[k]*out[n-k] for k in range(1,n+1))/a[0]
    return out

def deriv(p):return [k*p[k] for k in range(1,len(p))]

def continuants(edges_squared):
    ps=[[mp.mpf(1)],[mp.mpf(0),mp.mpf(1)]]
    for j2 in edges_squared:
        ps.append(add([mp.mpf(0)]+ps[-1],scale(ps[-2],-j2)))
    return ps

def sine(z,tau):
    w=scale(z,tau);w0=w[0];w[0]=0
    derivs=[mp.sin(w0),mp.cos(w0),-mp.sin(w0),-mp.cos(w0)]
    out=padded([mp.mpf(0)]);power=padded([mp.mpf(1)])
    for n in range(N+1):
        out=add(out,scale(power,derivs[n%4]/math.factorial(n)))
        power=mul(power,w)
    return out

def series(v,c,d):
    u=mp.mpf(1)/2
    a=v*v/(4*c);b=u*u+v*v-c-a
    P=continuants([a,b,c]);M=continuants([b,c])
    p=P[4];q=add([mp.mpf(0)]+p,scale(P[3],-d))
    n0=M[3];n1=add([mp.mpf(0)]+n0,scale(M[2],-d))
    pz=deriv(p);qz=deriv(q)
    X=padded([mp.mpf(0),mp.mpf(1)])
    low=padded([mp.mpf(0)])
    root_checks=[]
    for rho in [-v,-u,u,v]:
        z=padded([rho])
        dp=sum(pz[k]*rho**k for k in range(len(pz)))
        for order in range(1,N+1):
            ff=add(evaluate(p,z),scale(mul(X,evaluate(q,z)),-1))
            z[order]=-ff[order]/dp
        FF=add(evaluate(p,z),scale(mul(X,evaluate(q,z)),-1))
        numerator=add(evaluate(n0,z),scale(mul(X,evaluate(n1,z)),-1))
        denominator=add(evaluate(pz,z),scale(mul(X,evaluate(qz,z)),-1))
        weight=mul(numerator,inv(denominator))
        low=add(low,scale(mul(weight,sine(z,2*mp.pi)),-1))
        root_checks.append(max(abs(zz) for zz in FF))
    return low,root_checks,[a,b,c,d]

def propagation(J,x,dps,direct=True):
    with mp.workdps(dps):
        jj=[+z for z in J];xx=+x;tau=2*mp.pi
        B=mp.matrix(5)
        for k in range(4):B[k,k+1]=B[k+1,k]=jj[k]
        B[4,4]=1/xx
        D,U=mp.eigsy(B)
        terms=[-U[0,k]**2*mp.sin(tau*D[k]) for k in range(5)]
        f=sum(terms);fl=sum(terms[:4]);fh=terms[4]
        if direct:
            T=mp.matrix(10)
            edges=jj+[1/xx]+list(reversed(jj))
            for k,e in enumerate(edges):T[k,k+1]=T[k+1,k]=e
            E,V=mp.eigsy(T)
            aa=sum(V[9,k]*V[0,k]*mp.exp(-1j*tau*E[k]) for k in range(10))
            difference=abs(aa-1j*f)
        else:difference=mp.mpf(0)
        return f,fl,fh,max(abs(e) for e in D),difference

def fmt(x,n=50):return mp.nstr(x,n)

def main():
    mp.mp.dps=100
    cert=json.loads(Path('evidence/research-root-certificate.json').read_text())
    v,c,d=[mp.mpf(s) for s in cert['center_exact_decimal']]
    low,checks,j2=series(v,c,d)
    J=[mp.sqrt(z) for z in j2]
    # The independent output is computed before importing the residue evaluator.
    import certify_r4_root as rc
    residues=[j2[0]*j2[1]*j2[2]*j2[3]*zz for zz in rc.residues(v,c,d)]
    diffs=[abs(low[n]-residues[k]) for k,n in enumerate((1,3,5,7))]
    assert max(diffs)<mp.mpf('1e-80')
    assert max(checks)<mp.mpf('1e-80')
    ref_v=mp.mpf(3)/2
    ref_c,ref_d=mp.findroot(lambda cc,dd:(rc.residues(ref_v,cc,dd)[1],rc.residues(ref_v,cc,dd)[2]),
                         (mp.mpf('.98528'),mp.mpf('.50886')),tol=mp.mpf('1e-90'))
    ref_low,ref_checks,ref_j2=series(ref_v,ref_c,ref_d)
    ref_J=[mp.sqrt(z) for z in ref_j2]
    points=[]
    for k in [25,50,100,200,500,1000]:
        # Strong-bond phase near pi/2, rather than reciprocal-integer x values.
        xx=mp.mpf(4)/(4*k+1)
        f,fl,fh,norm,difference=propagation(J,xx,90)
        f60,_,_,_,_=propagation(J,xx,60,direct=False)
        rf,rfl,rfh,rnorm,rdiff=propagation(ref_J,xx,90)
        err=abs(f-low[1]*xx);rerr=abs(rf-ref_low[1]*xx)
        points.append({'x':fmt(xx),'phase_index_k':k,
            'candidate_abs_error':fmt(err),'candidate_error_div_x8':fmt(err/xx**8),
            'candidate_low_error_div_x9':fmt(abs(fl-low[1]*xx)/xx**9),
            'candidate_high_abs_div_x8':fmt(abs(fh)/xx**8),
            'candidate_success_probability_scalar':fmt(f*f),
            'candidate_norm_H_times_t_scalar':fmt(norm*2*mp.pi),
            'reference_abs_error':fmt(rerr),'reference_error_div_x7':fmt(rerr/xx**7),
            'reference_success_probability_scalar':fmt(rf*rf),
            'reference_norm_H_times_t_scalar':fmt(rnorm*2*mp.pi),
            'candidate_to_reference_error_ratio':fmt(err/rerr),
            'candidate_direct10_sector5_difference':fmt(difference),
            'reference_direct10_sector5_difference':fmt(rdiff),
            'candidate_60_90_digit_difference':fmt(abs(f-f60))})
    out={'method':'Continuant-derived implicit low eigenvalue and endpoint-weight power series, then independent 10x10/5x5 spectral propagation',
         'independence':'Does not use residue jets or their cached coefficients to construct the series; same context and primary defining model. Reads only the certificate parameter center before its calculation. No fresh referee claimed.',
         'order':N,'precision_dps':100,
         'coefficients_n0_through_n9':[fmt(z,80) for z in low],
         'series_equation_residuals':[fmt(z,20) for z in checks],
         'residue_coefficient_differences':[fmt(z,20) for z in diffs],
         'reference':{'scope':'High-precision reconstruction of the fixed-spectrum Table I R4 design; reference root not independently interval-enclosed in this script',
            'v':fmt(ref_v),'c':fmt(ref_c,80),'d':fmt(ref_d,80),'J':[fmt(z,80) for z in ref_J],
            'linear_response':fmt(ref_low[1],80),'septic_coefficient':fmt(ref_low[7],80)},
         'points':points,
         'limitations':'Sample propagation is a precision-stabilized comparison, not the uniform remainder proof. Nominal center has 1e-40 certified parameter uncertainty; formal cancellations hold at the exact enclosed root, not at rounded printed couplings. No total algorithmic speedup follows.'}
    Path('evidence/research-independent-replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'series_residual_max':fmt(max(checks),20),'coefficient_difference_max':fmt(max(diffs),20),
        'linear_response':fmt(low[1],30),'n9':fmt(low[9],30),
        'reference_n7':fmt(ref_low[7],30),
        'points':[{k:z[k] for k in ['x','candidate_error_div_x8','reference_error_div_x7','candidate_to_reference_error_ratio']} for z in points]}))

if __name__=='__main__':main()
