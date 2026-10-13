#!/usr/bin/env python3
"""Direct held-out checks for the frozen pass-3 Schur recurrence.

This checker does not import the prediction producer.  It rebuilds the signed
all-cycle-+1 matrices from the reproduced Pauli/cell generator, evaluates the
k=5 Schur response over QQ, and computes complete k=6 characteristic
polynomials over two finite fields with FLINT.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from flint import fmpq, fmpq_mat, fmpz_mod_ctx, fmpz_mod_mat


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
GENERATOR = HERE / "reproduce_sierpinski_hanoi.py"
FREEZE = HERE / "cycle-schur-pass3-freeze.json"
RESULT = HERE / "cycle-schur-pass3-replay.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_generator():
    spec = importlib.util.spec_from_file_location("direct_graph", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load reproduced graph generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_combinatorics(rr, k: int) -> dict:
    addresses, terms, frustration, _ = rr.graph_from_cells(k)
    cliques, root_edges, _ = rr.krausz_root(len(addresses), frustration)
    oriented, tree, cycles, flux = rr.all_plus_orientation(terms, root_edges)
    n, augmented_edges, augmented_oriented, local, degrees = rr.augment_local(
        root_edges, oriented, cliques
    )
    return {
        "k": k,
        "addresses": addresses,
        "terms": terms,
        "frustration": frustration,
        "cliques": cliques,
        "root_edges": root_edges,
        "oriented": oriented,
        "tree": tree,
        "cycles": cycles,
        "flux": flux,
        "n": n,
        "augmented_edges": augmented_edges,
        "augmented_oriented": augmented_oriented,
        "local": local,
        "degrees": degrees,
    }


def fq(value: Fraction | int) -> fmpq:
    value = Fraction(value)
    return fmpq(value.numerator, value.denominator)


def direct_response(data: dict, J: Fraction, z: Fraction) -> list[list[Fraction]]:
    n = data["n"]
    root_n = len(data["cliques"])
    matrix = [[fq(z if i == j else 0) for j in range(n)] for i in range(n)]
    for edge, (u, v) in enumerate(data["augmented_oriented"]):
        weight = Fraction(1) if edge < len(data["root_edges"]) else J
        # M=zI-A with A_uv=+weight on the stored u->v orientation.
        matrix[u][v] -= fq(weight)
        matrix[v][u] += fq(weight)
    boundary = [index for index, degree in enumerate(data["degrees"]) if degree == 1]
    if len(boundary) != 3 or any(index >= root_n for index in boundary):
        raise RuntimeError("unexpected boundary set")
    interior = [index for index in range(n) if index not in boundary]

    def block(rows: list[int], cols: list[int]) -> fmpq_mat:
        return fmpq_mat([[matrix[i][j] for j in cols] for i in rows])

    Mbb = block(boundary, boundary)
    Mbi = block(boundary, interior)
    Mib = block(interior, boundary)
    Mii = block(interior, interior)
    response = Mbb - Mbi * Mii.solve(Mib)
    out: list[list[Fraction]] = []
    for i in range(3):
        row = []
        for j in range(3):
            entry = response[i, j]
            row.append(Fraction(int(entry.numerator), int(entry.denominator)))
        out.append(row)
    return out


def match_canonical_response(
    response: list[list[Fraction]], alpha: Fraction, beta: Fraction
) -> list[int] | None:
    target = [[alpha if i == j else beta for j in range(3)] for i in range(3)]
    for signs in itertools.product((1, -1), repeat=3):
        if signs[0] != 1:
            continue
        transformed = [
            [response[i][j] * signs[i] * signs[j] for j in range(3)]
            for i in range(3)
        ]
        if transformed == target:
            return list(signs)
    return None


def direct_modular_charpoly(data: dict, prime: int, j_num: int, j_den: int) -> list[int]:
    ctx = fmpz_mod_ctx(prime)
    n = data["n"]
    rows = [[ctx(0) for _ in range(n)] for _ in range(n)]
    j = (j_num * pow(j_den, -1, prime)) % prime
    for edge, (u, v) in enumerate(data["augmented_oriented"]):
        weight = 1 if edge < len(data["root_edges"]) else j
        rows[u][v] += ctx(weight)
        rows[v][u] -= ctx(weight)
    matrix = fmpz_mod_mat(rows, ctx)
    polynomial = matrix.charpoly()
    coefficients = [int(value) for value in polynomial.coeffs()]
    if polynomial.degree() != n or len(coefficients) != n + 1:
        raise RuntimeError("direct modular characteristic polynomial has wrong degree")
    return coefficients


def main() -> None:
    expected = os.environ.get("PHYSICS_PYTHON")
    if not expected or Path(sys.executable).resolve() != Path(expected).resolve():
        raise RuntimeError(
            f"scientific Python mismatch: executable={sys.executable!r}, "
            f"PHYSICS_PYTHON={expected!r}"
        )
    if RESULT.exists():
        raise RuntimeError(f"refusing to overwrite replay {RESULT}")

    freeze_bytes = FREEZE.read_bytes()
    frozen = json.loads(freeze_bytes)
    rr = load_generator()
    start = time.perf_counter()
    k5 = build_combinatorics(rr, 5)
    k6 = build_combinatorics(rr, 6)
    build_seconds = time.perf_counter() - start

    expected_counts = {
        5: {"terms": 81, "root_vertices": 69, "cycles": 13, "local": 39, "modes": 108},
        6: {"terms": 243, "root_vertices": 204, "cycles": 40, "local": 120, "modes": 324},
    }
    count_records = []
    for data in (k5, k6):
        k = data["k"]
        actual = {
            "terms": len(data["terms"]),
            "root_vertices": len(data["cliques"]),
            "cycles": len(data["cycles"]),
            "local": len(data["local"]),
            "modes": data["n"],
        }
        if actual != expected_counts[k]:
            raise RuntimeError(f"count mismatch at k={k}: {actual}")
        if len(data["flux"]) != len(data["cycles"]) or not all(
            record["projected_eigenvalue"] == 1 for record in data["flux"]
        ):
            raise RuntimeError(f"cycle-sector check failed at k={k}")
        count_records.append({"k": k, **actual, "all_cycle_fluxes_plus_one": True})

    response_records = []
    for prediction in frozen["frozen_k5_direct_response_tests"]:
        J = Fraction(prediction["J"])
        z = Fraction(prediction["z"])
        alpha = Fraction(prediction["alpha_5"])
        beta = Fraction(prediction["beta_5"])
        point_start = time.perf_counter()
        response = direct_response(k5, J, z)
        elapsed = time.perf_counter() - point_start
        gauge = match_canonical_response(response, alpha, beta)
        if gauge is None:
            raise RuntimeError(f"frozen k=5 response mismatch at J={J}, z={z}")
        response_records.append({
            "J": str(J),
            "z": str(z),
            "frozen_alpha_5": str(alpha),
            "frozen_beta_5": str(beta),
            "direct_boundary_gauge": gauge,
            "all_nine_entries_exact": True,
            "direct_response_seconds": elapsed,
        })

    modular_records = []
    for prediction in frozen["frozen_k6_modular_characteristic_tests"]:
        prime = prediction["prime"]
        case_start = time.perf_counter()
        actual = direct_modular_charpoly(
            k6, prime, prediction["J_num"], prediction["J_den"]
        )
        elapsed = time.perf_counter() - case_start
        expected_coefficients = prediction["predicted_coefficients"]
        if actual != expected_coefficients:
            mismatch = next(
                index for index, (left, right) in enumerate(zip(actual, expected_coefficients))
                if left != right
            )
            raise RuntimeError(
                f"held-out k=6 characteristic mismatch mod {prime} at coefficient {mismatch}"
            )
        encoded = json.dumps(actual, separators=(",", ":")).encode("ascii")
        digest = hashlib.sha256(encoded).hexdigest()
        if digest != prediction["predicted_coefficients_sha256"]:
            raise RuntimeError("coefficient digest mismatch despite list equality")
        modular_records.append({
            "prime": prime,
            "J_num": prediction["J_num"],
            "J_den": prediction["J_den"],
            "degree": len(actual) - 1,
            "coefficient_count": len(actual),
            "all_coefficients_equal": True,
            "coefficient_sha256": digest,
            "direct_charpoly_seconds": elapsed,
        })

    result = {
        "schema_version": 1,
        "job_id": os.environ.get("PHYSICS_JOB_ID", "phys-00021-p01-research-407f59d97b19"),
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "sympy_version": sp.__version__,
        },
        "prediction_binding": {
            "freeze_file": "evidence/cycle-schur-pass3-freeze.json",
            "freeze_sha256_before_direct_tests": hashlib.sha256(freeze_bytes).hexdigest(),
            "producer_imported": False,
            "direct_generator": "evidence/reproduce_sierpinski_hanoi.py",
            "direct_generator_sha256": sha256(GENERATOR),
            "source_sha256": sha256(PROJECT / "source.md"),
        },
        "direct_graphs": count_records,
        "k5_exact_rational_responses": response_records,
        "k6_complete_modular_characteristic_polynomials": modular_records,
        "timing": {"direct_graph_build_seconds": build_seconds},
        "result": "pass",
        "limitations": "Finite-field identities are exact in the stated fields and test every coefficient, but they do not alone prove a characteristic identity over ZZ[J,z]; the all-depth proof uses the separate signed-copy and Schur induction.",
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "pass",
        "result": str(RESULT.relative_to(PROJECT)),
        "freeze_sha256": result["prediction_binding"]["freeze_sha256_before_direct_tests"],
        "k5_response_tests": len(response_records),
        "k6_modular_tests": [
            {"prime": item["prime"], "degree": item["degree"], "hash": item["coefficient_sha256"]}
            for item in modular_records
        ],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
