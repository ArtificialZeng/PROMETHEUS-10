#!/usr/bin/env python3
"""Exact graph certificate replay using edge sets and exhaustive binary spans.
Also reconstructs the two published Fig.15 examples from manual figure inputs.
No search-module import; not an independent referee.
"""
import hashlib
import json
import resource
import time
from collections import deque
from datetime import datetime, timezone
from itertools import combinations, permutations
from pathlib import Path

HERE=Path(__file__).resolve().parent

def canon(edges): return frozenset(frozenset(e) for e in edges)
def neighbors(e,v): return set().union(*(edge-{v} for edge in e if v in edge)) if any(v in edge for edge in e) else set()
def lc(e,v): return e ^ frozenset(frozenset(p) for p in combinations(sorted(neighbors(e,v),key=str),2))
def edge_list(e,labels):
    return [[a,b] for a,b in combinations(labels,2) if frozenset((a,b)) in e]
def components(e,labels):
    unseen=set(labels); ans=[]
    while unseen:
        start=min(unseen,key=str); found={start}; todo=[start]; unseen.remove(start)
        while todo:
            v=todo.pop(); new=neighbors(e,v)&unseen
            unseen-=new; found|=new; todo.extend(new)
        ans.append(sorted(found,key=str))
    return ans
def cut_matrix(e,inside,outside): return [[int(frozenset((a,b)) in e) for b in outside] for a in inside]
def span_rank(matrix):
    ncols=len(matrix[0]) if matrix else 0; span={tuple([0]*ncols)}
    for row in matrix: span |= {tuple(x^y for x,y in zip(v,row)) for v in list(span)}
    size=len(span); rank=size.bit_length()-1
    assert 2**rank==size
    return rank
def quotient(e,C): return frozenset(frozenset('c' if x in C else x for x in edge) for edge in e if not edge<=set(C))
def describe(e,labels,C):
    outside=[a for a in labels if a not in C]; matrix=cut_matrix(e,C,outside)
    return {'edges':edge_list(e,labels),'components':components(e,labels),
            'C_induced_components':components(frozenset(edge for edge in e if edge<=set(C)),C),
            'external_degrees':[sum(row) for row in matrix],
            'C_cut_matrix':matrix,'C_cut_rank':span_rank(matrix)}
def orbit(e,labels,cap=64):
    paths={e:[]}; queue=deque([e]); transitions=0
    while queue:
        g=queue.popleft()
        for v in labels:
            h=lc(g,v); transitions+=1
            if h not in paths:
                assert len(paths)<cap, 'orbit cap hit: completeness unknown'
                paths[h]=paths[g]+[v]; queue.append(h)
    return paths,transitions
def main():
    t=time.perf_counter(); started=datetime.now(timezone.utc).isoformat()
    d=json.loads((HERE/'witness-input.json').read_text()); labels=list(range(1,d['n']+1)); C=d['C']
    g=canon(d['G_edges']); h=canon(d['Gprime_edges']); cur=g; steps=[]
    for v in d['LC_word']:
        cur=lc(cur,v); steps.append(describe(cur,labels,C))
    assert cur==h
    endpoints=[describe(e,labels,C) for e in (g,h)]
    assert all(len(x['components'])==1 and max(x['external_degrees'])<=1 and x['C_cut_rank']==3 for x in endpoints)
    qlabels=d['condensed_labels']; q0=quotient(g,C); q1=quotient(h,C)
    outside=[a for a in qlabels if a not in d['witness_cut']]
    matrices=[cut_matrix(q,d['witness_cut'],outside) for q in (q0,q1)]
    ranks=[span_rank(a) for a in matrices]; assert ranks==[2,1]
    paths,transitions=orbit(q0,qlabels)
    assert q1 not in paths
    permutation_witness=None
    for perm in permutations(qlabels):
        mapping=dict(zip(qlabels,perm)); target=frozenset(frozenset(mapping[a] for a in edge) for edge in q1)
        if target in paths:
            permutation_witness={'mapping_of_Gprime_condensed':list(zip(qlabels,perm)),
                                 'LC_word_from_G_condensed':paths[target]}; break
    assert permutation_witness is not None
    old=json.loads((HERE/'old-figure-input.json').read_text()); old_results={}
    for key in ('a','b'):
        x=old[key]; old_labels=list(range(1,x['n']+1)); before=canon(x['edges_before']); after=canon(x['edges_after']); cur=before
        for v in x['LC_word']: cur=lc(cur,v)
        assert cur==after
        ends=[describe(e,old_labels,x['C']) for e in (before,after)]
        assert any(max(item['external_degrees'])>1 for item in ends)
        old_results[key]={'LC_word_verified':True,'endpoints':ends,'target_double_endpoint_condition':False}
    # Foliage relation: compare each pair within C using leaf/axil or twins.
    rel=[]
    for a,b in combinations(C,2):
        na=neighbors(g,a); nb=neighbors(g,b)
        is_pair=(na=={b} or nb=={a} or (na-{b}==nb-{a} and bool(na-{b})))
        rel.append({'pair':[a,b],'foliage_equivalent':is_pair})
    assert not any(x['foliage_equivalent'] for x in rel)
    result={'status':'pass','job_id':'phys-smallmac00008-p01-research-77290a585cd8',
            'started_at':started,'finished_at':datetime.now(timezone.utc).isoformat(),
            'method':'Set-theoretic edge toggling, OR endpoint quotient, exhaustive binary row spans and queue-exhausted 4-vertex LC orbit.',
            'independence':'Different implementation from discovery, same worker/context and witness. No external/referee acceptance.',
            'endpoints':endpoints,'steps':steps,'condensed_labels':qlabels,
            'condensed_edges':[edge_list(q,qlabels) for q in (q0,q1)],
            'witness_cut':d['witness_cut'],'complementary_cut':outside,
            'cut_matrices':matrices,'cut_ranks':ranks,
            'condensed_LC_orbit':{'size':len(paths),'cap':64,'transitions_checked':transitions,
                                 'queue_exhausted':True,'target_absent':True,
                                 'graphs':[{'edges':edge_list(e,qlabels),'word':word} for e,word in paths.items()]},
            'unlabelled_scope_warning':permutation_witness,
            'old_Fig15_checks':old_results,'C_foliage_pair_checks':rel,
            'elapsed_seconds':time.perf_counter()-t,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'arithmetic':'Exact finite set operations; span cardinalities powers of two. No floating tolerance or truncated negative-orbit inference.'}
    (HERE/'graph-replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','cut_ranks':ranks,'orbit_size':len(paths),
                      'old_external_degrees':{k:[x['external_degrees'] for x in z['endpoints']] for k,z in old_results.items()},
                      'label_permutation_limitation':permutation_witness,'seconds':result['elapsed_seconds']}))

if __name__=='__main__': main()
