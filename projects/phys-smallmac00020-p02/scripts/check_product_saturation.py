#!/usr/bin/env python3
"""Exact obstruction to saturating the Se3 witness with product rays.

This script tests only the equality case Q_SEP = 3/4.  Equality in the
Cauchy--Schwarz/tight-frame bound forces every transition probability of the
seven preparations to equal the target transition probability.  A product ray
has transition probability q^A_ij q^B_ij, where
q^X_ij=(1+r^X_i.r^X_j)/2 for unit Bloch vectors r^X_i in R^3.

The six zero target overlaps are assigned exhaustively to subsystem A,
subsystem B, or both.  Qubit orthogonality closes each assigned graph because
a ray has a unique orthogonal complement.  Exact Groebner reduction rejects
all but one closure pattern up to A/B exchange.  The survivor forces a 4-by-4
Bloch Gram matrix with negative determinant.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp


N = 7
ROOT = Path(__file__).resolve().parents[1]
SQRT7 = sp.sqrt(7)

# Zero-based unordered pairs.  These values are a separately simplified form
# of the exact overlaps recorded by the reproduction input.
TARGET = {
    (0, 1): sp.Rational(1, 2),
    (0, 2): sp.Rational(1, 2),
    (1, 2): sp.Rational(1, 4),
    (0, 3): sp.Rational(1, 2),
    (1, 3): sp.Rational(1, 4),
    (2, 3): sp.Rational(1, 4),
    (0, 4): sp.Integer(0),
    (1, 4): sp.Rational(1, 12),
    (2, 4): sp.Rational(1, 3),
    (3, 4): sp.Rational(1, 12),
    (0, 5): sp.Integer(0),
    (1, 5): sp.Rational(1, 4),
    (2, 5): sp.Integer(0),
    (3, 5): sp.Rational(1, 4),
    (4, 5): sp.Integer(0),
    (0, 6): (7 - 2 * SQRT7) / 14,
    (1, 6): (14 - 5 * SQRT7) / 42,
    (2, 6): (14 - 5 * SQRT7) / 42,
    (3, 6): (14 - 5 * SQRT7) / 42,
    (4, 6): sp.Integer(0),
    (5, 6): sp.Integer(0),
}
ZERO_EDGES = frozenset(pair for pair, value in TARGET.items() if value == 0)


def one_based(pairs):
    return [(i + 1, j + 1) for i, j in sorted(pairs)]


def check_reproduced_input() -> None:
    data = json.loads((ROOT / "evidence/input-a.json").read_text())
    observed = {}
    for record in data["pair_checks"]:
        i, j = sorted(index - 1 for index in record["pair"])
        observed[(i, j)] = sp.sympify(record["overlap_squared"])
    assert set(observed) == set(TARGET)
    for pair in TARGET:
        assert sp.simplify(observed[pair] - TARGET[pair]) == 0, pair


def qubit_closure(edges):
    """Return component/sign data and forced zero/one overlaps.

    In a connected local orthogonality graph, adjacent Bloch vectors are
    antipodal.  Hence same-parity vertices are the same ray and opposite-parity
    vertices are orthogonal.  A closure forcing a zero outside ZERO_EDGES is
    incompatible with the target immediately.
    """

    adjacency = [set() for _ in range(N)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)

    component = [None] * N
    sign = [None] * N
    component_count = 0
    for root in range(N):
        if component[root] is not None:
            continue
        component[root] = component_count
        sign[root] = 1
        stack = [root]
        while stack:
            i = stack.pop()
            for j in adjacency[i]:
                if component[j] is None:
                    component[j] = component_count
                    sign[j] = -sign[i]
                    stack.append(j)
                elif sign[j] != -sign[i]:
                    return None
        component_count += 1

    forced_zero = set()
    forced_one = set()
    for i, j in itertools.combinations(range(N), 2):
        if component[i] == component[j]:
            (forced_one if sign[i] == sign[j] else forced_zero).add((i, j))
    if not forced_zero <= ZERO_EDGES:
        return None
    return {
        "component": component,
        "sign": sign,
        "zero": frozenset(forced_zero),
        "one": frozenset(forced_one),
        "count": component_count,
    }


def description(model):
    return tuple(sorted(model["zero"])), tuple(sorted(model["one"]))


def enumerate_closures():
    ordered = {}
    zero_list = sorted(ZERO_EDGES)
    # 1=A, 2=B, 3=both.  Thus every exact target zero is accounted for.
    admissible_assignments = 0
    for assignment in itertools.product((1, 2, 3), repeat=len(zero_list)):
        edges_a = {edge for edge, label in zip(zero_list, assignment) if label & 1}
        edges_b = {edge for edge, label in zip(zero_list, assignment) if label & 2}
        model_a = qubit_closure(edges_a)
        model_b = qubit_closure(edges_b)
        if model_a is None or model_b is None:
            continue
        if model_a["zero"] | model_b["zero"] != ZERO_EDGES:
            continue
        admissible_assignments += 1
        ordered[(description(model_a), description(model_b))] = (model_a, model_b)

    exchange_classes = {}
    for model_a, model_b in ordered.values():
        key = min(
            (description(model_a), description(model_b)),
            (description(model_b), description(model_a)),
        )
        exchange_classes.setdefault(key, (model_a, model_b))
    return admissible_assignments, ordered, exchange_classes


def polynomial_system(model_a, model_b):
    variables = []
    cache = {}

    def local_q(model, prefix, i, j):
        ci = model["component"][i]
        cj = model["component"][j]
        si = model["sign"][i]
        sj = model["sign"][j]
        if ci == cj:
            return sp.Integer(1 if si == sj else 0)
        c, d = sorted((ci, cj))
        key = (prefix, c, d)
        if key not in cache:
            cache[key] = sp.Symbol(f"{prefix}{c}{d}")
            variables.append(cache[key])
        return (1 + si * sj * cache[key]) / 2

    equations = []
    for pair in sorted(TARGET):
        if TARGET[pair] == 0:
            continue
        qa = local_q(model_a, "a", *pair)
        qb = local_q(model_b, "b", *pair)
        equations.append((pair, sp.together(qa * qb - TARGET[pair])))
    return variables, equations, local_q


def groebner(variables, labelled_equations):
    return sp.groebner(
        [equation for _, equation in labelled_equations],
        *variables,
        extension=SQRT7,
        order="grevlex",
        method="f5b",
    )


def is_inconsistent(variables, labelled_equations):
    return groebner(variables, labelled_equations).contains(sp.Integer(1))


def irreducible_core(variables, equations):
    """Deterministically shrink to a deletion-minimal exact contradiction."""

    core = list(equations)
    changed = True
    while changed:
        changed = False
        for item in list(core):
            trial = [candidate for candidate in core if candidate is not item]
            if trial and is_inconsistent(variables, trial):
                core = trial
                changed = True
    return core


def main() -> None:
    check_reproduced_input()
    admissible, ordered, classes = enumerate_closures()
    print(f"SymPy {sp.__version__}")
    print("Exact target/input-A transition comparison: PASS (21/21)")
    print(f"Target zero-overlap edges: {one_based(ZERO_EDGES)}")
    print("Raw zero-edge assignments: 3^6 = 729")
    print(f"Assignments surviving exact qubit-orthogonality closure: {admissible}")
    print(f"Distinct ordered closure patterns: {len(ordered)}")
    print(f"Patterns up to A/B exchange: {len(classes)}")
    assert admissible == 26
    assert len(ordered) == 18
    assert len(classes) == 9

    inconsistent_count = 0
    survivors = []
    for index, (model_a, model_b) in enumerate(classes.values(), 1):
        variables, equations, local_q = polynomial_system(model_a, model_b)
        basis = groebner(variables, equations)
        inconsistent = basis.contains(sp.Integer(1))
        print(f"\nExchange class {index}")
        print(f"  A zero={one_based(model_a['zero'])}; A one={one_based(model_a['one'])}")
        print(f"  B zero={one_based(model_b['zero'])}; B one={one_based(model_b['one'])}")
        if inconsistent:
            inconsistent_count += 1
            core = irreducible_core(variables, equations)
            assert is_inconsistent(variables, core)
            print("  Exact transition equations: INCONSISTENT; Groebner basis is [1]")
            print("  Deletion-minimal contradictory pair set:")
            for pair, equation in core:
                print(f"    {(pair[0] + 1, pair[1] + 1)}: {sp.factor(equation)} = 0")
        else:
            print("  Exact transition equations alone: algebraically consistent")
            survivors.append((model_a, model_b, variables, equations, local_q, basis))

    assert inconsistent_count == 8
    assert len(survivors) == 1

    model_a, model_b, variables, equations, local_q, basis = survivors[0]
    short_zero = frozenset({(2, 5), (4, 5)})  # (3,6),(5,6) one-based
    short_one = frozenset({(2, 4)})           # (3,5) one-based
    if model_a["zero"] == short_zero and model_a["one"] == short_one:
        short_model, prefix = model_a, "a"
        long_model, long_prefix = model_b, "b"
    else:
        assert model_b["zero"] == short_zero and model_b["one"] == short_one
        short_model, prefix = model_b, "b"
        long_model, long_prefix = model_a, "a"

    # For rays 1,2,3,4 in the short subsystem, the remaining exact equations
    # force overlaps 3/4 from ray 1 to the others and 1/4 among rays 2,3,4.
    required_q = {
        (0, 1): sp.Rational(3, 4),
        (0, 2): sp.Rational(3, 4),
        (0, 3): sp.Rational(3, 4),
        (1, 2): sp.Rational(1, 4),
        (1, 3): sp.Rational(1, 4),
        (2, 3): sp.Rational(1, 4),
    }
    # Five of these six overlaps reduce directly modulo the transition ideal.
    # The remaining pair (2,4) follows from actual Bloch geometry: the ideal
    # forces long-subsystem q(2,3)=q(3,4)=1; equality in Cauchy--Schwarz for
    # unit Bloch vectors makes rays 2,3,4 identical, hence q(2,4)=1 too.  The
    # target product t_24=1/4 then fixes the short-subsystem q(2,4)=1/4.
    geometry_pair = (1, 3)
    for pair, expected in required_q.items():
        if pair == geometry_pair:
            continue
        expression = local_q(short_model, prefix, *pair)
        _, remainder = basis.reduce(sp.together(expression - expected))
        assert sp.simplify(remainder) == 0, (pair, remainder)
    for pair in ((1, 2), (2, 3)):
        expression = local_q(long_model, long_prefix, *pair)
        _, remainder = basis.reduce(sp.together(expression - 1))
        assert sp.simplify(remainder) == 0, (pair, remainder)

    gram = sp.eye(4)
    for (i, j), q in required_q.items():
        gram[i, j] = gram[j, i] = 2 * q - 1
    determinant = sp.factor(gram.det())
    charpoly = gram.charpoly()
    lam = charpoly.gen
    characteristic = sp.factor(charpoly.as_expr())
    assert determinant == -sp.Rational(27, 16)
    assert sp.expand(
        characteristic
        - (lam + sp.Rational(1, 2)) * (lam - sp.Rational(3, 2)) ** 3
    ) == 0

    print("\nOnly algebraic survivor (and its A/B swap)")
    print("  Transition ideal forces long-subsystem q(2,3)=q(3,4)=1")
    print("  Unit-Bloch geometry therefore forces q(2,4)=1 as well")
    print("  Forced short-subsystem q(1,k)=3/4 for k=2,3,4")
    print("  Forced short-subsystem q(k,l)=1/4 for 2<=k<l<=4")
    print("  Corresponding exact Bloch Gram matrix:")
    print(gram)
    print(f"  determinant={determinant}")
    print(f"  characteristic_polynomial={characteristic}")
    print("  eigenvalues={-1/2, 3/2, 3/2, 3/2}: NOT PSD")
    print("\nConclusion: no seven two-qubit product rays reproduce all 21 target")
    print("transition probabilities. Therefore an exactly separable strategy cannot")
    print("saturate W=3/4. Compactness implies Q_SEP<3/4, but this calculation does")
    print("not provide a numerical positive lower bound on 3/4-Q_SEP.")


if __name__ == "__main__":
    main()
