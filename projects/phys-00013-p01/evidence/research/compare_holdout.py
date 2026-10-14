"""Independent-input comparison against the previously saved degree8 formula."""
import json
from pathlib import Path
import sympy as sp
A=json.loads(Path('evidence/research/sym8-input-a.json').read_text())
B=json.loads(Path('evidence/research/sym8-input-b.json').read_text())
index={tuple(n):i for i,n in enumerate(A['basis'])}
def reverse(i): return ((i&1)<<2)|(i&2)|((i&4)>>2)
mapping=[]
for n in B['basis']:
    m=[0]*8
    for i,v in enumerate(n): m[reverse(i)]=v
    mapping.append(index[tuple(m)])
assert sorted(mapping)==list(range(A['dimension']))
for side in ['site1','site3']:
    a={(i,j):v for i,j,v in A['endpoint_casimirs'][side]}
    b={(mapping[i],mapping[j]):v for i,j,v in B['endpoint_casimirs'][side]}
    assert a==b
assert A['cross_gram']==B['cross_gram']
assert A['trace_moments']==B['trace_moments']
assert A['ranks']==B['ranks']==[1485,2205,1800,840,105]
G=sp.diag(*A['ranks']); C=sp.Matrix(A['cross_gram']); M=G.inv()*C
prediction={sp.Rational(6,(r+2)*(2*r+3)):1 for r in range(5)}
assert M.eigenvals()==prediction
one=sp.ones(5,1); global_projection=one*(one.T*G)/A['dimension']
assert global_projection**2==global_projection
assert M*global_projection==global_projection
assert (M-global_projection).eigenvals()=={sp.Rational(0):1,**{e:m for e,m in prediction.items() if e!=1}}
result={'degree':8,'dimension':A['dimension'],'ranks':A['ranks'],
        'entrywise_Casimir_match_including_zeros':True,'all_25_trace_moments_match':True,
        'all_25_cross_gram_entries_match':True,'whole_global_identity_removed':True,
        'observed_signed_cosines':[str(e) for e in sorted(prediction,reverse=True)],
        'new_holdout_angle':'1/11','formula_prediction_match':True,
        'frozen_proposal':'evidence/research/all-degree-proposal.md','pre_holdout_rank_correction':'evidence/research/proposal-correction-before-holdout.md',
        'coverage':'One new completed sector r=4; finite data support but do not prove the all-degree statement.',
        'independence':'Same agent; A differential-operator integer algebra and B tensor-swap rational algebra share no computed inputs.'}
Path('evidence/research/sym8-holdout-result.json').write_text(json.dumps(result,indent=2)+'\n')
Path('evidence/research/sym8-basis-map.json').write_text(json.dumps({'B_to_A':mapping,'signs':'none; symmetric occupation coordinates'},indent=2)+'\n')
print(json.dumps(result,indent=2))
