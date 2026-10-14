# phys-00040-p01

**Initial entropy-production decrease for product-profile narrow beams in the Landau–Maxwell equation**

Result class: `partial-results`; original question: `unresolved`; release: `draft_ready_author_review_required`.

## Background

A natural counterstreaming route to positive initial entropy acceleration is excluded beyond Gaussian local profiles, even for arbitrary fixed longitudinal score skewness. Within the specified beam scaling/covariance class, a putative positive p->0 sequence must violate local product structure or fixed-configuration hypotheses. The original all-data/all-time question remains unresolved.

## Original question

三维 Landau–Maxwell 气体的熵产生，是否从初始时刻起始终递减？

## Frozen scientific scope

In the three-dimensional homogeneous Landau-Maxwell equation with a(z)=(|z|^2 I-zz^T)/2, mass one, mean zero and energy three, fix finite distinct real mu_j, w_j>0 with sum w=1, sum w mu=0, sum w mu^2=3. For each j fix centered normalized P_j on R^2 and R_j on R, each a polynomial globally bounded below by a positive constant multiplied by a centered nondegenerate Gaussian, with Cov(P_j)=a_j I_2, Var(R_j)=lambda_j>0 and sum w a=1. Put kappa_p^2=1-(2p+p^2 sum w lambda)/3 and f_p(v)=p^-2 sum_j w_j P_j(v_perp/sqrt(p)) R_j((v3-kappa_p mu_j)/p). For sufficiently small p>0 with kappa_p>=1/2, its actual initial right entropy-production derivative is Dprime_0(f_p)=p^-2 sum_j w_j C_j+O(p^-1), with configuration-dependent remainder, where C_j=-(mu_j^2+3)^2 JP_j/2-2(1+2a_j+U4_j/4)J_j+(9+5mu_j^2-mu_j^2 K2_j)I_j-mu_j a_j S3_j. Here JP=E_P||Hess log P||_F^2, U4=E_P|X|^4, K2=E_P(X.grad log P)^2, I=E_R((log R)prime)^2, J=E_R((log R)doubleprime)^2 and S3=E_R((log R)prime)^3. Every such coefficient satisfies C_j<=-(5/28)(mu_j^2+3)^2 JP_j<=-45/(14a_j^2), so sum w C_j<=-45/14 and Dprime_0(f_p)<0 for all sufficiently small p. The same leading functional inequality holds for any regular positive product factors with the stated finite moments and valid integrations by parts. This is an initial-data asymptotic, not a closure or a result uniform over varying configurations; the original universal monotonicity problem remains unresolved.

## Proposed contribution and limitations

For every fixed finite normalized separated beam configuration with centered independent local transverse/longitudinal positive polynomial-Gaussian factors and widths sqrt(p),p, derive the full original-collision initial derivative Dprime_0(f_p)=p^-2 sum w C_j+O(p^-1). The general product coefficient includes longitudinal score skewness. Projected longitudinal curvature and transverse moment-curvature inequalities prove C_j<=-45/(14a_j^2), hence sum w C_j<=-45/14. Actual-mixture posterior overlap, tails and fixed-p initial differentiability are controlled analytically.

Fresh primary histories/fulltexts and bounded exact-claim/successor/product-beam neighbor searches on 2026-10-14. Actual located Villani v5 sections 7,13,24.1 and Delarue-Menozzi-Nualart v1 Proposition 2.3 checked. No matching later resolution or identical criterion located; absence is not openness/priority proof. Older Villani 1998/2000 fulltexts remain unreviewed. Candidate novelty/value are proposer assessments requiring a fresh referee; earlier acceptance covers a different scope. Exact model and scope are stated in the frozen claim. Human author review remains required.

## Artifacts and replay

[PDF](paper.pdf) · [TeX](manuscript/main.tex) · [BibTeX](manuscript/references.bib) · [Author handoff](AUTHOR_HANDOFF.md).

- [Replay guide](repro/README.md)

Run scientific commands in a scratch copy with the dependencies declared by the linked guide. No AI account is needed. `PACKAGE-PROVENANCE.json` documents the unmodified PDF, original bundle hashes, renamed PDF and any copied path substitutions. `SOURCE-BUNDLE-CONTENTS.json` is the original bundle inventory, not a claim that the public derivative has unchanged member names or hashes. AI scientific audits are internal checks, not external peer review.
