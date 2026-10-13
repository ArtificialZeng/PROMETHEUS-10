# Author handoff — fixed-ray qubit EB result note

## Core claim

For every fixed qubit entanglement-breaking channel `Psi`, the ray
`Phi_e=(1-e)D_(4/3)+e Psi` moves strictly below the reverse-depolarizing
enhancement factor for all sufficiently small positive `e`, unless the ray is
constant. If the normalized Choi Bell overlap `c_Psi` is positive, then
`K_* chi(Phi_e)-C_E(Phi_e)=c_Psi e log2(1/e)+O_Psi(e)`. If `c_Psi=0`, the
channel is unital with Bloch matrix `-Q`, and the gap is
`[K_*/2](lambda_max(Q)-1/3)e+O_Psi(e^2)`. The capacities are fully optimized,
and `C=chi` because all maps on the ray are EB.

The original comparison over every qubit EB channel remains unresolved. The
accepted result has no uniform neighborhood, no control of directions
`Psi=Psi(e)`, and no experimental claim.

## Hardest checks already represented in the dossier

- The endpoint mutual information has the global quadratic optimizer gap
  `2|r|^2/(9 ln 2)`, which confines the moving assisted-capacity optimizer.
- The missing eigenvalue of the purified output lifts as
  `c_Psi(1-|r|^2)e+O(e^2)` uniformly on a compact input ball.
- Holevo information is controlled over all ensembles by
  `|chi(Phi_e)-chi(D)| <= 2e log2(5)` for `e<=1/2`; no finite ensemble is used
  as an upper bound.
- On the zero-overlap face, an EB product decomposition forces
  `t=0`, `T=-Q`, `Q>=0`, `tr Q=1`, after which exact Pauli formulas give the
  linear coefficient.
- A fresh referee replay reconstructed the endpoint from Pauli Kraus operators
  and challenged both asymptotic coefficients. This is an AI-context audit,
  not external peer review.

Primary evidence: `audit/science.json`, `audit/science.md`,
`evidence/endpoint-perturbation-analysis.md`,
`evidence/eb-fidelity-geometry.md`, and `audit/referee_replay.log`.

## Draft and reproducibility package

- Manuscript source: `manuscript/main.tex`
- Bibliography: `manuscript/references.bib`
- Compiled draft: `manuscript/main.pdf`
- Figure: `manuscript/figures/two_regime_scaling.pdf`
- Figure code/data/instructions: `manuscript/reproducibility/`
- Fresh release build evidence:
  `manuscript/build-release-b39a5f157b5e/main.log` and
  `manuscript/build-release-b39a5f157b5e/main.bbl`
- Provisional venue record: `venue.json`
- Submission inventory: `publication.json`

The deterministic figure script was tested with Python 3.13, NumPy 2.4.2,
SciPy 1.15.3, and Matplotlib 3.10.0. It reproduces the endpoint values and the
two representative scaling limits. The plot is diagnostic; the proof is
analytic.

## Provisional target fit

The provisional target is a Research Article in the *Journal of Mathematical
Physics*. Its current scope explicitly includes Quantum Information and
Computation, and the Holevo endpoint and Shor EB-additivity papers appeared in
that journal. This is a plausible fit, not a recommendation or acceptance
prediction. The journal's current AI policy requires detailed disclosure when
AI affects analysis or conclusions; the draft contains such a statement.
SCIE/indexing and ranking were not independently verified and are not claimed.

## Caveats and decisions requiring the author

1. Confirm the draft identity exactly as supplied: `Xiaojian Zeng`, PBC School of
   Finance, Tsinghua University, 100190, China, `xiaojianzeng@foxmail.com`. In
   particular, confirm name spacing, postal form, and email.
2. Independently check every derivation, numerical convention, citation, and
   novelty statement. The prior-art search was targeted, not exhaustive.
3. Decide whether the local fixed-ray contribution is substantial enough for
   the provisional journal and reconfirm its current article types and policy
   immediately before submission.
4. Review and, if necessary, refine the generative-AI disclosure. The working
   system identified itself as OpenAI Codex with GPT-5.6 Sol, but exposed no service
   build identifier.
5. Supply or confirm conflict-of-interest, funding, author-contribution, and
   repository statements required by the chosen venue.
6. Supply figure alt text in the submission system if requested; the current
   AIP instructions require alt text for figures.
7. Do not describe the paper as proving a uniform neighborhood or the original
   all-EB inequality. A two-parameter estimate for `Psi(e)` approaching the
   zero-overlap face is the next scientific test.

No external submission has been made or authorized.
