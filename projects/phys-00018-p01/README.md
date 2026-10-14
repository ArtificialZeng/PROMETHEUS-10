# phys-00018-p01

**A local noise tradeoff for two cross-regulated genes with unequal finite RNA lifetimes**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

At unregulated RNA/protein mean one and finite unequal RNA lifetimes, arbitrary cross-transcription shaping cannot reduce both stationary protein Fano factors below their correctly mean-matched two-stage baselines within the stated response-dependent weak-feedback neighborhood. This excludes a whole nonlinear low-copy design route without LNA or a burst approximation. Searches for a legal simultaneous-suppression example must leave this neighborhood, change parent kinetics or consider larger networks.

## Original question

有限 mRNA 寿命的交叉调控网络，能否同时降低所有蛋白质的噪声？

## Frozen scientific scope

For the exact infinite-state two-stage N=2 gene-expression CTMC with parent tuples (c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1), let h1,h2 be any real bounded whole-lattice protein functions with |h_i|<=1, and a,b>0. Set g=max(a,b), f1=1+epsilon*a*h2(P2), f2=2-epsilon*b*h1(P1), with all other reaction channels unchanged. The exact independent-parent forms defined in evidence/research-pass2/operator-certificate-and-tail.md satisfy |V1|,|V2|<=4/5*sqrt(U1*U2) for all such response functions, without monotonicity or a finite plateau. For S=a^2*U1+b^2*U2>0, every 0<epsilon<min(1/g,S/(4480*g^3)) gives an admissible network with at least one stationary protein Fano factor strictly above its mean-matched finite-lifetime baseline B1=3/2 or B2=4/3. If both responses are constant, both Fano factors equal their baselines. This computer-assisted local theorem covers all response shapes for this fixed unequal-lifetime low-copy pair only; epsilon is response-dependent. The original arbitrary-N, arbitrary-kinetics, strong-feedback problem remains unresolved.

## Proposed contribution and limitations

A computer-assisted exact local no-simultaneous-output-suppression result for the finite-RNA parent pair (c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1), uniform over every real bounded whole-lattice response shape, including nonmonotone and arbitrarily rare tails. A new weaker whole-space weighted generator bound and finite Riesz residual enclosures remove the earlier artificial finite-plateau restriction, yielding |V_i|<=4/5 sqrt(U1 U2), with an explicit finite-feedback stationary covariance remainder.

Rechecked official arXiv histories 2607.20823,2605.15401,2512.20887 and the current burst-paper Discussion and official author list on 2026-10-13 UTC before legacy extension. Compared decisive pages in preserved primary PDFs/texts and targeted exact-title, finite-intermediate, finite-mRNA, two-stage weak-feedback, nonlinear cross-regulation and simultaneous-suppression searches. No matching later primary theorem was identified in this bounded screen. Current general resolution and global priority remain uncertain; absence of a hit is not proof of openness or novelty. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
