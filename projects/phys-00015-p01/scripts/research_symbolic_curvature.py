"""Exact symbolic Fourier-block reduction, initially at q=1.
No sign conclusion is hard-coded. t=tan(pi/n), v=tan(pi*k/n).
L=log((1+t)/(1-t)); generic k<n/2 with independent sine/cosine.
"""
import datetime,json,time
from pathlib import Path
import sympy as s

def run():
    start=time.monotonic();t,v,L=s.symbols('t v L',positive=True,real=True)
    I=s.I;z=(1+I*v)/(1-I*v);w=(1+I*t)/(1-I*t);g=(1-t)/(2*t)
    def eig(x):return s.cancel((g+1)*(x-1)+g*(1/x-1))
    lam=eig(w);A=w-1;B=1/w-1
    b=2*t/(1+t*t);lg=-2*t*(1-t)/(1+t*t)
    co=(1-v*v)/(1+v*v);si=2*v/(1+v*v)
    def lambda2(H,P,S):
        ans=g*H*H/2*(A+B)-g*H*(P*A+(P*co+S*si)*B)+(P*P+S*S)*lam
        for sign in [1,-1]:
            zz=z if sign==1 else 1/z
            lm=eig(w*zz);Am=w*zz-1;Bm=1/(w*zz)-1
            hp=H/2;pm=(P+I*sign*S)/2;pp=(P-I*sign*S)/2
            back=g*(Am+Bm*zz)*hp-lm*pm
            ahead=g*(A+B/zz)*hp-lam*pp
            ans+=2*back*ahead/(lam-lm)
        return s.cancel(ans)
    def ys(H,P,S):
        z2=lambda2(H,P,S)
        real=s.cancel((z2+s.conjugate(z2))/2)
        imag=s.cancel((z2-s.conjugate(z2))/(2*I))
        value=g/(g+1)**2*H*H/(2*b)+real/((g+1)*lg*b)+imag*(1/((g+1)*lg*b)-L/b**2)
        return s.factor(s.cancel(value))
    hh=ys(s.Integer(1),s.Integer(0),s.Integer(0));print('hh complete',flush=True)
    pp=ys(s.Integer(0),s.Integer(1),s.Integer(0));print('pp complete',flush=True)
    hc=s.factor(s.cancel((ys(s.Integer(1),s.Integer(1),s.Integer(0))-hh-pp)/2));print('hc complete',flush=True)
    hs=s.factor(s.cancel((ys(s.Integer(1),s.Integer(0),s.Integer(1))-hh-pp)/2));print('hs complete',flush=True)
    det=s.factor(s.cancel(hh*pp-hc*hc-hs*hs));print('det complete',flush=True)
    record={'job_id':'phys-00015-p01-research-a873439075b5','captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'parameters':'t=tan(pi/n),v=tan(pi*k/n),L=log((1+t)/(1-t)); q=1; 1<=k<n/2',
            'hh':str(hh),'pp':str(pp),'hc':str(hc),'hs':str(hs),'det':str(det),
            'elapsed_seconds':time.monotonic()-start,'status':'symbolic_formula_only'}
    Path('evidence/research-symbolic-curvature.json').write_text(json.dumps(record,indent=2)+'\n')
    for key in ['hh','pp','hc','hs','det']:print(key,'=',record[key],flush=True)

if __name__=='__main__':run()
