"""Independent finite-box perturbation diagnostic for the weak-feedback formula.

The analytic infinite-state coefficient is evaluated from a Poisson autocovariance
series. The sparse reflected generator and its first stationary derivative are
constructed separately. Finite-box results are diagnostics, not certifications.
"""

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


TAU = np.array([1., 2., 1.5])
A = np.array([1., 0.5, 2. / 3.])
LAM = TAU * A
KIND = ("zero", "parity", "zero")


def h(i, n):
    if KIND[i] == "zero":
        return float(n == 0)
    return float(1 if n % 2 == 0 else -1)


def autocov_series(i, terms=70):
    """Closed bivariate-Poisson series, independent of the sparse generator."""
    j = (i - 1) % 3
    lam = LAM[j]
    scale = 1. if KIND[i] == "zero" else 4.
    prefactor = math.exp(-2. * lam) if KIND[i] == "zero" else math.exp(-4. * lam)
    # Cov(h(Y_0),h(Y_t))=prefactor*(exp(scale*lam*exp(-t/tau_j))-1).
    total = 0.
    term = 1.
    for k in range(1, terms + 1):
        term *= scale * lam / k
        total += term / (1. / TAU[i] + k / TAU[j])
    return prefactor * total


def remainder_bound(i):
    """Crude explicit uniform K with |F_i-1-eps^2*S_i/a_i| <= K*|eps|^3."""
    j = (i - 1) % 3
    gamma = 1. / TAU
    norm_b2 = 2. / (gamma[i] + gamma[j])
    const_part = 4. * TAU[i] * TAU[j] + norm_b2 * TAU[i]
    linear_part = 2. * norm_b2 * sum(1. / (gamma[i] + gamma[k])
                                         for k in range(3) if k != i)
    m_bound = const_part + linear_part * 2.5 * LAM[i]
    centering_bound = 2. * TAU[i] * TAU[j]
    s = autocov_series(i)
    k = 2. * s / (A[i] ** 2) + 2. * (m_bound + centering_bound) / A[i]
    return dict(K=float(k), sufficient_epsilon_upper=float(s / (A[i] * k)),
                const_part=float(const_part), linear_part=float(linear_part),
                M=float(m_bound), centering_bound=float(centering_bound))


def generator(n):
    states = np.array(list(itertools.product(range(n + 1), repeat=3)), dtype=np.int32)
    shape = (n + 1,) * 3
    rows0, cols0, data0 = [], [], []
    rows1, cols1, data1 = [], [], []
    for col, x in enumerate(states):
        d0 = d1 = 0.
        for i in range(3):
            if x[i] < n:
                y = x.copy()
                y[i] += 1
                row = np.ravel_multi_index(y, shape)
                rows0.append(row); cols0.append(col); data0.append(A[i])
                v = h(i, x[(i - 1) % 3])
                rows1.append(row); cols1.append(col); data1.append(v)
                d0 += A[i]; d1 += v
            if x[i]:
                y = x.copy()
                y[i] -= 1
                row = np.ravel_multi_index(y, shape)
                v = x[i] / TAU[i]
                rows0.append(row); cols0.append(col); data0.append(v)
                d0 += v
        rows0.append(col); cols0.append(col); data0.append(-d0)
        rows1.append(col); cols1.append(col); data1.append(-d1)
    size = len(states)
    q0 = coo_matrix((data0, (rows0, cols0)), shape=(size, size)).tocsc()
    q1 = coo_matrix((data1, (rows1, cols1)), shape=(size, size)).tocsc()
    return states, q0, q1


def solve(n):
    states, q0, q1 = generator(n)
    mat = q0.tolil()
    mat[0, :] = np.ones(len(states))
    mat = mat.tocsc()
    rhs = np.zeros(len(states)); rhs[0] = 1.
    p0 = spsolve(mat, rhs)
    rhs1 = -(q1 @ p0); rhs1[0] = 0.
    p1 = spsolve(mat, rhs1)
    finite_fano = []
    for eps in (0.02, 0.01, 0.005, 0.0005):
        qe = q0 + eps * q1
        me = qe.tolil(); me[0, :] = np.ones(len(states))
        pe = spsolve(me.tocsc(), rhs)
        m = pe @ states.astype(float)
        s = pe @ (states.astype(float) ** 2)
        f = (s - m * m) / m
        finite_fano.append(dict(epsilon=eps, F=f.tolist(),
                                excess_over_epsilon2=((f - 1.) / eps**2).tolist(),
                                residual=float(np.max(np.abs(qe @ pe)))))
    out = []
    for i in range(3):
        j = (i - 1) % 3
        x = states[:, i].astype(float)
        y = np.array([h(i, z) for z in states[:, j]])
        mx, my = p0 @ x, p0 @ y
        c1 = p1 @ ((x - mx) * (y - my))
        out.append(dict(i=i+1, c1=float(c1), exact_infinite_S=autocov_series(i),
                        relative_error=float(c1 / autocov_series(i) - 1.),
                        coefficient_F=float(autocov_series(i) / A[i])))
    return dict(cap=n, baseline_mean=(p0 @ states).tolist(),
                baseline_probability_residual=float(np.max(np.abs(q0 @ p0))),
                response_probability_residual=float(np.max(np.abs(q0 @ p1 + q1 @ p0))),
                response_mass=float(sum(p1)), values=out,
                finite_fano_diagnostics=finite_fano)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--caps", type=int, nargs="+", default=[8, 10, 12, 14])
    ap.add_argument("--out", default="evidence/weak-feedback-check.json")
    args = ap.parse_args()
    result = dict(model="f_i=a_i+epsilon*h_i(predecessor); legal for 0<epsilon<1/2",
                  a=A.tolist(), tau=TAU.tolist(), lambda0=LAM.tolist(),
                  h=list(KIND), method="Sparse reflected-generator stationary derivative; comparison to independent infinite Poisson autocovariance series. Finite-box values alone are not infinite-state certificates.",
                  uniform_remainder_bounds=[remainder_bound(i) for i in range(3)],
                  cases=[solve(n) for n in args.caps])
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
