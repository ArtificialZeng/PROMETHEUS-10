# phys-00027-p01

**Time-independent Lindblad embeddings of two-parameter Werner–Holevo noise**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

The unrestricted reduction makes the known covariant rate inequalities decisive for calibrated symmetric and antisymmetric Werner-Holevo noise even when the underlying constant master equation is not assumed symmetric: outside the qutrit region no hidden Hamiltonian, noncovariant jumps, or logarithm branch can realize the observed channel. The two boundaries remain the zero-rate limits of the known symmetric-traceless and antisymmetric jump families.

## Original question

满秩双参数 Werner–Holevo 噪声：精确恒定 Lindblad 实现的区域与分支障碍

## Frozen scientific scope

For the frozen two-parameter noisy Werner-Holevo channel on M_d(C), write Phi=P0+s Ps+a Pa with s=1-d*x/(d-1)-d*y/(d+1) and a=1-(d-2)*x/(d-1)-(d+2)*y/(d+1). For every d>=3 in the sector s>0,a>0, there exists a finite time-independent same-system GKLS generator L with exp(L)=Phi, allowing arbitrary Hamiltonians, jumps and logarithm branches, if and only if s^((d+2)/d)<=a<=s^((d-2)/d). A valid generator has H=0 and nonnegative symmetric-traceless and imaginary-antisymmetric jump rates gamma_s=((d-2)log(s)-d log(a))/(2d) and gamma_a=(d log(a)-(d+2)log(s))/(2d). For d=3 this gives the complete classification in the frozen x>0,y>0,x+y<=1 domain: s=1-3x/2-3y/4>0, a=1-x/2-5y/4>0, and s^5<=a^3<=s. The negative even-multiplicity sectors for d>=4 are not classified.

## Proposed contribution and limitations

The proposed contribution is only the arbitrary-endpoint-generator necessity step and its qutrit consequence: for every d>=3 and s,a>0, any same-system time-independent GKLS logarithm of the O(d)-covariant endpoint, even if noncovariant and nonprincipal and with arbitrary Hamiltonian/jumps inside degenerate sectors, has a full-O(d) average fixed by branch-invariant real sector traces to the principal covariant logarithm. Combining this reduction with the known 2023 covariant cone gives the unrestricted positive-spectrum criterion. Odd real sector multiplicities plus singularity exclusion then give the complete frozen-domain d=3 classification. The covariant cone/exponential itself is not claimed new, and the signed d>=4 problem remains unresolved.

Complete retained primary PDFs arXiv:1801.06121v3, 2301.10679v4, and 2602.08464v1 were read at the recorded locators, and live primary records plus exact-claim/later-resolution searches were rechecked on 2026-10-13. The current model record remains arXiv:2405.11216v3. No returned primary record stated the narrowed arbitrary-noncovariant O(d) endpoint reduction or complete noisy-Werner--Holevo qutrit region. This bounded result is not proof of priority or openness; a fresh referee must independently repeat the comparison. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
