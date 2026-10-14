"""Independent exact replay of generator constants, marginal moments and residuals.

Does not import the Riesz generator, use its float solve, or read mutable handoffs.
Same proposer context and preserved U/Palm inputs; not a scientific referee.
"""
from pathlib import Path
from fractions import Fraction as R
import math,json,sys

ROOT=Path(__file__).resolve().parents[2];OLD=ROOT/'evidence/research-pass3';NEW=ROOT/'evidence/research-pass4'
sys.set_int_max_str_digits(0)

def ivadd(x,y):return (x[0]+y[0],x[1]+y[1])
def ivmul(x,y):
    v=[a*b for a in x for b in y];return min(v),max(v)

def stirling_rows(n):
    rows=[[1]]
    for i in range(1,n+1):
        old=rows[-1];cur=[0]*(i+1)
        for j in range(1,i+1):cur[j]=old[j-1]+(j*old[j] if j<len(old) else 0)
        rows.append(cur)
    return rows

def independent_factorial_moments(d):
    # From the independently derived cluster PGF logarithm at y=1:
    # k-th factorial cumulant is (k-1)! d!/(d+k-1)!.
    kap=[R(0)]+[R(math.factorial(k-1)*math.factorial(d),math.factorial(d+k-1)) for k in range(1,7)]
    fm=[R(1)]
    for n in range(1,7):fm.append(sum(math.comb(n-1,k-1)*kap[k]*fm[n-k] for k in range(1,n+1)))
    return fm

def check_parent(d,n,oldmat,info):
    x=json.loads((NEW/f'riesz-d{d}-n{n}-exact.json').read_text());palm=json.loads((OLD/f'palm-delta{d}-S64.json').read_text())
    Q=int(palm['denominator']);p=[(R(int(a),Q),R(int(b),Q)) for a,b in palm['protein_probability_numerators']]
    s=[R(z) for z in x['scales']];os=[R(z) for z in info['exact_scales']]
    categories=p[1:n]+[(1-sum(z[1] for z in p[:n]),1-sum(z[0] for z in p[:n]))]
    assert all(R(1,4)<s[i]*s[i]*categories[i][1]<=1 for i in range(n))
    combos=[{i:R(1)} for i in range(n-1)]+[{j:s[-1]/os[j] for j in range(n-1,64)}]
    matrices={}
    for target,oldkey in [('U','U'),('entry_error_bounds','eU')]:
        old=[[R(z) for z in row] for row in oldmat[oldkey]]
        new=[[sum(ci*cj*old[i][j] for i,ci in a.items() for j,cj in b.items()) for b in combos] for a in combos]
        assert new==[[R(z) for z in row] for row in x[target]]
        matrices[target]=new
    U=matrices['U'];E=matrices['entry_error_bounds']
    fm=independent_factorial_moments(d);st=stirling_rows(7)
    tails={}
    for k in [4,5,6]:
        total=sum(st[k+1][j+1]*fm[j] for j in range(k+1))
        tails[k]=total-sum((i+1)**k*p[i][0] for i in range(n))
        assert tails[k]==R(x['tail_moments'][str(k)]) and tails[k]>=0
    assert R(x['alpha'])==(R(3,102400) if d==1 else R(1,187272))
    funcs={tag:[(R(int(a),Q),R(int(b),Q)) for a,b in seq] for tag,seq in palm['return_coefficient_numerators'].items()}
    funcs['Dg']=funcs['D1'];funcs['Dr']=[]
    for j in range(65):
        funcs['Dr'].append(ivadd(funcs['D1'][j],funcs['Dt1'][j]) if d==2 else
            ivadd(funcs['D1'][j],ivmul((R(-1,2),R(-1,2)),funcs['D2'][j])))
    reports=[]
    for tag,record in x['functions'].items():
        src=funcs[tag][1:n]+[(-sum(v[1] for v in funcs[tag][:n]),-sum(v[0] for v in funcs[tag][:n]))]
        src=[(s[i]*a,s[i]*b) for i,(a,b) in enumerate(src)]
        assert src==[(R(a),R(b)) for a,b in record['source_intervals']]
        v=[R(z) for z in record['approximant_coefficients']]
        residual=[]
        for i in range(n):
            mid=(src[i][0]+src[i][1])/2
            radius=(src[i][1]-src[i][0])/2
            residual.append(abs(mid-sum(U[i][j]*v[j] for j in range(n)))+radius+sum(E[i][j]*abs(v[j]) for j in range(n)))
        assert residual==[R(z) for z in record['scaled_head_residual_bounds']]
        rz=sum(residual[i]/s[i] for i in range(n));assert rz==R(record['count_zero_residual_upper'])
        H=rz**2/p[0][0]+sum((i+2)**4*(residual[i]/s[i])**2/p[i+1][0] for i in range(n-1))
        mean=(R(0),R(0));values=[R(0)]
        for i in range(n):
            val=s[i]*v[i];values.append(val);mean=ivadd(mean,ivmul(categories[i],(val,val)))
        vmax=max(abs(a-b) for a in values for b in mean);assert vmax==R(record['centered_approximant_sup_upper'])
        c=R(3,4) if d==1 else R(2)
        C=R(1) if tag in ['A','H'] else (R(5,2) if tag=='Dg' else (R(15,4) if d==1 else R(5)))
        T=C*C*tails[6]+2*C*c*vmax*tails[5]+(c*vmax)**2*tails[4]
        assert H==R(record['head_residual_W4dual_squared_upper'])
        assert T==R(record['tail_residual_W4dual_squared_upper'])
        delta=R(record['projection_error_dual_norm_upper'])
        assert delta>=0 and delta**2 >= (H+T)/R(x['alpha'])
        vn=sum(v[i]*v[j]*U[i][j]+abs(v[i]*v[j])*E[i][j] for i in range(n) for j in range(n))
        assert vn==R(record['approximant_U_norm_squared_upper'])
        nv=R(record['approximant_U_norm_upper']);assert nv>=0 and nv**2>=vn
        assert R(record['projection_norm_upper'])==nv+delta
        reports.append({'function':tag,'all_exact_residual_and_tail_identities_replayed':True,
            'both_rational_square_root_enclosures_verified':True})
    return x,{'d':d,'basis':n,'stationary_moment_representation':'factorial cumulants from exact cluster marginal PGF, then Bell recurrence',
        'tail_moments_replayed':True,'change_of_basis_and_entry_errors_replayed':True,'functions':reports}

def replay_block(key,full):
    cert=json.loads((OLD/f'l2-certificate-n64-{key}-contraction.json').read_text())
    N=128;K=[[int(z) for z in row] for row in cert['K_numerators']]
    T=[[int(z) for z in row] for row in cert['T_numerators']]
    dk=int(cert['K_denominator']);dt=int(cert['T_denominator']);e=R(cert['central_entry_error_upper'])
    for i in range(N):
        for j in range(N):
            if i<64 and j<64:a=R(3,4)*R(full['1']['U'][i][j]);b=R(3,4)*R(full['1']['eU'][i][j])
            elif i>=64 and j>=64:a=R(3,4)*R(full['2']['U'][i-64][j-64]);b=R(3,4)*R(full['2']['eU'][i-64][j-64])
            else:
                ii,jj=(i,j-64) if i<64 else (j,i-64)
                a=R(full[key]['matrix'][ii][jj]);b=R(full[key]['entry_errors'][ii][jj])
            assert b+abs(a-R(K[i][j],dk))<=e
    Z=[[sum(T[i][k]*K[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
    M=[[sum(Z[i][k]*T[j][k] for k in range(N)) for j in range(N)] for i in range(N)]
    l=[R(sum(abs(z) for z in row),dt) for row in T];ls=sum(l)
    margins=[R(M[i][i]-sum(abs(M[i][j]) for j in range(N) if j!=i),dk*dt*dt)-e*l[i]*ls for i in range(N)]
    assert margins==[R(v) for v in cert['exact_Gershgorin_margins']]
    assert all(v>0 for v in margins)
    return {'form':key,'dimension':N,'input_enclosures_and_exact_congruence_margins_replayed':True,
        'finite_form_norm_at_most_three_quarters':True}

def main():
    # Independent exact checks of the intentionally loose radical constants.
    assert 6<R(5,2)**2 and 108<R(21,2)**2
    assert 1+2*R(5,2)+R(21,2)<17
    assert 2+3*R(5,2)+R(21,2)==20
    assert R(2,17**2*6**4)==R(1,187272)
    assert R(3,20**2*4**4)==R(3,102400)
    # Independent exponential convolution integrals, in the exact time unit.
    assert R(math.factorial(2),2**3)==R(1,4)
    assert R(1,2)-R(1,3)==R(1,6)
    assert R(1,4)-R(1,3)==R(-1,12)
    full=json.loads((OLD/'l2-gram-n64-exact.json').read_text())
    infos=json.loads((OLD/'l2-gram-n64-results.json').read_text())['parents']
    reports=[];checks=[]
    for n in [32,48]:
        ex={}
        for d in [1,2]:
            ex[d],r=check_parent(d,n,full[str(d)],next(p for p in infos if p['d']==d));reports.append(r)
        rr=json.loads((NEW/f'riesz-n{n}-results.json').read_text())
        for key,pairs in [('B1',[('A','Dr'),('H','Dg')]),('B2_transpose',[('Dr','A'),('Dg','H')])]:
            omitted=R(0)
            for a,b in pairs:
                fa=ex[1]['functions'][a];fb=ex[2]['functions'][b]
                da=R(fa['projection_error_dual_norm_upper']);db=R(fb['projection_error_dual_norm_upper'])
                ma=R(fa['projection_norm_upper']);mb=R(fb['projection_norm_upper'])
                omitted+=da*mb+ma*db+da*db
            item=next(c for c in rr['checks'] if c['form']==key)
            assert R(item['whole_space_omitted_form_norm_upper'])==omitted
            norm=R(3,4)+omitted;assert norm==R(item['whole_space_norm_upper'])
            assert item['norm_at_most_four_fifths']==(norm<=R(4,5))
            checks.append({'basis':n,'form':key,'whole_space_norm_bound_replayed':True,
                'at_most_four_fifths':norm<=R(4,5),'strictly_below_one':norm<1})
    blocks=[replay_block(k,full) for k in ['B1','B2_transpose']]
    result={'job_id':'phys-00018-p01-research-d34512ad717d','analytic_constant_and_filter_integral_checks':'pass',
        'parent_residual_checks':reports,'whole_space_norm_checks':checks,'preserved_contraction_certificate_replays':blocks,
        'same_proposer_context':True,'referee_acceptance':False,
        'independence':'Independent standard-library replay; factorial moments from PGF factorial cumulants rather than generator moments. Shared physical parents, preserved exact U/Palm inputs and proposer context. Analytic infinite-state proof still requires fresh referee review.'}
    (NEW/'exact-check-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
