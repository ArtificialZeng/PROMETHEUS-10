#!/usr/bin/env python3
"""Post-hoc comparison of independently implemented Poisson and Wick matrices."""

from __future__ import annotations

import numpy as np

from quotient_poisson import diffusion_matrix
from quotient_wick import CASES, wick_matrix


def main():
    largest_absolute = 0.0
    largest_relative = 0.0
    print("COMPARISON=real_polynomial_Poisson_vs_complex_two_time_Wick")
    print("shared_after_generation=physical_SDE,current_basis,parameter_cases_only")
    for parameters in CASES:
        m, gamma, k, temperature, kappa = parameters
        kstar = k - m * kappa**2 / gamma**2
        pd = diffusion_matrix(parameters, True, False)["diffusion"]
        pe = diffusion_matrix(parameters, False, False)["diffusion"]
        wd = wick_matrix(m, gamma, k, temperature, kappa)["matrix"]
        we = wick_matrix(m, gamma, kstar, temperature, 0.0)["matrix"]
        absolute = max(float(np.max(np.abs(pd - wd))), float(np.max(np.abs(pe - we))))
        scale = max(1.0, float(np.max(np.abs(pd))), float(np.max(np.abs(pe))))
        relative = absolute / scale
        largest_absolute = max(largest_absolute, absolute)
        largest_relative = max(largest_relative, relative)
        tolerance = 2e-7 * scale
        assert absolute < tolerance
        print(f"case={parameters},max_absolute_matrix_error={absolute:.17g},relative_to_largest_entry={relative:.17g},tolerance={tolerance:.17g},pass=true")
    print(f"largest_absolute_matrix_error={largest_absolute:.17g}")
    print(f"largest_relative_matrix_error={largest_relative:.17g}")
    print("status=PASS")


if __name__ == "__main__":
    main()
