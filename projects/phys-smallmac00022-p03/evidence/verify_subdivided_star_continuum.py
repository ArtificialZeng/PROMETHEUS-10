#!/usr/bin/env python3
"""Independent direct-basis replay of the continuum certificate's tight points.

This checker deliberately does not import the collective-spin generator.  It
builds K_s on the full computational parity bases, checks every saved rational
continuity inequality, and diagonalizes the reference point and the least-slack
candidate neighborhood for each q.  The floating replay is corroboration of
the exact packet, not the source of its continuum certification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import eigvalsh


SOURCE_SHA256 = "b0157003423c2c902269413156113e2b73122642841f382b726ed1a8066ae5c7"


def fraction(text: str) -> Fraction:
    return Fraction(text)


def parity_matrix(q: int, s: float, parity: int) -> np.ndarray:
    n = q + 3
    centre, middle, terminal = q, q + 1, q + 2
    edges = [(centre, leaf) for leaf in range(q)]
    edges.extend([(centre, middle), (middle, terminal)])
    basis = [state for state in range(1 << n) if state.bit_count() % 2 == parity]
    index = {state: position for position, state in enumerate(basis)}
    matrix = np.zeros((len(basis), len(basis)), dtype=np.float64)
    for state, column in index.items():
        for left, right in edges:
            left_bit = (state >> left) & 1
            right_bit = (state >> right) & 1
            if left_bit == right_bit == 0:
                matrix[column, column] += 1.0
                matrix[index[state ^ (1 << left) ^ (1 << right)], column] += s
            elif left_bit == right_bit == 1:
                matrix[column, column] += s * s
                matrix[index[state ^ (1 << left) ^ (1 << right)], column] += s
    assert np.array_equal(matrix, matrix.T)
    return matrix


def direct_margin(q: int, t: Fraction) -> float:
    t_float = float(t)
    s = t_float ** 0.5
    even = parity_matrix(q, s, 0)
    odd = parity_matrix(q, s, 1)
    even_top = eigvalsh(
        even, subset_by_index=[even.shape[0] - 2, even.shape[0] - 1]
    )
    odd_top = eigvalsh(
        odd, subset_by_index=[odd.shape[0] - 1, odd.shape[0] - 1]
    )[0]
    return float(even_top[-1] - max(even_top[-2], odd_top) - (1.0 - t_float))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()

    packet = json.loads(args.packet.read_text())
    assert packet["status"] == "exact_computer_assisted_continuum_certificate"
    assert hashlib.sha256(args.source.read_bytes()).hexdigest() == SOURCE_SHA256
    assert packet["min_q"] == 2 and packet["max_q"] >= packet["min_q"]

    total_neighborhoods = 0
    replay_records = []
    for record in packet["records"]:
        q = int(record["q"])
        neighborhoods = record["candidate_root_neighborhoods"]
        assert len(neighborhoods) == record["interior_candidate_root_count_with_duplicates"]
        assert sum(item["interior_real_roots"] for item in record["crossing_resultants"]) == len(neighborhoods)
        total_neighborhoods += len(neighborhoods)

        exact_slacks: list[tuple[Fraction, dict[str, str]]] = []
        for item in neighborhoods:
            lo, hi = fraction(item["t_lo"]), fraction(item["t_hi"])
            margin = fraction(item["exact_margin_lower"])
            variation = fraction(item["continuity_variation_upper"])
            assert 0 < lo <= hi < 1
            assert margin > variation >= 0
            exact_slacks.append((margin - variation, item))

        tight_slack, tight = min(exact_slacks, key=lambda pair: pair[0])
        tight_midpoint = (fraction(tight["t_lo"]) + fraction(tight["t_hi"])) / 2
        direct_tight = direct_margin(q, tight_midpoint)
        direct_reference = direct_margin(q, Fraction(1, 4))
        assert direct_tight > float(tight_slack) - 1e-10
        assert direct_reference > float(fraction(record["reference_margin_lower"])) - 1e-10
        assert direct_tight > 0 and direct_reference > 0
        replay_records.append(
            {
                "q": q,
                "n": q + 3,
                "tight_block": tight["block"],
                "tight_t_mid": float(tight_midpoint),
                "packet_tight_slack": float(tight_slack),
                "direct_full_basis_tight_margin": direct_tight,
                "direct_full_basis_reference_margin": direct_reference,
            }
        )

    assert [item["q"] for item in replay_records] == list(
        range(packet["min_q"], packet["max_q"] + 1)
    )
    print(f"packet_exact_inequalities=PASS neighborhoods={total_neighborhoods}")
    print("source_sha256=PASS")
    print("direct_full_basis_replay=PASS reference_and_least_slack_point_each_q")
    print(json.dumps(replay_records, sort_keys=True))
    print("numeric_replay_scope=corroboration_not_continuum_proof")


if __name__ == "__main__":
    main()
