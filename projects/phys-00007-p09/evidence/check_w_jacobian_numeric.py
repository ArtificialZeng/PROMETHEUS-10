"""Separately coded finite differences for exact Jacobian, stdlib binary64.
Reads exact output only after calculation for comparison. Not a fresh referee.
"""
import math,cmath,json
from itertools import product
from pathlib import Path
bits=list(product((0,1),repeat=3))
a=math.sqrt((3+math.sqrt(3))/6);b=math.sqrt((3-math.sqrt(3))/6)
q=[[1j*a,b],[-b,-1j*a]]
ps=[[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]]
def mm(A,B):return [[sum(A[j][h]*B[h][k] for h in range(2)) for k in range(2)] for j in range(2)]
def probabilities(theta):
 U=[]
 for j in range(3):
  t=theta[3*j:3*j+3];norm=math.sqrt(sum(v*v for v in t))
  R=[[complex(int(h==k)) for k in range(2)] for h in range(2)]
  if norm:
   R=[[math.cos(norm/2)*int(h==k)-1j*math.sin(norm/2)*sum(t[n]*ps[n][h][k] for n in range(3))/norm for k in range(2)] for h in range(2)]
  U.append(mm(R,q))
 z=[sum(math.prod(U[j][x[j]][y[j]] for j in range(3)) for y in [(0,0,1),(0,1,0),(1,0,0)])/math.sqrt(3) for x in bits]
 return [abs(sum((-1)**(sum(s[j]*x[j] for j in range(3))+x[0]*x[1]+x[0]*x[2]+x[1]*x[2])*v for x,v in zip(bits,z))/math.sqrt(8))**2 for s in bits]
assert max(abs(p-1/8) for p in probabilities([0]*9))<1e-14
computed=[]
for step in [1e-2,1e-3,1e-4,1e-5]:
 J=[[] for _ in range(8)]
 for k in range(9):
  t=[0]*9;t[k]=step;plus=probabilities(t);t[k]=-step;minus=probabilities(t)
  for n in range(8):J[n].append((plus[n]-minus[n])/(2*step))
 computed.append((step,J))
expected=json.loads(Path('evidence/w-jacobian.json').read_text())['probability_jacobian_numeric']
errors=[{'step':step,'maximum_entry_error':max(abs(x-y) for row,reference in zip(J,expected) for x,y in zip(row,reference))} for step,J in computed]
assert errors[-1]['maximum_entry_error']<1e-9
assert errors[1]['maximum_entry_error']<errors[0]['maximum_entry_error']/50
print(json.dumps({'method':'independent direct SU2 rotation and graph amplitudes; central differences','precision':'binary64, diagnostic only; exact certificates in w_jacobian.py','errors':errors,'status':'pass'},indent=2))
