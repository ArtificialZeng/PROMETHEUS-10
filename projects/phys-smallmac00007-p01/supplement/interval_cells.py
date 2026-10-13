"""Integer interval certificate. See README.md and the manuscript appendix."""
import argparse
import datetime
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import sys
import time

BITS = 128
S = 1 << BITS
ZERO = (0, 0)
ONE = (S, S)
LOG_TERMS = 56
COS_TERMS = 25

def ceildiv(n, d):
    assert d > 0
    return -((-n) // d)

def rat(n, d=1):
    return (n*S//d, ceildiv(n*S, d))

def add(x, y):
    return (x[0]+y[0], x[1]+y[1])

def neg(x):
    return (-x[1], -x[0])

def sub(x, y):
    return add(x, neg(y))

def mul(x, y):
    z = [a*b for a in x for b in y]
    return (min(z)//S, ceildiv(max(z), S))

def posmul(x, y):
    assert x[0] >= 0 and y[0] >= 0
    return (x[0]*y[0]//S, ceildiv(x[1]*y[1], S))

def scale(x, n, d=1):
    if n < 0:
        return neg(scale(x, -n, d))
    return (x[0]*n//d, ceildiv(x[1]*n, d))

def div(x, y):
    assert y[0] > 0
    lows = [a*S//b for a in x for b in y]
    highs = [ceildiv(a*S, b) for a in x for b in y]
    return (min(lows), max(highs))

def atan_fraction(n):
    # 80-term alternating expansion at 1/n; partial sum is a lower bound.
    m = 80
    p = sum((Fraction((-1)**j, (2*j+1)*n**(2*j+1)) for j in range(m)), Fraction())
    return p, p+Fraction(1, (2*m+1)*n**(2*m+1))

a2 = atan_fraction(2)
a3 = atan_fraction(3)
# tan(atan(1/2)+atan(1/3))=1, both angles positive and sum < pi/2.
pi_fracs = (4*(a2[0]+a3[0]), 4*(a2[1]+a3[1]))
PI = (pi_fracs[0].numerator*S//pi_fracs[0].denominator,
      ceildiv(pi_fracs[1].numerator*S, pi_fracs[1].denominator))
assert PI[0] > 3*S and PI[1] < ceildiv(22*S, 7)

def positive_log_reduced(y):
    assert y[0] >= S
    z = div(sub(y, ONE), add(y, ONE))
    assert z[0] >= 0 and z[1] <= S//2
    z2 = posmul(z,z)
    power = z
    total = ZERO
    for j in range(LOG_TERMS):
        total = add(total, scale(power, 1, 2*j+1))
        power = posmul(power,z2)
    total = scale(total,2)
    # Tail of 2*atanh(z), using z <= 1/2 and 1/(1-z^2) <= 4/3.
    tail = ceildiv(8*S, 3*(2*LOG_TERMS+1)*(1 << (2*LOG_TERMS+1)))
    return (total[0], total[1]+tail)

LN2 = positive_log_reduced(rat(2))

def log_interval(x):
    assert x[0] > 0
    k = x[0].bit_length()-1-BITS
    y = scale(x, 1 << (-k)) if k <= 0 else scale(x, 1, 1 << k)
    return add(positive_log_reduced(y), scale(LN2,k))

COS_REM = Fraction(22,7)**(2*COS_TERMS) / math.factorial(2*COS_TERMS)
COS_ERR = ceildiv(COS_REM.numerator*S, COS_REM.denominator)

def cosine(x):
    assert 0 <= x[0] <= x[1] < ceildiv(22*S,7)
    x2 = posmul(x,x)
    total = ONE
    term = ONE
    for j in range(1,COS_TERMS):
        term = neg(scale(mul(term,x2),1,(2*j-1)*(2*j)))
        total = add(total,term)
    # Taylor through degree 48; degree-49 coefficient is zero, remainder <= x^50/50!.
    return (total[0]-COS_ERR,total[1]+COS_ERR)

def sine(x):
    # Independent scalar use of cos(pi/2-x); all calls here have 0<x<pi/2.
    return cosine(sub(scale(PI,1,2),x))

def entropy(c):
    p = scale(add(ONE,c),1,2)
    q = sub(ONE,p)
    assert p[0] > 0 and q[0] > 0 and p[1] < S and q[1] < S
    return neg(div(add(mul(p,log_interval(p)),mul(q,log_interval(q))),LN2))

def node(j,n):
    angle = scale(PI,j,2*n)
    if j == 0:
        return angle, ONE, ZERO
    if j == n:
        return angle, neg(ONE), ZERO
    c = cosine(scale(angle,2))
    h = entropy(c)
    assert h[0] >= 0 and h[1] <= S+100000
    return angle,c,h

def bounds_json(x):
    # Decimal representations below are outward rounded, using integer division only.
    D = 10**20
    def fmt(i):
        sign = '-' if i < 0 else ''
        i = abs(i)
        return sign+str(i//D)+'.'+str(i%D).zfill(20)
    return {'lower_integer':str(x[0]),'upper_integer':str(x[1]),'denominator':str(S),
            'lower_decimal':fmt(x[0]*D//S),'upper_decimal':fmt(ceildiv(x[1]*D,S))}

def scalar_check():
    s06,s04 = sine(rat(3,5)),sine(rat(2,5))
    d = scale(add(s06,s04),1,2)
    w = rat(66,125)
    sw = sine(w)
    q = div(d,sw)
    w0 = div(sub(rat(1,2),mul(q,w)),sub(ONE,q))
    L = sub(add(add(rat(-211,50),scale(s06,5907,100)),scale(s04,5487,100)),rat(1989,40))
    U = mul(q,entropy(sw))
    gap = sub(L,U)
    assert q[0] > 0 and q[1] < S
    assert w0[0] > 0 and w0[1] < PI[0]//2
    assert L[0]*10000 > 7758*S
    assert U[1]*10000 < 7653*S
    assert gap[0]*10000 > 105*S
    # Baseline checks with exact endpoint facts: h(0)=1, F(0,0)=1,
    # F(1,-1)=0, minimum deterministic cost pi*|C0-C1|/4.
    assert entropy(ZERO)[0] <= S <= entropy(ZERO)[1]
    center_domain_gap = sub(sine(rat(1,2)),d)
    assert center_domain_gap[0] > 0
    return {k:bounds_json(v) for k,v in [('pi',PI),('ln2',LN2),('q',q),('w0',w0),
        ('d',d),('L_off',L),('U_mid',U),('strict_gap',gap),('sin_half_minus_d',center_domain_gap)]}

def run(n):
    start = time.monotonic()
    left = node(0,n)
    running = None
    global_lower = None
    min_i = None
    minimizer = None
    max_node_width = 0
    for j in range(n):
        right = node(j+1,n)
        al,cl,hl = left
        ar,cr,hr = right
        # Binary entropy along theta is increasing then decreasing; any cell
        # has entropy >= min(entropy(left),entropy(right)), including pi/4.
        hs = min(hl[0],hr[0])
        f0 = hs//2 - ceildiv(5907*cl[1],100) - ceildiv(1989*ar[1],20)
        f1 = hs//2 + 5487*cr[0]//100 + 1989*al[0]//20
        if running is None or f0 < running:
            running,min_i = f0,j
        candidate = running+f1
        if global_lower is None or candidate < global_lower:
            global_lower,minimizer = candidate,[min_i,j]
        max_node_width = max(max_node_width,hr[1]-hr[0])
        left = right
        if (j+1) % 8192 == 0:
            print(json.dumps({'progress_cells':j+1,'cells_total':n,'elapsed_seconds':round(time.monotonic()-start,3)}),flush=True)
    analytic_reverse = rat(-21,5)[0]
    full_lower = min(global_lower,analytic_reverse)
    passed = full_lower*50 > -211*S
    return {'N_cells':n,'full_domain_affine_pass':passed,
        'ordered_triangle_lower':bounds_json((global_lower,global_lower)),
        'reverse_triangle_lower':bounds_json((analytic_reverse,analytic_reverse)),
        'global_lower':bounds_json((full_lower,full_lower)),
        'margin_above_t':bounds_json(sub((full_lower,full_lower),rat(-211,50))),
        'minimum_cell_indices':minimizer,'max_entropy_node_width_integer':str(max_node_width),
        'seconds':time.monotonic()-start,'scalar_enclosures':scalar_check()}

