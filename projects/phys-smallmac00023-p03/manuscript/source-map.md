# Manuscript-to-evidence map

The entire scientific claim is the unchanged accepted statement in claim.json,
with acceptance in audit/science.json and its independently checked scope in
audit/science.md. Internal provenance is kept in this local dossier, not the paper.

| Manuscript material | Bound scientific evidence | Primary attribution |
| --- | --- | --- |
| Channel, Choi convention and finite restriction | physics.json; reproduction.json; evidence/input-a.json; evidence/input-b.json | Mele v3, Lemma 25, Definition 33, Lemma 36 |
| Anti-degradability and Choi two-extension equivalence | literature/reproduction-source-excerpts.md; accepted referee report | Mele v3, Lemma 54; Myhr and Lütkenhaus |
| Prior qubit bound 2/3 and stronger-dephasing qutrit regime | evidence/qubit-baseline.json; evidence/research-prior-comparison.md | Mele v3, Eq. (62), Lemma 39 Facts 3 and 6; Fig. 4 / Eq. (70) |
| Necessary 14-dimensional support, two swap sectors and transfer | evidence/research-reduction.md; evidence/qutrit-reduction.json | Own channel-specific derivation; Myhr Appendix A explains the general caveat |
| Sextic, root branch and narrower rational isolation | evidence/research-endpoint-proof.md; evidence/qutrit-exact-certificate.json | Own exact endpoint calculation |
| Rank-four primal and both Choi marginals | evidence/research-endpoint-proof.md; evidence/qutrit-symbolic-replay.json | Own Gram construction; independently checked in audit/replay.log |
| Face dual, derivative and full 27-dimensional Schur lift | evidence/research-endpoint-proof.md; evidence/qutrit-exact-certificate.json; evidence/qutrit-symbolic-replay.json | Own certificate family and analytic lift |
| Loss postcomposition and adjoint pullback, all lambda | evidence/qutrit-composition-check.json; evidence/research-endpoint-proof.md | Mele v3, Lemma 28 / Eq. (67); own primal/dual applications |
| Capacity consequence and infinite-channel implication | evidence/research-endpoint-proof.md; accepted scope report | Mele v3, Corollary 35; anti-degradability implies zero unassisted quantum capacity |
| Ranade symmetry-class comparison | evidence/research-prior-comparison.md; audit/referee-equivalence.md | Ranade v1 Sec. 2 / Eq. (3) / Theorem 1 |

All numeric claims trace to the exact polynomial and the rational interval
records. The displayed threshold and difference from 2/3 are rounded descriptions.
The conservative rational bounds in Table 2 enlarge the actual certificate
intervals; they do not replace exact arithmetic with decimal confidence.
The root count uses an exact Sturm chain with rational endpoints. No floating
optimizer or finite scan establishes the quantified conclusion.

The supplied supplementary code/data are exact copies of the selected accepted
files, with binding recorded in evidence/write-supplement-binding.json. The
portable runner checks equality of generated JSON records in a fresh directory.
Environment and regeneration instructions are supplementary/environment.json,
supplementary/requirements.txt and supplementary/README.md.

Bibliographic metadata were checked against actual primary pages during writing:

- Mele, Salek, Giovannetti and Lami, [APS record](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.110.012460)
  and [arXiv v3](https://arxiv.org/abs/2401.15634v3).
- Myhr and Lütkenhaus, [APS record](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.79.062307)
  and [arXiv record](https://arxiv.org/abs/0812.3667).
- Ranade, [arXiv record with journal/DOI metadata](https://arxiv.org/abs/0906.5255)
  and [primary v1 PDF](https://arxiv.org/pdf/0906.5255v1).

This is a writer's attribution preflight, not the fresh release citation audit.
The original downloaded primary sources remain only in the local dossier.
