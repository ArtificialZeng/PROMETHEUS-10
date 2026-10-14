#!/usr/bin/env python3
"""Independent satisfied-bond chain recursion and weighted geometric Kac-Ward.
Does not import check_fan or read any first-checker outputs.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,sys,datetime
import sympy as s
HERE=Path(__file__).resolve().parent
sys.set_int_max_str_digits(20000)

def dump(name,data): (HERE/name).write_text(json.dumps(data,indent=2)+'\n')

def chain(n,p,q,C):
    # Three bonds at the first auxiliary spin; three more at each subsequent spin.
    plus,minus=(p**3,q**3) if C==1 else (p*p*q,p*q*q)
    for _ in range(1,n):
        plus,minus=p*p*(p*plus+q*minus),q*q*(q*plus+p*minus)
    return plus+minus

def logarithm_interval(r,terms=80):
    z=(r-1)/(r+1)
    assert 0<z<1
    low=2*sum((z**(2*k+1)/Q(2*k+1) for k in range(terms)),Q(0))
    high=low+2*z**(2*terms+1)/(Q(2*terms+1)*(1-z*z))
    return low,high

def root_bisect():
    def f(r): return r**3-r**2+r-3
    lo,hi=Q(1),Q(2)
    for _ in range(80):
        mid=(lo+hi)/2
        if f(mid)<0: lo=mid
        else: hi=mid
    assert f(lo)<0<f(hi)
    ll,_=logarithm_interval(lo); _,lh=logarithm_interval(hi)
    tl,th=2/lh,2/ll
    assert Q(44035,10000)<tl<th<Q(44045,10000)
    return {'critical_r_polynomial':'r^3-r^2+r-3','r_lower':str(lo),'r_upper':str(hi),
            'Tc_over_J_lower':str(tl),'Tc_over_J_upper':str(th),
            'Tc_over_J_display':[float(tl),float(th)],
            'published_three_decimal_4_404_correct_rounding':True,
            'uniqueness':'derivative 3*r^2-2*r+1 is positive for every real r',
            'logarithm_control':'positive artanh series with explicit geometric remainder, 80 terms'}

def main():
    a,b=s.symbols('a b')
    weights=[a,b,b,a,b,b]
    z=(s.sqrt(3)+s.I)/2 # exp(i*pi/6), from geometric directed turn angles.
    rows=[]; phase_powers=[]
    for i in range(6):
        row=[]; powerrow=[]
        for j in range(6):
            d=(j-i)%6
            if d>3: d-=6
            if d==3:
                row.append(s.Integer(0)); powerrow.append(None)
            else:
                row.append(weights[i]*s.expand(z**d)); powerrow.append(d)
        rows.append(row); phase_powers.append(powerrow)
    W=s.Matrix(rows)
    print('Geometric 6x6 Kac-Ward determinant started',flush=True)
    det=s.expand((s.eye(6)-W).det(method='domain-ge'))
    det=s.Poly(det,a,b,extension=(s.sqrt(3),s.I)).as_expr()
    P=1-a-2*b-2*a*b-b*b+a*b*b
    assert s.expand(det-P**2)==0
    print('Exact determinant equals signed triangular polynomial squared',flush=True)
    A,B=s.symbols('A B',positive=True)
    rational=s.factor(P.subs({a:(A-1)/(A+1),b:(B-1)/(B+1)}))
    expected=4*(2*B-A*(B*B-1))/((A+1)*(B+1)**2)
    assert s.factor(rational-expected)==0
    x=s.symbols('x')
    isotropic=s.factor(P.subs({a:x,b:x}))
    assert s.expand(isotropic-(x+1)*(x*x-4*x+1))==0
    n,p,q=1024,11,10
    wp,wm=chain(n,p,q,1),chain(n,p,q,-1)
    w0=(p*q*(p+q))**n
    up,um=Q(wp,w0),Q(wm,w0)
    margin=Q(p*p,q*q)*up-um-2
    assert margin>0 and up>um>1
    # A simple rational lower certificate avoids interpreting thousands of digits.
    assert margin>Q(1)
    dump('independent-chain-certificate.json',{'N':n,'p':p,'q':q,
          'satisfied_bond_trace_plus_integer':str(wp),
          'satisfied_bond_trace_minus_integer':str(wm),
          'zero_field_trace_integer':str(w0),
          'U_plus':str(up),'U_minus':str(um),'ordering_margin':str(margin),
          'ordering_margin_greater_than_1':True})
    baseline=root_bisect()
    dump('input-b.json',{'representation':'geometric Kac-Ward principal turn-angle matrix plus unnormalized satisfied-bond dynamic recursion',
          'source':'EJP18(2013)44 Definition2.1 and Proposition2.2 pp5-6; Theorem1.1 pp2-3',
          'directed_angles_in_units_pi_over_3':[0,1,2,3,4,5],
          'weights':['a','b','b','a','b','b'],'phase_powers_of_exp_i_pi_over_6':phase_powers,
          'backtracking':'opposite directed angle omitted',
          'KW_determinant':str(s.factor(det)),
          'satisfied_bond_recurrence':{'initial_C_plus':['p^3','q^3'],'initial_C_minus':['p^2*q','p*q^2'],
          'next':['p^2*(p*v_plus+q*v_minus)','q^2*(q*v_plus+p*v_minus)'],
          'normalization':'(p*q*(p+q))^N'},
          'independence':'no first-checker data, code, graph, or polynomial read; common primary model and criticality theorem only'})
    dump('independent-results.json',{'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'weighted_KW_identity':'det(I-W)=(1-a-2b-2ab-b^2+ab^2)^2',
          'temperature_sign_identity':str(rational),
          'isotropic_signed_factor':str(isotropic),
          'triangular_physical_root':'2-sqrt(3)','triangular_Tc_over_J':'4/log(3)',
          'half_interpolated_triangular':baseline,
          'large_N_margin_greater_than_1':True,
          'limitations':'Same proposer worker; independently coded representations, not fresh referee or external peer review.'})
    print(json.dumps({'KW_exact':True,'isotropic_exact':True,'baseline_Tc':baseline['Tc_over_J_display'],
          'large_N_margin_greater_than_1':True},indent=2))

if __name__=='__main__':main()
