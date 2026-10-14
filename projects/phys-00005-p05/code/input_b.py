"""B: independently derive action from ket-bra; vertex 0 is LSB. No A import."""
import sympy as S
import json
from pathlib import Path
def build(n,edges,s,phases):
    H=S.zeros(1<<n)
    for x in range(1<<n):
        for (p,q),u in zip(edges,phases):
            a=(x>>p)&1;b=(x>>q)&1
            if a!=b: continue
            y=x ^ (1<<p) ^ (1<<q)
            if a==0:
                H[x,x]-=1
                H[y,x]-=s*u
            else:
                H[x,x]-=s**2
                H[y,x]-=s*S.conjugate(u)
    return H
if __name__=='__main__':
    data={'derivation':'phi=<00 component 1; 11 component s*u>; -phi phi-dagger sends 00 to -00-s*u*11 and 11 to -s*conjugate(u)*00-s^2*11; annihilates 01,10', 'basis':'integer x=sum_v b_v 2^v, vertex 0 least significant', 'independent_input':'Derived from defining ket in Eq64 and phase replacement in Eq77, rechecked against primary rendered h(z); no A data or cached matrices read', 'published_parent':'normalized ket (00+11)/sqrt(2) makes E=(I+XX-YY+ZZ)/4; negative unnormalized model=-2E at s=1', 'implementation':'code/input_b.py'}
    Path('evidence/reproduction/input-b.json').write_text(json.dumps(data,indent=2)+'\n')
