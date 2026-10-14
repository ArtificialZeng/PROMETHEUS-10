"""A: direct source-rendering transcription; Kronecker matrix units, MSB vertex 0."""
import sympy as S
import json
from pathlib import Path
I=S.I
local=S.Matrix([[-1,0,0,-S.Symbol('s')*S.conjugate(S.Symbol('u'))],[0,0,0,0],[0,0,0,0],[-S.Symbol('s')*S.Symbol('u'),0,0,-S.Symbol('s')**2]])
def build(n,edges,s,phases):
    out=S.zeros(2**n)
    for (i,j),u in zip(edges,phases):
        h=S.Matrix([[-1,0,0,-s*S.conjugate(u)],[0,0,0,0],[0,0,0,0],[-s*u,0,0,-s*s]])
        for row in range(4):
            for col in range(4):
                if h[row,col]==0: continue
                factors=[S.eye(2) for _ in range(n)]
                for v,r,c in [(i,row//2,col//2),(j,row%2,col%2)]:
                    m=S.zeros(2);m[r,c]=1;factors[v]=m
                out+=h[row,col]*S.kronecker_product(*factors)
    return out
if __name__=='__main__':
    data={'source':'2602.03605v1 PDF p26 h(z), Eq77; Ju-Nagda PDF p2 normalized EPR', 'basis':'vertex 0 is leftmost / most significant bit', 'local_negative_h_rows':[[ '-1','0','0','-s conjugate(u)'],['0','0','0','0'],['0','0','0','0'],['-s u','0','0','-s^2']], 'phase':'u=exp(i theta)', 'parent_map':'H(s=1,u=1)=-2 sum Eij', 'implementation':'code/input_a.py'}
    Path('evidence/reproduction/input-a.json').write_text(json.dumps(data,indent=2)+'\n')
