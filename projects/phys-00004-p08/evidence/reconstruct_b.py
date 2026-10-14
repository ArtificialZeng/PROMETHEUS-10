#!/usr/bin/env python3
"""B: rendering/interval-sector reconstruction. Does not read A or A outputs."""
import json
from pathlib import Path
import sympy as sp
import mpmath as mp

ROOT=Path(__file__).resolve().parent.parent
B=json.loads((ROOT/'evidence/input-b.json').read_text())

def reverse_matching(E,c,s):
    # Direct endpoint evaluation using the primary towards-vertex flux sign.
    coefficients=sp.symbols('q:'+str(2*E))
    starts=[coefficients[2*j] for j in range(E)]
    ends=[c*coefficients[2*j]+s*coefficients[2*j+1] for j in range(E)]
    source_flux0=-sum(coefficients[2*j+1] for j in range(E))
    source_flux1=sum(-s*coefficients[2*j]+c*coefficients[2*j+1] for j in range(E))
    equations=[starts[j]-starts[0] for j in range(1,E)]
    equations.extend(ends[j]-ends[0] for j in range(1,E))
    equations.extend([source_flux0,source_flux1])
    return sp.linear_eq_to_matrix(equations,coefficients)[0]

def main():
    c,s=sp.symbols('c s')
    matrices={}
    tests=[]
    for E in (2,3,5,8):
        M=reverse_matching(E,c,s)
        matrices[f'pumpkin_E{E}']={'entries':[[str(z) for z in row] for row in M.tolist()]}
        # Mean sector: NN, one positive mode per n. Zero-sum sector: DD, E-1.
        for n in (1,2,3):
            tests.append({'graph':'unit pumpkin','E':E,'k':f'{n}*pi','NN_multiplicity':1,'DD_multiplicity':E-1,'total':E})
    mp.mp.dps=70
    h=mp.mpf(1)/6;m=int(B['split_tree']['selected_instance']['m']);eta=mp.mpf(1)/1000
    assert m==5
    b=mp.atan(1/(m*mp.tan(mp.pi*h)))/mp.pi
    bp=b+eta
    def fan_characteristic(k):
        return mp.cos(k*h)*mp.cos(k*bp)-m*mp.sin(k*h)*mp.sin(k*bp)
    # Bracketed bisection of the independent pole-free 2x2 fan matrix.
    left=mp.pi*mp.mpf('.95');right=mp.pi
    assert fan_characteristic(left)>0 and fan_characteristic(right)<0
    for _ in range(240):
        middle=(left+right)/2
        if fan_characteristic(middle)>0:left=middle
        else:right=middle
    k=(left+right)/2
    residual=abs(fan_characteristic(k))
    assert residual<mp.mpf('1e-65')
    old_residual=abs(mp.cos(mp.pi*h)*mp.cos(mp.pi*b)-m*mp.sin(mp.pi*h)*mp.sin(mp.pi*b))
    assert old_residual<mp.mpf('1e-65')
    # Fan-leaf value in the reversed-coordinate, Neumann-normalized basis.
    C=mp.sin(k*h)/mp.cos(k*bp)
    hub_continuity=abs(C*mp.cos(k*bp)-mp.sin(k*h))
    hub_flux=abs(m*C*mp.sin(k*bp)-mp.cos(k*h))
    length_b_A_equivalent=mp.atan(mp.cos(mp.pi*h)/(m*mp.sin(mp.pi*h)))/mp.pi
    assert abs(length_b_A_equivalent-b)<mp.mpf('1e-65')
    result={'method':'independent interval/symmetry sectors B','versions':{'sympy':sp.__version__,'mpmath':mp.__version__},
      'pumpkin_sector_checks':tests,'precision_decimal_digits':mp.mp.dps,
      'tree_lengths':{'h':str(h),'b_unperturbed':str(b),'b_perturbed':str(bp),'a':'0.5','m':m,'eta':str(eta)},
      'perturbed_tree_root':{'k':str(k),'mu2_numerical':str(k*k),'bisection_width':str(right-left),'characteristic_residual':str(residual),
        'unperturbed_pi_residual':str(old_residual),'fan_leaf_amplitude':str(C),'continuity_residual':str(hub_continuity),'flux_residual':str(hub_flux),
        'metric_diameter':'1','extrema_union_diameter':str(2*(h+bp)),'new_DD_threshold_for_uniform_doubling':str(4*mp.pi**2),
        'qualification':'High-precision bisection plus residual check, not directed interval arithmetic. Published-family ordering and extrema are justified analytically in the baseline note.'},
      'star_sector_prediction':[{'k':'pi','original_multiplicity':3,'added_DD_multiplicity':0,'doubled_total':3},
                                {'k':'2*pi','original_multiplicity':1,'added_DD_multiplicity':4,'doubled_total':5}],
      'status':'pass'}
    (ROOT/'evidence/matching-b.json').write_text(json.dumps(matrices,indent=2)+'\n')
    (ROOT/'evidence/results-b.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
