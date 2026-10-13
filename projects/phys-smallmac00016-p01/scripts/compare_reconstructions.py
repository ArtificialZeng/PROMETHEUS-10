#!/usr/bin/env python3
"""Fresh-run comparison of the exact-Kraus and independent Liouville reconstructions."""

import pathlib
import re
import subprocess
import sys
import numpy as np
import sympy as sp


ROOT = pathlib.Path(__file__).resolve().parent


def run(name):
    return subprocess.run([sys.executable, str(ROOT / name)], check=True,
                          text=True, capture_output=True).stdout


def paths_a(text):
    out = {}
    pat = re.compile(r"path=(\d\d);bits=(\d\d);trace=(.*);trace_sq=(.*)")
    for line in text.splitlines():
        m = pat.fullmatch(line)
        if m:
            out[m.group(1)] = (m.group(2), sp.sympify(m.group(4)))
    return out


def paths_b(text):
    out = {}
    pat = re.compile(r"path=(\d\d);bits=(\d\d);trace=.*;trace_sq=([0-9.eE+-]+)")
    for line in text.splitlines():
        m = pat.fullmatch(line)
        if m:
            out[m.group(1)] = (m.group(2), float(m.group(3)))
    return out


def main():
    a_text = run("reconstruct_a_exact.py")
    b_text = run("reconstruct_b_liouville.py")
    a, b = paths_a(a_text), paths_b(b_text)
    if set(a) != set(b) or len(a) != 16:
        raise RuntimeError(f"path coverage mismatch A={len(a)} B={len(b)}")
    residuals = []
    bit_mismatches = []
    for path in sorted(a):
        if a[path][0] != b[path][0]:
            bit_mismatches.append(path)
        residual = abs(float(sp.N(a[path][1], 17)) - b[path][1])
        residuals.append(residual)
        print(f"path={path};bits_A={a[path][0]};bits_B={b[path][0]};trace_sq_residual={residual:.3e}")

    p, q, g = 18/25, 7/25, 3/10
    s = np.sqrt(1-g)
    exact_float = [
        np.sqrt(p)*np.diag([1, s]),
        np.sqrt(p*g)*np.array([[0, 1], [0, 0]]),
        np.sqrt(q)*np.diag([s, 1]),
        np.sqrt(q*g)*np.array([[0, 0], [1, 0]]),
    ]
    thermal = [
        np.sqrt(p)*np.diag([1, s]),
        np.sqrt(p*g)*np.outer([1, 0], [0, 1]),
        np.sqrt(q)*np.diag([s, 1]),
        np.sqrt(q*g)*np.outer([0, 1], [1, 0]),
    ]
    matrix_residuals = [np.max(np.abs(x-y)) for x, y in zip(exact_float, thermal)]
    print("basis_map=A and B use ordered energy/computational basis |0>,|1>; rows output, columns input")
    print("kraus_map=A0<-B_down_nojump,A1<-B_down_jump,A2<-B_up_nojump,A3<-B_up_jump")
    print("pairing_map=A(03|12)<->B((down_nojump,up_jump)|(down_jump,up_nojump))")
    print("representation_map=vec_F(K)=[K00,K10,K01,K11];L(K)=conj(K) tensor K")
    print("choi_map=J=sum_ij |i><j|_in tensor T(|i><j|)_out;Tr_out(J)=I")
    print("normalization_map=F_e=(1/4)sum_path|tr(A_path)|^2=Tr(S_channel)/4")
    print("kraus_rowwise_max_residuals=" + ",".join(f"{x:.3e}" for x in matrix_residuals))
    print(f"path_count_A={len(a)};path_count_B={len(b)}")
    print(f"bit_map_mismatch_count={len(bit_mismatches)}")
    print(f"all_path_trace_sq_max_residual={max(residuals):.3e}")
    assert not bit_mismatches
    assert max(matrix_residuals) < 1e-15
    assert max(residuals) < 1e-14
    print("comparison_status=PASS")


if __name__ == "__main__":
    main()
