"""Independent A: transcribe Bia Eqs.10,15,17 into computational Choi blocks.
No spin-basis coefficients or input B are used. All outputs are project-relative.
"""
from pathlib import Path
import json, time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import expm

OUT=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
W=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
a=np.pi/4

def encode(m):
    return {'real':m.real.tolist(),'imag':m.imag.tolist()}

def choi(theta,lam):
    u=expm(-1j*np.einsum('i,ijk->jk',theta,P))
    j=np.zeros((4,4),complex)
    for b in range(2):
        for c in range(2):
            e=np.zeros((2,2),complex);e[b,c]=1
            channel=(1-lam)*u@e@u.conj().T+lam*np.trace(e)*I/2
            j+=np.kron(e,channel)
    return j

def integrate(nr,nmu,nphi,lam):
    xs,ws=leggauss(nr); rs=(xs+1)*a/2; rw=ws*a/2*3*rs**2/a**3
    mus,mw=leggauss(nmu)
    gam=np.zeros((4,4,4),complex);g2=np.zeros((4,4),complex)
    mass=0
    for r,wr in zip(rs,rw):
        for mu,wm in zip(mus,mw):
            for phi in 2*np.pi*np.arange(nphi)/nphi:
                theta=r*np.array([np.sqrt(1-mu*mu)*np.cos(phi),np.sqrt(1-mu*mu)*np.sin(phi),mu])
                rho=W@choi(theta,lam)@W.conj().T/2
                weight=wr*wm/(2*nphi)
                gam[0]+=weight*rho
                for i in range(3):gam[i+1]+=weight*theta[i]*rho
                g2+=weight*r*r*rho
                mass+=weight
    return gam,g2,mass

def main():
    start=time.monotonic();runs=[]
    for nr,nmu,nphi in [(12,2,4),(24,4,8),(48,6,12)]:
        gam,g2,mass=integrate(nr,nmu,nphi,0)
        runs.append({'nodes':[nr,nmu,nphi],'prior_mass':mass,
                     'Gamma':[encode(m) for m in gam],'Gamma_r2':encode(g2)})
    points=[]
    for lam in [0,.5,1]:
        for theta in [[0,0,0],[.1,-.2,.3],[0,a,0],[a/np.sqrt(3)]*3]:
            j=choi(np.array(theta),lam)
            # Partial trace over Choi output is the input identity.
            pt=np.trace(j.reshape(2,2,2,2),axis1=1,axis2=3)
            points.append({'lambda':lam,'theta':theta,'J':encode(j),'trace':float(np.trace(j).real),
                           'min_eigenvalue':float(np.linalg.eigvalsh(j).min()),
                           'tp_residual':float(np.max(np.abs(pt-I)))})
    record={'representation':'computational output-ancilla 00,01,10,11 after W J Wdag/2',
            'method':'matrix exponential and channel action on each E_ab; full independent r,mu,phi quadrature',
            'source_equations':'10,15-17,3-4,24-26','Pauli':[encode(m) for m in P],'factor_swap_W':encode(W),
            'a':a,'runs':runs,'point_checks':points,'elapsed_seconds':time.monotonic()-start,
            'input_files_read':'none; defining equations transcribed into this script'}
    (OUT/'input-a.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'input':'A','elapsed_seconds':record['elapsed_seconds'],'prior_mass':runs[-1]['prior_mass'],
                      'quadrature_delta':float(np.max(np.abs(gam-np.array([np.array(m['real'])+1j*np.array(m['imag']) for m in runs[-2]['Gamma']]))))}))

if __name__=='__main__':main()
