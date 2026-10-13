#!/usr/bin/env python3
"""Independent representation replay using Python standard library only.

Does not import the discovery programs, numpy or scipy, or read their tree caches.
Reads ONLY the proposed monomial/support/weight witnesses from the certificate.
Reconstructs trees via parent maps and polynomials via 3x3 generator cofactors.
This is a same-worker replay, not the required fresh scientific referee.
"""
from itertools import product, permutations, combinations
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import json, time, hashlib

E=[(i,j) for i in range(4) for j in range(4) if i!=j]
ZERO=(0,)*12
checks=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    checks.append(name)

def add(p,q):
    z=Counter(p)
    for m,v in q.items():z[m]+=v
    return {m:v for m,v in z.items() if v}

def mul(p,q):
    z=defaultdict(int)
    for m,v in p.items():
        for n,w in q.items():z[tuple(a+b for a,b in zip(m,n))]+=v*w
    return {m:v for m,v in z.items() if v}

def scale(p,a):return {m:a*v for m,v in p.items() if a*v}
def unit(e,n=12):return tuple(int(j==e) for j in range(n))

def determinant(a):
    n=len(a);out={}
    for p in permutations(range(n)):
        parity=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2
        term={(0,)*12: (-1)**parity}
        for i,j in enumerate(p):term=mul(term,a[i][j])
        out=add(out,term)
    return out

def parent_trees():
    ans=[]
    for root in range(4):
        nodes=[v for v in range(4) if v!=root]; valid=[]
        for dests in product(*[[i for i in range(4) if i!=j] for j in nodes]):
            parent=dict(zip(nodes,dests));good=True
            for start in nodes:
                seen=set();v=start
                while v!=root:
                    if v in seen:good=False;break
                    seen.add(v);v=parent[v]
                if not good:break
            if good:valid.append(tuple(sorted(E.index((parent[j],j)) for j in nodes)))
        ans.append(sorted(valid))
    return ans

def strong(arcs):
    for r in range(4):
        seen={r}
        while True:
            more=seen|{v for u,v in arcs if u in seen}
            if more==seen:break
            seen=more
        if len(seen)!=4:return False
    return True

def substitute(poly,rate_polys):
    result={}
    for mon,c in poly.items():
        term={(0,)*9:c}
        for e,power in enumerate(mon):
            for _ in range(power):term=mul(term,rate_polys[e])
        result=add(result,term)
    return result

def evaluate(poly,x):
    out=F(0)
    for m,c in poly.items():
        v=F(c)
        for a,p in zip(x,m):v*=a**p
        out+=v
    return out

def solve(mat,b):
    a=[list(map(F,row))+[F(v)] for row,v in zip(mat,b)];n=len(a)
    for j in range(n):
        p=next(i for i in range(j,n) if a[i][j]);a[j],a[p]=a[p],a[j]
        v=a[j][j];a[j]=[x/v for x in a[j]]
        for i in range(n):
            if i!=j:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    return [a[i][-1] for i in range(n)]

def main():
    start=time.monotonic();cert=json.loads((Path(__file__).resolve().parent / 'certificate.json').read_text())
    trees=parent_trees();check('parent-map tree counts 16 per root',list(map(len,trees))==[16]*4)
    families=list(product(range(16),repeat=4));counts=Counter();multiplicities=[]
    for f in families:
        m=tuple(sum(e in trees[r][f[r]] for r in range(4)) for e in range(12))
        counts[m]+=1;multiplicities.append(m)
    unique={i for i,m in enumerate(multiplicities) if counts[m]==1}
    check('65536 families, 5955 directed classes, 346 singleton families',len(families)==65536 and len(counts)==5955 and len(unique)==346)
    # Independent graph cone coverage: exactly the 24 relabelings of one strong tournament.
    pairs=list(combinations(range(4),2))
    canonical={(0,1),(1,2),(2,0),(0,3),(3,1),(2,3)}
    tournaments={frozenset((j,i) if b else (i,j) for (i,j),b in zip(pairs,bits)) for bits in product([0,1],repeat=6)}
    strong_t={t for t in tournaments if strong(t)}
    orbit={frozenset((p[i],p[j]) for i,j in canonical) for p in permutations(range(4))}
    check('all 24 strong tournaments are canonical relabelings',len(strong_t)==24 and strong_t==orbit)
    # Laplacian L=-W, columns are source states. Use q as twelve independent symbols.
    lap=[[{} for j in range(4)] for i in range(4)]
    for e,(i,j) in enumerate(E):
        atom={unit(e):1};lap[i][j]=scale(atom,-1);lap[j][j]=add(lap[j][j],atom)
    tau=[]
    for r in range(4):
        keep=[i for i in range(4) if i!=r]
        p=determinant([[lap[i][j] for j in keep] for i in keep]);tau.append(p)
        tree_polys={tuple(int(e in t) for e in range(12)):1 for t in trees[r]}
        check('independent cofactor equals parent tree polynomial at root '+str(r),p==tree_polys)
    # Explicit rate map, separately transcribed in the fixed E order.
    # Symmetric variable order 01,02,03,12,13,23; then A,B,C.
    assignments=[[0],[1,6,8],[2],[0,6],[3],[4,7,8],
                 [1],[3,6,7,8],[5],[2,8],[4],[5,7]]
    rate_polys=[{unit(i,9):1 for i in inds} for inds in assignments]
    for j in range(4):
        outgoing={};incoming={}
        for e,(i,k) in enumerate(E):
            if k==j:outgoing=add(outgoing,rate_polys[e])
            if i==j:incoming=add(incoming,rate_polys[e])
        check('Eulerian polynomial conservation at state '+str(j),outgoing==incoming)
    expanded_tau=[substitute(p,rate_polys) for p in tau]
    check('common tau for every root from determinants',all(p==expanded_tau[0] for p in expanded_tau))
    common=expanded_tau[0]
    check('93 nonnegative cubic monomials',len(common)==93 and all(c>0 and sum(m)==3 for m,c in common.items()))
    # Derivatives are taken with respect to independent directed q BEFORE substitution.
    numerators=[[substitute({m:c*m[e] for m,c in p.items() if m[e]},rate_polys) for e in range(12)] for p in tau]
    records={tuple(r['monomial']):r for r in cert['records']}
    check('certificate covers exactly all determinant monomials',set(records)==set(common))
    for mon,coefficient in sorted(common.items()):
        row=records[mon];support=row['unique_family_ids'];weights=list(map(F,row['weights']))
        check('support and probability '+str(mon),len(support)==len(weights) and set(support)<=unique and min(weights)>=0 and sum(weights)==1)
        for r in range(4):
            for e in range(12):
                mixed=sum(w*int(e in trees[r][families[fid][r]]) for fid,w in zip(support,weights))
                check('coefficient identity '+str((mon,r,e)),coefficient*mixed==numerators[r][e].get(mon,0))
        # These redundant discovery values are compared only after independent reconstruction.
        check('discovery coefficient agrees '+str(mon),coefficient==row['coefficient'])
    raw_cases=[[2,3,5,7,11,13,17,19,23,29,31,37],
               [1]*12,[1,1,10000,10000,1,1,1,10000,1,1,1,10000],
               [1,7,11,1000000,13,17,19,23,29,31,37,41],
               [5,3,9,8,2,6,10,1,4,7,12,11],
               [3,11,2,7,13,5,17,19,23,29,31,37],
               # Triangle residual plus isolated state; nonuniform stationary distribution.
               [4,24,25,7,21,55,3,24,65,5,22,39],
               # Pure directed four-cycle residual with all symmetric traffic strictly positive.
               [2,8,5,2,7,16,3,12,13,10,11,13],
               # Reversible but nonuniform steady state: zero residual-current cone vertex.
               [4,9,25,2,21,55,3,14,65,5,22,39]]
    test_records=[]
    for testno,raw in enumerate(raw_cases):
        k=[F(v,sum(raw)) for v in raw]
        ts=[evaluate(p,k) for p in tau];pi=[v/sum(ts) for v in ts]
        q=[v*pi[j] for v,(i,j) in zip(k,E)]
        # Find a canonical tournament containing all strictly positive residual currents.
        perm=next(p for p in permutations(range(4)) if all(q[E.index((p[i],p[j]))]<=q[E.index((p[j],p[i]))] for i,j in canonical))
        qnew=[q[E.index((perm[i],perm[j]))] for i,j in E]
        xs=[min(qnew[E.index((i,j))],qnew[E.index((j,i))]) for i,j in pairs]
        xs += [qnew[E.index((1,0))]-qnew[E.index((0,1))],
               qnew[E.index((3,2))]-qnew[E.index((2,3))],
               qnew[E.index((3,0))]-qnew[E.index((0,3))]]
        check('nonnegative cone coordinates '+str(testno),min(xs[:6])>0 and min(xs[6:])>=0)
        check('exact cone reconstruction '+str(testno),[evaluate(p,xs) for p in rate_polys]==qnew)
        z=evaluate(common,xs);theta=defaultdict(F)
        for mon,ct in common.items():
            rho=F(ct,z)
            for v,power in zip(xs,mon):rho*=v**power
            for fid,beta in zip(records[mon]['unique_family_ids'],records[mon]['weights']):theta[fid]+=rho*F(beta)
        check('exact convex weights '+str(testno),min(theta.values())>=0 and sum(theta.values())==1)
        h=[[F(0) for e in E] for r in range(4)]
        for fid,wt in theta.items():
            for r in range(4):
                for e in trees[r][families[fid][r]]:
                    i,j=E[e];h[perm[r]][E.index((perm[i],perm[j]))]+=wt
        for r in range(4):
            for e in range(12):
                direct=evaluate({m:c*m[e] for m,c in tau[r].items() if m[e]},k)/ts[r]
                check('all-d coefficient check '+str((testno,r,e)),h[r][e]==direct)
        d=[F(((7*e+testno*3)%11)-5,5) for e in range(12)]
        w=[[F(0) for j in range(4)] for i in range(4)];wp=[[F(0) for j in range(4)] for i in range(4)]
        for (i,j),v,t in zip(E,k,d):w[i][j]=v;w[j][j]-=v;wp[i][j]=v*t;wp[j][j]-=v*t
        norm=[row[:] for row in w];norm[3]=[F(1)]*4
        linear_pi=solve(norm,[0,0,0,1]);check('linear steady state '+str(testno),linear_pi==pi)
        rhs=[-sum(wp[i][j]*pi[j] for j in range(4)) for i in range(4)];rhs[3]=F(0)
        dpi=solve(norm,rhs);response=[v/p for v,p in zip(dpi,pi)]
        g=[sum(h[r][e]*d[e] for e in range(12)) for r in range(4)];mean=sum(p*v for p,v in zip(pi,g))
        check('exact arbitrary-sign physical response '+str(testno),response==[v-mean for v in g])
        test_records.append({'raw_rates':raw,'normalized_pi':list(map(str,pi)),'canonical_to_actual_permutation':perm,
                             'cone_variables':list(map(str,xs)),'d':list(map(str,d)),'r':list(map(str,response)),
                             'nonzero_theta':{str(fid):str(v) for fid,v in theta.items() if v}})
    result={'status':'pass','method':'standard-library parent-map enumeration; cofactor determinant and independent-rate derivatives before Eulerian substitution; exact Fraction witness replay; tournament enumeration; exact linear systems',
            'independence':'same research worker, separately written implementation; no numpy/scipy/discovery imports or tree cache read. Certificate weights are the proposed witness, not independently discovered. Fresh referee still required.',
            'checks_passed':len(checks),'monomials_checked':93,'unique_families_reconstructed':346,'strong_tournaments':24,
            'exact_rate_tests':test_records,'seconds':time.monotonic()-start,
            'certificate_sha256':hashlib.sha256((Path(__file__).resolve().parent / 'certificate.json').read_bytes()).hexdigest(),
            'limitations':'Finite certificate verifies the algebra. Analytic Eulerian reduction and residual-support argument must be reviewed in proof.md; novelty not established by this program.'}
    Path('cofactor-results.json').write_text(json.dumps(result,indent=2)+'\n')
    Path('cofactor-checks.log').write_text('\n'.join('PASS '+s for s in checks)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='exact_rate_tests'},indent=2))

if __name__=='__main__':main()
