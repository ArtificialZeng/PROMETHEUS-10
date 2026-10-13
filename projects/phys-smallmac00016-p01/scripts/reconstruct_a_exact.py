#!/usr/bin/env python3
"""Exact direct-Kraus reconstruction of the fixed 03|12 GAD baseline."""

import sympy as sp


def liouville(k):
    return sp.kronecker_product(sp.conjugate(k), k)


def main():
    p = sp.Rational(18, 25)
    q = sp.Rational(7, 25)
    gamma = sp.Rational(3, 10)
    s = sp.sqrt(1 - gamma)
    z = sp.Integer(0)
    K = [
        sp.sqrt(p) * sp.diag(1, s),
        sp.sqrt(p * gamma) * sp.Matrix([[0, 1], [0, 0]]),
        sp.sqrt(q) * sp.diag(s, 1),
        sp.sqrt(q * gamma) * sp.Matrix([[0, 0], [1, 0]]),
    ]
    I = sp.eye(2)
    X = sp.Matrix([[0, 1], [1, 0]])
    Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    Z = sp.diag(1, -1)
    groups = {0: (0, 3), 1: (1, 2)}
    bit = {x: b for b, xs in groups.items() for x in xs}

    completeness = sp.simplify(sum((k.H * k for k in K), sp.zeros(2)) - I)
    vec_columns = sp.Matrix.hstack(*[sp.Matrix(k).reshape(4, 1) for k in K])
    print("representation=A/direct exact Kraus transcription")
    print("python_backend=sympy")
    print(f"parameters=p={p};q={q};gamma={gamma};s={s}")
    print("basis=|0>,|1>;rows=output;columns=input")
    print("kraus_completeness=" + str(completeness.tolist()))
    print(f"kraus_linear_rank={vec_columns.rank()}")
    print(f"diagonal_minor_squared={sp.simplify(p*q*gamma**2)}")

    def instrument(b, op):
        return sp.simplify(sum((K[x] * op * K[x].H for x in groups[b]), sp.zeros(2)))

    for label, op in (("X", X), ("Y", Y), ("Z", Z)):
        for b in (0, 1):
            print(f"I{b}({label})={instrument(b, op).tolist()}")

    R1 = {0: I, 1: X}
    R2 = {0: I, 1: X}  # indexed by the retained first bit for this history witness
    total = z
    S_hidden = sp.zeros(4)
    print("history_path_table_begin")
    for x1 in range(4):
        for x2 in range(4):
            b1, b2 = bit[x1], bit[x2]
            A = sp.simplify(R2[b1] * K[x2] * R1[b1] * K[x1])
            amp = sp.simplify(sp.trace(A))
            sq = sp.simplify(amp * sp.conjugate(amp))
            total += sq
            S_hidden += liouville(A)
            print(f"path={x1}{x2};bits={b1}{b2};trace={amp};trace_sq={sq}")
    f_hidden = sp.simplify(total / 4)
    f_liouville = sp.simplify(sp.trace(S_hidden) / 4)
    print("history_path_table_end")
    print(f"F_history_hidden={f_hidden}")
    print(f"F_history_liouville={f_liouville}")
    print(f"F_history_formula={sp.simplify(1-gamma+p*gamma**2/2)}")

    cap_x = s
    cap_y = s
    cap_z = p
    frob_sq = sp.simplify(cap_x**2 + cap_y**2 + cap_z**2)
    f_upper = sp.simplify((1 + frob_sq) / 4)
    print(f"column_caps={cap_x},{cap_y},{cap_z}")
    print(f"frobenius_squared_cap={frob_sq}")
    print(f"F_markov_arbitrary_CPTP_upper={f_upper}")
    print(f"witness_minus_upper={sp.simplify(f_hidden-f_upper)}")

    # Published resolved-record benchmark: S1 Eq. (20), theta=pi/6, phi=pi/4.
    T0 = sp.diag(sp.sqrt(3) / 2, sp.sqrt(2) / 2)
    T1 = sp.Matrix([[0, sp.sqrt(2) / 2], [sp.Rational(1, 2), 0]])
    A0 = T0
    A1 = sp.diag(sp.Rational(1, 2), sp.sqrt(2) / 2)
    abs_ops = (A0, A1)
    f_markov = sp.simplify(sum((sp.trace(abs_ops[j] * abs_ops[i]) ** 2
                                for i in range(2) for j in range(2)), z) / 4)
    f_prop5 = z
    for i in range(2):
        for j in range(2):
            prod = (T0, T1)[j] * (T0, T1)[i]
            trace_abs_sq = sp.simplify(sp.trace(prod.H * prod) + 2 * sp.Abs(sp.det(prod)))
            f_prop5 += trace_abs_sq / 4
    exact = sp.Rational(3, 4) + sp.sqrt(3) / 8
    print("published_source_input=Rexiti_et_al_Eq20_theta_pi6_phi_pi4")
    print(f"published_F2_markov_Eq8={sp.simplify(f_markov)}")
    print(f"published_F2_Gregoratti_Werner_Prop5={sp.simplify(f_prop5)}")
    print(f"published_exact_target={exact}")
    assert completeness == sp.zeros(2)
    assert vec_columns.rank() == 4
    assert f_hidden == sp.Rational(1831, 2500)
    assert f_liouville == f_hidden
    assert f_upper == sp.Rational(456, 625)
    assert sp.simplify(f_markov - exact) == 0
    assert sp.simplify(f_prop5 - exact) == 0
    print("reconstruction_A_status=PASS")


if __name__ == "__main__":
    main()
