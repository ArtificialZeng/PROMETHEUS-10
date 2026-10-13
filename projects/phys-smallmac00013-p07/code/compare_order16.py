#!/usr/bin/env python3
"""Cross-check the independent reserved hold-out calculations at order 16."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def terms(record: dict[str, object]) -> dict[int, int]:
    return {item["R"]: item["count"] for item in record["coefficients"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transfer", type=Path, required=True)
    parser.add_argument("--pfaffian", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    transfer = json.loads(args.transfer.read_text(encoding="utf-8"))
    pfaffian = json.loads(args.pfaffian.read_text(encoding="utf-8"))
    checks: list[tuple[str, bool, str]] = []
    checks.append((
        "matrix order",
        transfer["matrix_order"] == pfaffian["matrix_order"] == 16,
        "both routes report the predeclared order-16 hold-out",
    ))
    checks.append((
        "order-16 [t^3] coefficient vector",
        terms(transfer["lhs_t_coefficient"]) == terms(pfaffian["lhs_t3"]),
        "definition transfer versus BFK low-t Pfaffian",
    ))
    checks.append((
        "order-16 predicted RHS",
        terms(transfer["predicted_rhs"]) == terms(pfaffian["predicted_rhs"]),
        "independent constructions",
    ))
    checks.append((
        "order-16 zero difference",
        transfer["difference_is_zero"] is True and pfaffian["difference_is_zero"] is True,
        "exact integer/polynomial zero",
    ))
    checks.append((
        "order-14 unrefined coefficient vector",
        terms(transfer["rhs_unrefined"]) == terms(pfaffian["unrefined_order_minus_two"]),
        "definition transfer versus BFK Eq. (8.10)",
    ))
    checks.append((
        "order-16 minor relation",
        pfaffian["minor_relation"]["difference_is_zero"] is True,
        "C1=(1+7r)C0 exactly",
    ))
    order14_total = transfer["rhs_unrefined"]["total_at_r_1"]
    checks.append((
        "r=1 boundary factor",
        transfer["lhs_t_coefficient"]["total_at_r_1"] == 7 * order14_total,
        "[t^3] total equals 7 times the order-14 OSASM total",
    ))
    checks.append((
        "r=1 minor factor",
        pfaffian["c1"]["total_at_r_1"] == 8 * pfaffian["c0"]["total_at_r_1"],
        "specialization of C1=(1+7r)C0",
    ))

    lines = ["Independent exact order-16 reserved hold-out comparison"]
    failures: list[str] = []
    for name, passed, detail in checks:
        lines.append(f"{name}: {'PASS' if passed else 'FAIL'}; {detail}")
        if not passed:
            failures.append(name)
    lines.append(f"OVERALL: {'PASS' if not failures else 'FAIL'}")
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("failed checks: " + ", ".join(failures))


if __name__ == "__main__":
    main()
