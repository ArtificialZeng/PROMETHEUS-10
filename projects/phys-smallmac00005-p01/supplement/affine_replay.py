"""Independent exhaustive audit through affine-support/quadratic-phase states.

Generation does not use submitted symplectic spaces, Clifford orbit, signatures,
or answers. Submitted raw rays are opened only AFTER the independent collection
and its polynomial values have been completed. All arithmetic is Python integer.
The operator coefficients come from this referee's phase-integral reconstruction.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
import json, hashlib, time
from fractions import Fraction

root=Path(__file__).resolve().parents[1]
start=time.monotonic()
data=json.loads((root/'generated/phase-replay-data.json').read_text())
matrices=[]
for degree in ('1','3'):
    mat=[]
    for row in data['H_coefficients'][degree]:
        vals=[240*Fraction(x) for x in row]
        assert all(x.denominator==1 for x in vals)
        mat.append([int(x) for x in vals])
    matrices.append([(r,c,mat[r][c]) for r in range(16) for c in range(16) if mat[r][c]])

def bitcount(x): return bin(x).count('1')

def subspaces(n,k):
    # Unique reduced-row-echelon bases, with coordinate columns ordered 0..n-1.
    for pivots in combinations(range(n),k):
        free=[(r,c) for r,p in enumerate(pivots) for c in range(p+1,n) if c not in pivots]
        for assignment in range(1<<len(free)):
            rows=[1<<p for p in pivots]
            for i,(r,c) in enumerate(free):
                if assignment>>i&1: rows[r]|=1<<c
            yield rows

def state_values(key,norm):
    # key entries: 0 is zero amplitude, 1..4 are i**(entry-1).
    re=[0,1,0,-1,0]; im=[0,0,1,0,-1]
    ans=[]
    for entries in matrices:
        val=sum(a*(re[key[r]]*re[key[c]]+im[key[r]]*im[key[c]]) for r,c,a in entries)
        assert val%norm==0
        ans.append(val//norm)
    return tuple(ans)

states={}; counts={}; subcounts={}; histogram=Counter()
for k in range(5):
    before=len(states); subcount=0
    for rows in subspaces(4,k):
        subcount+=1
        linear=[]
        for y in range(1<<k):
            v=0
            for i,row in enumerate(rows):
                if y>>i&1: v^=row
            linear.append(v)
        assert len(set(linear))==(1<<k)
        cosets=[r for r in range(16) if r==min(r^v for v in linear)]
        pairs=list(combinations(range(k),2))
        for shift in cosets:
            coords=[shift^v for v in linear]
            assert coords[0]==min(coords)
            for ds in product(range(4),repeat=k):
                phase_linear=[sum(ds[i] for i in range(k) if y>>i&1) for y in range(1<<k)]
                for q in range(1<<len(pairs)):
                    key=[0]*16
                    for y,position in enumerate(coords):
                        exponent=phase_linear[y]
                        for j,(a,b) in enumerate(pairs):
                            if q>>j&1 and y>>a&1 and y>>b&1: exponent+=2
                        key[position]=1+exponent%4
                    key=bytes(key)
                    assert key not in states
                    values=state_values(key,1<<k)
                    assert values[0]<=0 and sum(values)<=0
                    states[key]=values; histogram[values]+=1
    counts[k]=len(states)-before; subcounts[k]=subcount
print(json.dumps({'check':'independent_affine_generation','states':len(states),
    'by_support_dimension':counts,'binary_linear_subspaces':subcounts,
    'coefficient_classes':len(histogram),'identically_zero':histogram[(0,0)],
    'positive_ray_count':0,'arithmetic':'Python arbitrary precision integers',
    'status':'pass'}),flush=True)

# Only here are the submitted rays read, for exact comparison with our states.
phase_re=[1,0,-1,0];phase_im=[0,1,0,-1]
submitted={}; mismatch=[]
with (root/'evidence/stabilizer4-rays.jsonl').open() as handle:
    for line in handle:
        ray=json.loads(line)
        terms=[]
        for code,sign in ray['signed_pauli_support']:
            x=z=ny=0
            for bit in range(4):
                p=(code>>(2*bit))&3
                if p&1: x|=1<<bit
                if p&2: z|=1<<bit
                if p==3: ny+=1
            terms.append((x,z,ny%4,sign))
        diagonals=[sum(sign*(-1 if bitcount(z&col)%2 else 1) for x,z,ny,sign in terms if x==0) for col in range(16)]
        base=next(col for col,v in enumerate(diagonals) if v>0)
        denom=diagonals[base]
        assert all(v in (0,denom) for v in diagonals)
        real=[0]*16;imag=[0]*16
        for x,z,ny,sign in terms:
            coefficient=sign*(-1 if bitcount(z&base)%2 else 1)
            real[base^x]+=coefficient*phase_re[ny]
            imag[base^x]+=coefficient*phase_im[ny]
        mapping={(0,0):0,(denom,0):1,(0,denom):2,(-denom,0):3,(0,-denom):4}
        key=bytes(mapping[(a,b)] for a,b in zip(real,imag))
        # Check the complete supplied Pauli expansion, not just the column used
        # to recover its vector. Sixteen distinct signed stabilizers determine
        # the full rank-one projector uniquely.
        signs=dict(ray['signed_pauli_support'])
        assert len(signs)==16 and signs[0]==1
        span={0}
        for generator,eigenvalue in zip(ray['generators'],ray['eigenvalues']):
            assert signs[generator]==eigenvalue
            span |= {v^generator for v in list(span)}
        assert len(span)==16 and span==set(signs)
        for x,z,ny,sign in terms:
            for col,amplitude in enumerate(key):
                target=key[col^x]
                if amplitude==0:
                    assert target==0
                else:
                    phase=amplitude-1+ny+(2 if (sign<0)^(bitcount(z&col)%2==1) else 0)
                    assert target==1+phase%4
        assert key not in submitted
        coeff=ray['g_t_coefficients_over_240']
        assert coeff[0]==0 and coeff[2]==0
        vals=(coeff[1],coeff[3]);submitted[key]=vals
        if states.get(key)!=vals: mismatch.append(ray['id'])
assert not mismatch and submitted==states
cert=json.loads((root/'evidence/stabilizer4-certificate.json').read_text())
expected={(e['alpha'],e['beta']):e['count'] for e in cert['classes']}
assert dict(histogram)==expected
out={'job_id':'phys-smallmac00005-p01-referee-21dd7db15df1','method':'affine support with Z4 linear and even quadratic phase',
 'state_counts':counts,'linear_subspace_counts':subcounts,'total':len(states),
 'classes':[{'alpha':a,'beta':b,'count':c} for (a,b),c in sorted(histogram.items())],
 'raw_ray_set_and_coefficients_equal':True,'mismatches':mismatch,
 'full_pauli_eigenvector_and_generator_checks':True,
 'independence':'No discovery code imported. State generation and values completed before submitted ray file was read; operators are independently reconstructed by referee phase/u integration.',
 'raw_input_sha256':hashlib.sha256((root/'evidence/stabilizer4-rays.jsonl').read_bytes()).hexdigest(),
 'elapsed_seconds':time.monotonic()-start}
(root/'generated/affine-replay-data.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'check':'submitted_raw_ray_comparison','rays':len(submitted),
 'same_states_and_coefficients':True,'same_class_histogram':True,
 'all_587520_signed_pauli_eigenvector_checks':True,
 'mismatches':mismatch,'elapsed_seconds':time.monotonic()-start,'status':'pass'}),flush=True)
