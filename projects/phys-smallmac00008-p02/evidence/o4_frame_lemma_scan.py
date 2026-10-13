#!/usr/bin/env python3
"""Discovery test for the reduced orthogonal-frame collinearity lemma.

For a triple of arbitrary traceless real-symmetric 4x4 matrices G_r, search for
O in SO(4) such that B[i,r]=(O.T G_r O)[i,i] has rank at most one.  Vanishing
2x2 minors are necessary and sufficient.  This is float64 local optimization,
not a proof or global enclosure.
"""

import argparse
import json

import numpy as np
from scipy.linalg import expm
from scipy.optimize import least_squares


PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]


def exp_coordinates(p):
    a = np.zeros((4, 4))
    for value, (i, j) in zip(p, PAIRS):
        a[i, j], a[j, i] = value, -value
    return expm(a)


def givens_coordinates(p):
    o = np.eye(4)
    for theta, (i, j) in zip(p, PAIRS):
        g = np.eye(4)
        c, s = np.cos(theta), np.sin(theta)
        g[i, i], g[j, j], g[i, j], g[j, i] = c, c, -s, s
        o = o @ g
    return o


def random_triple(seed):
    rng = np.random.default_rng(seed)
    triple = []
    for _ in range(3):
        g = rng.normal(size=(4, 4))
        g = (g + g.T) / 2.0
        g -= np.trace(g) * np.eye(4) / 4.0
        triple.append(g)
    return np.asarray(triple)


def residual(p, triple, coordinates):
    o = coordinates(p)
    b = np.column_stack([np.diag(o.T @ g @ o) for g in triple])
    return np.concatenate([np.cross(b[i], b[j]) for i, j in PAIRS])


def run(seed, starts, max_nfev):
    triple = random_triple(seed)
    rng = np.random.default_rng(seed + 50_000)
    output = {"seed": seed, "input_trace_max_abs": float(np.max(np.abs(np.trace(triple, axis1=1, axis2=2))))}
    for name, coordinates in [("exp", exp_coordinates), ("givens", givens_coordinates)]:
        values = []
        for p0 in [np.zeros(6)] + [rng.uniform(-np.pi, np.pi, 6) for _ in range(starts - 1)]:
            fit = least_squares(
                residual,
                p0,
                args=(triple, coordinates),
                ftol=1e-13,
                xtol=1e-13,
                gtol=1e-13,
                max_nfev=max_nfev,
            )
            values.append(float(np.dot(fit.fun, fit.fun)))
        output[f"{name}_best_squared_minor_residual"] = min(values)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=list(range(9100, 9108)))
    parser.add_argument("--starts", type=int, default=16)
    parser.add_argument("--max-nfev", type=int, default=2000)
    args = parser.parse_args()
    print(json.dumps([run(s, args.starts, args.max_nfev) for s in args.seeds], indent=2))


if __name__ == "__main__":
    main()
