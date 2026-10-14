"""A: direct matrices and normalized channel action on matrix units.
No imports from input B or its output. Fraction arithmetic is exact.
"""
import json
from fractions import Fraction as F
from pathlib import Path

GATES = {
    'identity': [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
    'CNOT': [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],
    'SWAP': [[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],
    'controlled_rotation': [[1,0,0,0],[0,1,0,0],[0,0,F(3,5),-F(4,5)],[0,0,F(4,5),F(3,5)]],
}
cases=[]
for name, data in GATES.items():
    u=[[F(z) for z in row] for row in data]
    assert all(sum(u[r][j]*u[r][k] for r in range(4)) == (j==k) for j in range(4) for k in range(4))
    for p in (F(0),F(1,2),F(1)):
        omega=[[F(0) for j in range(16)] for i in range(16)]
        # |r><s|_reference tensor N(|r><s|)/4, order RA,RB,A,B.
        for r in range(4):
            for s in range(4):
                for o in range(4):
                    for v in range(4):
                        action=(1-p)*u[o][r]*u[v][s] + (p/F(4) if r==s and o==v else 0)
                        omega[4*r+o][4*s+v]=action/F(4)
        cases.append({'gate':name,'p':str(p),'unitary':[[str(z) for z in row] for row in u],
                      'omega':[[str(z) for z in row] for row in omega]})
out={'method':'matrix-unit channel action, independently transcribed real gate matrices',
     'basis':['RA','RB','A','B'],'index':'8*RA+4*RB+2*A+B','cases':cases}
Path('evidence/input-a.json').write_text(json.dumps(out,indent=2)+'\n')
print('A: 12 normalized 16x16 Choi matrices written using exact rational channel action.')
