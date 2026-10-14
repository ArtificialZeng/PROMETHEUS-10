# Manuscript source map

The paper's central claim and physical scope are the already checked exact R=4
existence result. The manuscript adds exposition, displayed-data exports and
portable reproduction instructions, not a new scientific extension.

| Manuscript content | Stable scientific input or primary source | Scope |
| --- | --- | --- |
| Ten-site definition and R=4 target | problem.md; original Kay--Tamon preprint, Section II.A and Table I | Fixed positive couplings, zero diagonal, open chain, all 0<x<=1/16 |
| Reflection sign and polynomial identities | evidence/research-residue-derivation.md; evidence/reproduction-conventions.md; evidence/research-symbolic-and-bound-check.json | Exact model identities; no full-amplitude Taylor expansion at zero |
| Cancellation equations, exact witness, nonzero response | evidence/research-root-certificate.json; scripts/certify_r4_root.py | Unique zero in the specified exact box, not rounded couplings |
| Complete uniform remainder | evidence/research-uniform-proof.md; scripts/check_r4_symbolic_and_bounds.py | Low analytic tail plus the retained high-energy spectral weight |
| High-mode asymptotics and limsup for this witness | evidence/research-uniform-proof.md | No general-R optimality claim |
| Kraus error, probability, units, conditional normalization and cost | evidence/research-uniform-proof.md; physics.json | Square invertible norm-one A, gamma<=1/(16 kappa), postselection |
| Scalar numerical table and precision statements | evidence/research-independent-replay.json; scripts/replay_r4_eigenseries.py | Numerically reconstructed prior reference; samples support calculations, not the uniform proof |
| Exact displayed center and preconditioner | manuscript/certificate-center.tex; manuscript/certificate-preconditioner.tex | Literal exports of retained certificate inputs |
| Table regeneration | reproducibility/export_manuscript_data.py; manuscript/comparison-table.tex | Pure export from accepted retained data |

Primary literature, checked on 2026-10-12:

- Alastair Kay and Christino Tamon, *Matrix Inversion by Quantum Walk*,
  [arXiv:2508.06611v1](https://arxiv.org/abs/2508.06611v1), 2025.
  Section II.A Conjecture 1, Table I, Appendix A, and Example 1. Its current
  version page still lists v1. The chain model, odd-coefficient mechanism and
  endpoint suppression are attributed to this preprint. It is identified in
  manuscript text because the selected journal's guideline requests unpublished
  work in text rather than the reference list.
- Alastair Kay and Christino Tamon, *The strength of weak coupling*,
  [arXiv:2512.08141v1](https://arxiv.org/abs/2512.08141v1), 2025.
  Theorem 4.1, Sections 4.2 and 6; current version page still lists v1. The checked
  statements concern a different weak-coupling transfer regime. Identified in text.
- Christopher Kang and Yuan Su, *Quantum matrix arithmetics with Hamiltonian
  evolution*, [DOI:10.1145/3816436](https://doi.org/10.1145/3816436), 2026.
  Current [arXiv:2510.06316v3](https://arxiv.org/abs/2510.06316v3), revised
  2026-09-01, Section 4.4, Proposition 19 and Corollary 20. The original
  scientific dossier contains this v3 full text; a complete reading of all 94
  pages is not claimed. Bibliography record is tied to the journal metadata;
  the compared statements are explicitly the current v3 statements.
- Gabor Lippner and Yujia Shi, *Quantifying state transfer strength on graphs
  with involution*, Quantum Information Processing 23, 166 (2024),
  [DOI:10.1007/s11128-024-04362-5](https://doi.org/10.1007/s11128-024-04362-5).
  Publisher abstract and introduction support the limited contextual statement
  on quantitative transfer with involution and the journal-fit comparison.
  No central result is based on this additional introductory citation.

The exact source versions in the scientific dossier are preserved. Current
version and targeted later-resolution checks were repeated before manuscript
extension and preserved separately. The search was bounded and nonexhaustive;
absence of a search result does not establish priority or unrestricted openness.

Redistribution selection includes own manuscript/code/calculated JSON only.
Full third-party primary PDFs/texts and browser retrieval records remain in the
local dossier; they are not selected for the author submission archive.
