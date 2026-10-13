# Manuscript claim and source map

This map follows the currently accepted science report and the two-page article in
`manuscript/main.tex`. It is a writing aid for a fresh release review, not a release
verdict. Equation labels refer to that TeX file. The article itself is self-contained.

| Material | Primary location and accepted evidence |
| --- | --- |
| Graph state and stabilizers, eq:state; LC and its unitary, eq:unitary | Vandré et al., Phys. Rev. A 111,052449 (2025), pp.052449-3–4, Eqs.(3)–(5),(10)–(11). Local source: literature/vandre-pra-2025.pdf. |
| Fixed labels and physical qubit locations | Same paper, Sec.II.C.3 and Fig.4, p.052449-5; explicit contrast with permutations. The article's fixed-label interpretation is stated in its abstract and model. |
| Boolean OR definition, endpoint premise and target, eq:premise–eq:target | Same paper p.052449-11, Definition 8 and Conjecture 1. The definition has an existence condition, not parity, and no connected-C assumption. Both-endpoint and unrestricted-intermediate-path conventions are explicit in source.md, problem.md and the accepted report. |
| Complete six-qubit edge lists, input matrices, LC word, eq:edges–eq:lc | New result: evidence/research-pass1/proof.md §§2–3; audit/science.md correctness section; audit/referee-0f50c3c6c5f1/replay.py and replay.log, fields input_endpoints and candidate_circuit. The public copy is supplement/referee_replay.py. |
| Condensed edge sets and strict rank witness, eq:quotients–eq:cutwitness | New result: accepted proof §4; current independent replay fields outputs. The two exact matrices have ranks 2 and 1. This is an analytic counterexample, not a finite-search non-hit. |
| Reduced stabilizers and physical rank formula, eq:projector–eq:rank | Known ingredients: Vandré et al., pp.052449-5–6, Eqs.(12)–(17),(21),(23). The article derives the projector/rank identity directly. The new marginal spectra are checked by direct rational partial trace without using this rank formula. |
| Exact marginal matrices, spectra and bit entropies, eq:marginals | New calculation in accepted proof §4 and current replay outputs. rho_B(Q)=I/4, rho_B(Q')=(I+X4 tensor X5)/4. The checker proves the flat spectrum by rho^2=lambda rho and trace one. |
| Established rank-one condensation rule | Vandré et al. p.052449-11, Lemma 5; its Appendix C.1 proof. The candidate cut rank is 3, not 1. |
| Fig.15 comparison | Same paper p.052449-16, Appendix C.2, Fig.15(a,b). Ordered condensed sets: (1,2,3) in (a), (3,4,5) in (b). Degree profiles (1,0,1) to (1,0,3) and (2,0,2) to (2,2,2) are actual independent transcriptions/replays in current replay primary_figure_checks. |
| Foliage condensation and candidate classes | Burchardt and Hahn, Quantum 9,1720 (2025), arXiv:2305.07645v2 §4, Observation 3 and Corollary 2, PDF p.7; definitions in §3. Local PDF: literature/foliage-2305.07645v2.pdf. Current audit/referee-0f50c3c6c5f1/source-comparison.md checks classes {2,4},{3,5},{1},{6}. |
| Disconnected C and the permutation limitation, eq:permutation | Accepted proof §5; current independent replay unlabeled_limitation and exact swap assertion. No connected-C, unlabeled, minimum-vertex or shortest-word claim is made. |
| 152 exact marginal checks | Current accepted replay all_nontrivial_marginal_checks; 2(64-2)+2(16-2)=152. Writing-phase rerun: build/reproduction/referee_replay.py.log. |
| Physical use and finite regime | Accepted proof §5 and audit/science.md physical-admissibility/significance sections. The false rule would reject an actually equivalent input pair; OR is only classical preprocessing, not a proposed quantum channel. |

Primary publication links:

- [Vandré et al.](https://doi.org/10.1103/PhysRevA.111.052449), publisher page checked in venue/current-write-primary-web.json. The published numbering is used throughout. The later arXiv v2 instead numbers Definition 13 / Lemma 15 / Conjecture 16.
- [Burchardt and Hahn](https://doi.org/10.22331/q-2025-04-24-1720), publisher-supplied BibTeX and metadata checked in venue/current-write-detail-web.json. The manuscript bibliography retains its existing accurate record.

Only these two papers are cited in the Comment. The current accepted referee also
examined Zhang arXiv:2311.16188v2, Burchardt–de Jong–Vandré arXiv:2410.03961v2 and
Bourneuf et al. arXiv:2607.09469v1 to compare the relevant maps and premises. That bounded
coverage is documented in audit/referee-0f50c3c6c5f1/source-comparison.md. These works
are not invoked to prove the new certificate and no exhaustive priority claim is made.
Historical pending entries in frozen scientific records remain unchanged.

The audit and literature paths above index the local private dossier; they are not
included in the submission whitelist. Public readers have the full analytic certificate,
primary DOIs, code and explicit inputs. The independent checker is a byte-identical
copy of the implementation attached to the current accepted report; replaying it does
not constitute a new independent review. The only authored PDF dependencies are
manuscript/main.tex and manuscript/references.bib; system TeX packages and generated
auxiliary/BibTeX files are build dependencies, not additional authored sources.
