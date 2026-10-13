#!/usr/bin/env python3
"""Fresh referee: exact probabilities of proposal/acceptance histories.

Reads no submitted code, cached answer, matrix, or certificate. Only this file's
independently transcribed graph, energies, and bath parameters are inputs.
Python standard library; Fraction arithmetic throughout all sign decisions.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform
import resource
import time

START = time.perf_counter()
HERE = Path(__file__).resolve().parent
checks = {}

def require(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = True

def rational(v):
    return f"{v.numerator}/{v.denominator}"

def record(v):
    d = 10**12
    n = v.numerator * d // v.denominator
    require(f"enclosure_{len(checks)}", F(n,d) <= v < F(n+1,d))
    return {"exact": rational(v), "floor_at_1e12": n,
            "strict_upper_at_1e12": n+1, "decimal_for_orientation": float(v)}

def events(current, neighbours, weights):
    """Pick one neighbour; draw the heat-bath conditional on this pair.

    Rejections for different proposed neighbours remain distinct events.
    This directly realizes source Eqs.(30)-(33), without matrix multiplication.
    """
    for proposed in neighbours[current]:
        denom = len(neighbours[current]) * (weights[current]+weights[proposed])
        yield proposed, 1, weights[proposed] / denom
        yield current, 0, weights[current] / denom

def histories(vertices, neighbours, energies, qs, initial=None, bath_weights=None):
    weights = [{v:q**(-energies[v]) for v in vertices} for q in qs]
    z0 = sum(weights[0].values(), F(0))
    initial = initial if initial is not None else {v:weights[0][v]/z0 for v in vertices}
    paths = [((v,), (), initial[v]) for v in vertices]
    marginal = [initial]
    counts = [len(paths)]
    for step in range(1,len(qs)):
        wk = weights[step] if bath_weights is None else bath_weights[step-1]
        paths = [(states+(dest,), jumps+(accepted,), mass*chance)
                 for states,jumps,mass in paths
                 for dest,accepted,chance in events(states[-1],neighbours,wk)]
        p = {v:F(0) for v in vertices}
        for states,jumps,mass in paths:
            p[states[-1]] += mass
        require(f"path_normalization_step_{step}_{len(checks)}",sum(p.values())==1)
        require(f"positive_path_mass_step_{step}_{len(checks)}",all(x[2]>0 for x in paths))
        marginal.append(p)
        counts.append(len(paths))
    act = [sum((mass*jumps[k] for states,jumps,mass in paths),F(0))
           for k in range(len(qs)-1)]
    return marginal, act, counts

# Vertex order differs from the submitted class-ordered arrays.
V = tuple([f"C{i}" for i in range(4)]+[f"A{i}" for i in range(3)]+[f"B{i}" for i in range(4)])
E = {v:{"A":0,"B":1,"C":64}[v[0]] for v in V}
edge_set = {frozenset((a,b)) for a in V for b in V
            if (a[0]=="A" and b[0]=="B")
            or (a[0]=="B" and b=="C"+a[1:])
            or (a[0]==b[0]=="C" and a!=b)}
nbr = {v:tuple(w for w in V if frozenset((v,w)) in edge_set) for v in V}
require("11_vertices_22_unique_edges",len(V)==11 and len(edge_set)==22)
require("simple_undirected_degree_4",all(len(nbr[v])==4 and v not in nbr[v]
        and all(v in nbr[w] for w in nbr[v]) for v in V))
reached={V[0]}
for _ in V:
    reached.update(w for v in tuple(reached) for w in nbr[v])
require("connected",reached==set(V))
Q = (F(10001,10000),F(33,32),F(64))
require("strict_positive_finite_cooling",1<Q[0]<Q[1]<Q[2])

# Source reconstruction: heat-bath pair law, equilibrium invariance and Eq.(40)
# on every point-mass distribution. These finite checks supplement the derivation.
for k,q in enumerate(Q):
    w={v:q**(-E[v]) for v in V}; norm=sum(w.values()); gamma={v:w[v]/norm for v in V}
    out={v:F(0) for v in V}
    eq_activity=F(0)
    for v in V:
        ev=list(events(v,nbr,w))
        require(f"bath_{k}_{v}_event_probability",sum(c for _,_,c in ev)==1 and all(c>0 for _,_,c in ev))
        av=sum(c*j for _,j,c in ev)
        edge_sum=sum((w[a]-w[b]) * (F(a==v)-F(b==v))/(w[a]+w[b])
                     for a,b in (tuple(e) for e in edge_set))
        require(f"bath_{k}_{v}_Eq40_basis",av==F(1,2)-edge_sum/8)
        eq_activity+=gamma[v]*av
        for dest,j,c in ev:
            out[dest]+=gamma[v]*c
    require(f"bath_{k}_Gibbs_stationarity",out==gamma)
    for a,b in (tuple(e) for e in edge_set):
        require(f"bath_{k}_detailed_balance_{a}_{b}",
                gamma[a]*w[b]/(4*(w[a]+w[b]))==gamma[b]*w[a]/(4*(w[a]+w[b])))
    e38=F(1,2)-sum((gamma[a]-gamma[b])**2/(gamma[a]+gamma[b])
                   for a,b in (tuple(e) for e in edge_set))/8
    require(f"bath_{k}_Eq38",eq_activity==e38 and eq_activity<=F(1,2))

P,ACT,COUNTS=histories(V,nbr,E,Q)
AVG=sum(ACT)/2
require("claim_A1_gt_63_over_125",ACT[1]>F(63,125))
require("claim_mean_gt_251_over_500",AVG>F(251,500))
require("first_activity_less_half",ACT[0]<F(1,2))
require("population_inversion_B_over_A",P[1]['B0']>P[1]['A0'])
require("all_class_probabilities_equal",all(len({p[v] for v in V if v[0]==c})==1
        for p in P for c in "ABC"))

# Breakdown by actual microstate jump, including transitions within the C class.
types={"AB":F(0),"BC":F(0),"CC":F(0)}
w2={v:Q[2]**(-E[v]) for v in V}
for v in V:
    for dest,j,c in events(v,nbr,w2):
        if j:
            kind=''.join(sorted((v[0],dest[0])))
            types[kind]+=P[1][v]*c
require("microstate_jump_breakdown",sum(types.values())==ACT[1] and types["CC"]==F(3,2)*P[1]['C0'])
signed_sum=sum((w2[a]-w2[b])*(P[1][a]-P[1][b])/(w2[a]+w2[b])
               for a,b in (tuple(e) for e in edge_set))
require("actual_second_step_Eq40",ACT[1]==F(1,2)-signed_sum/8 and signed_sum<0)

# Published independent baseline: four periodic Ising spins, beta J=(log 2)/2.
# e=H/(2J), so the exact Boltzmann weight is 2**(-e), no square roots.
S=tuple(product((-1,1),repeat=4))
H={s:-sum(s[i]*s[(i+1)%4] for i in range(4))//2 for s in S}
snbr={s:tuple(t for t in S if sum(a!=b for a,b in zip(s,t))==1) for s in S}
weights={s:F(2)**(-H[s]) for s in S}; partition=sum(weights.values())
g={s:weights[s]/partition for s in S}
rate=sum(g[s]*sum(j*p for _,j,p in events(s,snbr,weights)) for s in S)
x=F(2); eta=(x-1)/(x+1)
published=x/(1+x*x)*(1-eta**4)/(1+eta**4)
published_Z=x**(-2)*((x+1)**4+(x-1)**4)
require("published_L4_partition",partition==published_Z==F(41,2))
require("published_L4_Glauber_rate",rate==published==F(16,41))

# Referee's independent robustness proof uses differentiation of Gibbs weights:
# ||gamma(e+d)-gamma(e)||_1 <= integral 2*b0*delta dt = 2*b0*delta.
# Together with logistic derivative <=1/4 and stochastic contraction, the two
# activity errors are at most delta*(2*b0+b1/2) and
# delta*(2*b0+b1+b2/2). All b upper bounds below are strict.
d=F(1,1000); b0=F(1,10000); b1=F(1,32); b2=F(21,5)
require("exp_point7_lower_polynomial_gt2",sum(F(7,10)**k/F((1,1,2,6)[k]) for k in range(4))>2)
err0=d*(2*b0+b1/2)
err1=d*(2*b0+b1+b2/2)
erravg=(err0+err1)/2
claimed1=F(1003737,2000000); claimedavg=F(8014821,16000000)
require("robustness_claim_A1",F(63,125)-err1>claimed1>F(1,2))
require("robustness_claim_mean",F(251,500)-erravg>claimedavg>F(1,2))

# Diagnostic mechanism in the stated scale-separated limit, by limiting
# per-proposal accept/reject probabilities (not used as a finite witness).
def limiting_accept(current,proposed,bath):
    a,b=current[0],proposed[0]
    if a==b: return F(1,2)
    if {a,b}=={"A","B"} and bath==1: return F(1,2)
    return F(E[proposed]<E[current])
plim={v:F(1,11) for v in V}; limacts=[]
for bath in (1,2):
    pnext={v:F(0) for v in V}; act=F(0)
    for v in V:
        for u in nbr[v]:
            ac=limiting_accept(v,u,bath)
            pnext[u]+=plim[v]*ac/4
            pnext[v]+=plim[v]*(1-ac)/4
            act+=plim[v]*ac/4
    plim=pnext; limacts.append(act)
require("limit_second_activity_45_88",limacts[1]==F(45,88))
require("limit_mean_89_176",sum(limacts)/2==F(89,176))

output={
 "job_id":"phys-smallmac00006-p01-referee-9ad8026e1081",
 "method":"exhaustive weighted proposal/acceptance histories; exact Fractions; no submitted input files read",
 "python":platform.python_version(),"path_counts":COUNTS,
 "graph":{"vertices":V,"edges":sorted(sorted(e) for e in edge_set),"degree":4},
 "q_protocol":list(map(rational,Q)),"energies":E,
 "probabilities":[{v:rational(p[v]) for v in V} for p in P],
 "A0":record(ACT[0]),"A1":record(ACT[1]),"mean":record(AVG),
 "p1_class_per_vertex":{c:record(P[1][c+'0']) for c in "ABC"},
 "second_step_jump_breakdown":{k:record(v) for k,v in types.items()},
 "Eq40_undirected_signed_sum":rational(signed_sum),
 "baseline":{"partition":rational(partition),"rate":rational(rate)},
 "robustness":{"independent_Gibbs_bound":"2*b0*delta via derivative along energy interpolation",
   "strict_error0_bound":rational(err0),"strict_error1_bound":rational(err1),
   "strict_mean_error_bound":rational(erravg),
   "lower1_from_coarse_baseline":rational(F(63,125)-err1),
   "lower_mean_from_coarse_baseline":rational(F(251,500)-erravg),
   "claimed1":rational(claimed1),"claimed_mean":rational(claimedavg)},
 "limits":list(map(rational,limacts)),"checks":checks,
 "max_output_rational_bits":max(max(x.numerator.bit_length(),x.denominator.bit_length())
    for x in [*ACT,AVG,*[v for p in P for v in p.values()]]),
 "elapsed_seconds":time.perf_counter()-START,
 "maxrss_platform_units":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 "limitations":"No global graph scan or priority certificate. Analytic robustness covers the entire energy box; no corner sampling substitutes for it. No SK-only, hypercube-only, slow-cooling, or final performance-formula claim."
}
(HERE/'referee-replay.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({"status":"pass","checks":len(checks),"path_counts":COUNTS,
 "A0":output['A0'],"A1":output['A1'],"mean":output['mean'],
 "baseline":output['baseline'],"robustness":output['robustness'],
 "elapsed_seconds":output['elapsed_seconds'],"max_output_rational_bits":output['max_output_rational_bits'],
 "maxrss_platform_units":output['maxrss_platform_units'],
 "code_sha256":output['code_sha256']},indent=2))
