# Author handoff: three-port coherent-transport TUR

## Core accepted claim

For every stationary elastic number-preserving noninteracting normal-fermion conductor with exactly three physical reservoirs and at most one propagating channel per lead,

`sigma/k_B >= (9/10) J asinh(J/C2)`.

Here `J` is the magnitude of the terminal-0 particle-count mean rate, `C2` is the full count variance per time with no electrical-noise factor two, and `sigma` is the actual heat entropy production summed over all three reservoirs. The result allows arbitrary fixed biases and broken time reversal. An exact rational witness gives `psi0 < 0.85395851552904 < 0.9`, so the theorem positively resolves the original strict-improvement question. It does not determine the optimal coefficient or claim saturation.

## Hardest checks already completed

- Primary determinant, current, full-noise, and all-reservoir heat-entropy conventions were reconstructed independently.
- Birkhoff reduction retains the exact variance-concavity remainder; all six permutations, both current signs, and both three-cycle orientations are covered.
- Analytic arguments cover dilute, nearly full, near-diagonal, tiny-occupation, and opposite-saturation regimes.
- The remaining scalar inequality has a complete 3,782-leaf rational interval cover. A separate `2^128` fixed-point checker replays the tree, square roots, logarithms, constants, and all 3,393 numerical leaves.
- A fresh scientific referee workflow accepted the unchanged frozen claim after separate source reconstruction, certificate replay, physical-scope audit, and bounded current primary-literature review.

## Caveats requiring author attention

- The AI referee is not external peer review. Priority searches were bounded; absence of a hit is not proof of exhaustive novelty.
- The coefficient `9/10` is certified but not claimed optimal or physically attainable.
- The theorem excludes extra channels or terminals, superconductivity/Andreev counting, interactions, driving, hidden probes, and inelastic replacements outside the stated scattering model.
- The central compact inequality is computer-assisted; the analytic exterior and finite certificate are both necessary.
- Author name, affiliation, postal code, email, target venue, and all policy disclosures must be confirmed.

## Source map

- Physical statement and conventions: `source.md`, `problem.md`, `physics.json`.
- Primary source ledger and reproduced baseline: `source-ledger.json`, `reproduction.json`, `evidence/reproduce/`.
- Full proof: `evidence/research/uniform-bound-proof.md`.
- Certificate and checkers: `evidence/research/certify_cycle.py`, `cycle-certificate.json`, `check_certificate_integer.py`, `integer-replay-data.json`.
- Accepted independent review: `audit/science.md`, `audit/referee-analytic-review.md`, `audit/referee-literature-review.md`.
- Manuscript: `manuscript/main.tex`, `manuscript/references.bib`.
- Reproduction instructions: `manuscript/REPRODUCIBILITY.md`.

## Venue and AI use

Physical Review Research, Regular Article, is the current local target. Scope and APS AI-policy evidence are recorded in `venue/aims-and-policy.md`. Codex contributed substantively to reasoning, computation, literature screening, and drafting; the manuscript says so. Before submission, the named author must independently review all outputs and assume responsibility, revise the disclosure if required by then-current policy, and decide whether this venue and open-access terms are acceptable.

No external submission or human approval has been performed.
