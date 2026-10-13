#!/usr/bin/env python3
"""Independent replay of the k=5 certificate from frozen input-a.json.

Unlike exact_k5_degeneracy.py, this checker does not import or execute the graph
generator.  It rebuilds the matrix from the serialized signed root edges and
local-attachment list, checks the stored integer kernel, and tests the stored
bivariate factorization at the held-out rational parameter J=2/5.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


EVIDENCE = Path(__file__).resolve().parent
INPUT = EVIDENCE / "input-a.json"
RESULT = EVIDENCE / "exact-k5-degeneracy.json"
KERNEL = EVIDENCE / "exact-k5-kernel-basis.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    kernel_record = json.loads(KERNEL.read_text(encoding="utf-8"))
    root = [tuple(edge) for edge in source["oriented_root_edges_by_term"]]
    cliques = source["root_cliques"]
    local = source["local_field_attachment_vertices"]
    n = source["augmented_root_vertex_count"]
    augmented = root + [(vertex, len(cliques) + index)
                        for index, vertex in enumerate(local)]
    if (len(root), len(local), len(cliques), n) != (81, 39, 69, 108):
        raise RuntimeError("serialized graph counts changed")

    J, z, x = sp.symbols("J z x")
    A = sp.zeros(n)
    for edge, (u, v) in enumerate(augmented):
        weight = 1 if edge < len(root) else J
        A[u, v], A[v, u] = weight, -weight

    # Held-out rational specialization: B=5 A(2/5) is integral.  Compare a
    # fresh exact charpoly with 5^108 p_A(z/5,2/5) reconstructed only from the
    # factor strings stored by the producer.
    B_holdout = A.subs(J, sp.Rational(2, 5)) * 5
    domain = DomainMatrix.from_Matrix(B_holdout)
    direct_coefficients = [domain.domain.to_sympy(value) for value in domain.charpoly()]
    direct = sp.Poly.from_list(direct_coefficients, gens=z)
    factors = result["exact_bivariate_factorization"]["det_zI_minus_A_factors"]
    reconstructed = sp.Integer(1)
    for item in factors:
        factor = sp.sympify(item["factor"], locals={"J": J, "z": z})
        reconstructed *= factor ** int(item["exponent"])
    heldout = sp.Poly(sp.expand(5**n * reconstructed.subs({J: sp.Rational(2, 5), z: z / 5})), z)
    if direct != heldout:
        raise RuntimeError("held-out exact characteristic polynomial mismatch")

    B_special = A.subs(J, sp.Rational(1, 3)) * 3
    K = B_special * B_special + sp.eye(n)
    vectors = sp.Matrix(kernel_record["vectors"])
    if vectors.shape != (28, 108) or K * vectors.T != sp.zeros(108, 28):
        raise RuntimeError("stored exact kernel substitution failed")
    if DomainMatrix.from_Matrix(vectors).to_field().rank() != 28:
        raise RuntimeError("stored kernel vectors are not independent")

    # Replay every rational branch-isolation interval from the stored
    # dispersive factor, including its exact ordering relative to x=J.
    G = sp.sympify(result["exact_bivariate_factorization"]["dispersive_factor"],
                   locals={"J": J, "x": x})
    branch_checks = []
    for item in result["rational_branch_tracking"]:
        j_value = sp.Rational(item["J"])
        lower = sp.Rational(item["dispersive_x_interval"][0])
        upper = sp.Rational(item["dispersive_x_interval"][1])
        count = int(sp.Poly(G.subs(J, j_value), x, domain=sp.QQ).count_roots(lower, upper))
        ordering = "dispersive_above_flat" if lower > j_value else "dispersive_below_flat"
        if count != 1 or ordering != item["ordering"]:
            raise RuntimeError("stored rational branch tracking failed replay")
        branch_checks.append({"J": str(j_value), "root_count": count, "ordering": ordering})

    print(json.dumps({
        "status": "pass",
        "representation": "serialized input-a signed edges; generator not imported",
        "input_a_sha256": digest(INPUT),
        "result_sha256": digest(RESULT),
        "kernel_sha256": digest(KERNEL),
        "heldout_J": "2/5",
        "heldout_charpoly_degree": direct.degree(),
        "heldout_charpoly_exact_match": True,
        "kernel_shape": list(vectors.shape),
        "kernel_exact_substitution": True,
        "kernel_independent_rows": 28,
        "branch_checks": branch_checks,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
