"""Independent referee implementation. No project discovery modules are imported.

Run with the existing scientific Python; all outputs stay in audit/.
The input NPZ, when used, is an exact dyadic proof witness, never a cached answer.
"""
from pathlib import Path
from fractions import Fraction
import json, hashlib, time, sys, math
import numpy as np
from flint import arb, acb, acb_mat, fmpz, ctx

JOB = 'PHY-14-referee-5a932658dcd5'
ctx.prec = 224
OUT = Path('audit')

def save(name, obj):
    obj = {'job_id': JOB, 'precision_bits': ctx.prec, **obj}
    (OUT/name).write_text(json.dumps(obj, indent=2)+'\n')
    print(json.dumps(obj, indent=2), flush=True)

def ar(x):
    if isinstance(x, float):
        n,d=x.as_integer_ratio(); return arb(n)/d
    return arb(x)

def az(x):
    return acb(ar(float(x.real)), ar(float(x.imag)))

def source():
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    Z=np.diag([1,-1]).astype(complex)
    def kron(xs):
        v=np.array([[1]],complex)
        for x in xs:v=np.kron(v,x)
        return v
    cases=[]
    for L in [2,4,6]:
        N=2**L
        single={k:[kron([M if j==s else I for j in range(L)]) for s in range(L)]
                for k,M in [('X',X),('Y',Y),('Z',Z)]}
        ferm=[]
        for j in range(L):
            c=np.zeros((N,N),complex); mask=1<<(L-1-j)
            for n in range(N):
                if n&mask:
                    c[n^mask,n]=(-1)**((n>>(L-j)).bit_count())
            ferm.append(c)
        aa=[];bb=[]
        for j in range(L):
            prefix=kron([Y if k<j else I for k in range(L)])
            alpha=prefix@single['X'][j];beta=-prefix@single['Z'][j]
            aa.append(alpha if j%2==0 else beta)
            bb.append(beta if j%2==0 else alpha)
        for Delta,mu in [(Fraction(1),Fraction(0)),(Fraction(7,6),Fraction(0)),(Fraction(7,6),Fraction(2,7))]:
            HF=np.zeros((N,N),complex);HS=HF.copy();scale=2100
            for j in range(L-1):
                m=Fraction(6 if j%2==0 else 4,5)
                c,d=ferm[j],ferm[j+1]
                HF-=int(scale*m)*(c.conj().T@d+d.conj().T@c)
                HF-=int(scale*m*Delta)*(c.conj().T@d.conj().T+d@c)
                density=(2*c.conj().T@c-np.eye(N))@(2*d.conj().T@d-np.eye(N))
                HF+=int(scale*m/5)*(1-1j)*density
                HS-=int(scale*m*(1+Delta)/2)*(single['X'][j]@single['X'][j+1])
                HS-=int(scale*m*(1-Delta)/2)*(single['Y'][j]@single['Y'][j+1])
                HS+=int(scale*m/5)*(1-1j)*(single['Z'][j]@single['Z'][j+1])
            for j,c in enumerate(ferm):
                HF-=int(scale*mu/2)*(2*c.conj().T@c-np.eye(N))
                HS+=int(scale*mu/2)*single['Z'][j]
            assert np.array_equal(HF,HS)
            if Delta==1 and mu==0:
                HC=np.zeros((N,N),complex);VC=HC.copy();VS=HC.copy()
                for j in range(L-1):
                    m=Fraction(6 if j%2==0 else 4,5)
                    wa=(1-1j)/5 if j%2==0 else 1
                    wb=1 if j%2==0 else (1-1j)/5
                    # Integer-scaled coefficients, so every matrix operation is exact.
                    ca=complex(round((scale*float(m)*wa).real),round((scale*float(m)*wa).imag))
                    cb=complex(round((scale*float(m)*wb).real),round((scale*float(m)*wb).imag))
                    HC+=1j*ca*(aa[j]@aa[j+1])+1j*cb*(bb[j]@bb[j+1])
                    Vquad=bb[j]@bb[j+1] if j%2==0 else aa[j]@aa[j+1]
                    VC+=int(scale*m/2)*(1j*Vquad-aa[j]@aa[j+1]@bb[j]@bb[j+1])
                    VS+=int(scale*m/2)*(-single['X'][j]@single['X'][j+1]+single['Y'][j]@single['Y'][j+1])
                assert np.array_equal(HC,HF)
                assert np.array_equal(VC,VS)
                parity=kron([Z]*L)
                assert all(np.array_equal(parity@a,-a@parity) for a in aa)
                assert all(np.array_equal(parity@b,b@parity) for b in bb)
            cases.append({'L':L,'Delta':str(Delta),'mu':str(mu),'fermion_vs_spin_gaussian_integer_equality':True})
    import sympy as sp
    p,h,z,r,w=sp.symbols('p h z r w', nonzero=True)
    sn=(r-1/r)/(2*sp.I);sm=(r/z-z/r)/(2*sp.I);sp1=(r*z-1/(r*z))/(2*sp.I)
    lu=-2*sp.I*(p*sn-h*sm)/w
    lun=-2*sp.I*(p*sp1-h*sn)/w
    rec1=sp.factor(-2*sp.I*p*sn+2*sp.I*h*sm-w*lu)
    rec2=sp.factor((2*sp.I*p*lu-2*sp.I*h*lun-w*sn)*w)
    rec2=sp.expand(sp.factor(rec2.subs(w*w,4*(p*p+h*h-p*h*(z+1/z)))))
    assert rec1==0 and rec2==0
    baseline=[]
    for eta in [Fraction(0),Fraction(1,5)]:
        a=1+eta;b=1-eta
        for sector,critical in [('A',b/a),('B',a/b)]:
            for sign in [-1,1]:
                U=sign*critical;pp,hh=(U*a,b) if sector=='A' else (a,U*b)
                squared=4*(pp*pp+hh*hh-2*pp*hh*sign)
                assert squared==0
                baseline.append({'eta':str(eta),'sector':sector,'U_over_t':str(U),'cos_q':sign,'frequency_squared_exact':str(squared)})
    save('referee-source.json',{'cases':cases,'quadratic_and_quartic_clifford_source_exact':True,
        'physical_parity_exact':True,'left_scattering_all_n_symbolic_residuals':[str(rec1),str(rec2)],
        'published_Eq5_Hermitian_gap_baseline':baseline,
        'representation':'Independent occupation-bit matrices versus tensor Pauli and Clifford matrices; all scaled entries are exact Gaussian integers below 2^53.'})

def root_data():
    g=acb(arb(1)/5,-arb(1)/5);a=arb(6)/5;b=arb(4)/5
    pa,ha=g*a,acb(b);pb,hb=acb(a),g*b
    xc=arb('0.914005998943111754560338502271033241599810017455941304810241')
    yc=arb('-0.769581730425783703625420540788997375179263443033756807855182')
    rad=arb('1e-20')
    def om(p,h,x):return 2*(p*p+h*h+2*p*h*x).sqrt()
    def freq(x,y):
        return om(pa,ha,-arb(99)/100)+om(pa,ha,-arb(95)/100)+om(pa,ha,x)-om(pb,hb,y-arb(1)/100)-om(pb,hb,y+arb(1)/100)
    def jac(x,y):
        dx=4*pa*ha/om(pa,ha,x)
        dy=-4*pb*hb*(1/om(pb,hb,y-arb(1)/100)+1/om(pb,hb,y+arb(1)/100))
        return [[dx.real,dy.real],[dx.imag,dy.imag]]
    Jc=jac(xc,yc)
    C=np.linalg.inv(np.array([[float(v.mid()) for v in row] for row in Jc]))
    C=[[ar(float(v)) for v in row] for row in C]
    xb=xc+arb(0,rad);yb=yc+arb(0,rad)
    for pp,hh,xx in [(pa,ha,-arb(99)/100),(pa,ha,-arb(95)/100),(pa,ha,xb),(pb,hb,yb-arb(1)/100),(pb,hb,yb+arb(1)/100)]:
        assert xx>-1 and xx<1 and (pp*pp+hh*hh+2*pp*hh*xx).real>0
    J=jac(xb,yb);fc=freq(xc,yc)
    eta=max(abs(C[i][0]*fc.real+C[i][1]*fc.imag).upper() for i in range(2))
    q=max(sum(abs(arb(int(i==j))-sum(C[i][k]*J[k][j] for k in range(2))).upper() for j in range(2)) for i in range(2))
    assert eta<arb('1e-50') and q<arb('1e-12') and eta+q*rad<rad
    assert abs(C[0][0]*C[1][1]-C[0][1]*C[1][0]).lower()>0
    return pa,ha,pb,hb,xb,yb,om,{'center_displacement_upper':str(eta),'contraction_infinity_norm_upper':str(q),'radius':'1e-20','frequency_box':str(freq(xb,yb)),'preconditioner':[[str(v) for v in row] for row in C]}

def constants():
    pa,ha,pb,hb,xb,yb,om,root=root_data()
    alpha=arb(1)/1000;rho=pa/ha;c=(1-rho*rho).sqrt();r=abs(rho)**2
    # Analytic extrema: Re omega strictly increases with x because arg(ph)=-pi/4
    # and arg(sqrt(G)) lies in (-pi/4,pi/4). Endpoint frequencies are exact.
    amin=arb(28)/25;amax=arb(52)/25;bmin=arb(52)/25;bmax=arb(68)/25
    ga=arb(328)/625/arb(2).sqrt()  # minimum |G_A|=(.64-.1152)/sqrt(2)
    gb=arb(692)/625              # minimum |G_B| at x=-1
    ja=(abs(pa)+abs(ha))**2/ga;jb=(abs(pb)+abs(hb))**2/gb
    qnorm=abs(c)**2/(1-r)
    gap=amin-(bmax-bmin)
    assert gap<2*bmin-amax and gap<8-2*bmax
    M=(qnorm+ja)*jb**2/gap
    def nq(s):return (abs(c)**2/(1-r*(2*s).exp())).sqrt()
    def dq(s):return (abs(c)**2*(1/(1-r*(2*s).exp())-2/(1-r*s.exp())+1/(1-r))).sqrt()
    shift=2*(abs(ha)+2*abs(hb))*(alpha.exp()-1)
    pdiff=dq(alpha)*nq(-alpha)+nq(arb(0))*dq(-alpha)
    E=shift+8*pdiff
    assert M*E<1
    Mw=M/(1-M*E)
    ma=2*(abs(pa)+abs(ha))/amin;mb=2*(abs(pb)+abs(hb))/bmin
    assert ma>1 and mb>1
    dual=(4*arb(6)/5*6*ma**3*2*mb**2)*2/(1-(-2*alpha).exp())**arb('1.5')
    mult=Mw*dual
    ceiling=math.ceil(float(mult.upper()))+1
    assert arb(ceiling)>mult.upper()
    obj={'root':root,'exact_Re_bands':[['28/25','52/25'],['52/25','68/25']],
         'min_abs_G_A':str(ga),'min_abs_G_B':str(gb),'cubic_separation':'12/25',
         'unweighted_inverse':str(M),'weighted_perturbation':str(E),'neumann_product':str(M*E),
         'weighted_inverse':str(Mw),'functional_dual':str(dual),'residual_multiplier':str(mult),
         'integer_multiplier_upper':ceiling,'analytic_extrema':True}
    return ceiling,obj

def matrices(L):
    # A has L-1 coordinates; its missing terminal coordinate is only a finite solver choice.
    # Every physical boundary crossing is restored by the independent certificate.
    g=(1-1j)/5;a=1.2;b=.8
    def K(n,wa,wb):
        w=np.array([wa if j%2==0 else wb for j in range(n-1)],complex)
        return np.diag(2j*w,1)+np.diag(-2j*w,-1)
    return K(L-1,g*a,b),K(L,a,g*b)

def forcing(L,q):
    f=np.zeros((L-1,L,L),complex)
    for j in range(L-2):
        m=1.2 if j%2==0 else .8
        f[j,j,j+1]+=m*q[j+1];f[j+1,j,j+1]-=m*q[j]
    return f-f.swapaxes(1,2)

def solve(L):
    from scipy.sparse.linalg import LinearOperator,gmres
    KA,KB=matrices(L);rho=.3-.3j
    q=np.zeros(L-1,complex);q[::2]=rho**np.arange(L//2);q/=np.sqrt(q@q)
    f=forcing(L,q);shape=f.shape
    def apply(v,dtype=np.complex128):
        X=v.reshape(shape).astype(dtype,copy=False)
        A=KA.astype(dtype);B=KB.astype(dtype);qq=q.astype(dtype)
        # Explicit nearest-neighbour shifts avoid importing a tensor eigensystem.
        Y=np.zeros_like(X)
        Y[:-1]+=np.diag(A,1)[:,None,None]*X[1:]
        Y[1:]+=np.diag(A,-1)[:,None,None]*X[:-1]
        Y[:,:-1]+=np.diag(B,1)[None,:,None]*X[:,1:]
        Y[:,1:]+=np.diag(B,-1)[None,:,None]*X[:,:-1]
        Y[:,:,:-1]+=np.diag(B,1)[None,None,:]*X[:,:,1:]
        Y[:,:,1:]+=np.diag(B,-1)[None,None,:]*X[:,:,:-1]
        Y+=8*qq[:,None,None]*np.einsum('a,abc->bc',qq,X)[None,:,:]
        return Y.ravel()
    op=LinearOperator((f.size,f.size),matvec=apply,dtype=complex)
    start=time.monotonic();counts=[0]
    def cb(_):counts[0]+=1
    x,info=gmres(op,f.ravel(),rtol=1e-12,atol=0,restart=160,maxiter=15,callback=cb,callback_type='pr_norm')
    print('initial GMRES',L,info,counts[0],float(np.linalg.norm(apply(x)-f.ravel())),flush=True)
    assert info==0,info
    for _ in range(2):
        res=f.astype(np.clongdouble).ravel()-apply(x,np.clongdouble)
        dx,info=gmres(op,np.asarray(res,dtype=complex),rtol=1e-7,atol=1e-28,restart=160,maxiter=10)
        assert info==0,info
        x=np.asarray(x.astype(np.clongdouble)+dx.astype(np.clongdouble),dtype=complex)
    X=x.reshape(shape);X=(X-X.swapaxes(1,2))/2
    path=OUT/f'referee-Q1-L{L}.npz';np.savez_compressed(path,Q1_cubic=X)
    save(f'referee-solve-L{L}.json',{'L':L,'method':'Independent nearest-neighbour GMRES plus long-double residual correction; no saved discovery vector supplied to solver.',
         'iterations':counts[0],'seconds':time.monotonic()-start,'finite_solver_residual':float(np.linalg.norm(apply(X.ravel())-f.ravel())/np.sqrt(2)),
         'witness':str(path),'witness_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})

def residual_certificate(X):
    """Exact Gaussian integer quadratic action, then Arb source and normalization.

    A common power-of-two denominator is inferred from the actual finite floats.
    This uses neither numerical eigenvalues nor residuals from the submitted logs.
    """
    L=X.shape[1];N=L//2;alpha=arb(1)/1000
    vals=np.concatenate((np.abs(X.real).ravel(),np.abs(X.imag).ravel()))
    nz=vals[vals!=0];D=max(0,53-int(np.frexp(nz)[1].min()));del vals,nz
    shape=(L,L+1,L+1)
    R=np.zeros(shape,dtype=object);I=np.zeros(shape,dtype=object)
    def integer(v):
        n,d=float(v).as_integer_ratio();return n<<(D-(d.bit_length()-1))
    R[:L-1,:L,:L]=np.fromiter((integer(v) for v in X.real.ravel()),dtype=object,count=X.size).reshape(X.shape)
    I[:L-1,:L,:L]=np.fromiter((integer(v) for v in X.imag.ravel()),dtype=object,count=X.size).reshape(X.shape)
    YR=np.zeros(shape,dtype=object);YI=np.zeros(shape,dtype=object)
    for axis,n in enumerate(shape):
        for j in range(n-1):
            if axis==0:wr,wi=(6,-6) if j%2==0 else (20,0)
            else:wr,wi=(30,0) if j%2==0 else (4,-4)
            kr,ki=-2*wi,2*wr
            left=[slice(None)]*3;right=left.copy();left[axis]=j;right[axis]=j+1
            left=tuple(left);right=tuple(right)
            YR[left]+=kr*R[right]-ki*I[right];YI[left]+=ki*R[right]+kr*I[right]
            YR[right]-=kr*R[left]-ki*I[left];YI[right]-=ki*R[left]+kr*I[left]
    del R,I
    denom=arb(25)*arb(2)**D
    g=acb(arb(1)/5,-arb(1)/5);rho=g*arb(3)/2;C=(1-rho*rho).sqrt()
    q=[C*rho**n for n in range(N)]
    src={}
    for j in range(L-1):
        m=arb(6 if j%2==0 else 4)/5
        if j%2==0:src[(j+1,j,j+1)]=m*q[j//2]
        else:src[(j,j,j+1)]=-m*q[(j+1)//2]
    accum=0
    for a in range(L):
        for b in range(L+1):
            for c in range(b+1,L+1):
                accum+=YR[a,b,c]**2+YI[a,b,c]**2
    # Remove the purely rational contribution at the sparse source positions.
    for idx in src:accum-=YR[idx]**2+YI[idx]**2
    norm2=arb(fmpz(accum))/(denom*denom)
    for idx,s in src.items():
        z=acb(arb(fmpz(YR[idx]))/denom,arb(fmpz(YI[idx]))/denom)+s
        norm2+=z.real*z.real+z.imag*z.imag
    physical=norm2.sqrt();del YR,YI
    znorm2=arb(0)
    for b in range(L):
        for c in range(b+1,L):
            z=sum((q[n]*az(X[2*n,b,c]) for n in range(N)),acb(0))
            znorm2+=z.real*z.real+z.imag*z.imag
    znorm=znorm2.sqrt()
    weighted_finite=(3*alpha*(N+1)).exp()*physical
    weighted_source=4*arb(6)/5*abs(C)*(3*alpha*(N+2)).exp()*abs(rho)**N/(1-abs(rho)*(3*alpha).exp())
    weighted_q=(abs(C)**2/(1-abs(rho)**2*(2*alpha).exp())).sqrt()
    weighted_mass=8*weighted_q*(2*alpha*(N+1)).exp()*znorm
    total=weighted_finite+weighted_source+weighted_mass
    extended=(physical*physical+(arb(6)**2+arb(4)**2)/25*abs(C*rho**N)**2).sqrt()
    return total,{'dyadic_denominator_power':D,'finite_physical_residual_l2':str(physical),
        'physical_residual_including_next_geometric_source_coefficient':str(extended),
        'normalization_contraction_l2':str(znorm),'weighted_finite':str(weighted_finite),
        'weighted_source_tail':str(weighted_source),'weighted_mass':str(weighted_mass),
        'weighted_residual_total':str(total),'boundary':'Physical A cutoff coupling and B cutoff crossing coupling explicitly included; no final physical bond deleted.'}

def scattering(p,h,x,sign,length,om):
    omega=sign*om(p,h,x);q=(-x).acos();out=[]
    for n in range(1,(length+1)//2+1):
        v=(n*q).sin();vp=((n-1)*q).sin()
        out.extend([-2*acb(0,1)*(p*v-h*vp)/omega,acb(v)])
    return out[:length],omega

def det3(v,w,z):
    return v[0]*(w[1]*z[2]-w[2]*z[1])-w[0]*(v[1]*z[2]-v[2]*z[1])+z[0]*(v[1]*w[2]-v[2]*w[1])

def formfactor_certificate(X,off=False):
    L=X.shape[1]
    pa,ha,pb,hb,xb,yb,om,root=root_data()
    if off:xb+=arb(1)/100
    AX=[-arb(99)/100,-arb(95)/100,xb];BX=[yb-arb(1)/100,yb+arb(1)/100]
    A=[];B=[];freq=acb(0)
    for x in AX:
        row,w=scattering(pa,ha,x,1,L+1,om);A.append(row);freq+=w
    for x in BX:
        row,w=scattering(pb,hb,x,-1,L+1,om);B.append(row);freq+=w
    Acols=[[A[s][j] for s in range(3)] for j in range(L+1)]
    Bmat=acb_mat([[B[s][j] for s in range(2)] for j in range(L)])
    Phi=acb(0)
    # Contract each independent cubic A index against both B scattering rows.
    # The final j=L-1 term is the essential bond crossing the support cutoff.
    for i in range(L-1):
        M=acb_mat([[az(X[i,j,k]) for k in range(L)] for j in range(L)])
        T=M*Bmat
        for j in range(L):
            k=j+1;m=arb(6 if j%2==0 else 4)/5
            coeff=B[0][k]*T[j,1]-B[1][k]*T[j,0]
            if k<L:coeff-=B[0][j]*T[k,1]-B[1][j]*T[k,0]
            Phi+=m*det3(Acols[j],Acols[k],Acols[i])*coeff
    return Phi,freq

def certificate(path):
    start=time.monotonic();X=np.load(path,allow_pickle=False)['Q1_cubic']
    assert X.shape[0]==X.shape[1]-1 and X.shape[1]==X.shape[2]
    assert np.array_equal(X,-X.swapaxes(1,2))
    ceiling,bounds=constants()
    res,record=residual_certificate(X)
    print('residual complete',time.monotonic()-start,record['weighted_residual_total'],flush=True)
    phi,omega=formfactor_certificate(X)
    error=ceiling*res
    lower=phi.real.lower()-error.upper();upper=phi.real.upper()+error.upper()
    stem=Path(path).stem.replace('research-halfline-','frozen-')
    save('referee-certificate-'+stem+'.json',{'input':path,'input_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        'residual':record,'root':bounds['root'],'independent_integer_residual_multiplier':ceiling,
        'finite_functional':str(phi),'frequency_sum_box':str(omega),'functional_error_upper':str(error.upper()),
        'infinite_real_lower':str(lower),'infinite_real_upper':str(upper),'strict_Re_greater_than_0.0001':bool(lower>arb('0.0001')),
        'nonzero_certified':bool(lower>0),'seconds':time.monotonic()-start,
        'independence':'Gaussian integer nearest-neighbour action and exterior determinant contraction implemented from source algebra; no discovery module, eigensystem, or reported residual imported.'})

def controls():
    L=6;base=L+1;rng=np.random.default_rng(51932658)
    X=np.zeros((L-1,L,L),complex)
    for _ in range(30):
        i=int(rng.integers(L-1));b,c=sorted(rng.choice(L,2,replace=False).tolist())
        X[i,b,c]+=int(rng.integers(-3,4))+1j*int(rng.integers(-3,4))
    X-=X.swapaxes(1,2)
    def mul(a,b):
        s=(-1)**sum(i>j for i in a for j in b)
        return s,tuple(sorted(set(a)^set(b)))
    def add(d,k,v):
        d[k]=d.get(k,0)+v
    brute={};without_crossing={}
    for j in range(L):
        t=(j,j+1,base+j,base+j+1);v=-3 if j%2==0 else -2
        for i in range(L-1):
            for b in range(L):
                for c in range(b+1,L):
                    xx=X[i,b,c]
                    if xx==0:continue
                    mon=(i,base+b,base+c)
                    st,out=mul(t,mon);sx,out2=mul(mon,t)
                    if len(out)==5 and sum(x<base for x in out)==3:
                        assert out==out2
                        add(brute,out,v*(st-sx)*xx)
                        if j<L-1:add(without_crossing,out,v*(st-sx)*xx)
    fast={}
    def wedge(aa,bb,coef):
        if len(set(aa))<3 or len(set(bb))<2:return
        s=(-1)**(sum(aa[k]>aa[l] for k in range(3) for l in range(k+1,3))+int(bb[0]>bb[1]))
        add(fast,tuple(sorted(aa)+[base+b for b in sorted(bb)]),s*coef)
    for j in range(L):
        k=j+1;m=6 if j%2==0 else 4
        for i in range(L-1):
            for r in range(L):
                wedge([j,k,i],[k,r],m*X[i,j,r])
                if k<L:wedge([j,k,i],[j,r],-m*X[i,k,r])
    keys=set(brute)|set(fast)
    assert all(brute.get(k,0)==fast.get(k,0) for k in keys)
    pa,ha,pb,hb,xb,yb,om,_=root_data()
    A=[scattering(pa,ha,x,1,L+1,om)[0] for x in [-arb(99)/100,-arb(95)/100,xb]]
    B=[scattering(pb,hb,x,-1,L+1,om)[0] for x in [yb-arb(1)/100,yb+arb(1)/100]]
    def dot(d):
        v=acb(0)
        for k,c in d.items():
            aa=[x for x in k if x<base];bb=[x-base for x in k if x>=base]
            da=det3(*[[A[s][j] for s in range(3)] for j in aa])
            db=B[0][bb[0]]*B[1][bb[1]]-B[1][bb[0]]*B[0][bb[1]]
            v+=az(c)/5*da*db
        return v
    direct=dot(brute);contracted,_=formfactor_certificate(X)
    diff=direct-contracted
    assert diff.real.contains(0) and diff.imag.contains(0) and abs(diff).upper()<arb('1e-12')
    boundary=direct-dot(without_crossing)
    assert abs(boundary).lower()>arb('1e-6')
    save('referee-adversarial-controls.json',{'exact_clifford_commutator_vs_exterior_formula':True,
        'quintic_coefficients_checked':len(keys),'interval_contraction_difference':str(diff),
        'cutoff_crossing_bond_contribution':str(boundary),'cutoff_crossing_nonzero':True,
        'test_input':'30 deterministic random Gaussian-integer cubic coefficients, seed 51932658, L=6; full physical crossing bond included.'})

if __name__=='__main__':
    if sys.argv[1]=='source':source()
    elif sys.argv[1]=='bounds':save('referee-root-bounds.json',constants()[1])
    elif sys.argv[1]=='solve':solve(int(sys.argv[2]))
    elif sys.argv[1]=='certificate':certificate(sys.argv[2])
    elif sys.argv[1]=='controls':controls()
