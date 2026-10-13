#!/usr/bin/env python3
"""Direct-matrix, SVD-polar, recovered-Kraus and Choi/Bell replay of Example 8."""
import json
import numpy as np

tol = 2.0e-12
rt3 = np.sqrt(3.0)
I2 = np.eye(2, dtype=complex)
T = [
    np.array([[rt3 / 2, 0], [0, 0]], dtype=complex),
    np.array([[0, rt3 / 2], [0, 0]], dtype=complex),
    np.array([[0.5, 0], [0, 0.5]], dtype=complex),
]
U = np.array([[rt3 / 2, 0, -0.5], [0, 1, 0], [0.5, 0, rt3 / 2]], dtype=complex)
K = [sum((U[i, a] * T[a] for a in range(3)), start=np.zeros((2, 2), complex)) for i in range(3)]

def pos_sqrt(h):
    w, v = np.linalg.eigh((h + h.conj().T) / 2)
    if np.min(w) < -tol:
        raise AssertionError(f"non-positive Gram matrix: {w}")
    return (v * np.sqrt(np.maximum(w, 0.0))) @ v.conj().T

def correction_and_abs(x):
    # Full SVD supplies a unitary extension on every null space.
    u, s, vh = np.linalg.svd(x, full_matrices=True)
    polar_u = u @ vh
    correction = polar_u.conj().T
    return correction, correction @ x, s

def choi(kraus):
    j = np.zeros((4, 4), dtype=complex)
    for x in kraus:
        vx = x.reshape(4, order="F")
        j += np.outer(vx, vx.conj())
    return j

def channel_checks(kraus):
    tp = sum((x.conj().T @ x for x in kraus), start=np.zeros((2, 2), complex))
    j = choi(kraus)
    return {
        "tp_residual_inf": float(np.max(np.abs(tp - I2))),
        "choi_min_eigenvalue": float(np.min(np.linalg.eigvalsh((j + j.conj().T) / 2))),
        "choi_rank_tol_1e-12": int(np.count_nonzero(np.linalg.eigvalsh((j + j.conj().T) / 2) > 1e-12)),
    }

def bell_fidelity(kraus):
    bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    # (I tensor E)(Phi)=J_E/2 for the input-tensor-output Choi convention.
    return float(np.real(bell.conj() @ choi(kraus) @ bell) / 2)

A = [pos_sqrt(x.conj().T @ x) for x in K]
R1, effective1, singular_values = [], [], []
for x in K:
    r, ax, s = correction_and_abs(x)
    R1.append(r)
    effective1.append(ax)
    singular_values.append(s)

markov, bayes, branches = [], [], []
for i in range(3):
    for j in range(3):
        m = R1[j] @ K[j] @ effective1[i]
        x = K[j] @ effective1[i]
        rb, b, s = correction_and_abs(x)
        markov.append(m)
        bayes.append(b)
        branches.append({
            "i": i + 1,
            "j": j + 1,
            "pre_recovery_rank": int(np.linalg.matrix_rank(x, tol=1e-12)),
            "pre_recovery_frobenius_norm": float(np.linalg.norm(x)),
            "bayes_correction_unitarity_residual": float(np.max(np.abs(rb.conj().T @ rb - I2))),
            "markov_trace": float(np.real(np.trace(m))),
            "bayes_abs_trace": float(np.real(np.trace(b))),
        })

raw_f1 = 0.25 * sum(abs(np.trace(pos_sqrt(x.conj().T @ x))) ** 2 for x in T)
checks = {
    "source_channel": channel_checks(T),
    "mixed_channel": channel_checks(K),
    "one_step_recovered": channel_checks(effective1),
    "two_step_markov": channel_checks(markov),
    "two_step_bayes": channel_checks(bayes),
}
result = {
    "method": "direct matrices; Hermitian eigensolver for positive parts; full-SVD null-space unitary extension; recovered Kraus Choi/Bell evaluation",
    "float64_tolerance": tol,
    "u_unitarity_residual_inf": float(np.max(np.abs(U.conj().T @ U - np.eye(3)))),
    "mixed_kraus": [[[[float(z.real), float(z.imag)] for z in row] for row in x] for x in K],
    "positive_part_commutators_max_frobenius": float(max(np.linalg.norm(A[i] @ A[j] - A[j] @ A[i]) for i in range(3) for j in range(3))),
    "polar_reconstruction_residual_max": float(max(np.max(np.abs(effective1[i] - A[i])) for i in range(3))),
    "first_step_singular_branch_count": int(sum(np.min(s) < 1e-12 for s in singular_values)),
    "two_step_branch_count": len(branches),
    "zero_two_step_branches": int(sum(b["pre_recovery_frobenius_norm"] < 1e-12 for b in branches)),
    "branches": branches,
    "raw_eq35_F1_control": float(raw_f1),
    "optimized_F1_choi_bell": bell_fidelity(effective1),
    "F2_markov_choi_bell": bell_fidelity(markov),
    "F2_bayes_choi_bell": bell_fidelity(bayes),
    "checks": checks,
}

assert result["u_unitarity_residual_inf"] < tol
assert result["polar_reconstruction_residual_max"] < tol
assert result["first_step_singular_branch_count"] >= 1
assert result["two_step_branch_count"] == 9 and result["zero_two_step_branches"] == 0
assert abs(result["raw_eq35_F1_control"] - 5 / 8) < tol
assert abs(result["optimized_F1_choi_bell"] - 3 / 4) < tol
assert abs(result["F2_markov_choi_bell"] - 5 / 8) < tol
assert abs(result["F2_bayes_choi_bell"] - 5 / 8) < tol
for c in checks.values():
    assert c["tp_residual_inf"] < tol and c["choi_min_eigenvalue"] > -tol
print(json.dumps(result, indent=2, sort_keys=True))
