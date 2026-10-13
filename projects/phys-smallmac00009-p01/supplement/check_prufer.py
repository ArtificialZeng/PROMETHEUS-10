#!/usr/bin/env python3
"""Fresh exact referee replay. Only submitted witness supports/weights are input.

No discovery/reproduction implementation, cached enumeration, owner log or prior
verdict is imported. Trees use Prufer codes; cone polynomials use multisets of
cycle/symmetric-flow labels; Markov response uses separate rational row solves.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random
import time

BASE = Path(__file__).resolve().parent
CERT_PATH = BASE / 'certificate.json'
START = time.perf_counter()
OUT = tuple(permutations(range(4), 2))  # (source, destination)
PAIRS = tuple(combinations(range(4), 2))
IN_ORDER = tuple((dest, src) for dest in range(4) for src in range(4) if src != dest)
EDGE_ID = {(src, dest): i for i, (dest, src) in enumerate(IN_ORDER)}
CYCLES = ((0, 1, 2, 0), (1, 2, 3, 1), (0, 3, 1, 2, 0))
CANON = frozenset(e for cycle in CYCLES for e in zip(cycle, cycle[1:]))
COUNTS = Counter()


def check(condition, name):
    if not condition:
        raise AssertionError(name)
    COUNTS[name.split(':', 1)[0]] += 1


def prufer_trees(n):
    """All labeled undirected trees, then orient by BFS from each root."""
    rooted = [set() for _ in range(n)]
    for code in product(range(n), repeat=max(0, n - 2)):
        deg = [1 + code.count(i) for i in range(n)]
        edges = []
        for v in code:
            leaf = next(i for i in range(n) if deg[i] == 1)
            edges.append((leaf, v))
            deg[leaf] -= 1
            deg[v] -= 1
        leaves = [i for i in range(n) if deg[i] == 1]
        edges.append(tuple(leaves))
        adj = defaultdict(list)
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        for root in range(n):
            seen, queue, tree = {root}, [root], []
            for parent in queue:
                for child in adj[parent]:
                    if child not in seen:
                        seen.add(child)
                        queue.append(child)
                        tree.append((child, parent))
            rooted[root].add(frozenset(tree))
    return rooted


TREES = [sorted(ts, key=lambda t: tuple(sorted(EDGE_ID[e] for e in t)))
         for ts in prufer_trees(4)]
check([len(ts) for ts in TREES] == [16] * 4, 'K4 tree count')


def family_classes(trees, out):
    classes = defaultdict(list)
    radix = len(trees[0])
    for indices in product(range(radix), repeat=len(trees)):
        mult = Counter(e for r, t in enumerate(indices) for e in trees[r][t])
        family_id = 0
        for t in indices:
            family_id = radix * family_id + t
        classes[tuple(mult[e] for e in out)].append(family_id)
    return classes


CLASSES = family_classes(TREES, OUT)
UNIQUE = {v[0] for v in CLASSES.values() if len(v) == 1}
check(sum(map(len, CLASSES.values())) == 65536, 'family total')
check(len(CLASSES) == 5955, 'multiplicity class total')
check(len(UNIQUE) == 346, 'unique family total')
tri = [sorted(t, key=lambda x: sorted(x)) for t in prufer_trees(3)]
tricl = family_classes(tri, tuple(permutations(range(3), 2)))
check(sum(map(len, tricl.values())) == 27, 'published triangle total')
check(sum(len(v) == 1 for v in tricl.values()) == 11, 'published triangle unique')


def decode(fid):
    check(isinstance(fid, int) and 0 <= fid < 65536, 'witness ID valid')
    inds = []
    for place in (4096, 256, 16, 1):
        t, fid = divmod(fid, place)
        inds.append(t)
    return [TREES[r][t] for r, t in enumerate(inds)]


def reach(support):
    closure = {(v, v) for v in range(4)} | set(support)
    for k in range(4):
        for i in range(4):
            for j in range(4):
                if (i, k) in closure and (k, j) in closure:
                    closure.add((i, j))
    return closure


PERMS = list(permutations(range(4)))
CANON_COPIES = [frozenset((p[u], p[v]) for u, v in CANON) for p in PERMS]
strong = []
for bits in product((0, 1), repeat=6):
    edges = frozenset((v, u) if b else (u, v) for (u, v), b in zip(PAIRS, bits))
    if len(reach(edges)) == 16:
        strong.append(edges)
check(len(strong) == 24, 'strong tournament count')
check(set(strong) == set(CANON_COPIES), 'complete tournament orbit')
admissible_supports = []
for states in product((0, 1, 2), repeat=6):
    support = frozenset((u, v) if a == 1 else (v, u)
                        for (u, v), a in zip(PAIRS, states) if a)
    closure = reach(support)
    # A strictly positive circulation on every support edge exists exactly when
    # each edge belongs to a directed cycle; sum the cycles for sufficiency.
    if all((v, u) in closure for u, v in support):
        admissible_supports.append(support)
        check(any(support <= full for full in CANON_COPIES), 'residual support embeds')

# Derive the nine independent cone generators from symmetric pair flows and
# three explicit directed cycles, without reading the submitted rate table.
LABELS = {e: [] for e in OUT}
for i, (u, v) in enumerate(PAIRS):
    LABELS[u, v].append(i)
    LABELS[v, u].append(i)
for i, cycle in enumerate(CYCLES, 6):
    for e in zip(cycle, cycle[1:]):
        LABELS[e].append(i)
for label in range(9):
    check(all(sum(label in LABELS[u, v] for v in range(4) if v != u) ==
              sum(label in LABELS[v, u] for v in range(4) if v != u)
              for u in range(4)), 'generator conserves flow')

# Polynomial keys are sorted triples of labels, not cached exponent vectors.
TAU = [Counter() for _ in range(4)]
NUM = {(r, e): Counter() for r in range(4) for e in OUT}
for r in range(4):
    for tree in TREES[r]:
        expansion = Counter(tuple(sorted(m)) for m in product(*(LABELS[e] for e in tree)))
        TAU[r].update(expansion)
        # Marks each original directed edge before Eulerian substitution.
        for edge in tree:
            NUM[r, edge].update(expansion)
for r in range(1, 4):
    check(TAU[r] == TAU[0], 'root polynomial equality')
check(len(TAU[0]) == 93, 'complete degree three support')
check(all(len(m) == 3 for m in TAU[0]), 'exact polynomial degree')
check(Counter(TAU[0].values()) == Counter({1: 82, 2: 10, 3: 1}), 'coefficient histogram')

CERT = json.loads(CERT_PATH.read_text())
check(CERT['variables'] == ['s01', 's02', 's03', 's12', 's13', 's23', 'A', 'B', 'C'], 'witness variable convention')
check(CERT['edge_order_destination_source'] == [list(e) for e in IN_ORDER], 'witness edge convention')
WITNESSES = {}
USED = set()
ABC = None
for row in CERT['records']:
    exponent = row['monomial']
    check(len(exponent) == 9 and all(type(v) is int and v >= 0 for v in exponent)
          and sum(exponent) == 3, 'witness exponent valid')
    monomial = tuple(i for i, power in enumerate(exponent) for _ in range(power))
    check(monomial not in WITNESSES and monomial in TAU[0], 'witness monomial coverage')
    families, weights = row['unique_family_ids'], [F(s) for s in row['weights']]
    check(len(weights) == len(families) and len(set(families)) == len(families), 'witness support shape')
    check(all(w >= 0 for w in weights) and sum(weights) == 1, 'witness convexity')
    check(all(fid in UNIQUE for fid in families), 'witness true uniqueness')
    trees = [decode(fid) for fid in families]
    c = TAU[0][monomial]
    check(c == row['coefficient'], 'submitted scalar crosscheck')
    for r in range(4):
        for edge in OUT:
            lhs = NUM[r, edge][monomial]
            rhs = c * sum(w for ts, w in zip(trees, weights) if edge in ts[r])
            check(lhs == rhs, 'exact coefficient identity')
            check(lhs == row['numerator_matrix'][r][EDGE_ID[edge]], 'submitted numerator crosscheck')
    WITNESSES[monomial] = list(zip(families, weights))
    USED.update(families)
    if monomial == (6, 7, 8):
        ABC = {'coefficient': c, 'family_ids': families, 'weights': [str(w) for w in weights]}
check(set(WITNESSES) == set(TAU[0]), 'no omitted monomial')
check(len(USED) == 78, 'canonical witness support total')


def solve(matrix, rhs):
    """Independent exact Gaussian elimination, never scipy or cached inverse."""
    n = len(rhs)
    a = [[F(v) for v in row] + [F(b)] for row, b in zip(matrix, rhs)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if a[r][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for r in range(n):
            if r != col:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[col])]
    return [a[r][-1] for r in range(n)]


def generator(k):
    q = [[F(0) for _ in range(4)] for _ in range(4)]
    for (u, v), rate in k.items():
        q[u][v] += rate
        q[u][u] -= rate
    return q


def stationary(q):
    matrix = [[q[j][i] for j in range(4)] for i in range(3)] + [[F(1)] * 4]
    pi = solve(matrix, [0, 0, 0, 1])
    check(all(x > 0 for x in pi) and sum(pi) == 1, 'positive normalized stationary')
    check(all(sum(pi[u] * q[u][v] for u in range(4)) == 0 for v in range(4)), 'stationary row equation')
    return pi, matrix


def marginals(k):
    h = {}
    taus = []
    for r in range(4):
        weights = [product_fraction(k[e] for e in t) for t in TREES[r]]
        tau = sum(weights)
        taus.append(tau)
        for edge in OUT:
            h[r, edge] = sum(w for t, w in zip(TREES[r], weights) if edge in t) / tau
    return h, taus


def product_fraction(values):
    out = F(1)
    for value in values:
        out *= value
    return out


def cone_coordinates(flow):
    for p, copy in zip(PERMS, CANON_COPIES):
        residual = {e for e in OUT if flow[e] > flow[e[::-1]]}
        if residual <= copy:
            local = {(u, v): flow[p[u], p[v]] for u, v in OUT}
            sym = [min(local[u, v], local[v, u]) for u, v in PAIRS]
            x = sym + [local[0, 1] - sym[0], local[2, 3] - sym[5], local[0, 3] - sym[2]]
            check(all(z > 0 for z in sym) and all(z >= 0 for z in x[6:]), 'cone coordinate nonnegativity')
            check(all(local[e] == sum(x[i] for i in LABELS[e]) for e in OUT), 'full exact cone reconstruction')
            return p, x
    raise AssertionError('No canonical cone covers legal stationary flow')


def audit_rate_instance(name, raw):
    total = sum(raw.values())
    k = {e: F(v) / total for e, v in raw.items()}
    check(all(v > 0 for v in k.values()) and sum(k.values()) == 1, 'legal normalized rates')
    qrow = generator(k)
    pi, matrix = stationary(qrow)
    h, taus = marginals(k)
    check(pi == [t / sum(taus) for t in taus], 'tree versus linear stationary')
    flow = {(u, v): k[u, v] * pi[u] for u, v in OUT}
    hf, tf = marginals(flow)
    check(h == hf and len(set(tf)) == 1, 'fixed basepoint flow invariance')
    p, x = cone_coordinates(flow)
    monweights = {m: c * product_fraction(x[i] for i in m) for m, c in TAU[0].items()}
    norm = sum(monweights.values())
    check(norm > 0 and norm == tf[0], 'positive common denominator')
    theta = defaultdict(F)
    for m, support in WITNESSES.items():
        for fid, weight in support:
            theta[fid] += monweights[m] / norm * weight
    check(all(w >= 0 for w in theta.values()) and sum(theta.values()) == 1, 'constructed theta convexity')
    reconstructed = defaultdict(F)
    for fid, weight in theta.items():
        for root, tree in enumerate(decode(fid)):
            for u, v in tree:
                reconstructed[p[root], (p[u], p[v])] += weight
    check(all(reconstructed[key] == h[key] for key in h), 'all marginals after inverse permutation')
    # All twelve independent perturbation directions; this spans any real d.
    for edge in OUT:
        u, v = edge
        forcing = [F(0)] * 4
        forcing[u] += k[edge] * pi[u]
        forcing[v] -= k[edge] * pi[u]
        dp = solve(matrix, forcing[:3] + [F(0)])
        check(sum(dp) == 0, 'linear response normalization')
        for r in range(4):
            val = h[r, edge] - sum(pi[j] * h[j, edge] for j in range(4))
            check(dp[r] / pi[r] == val, 'independent generator derivative')
    check(all(sum(h[r, e] for e in OUT) == 3 for r in range(4)), 'uniform time scaling null response')
    return {'name': name, 'rate_ratio': str(max(k.values()) / min(k.values())),
            'pi': list(map(str, pi)), 'permutation': p,
            'cycle_coordinates': list(map(str, x[6:])),
            'nonzero_theta': sum(w > 0 for w in theta.values())}


cases = [('equal_rates', {e: F(1) for e in OUT})]
# Every boundary stratum A,B,C=0/nonzero, all 24 state permutations and highly
# nonuniform holding times test cone transport and fixed-pi centering.
for flags in product((0, 1), repeat=3):
    x = list(map(F, (2, 3, 5, 7, 11, 13))) + [F(a * b) for a, b in zip(flags, (17, 19, 23))]
    local = {e: sum(x[i] for i in LABELS[e]) for e in OUT}
    for perm_id, p in enumerate(PERMS):
        hold = (F(1, 31), F(3, 31), F(8, 31), F(19, 31))
        raw = {(p[u], p[v]): local[u, v] / hold[p[u]] for u, v in OUT}
        cases.append((f'cone_flags_{flags}_permutation_{perm_id}', raw))
rng = random.Random(731904260913)
for i in range(16):
    cases.append((f'fresh_rational_{i}', {e: F(rng.randint(1, 37), rng.randint(1, 41)) * F(10) ** rng.randint(-4, 4) for e in OUT}))
cases.append(('extreme_36_orders', {e: F(10) ** ([-18, 18, -9, 7, -13, 11, 5, -6, 15, -16, 3, 1][i]) for i, e in enumerate(OUT)}))
RESULTS = [audit_rate_instance(name, rates) for name, rates in cases]

# Published one-site Hill special case, exact direct derivative at x=1.
x = F(1)
prob = x / (1 + x)
response = x / (1 + x) ** 2
hill = response / (prob * (1 - prob))
check((prob, response, hill) == (F(1, 2), F(1, 4), F(1)), 'published single binding benchmark')

result = {
    'implementation_origin': 'separately implemented Prufer checker; publication replay',
    'completed_at': datetime.now(timezone.utc).isoformat(),
    'method': 'Prufer tree enumeration; full directed multiplicity classes; cycle-label polynomial expansion; Fraction certificate; independent row-generator linear solves',
    'read_submitted_scientific_data': ['certificate.json'],
    'certificate_sha256': sha256(CERT_PATH.read_bytes()).hexdigest(),
    'implementation_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    'status': 'pass',
    'trees_per_root': list(map(len, TREES)), 'families': 65536,
    'multiplicity_classes': len(CLASSES), 'unique_families': len(UNIQUE),
    'strong_tournaments': len(strong), 'oriented_supports_examined': 729,
    'circulation_admissible_supports': len(admissible_supports),
    'monomials': len(TAU[0]), 'coefficient_histogram': dict(Counter(TAU[0].values())),
    'used_unique_families': len(USED), 'abc_witness': ABC,
    'exact_checks_by_kind': dict(COUNTS),
    'exact_rate_instances': len(RESULTS), 'rate_instances': RESULTS,
    'seconds': time.perf_counter() - START,
    'limitations': 'Finite certificate plus analytic cone proof establishes only the frozen K4 first-order static statement. Rate instances check conventions, not the universal quantifiers. No discovery code was imported; proposed certificate supports were shared as untrusted witnesses. This is AI-assisted internal review, not external peer review or author approval.'
}
Path('prufer-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'rate_instances'}, ensure_ascii=False, indent=2))
