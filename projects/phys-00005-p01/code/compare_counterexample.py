#!/usr/bin/env python3
"""Compare the independent structural/spectral and literal/exact witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-a", required=True)
    parser.add_argument("--method-b", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log", required=True)
    args = parser.parse_args()
    path_a = Path(args.method_a)
    path_b = Path(args.method_b)
    a = json.loads(path_a.read_bytes())
    b = json.loads(path_b.read_bytes())
    if a["n"] != b["n"] or a["edges_zero_based"] != b["edges_zero_based"]:
        raise AssertionError("independent witness edge lists differ")
    if a["laplacian"] != b["laplacian"]:
        raise AssertionError("independently built Laplacians differ")
    exact_tau = Fraction(b["tau_exact"])
    exact_path = Fraction(b["path_tau_exact"])
    exact_delta = Fraction(b["delta_exact"])
    if exact_tau - exact_path != exact_delta or exact_delta >= 0:
        raise AssertionError("exact deficit identity/sign failed")
    numeric_errors = {
        "loose_tau_minus_exact_abs": abs(float(a["tau_loose"]) - float(exact_tau)),
        "strict_tau_minus_exact_abs": abs(float(a["tau_strict"]) - float(exact_tau)),
    }
    if max(numeric_errors.values()) > 1.0e-12:
        raise AssertionError("independent numerical/exact traces disagree")
    output = {
        "claim": "The listed n=16 simple unweighted graph has tau(G)=1673/1192 < tau(P_16)=23/16 and therefore disproves the frozen universal path-minimization inequality.",
        "comparison": {
            "complete_edge_lists_equal": "pass",
            "exact_deficit_identity": "pass",
            "independently_constructed_laplacians_equal_entrywise": "pass",
            "numerical_exact_agreement_within_1e-12": "pass",
        },
        "delta_exact": str(exact_delta),
        "method_a": str(path_a),
        "method_a_sha256": file_hash(path_a),
        "method_b": str(path_b),
        "method_b_sha256": file_hash(path_b),
        "n": int(a["n"]),
        "numeric_errors": numeric_errors,
        "path_tau_exact": str(exact_path),
        "physical_interpretation": "For a uniform initial vertex, the exact Cesaro-averaged return probability is smaller than the path value by 81/38144.",
        "status": "exact_counterexample_verified",
        "tau_exact": str(exact_tau),
        "uniform_return_deficit_exact": str(exact_delta / int(a["n"])),
    }
    Path(args.output).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.log).write_text(
        "\n".join(
            [
                "COUNTEREXAMPLE INDEPENDENT COMPARISON",
                f"Method A SHA-256: {output['method_a_sha256']}",
                f"Method B SHA-256: {output['method_b_sha256']}",
                "PASS: complete edge lists and independently constructed Laplacians agree entrywise.",
                f"PASS: numerical/exact errors {numeric_errors} are <= 1e-12.",
                f"PASS: tau={exact_tau}, path_tau={exact_path}, exact_delta={exact_delta}<0.",
                f"Uniform-initial-vertex return deficit: {exact_delta/int(a['n'])}.",
                "Scope: this one admissible witness disproves the universal quantifier; it does not classify minimizers at n=16 or any other n.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"delta": str(exact_delta), "status": output["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
