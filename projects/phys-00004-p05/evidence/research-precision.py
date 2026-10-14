"""Independent mpmath spectral/reflection replay from saved binary64 inputs."""
from pathlib import Path
import json
import numpy as np
import mpmath as mp
root=Path(__file__).resolve().parent
scan=json.loads((root/'research-scan.json').read_text())['records']
raw=np.load(root/'research-inputs.npz')
ids=sorted(set([min(range(len(scan)),key=lambda j:scan[j]['gap_out']),
    max(range(len(scan)),key=lambda j:scan[j]['gain']),
    max(range(len(scan)),key=lambda j:scan[j]['noncommutation']),0]))
def run(rho,p,dps):
    mp.mp.dps=dps
    I=mp.eye(2); X=mp.matrix([[0,1],[1,0]]); Y=mp.matrix([[0,-1j],[1j,0]]); Z=mp.matrix([[1,0],[0,-1]])
    ss=[I,X,Y,Z]
    def kron(a,b):return mp.matrix([[a[i//b.rows,j//b.cols]*b[i%b.rows,j%b.cols] for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])
    rho=mp.matrix([[mp.mpc(float(v.real),float(v.imag)) for v in row] for row in rho])
    # The saved float probabilities define an exact nonnegative normalized channel here.
    p=[mp.mpf(float(v)) for v in p]; p=[v/sum(p) for v in p]
    def marginal(r):return mp.matrix([[sum(r[2*i+k,2*j+k] for k in range(2)) for j in range(2)] for i in range(2)])
    def pin(r,ref):
        m=marginal(ref); rv=[mp.re(sum((m*s)[j,j] for j in range(2))) for s in ss[1:]]
        gap=mp.sqrt(sum(v*v for v in rv)); assert gap>0
        N=sum((rv[j]/gap*ss[j+1] for j in range(3)),mp.zeros(2))
        K=kron(N,I); return (r+K*r*K)/2,gap
    def ent(r):
        ev=mp.eighe(r,eigvals_only=True)
        assert min(ev)>-mp.mpf(10)**(-dps+5)
        return -sum(v*mp.log(v,2) for v in ev if v>0)
    def channel(r):return sum((p[j]*kron(ss[j],I)*r*kron(ss[j],I) for j in range(4)),mp.zeros(4))
    tau,gi=pin(rho,rho); out=channel(rho); po,go=pin(out,out); sigma=channel(tau); fixed,_=pin(sigma,out)
    gain=ent(po)-ent(out)-ent(tau)+ent(rho)
    return dict(gain=mp.nstr(gain,dps-10),gap_in=mp.nstr(gi,25),gap_out=mp.nstr(go,25),compatibility_residual=mp.nstr(mp.norm(fixed-sigma),10))
results=[]
for idx in ids:
    low=run(raw['rho'][idx],raw['p'][idx],50); high=run(raw['rho'][idx],raw['p'][idx],80)
    diff=abs(mp.mpf(low['gain'])-mp.mpf(high['gain']))
    assert diff<mp.mpf('1e-35')
    results.append(dict(index=idx,dps50=low,dps80=high,gain_precision_difference=mp.nstr(diff,12),binary64_gain=scan[idx]['gain']))
result=dict(cases=results,limitations='Same proposer, saved binary64 matrices; independently reconstructed channel and reflection pinching with mpmath eigensolver. Precision agreement is not a rigorous enclosure and does not establish the exact theorem. State trace and Hermiticity inherit binary64 input error; no positive-gain witness is claimed.')
(root/'research-precision.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
