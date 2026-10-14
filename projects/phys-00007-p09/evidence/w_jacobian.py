"""Exact local-control Jacobian at the published W triangle solution.
Uses only stdlib; no mutable handoffs or cached answers are inputs.
Tangent convention V(theta)=(tensor exp(-i theta_jk sigma_k/2)) q^tensor3.
"""
from radical_algebra import *
from hashlib import sha256

labels=list(product((0,1),repeat=3))
paulis=[X,Y,Z]
def mv(m,v):return [sum(x*y for x,y in zip(row,v)) for row in m]
def dot(v,w):return sum(x.conj()*y for x,y in zip(v,w))
def graph_sum(v,label):
 return sum((-1)**(sum(t*x for t,x in zip(label,bits))+bits[0]*bits[1]+bits[0]*bits[2]+bits[1]*bits[2])*v[n] for n,bits in enumerate(labels))
V=tensor([q,q,q])
w=[one if n in (1,2,4) else zero for n in range(8)]
z=mv(V,w) # omit common W normalization sqrt3
A=[graph_sum(z,l) for l in labels] # omit graph normalization sqrt8
assert all(x.conj()*x==3 for x in A)
controls=[tensor([p if h==j else I for h in range(3)]) for j in range(3) for p in paulis]
dz=[[-i*Q(1,2)*x for x in mv(C,z)] for C in controls]
D=[[graph_sum(v,l) for v in dz] for l in labels]
J=[[(A[n].conj()*d+d.conj()*A[n])*Q(1,24) for d in D[n]] for n in range(8)]
assert all(sum(row[k] for row in J)==0 for k in range(9))
assert all(v==v.conj() for row in J for v in row)

# Independent differential formula using graph stabilizer moments, not amplitudes.
K=[tensor([X if h==j else Z for h in range(3)]) for j in range(3)]
moments=[];MJ=[]
for s in labels[1:]:
 S=tensor([I,I,I])
 for k,bit in enumerate(s):
  if bit:S=mul(S,K[k])
 assert dot(z,mv(S,z))*Q(1,3)==0
 moments.append(S)
 row=[]
 for C in controls:
  comm=add(mul(C,S),scale(-1,mul(S,C)))
  row.append(i*Q(1,6)*dot(z,mv(comm,z)))
 MJ.append(row)
for n,l in enumerate(labels):
 for k in range(9):
  assert J[n][k]==sum((-1)**sum(x*y for x,y in zip(l,s))*MJ[h][k] for h,s in enumerate(labels[1:]))*Q(1,8)

def eliminate(M):
 """Division-free exact elimination; track invertible row operations."""
 M=[row.copy() for row in M]; nr=len(M); nc=len(M[0]); E=[[F(int(j==k)) for k in range(nr)] for j in range(nr)]
 piv=[]; rrow=0
 for col in range(nc):
  candidates=[h for h in range(rrow,nr) if M[h][col]!=0]
  if not candidates:continue
  h=candidates[0];M[h],M[rrow]=M[rrow],M[h];E[h],E[rrow]=E[rrow],E[h]
  pivot=M[rrow][col]
  for h in range(nr):
   if h==rrow or M[h][col]==0:continue
   f=M[h][col]
   M[h]=[pivot*x-f*y for x,y in zip(M[h],M[rrow])]
   E[h]=[pivot*x-f*y for x,y in zip(E[h],E[rrow])]
  piv.append(col);rrow+=1
  if rrow==nr:break
 assert all(v==0 for row in M[rrow:] for v in row)
 return rrow,piv,M,E
rank,piv,R,E=eliminate(J[:7])
mrank,mpiv,MR,ME=eliminate(MJ)
assert rank==mrank
left=E[rank:]
assert all(sum(c*J[n][k] for n,c in enumerate(v))==0 for v in left for k in range(9))
# Transparent certificates replacing elimination's arbitrarily scaled null vectors.
ell=[-2,-2,0,-2,0,0,1]
assert all(sum(c*MJ[n][k] for n,c in enumerate(ell))==0 for k in range(9))
pell=[5,4,4,1,4,1,1]
assert all(sum(c*J[n][k] for n,c in enumerate(pell))==0 for k in range(9))
sqrt2=2*r*a*b
assert sqrt2*sqrt2==2
for h,j in [(3,0),(1,1),(0,2)]:
 for k in range(3):
  assert MJ[h][3*k]==0
  assert MJ[h][3*k+1]==r*(Q(1,3) if k==j else Q(-2,9))
  assert MJ[h][3*k+2]==(2*a*b*Q(1,3) if k==j else zero)
def determinant(m):
 if len(m)==1:return m[0][0]
 return sum((-1)**k*v*determinant([row[:k]+row[k+1:] for row in m[1:]]) for k,v in enumerate(m[0]) if v!=0)
minor=determinant([[MJ[h][k] for k in [2,5,8,0,3,6]] for h in [3,1,0,5,4,2]])
assert minor==-r*Q(16,6561)
null=[[zero,sqrt2 if j==h else zero,F(-3 if j==h else 2)] for h in range(3) for j in range(3)]
null=[sum(null[3*h:3*h+3],[]) for h in range(3)]
assert all(sum(x*y for x,y in zip(row,v))==0 for row in MJ for v in null)
# Curvature of the missing moment in the three tangent null directions.
O=add(moments[6],scale(-2,add(add(moments[0],moments[1]),moments[3])))
Hs=[]
for v in null:
 H=[[zero for _ in range(8)] for _ in range(8)]
 for t,C in zip(v,controls):H=add(H,scale(t*Q(1,2),C))
 Hs.append(H)
def comm(A,B):return add(mul(A,B),scale(-1,mul(B,A)))
Hessian=[[-Q(1,6)*dot(z,mv(add(comm(H,comm(T,O)),comm(T,comm(H,O))),z)) for T in Hs] for H in Hs]
assert all(v==0 for row in Hessian for v in row)
Oz=mv(O,z)
state_obstruction_norm=dot(Oz,Oz)*Q(1,3)
delta=mv(dag(V),Oz) # normalized perturbation ket is this vector /sqrt3
assert dot(w,delta)==0 and dot(delta,delta)*Q(1,3)==13
assert state_obstruction_norm==13
out_extra={'moment_left_null_simple':ell,'probability_left_null_simple_seven_rows':pell,
 'rank_six_minor':{'moment_rows_zero_based':[3,1,0,5,4,2],'control_columns_zero_based':[2,5,8,0,3,6],'determinant':'-16 sqrt3 /6561','exact':minor.record()},
 'control_kernel_exact':record(null),'control_kernel_description':'v_h: X_j=0, Y_j=sqrt2 delta_jh, Z_j=2-5 delta_jh',
 'missing_moment':'<K1 K2 K3>-2(<K1>+<K2>+<K3>)',
 'missing_moment_applied_to_transformed_W_exact':[v.record() for v in Oz],
 'missing_moment_applied_to_transformed_W_norm_squared_exact':state_obstruction_norm.record(),
 'missing_moment_applied_to_transformed_W_norm_squared_numeric':state_obstruction_norm.val().real,
 'obstructed_state_tangent_numerator_exact':[v.record() for v in delta],
 'obstructed_state_path':'psi(t)=(W+t delta_normalized)/sqrt(1+13t^2), delta_normalized=V0^dag O V0 W; dimensionless real t',
 'obstructed_state_missing_moment_derivative':26,
 'missing_moment_kernel_hessian_exact':record(Hessian),'missing_moment_kernel_hessian_numeric':[[v.val().real for v in row] for row in Hessian]}
out={'tangent_convention':'left exp(-i theta sigma/2), controls (1X,1Y,1Z,2X,2Y,2Z,3X,3Y,3Z)',
 'probability_labels':labels,'probability_jacobian_exact':record(J),'probability_jacobian_numeric':[[v.val().real for v in row] for row in J],
 'seven_constraint_rows':'labels 000 through 110; row 111 follows normalization',
 'rank':rank,'pivot_columns_zero_based':piv,'left_null_vectors_exact':record(left),
 'left_null_vectors_numeric':[[v.val().real for v in row] for row in left],
 'moment_labels':labels[1:],'moment_jacobian_exact':record(MJ),'moment_jacobian_numeric':[[v.val().real for v in row] for row in MJ],
 'moment_rank':mrank,'moment_left_null_vectors_exact':record(ME[mrank:]),
 'checks':{'normalization_derivative':'exact zero','moment_vs_probability':'all 72 entries agree by Walsh transform','left_null':'exactly zero'},
 'scope':'Rank at one published solution only. Rank deficiency neither disproves encodability nor excludes another regular solution.'}
out.update(out_extra)
Path('evidence/w-jacobian.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['rank','pivot_columns_zero_based','probability_jacobian_numeric','moment_rank','moment_jacobian_numeric','moment_left_null_simple','control_kernel_description','missing_moment_kernel_hessian_numeric','missing_moment_applied_to_transformed_W_norm_squared_numeric','checks']},indent=2))
