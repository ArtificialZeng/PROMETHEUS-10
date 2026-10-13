#!/usr/bin/env python3
"""Independent thermal-transition/Liouville reconstruction of the same input."""

import sys
import numpy as np
import scipy


def L(k):
    return np.kron(k.conj(), k)


def sqrt_psd(a):
    w, v = np.linalg.eigh((a + a.conj().T) / 2)
    return (v * np.sqrt(np.clip(w, 0, None))) @ v.conj().T


def choi_from_action(action):
    j = np.zeros((4, 4), dtype=complex)
    for i in range(2):
        for k in range(2):
            e = np.zeros((2, 2), dtype=complex)
            e[i, k] = 1
            j[2*i:2*i+2, 2*k:2*k+2] = action(e)
    return j


def partial_trace_output(j):
    return np.einsum("iaja->ij", j.reshape(2, 2, 2, 2))


def main():
    p_thermal = 18.0 / 25.0
    excited_thermal = 1.0 - p_thermal
    loss = 3.0 / 10.0
    survival = np.sqrt(1.0 - loss)
    e0 = np.array([1.0, 0.0])
    e1 = np.array([0.0, 1.0])
    # Derived independently as downward and upward thermal-transition branches.
    branches = [
        np.sqrt(p_thermal) * np.diag([1.0, survival]),
        np.sqrt(p_thermal * loss) * np.outer(e0, e1),
        np.sqrt(excited_thermal) * np.diag([survival, 1.0]),
        np.sqrt(excited_thermal * loss) * np.outer(e1, e0),
    ]
    grouping = {0: (0, 3), 1: (1, 2)}
    observed = {x: b for b, xs in grouping.items() for x in xs}
    eye = np.eye(2)
    xgate = np.array([[0.0, 1.0], [1.0, 0.0]])
    ygate = np.array([[0.0, -1j], [1j, 0.0]])
    zgate = np.diag([1.0, -1.0])
    print("representation=B/thermal transitions and column-major Liouville matrices")
    print(f"python={sys.version.split()[0]};numpy={np.__version__};scipy={scipy.__version__}")
    tp = sum(k.conj().T @ k for k in branches)
    print(f"kraus_tp_inf_residual={np.max(np.abs(tp-eye)):.3e}")
    j = sum(np.outer(k.reshape(-1, order='F'), k.reshape(-1, order='F').conj()) for k in branches)
    eig = np.linalg.eigvalsh(j)
    print("choi_convention=J=sum_ij |i><j|_in tensor T(|i><j|)_out;vec_F")
    print("choi_eigenvalues=" + np.array2string(eig, precision=15, separator=","))
    print(f"choi_tp_partial_trace_residual={np.max(np.abs(partial_trace_output(j)-eye)):.3e}")
    print(f"choi_rank_tol_1e-12={np.count_nonzero(eig > 1e-12)}")

    r1 = {0: eye, 1: xgate}
    r2_history = {0: eye, 1: xgate}
    hidden_super = np.zeros((4, 4), dtype=complex)
    path_rows = []
    print("history_path_table_begin")
    for x1 in range(4):
        for x2 in range(4):
            b1, b2 = observed[x1], observed[x2]
            a = r2_history[b1] @ branches[x2] @ r1[b1] @ branches[x1]
            amp = np.trace(a)
            sq = abs(amp) ** 2
            path_rows.append((x1, x2, b1, b2, amp, sq))
            hidden_super += L(a)
            print(f"path={x1}{x2};bits={b1}{b2};trace={amp.real:.15g}{amp.imag:+.3g}j;trace_sq={sq:.15g}")
    print("history_path_table_end")
    f_hidden = sum(row[-1] for row in path_rows) / 4.0
    f_liouville = np.trace(hidden_super).real / 4.0
    print(f"F_history_hidden={f_hidden:.15f}")
    print(f"F_history_liouville={f_liouville:.15f}")
    print(f"history_representation_residual={abs(f_hidden-f_liouville):.3e}")

    # Explicitly check a clock-dependent current-bit factorization with four distinct CPTP maps.
    hgate = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2.0)
    rec1 = {0: [eye], 1: [xgate]}
    rec2 = {0: [hgate], 1: [zgate]}
    def rec_super(ks):
        return sum(L(k) for k in ks)
    for label, rec in (("R10", rec1[0]), ("R11", rec1[1]), ("R20", rec2[0]), ("R21", rec2[1])):
        cptp = sum(k.conj().T @ k for k in rec)
        print(f"{label}_CPTP_residual={np.max(np.abs(cptp-eye)):.3e}")
    inst = {b: sum(L(branches[x]) for x in grouping[b]) for b in (0, 1)}
    c1 = sum(rec_super(rec1[b]) @ inst[b] for b in (0, 1))
    c2 = sum(rec_super(rec2[b]) @ inst[b] for b in (0, 1))
    explicit = np.zeros((4, 4), dtype=complex)
    for x1 in range(4):
        for x2 in range(4):
            explicit += rec_super(rec2[observed[x2]]) @ L(branches[x2]) @ rec_super(rec1[observed[x1]]) @ L(branches[x1])
    print(f"time_dependent_factorization_inf_residual={np.max(np.abs(explicit-c2@c1)):.3e}")

    # Independently reconstruct the published input from S1 Eq. (18), not Eq. (20).
    theta = np.pi / 6.0
    phi = np.pi / 4.0
    lx, ly = np.cos(phi-theta), np.cos(phi+theta)
    lz, tz = lx*ly, np.sin(phi-theta)*np.sin(phi+theta)
    I2 = eye.astype(complex)
    def affine_action(a):
        coeff_i = np.trace(a) / 2.0
        coeff_x = np.trace(xgate @ a) / 2.0
        coeff_y = np.trace(ygate @ a) / 2.0
        coeff_z = np.trace(zgate @ a) / 2.0
        return coeff_i*(I2+tz*zgate) + lx*coeff_x*xgate + ly*coeff_y*ygate + lz*coeff_z*zgate
    j_source = choi_from_action(affine_action)
    ew, ev = np.linalg.eigh((j_source+j_source.conj().T)/2)
    source_ks = []
    for idx in np.where(ew > 1e-12)[0]:
        source_ks.append((np.sqrt(ew[idx])*ev[:, idx]).reshape((2, 2), order='F'))
    abs_ks = [sqrt_psd(k.conj().T @ k) for k in source_ks]
    corrected = sum(L(a) for a in abs_ks)
    f_markov = np.trace(corrected @ corrected).real / 4.0
    f_final = 0.0
    for ki in source_ks:
        ai = sqrt_psd(ki.conj().T @ ki)
        for kj in source_ks:
            f_final += np.linalg.svd(kj @ ai, compute_uv=False).sum() ** 2 / 4.0
    target = 3.0/4.0 + np.sqrt(3.0)/8.0
    print("published_source_input=Rexiti_et_al_Eq18_affine_to_Choi")
    print("published_source_choi_eigenvalues=" + np.array2string(ew, precision=15, separator=","))
    print(f"published_source_TP_residual={np.max(np.abs(partial_trace_output(j_source)-eye)):.3e}")
    print(f"published_F2_markov_superop={f_markov:.15f}")
    print(f"published_F2_final_only_singular_values={f_final:.15f}")
    print(f"published_exact_target_float={target:.15f}")

    assert np.max(np.abs(tp-eye)) < 1e-14
    assert np.count_nonzero(eig > 1e-12) == 4
    assert abs(f_hidden - 1831.0/2500.0) < 1e-14
    assert abs(f_hidden-f_liouville) < 1e-14
    assert np.max(np.abs(explicit-c2@c1)) < 1e-14
    assert abs(f_markov-target) < 2e-14
    assert abs(f_final-target) < 2e-14
    print("reconstruction_B_status=PASS")


if __name__ == "__main__":
    main()
