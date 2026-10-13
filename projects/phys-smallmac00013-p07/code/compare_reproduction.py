#!/usr/bin/env python3
"""Compare independent OSASM routes and the published BFK baselines."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TABLE3 = {1: 1, 2: 1, 3: 4, 4: 3, 5: 32, 6: 26, 7: 640, 8: 646, 9: 34048, 10: 45885, 11: 4945920, 12: 9304650}


def term_map(record: dict[str, object]) -> dict[tuple[int, int], int]:
    return {(x["R"], x["T"]): x["count"] for x in record["terms"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-a", type=Path, required=True)
    parser.add_argument("--input-b", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    route_a = json.loads(args.input_a.read_text(encoding="utf-8"))
    route_b = json.loads(args.input_b.read_text(encoding="utf-8"))
    common = sorted(set(route_a["orders"]) & set(route_b["orders"]), key=int)
    lines: list[str] = []
    failures: list[str] = []

    lines.append("Convention map: matrix order m is BFK subscript n; R=sum_{i<j}|A_ij|; T is one-based; monomial key (R,T) maps to r^R t^T.")
    for key in common:
        a_terms = term_map(route_a["orders"][key])
        b_terms = term_map(route_b["orders"][key])
        status = "PASS" if a_terms == b_terms else "FAIL"
        lines.append(f"full polynomial order={key}: {status}; terms={len(a_terms)}; total={sum(a_terms.values())}")
        if status == "FAIL":
            failures.append(f"route disagreement order {key}")

    expected_eq83 = {
        1: {(0, 1): 1},
        2: {(1, 2): 1},
        3: {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 2): 1},
        4: {(2, 2): 1, (2, 3): 1, (2, 4): 1},
    }
    for order, expected in expected_eq83.items():
        actual = term_map(route_a["orders"][str(order)])
        status = "PASS" if actual == expected else "FAIL"
        lines.append(f"BFK Eq. (8.3) order={order}: {status}")
        if status == "FAIL":
            failures.append(f"Eq. 8.3 order {order}")

    for key, record in route_a["orders"].items():
        order = int(key)
        expected = TABLE3.get(order)
        if expected is None:
            continue
        status = "PASS" if record["total"] == expected else "FAIL"
        lines.append(f"BFK Table 3 order={order}: {status}; got={record['total']}; expected={expected}")
        if status == "FAIL":
            failures.append(f"Table 3 order {order}")

    # Eq. (8.32): [t^2] X_m = r X_{m-2}(r,1), for even m.
    for key, record in route_a["orders"].items():
        order = int(key)
        if order < 2 or order % 2:
            continue
        lhs: dict[int, int] = {}
        for (rho, tau), count in term_map(record).items():
            if tau == 2:
                lhs[rho] = count
        if order == 2:
            rhs = {1: 1}
        else:
            rhs_counts = term_map(route_a["orders"][str(order - 2)])
            rhs = {}
            for (rho, _tau), count in rhs_counts.items():
                rhs[rho + 1] = rhs.get(rho + 1, 0) + count
        status = "PASS" if lhs == rhs else "FAIL"
        lines.append(f"BFK Eq. (8.32) order={order}: {status}; coefficient_terms={len(lhs)}")
        if status == "FAIL":
            failures.append(f"Eq. 8.32 order {order}")

    lines.append(f"OVERALL: {'PASS' if not failures else 'FAIL'}")
    if failures:
        lines.append("Failures: " + "; ".join(failures))
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
