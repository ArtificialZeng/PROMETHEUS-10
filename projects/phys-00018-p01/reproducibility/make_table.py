"""Generate the manuscript table from frozen exact rational upper bounds."""
from fractions import Fraction
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def upward_decimal(value, places=12):
    value = Fraction(value)
    unit = 10 ** places
    numerator = -((-value.numerator * unit) // value.denominator)
    whole, remainder = divmod(numerator, unit)
    displayed = f"{whole}.{remainder:0{places}d}"
    assert Fraction(displayed) >= value
    return displayed


def main():
    rows, records = [], []
    for n in (32, 48):
        record = json.loads((ROOT / f"evidence/research-pass4/riesz-n{n}-results.json").read_text())
        for index, item in enumerate(record["checks"], 1):
            exact = Fraction(item["whole_space_norm_upper"])
            upper = upward_decimal(exact)
            flag = exact <= Fraction(4, 5)
            assert flag == item["norm_at_most_four_fifths"]
            rows.append(f"{n} & $V_{index}$ & {upper} & " + ("Yes" if flag else "No") + r" \\")
            records.append({"basis": n, "form": f"V{index}", "exact_upper": str(exact),
                            "displayed_upper": upper, "below_four_fifths": flag})
    text = r"""\begin{table}[htbp]
\centering
\begin{tabular}{@{}rccc@{}}
\toprule
Riesz dimension $n$ & Return form & Full-space norm upper bound & Below $4/5$ \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\caption{Whole-space return bounds after finite Riesz projection and
explicit residual-tail control. Each decimal is rounded upward from
an exact rational bound. The finite projected norm bound is $3/4$,
certified in a 64-dimensional response space. The 32-dimensional
projection is insufficient for the selected $4/5$ constant; the
48-dimensional projection establishes it.}
\label{tab:certificate}
\end{table}
"""
    (ROOT / "manuscript/certificate-table.tex").write_text(text)
    out = ROOT / "evidence/write"
    out.mkdir(parents=True, exist_ok=True)
    (out / "table-generation.json").write_text(
        json.dumps({"method": "Exact rational ceiling, 12 decimal places",
                    "records": records}, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "all_rounding_outward": True}))


if __name__ == "__main__":
    main()
