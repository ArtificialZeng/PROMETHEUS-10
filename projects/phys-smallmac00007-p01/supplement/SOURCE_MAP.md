# Scientific source map

External literature defines the problem and prior methods. The counterexample
and its numerical certificates are results of this manuscript.

1. Jones, Aloy, Higgins and Mueller, *Certified Randomness From Quantum Speed
   Limits*, PRX Quantum 7, 010349 (2026), DOI
   [10.1103/bnrq-sp5w](https://doi.org/10.1103/bnrq-sp5w).
   Locations refer to [arXiv:2506.14526v3](https://arxiv.org/abs/2506.14526v3):
   p. 4 Eqs. (8)--(9), the branch correlation domain; p. 13 Eq. (27), the
   average-speed entropy relaxation; p. 15 Eq. (32), affine dual bounds;
   p. 16 Lemma 3 and its following paragraph, the conservative center
   inequality and equality conjecture; p. 21 Appendix E(v), propagation
   of conservative bounds. The conjecture is refuted; the lemma is retained.
2. Van Himbeeck and Pironio, *Correlations and randomness generation based
   on energy constraints*, [arXiv:1905.09117v1](https://arxiv.org/abs/1905.09117v1):
   pp. 11--14, Eqs. (26)--(29); p. 18, Remark 9. Full statistics, entropy
   convex roofs, and dual bounds are prior methods. Its input-dependent
   average energy constraints differ from the scalar average speed here.
3. Jones, Ludescher, Aloy and Mueller, *Theory-independent randomness
   generation from spatial symmetries*, Quantum 10, 1966 (2026), DOI
   [10.22331/q-2026-01-16-1966](https://doi.org/10.22331/q-2026-01-16-1966).
   [Version 4 Appendix E](https://arxiv.org/html/2210.14811v4#A5),
   Eqs. (55)--(58), describes a correspondence without a max-average
   assumption. That is not an equivalence of the present ensemble budgets.
4. [Python 3.9 decimal documentation](https://docs.python.org/3.9/library/decimal.html),
   Decimal.ln and Context.ln: logarithms are correctly rounded to nearest.
   The Decimal checker widens each result to adjacent representable numbers.

For the new result, manuscript Sections III--V specify the points, rational
coefficients, global affine lower bound, and exactly feasible center ensemble.
Appendix A gives explicit elementary-function remainder bounds and the second
cell coverage. `decimal_grid.py` computes the node minimum and Lipschitz
correction. `interval_cells.py` computes the continuous-cell enclosure with a
different arithmetic backend. `reproduce.py` executes both and compares with
`certificate.json`; `validation.json` retains actual output from one run.
`plot_gap.py` uses the certificate values for its displayed entropy marks.

Neither narrow witness intervals nor figure marks are exact optimized
entropies. The guarantee concerns the average branch-speed relaxation with
classical side information. Human scientific review and publication approval
remain pending.
