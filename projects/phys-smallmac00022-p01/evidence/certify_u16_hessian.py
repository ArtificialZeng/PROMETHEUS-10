#!/usr/bin/env python3
"""Rigorous analytic Hessian certificate for the minimal (4,4) flag split.

At r=1/2 the canonical two-copy coefficient matrix has rank four.  This
program constructs an exact orthonormal 81-vector slice of the 112-dimensional
first-order rank-preserving tangent, after removing the 31-dimensional
U(4) x U(4) local-ancilla orbit.  It evaluates the analytic entropy Hessian
with python-flint Arb ball arithmetic and certifies H - 159/1000 I positive
definite by an interval LDL^T factorization.  This shifted positive-
definiteness certificate is itself a rigorous lower eigenvalue bound.

No finite differences, fitted error bars, or binary64 values enter the
certificate.  The formulas use the four positive eigenvalues of rho_AA' and
include the off-support eigenvector-motion term explicitly.
"""

from __future__ import annotations

import hashlib
import os
import platform
import sys
from pathlib import Path

import flint
import numpy as np
from flint import acb, acb_mat, arb, arb_mat, ctx


BITS = int(os.environ.get("U16_ARB_BITS", "320"))
ctx.prec = BITS

DIM = 16
ACTIVE = [0, 5, 10, 15]
NORMAL = [i for i in range(DIM) if i not in ACTIVE]
ZERO = acb(0)
ONE = arb(1)
IUNIT = acb(0, 1)


def dagger(a: acb_mat) -> acb_mat:
    return a.conjugate().transpose()


def zero_matrix(rows: int = DIM, cols: int = DIM) -> acb_mat:
    return acb_mat(rows, cols)


def submatrix(a: acb_mat, rows: list[int], cols: list[int]) -> acb_mat:
    return acb_mat([[a[i, j] for j in cols] for i in rows])


def abs_square(z: acb) -> arb:
    return z.real * z.real + z.imag * z.imag


def max_radius(a: arb_mat) -> arb:
    answer = arb(0)
    for x in a.entries():
        if x.rad() > answer:
            answer = x.rad()
    return answer


# C1=[[1,2],[2,2]]/sqrt(13), and C=C1 tensor C1.
sqrt13 = arb(13).sqrt()
c1 = [[ONE / sqrt13, arb(2) / sqrt13],
      [arb(2) / sqrt13, arb(2) / sqrt13]]
C = [[c1[i // 2][j // 2] * c1[i % 2][j % 2]
      for j in range(4)] for i in range(4)]


def coefficient_matrix(w: acb_mat) -> acb_mat:
    """Return M(W)_(I,a),(J,b)=C_(I,J) W_(a,b),(I,J)."""
    m = zero_matrix()
    for ii in range(4):
        for aa in range(4):
            row = 4 * ii + aa
            for jj in range(4):
                branch = 4 * ii + jj
                cij = C[ii][jj]
                for bb in range(4):
                    col = 4 * jj + bb
                    m[row, col] = cij * w[4 * aa + bb, branch]
    return m


IDENTITY = acb_mat(DIM, DIM)
for index in range(DIM):
    IDENTITY[index, index] = 1
M0 = coefficient_matrix(IDENTITY)
M0H = dagger(M0)


# Exact eigenbasis of R1=[[5,6],[6,8]]/13.  The columns are v_- and
# v_+, proportional to (4,1-sqrt(17)) and (4,1+sqrt(17)).
sqrt17 = arb(17).sqrt()
norm_minus = (arb(34) - arb(2) * sqrt17).sqrt()
norm_plus = (arb(34) + arb(2) * sqrt17).sqrt()
u1 = [[arb(4) / norm_minus, arb(4) / norm_plus],
      [(ONE - sqrt17) / norm_minus, (ONE + sqrt17) / norm_plus]]

U = acb_mat(4, 4)
for i1 in range(2):
    for i2 in range(2):
        row = 2 * i1 + i2
        for a1 in range(2):
            for a2 in range(2):
                col = 2 * a1 + a2
                U[row, col] = u1[i1][a1] * u1[i2][a2]
UH = dagger(U)

lam_minus = (arb(13) - arb(3) * sqrt17) / arb(26)
lam_plus = (arb(13) + arb(3) * sqrt17) / arb(26)
LAM = [lam_minus * lam_minus,
       lam_minus * lam_plus,
       lam_minus * lam_plus,
       lam_plus * lam_plus]
LAM_CLASS = [0, 1, 1, 2]
LN2 = arb(2).log()
FPRIME = [-(x.log() + ONE) / LN2 for x in LAM]

DIVIDED = [[arb(0) for _ in range(4)] for _ in range(4)]
for i in range(4):
    for j in range(4):
        if LAM_CLASS[i] == LAM_CLASS[j]:
            DIVIDED[i][j] = -ONE / (LAM[i] * LN2)
        else:
            DIVIDED[i][j] = ((FPRIME[i] - FPRIME[j]) /
                              (LAM[i] - LAM[j]))


def helmert_contrasts() -> list[list[arb]]:
    """An exact orthonormal basis of (1,1,1,1)^perp."""
    sqrt2 = arb(2).sqrt()
    sqrt6 = arb(6).sqrt()
    sqrt12 = arb(12).sqrt()
    return [
        [ONE / sqrt2, -ONE / sqrt2, arb(0), arb(0)],
        [ONE / sqrt6, ONE / sqrt6, -arb(2) / sqrt6, arb(0)],
        [ONE / sqrt12, ONE / sqrt12, ONE / sqrt12,
         -arb(3) / sqrt12],
    ]


HELMERT = helmert_contrasts()


def quotient_basis() -> tuple[list[acb_mat], list[str]]:
    """Build the exact 9+36+36 local-gauge-orthogonal tangent basis."""
    basis: list[acb_mat] = []
    labels: list[str] = []

    # Nonfactorizable phase tables h_p h_q^T: 9 dimensions.
    for p, hp in enumerate(HELMERT):
        for q, hq in enumerate(HELMERT):
            k = zero_matrix()
            for ii in range(4):
                for jj in range(4):
                    x = 4 * ii + jj
                    k[x, x] = IUNIT * hp[ii] * hq[jj]
            basis.append(k)
            labels.append(f"phase-h{p}-h{q}")

    sqrt2 = arb(2).sqrt()

    # Edges sharing I.  For each unordered J edge and real/imaginary
    # generator, contrast its four copies across I: 6*2*3=36 dimensions.
    for j0 in range(4):
        for j1 in range(j0 + 1, 4):
            for imaginary in (False, True):
                for p, hp in enumerate(HELMERT):
                    k = zero_matrix()
                    for ii in range(4):
                        x = 4 * ii + j0
                        y = 4 * ii + j1
                        value = hp[ii] / sqrt2
                        if imaginary:
                            k[y, x] = IUNIT * value
                            k[x, y] = IUNIT * value
                        else:
                            k[y, x] = value
                            k[x, y] = -value
                    basis.append(k)
                    kind = "imag" if imaginary else "real"
                    labels.append(f"same-I-{kind}-J{j0}{j1}-h{p}")

    # Edges sharing J, contrasted across the four J copies: another 36.
    for i0 in range(4):
        for i1 in range(i0 + 1, 4):
            for imaginary in (False, True):
                for p, hp in enumerate(HELMERT):
                    k = zero_matrix()
                    for jj in range(4):
                        x = 4 * i0 + jj
                        y = 4 * i1 + jj
                        value = hp[jj] / sqrt2
                        if imaginary:
                            k[y, x] = IUNIT * value
                            k[x, y] = IUNIT * value
                        else:
                            k[y, x] = value
                            k[x, y] = -value
                    basis.append(k)
                    kind = "imag" if imaginary else "real"
                    labels.append(f"same-J-{kind}-I{i0}{i1}-h{p}")

    return basis, labels


BASIS, LABELS = quotient_basis()


def entropy_curvature(k: acb_mat) -> arb:
    """Analytic second derivative of the four-large-weight entropy.

    For rho(t)=rho0+t rho1+t^2 rho2/2+..., the formula is

      sum_a f'(la) (rho2)_aa
      + sum_ab f'[la,lb] |(rho1)_ab|^2
      + 2 sum_na f'(la)/la |(rho1)_na|^2.

    The last term is the positive-eigenvalue motion caused by coupling to
    the zero eigenspace.  The zero eigenvalues have vanishing t^2
    coefficient for the first-order rank-preserving tangent.
    """
    m1 = coefficient_matrix(k)
    m2 = coefficient_matrix(k * k)
    rho1 = m1 * M0H + M0 * dagger(m1)
    rho2 = m2 * M0H + M0 * dagger(m2) + arb(2) * (m1 * dagger(m1))

    x = UH * submatrix(rho1, ACTIVE, ACTIVE) * U
    z = UH * submatrix(rho2, ACTIVE, ACTIVE) * U
    y = submatrix(rho1, NORMAL, ACTIVE) * U

    answer = arb(0)
    for a in range(4):
        answer += FPRIME[a] * z[a, a].real
    for a in range(4):
        for b in range(4):
            answer += DIVIDED[a][b] * abs_square(x[a, b])
    for a in range(4):
        column_norm = sum((abs_square(y[n, a]) for n in range(12)), arb(0))
        answer += arb(2) * FPRIME[a] * column_norm / LAM[a]
    return answer


def analytic_hessian() -> arb_mat:
    n = len(BASIS)
    diagonal = [entropy_curvature(k) for k in BASIS]
    h = arb_mat(n, n)
    for i in range(n):
        h[i, i] = diagonal[i]
        for j in range(i):
            cross = ((entropy_curvature(BASIS[i] + BASIS[j])
                      - diagonal[i] - diagonal[j]) / arb(2))
            h[i, j] = cross
            h[j, i] = cross
        if (i + 1) % 10 == 0 or i + 1 == n:
            print(f"hessian_rows_completed={i + 1}/{n}", flush=True)
    return h


def interval_ldl_positive(a: arb_mat) -> tuple[list[arb], arb_mat, arb]:
    """Outward-rounded no-pivot LDL^T; every positive pivot is a proof."""
    n = a.nrows()
    lower = [[arb(0) for _ in range(n)] for _ in range(n)]
    pivots: list[arb] = []
    minimum_lower = None
    for i in range(n):
        lower[i][i] = ONE
        pivot = a[i, i]
        for k in range(i):
            pivot -= lower[i][k] * lower[i][k] * pivots[k]
        if not pivot > 0:
            raise ArithmeticError(
                f"LDL pivot {i} is not certified positive: {pivot.str(30)}"
            )
        pivots.append(pivot)
        endpoint = pivot.lower()
        if minimum_lower is None or endpoint < minimum_lower:
            minimum_lower = endpoint
        for j in range(i + 1, n):
            value = a[j, i]
            for k in range(i):
                value -= lower[j][k] * lower[i][k] * pivots[k]
            lower[j][i] = value / pivot
    assert minimum_lower is not None
    return pivots, arb_mat(lower), minimum_lower


def verify_basis() -> None:
    if len(BASIS) != 81:
        raise AssertionError(f"wrong quotient dimension: {len(BASIS)}")
    gram = arb_mat(81, 81)
    anti_ok = True
    for i, ki in enumerate(BASIS):
        anti = ki + dagger(ki)
        anti_ok = anti_ok and anti.contains(zero_matrix())
        for j in range(i + 1):
            product = dagger(BASIS[j]) * ki
            value = product.trace().real
            gram[i, j] = value
            gram[j, i] = value
    identity = arb_mat(81, 81)
    for i in range(81):
        identity[i, i] = 1
    if not gram.contains(identity):
        raise AssertionError("quotient basis Gram enclosure misses identity")
    if not anti_ok:
        raise AssertionError("anti-Hermitian basis check failed")

    # Phase tables have zero row and column sums.  Rook contrasts have zero
    # coefficient sum across the copies of their local ancillary generator;
    # these are exactly the 31 orbit-orthogonality conditions.
    for h in HELMERT:
        if not sum(h, arb(0)).contains(0):
            raise AssertionError("Helmert vector is not orthogonal to ones")
    print("basis dimension=81 phase=9 same_I=36 same_J=36 "
          "orthonormal_enclosure=true antihermitian=true "
          "local_gauge_orthogonal=true")


def verify_eigenbasis() -> None:
    rho_active = submatrix(M0 * M0H, ACTIVE, ACTIVE)
    diagonalized = UH * rho_active * U
    target = acb_mat(4, 4)
    for i, value in enumerate(LAM):
        target[i, i] = value
    if not diagonalized.contains(target) or not target.contains(diagonalized):
        # Mutual containment is stronger than needed, but is normally true for
        # these two independently assembled exact ball expressions.
        difference = diagonalized - target
        if not difference.contains(acb_mat(4, 4)):
            raise AssertionError("active eigenbasis check failed")
    unitary_residual = UH * U - acb_mat([[1 if i == j else 0
                                         for j in range(4)] for i in range(4)])
    if not unitary_residual.contains(acb_mat(4, 4)):
        raise AssertionError("eigenbasis orthonormality check failed")
    print("active_spectrum=" + ",".join(x.str(24) for x in LAM))
    print("active_eigenbasis_exact_enclosure=true")


def verify_opening_map() -> None:
    """Certify injectivity and the exact least squared singular scale.

    Each unordered grid edge whose two coordinates both change maps to two
    unique normal-normal entries.  Its normalized real and imaginary
    generators are orthogonal and both have squared image norm
    (C_x^2+C_y^2)/2.  The 72 disjoint entry pairs therefore give 144
    orthogonal real image vectors.
    """
    entry_pairs: set[frozenset[tuple[int, int]]] = set()
    norms: list[arb] = []
    for x in range(16):
        ii, jj = divmod(x, 4)
        for y in range(x + 1, 16):
            aa, bb = divmod(y, 4)
            if ii == aa or jj == bb:
                continue
            support = frozenset(((4 * ii + aa, 4 * jj + bb),
                                 (4 * aa + ii, 4 * bb + jj)))
            if support in entry_pairs:
                raise AssertionError("opening-map image supports collide")
            entry_pairs.add(support)
            norms.append((C[ii][jj] * C[ii][jj]
                          + C[aa][bb] * C[aa][bb]) / arb(2))
    if len(entry_pairs) != 72 or len(set().union(*entry_pairs)) != 144:
        raise AssertionError("opening-map support count is wrong")
    minimum = norms[0]
    for value in norms[1:]:
        if value < minimum:
            minimum = value
    exact_target = arb(5) / arb(338)
    if not minimum.contains(exact_target):
        raise AssertionError("opening-map least norm misses 5/338")
    print("opening_linear_map real_dimension=144 injective=true "
          "orthogonal_image_basis=true "
          f"least_squared_scale={minimum.str(30)} exact_value=5/338")


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    source_hash = hashlib.sha256((project / "source.md").read_bytes()).hexdigest()
    print(f"python={platform.python_version()} executable={sys.executable}")
    print(f"python_flint={flint.__version__} arb_bits={BITS}")
    print(f"source_sha256={source_hash}")
    verify_basis()
    verify_eigenbasis()
    verify_opening_map()

    h = analytic_hessian()
    print(f"hessian_dimension={h.nrows()} max_entry_radius={max_radius(h).str(8)}")

    threshold = arb(159) / arb(1000)
    shifted = arb_mat(h)
    for i in range(81):
        shifted[i, i] -= threshold
    pivots, lower, minimum_pivot_lower = interval_ldl_positive(shifted)
    diagonal = arb_mat(81, 81)
    for i, pivot in enumerate(pivots):
        diagonal[i, i] = pivot
    reconstruction_residual = lower * diagonal * lower.transpose() - shifted
    if not reconstruction_residual.contains(arb_mat(81, 81)):
        raise ArithmeticError("interval LDL reconstruction misses zero")
    print("interval_ldl_shift=159/1000 all_pivots_positive=true "
          f"pivot_count={len(pivots)} "
          f"minimum_pivot_lower={minimum_pivot_lower.str(24)}")
    print("interval_ldl_reconstruction_zero_enclosed=true "
          f"max_residual_radius={max_radius(reconstruction_residual).str(8)}")

    # Midpoint diagonalization is only a diagnostic and is not used by the
    # certificate.  Exact degeneracies make the generic verified eigensolver
    # unnecessarily fragile; shifted interval LDL already proves the claimed
    # lower eigenvalue bound by Sylvester's criterion.
    midpoint = np.array([[float(h[i, j].mid()) for j in range(81)]
                         for i in range(81)])
    approximate = np.linalg.eigvalsh(midpoint)
    print("binary64_midpoint_eigensolver=diagnostic_not_certificate")
    print(f"midpoint_lambda_min={approximate[0]:.15f}")
    print(f"midpoint_lambda_max={approximate[-1]:.15f}")
    print("rigorous_conclusion=lambda_min_gt_159_over_1000")
    print("certificate=PASS")


if __name__ == "__main__":
    main()
