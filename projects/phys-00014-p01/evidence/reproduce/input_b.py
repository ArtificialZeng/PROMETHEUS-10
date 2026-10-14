"""Independent B: source Eq.20, angular identities, high-precision radial integrals.
Does not import input_a, read input-a.json or use its numerical coefficients.
"""
from pathlib import Path
import json
import mpmath as mp

OUT=Path(__file__).resolve().parent
mp.mp.dps=80
a=mp.pi/4

def matrix(m):
    return {'real':[[float(mp.re(z)) for z in row] for row in m],
            'imag':[[float(mp.im(z)) for z in row] for row in m]}

def blank():return [[mp.mpc(0) for _ in range(4)] for _ in range(4)]

def radial(f):return 3/a**3*mp.quad(lambda r:r*r*f(r),[0,a])

def main():
    # Derive from c|0> - i s n_j |j>, E[n_i n_j]=delta_ij/3.
    c=radial(lambda r:mp.cos(r)**2)
    s=radial(lambda r:mp.sin(r)**2)/3
    q=radial(lambda r:r*mp.sin(r)*mp.cos(r))/3
    c2=radial(lambda r:r*r*mp.cos(r)**2)
    s2=radial(lambda r:r*r*mp.sin(r)**2)/3
    # Closed primitives provide a separate check on adaptive mp.quad.
    c_closed=mp.mpf(1)/2+3/(4*a)-3/(8*a**3)
    q_closed=3/(8*a)-3/(16*a**3)
    data=[]
    for lam in [mp.mpf(0),mp.mpf('.5'),mp.mpf(1)]:
        aa=(1-lam)*c+lam/4;bb=(1-lam)*s+lam/4;qq=(1-lam)*q
        g=blank();g[0][0]=aa
        for i in range(1,4):g[i][i]=bb
        gs=[g]
        for i in range(1,4):
            gi=blank();gi[0][i]=1j*qq;gi[i][0]=-1j*qq;gs.append(gi)
        g2=blank();g2[0][0]=(1-lam)*c2+lam*(3*a*a/5)/4
        for i in range(1,4):g2[i][i]=(1-lam)*s2+lam*(3*a*a/5)/4
        data.append({'lambda':float(lam),'A':str(aa),'B':str(bb),'Q':str(qq),
                     'Gamma':[matrix(m) for m in gs],'Gamma_r2':matrix(g2)})
    # Independently transcribed computational spin columns in SOURCE input-output order.
    z=mp.sqrt(mp.mpf('.5'))
    S=[[z,0,0,z],[0,z,1j*z,0],[0,z,-1j*z,0],[z,0,0,-z]]
    record={'representation':'spin basis ordered 0,x,y,z; source input-output order',
            'source_equations':'16,18-20,3-4,24-26','spin_columns_S':matrix(S),'a':str(a),
            'angular_identities':'E[n_i]=0; E[n_i n_j]=delta_ij/3; all odd direction moments vanish',
            'radial_density':'3 r^2/a^3 on 0<=r<=a','precision_decimal_digits':80,'noise_runs':data,
            'closed_radial_checks':{'C':str(c_closed),'Q':str(q_closed),
                 'C_difference':str(c-c_closed),'Q_difference':str(q-q_closed)},
            'input_files_read':'none; Eq.20 separately transcribed and moment integrals independently derived'}
    (OUT/'input-b.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'input':'B','A':str(c),'B':str(s),'Q':str(q),
                      'closed_form_residuals':[str(c-c_closed),str(q-q_closed)]}))

if __name__=='__main__':main()
