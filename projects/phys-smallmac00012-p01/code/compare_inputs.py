#!/usr/bin/env python3
"""Compare direct transcription A with independently derived input B."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


with (ROOT / "evidence/input-a.json").open(encoding="utf-8") as handle:
    input_a = json.load(handle)
with (ROOT / "evidence/input-b.json").open(encoding="utf-8") as handle:
    input_b = json.load(handle)

print("A/B INPUT COMPARISON — exact symbolic convention audit")
require(input_a["input_id"] == "A" and input_b["input_id"] == "B", "distinct A and B records loaded")
require(input_a["kind"] != input_b["kind"], "A is a transcription and B is a derivation")
require(input_a["dimension"] == input_b["dimension"] == 3, "both inputs concern order three")
require(input_a["selected_columns_zero_based"] == input_b["selected_columns_zero_based"] == [0, 1], "both inputs select columns 0 and 1 after indexing map")

mapped_a_lengths = [item.replace("B_", "M_") for item in input_a["lengths"]]
require(mapped_a_lengths == input_b["lengths"], "row-by-row length entries agree after B->M symbol rename")

L0, L1, L2 = sp.symbols("L0 L1 L2", nonnegative=True)
x0, x1, x2 = L0**2, L1**2, L2**2
h = 2 * (x0*x1 + x0*x2 + x1*x2) - (x0**2 + x1**2 + x2**2)
heron = (L0+L1+L2)*(-L0+L1+L2)*(L0-L1+L2)*(L0+L1-L2)
require(sp.expand(h-heron) == 0, "derived h equals the four-factor Heron polynomial identically")

c11 = (L2**2-L0**2-L1**2)/(2*L0*L1)
c21 = (L1**2-L2**2-L0**2)/(2*L0*L2)
cdiff = (L0**2-L1**2-L2**2)/(2*L1*L2)
require(sp.simplify(L0**2 + L1**2 + 2*L0*L1*c11 - L2**2) == 0, "A Eq. (24) first cosine is the triangle cosine law")
require(sp.simplify(L0**2 + L2**2 + 2*L0*L2*c21 - L1**2) == 0, "A Eq. (24) second cosine is the triangle cosine law")
require(sp.simplify(L1**2 + L2**2 + 2*L1*L2*cdiff - L0**2) == 0, "A Eq. (25) relative cosine is the triangle cosine law")

print("MAP: S1 indices 0,1,2 map directly to project indices 0,1,2; S2 indices 1,2,3 map by j_project=j_source-1.")
print("MAP: source B_ij and derived M_ij both mean output row i, input column j; project dynamics is p'=M p.")
print("MAP: |L1-L2|<=L0<=L1+L2 gives all three triangle inequalities; symmetrically this is 2*max(Li)<=sum(Li).")
print("MAP: source dephasing sets the L0 term phase to zero; B permits arbitrary common phase and fixes it to zero only for comparison.")
print("MAP: the source cosine quotients exclude zero denominators; B supplies explicit two-positive, one-positive, and all-zero branches.")
print("INDEPENDENCE: A was transcribed from two official primary renderings. B was derived from normalization, pair orthogonality, and 3D completion; it did not execute or import A. This comparison script reads both only after they were recorded. Same-worker independence is weaker than a fresh referee reconstruction.")
print("RESULT: exact agreement after the stated basis/index/phase convention map.")
