"""Exact short-delay witness and elementary remainder/tail certificates.

This script does not read either numerical propagation implementation.
The proof, including the physical meaning of the computation, is in proof.md.
"""
import json
from pathlib import Path
import sympy as s

OUT = Path('evidence/research')
r = s.symbols('r', positive=True)
rates = [(r, 1, 1), (1, r, 1), (1, 1, r)]
S = [s.Matrix([[-a-c, 0, c], [0, -a-b, b], [c, b, -b-c]])
     for a, b, c in rates]
C = s.zeros(3)
boundary_terms = []
for i in range(3):
    j = (i+1) % 3
    comm = S[j]*S[i] - S[i]*S[j]
    term = s.factor(rates[i][0]*rates[j][0]*comm[0, 1])
    boundary_terms.append(str(term))
    C += rates[i][0]*rates[j][0]*comm
coefficient = s.factor(C[0, 1] / (6*(r+2)))
assert s.simplify(coefficient + (r-1)**2/(6*(r+2))) == 0
reverse_order=[0,2,1]
reverse_comm=s.zeros(3)
for index,i in enumerate(reverse_order):
    j=reverse_order[(index+1)%3]
    reverse_comm+=rates[i][0]*rates[j][0]*(S[j]*S[i]-S[i]*S[j])
assert s.simplify(reverse_comm[0,1]+C[0,1])==0
assert coefficient.subs(r,1)==0

# Independent exact check by explicitly composing absorbing-chain series in
# a different state order. Here the density is the derivative of absorption.
basis = [2, 0, 1, '+', '-']
pos = {state: i for i, state in enumerate(basis)}
Q = []
for a, b, c in rates:
    G = s.zeros(5)
    for u, v, k in [(0,1,a), (1,0,a), (1,2,b), (2,1,b), (2,0,c), (0,2,c)]:
        dest = '+' if (u,v)==(0,1) else '-' if (u,v)==(1,0) else v
        G[pos[u], pos[dest]] += k
        G[pos[u], pos[u]] -= k
    assert G*s.ones(5,1) == s.zeros(5,1)
    Q.append(G)
b_coefficients = []
for degree in range(3):
    total = 0
    for i in range(3):
        j = (i+1) % 3
        poly = sum((Q[i]**u * Q[j]**(degree-u) for u in range(degree+1)), s.zeros(5))
        flux = poly*Q[j]
        total += rates[i][0]*(flux[pos[1],pos['+']] - flux[pos[0],pos['-']])
    b_coefficients.append(s.factor(total/(s.factorial(degree+1)*(r+2))))
assert all(s.simplify(u-v)==0 for u,v in zip(b_coefficients,[0,0,coefficient]))

base = s.Matrix([[2,0,-1],[0,2,-1],[-1,-1,2]])
positive = base-s.eye(3)/2
minors = [positive[:i,:i].det() for i in (1,2,3)]
assert all(x>0 for x in minors)
S10 = [z.subs(r,10) for z in S]
original=[]
for triple in rates:
    a,b,c=triple
    L=s.Matrix([[-a-c,a,c],[a,-a-b,b],[c,b,-b-c]])
    assert L*s.ones(3,1)==s.zeros(3,1)
    assert s.ones(1,3)*L==s.zeros(1,3)
    assert L==L.T
    original.append(L)
for mat in S10:
    assert mat == mat.T
    assert max(sum(abs(mat[i,j]) for j in range(3)) for i in range(3)) <= 22
    assert all(e >= 0 for e in (-mat-base).eigenvals())

delta = s.Rational(1,20000)
# |R(x)| <= (7/2) x sum_{d>=3} (22x)^d/d!
#          <= (7/12)22^3 x^4 exp(22x).
# exp(y)<=1/(1-y) for 0<=y<1 supplies a rational comparison.
remainder_over_x3 = s.Rational(7,12)*22**3*delta/(1-22*delta)
assert remainder_over_x3 < s.Rational(9,16)
entropy_lower = s.Rational(27,4480)*delta**7
assert entropy_lower > 0
H = s.Integer(80)
tail_formula = s.Rational(80,3)*s.exp(-H/2)*(2*s.log(20)+22*H+44)
result = {
    'scope':'Exact model-level upper-bound counterexample; not a scientific referee verdict',
    'dimensionless_units':'x=tau/t_star; reported entropy is t_star*hat_sigma',
    'rates_family':[['r','1','1'],['1','r','1'],['1','1','r']],
    'killed_matrices_r10':[[list(map(str,row)) for row in mat.tolist()] for mat in S10],
    'weighted_boundary_commutator_entries':boundary_terms,
    'delta_x3_coefficient_family':str(coefficient),
    'absorbing_row_series_coefficients':list(map(str,b_coefficients)),
    'delta_x3_coefficient_r10':str(coefficient.subs(r,10)),
    'reversed_protocol_coefficient':str(s.factor(reverse_comm[0,1]/(6*(r+2)))),
    'constant_protocol_r1_coefficient':str(coefficient.subs(r,1)),
    'strict_interval_delta':str(delta),
    'remainder_bound_divided_by_x3':str(remainder_over_x3),
    'remainder_bound_below':'9/16',
    'density_difference_bound':'Psi_++ - Psi_-- <= -(9/16)*x^3 for 0<x<=1/20000',
    'strict_entropy_lower_bound':str(entropy_lower),
    'strict_entropy_lower_decimal':str(s.N(entropy_lower,12)),
    'full_entropy_exact':'0',
    'base_minus_half_identity_leading_minors':list(map(str,minors)),
    'density_bounds':'(x^2/2) exp(-11x) <= Psi_++,Psi_-- <= 10 exp(-x/2)',
    'entropy_tail_H80_formula':str(tail_formula),
    'entropy_tail_H80_decimal':str(s.N(tail_formula,12)),
    'normalization_tail_H80_bound':'sqrt(3)*exp(-40)',
    'precision':'symbolic rational arithmetic; displayed tail decimals illustrative, formula is the bound'
}
(OUT/'exact-result.json').write_text(json.dumps(result,indent=2)+'\n')
admissibility={
    'scope':'Input admissibility only; no target-bound acceptance',
    'family_domain':'t_star>0, r>0; three segments of duration t_star; reversed rates equal on every edge',
    'physical_generators_dimensionless':[[list(map(str,row)) for row in mat.tolist()] for mat in original],
    'conservation':'Both row and column sums vanish exactly',
    'positive_rates':'The six graph rates are r or 1; both strictly positive for r>0',
    'periodic_state':['1/3','1/3','1/3'],
    'local_detailed_balance':'F_i=f_ij=0, symmetric rates; every thermodynamic edge flux ratio is exactly one',
    'periodic_uniqueness':'Each positive-rate complete-graph segment propagator is strictly positive stochastic; its product has a unique stationary probability vector',
    'visible_events':['1->2','2->1'],
    'conditional_initial_states':['2','1'],
    'bar_event_flux_times_t_star':str((r+2)/9),
    'event_phase_density':'a(s)/(r+2) on dimensionless phase [0,3)',
    'r10_max_escape_rate_times_t_star':11,
    'joint_normalization':'Decay of killed survival, established by K-(1/2)I>0 for r=10; positive min(r,1) rescales it for the family',
    'full_entropy_zero':'Direct substitution of each edge flux ratio=1; only the target definition, no controller cost'
}
(OUT/'admissibility.json').write_text(json.dumps(admissibility,indent=2)+'\n')
print(json.dumps(result,indent=2))
