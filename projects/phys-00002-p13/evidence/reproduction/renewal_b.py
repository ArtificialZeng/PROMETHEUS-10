"""Independent backward/renewal route. Does not import or read route A.
Positive nearest-neighbor walk, exact Fraction series through fourth order.
"""
from fractions import Fraction as F
from math import factorial

def single_site_cumulants(u,w):
    assert u>w>0
    # First-step conditioning: w*f^2-(u+w+s)*f+u=0.
    a=[F(1)]+[F(0)]*4
    for n in range(1,5):
        a[n]=(w*sum(a[j]*a[n-j] for j in range(1,n))-a[n-1])/(u-w)
    # Log coefficients using f'=f*g': n*f_n=sum_{j=1}^n j*g_j*f_{n-j}.
    g=[F(0)]*5
    for n in range(1,5):
        g[n]=a[n]-sum(F(j,n)*g[j]*a[n-j] for j in range(1,n))
    return [(-1)**n*factorial(n)*g[n] for n in range(1,5)]

def closed_cumulants(u,w):
    d=u-w; R=u+w
    return [1/d,R/d**3,(3*R**2-d**2)/d**5,
            3*R*(5*R**2-3*d**2)/d**7]

def backward_matrix(a,b,variable,multiply,plus,negative):
    r=variable(7); ri=variable(7,-1)
    # Independent departure-rate transcription: diagonal -a_i-b_i;
    # forward next state times r, backward previous state times 1/r.
    return [[negative(plus(a[0],b[0])),multiply(a[0],r),multiply(b[0],ri)],
            [multiply(b[1],ri),negative(plus(a[1],b[1])),multiply(a[1],r)],
            [multiply(a[2],r),multiply(b[2],ri),negative(plus(a[2],b[2]))]]

def cycle_coefficients(u,w):
    # Nine directed spanning-tree terms derived by deleting each destination root.
    c1=(u[0]*u[1]+u[0]*u[2]+u[1]*u[2]
        +w[0]*w[1]+w[0]*w[2]+w[1]*w[2]
        +u[0]*w[1]+u[1]*w[2]+u[2]*w[0])
    return c1,sum(u)+sum(w)

def periodic_cycle_cumulants(u,w):
    """Backward first-passage equations on the infinite periodic lift.
    f_i is the transform for passage i -> i+1, with all backward excursions.
    No determinant, cycle coefficient, or route-A value is used.
    """
    nsites=len(u)
    def solve(matrix,rhs):
        aug=[list(map(F,row))+[F(x)] for row,x in zip(matrix,rhs)]
        for i in range(nsites):
            pivot=next(j for j in range(i,nsites) if aug[j][i])
            aug[i],aug[pivot]=aug[pivot],aug[i]
            div=aug[i][i];aug[i]=[x/div for x in aug[i]]
            for j in range(nsites):
                if j!=i:
                    fac=aug[j][i];aug[j]=[a-fac*b for a,b in zip(aug[j],aug[i])]
        return [row[-1] for row in aug]
    # (u_i+w_{i-1}+s)f_i = u_i+w_{i-1} f_{i-1} f_i.
    matrix=[[F(0)]*nsites for _ in u]
    for i in range(nsites):
        matrix[i][i]=u[i];matrix[i][(i-1)%nsites]-=w[(i-1)%nsites]
    f=[[F(1)]+[F(0)]*4 for _ in u]
    for n in range(1,5):
        rhs=[]
        for i in range(nsites):
            prev=(i-1)%nsites
            rhs.append(-f[i][n-1]+w[prev]*sum(f[prev][j]*f[i][n-j] for j in range(1,n)))
        coeff=solve(matrix,rhs)
        for i in range(nsites):f[i][n]=coeff[i]
    # A completed cycle passes each phase once; strong Markov property adds logs.
    total=[F(0)]*5
    for row in f:
        g=[F(0)]*5
        for n in range(1,5):
            g[n]=row[n]-sum(F(j,n)*g[j]*row[n-j] for j in range(1,n))
            total[n]+=g[n]
    return [(-1)**n*factorial(n)*total[n] for n in range(1,5)]
