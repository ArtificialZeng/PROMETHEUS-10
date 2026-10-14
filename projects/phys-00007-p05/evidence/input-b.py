"""B: independently propagate two normalized Bell pairs by gate truth rules.
Does not read or import input-a.py, input-a.json, or any matrix values from A.
"""
import json
from fractions import Fraction as R
from pathlib import Path

def circuit(name, a, b):
    if name=='identity': return [(a,b,R(1))]
    if name=='CNOT': return [(a,a^b,R(1))]
    if name=='SWAP': return [(b,a,R(1))]
    if name=='controlled_rotation':
        if a==0: return [(a,b,R(1))]
        return [(1,0,R(3,5)),(1,1,R(4,5))] if b==0 else [(1,0,-R(4,5)),(1,1,R(3,5))]
    raise ValueError(name)

cases=[]
for name in ('identity','CNOT','SWAP','controlled_rotation'):
    ket=[R(0)]*16
    # Start with sum_ab |a,a>_RA,A' |b,b>_RB,B' /2.
    # Store after propagation in RA,A,RB,B, grouped X:Y.
    for a in (0,1):
        for b in (0,1):
            for oa,ob,amp in circuit(name,a,b):
                ket[8*a+4*oa+2*b+ob]+=amp/2
    assert sum(z*z for z in ket)==1
    for noise in (R(0),R(1,2),R(1)):
        matrix=[[(1-noise)*ket[i]*ket[j]+(noise/16 if i==j else 0) for j in range(16)] for i in range(16)]
        cases.append({'gate':name,'p':str(noise),'ket':list(map(str,ket)),
                      'omega':[[str(z) for z in row] for row in matrix]})
out={'method':'independent Bell-pair propagation and projector plus scalar white noise',
     'basis':['RA','A','RB','B'],'index':'8*RA+4*A+2*RB+B','cases':cases}
Path('evidence/input-b.json').write_text(json.dumps(out,indent=2)+'\n')
print('B: 12 normalized 16x16 Choi matrices written from independent circuit/vector rules.')
