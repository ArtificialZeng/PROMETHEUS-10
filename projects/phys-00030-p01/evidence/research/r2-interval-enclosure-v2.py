"""Outward interval attempt for the FIXED r1 387-dot Hamiltonian.

No cached quadrature answers are used. mpmath.iv supplies directed endpoints.
Trigonometric Hamiltonian coefficients are enclosed at 250 decimal digits.
Real continuants are converted to centered Taylor intervals to retain cancellation.
An adaptive heap integrates interval ranges, never a quadrature error estimate.
All work runs synchronously in this one process; no other worker is launched.
"""
import argparse, datetime, heapq, json, math, signal, time
from pathlib import Path
import mpmath as mp

iv = mp.iv
mp.mp.dps = 110
iv.dps = 250
n = 128
scale = iv.mpf(1)/100
gc = iv.mpf(200000)/scale
theta = iv.pi/(2*n)
gf = 1/(2*iv.sin(theta))
h2 = [1/(4*iv.sin((2*l+1)*theta)*iv.sin((2*l-1)*theta)) for l in range(1,n)]
lam2 = gf*gc
a = gf*scale/iv.sqrt(iv.mpf(5000)*35000)
product_h2 = iv.mpf(1)
for x in h2:
    product_h2 *= x

def cp(h):
    old, cur = [iv.mpf(1)], [iv.mpf(0),iv.mpf(1)]
    for x in h:
        new = [iv.mpf(0)]+cur
        for j,y in enumerate(old):
            new[j] -= x*y
        old,cur = cur,new
    return cur

F = cp(h2)
B = cp(h2[1:])
G = cp(h2[1:-1])
K = F.copy()
for j,x in enumerate(G):
    K[j] += gf**2*x
# K is evaluated with its ACTUAL interval coefficients. No presumed exact
# Butterworth identity is substituted; cancellation is enclosed in these bytes.
FE = F[::2]
BE = B[1::2]

def lower(x):
    return mp.mp.make_mpf(x._mpi_[0])
def upper(x):
    return mp.mp.make_mpf(x._mpi_[1])
def absupper(x):
    return max(abs(lower(x)),abs(upper(x)))
def numeric(x):
    # Conservative binary64 export only; the kernel uses arbitrary precision.
    return [math.nextafter(float(lower(x)),-math.inf),
            math.nextafter(float(upper(x)),math.inf)]
def hull(lo,hi):
    return iv.mpf([lo,hi])
def clip_unit(x):
    return hull(max(mp.mpf(0),lower(x)),min(mp.mpf(1),upper(x)))

setup_record = {
    'coefficient_precision_decimal_digits':250,
    'F_degree':len(F)-1,'B_degree':len(B)-1,
    'K_degree':len(K)-1,
    'largest_nonleading_K_coefficient_absolute_upper':str(max(absupper(x) for x in K[:-1])),
    'Gamma_f_in_q_units':numeric(gf),
    'product_filter_hopping_squared_in_q_units':numeric(product_h2),
    'coefficient_generation':'Real Hermitian continuant recurrence, independent of old scattering scripts',
}
iv.dps = 85
mp.mp.dps = 100
ORDER = 20
BINOM = [[math.comb(k,ORDER) if k>=ORDER else 0 for k in range(len(p))] for p in [FE,BE]]
ABS = [[hull(absupper(x),absupper(x)) for x in p] for p in [FE,BE]]

# Nearest-rounded point jets use an explicit forward-error envelope. All
# trigonometric coefficients and non-polynomial functions still use iv.
CENTERS=[]
RELATIVE=[]
for p in [FE,BE]:
    centers=[(lower(x)+upper(x))/2 for x in p]
    errors=[]
    for c,x in zip(centers,p):
        if c==0:
            if lower(x)!=0 or upper(x)!=0:raise ArithmeticError('uncertain zero coefficient')
            errors.append(iv.mpf(0))
        else:errors.append(abs(x-iv.mpf(c))/abs(iv.mpf(c)))
    CENTERS.append(centers)
    RELATIVE.append(max(upper(x) for x in errors))
ROUND_OPS=4*(max(len(FE),len(BE))+1)*(ORDER+1)
UNIT_ROUND=iv.mpf(2)**(1-mp.mp.prec)
GAMMA=ROUND_OPS*UNIT_ROUND/(1-ROUND_OPS*UNIT_ROUND)
setup_record['point_jet_precision_bits']=mp.mp.prec
setup_record['point_jet_rounding_operations_bound']=ROUND_OPS
setup_record['point_jet_gamma_upper']=numeric(GAMMA)[1]
setup_record['coefficient_relative_radius_upper']=[float(x) for x in RELATIVE]

def poly_interval(p,q,mid,absp,binom):
    """Degree-19 Taylor range with a monomial derivative remainder.

    Basic mpf + and * are nearest rounded. Every path in the generalized
    Horner recurrence has fewer than ROUND_OPS operations. The absolute
    recurrence bounds forward error by gamma*S, with S itself inflated by
    1/(1-gamma). Coefficient intervals add their relative radius times S.
    This explicitly controls cancellation of the large monomial coefficients.
    """
    pi=0 if p is FE else 1
    centers=CENTERS[pi]
    xc=mp.mpf(mid)**2
    x=q**2
    dx=x-iv.mpf(xc)
    radius=hull(absupper(dx),absupper(dx))
    xmax=hull(max(abs(lower(x)),abs(upper(x))),max(abs(lower(x)),abs(upper(x))))
    jets=[mp.mpf(0) for _ in range(ORDER)]
    absolute_jets=[mp.mpf(0) for _ in range(ORDER)]
    for c in centers[::-1]:
        for k in range(ORDER-1,0,-1):
            jets[k]=jets[k]*xc+jets[k-1]
            absolute_jets[k]=absolute_jets[k]*xc+absolute_jets[k-1]
        jets[0]=jets[0]*xc+c
        absolute_jets[0]=absolute_jets[0]*xc+abs(c)
    jet=[]
    for v,A in zip(jets,absolute_jets):
        error=(GAMMA+RELATIVE[pi])*iv.mpf(A)/(1-GAMMA)
        jet.append(iv.mpf(v)+hull(-upper(error),upper(error)))
    result=jet[-1]
    for c in jet[-2::-1]:result=result*dx+c
    derivative_coefficient=iv.mpf(0)
    for k in range(len(p)-1,ORDER-1,-1):
        derivative_coefficient=derivative_coefficient*xmax+absp[k]*binom[k]
    remainder=derivative_coefficient*radius**ORDER
    return result+hull(-upper(remainder),upper(remainder))

def horner(p,x):
    v = iv.mpf(0)
    for c in p[::-1]:
        v = v*x+c
    return v

def transmissions(lo,hi):
    q = hull(lo,hi)
    mid = (lo+hi)/2
    f = poly_interval(FE,q,mid,ABS[0],BINOM[0])
    b = q*poly_interval(BE,q,mid,ABS[1],BINOM[1])
    k = horner(K,q)
    gamma = gf*iv.sqrt((1+scale*q/5000)*(1-scale*q/35000))
    g = (k-f)/gf**2
    bk = q*b-lam2*g
    dr,di = f-a*q*b,gamma*b
    cr,ci = q*f-lam2*b-a*q*bk,gamma*bk
    root3gc = iv.sqrt(3)*gc
    norm0 = cr**2+ci**2
    normp = (cr-root3gc*dr)**2+(ci-root3gc*di)**2
    normm = (cr+root3gc*dr)**2+(ci+root3gc*di)**2
    denominator = norm0*normp*normm
    if lower(denominator)<=0:
        return hull(0,1),hull(0,1),False
    # Reverse numerator C-i gc D expanded BEFORE interval evaluation. This
    # retains the very small filter reflection instead of subtracting phases.
    leak_re = q*f+gc*(gamma-gf)*b-a*q*bk
    leak_im = q*(gamma+gc*a)*b-gc*(gamma/gf)*k+gc*(gamma/gf-1)*f
    main_re,main_im = cr-gc*di,ci+gc*dr
    prefactor = 4*gamma**2*lam2**2*product_h2**2*gc**2/denominator
    reverse = prefactor*(leak_re**2+leak_im**2)
    forward = prefactor*(main_re**2+main_im**2)
    return clip_unit(reverse),clip_unit(forward),True

expminus,expplus = iv.exp(-24),iv.exp(24)
def ranges(lo,hi):
    q=hull(lo,hi)
    u,v,validated=transmissions(lo,hi)
    z=iv.exp(scale*q)
    e0,e1,e2=iv.exp(-1),iv.exp(3),iv.exp(24)
    d0,d1,d2=1+z*e0,1+z*e1,1+z*e2
    ju=z*(e1-e0)/(d0*d1)
    j12=z*(e2-e1)/(d1*d2)
    jv=ju+j12
    eu=25*ju+21*j12
    ev=4*ju+25*j12
    J=u*ju+v*jv
    entropy=u*eu+v*ev
    Au=z*(e1*(expminus-1)+e0*(expplus-1))/(d0*d1)
    Av=z*(e2*(expminus-1)+e0*(expplus-1))/(d0*d2)
    M=1+u*Au+v*Av
    # For X in {-1,0,1}, exp(-24)<=M<=exp(24) exactly.
    M=hull(max(lower(expminus),lower(M)),min(upper(expplus),upper(M)))
    chi=iv.log(M)
    residual=u*(-76*ju-84*j12)+v*(8*ju-76*j12)-chi
    return [scale*x for x in [residual,J,entropy,chi]],validated

def tail_bounds():
    # q cuts [-8192,16384], delta cuts [-81.92,163.84].
    # A nonzero count needs at least one hole/particle in the three leads.
    holes=3*iv.exp(iv.mpf('-81.92')+24)
    particles=3*iv.exp(1-iv.mpf('163.84'))
    jt=2*(holes+particles)
    et=28*jt
    ct=2*iv.exp(24)*(holes+particles)
    dt=24*jt+4*et+ct
    return [dt,jt,et,ct]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seconds',type=int,default=660)
    parser.add_argument('--target-width',type=float,default=.004)
    parser.add_argument('--output',default='evidence/research/r2-interval-enclosure-v2.json')
    args=parser.parse_args()
    start=time.monotonic()
    output=Path(args.output)
    data={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status':'in_progress','fixed_model':'evidence/research/r1-tightbinding-model.md',
          'setup':setup_record,'interval_precision_decimal_digits':85,'Taylor_order':ORDER,
          'target_width':args.target_width,'results':[],'mode':'interval_ranges_not_quadrature_estimates',
          'limits':'Proposer calculation; no independent referee acceptance', 'point_rounding':'Explicit generalized-Horner forward error envelope; see setup fields'}
    def save():
        data['elapsed_seconds']=time.monotonic()-start
        output.write_text(json.dumps(data,indent=2)+'\n')
    # Dyadic endpoints avoid undocumented decimal-to-binary parameter changes.
    points=sorted(set([-8192.,16384.,0.]+[float(j)/32 for j in range(-64,65)]
                      +[sign*2.**k for sign in [-1,1] for k in range(2,15)
                        if -8192<=sign*2.**k<=16384]))
    heap=[];serial=0;total=[iv.mpf(0) for _ in range(4)];failures=0
    def panel(lo,hi):
        nonlocal serial,failures
        vals,ok=ranges(lo,hi)
        vals=[x*iv.mpf(hi-lo) for x in vals]
        width=upper(vals[0])-lower(vals[0])
        serial+=1
        if not ok:failures+=1
        return (-float(width),serial,lo,hi,vals,ok)
    def report(label):
        tails=tail_bounds()
        enclosed=[x+hull(-upper(t),upper(t)) for x,t in zip(total,tails)]
        row={'stage':label,'active_panels':len(heap),'evaluated_panels':serial,
             'fallback_evaluations':failures,'integral_enclosures':dict(zip(['Delta','J','sigma_over_kB','chi_minus24'],map(numeric,enclosed))),
             'analytic_tail_bounds':dict(zip(['Delta','J','sigma_over_kB','chi_minus24'],[numeric(t)[1] for t in tails]))}
        data['results'].append(row);save();print(json.dumps(row),flush=True)
        return enclosed
    last_report=start
    def ceiling(signum,frame):raise TimeoutError('bounded enclosure computation ceiling')
    signal.signal(signal.SIGALRM,ceiling);signal.alarm(args.seconds)
    try:
        for lo,hi in zip(points[:-1],points[1:]):
            row=panel(lo,hi);heapq.heappush(heap,row)
            total=[x+y for x,y in zip(total,row[4])]
        report('initial')
        while float(upper(total[0])-lower(total[0]))>args.target_width:
            row=heapq.heappop(heap);_,_,lo,hi,old,_=row
            mid=(lo+hi)/2
            if mid==lo or mid==hi:raise ArithmeticError('binary endpoint subdivision exhausted')
            left,right=panel(lo,mid),panel(mid,hi)
            heapq.heappush(heap,left);heapq.heappush(heap,right)
            # Re-sum endpoints separately; interval subtraction would retain
            # old uncertainty rather than replacing the old panel.
            replaced=[]
            for x,y,z,w in zip(total,old,left[4],right[4]):
                ls=iv.mpf(lower(x))-iv.mpf(lower(y))+iv.mpf(lower(z))+iv.mpf(lower(w))
                us=iv.mpf(upper(x))-iv.mpf(upper(y))+iv.mpf(upper(z))+iv.mpf(upper(w))
                replaced.append(hull(lower(ls),upper(us)))
            total=replaced
            if time.monotonic()-last_report>=20:
                report('refinement');last_report=time.monotonic()
        enclosure=report('final')
        if lower(enclosure[0])>0 and lower(enclosure[1])>0 and lower(enclosure[2])>0:
            data['status']='positive_residual_enclosed_proposer_only'
        else:data['status']='completed_enclosure_no_positive_witness'
        data['panels']=[{'q_interval':[r[2],r[3]],'integrated_ranges':[numeric(x) for x in r[4]],'transmission_denominator_validated':r[5]} for r in sorted(heap,key=lambda r:r[2])]
    except TimeoutError as e:
        data['status']='incomplete_computation_ceiling';data['obstacle']=str(e)
        if heap:report('partial_at_ceiling')
    except Exception as e:
        data['status']='failed_enclosure_attempt';data['obstacle']=repr(e)
        if heap:report('partial_at_failure')
        raise
    finally:
        signal.alarm(0);save();print(json.dumps({'status':data['status'],'seconds':data['elapsed_seconds']}),flush=True)

if __name__=='__main__':main()
