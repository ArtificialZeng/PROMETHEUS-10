#!/usr/bin/env python3
"""Exact adversarial tests for the elementary right-quotient criterion.

All calculations use SymPy exact arithmetic.  The independently constructed
superoperator quotient is compared with both source Eq. (3) and the proposed
congruence reduction.  The frozen ordered pair is a=1, b=0 in dimension three.
"""

from dataclasses import dataclass

import sympy as sp


N = 3
A_LEVEL = 1
B_LEVEL = 0
I3 = sp.eye(N)
H = sp.diag(0, 1, 2)


def dagger(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.conjugate().T


def matrix_unit(row: int, column: int) -> sp.Matrix:
    ans = sp.zeros(N)
    ans[row, column] = 1
    return ans


def vec(matrix: sp.Matrix) -> sp.Matrix:
    """Source column-vectorization: sum_j |j> tensor matrix|j>."""
    return sp.Matrix([matrix[row, column] for column in range(N) for row in range(N)])


def choi(kraus: list[sp.Matrix]) -> sp.Matrix:
    ans = sp.zeros(N * N)
    for operator in kraus:
        vector = vec(operator)
        ans += vector * dagger(vector)
    return sp.simplify(ans)


def superoperator(kraus: list[sp.Matrix]) -> sp.Matrix:
    """Matrix S such that vec(Phi(X)) = S vec(X)."""
    ans = sp.zeros(N * N)
    for operator in kraus:
        ans += sp.kronecker_product(operator.conjugate(), operator)
    return sp.simplify(ans)


def choi_from_superoperator(superop: sp.Matrix) -> sp.Matrix:
    """Independent reshuffle from matrix-unit action to input-first Choi."""
    ans = sp.zeros(N * N)
    for i in range(N):
        for j in range(N):
            input_column = j * N + i
            for alpha in range(N):
                for beta in range(N):
                    output_row = beta * N + alpha
                    ans[i * N + alpha, j * N + beta] = superop[output_row, input_column]
    return ans


def partial_trace_output(ch: sp.Matrix) -> sp.Matrix:
    ans = sp.zeros(N)
    for i in range(N):
        for j in range(N):
            ans[i, j] = sum(ch[i * N + alpha, j * N + alpha] for alpha in range(N))
    return sp.simplify(ans)


def is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def psi_kraus(
    lam: sp.Expr, a_level: int = A_LEVEL, b_level: int = B_LEVEL
) -> list[sp.Matrix]:
    k_op = sp.eye(N)
    k_op[a_level, a_level] = sp.sqrt(1 - lam)
    l_op = sp.sqrt(lam) * matrix_unit(b_level, a_level)
    return [k_op, l_op]


def direct_quotient_choi(
    kraus: list[sp.Matrix],
    lam: sp.Expr,
    a_level: int = A_LEVEL,
    b_level: int = B_LEVEL,
) -> sp.Matrix:
    s_phi = superoperator(kraus)
    s_psi = superoperator(psi_kraus(lam, a_level, b_level))
    return sp.simplify(choi_from_superoperator(s_phi * s_psi.inv()))


def eq3_quotient_choi(
    ch: sp.Matrix,
    lam: sp.Expr,
    a_level: int = A_LEVEL,
    b_level: int = B_LEVEL,
) -> sp.Matrix:
    k_op, l_op = psi_kraus(lam, a_level, b_level)
    d_op = sp.kronecker_product(k_op.inv().T, I3)
    z_l = sp.kronecker_product(l_op.T, I3)
    return sp.simplify(d_op * ch * dagger(d_op) - z_l * ch * dagger(z_l) / (1 - lam))


Z = sp.kronecker_product(matrix_unit(A_LEVEL, B_LEVEL), I3)
Q = sp.kronecker_product(matrix_unit(A_LEVEL, A_LEVEL), I3)
COVARIANCE_GENERATOR = sp.kronecker_product(H.T, I3) - sp.kronecker_product(I3, H)


def reduced_choi(ch: sp.Matrix, lam: sp.Expr) -> sp.Matrix:
    return sp.simplify(ch - lam * Z * ch * dagger(Z))


def congruence_quotient_choi(
    ch: sp.Matrix,
    lam: sp.Expr,
    a_level: int = A_LEVEL,
    b_level: int = B_LEVEL,
) -> sp.Matrix:
    k_op, _ = psi_kraus(lam, a_level, b_level)
    d_op = sp.kronecker_product(k_op.inv().T, I3)
    z_op = sp.kronecker_product(matrix_unit(a_level, b_level), I3)
    reduced = sp.simplify(ch - lam * z_op * ch * dagger(z_op))
    return sp.simplify(d_op * reduced * dagger(d_op))


def tp_residual(kraus: list[sp.Matrix]) -> sp.Matrix:
    return sp.simplify(sum((dagger(k) * k for k in kraus), sp.zeros(N)) - I3)


def inclusion_matrix(vectors: sp.Matrix, operator: sp.Matrix) -> tuple[bool, sp.Matrix | None]:
    transformed = operator * vectors
    included = vectors.row_join(transformed).rank() == vectors.rank()
    if not included:
        return False, None
    left_inverse = (dagger(vectors) * vectors).inv() * dagger(vectors)
    coefficients = sp.simplify(left_inverse * transformed)
    assert is_zero_matrix(vectors * coefficients - transformed)
    return True, coefficients


def classical_kraus(columns: dict[int, list[tuple[int, sp.Rational]]]) -> list[sp.Matrix]:
    operators: list[sp.Matrix] = []
    for input_level in range(N):
        entries = columns[input_level]
        assert sum((probability for _, probability in entries), sp.S.Zero) == 1
        for output_level, probability in entries:
            operators.append(sp.sqrt(probability) * matrix_unit(output_level, input_level))
    return operators


@dataclass(frozen=True)
class Example:
    name: str
    kraus: list[sp.Matrix]
    expected_rank: int
    expected_n: bool
    expected_extra: bool
    expected_threshold: sp.Rational | None


amplitude = [
    sp.diag(1, sp.Rational(1, 2), 1),
    sp.sqrt(3) / 2 * matrix_unit(B_LEVEL, A_LEVEL),
]

coherent_rank3 = [
    sp.diag(1 / sp.sqrt(2), sp.Rational(1, 2), 1 / sp.sqrt(3)),
    sp.diag(1 / sp.sqrt(2), sp.Rational(1, 2), sp.sqrt(sp.Rational(2, 3))),
    1 / sp.sqrt(2) * matrix_unit(B_LEVEL, A_LEVEL),
]

examples = [
    Example("rank2_amplitude_mu_3_over_4", amplitude, 2, True, False, sp.Rational(3, 4)),
    Example("rank3_coherent_zero_gap", coherent_rank3, 3, True, False, sp.Rational(1, 2)),
    Example(
        "rank3_classical",
        classical_kraus({0: [(0, sp.Rational(1))], 1: [(0, sp.Rational(1))], 2: [(2, sp.Rational(1))]}),
        3,
        True,
        True,
        sp.Rational(1),
    ),
    Example(
        "rank4_classical",
        classical_kraus({0: [(0, sp.Rational(1))], 1: [(0, sp.Rational(1, 3)), (1, sp.Rational(2, 3))], 2: [(2, sp.Rational(1))]}),
        4,
        True,
        True,
        sp.Rational(1, 3),
    ),
    Example(
        "rank5_classical",
        classical_kraus({0: [(0, sp.Rational(1))], 1: [(0, sp.Rational(1, 4)), (1, sp.Rational(3, 4))], 2: [(1, sp.Rational(2, 5)), (2, sp.Rational(3, 5))]}),
        5,
        True,
        True,
        sp.Rational(1, 4),
    ),
    Example(
        "rank6_classical",
        classical_kraus({0: [(0, sp.Rational(1))], 1: [(0, sp.Rational(1, 5)), (1, sp.Rational(2, 5)), (2, sp.Rational(2, 5))], 2: [(1, sp.Rational(1, 3)), (2, sp.Rational(2, 3))]}),
        6,
        True,
        True,
        sp.Rational(1, 5),
    ),
    Example(
        "rank7_classical",
        classical_kraus({0: [(0, sp.Rational(1))], 1: [(0, sp.Rational(1, 6)), (1, sp.Rational(1, 3)), (2, sp.Rational(1, 2))], 2: [(0, sp.Rational(1, 5)), (1, sp.Rational(3, 10)), (2, sp.Rational(1, 2))]}),
        7,
        True,
        True,
        sp.Rational(1, 6),
    ),
    Example(
        "rank8_classical",
        classical_kraus({0: [(0, sp.Rational(2, 5)), (1, sp.Rational(3, 5))], 1: [(0, sp.Rational(1, 10)), (1, sp.Rational(1, 5)), (2, sp.Rational(7, 10))], 2: [(0, sp.Rational(1, 6)), (1, sp.Rational(1, 3)), (2, sp.Rational(1, 2))]}),
        8,
        True,
        True,
        sp.Rational(1, 4),
    ),
    Example(
        "rank3_dephasing_N_failure",
        classical_kraus({0: [(0, sp.Rational(1))], 1: [(1, sp.Rational(1))], 2: [(2, sp.Rational(1))]}),
        3,
        False,
        True,
        None,
    ),
]


def sorted_exact_eigenvalues(matrix: sp.Matrix) -> list[sp.Expr]:
    values: list[sp.Expr] = []
    for value, multiplicity in matrix.eigenvals().items():
        values.extend([sp.simplify(value)] * multiplicity)
    return sorted(values, key=lambda value: float(sp.N(value, 30)))


def check_example(example: Example) -> None:
    ch = choi(example.kraus)
    vectors = sp.Matrix.hstack(*(vec(k) for k in example.kraus))

    assert is_zero_matrix(tp_residual(example.kraus))
    assert partial_trace_output(ch) == I3
    assert ch.rank() == example.expected_rank
    assert vectors.rank() == example.expected_rank
    assert is_zero_matrix(COVARIANCE_GENERATOR * ch - ch * COVARIANCE_GENERATOR)

    n_holds, a_matrix = inclusion_matrix(vectors, Z)
    extra_holds, _ = inclusion_matrix(vectors, Q)
    assert n_holds == example.expected_n
    assert extra_holds == example.expected_extra

    if n_holds:
        assert a_matrix is not None
        aa_dagger = sp.simplify(a_matrix * dagger(a_matrix))
        eigenvalues = sorted_exact_eigenvalues(aa_dagger)
        max_eigenvalue = eigenvalues[-1]
        threshold = sp.simplify(1 / max_eigenvalue)
        assert threshold == example.expected_threshold
        assert is_zero_matrix(reduced_choi(ch, sp.Symbol("lambda")) - vectors * (sp.eye(example.expected_rank) - sp.Symbol("lambda") * aa_dagger) * dagger(vectors))

        lam_inside = threshold / 2
        q_direct = direct_quotient_choi(example.kraus, lam_inside)
        q_eq3 = eq3_quotient_choi(ch, lam_inside)
        q_congruence = congruence_quotient_choi(ch, lam_inside)
        assert is_zero_matrix(q_direct - q_eq3)
        assert is_zero_matrix(q_eq3 - q_congruence)
        assert partial_trace_output(q_direct) == I3

        reduced_inside_eigs = sorted_exact_eigenvalues(sp.eye(example.expected_rank) - lam_inside * aa_dagger)
        assert all(value > 0 for value in reduced_inside_eigs)
        endpoint_eigs = sorted_exact_eigenvalues(sp.eye(example.expected_rank) - threshold * aa_dagger)
        assert endpoint_eigs[0] == 0
        assert all(value >= 0 for value in endpoint_eigs)

        if threshold < 1:
            lam_outside = (threshold + 1) / 2
            outside_eigs = sorted_exact_eigenvalues(sp.eye(example.expected_rank) - lam_outside * aa_dagger)
            assert outside_eigs[0] < 0
            outside_status = f"outside_lambda={lam_outside}, negative_reduced_eigenvalue={outside_eigs[0]}"
        else:
            outside_status = "threshold=1, so every inverse-domain lambda in [0,1) is CP"

        print(
            f"PASS {example.name}: CPTP,covariant,rank={ch.rank()},N=true,"
            f"extra={str(extra_holds).lower()},lambda_max={threshold}; "
            f"direct=Eq3=congruence at lambda={lam_inside}; {outside_status}"
        )
    else:
        lam = sp.Rational(1, 10)
        b_matrix = sp.simplify(Z * ch * dagger(Z))
        kernel = sp.Matrix.hstack(*ch.nullspace())
        compressed = sp.simplify(dagger(kernel) * b_matrix * kernel)
        assert compressed.rank() > 0
        assert any(value > 0 for value in sorted_exact_eigenvalues(compressed))
        q_direct = direct_quotient_choi(example.kraus, lam)
        q_eq3 = eq3_quotient_choi(ch, lam)
        q_congruence = congruence_quotient_choi(ch, lam)
        assert is_zero_matrix(q_direct - q_eq3)
        assert is_zero_matrix(q_eq3 - q_congruence)
        reduced_kernel_block = sp.simplify(dagger(kernel) * reduced_choi(ch, lam) * kernel)
        assert any(value < 0 for value in sorted_exact_eigenvalues(reduced_kernel_block))
        print(
            f"PASS {example.name}: CPTP,covariant,rank={ch.rank()},N=false; "
            f"kernel-compressed ZCZ* rank={compressed.rank()}, quotient indefinite for every lambda>0; "
            f"direct=Eq3=congruence checked at lambda={lam}"
        )


def check_all_ordered_pairs() -> None:
    """Exercise the exact nonclassical rank-two test for all six energy pairs."""
    lam = sp.Rational(3, 8)
    for a_level in range(N):
        for b_level in range(N):
            if a_level == b_level:
                continue
            k_op = sp.eye(N)
            k_op[a_level, a_level] = sp.Rational(1, 2)
            l_op = sp.sqrt(3) / 2 * matrix_unit(b_level, a_level)
            kraus = [k_op, l_op]
            ch = choi(kraus)
            vectors = sp.Matrix.hstack(*(vec(k) for k in kraus))
            z_op = sp.kronecker_product(matrix_unit(a_level, b_level), I3)
            q_op = sp.kronecker_product(matrix_unit(a_level, a_level), I3)

            n_holds, a_matrix = inclusion_matrix(vectors, z_op)
            extra_holds, _ = inclusion_matrix(vectors, q_op)
            assert n_holds and not extra_holds and a_matrix is not None
            assert sorted_exact_eigenvalues(a_matrix * dagger(a_matrix))[-1] == sp.Rational(4, 3)
            assert is_zero_matrix(COVARIANCE_GENERATOR * ch - ch * COVARIANCE_GENERATOR)
            q_direct = direct_quotient_choi(kraus, lam, a_level, b_level)
            q_eq3 = eq3_quotient_choi(ch, lam, a_level, b_level)
            q_congruence = congruence_quotient_choi(ch, lam, a_level, b_level)
            assert is_zero_matrix(q_direct - q_eq3)
            assert is_zero_matrix(q_eq3 - q_congruence)
            assert partial_trace_output(q_direct) == I3
            print(
                f"PASS ordered_pair a={a_level},b={b_level}: rank=2,N=true,extra=false,"
                f"lambda_max=3/4; direct=Eq3=congruence at lambda={lam}"
            )


def main() -> None:
    print("Exact arithmetic: SymPy", sp.__version__)
    print("Ordered energy-level pair: a=1, b=0; H=diag(0,1,2)")
    print("Reduction checked: C(Phi Psi_lambda^-1)=D_lambda[C-lambda Z C Z*]D_lambda*")
    for example in examples:
        check_example(example)
    check_all_ordered_pairs()
    print(
        f"ALL_PASS examples={len(examples)} ranks_covered=2,3,4,5,6,7,8 "
        "ordered_pairs_covered=6"
    )


if __name__ == "__main__":
    main()
