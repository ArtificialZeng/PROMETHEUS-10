# phys-00002-p10

**A balanced beam-splitter counterexample to the low-order Wigner–Rényi vacuum bound**

Result class: `disproofs`; original question: `disproved`; release: `draft_ready_author_review_required`.

## Background

Balanced mixing of two independent non-Gaussian low-energy states does not preserve the vacuum minimum for all low-order Wigner–Rényi entropies; the proposed extension to every alpha in (0,1/2) fails.

## Original question

低阶 Wigner–Rényi 熵：真空是否仍给出最小值？

## Frozen scientific scope

The universal low-order Wigner–Rényi vacuum bound for independently prepared balanced beam-splitter inputs is false. With [x,p]=i and Wvac=exp(-(x²+p²))/pi, prepare psi=(20|0>+|2>)/sqrt401 independently on both modes, trace one output after the balanced lossless mixer, and set alpha=1/4. Its exact retained Wigner function is exp(-R)[(401-2R+R²/2+20sqrt2(x²-p²))/401]²/pi, R=x²+p². A directed full-plane upper bound proves I_1/4(Wout)<9.43718<9.43892<I_1/4(Wvac)=4pi^(3/4), hence h_1/4(Wout)<h_1/4(Wvac). No other alpha range or optimum is claimed.

## Proposed contribution and limitations

Exact independent product input psi=(20|0>+|2>)/sqrt401 yields an admissible beam-splitter state violating the vacuum bound at alpha=1/4; directed full-plane upper I<9.43718, vacuum I>9.43892.

2026-10-12 official full text and version histories of 2411.05562v2 and 2609.24670v1; preserved 2601.16898v2 context; bounded searches for Wigner Rényi beam-splitter low-alpha counterexamples, cross-Wigner p<1 and squeezed alpha=1/4. No matching resolution located; absence of hit is not exhaustive priority proof. Referee novelty audit remains mandatory. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](reproducibility/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
