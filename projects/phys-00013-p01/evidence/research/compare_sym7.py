"""Compare independent inputs and check exact full invariant removal."""
import json, hashlib
from pathlib import Path
import sympy as s

A=json.loads(Path('evidence/research/sym7-input-a.json').read_text())
B=json.loads(Path('evidence/research/sym7-input-b.json').read_text())
ia={tuple(n):i for i,n in enumerate(A['basis'])}
def reverse_mode(i): return ((i&1)<<2)|(i&2)|((i&4)>>2)
mapping=[]
for n in B['basis']:
    m=[0]*8
    for i,v in enumerate(n): m[reverse_mode(i)]=v
    mapping.append(ia[tuple(m)])
assert sorted(mapping)==list(range(A['dimension']))
assert A['ranks']==B['ranks']
assert A['trace_moments']==B['trace_moments']
assert A['cross_gram']==B['cross_gram']
for endpoint in ['site1','site3']:
    ma={(i,j):v for i,j,v in A['endpoint_casimirs'][endpoint]}
    mb={(mapping[i],mapping[j]):v for i,j,v in B['endpoint_casimirs'][endpoint]}
    assert ma==mb
    print(endpoint+': all Casimir entries match under bit reversal (zeros included); '+str(len(ma))+' nonzero entries.')
G=s.diag(*A['ranks']); C=s.Matrix(A['cross_gram']); M=G.inv()*C
one=s.ones(4,1); d=A['dimension']; global_coeff=one*(one.T*G)/d
assert global_coeff**2==global_coeff
assert M*global_coeff==global_coeff*M==global_coeff
assert C*one==G*one
char=s.factor((M-global_coeff).charpoly().as_expr())
eigs=(M-global_coeff).eigenvals()
assert eigs=={s.Rational(0):1,s.Rational(2,5):1,s.Rational(3,14):1,s.Rational(2,15):1}
w=(M-s.Rational(2,5)*s.eye(4)).nullspace()[0]
assert (one.T*G*w)[0]==0
assert C*w==s.Rational(2,5)*G*w
result={'degree':7,'dimension':d,'casimir_entrywise_comparison':'exact_pass',
        'basis_map':'evidence/research/sym7-basis-map.json','all_16_cross_gram_entries':'exact_pass',
        'completed_local_dimensions':[4,4],
        'raw_local_dimension_from_independent_Cauchy_branching':sum(b['dim_SU2']**2 for b in B['branching']),
        'global_dimension':1,
        'global_dimension_reason':'Sym^7 C8 is irreducible, highest weight 7 omega1; complete SU8 commutant CI. A(X)=Tr(X)I/3432.',
        'global_coefficient_projector':[[str(v) for v in row] for row in global_coeff.tolist()],
        'nonfixed_signed_characteristic_polynomial':str(char),
        'largest_nonfixed_cosine':'2/5','squared_cosines':['4/25','9/196','4/225'],
        'witness_coefficients':[str(v) for v in w],
        'witness_trace':str((one.T*G*w)[0]),'witness_HS_norm_squared':str((w.T*G*w)[0]),
        'strict_exceedance_of_half':False,
        'original_status':'unresolved','candidate_kind':'none',
        'scope':'Exact failed counterexample test in one representation; not an all-PU8 theorem or referee acceptance.'}
Path('evidence/research/sym7-basis-map.json').write_text(json.dumps({'convention':'B mode4c+2b+a maps to A4a+2b+c; occupations permute without wedge signs; monomial metrics agree','B_to_A':mapping},indent=2)+'\n')
Path('evidence/research/sym7-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
