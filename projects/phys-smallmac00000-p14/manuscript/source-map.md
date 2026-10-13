# Manuscript-to-evidence map

The accepted scientific snapshot is audit/snapshot.json, digest
a525566d13f32770206e6c2373e1c6217297fa7bce4378af633ae80277716793.
Its 208 listed files remain unchanged. The actual accepting referee is
PHY-14-referee-5a932658dcd5, verdict accept, in audit/science.json and
audit/science.md. The schema recovery preserves that decision and identity;
it is not a second scientific review. The writing job is
PHY-14-write-48967e21f0da. Original status remains unresolved.

## Core statements

| Manuscript location | Exact support and relevant limit |
| --- | --- |
| Section 2, fermionic and spin Hamiltonians | Published Sayyad–Lado Eqs. (1)–(2), literature/sayyad-lado-published.pdf; source-ledger.json; evidence/convention-map.md; audit/referee-source.json. Original odd-left physical half-line, t=1, U=delta=eta=1/5, mu=0, Delta=1+epsilon. |
| Proposition 1, normalized Q0 and claim | claim.json accepted_statement as reproduced in audit/science.json; evidence/research-halfline-derivation.md sections 1–3 and 6; audit/science.md. |
| Section 3, spectral similarity and all-degree uniqueness | evidence/research-halfline-derivation.md section 2 and the referee's independently reconstructed operator argument in audit/science.md. Fixed-degree bounded similarity and measure-zero continuum kernel; no uniform bound in Clifford degree asserted. |
| Section 4, linear Q1, cubic inverse, locality | Accepted derivation sections 3–4; referee report and audit/referee-root-bounds.json. Referee-certified exact real band endpoints, separation 12/25, weighted inverse below 61.103. |
| Section 5 and Appendix B, exact 3A−2B root | audit/referee_check.py root_data(), audit/referee-root-bounds.json; original evidence/research-second-bulk-seed.json. Exact decimal center, radius 1e-20, nonzero-determinant dyadic preconditioner, contraction self-map. |
| Eq. (29), integer multiplier | audit/referee-root-bounds.json and constants() in audit/referee_check.py. Integer 1248632935 bounds the product of the unrounded inverse and functional constants. |
| Table 1, Eq. (34), 96-site forcing bound | audit/referee-certificate-frozen-Q1-L96-eta0.2.json. Original input evidence/research-halfline-Q1-L96-eta0.2.npz; the independent checker treats entries as exact dyadics and restores all physical support-crossing bonds. |
| Eq. (35), independent 80-site result | audit/referee-Q1-L80.npz and audit/referee-certificate-referee-Q1-L80.json. Separately generated from zero; excludes zero but does not alone prove the 0.0001 threshold. |
| Section 5 controls | audit/referee-source.json and audit/referee-adversarial-controls.json; L16 inconclusive record audit/referee-certificate-referee-Q1-L16.json. |
| Section 6, contradiction and domain | Accepted derivation section 6; explicit operator-domain justification in audit/science.md. Norm-localized derivatives, tracial local testing and summation by parts; no bounded infinite Hamiltonian assumption. |
| Figure 1 | reproducibility/reference/bounds.json and certificate96.json/certificate80.json; reproducibility/plot_bounds.py; manuscript/figures/certified-bounds-data.json. Rounded-outward enclosure plot, not a statistical fit. |
| Appendix C, physical residual and contraction | audit/referee_check.py residual_certificate() and formfactor_certificate(); accepted derivation sections 4–5; independent Clifford control. The copied core is byte-identical. |

The copies in reproducibility/reference retain the actual original record
identity and original filenames. manuscript/reproduction-provenance.json
maps all eight copied files to their original bytes. The portable wrapper
changes only output handling and execution labels. Its successful writing-phase
replay is recorded in manuscript/replay-execution.json; this is not fresh science
review or acceptance.

## Bibliography and attribution

Five entries are used, with no self-citation quota. The following checked
primary records support metadata and the bounded comparisons:

| Key | Primary source and use |
| --- | --- |
| Sayyad2023 | [Journal DOI](https://doi.org/10.1103/PhysRevResearch.5.L022046), archived published Eqs. (1)–(5), and [arXiv v1](https://arxiv.org/abs/2302.13561v1). Defines model and exactly solvable slice. Its printed Eq. (6) is not used as an input or a new result in this paper. |
| Fendley2016 | [Author record](https://arxiv.org/abs/1512.03441v1) and [journal DOI](https://doi.org/10.1088/1751-8113/49/30/30LT01); archived full text. Uniform XYZ construction and bounded discussion of spatially varying couplings, not an all-order claim for our dimerized complex point. |
| Olund2025 | [Published record](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.111.L201114); detailed comparison uses the [versioned author text](https://arxiv.org/html/2305.16382v1), resonance/band-overlap and interaction sections. The preprint version is identified in the bibliography. General resonance mechanism is prior art. |
| Moudgalya2026 | [Versioned author preprint](https://arxiv.org/abs/2603.02326v1), archived full text, Sec. VI and Appendix D. Uniform XYZ reformulation and distinction of finite boundary modifications. Listed as a preprint; no journal venue invented. |
| Johansson2017 | [Author preprint](https://arxiv.org/abs/1611.02831) for ball arithmetic; [Inria primary publication record](https://radar.inria.fr/report/2017/lfant/uid9.html) confirms IEEE Trans. Computers 66(8), 1281–1292 and DOI 10.1109/TC.2017.2690633. Cites the arithmetic method, not a theorem proving this physics result. |

Current primary web records are retained locally in manuscript/primary-web-*.json.
This bounded verification does not certify exhaustive novelty. A fresh release
worker must still verify every citation, imported source, rendered reference and
page. Human verification and journal-policy judgment remain pending.
