#!/usr/bin/env python3
"""Independent exact CZ-state / local-matrix replay; no search-module import.

All inputs are independently transcribed circuit lists. Does not read bitsets,
search signatures or ranks. Graph edges after rotations are recovered from the
state's two-excitation amplitudes. Marginals are computed by direct partial trace.
"""
import hashlib
import json
import resource
import sys
import time
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def state(labels,edges):
    n=len(labels); v=[s.Integer(1)]*(2**n)
    for a,b in edges:
        i=1<<(n-1-labels.index(a)); j=1<<(n-1-labels.index(b))
        for x in range(2**n):
            if x&i and x&j: v[x]=-v[x]
    return v

def recover_edges(v,labels):
    n=len(labels); base=v[0]
    signs=[s.simplify(x/base) for x in v]
    assert all(x in (1,-1) for x in signs)
    assert all(signs[1<<(n-1-i)]==1 for i in range(n))
    edges=[]
    for i,j in combinations(range(n),2):
        x=(1<<(n-1-i))|(1<<(n-1-j))
        if signs[x]==-1: edges.append([labels[i],labels[j]])
    assert state(labels,edges)==signs, 'two-excitation fit must match all amplitudes'
    return edges

def rotate_raw(v,n,position,kind):
    # Omit one sqrt(2), tracked explicitly by the caller.
    gate=([[1,-s.I],[-s.I,1]] if kind=='X' else [[1+s.I,0],[0,1-s.I]])
    b=1<<(n-1-position); out=v[:]
    for x in range(2**n):
        if x&b: continue
        y=x|b
        out[x]=s.expand(gate[0][0]*v[x]+gate[0][1]*v[y])
        out[y]=s.expand(gate[1][0]*v[x]+gate[1][1]*v[y])
    return out

def density(signs,labels,subsystem):
    n=len(labels); inside=[labels.index(a) for a in subsystem]
    outside=[i for i in range(n) if i not in inside]
    blocks={}
    for x,value in enumerate(signs):
        bs=[(x>>(n-1-i))&1 for i in range(n)]
        a=tuple(bs[i] for i in inside); b=tuple(bs[i] for i in outside)
        ia=sum(bit<<(len(a)-1-j) for j,bit in enumerate(a))
        blocks.setdefault(b,[0]*(2**len(inside)))[ia]=value
    rho=s.zeros(2**len(inside))
    for block in blocks.values():
        v=s.Matrix(block); rho+=v*v.conjugate().T/s.Integer(2**n)
    assert rho==rho.conjugate().T and s.trace(rho)==1
    spectrum=rho.eigenvals(); assert all(value>=0 for value in spectrum)
    ent=s.simplify(-sum(mult*value*s.log(value,2) for value,mult in spectrum.items() if value))
    return {'labels':subsystem,'matrix':[[str(v) for v in row] for row in rho.tolist()],
            'rank':rho.rank(),'spectrum':{str(v):m for v,m in spectrum.items()},
            'entropy_bits':str(ent),'trace_one_hermitian_positive':True}

def main():
    t=time.perf_counter(); started=datetime.now(timezone.utc).isoformat()
    data=json.loads((HERE/'independent-circuit-input.json').read_text())
    labels=data['labels']; n=len(labels); initial=state(labels,data['CZ_initial'])
    final=state(labels,data['CZ_final']); v=initial[:]; gate_count=0; steps=[]
    rx=s.Matrix([[1,-s.I],[-s.I,1]])/s.sqrt(2)
    rz=s.diag(1+s.I,1-s.I)/s.sqrt(2)
    assert s.simplify(rx*rx.conjugate().T)==s.eye(2)
    assert s.simplify(rz*rz.conjugate().T)==s.eye(2)
    assert sum(a*a for a in initial)==2**n and sum(a*a for a in final)==2**n
    for spec in data['local_steps']:
        current=recover_edges(v,labels)
        neighbors=sorted(b if a==spec['center'] else a for a,b in current if spec['center'] in (a,b))
        assert neighbors==spec['neighbors']
        for label,kind in [(spec['center'],'X')]+[(a,'Z') for a in spec['neighbors']]:
            v=rotate_raw(v,n,labels.index(label),kind); gate_count+=1
        edges=recover_edges(v,labels)
        phase=s.simplify(v[0]/s.sqrt(2**gate_count))
        assert s.simplify(phase*s.conjugate(phase))==1
        degrees=[sum(int((a in data['C'])!=(b in data['C'])) for a,b in edges if c in (a,b)) for c in data['C']]
        steps.append({'local_operation':spec,'recovered_edges':edges,'cumulative_phase':str(phase),
                      'C_external_degrees':degrees,'all_amplitudes_match_reconstructed_CZ':True})
    residual=[s.expand(a-v[0]*b) for a,b in zip(v,final)]
    assert all(x==0 for x in residual)
    assert s.simplify(v[0]/s.sqrt(2**gate_count))==-1
    qlabels=data['condensed_labels']; q0=state(qlabels,data['condensed_CZ_initial']); q1=state(qlabels,data['condensed_CZ_final'])
    # Separate quotient construction checks the manually supplied condensed circuits.
    quotient_checks=[]
    for key,qkey in [('CZ_initial','condensed_CZ_initial'),('CZ_final','condensed_CZ_final')]:
        observed=set()
        for a,b in data[key]:
            a='c' if a in data['C'] else a; b='c' if b in data['C'] else b
            if a!=b: observed.add(frozenset((a,b)))
        assert observed=={frozenset(e) for e in data[qkey]}
        quotient_checks.append({'input':key,'Boolean_OR_quotient_matches':True})
    original_rhos=[density(x,labels,data['C']) for x in (initial,final)]
    condensed_rhos=[density(x,qlabels,data['witness_subsystem']) for x in (q0,q1)]
    assert [x['rank'] for x in original_rhos]==[8,8]
    assert [x['rank'] for x in condensed_rhos]==[4,2]
    assert [x['entropy_bits'] for x in condensed_rhos]==['2','1']
    report={'status':'pass','job_id':'phys-smallmac00008-p01-research-77290a585cd8',
            'started_at':started,'finished_at':datetime.now(timezone.utc).isoformat(),
            'method':'Independent explicit local 2x2 Clifford rotations of all 64 CZ-state amplitudes; graph recovered from amplitudes; direct partial traces, exact spectra.',
            'independence':'Same worker/context and same claimed example/primary conventions. New manual circuit input and code; no imports/reads of search implementation, rows, signatures or cached ranks. Not a fresh referee.',
            'initial_edges_recovered':recover_edges(initial,labels),'final_edges_recovered':recover_edges(final,labels),
            'steps':steps,'local_gate_count':gate_count,'final_phase':'-1',
            'local_matrices_unitary':True,'CZ_initial_and_final_states_normalized':True,
            'all_64_amplitudes_exact':True,'quotient_checks':quotient_checks,
            'original_C_marginals':original_rhos,'condensed_cut_marginals':condensed_rhos,
            'elapsed_seconds':time.perf_counter()-t,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python':sys.version,'sympy':s.__version__,
            'precision':'Exact Gaussian integers, rational matrices and algebraic phases. No numerical tolerance.',
            'limits':'Largest state 64 amplitudes; largest density matrix 8x8. No general minimality/unlabelled claim.',
            'input_sha256':hashlib.sha256((HERE/'independent-circuit-input.json').read_bytes()).hexdigest()}
    (HERE/'quantum-replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'phase':report['final_phase'],
                      'ranks_original':[x['rank'] for x in original_rhos],
                      'ranks_condensed':[x['rank'] for x in condensed_rhos],
                      'seconds':report['elapsed_seconds'],'peak_rss_bytes':report['peak_rss_bytes']}))

if __name__=='__main__': main()
