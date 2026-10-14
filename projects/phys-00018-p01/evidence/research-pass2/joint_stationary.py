"""Independent infinite-state stationary probabilities with rational enclosures.

For c=delta=d in {1,2}, beta=gamma=1, surviving RNAs have independent
Poisson-mixture protein marks; dead RNAs supply an independent compound
Poisson protein population. Coefficients are enclosed using alternating
Taylor sums and outward fixed-point integer convolution.
"""
from fractions import Fraction as F
import json, math
from pathlib import Path

BITS=192
Q=1<<BITS
ORDER=100

def bracket_alternating(terms):
    z=F(0);upper=None;lower=None
    for l in range(ORDER+2):
        z+=(-1 if l%2 else 1)*terms(l)
        if l==ORDER:upper=z
        if l==ORDER+1:lower=z
    assert 0<=lower<=upper
    return lower,upper

def fixed(lo,hi):
    return ((lo.numerator*Q)//lo.denominator,-((-hi.numerator*Q)//hi.denominator))

def mult(a,b):return ((a[0]*b[0])//Q,-((-a[1]*b[1])//Q))

def div(a,k):return (a[0]//k,-((-a[1])//k))

def conv(a,b,S):
    out=[]
    for k in range(S+1):
        lo=sum(a[j][0]*b[k-j][0] for j in range(k+1))
        hi=sum(a[j][1]*b[k-j][1] for j in range(k+1))
        out.append((lo//Q,-((-hi)//Q)))
    return out

def generate(d,R,S,path):
    assert d in {1,2}
    qa=[];levy=[(0,0)]
    for j in range(S+1):
        qa.append(fixed(*bracket_alternating(lambda l:F(math.factorial(d)*math.factorial(j+l),math.factorial(j)*math.factorial(l)*math.factorial(j+l+d)))))
        if j:
            levy.append(fixed(*bracket_alternating(lambda l:F(d*math.factorial(d)*math.factorial(j+l-1),math.factorial(j)*math.factorial(l)*math.factorial(j+l+d)))))
    # lambda_D = d*d! sum_{k>=1} (-1)^{k+1}/[k(d+k)!].
    lamlo,lamhi=bracket_alternating(lambda l:F(d*math.factorial(d),(l+1)*math.factorial(d+l+1)))
    elo,_=bracket_alternating(lambda l:lamhi**l/math.factorial(l))
    _,ehi=bracket_alternating(lambda l:lamlo**l/math.factorial(l))
    pd=[fixed(elo,ehi)]
    for k in range(1,S+1):
        lo=sum(j*levy[j][0]*pd[k-j][0] for j in range(1,k+1))
        hi=sum(j*levy[j][1]*pd[k-j][1] for j in range(1,k+1))
        pd.append((lo//(k*Q),-((-hi)//(k*Q))))
    e1=fixed(*bracket_alternating(lambda l:F(1,math.factorial(l))))
    pm=e1
    power=[(Q,Q)]+[(0,0)]*S
    probability=[]
    for m in range(R+1):
        cp=conv(power,pd,S)
        probability.extend(mult(pm,z) for z in cp)
        if m<R:
            power=conv(power,qa,S);pm=div(pm,m+1)
    middle=[F(lo+hi,2*Q) for lo,hi in probability]
    err=sum(F(hi-lo,2*Q) for lo,hi in probability)
    record={'route':'labelled Poisson RNA clusters; alive and dead RNA decomposition',
        'parameters':{'c':d,'delta':d,'beta':1,'gamma':1},'rectangle':{'RNA_cap':R,'protein_cap':S},
        'fixed_point_bits':BITS,'alternating_taylor_order':ORDER,'denominator':str(Q),
        'interval_probability_numerators':[[str(lo),str(hi)] for lo,hi in probability],
        'inside_probability_error_l1_upper':str(err),'dead_cluster_intensity_interval':[str(lamlo),str(lamhi)],
        'no_stationary_normalization_or_finite_generator_solve':True}
    Path(path).write_text(json.dumps(record,indent=2)+'\n')
    return middle,err,record
