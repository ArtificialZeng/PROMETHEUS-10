"""Exact combinatorial POVM-span certificate for the frozen seven-T witness.

No floating point or finite-field rank is used. The seven rotation axes have
linearly independent ancillary X parts, so exactly one expansion branch can
survive the |0^7> contraction for each measured stabilizer element.
"""

import json
from collections import Counter
from pathlib import Path


N = 11
n = 4
m = 7


def symp(a, b):
    return ((a[0] & b[1]).bit_count() + (a[1] & b[0]).bit_count()) & 1


def rank_gf2(vectors):
    pivots = {}
    for v in vectors:
        w = v
        while w:
            k = w.bit_length() - 1
            if k not in pivots:
                pivots[k] = w
                break
            w ^= pivots[k]
    return len(pivots)


def read_witness():
    w = json.loads(Path("evidence/seven-t-witness.json").read_text())
    M = [tuple(v) for v in w["measurement_generators_xz"]]
    axes = [(tuple(p), s) for p, s in w["rotation_axes_xz_and_direction"]]
    assert len(M) == N and len(axes) == 7
    assert rank_gf2(x | (z << N) for x, z in M) == N
    assert all(symp(a, b) == 0 for a in M for b in M)
    return M, axes


def unique_ancilla_branches(axes):
    table = {}
    for mask in range(1 << len(axes)):
        x = 0
        for j, (p, _) in enumerate(axes):
            if (mask >> j) & 1:
                x ^= p[0] >> n
        assert x not in table
        table[x] = mask
    assert len(table) == 1 << m
    return table


def compute():
    M, axes = read_witness()
    branches = unique_ancilla_branches(axes)
    frequencies = Counter()
    first_representative = {}
    zero_rows = 0
    anti_histogram = Counter()
    for group_mask in range(1 << N):
        x = z = 0
        for j, (gx, gz) in enumerate(M):
            if (group_mask >> j) & 1:
                x ^= gx
                z ^= gz
        branch_mask = branches[x >> n]
        q = (x, z)
        nonzero = True
        anti_count = 0
        for j in range(6, -1, -1):
            p, direction = axes[j]
            anti = symp(p, q)
            choose_product = (branch_mask >> j) & 1
            if choose_product and not anti:
                nonzero = False
                break
            if anti:
                anti_count += 1
            if choose_product:
                q = (q[0] ^ p[0], q[1] ^ p[1])
        if not nonzero:
            zero_rows += 1
            continue
        assert q[0] >> n == 0
        data_code = (q[0] & 15) | ((q[1] & 15) << n)
        frequencies[data_code] += 1
        first_representative.setdefault(data_code, group_mask)
        anti_histogram[anti_count] += 1
    assert sum(frequencies.values()) + zero_rows == 1 << N
    assert len(frequencies) == 220, len(frequencies)
    return {
        "scope": "exact rank of one realizable 4-data, 7-ancilla, 7-T circuit",
        "measurement_group_independent_commuting_rank": N,
        "ancillary_x_axis_rank": m,
        "total_fourier_rows": 1 << N,
        "zero_fourier_rows": zero_rows,
        "nonzero_fourier_rows": sum(frequencies.values()),
        "distinct_surviving_data_paulis": len(frequencies),
        "exact_povm_span_rank": len(frequencies),
        "missing_data_pauli_codes": [j for j in range(256) if j not in frequencies],
        "data_pauli_frequency": dict(sorted(frequencies.items())),
        "one_measured_group_mask_per_surviving_data_pauli": dict(
            sorted(first_representative.items())),
        "anticommuting_rotation_count_histogram": dict(sorted(anti_histogram.items())),
        "coefficient_rule": "Each nonzero row equals a single signed data Pauli times (1/sqrt(2))^r, with r the listed anticommuting-rotation count for that row. Unique ancillary-X branch forbids cancellation.",
        "original_four_qubit_seven_T_question": "unresolved: rank 220 < 256",
    }


if __name__ == "__main__":
    result = compute()
    Path("evidence/seven-t-rank-220-exact.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "exact_povm_span_rank", "zero_fourier_rows",
        "nonzero_fourier_rows", "missing_data_pauli_codes")}, indent=2))
