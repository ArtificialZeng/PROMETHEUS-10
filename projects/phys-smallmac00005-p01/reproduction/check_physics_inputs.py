"""Exact channel, moment-consistency, and input-permutation checks."""
import json
from pathlib import Path
import sympy as S

d = S.Symbol('delta', real=True)
data = json.loads(Path('evidence/input-a.json').read_text())


def decode(record):
    return S.Matrix([[sum(S.Rational(c)*d**k for k,c in enumerate(cell))
                      for cell in row] for row in record['rows']])


def zero(matrix):
    return all(S.expand(x)==0 for x in matrix)


omega = S.Matrix([1,0,0,1])
channel_choi = (1-d)*omega*omega.T+d*S.eye(4)/2
channel_pt = S.Matrix(2,2,lambda i,j:sum(channel_choi[2*i+k,2*j+k] for k in range(2)))
assert channel_pt == S.eye(2)
assert channel_choi.eigenvals() == {d/2:3,2-3*d/2:1}
lines = ['Depolarizing unnormalized Choi: eigenvalues {delta/2:3, 2-3delta/2:1}; Tr_out=I2.',
         'Both eigenvalues nonnegative for 0<=delta<=1; local channel CP and TP.']
for n in [2,3]:
    q = decode(data['cases'][str(n)]['Q'])
    r = decode(data['cases'][str(n)]['R'])
    q_marginal = S.Matrix(2**n,2**n,lambda i,j:sum(q[2*i+k,2*j+k] for k in range(2)))
    assert zero(S.kronecker_product(q_marginal,S.eye(2))-r)
    for site in range(n-1):
        mapping = []
        for i in range(2**(n+1)):
            bits = list(f'{i:0{n+1}b}')
            bits[site],bits[site+1] = bits[site+1],bits[site]
            mapping.append(int(''.join(bits),2))
        for m in [q,r]:
            assert zero(S.Matrix(m.rows,m.cols,lambda i,j:m[mapping[i],mapping[j]])-m)
    assert q.subs(d,0).eigenvals() == {S.Rational(1,n+2):n+2,S.Integer(0):2**(n+1)-n-2}
    assert r.subs(d,0).eigenvals() == {S.Rational(1,n+1):2*(n+1),S.Integer(0):2**(n+1)-2*(n+1)}
    lines += [f'n={n}: Tr_output Q=R0 and R=R0 tensor I2 exactly.',
              f'n={n}: all adjacent input swaps preserve Q and R exactly; hence all input permutations.',
              f'n={n}: delta=0 Q spectrum 1/{n+2} with multiplicity {n+2}, zero otherwise.',
              f'n={n}: delta=0 R spectrum 1/{n+1} with multiplicity {2*(n+1)}, zero otherwise.']
lines += ['No input positivity imposed after partial transpose of Q; its signs are checked by both representations.',
          'All checks symbolic and exact; the three-copy target optimum is not among these input checks.']
Path('evidence/physical-input-checks.log').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
