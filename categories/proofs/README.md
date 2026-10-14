# PROMETHEUS-10 · Proof

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

An inspectable archive of AI-assisted physics research. **93 PDFs are preserved; 90 canonical research entries are indexed.** Three earlier results covered by later, more general or stronger claims remain linked as historical versions and are not counted twice. “10” is the name of the original collection, not the current manuscript count.

These are research drafts requiring human scientific, priority and authorship review. Recorded proof/disproof classes refer to the precise frozen claim. Partial and computational results leave the original problem unresolved. Separate AI review contexts are internal checks, not external peer review or journal acceptance. The original channel-boundariness draft retains its historical binding-gate limitation.

Scientific statements and manuscript titles retain their source language. Navigation, status, usage and the original ten detailed descriptions are localized; quoted scientific claims are not silently translated or weakened.

[PROMETHEUS-10](../../README.md)

[Searchable full catalog](../../catalog.html) · [Semantic comparison and deduplication](../../SEMANTIC_DEDUPLICATION.md) · [Reproduction guide](../../reproducibility/README.md)

## Browse the four result classes

| | Canonical entries |
|---|---:|
| [Proof](../proofs/README.md) | **32** |
| [Disproof](../disproofs/README.md) | **18** |
| [Partial result](../partial-results/README.md) | **38** |
| [Computational result](../computational-papers/README.md) | **2** |

The supervised workflow checks primary sources, reconstructs equations independently, reproduces a published baseline, develops a bounded result, and uses a fresh internal referee before writing and release checks. Compact evidence-indexed handoffs and shared tools reduce repeated work; cached input is a subset of input, not additional usage. No unmeasured token savings or success rate is asserted.

## Proof

<details>
<summary><strong>phys-00002-p02 · Four qubit measurements: the exact compatibility threshold</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Noisy quantum measurements can sometimes be implemented as marginals of a single parent measurement. Where is the noise threshold? |
| **Result and original-problem scope** | The draft proves the threshold 1/D for four strictly ordered planar, unbiased binary qubit measurements with common visibility. |
| **Proposed contribution** | Matching constructive and dual bounds give an analytic threshold; SOCP/SDP checks corroborate the formula. |
| **Limitations / bottlenecks** | Restricted to this four-measurement geometry and noise model; not a theorem for arbitrary POVMs or all measurement counts. |
| **PDF and source** | [PDF](../../projects/phys-00002-p02/paper.pdf) · [TeX](../../projects/phys-00002-p02/manuscript/main.tex) · [Bib](../../projects/phys-00002-p02/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p02) · `python reproducibility/reproduce.py --project phys-00002-p02` |

> Novelty reassessment remains required because a later primary answer arXiv:2609.38836v1, dated 30 September 2026, was recorded. Preserve the historical proof and source; do not relabel it as a newly open or priority-established result.

</details>

<details>
<summary><strong>phys-00002-p15 · Critical resetting erases coherence—at a controlled rate</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Random resetting changes long-time quantum dynamics. The critical Sibuya exponent separates qualitatively different renewal regimes. |
| **Result and original-problem scope** | For alpha=1 and a fixed finite-dimensional unitary register, the draft proves trace-norm convergence to spectral pinching, with fixed-gap rates. |
| **Proposed contribution** | A critical-case asymptotic theorem connects renewal coefficients to decay of off-diagonal quantum coherence. |
| **Limitations / bottlenecks** | Fixed dimension and fixed spectral gaps; no uniform closing-gap, thermodynamic-limit or arbitrary-reset theorem. |
| **PDF and source** | [PDF](../../projects/phys-00002-p15/paper.pdf) · [TeX](../../projects/phys-00002-p15/manuscript/main.tex) · [Bib](../../projects/phys-00002-p15/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p15) · `python reproducibility/reproduce.py --project phys-00002-p15` |

</details>

<details>
<summary><strong>phys-00003-p01 · Can torque lower the noise of a Gaussian particle?</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Nonequilibrium driving changes current fluctuations. Comparing with the same equilibrium trap tests whether a drive can suppress noise. |
| **Result and original-problem scope** | For the stable, zero-field, torque-driven underdamped Ornstein–Uhlenbeck model, degree-one/three position-current noise is bounded below by the matched equilibrium value. |
| **Proposed contribution** | Exact polynomial and independent Wick/Poisson calculations identify the nonnegative excess and gradient-boundary equality cases. |
| **Limitations / bottlenecks** | Restricted dynamics and polynomial current class; nonlinear forces, magnetic fields and higher degrees are outside the theorem. |
| **PDF and source** | [PDF](../../projects/phys-00003-p01/paper.pdf) · [TeX](../../projects/phys-00003-p01/manuscript/main.tex) · [Bib](../../projects/phys-00003-p01/manuscript/references.bib) · [Code / data](../../projects/phys-00003-p01) · `python reproducibility/reproduce.py --project phys-00003-p01` |

</details>

<details>
<summary><strong>phys-00004-p01 · Two noisy quantum batteries: can joint inputs help?</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Quantum battery work extraction may benefit from correlations. Generalized amplitude damping models a finite-temperature relaxation channel. |
| **Result and original-problem scope** | The draft proves W2(e)=2W1(e) for the stated two-use energy-constrained setting, including complex input states and global unitary extraction. |
| **Proposed contribution** | A phase reduction and exact polynomial positivity certificate close the two-use optimization in this model. |
| **Limitations / bottlenecks** | No claim for arbitrary channel families, arbitrarily many uses, or alternative operational definitions of work. |
| **PDF and source** | [PDF](../../projects/phys-00004-p01/paper.pdf) · [TeX](../../projects/phys-00004-p01/manuscript/main.tex) · [Bib](../../projects/phys-00004-p01/manuscript/references.bib) · [Code / data](../../projects/phys-00004-p01) · `python reproducibility/reproduce.py --project phys-00004-p01` |

</details>

<details>
<summary><strong>phys-smallmac00002-p01 · Absence of reflection-symmetric two-periodic boundary laws in the competing three-state SOS model</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 竞争 SOS 树模型：是否严格不存在反射对称二周期 Gibbs 相？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For all t,h,u>0, f(f(u))=u implies f(u)=u, with f(u)=(u^2+4thu+2t^2(h^2+1))/(t^2u^2+2th(t^2+1)u+t^4+2t^2h^2+1). Equivalently the positive reflection-symmetric level-message update has no nonfixed two-cycle. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00002-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00002-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00002-p01) · [Author handoff](../../projects/phys-smallmac00002-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00002-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00003-p01 · Maximum purity of absolutely PPT states of two qutrits</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 双qutrit绝对PPT态：最大纯度是否恰为 \(17/121\)？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every density operator rho on C^3 tensor C^3 that remains PPT under every global U in U(9), Tr(rho^2)<=17/121. Equality holds if and only if its decreasingly ordered spectrum is (3,1,1,1,1,1,1,1,1)/11. Equivalently, this is the exact maximum over all nonnegative ordered trace-one nine-spectra satisfying BOTH source LMIs. The proposed proof uses exact exhaustive vertices of a three-cut outer polytope, analytic completeness and strict convexity, and both-LMI attainment. This is a proof candidate awaiting a fresh scientific referee. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00003-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00003-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00003-p01) · [Author handoff](../../projects/phys-smallmac00003-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00003-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00005-p01 · Three-copy universal qubit purification under complete stabilizer preservation</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 三份未知噪声qubit：完全稳定子保持操作能否提高普适提纯保真度？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For a normalized-Haar pure qubit psi and three copies independently subjected to D_delta(X)=(1-delta)X+(delta/2)Tr(X)I, every completely positive trace-nonincreasing map E:M8->M2 that, tensored with any finite qubit identity, preserves the stabilizer positive cone has success-weighted conditional Haar fidelity F_delta(E)<=1-delta/2 whenever its average success is s>0. For every 0<delta<1 and every 0<s<=1, E_s=s Tr_(two inputs) is admissible and attains equality. Therefore the maximum in the unchanged source.md is exactly 1-delta/2 throughout its full stated domain. This three-input proof candidate does not assert the source paper's broader arbitrary-copy conjecture. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00005-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00005-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00005-p01) · [Author handoff](../../projects/phys-smallmac00005-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00005-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00005-p03 · A third magnetic Neumann level below the Dirichlet ground state on the disk</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 磁圆盘的第三个Neumann能级，是否始终不高于Dirichlet基态？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For the spinless magnetic Laplacian H_b=(-i nabla-b(-y,x)/2)^2 on the unit disk, with Dirichlet eigenvalues lambda_k(b) and magnetic-Neumann eigenvalues mu_k(b) ordered with multiplicity, mu_3(b)<=lambda_1(b) for every b>0. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00005-p03/paper.pdf) · [TeX](../../projects/phys-smallmac00005-p03/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00005-p03) · [Author handoff](../../projects/phys-smallmac00005-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00005-p03/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00006-p04 · 指定两浓度幂律反应系统，能否严格认证四条嵌套极限环？</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 指定两浓度幂律反应系统，能否严格认证四条嵌套极限环？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | Existence of admissible parameters in the original source ODE with a hyperbolically stable unique positive equilibrium and at least four nested hyperbolic periodic orbits, repelling/attracting/repelling/attracting outward, all in a compact positive annulus. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00006-p04/paper.pdf) · [TeX](../../projects/phys-smallmac00006-p04/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00006-p04) · [Author handoff](../../projects/phys-smallmac00006-p04/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00006-p04/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00009-p01 · Unique spanning-tree families bound the static response of every complete four-state Markov network</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 四态反应网络的稳态灵敏度，是否落在唯一生成树家族的凸包内？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every strictly positive finite set of twelve directed rates k on K4 with sum k=1 and every d in \[-1,1\]^12 in the original column-generator model, r_j=partial_lambda log pi_j&#124;0 lies in the convex hull of v^alpha_j=G^alpha_j-sum_l pi_l G^alpha_l over exactly the families unique under the full directed-edge multiplicity vector. More strongly, the 4x12 rooted-tree edge-marginal matrix H(k) is a convex combination of the unique-family incidence matrices with nonnegative normalized weights depending on k only. Proof: research/proof.md and the complete 93-coefficient exact certificate. This resolves only the full K4 source claim, not the general-graph conjecture, full-hull attainability or full-tree coupling. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00009-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00009-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00009-p01) · [Author handoff](../../projects/phys-smallmac00009-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00009-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00009-p02 · Pure-state uniqueness under common-axis measurements of three qubits excludes mixed-state impostors</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 三qubit均匀旋转测量：纯态唯一性是否足以排除所有混态仿冒？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every complex unit vector psi in C^8, under the complete labeled three-qubit common-axis effects E_b(n)=tensor_j(I+b_j n.sigma)/2 for all unit n and all b, uniqueness of P=&#124;psi><psi&#124; among pure states implies uniqueness among all complex density matrices. More strongly, every nontrivial density-matrix competitor rho with the same data has K=rho-P of rank two with eigenvalues +/-s, and P,rho share its two-dimensional range; Q=P-2Tr(PK)K/Tr(K^2) is a distinct pure competitor. This is an exact three-qubit identifiability theorem, not an all-N or finite-error certification claim. A complete proposed computer-assisted proof is submitted for fresh review. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00009-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00009-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00009-p02) · [Author handoff](../../projects/phys-smallmac00009-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00009-p02/manuscript/REPRODUCE.md) |

</details>

<details>
<summary><strong>phys-smallmac00012-p01 · Order-three unistochastic matrices form a monoid: exact compression of measured qutrit dynamics</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 三能级的两段“酉演化后测量”，能否总压缩成一段？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every U,V in U(3), there exists W in U(3) such that &#124;W_ij&#124;^2 equals \[B(V)B(U)\]_ij for all i,j. Equivalently, the order-three unistochastic set U_3 is a monoid under ordinary matrix multiplication. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00012-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00012-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00012-p01) · [Author handoff](../../projects/phys-smallmac00012-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00012-p01/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00014-p01 · The third magnetic Neumann eigenvalue does not exceed the Dirichlet ground state on an annulus</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 均匀磁场圆环上的第三 Neumann 能级是否仍低于 Dirichlet 基态？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For the dimensionless homogeneous-field magnetic Laplacian H_{a,b}=(-i nabla-A_b)^2 on every concentric annulus A_a={a<r<1}, with 0<a<1, b>0, no added harmonic Aharonov--Bohm flux, and respectively magnetic Neumann or Dirichlet conditions on both boundary circles, the globally ordered eigenvalues counted with multiplicity satisfy mu_3(A_a,b) <= lambda_1(A_a,b). |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00014-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00014-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00014-p01) · [Author handoff](../../projects/phys-smallmac00014-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00014-p01/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00014-p11 · No history advantage in repeated environment-assisted qubit recovery</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 三次固定环境测量时，历史反馈首次产生优势吗？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every qubit CPTP map with positive-definite Choi matrix, using the same four-outcome orthogonal projective measurement on each fresh minimal environment, the separately optimized current-outcome Markovian polar-recovery and full-history/final-only Bayesian entanglement fidelities are equal at three uses. More strongly, within the same physical model they are equal for every positive integer n and have common value (1+&#124;&#124;Q&#124;&#124;_*^n)/2, where Q is the determinant polarization matrix of any minimal Kraus frame. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00014-p11/paper.pdf) · [TeX](../../projects/phys-smallmac00014-p11/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00014-p11) · [Author handoff](../../projects/phys-smallmac00014-p11/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00014-p11/reproducibility/README.md) |

**Related results / preserved versions**

- [phys-smallmac00008-p02](../../projects/phys-smallmac00008-p02): Earlier covered version; preserved and not counted independently. The earlier optimized two-use equality for full-Choi-rank qubit channels is included in the later all-positive-integer-use theorem under the same fresh minimal environment, fixed full four-outcome measurement and recovery conventions. The all-n determinant-polarization result subsumes n=2.

</details>

<details>
<summary><strong>phys-smallmac00015-p01 · A sharp weak-driving phase bound for symmetric complete Markov networks</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 对称完全图 K_N 的弱驱动相位常数是否统一等于二态极限？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | In the frozen symmetric-splitting complete-graph model, for every integer N>=3, k0>0, finite offset vector, period T>0, and finite real Fourier drive, the weak coefficients satisfy A2>=2k0 B2. At finite offsets the inequality is strict whenever at least one energy difference varies in time; equality is exactly the zero-response class A2=B2=0. The coefficient 2 is optimal but is attained by a response-active system only at the excluded offset boundary, approached by x1=x2=1 and x3=...=xN=delta down to zero. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00015-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00015-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00015-p01) · [Author handoff](../../projects/phys-smallmac00015-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00015-p01/reproducibility/README.md) |

**Related results / preserved versions**

- [phys-smallmac00014-p03](../../projects/phys-smallmac00014-p03): Earlier covered version; preserved and not counted independently. The earlier finite-offset symmetric K3 weak-drive inequality and sharp factor 2 are the N=3 specialization of the later complete-K_N weak-Fourier-drive theorem. Neither proves a finite-amplitude phase bound. The earlier specialized calculation remains available.

</details>

<details>
<summary><strong>phys-smallmac00016-p01 · Exact current-bit optimum and a robust history advantage for coarse-grained generalized-amplitude-damping feedback</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 粗粒化 GAD 反例中两步 current-bit 恢复的精确最优值是多少？ |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For the ordered full-Choi-rank generalized-amplitude-damping qubit instrument, the incoherent 03&#124;12 one-bit readout, two independent uses, and arbitrary clock-dependent qubit CPTP recoveries conditioned only on the current bit: (i) at p=18/25 and gamma=3/10 the exact optimum is F_2^M=289/400, attained by identity recovery, while the fixed feasible history policy attains 1831/2500 and therefore has exact advantage 99/10000; and (ii) on the closed rectangle R=\[71/100,723/1000\] x \[29/100,303/1000\], the same history policy attains H=1-gamma+p gamma^2/2 and every admissible current-bit policy obeys F_2^M<=H-1/1000, hence F_2^B-F_2^M>=1/1000 throughout R. The rectangle is a sufficient certified region, not a maximality claim, and no off-center exact optimum or exact Bayesian optimum is asserted. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00016-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00016-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00016-p01) · [Author handoff](../../projects/phys-smallmac00016-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00016-p01/manuscript/REPRODUCIBILITY.md) |

**Related results / preserved versions**

- [phys-smallmac00015-p06](../../projects/phys-smallmac00015-p06): Earlier covered version; preserved and not counted independently. Both use the same ordered GAD instrument, incoherent 03|12 bit, p=18/25, gamma=3/10 and two-use policy distinction. The later exact current-bit optimum 289/400 and history value 1831/2500 give 99/10000 advantage, strengthening the earlier 7/2500 witness, and add a certified rectangle. The n=1 equality also settles earliest onset.

</details>

<details>
<summary><strong>phys-smallmac00018-p01 · Exact indirect-gap boundary in a flux-one-third Harper–Hofstadter model with a period-three mass</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 磁通 1/3 Harper–Hofstadter 三带模型的间接绝缘隙边界 |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For the frozen Hamiltonian in problem.md, G1(r,m)=G2(r,m)=G(r,m). Let rc=sqrt((69-11sqrt(33))/8). For 1/2<=r<=rc, G is positive for every m except m=+/-sqrt(3)r, where G=0. For rc<r<=2 there are unique 0<m_-(r)<sqrt(3)r<m_+(r), given by the two physical branches X in (Xc,1) and X in (3/4,Xc) of equations (1)-(2) in evidence/global-boundary-certification.md with Xc=(7+sqrt(33))/16, such that G<0 exactly when m_-(r)<&#124;m&#124;<m_+(r), G=0 at &#124;m&#124;=m_-(r),m_+(r), and G>0 otherwise. Hence the relative insulating boundary consists exactly of the two direct segments m=+/-sqrt(3)r for 1/2<=r<=rc joined at their cusps to four mass-reflected indirect branches for rc<=r<=2. The extremizers are exactly those parametrized in Section 4 of that evidence file and their spectral/mass reflections; no other momentum or exceptional Laurent-factor sector occurs. The isolated-band Chern tuple is (+1,-2,+1) for &#124;m&#124;<sqrt(3)r and (0,0,0) for &#124;m&#124;>sqrt(3)r, with the nonzero tuple negated under flux/orientation reversal. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00018-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00018-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00018-p01) · [Author handoff](../../projects/phys-smallmac00018-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00018-p01/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00013-p03 · Exact unrestricted Gaussian rank of two canonical matchgate magic states</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 两份 canonical matchgate magic state 的 unrestricted Gaussian rank |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For &#124;M>=(&#124;0000>+&#124;1111>)/sqrt(2), the exact unrestricted fermionic Gaussian rank over C of &#124;M> tensor &#124;M> is chi_G=4, with no particle-number, reality, blockwise ZZ, copy-exchange, or Pfaffian-chart restriction. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00013-p03/paper.pdf) · [TeX](../../projects/phys-smallmac00013-p03/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00013-p03) · [Author handoff](../../projects/phys-smallmac00013-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00013-p03/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00013-p04 · An exact criterion for removing an elementary amplitude-damping factor from a quantum channel</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 相位协变 qutrit 的 elementary 右除必要条件是否充分 |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every phase-covariant CPTP map Phi:M3->M3 with H=diag(0,1,2), Choi rank 2 through 8, and every ordered pair of distinct energy levels (a,b), condition (N) implies the existence of lambda in (0,1) and a CPTP Theta such that Phi=Theta composed with Psi_{lambda,a->b}. In fact, for any finite-dimensional CPTP Phi and orthogonal x,y, (N) is necessary and sufficient for such an elementary right quotient; if ZV=VA for a linearly independent minimal Kraus synthesis V, the quotient is CP exactly when 0<=lambda<1 and lambda<=&#124;&#124;A&#124;&#124;_2^{-2}. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00013-p04/paper.pdf) · [TeX](../../projects/phys-smallmac00013-p04/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00013-p04) · [Author handoff](../../projects/phys-smallmac00013-p04/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00013-p04/manuscript/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00013-p07 · The third boundary coefficient of even off-diagonally symmetric alternating-sign matrices</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 偶阶 OSASM 的第三列加权边界系数公式 |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every integer n>=2, the even-order OSASM boundary polynomial satisfies \[t^3\]X^O_{2n}(r,t)=r(1+(n-2)r^2)X^O_{2n-2}(r,1) in Z\[r\], under the definitions and BFK normalization frozen in problem.md and physics.json. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00013-p07/paper.pdf) · [TeX](../../projects/phys-smallmac00013-p07/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00013-p07) · [Author handoff](../../projects/phys-smallmac00013-p07/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00013-p07/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00020-p03 · Two-scale finite-size edge splitting at a repeated root of an extended Su–Schrieffer–Heeger chain</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | extended-SSH 重复衰减根线上的四个有限链边缘能级 |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For the finite open extended-SSH family H_N with u2=1, u0=r^2, u1=2r and r in \[1/5,4/5\], the exact confluent four-state pencil has positive energies r^{N+1}/phi_{1,N} and r^{N+1}/phi_{2,N} with the finite sums defined in the evidence. For every integer N>=61 the exact two positive in-gap energies obey the explicit uniform error functions R_a(N,r), these errors are relative o(1) uniformly in r, the leading laws are E_{N,1}=(1-r^2)r^{N+1}/N\[1+o(1)\] and E_{N,2}=N(1-r^2)^3r^{N-1}\[1+o(1)\], and no third positive level lies below the bulk-band distance (1-r)^2. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00020-p03/paper.pdf) · [TeX](../../projects/phys-smallmac00020-p03/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00020-p03) · [Author handoff](../../projects/phys-smallmac00020-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00020-p03/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00021-p01 · Exact finite-depth crossings in a Sierpinski–Hanoi free-fermion spin model</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Sierpinski–Hanoi 自由费米近简并的精确有限尺度递推 |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | In the finite open Sierpinski-Hanoi model defined in problem.md, restricted to the all-canonical-cycle-+1 single-particle sector and using the source normalization, the k=5 Figure-5 landmarks are exact transverse crossings at J=+/-1/3 and lambda=1/6. Their unique nonzero continuation exists for every k>=3 at J_k=+/-3^(-(k-3)/2), x_k=&#124;J_k&#124; and lambda_k=&#124;J_k&#124;/2; the generic flat multiplicity c_k=(3^(k-2)-1)/2 becomes c_k+1 and &#124;J_(k+1)/J_k&#124;=1/sqrt(3). On fixed I_+=\[1/4,1/2\] and I_-=-I_+, Delta_k is zero iff k=5; for k=3,4 and k>=6 it obeys the explicit positive coefficient-norm bound in evidence/fixed-interval-gap-salvage-result.md. Separately named moving windows W_k^+=\[J_k/2,3J_k/2\] and W_k^-=-W_k^+ have zero minima for every k>=3. The characteristic polynomial is generated by the signed three-scalar recurrence and exact quotient in the evidence. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00021-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00021-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00021-p01) · [Author handoff](../../projects/phys-smallmac00021-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00021-p01/manuscript/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00023-p03 · An exact anti-degradability threshold for the three-level bosonic loss–dephasing channel</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 固定 (e^{-\gamma}=1/2) 时三 Fock 能级 loss–dephasing 信道的精确反可降阈值 |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For N^(3)_(lambda,ln2) defined exactly in immutable source.md, with lambda in\[0,1\] and normalized A,B Choi, anti-degradability holds if and only if lambda<=r, where r is the unique root in\[66454426803/10^11,66454426804/10^11\] of601r^6-714r^5+113r^4-1040r^3+2080r^2-1280r+256 (approximately0.664544268033). The exact rank4 X_r supplied in evidence/research-endpoint-proof.md is PSD, trace1, swap invariant and has both marginalsJ_r. That proof supplies explicit Hermitian strict separating H_lambda with W_Hlambda PSD in the full27-dimensional space and Tr(H_lambda J_lambda)<0 for every lambda>r, and exact post-loss extensions for every lambda<=r. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00023-p03/paper.pdf) · [TeX](../../projects/phys-smallmac00023-p03/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00023-p03) · [Author handoff](../../projects/phys-smallmac00023-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00023-p03/supplementary/README.md) |

</details>

<details>
<summary><strong>phys-00004-p05 · Diagonal quantum discord under unital qubit noise: a relative-entropy proof for two-qubit states</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Within the stated finite-dimensional single-use noise model, local unital noise cannot increase diagonal discord despite a moving marginal eigenbasis. This supplies the resource monotonicity left numerically supported in S1 for the frozen two-qubit domain. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every two-qubit density operator rho_AB and every unital CPTP channel E_A, provided both rho_A and E_A(rho_A) are nondegenerate, the entropy-based diagonal discord S(pi_A rho_AB)-S(rho_AB), using each state's own marginal spectral projections, is nonincreasing under E_A tensor id_B. This settles precisely the frozen source.md/problem.md domain, including rank-deficient global states and arbitrarily small positive marginal gaps. |
| **Proposed contribution** | Exact proof of the entire frozen nondegenerate two-qubit/unital-CPTP inequality via channel-image compatibility with output marginal pinching and the quantum relative-entropy Pythagorean identity. Channel/dephasing commutation is unnecessary for this entropy-based claim. |
| **Limitations / bottlenecks** | 2026-10-12 exact-title and diagonal-discord/unital/monotonicity/counterexample/conjecture/proof/relative-entropy/pinching/noncommuting/Pythagorean searches; latest S1 version record and relevant full primary passages checked; S2 actual v4 primary PDF/text rechecked. No later exact resolution identified, but no exhaustive citation graph or priority guarantee. Primary and raw query evidence preserved. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00004-p05/paper.pdf) · [TeX](../../projects/phys-00004-p05/manuscript/main.tex) · [Code / data](../../projects/phys-00004-p05) · [Author handoff](../../projects/phys-00004-p05/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00004-p05/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00004-p06 · Global optimality of every-jump resetting for a Cauchy flight: a computer-assisted survival comparison</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Within the reset-before-jump Cauchy search model, Q2>=Q1^2 selects reset before every jump as the unique optimum among constant Bernoulli resetting rates; interior reset-rate optimization cannot lower the mean passage time, even at equality of the two-step criterion. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every finite b>=0 in the unit Cauchy reset-before-jump killed walk, Q2(b)>=Q1(b)^2 implies T_b(r)>T_b(1)=1/\[1-F(b)\] for every0<r<1; r=1 is equality. |
| **Proposed contribution** | Computer-assisted proof of the complete frozen unit-Cauchy implication for every finite b>=0 and every 0<r<=1, strengthened to strict interior comparison. A finite survival enclosure for orders3..9 plus exact zero-barrier induction gives all-order coefficient dominance; a separate finite/analytic exclusion proves the antecedent cannot hold for b>=1.809. |
| **Limitations / bottlenecks** | Current exact-title/identifier, Cauchy/global/sufficient/proof/conjecture and later-result searches on2026-10-12; primary originalv1 full HTML, Bonomo-Pal geometric convention and later2507.11196v1 full HTML rechecked. No exact later resolution located. Journal fulltext retrieval failed; targeted primary-PDF indexing still locates the conjecture, but no full version comparison is claimed. Abstract-only newer lead and inaccessible neighboring2D paper are recorded. Novelty/priority remain provisional for fresh referee review. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00004-p06/paper.pdf) · [TeX](../../projects/phys-00004-p06/manuscript/main.tex) · [Code / data](../../projects/phys-00004-p06) · [Author handoff](../../projects/phys-00004-p06/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00004-p06/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00004-p08 · Arbitrarily clustered hot spots on bridgeless quantum graphs</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | For homogeneous standard-Kirchhoff network diffusion, the hottest/coldest set of the unique slowest nonconstant mode does not impose any positive universal lower bound relative to network metric diameter, even when every edge lies on a cycle. This is a model prediction with constant diffusivity, without a fixed-volume or bounded-degree constraint. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every real epsilon>0 there is a finite connected compact positive-length standard-Kirchhoff metric multigraph Gamma with every edge on a cycle, diameter 1, simple first positive eigenvalue mu2, and complete global maximum/minimum union M satisfying diam(M)<epsilon. Explicit witness: for m=max(4,ceil(36/(pi^2*epsilon^2))), h=atan(1/sqrt(m))/pi, take a central tree with two long arms 1/2, two stems h to fan hubs, and m leaves of length 2h per hub; replace every edge by two equal parallel copies. Its simple mu2=\[atan(1/sqrt(2m+1))/h\]^2, its full metric diameter is 1, and its complete extrema union is exactly the 2m fan leaf vertices of diameter 6h<epsilon. This is the original Conjecture 8.9 no-bridge scope, allowing articulation vertices and no fixed volume/degree restriction. |
| **Proposed contribution** | An explicit one-integer uniformly doubled lengthened split-tree family proves the full printed existence statement: for m>=4, h=atan(1/sqrt(m))/pi, mu2=\[atan(1/sqrt(2m+1))/h\]^2 is simple, the exact complete extrema union has diameter 6h, and the actual doubled metric diameter is 1. m=max(4,ceil(36/(pi^2*epsilon^2))) makes 6h<epsilon for every epsilon>0. |
| **Limitations / bottlenecks** | Fresh bounded primary-source searches and exact-transfer comparison on 2026-10-12, recorded in evidence/research-pass1-literature.md and raw web-01 through -08. Current official original v4, survey v3, and same-authors higher-dimensional v2 were checked. No direct later resolution was identified; incomplete indexing and other terminology limit any priority claim. candidate_novel is provisional and requires a fresh referee novelty/significance check. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00004-p08/paper.pdf) · [TeX](../../projects/phys-00004-p08/manuscript/main.tex) · [Code / data](../../projects/phys-00004-p08) · [Author handoff](../../projects/phys-00004-p08/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00004-p08/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00005-p06 · An eighth-order inverse-response filter in a ten-site quantum walk</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | The same autonomous ten-site model and tau=2pi achieve one higher absolute response order, hence seventh rather than sixth conditional inverse-state power in gamma under the stated spectral and normalization factors. Couplings remain of order one, with a larger leading scalar success coefficient. Matched full-propagation samples show much smaller error at similar norm(H)*t; no complete algorithmic or hardware speedup is asserted. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For the exact R=4 ten-site zero-diagonal open Hermitian Jacobi chain of source.md/problem.md, there exist fixed positive couplings specified by the unique cancellation root in evidence/research-root-certificate.json, tau=2pi, a nonzero real linear coefficient ell in (-1.078612,-1.078611), x0=1/16 and C=131072002 such that &#124;<10&#124;exp(-i tau T4(x;J))&#124;1>-i ell x&#124;<=C*x^8 for every 0<x<=x0. This is the precise R=4 existence resolution, including the high-energy branch; it does not settle the original author all-R conjecture. |
| **Proposed contribution** | An explicit exact-root specification of positive fixed R=4 couplings cancels cubic, quintic and septic low-energy coefficients simultaneously, retains a nonzero linear response, and gives the full-amplitude bound &#124;a4-i ell x&#124;<=131072002*x^8 for every 0<x<=1/16. Root existence is certified by interval contraction; the oscillatory high branch is bounded separately. |
| **Limitations / bottlenecks** | Primary version pages were reopened on 2026-10-12 around 17:32-17:34 UTC: 2508.06611v1, 2512.08141v1 and 2510.06316v3. Reread the original Conjecture 1/Table I/Appendix A, successor Theorem 4.1/Sections 4.2 and 6, and competitor v3 Section 4.4/Proposition 19/Corollary 20. Targeted exact-title/identifier/author searches identified no direct later resolution in this limited screen. The competitor uses repeated Hamiltonian-QSVT queries. Coverage is not exhaustive, absence of a hit does not prove priority, and candidate_novel requests independent novelty/significance review. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00005-p06/paper.pdf) · [TeX](../../projects/phys-00005-p06/manuscript/main.tex) · [Code / data](../../projects/phys-00005-p06) · [Author handoff](../../projects/phys-00005-p06/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00005-p06/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00007-p05 · Exact conditional min-entropy of two-qubit unitary channels with white noise</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | The conditioning-channel TP restriction has zero cost for this single-use family; its conditional channel min-entropy is computed exactly from the pure-unitary Choi Schmidt spectrum rather than by a constrained SDP. Units are bits and the resource interpretation uses trivial output Hamiltonians. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every U in U(4) and real p in \[0,1\], let Omega=(1-p)&#124;u><u&#124;+p I16/16 be the normalized Choi state in the grouped X=RA A,Y=RB B order, rho_U=Tr_X &#124;u><u&#124; and L=Tr sqrt(rho_U). For the exact SDPs in problem.md, including Tr_B Q=(Tr Q)I_RB/2 in t, s(Omega)=t(Omega)=(1-p)L^2+p/4. A common optimizer is Q=(1-p)L sqrt(rho_U)+(p/16)I4. Hence S_infty\[A&#124;B\]_N=H_min(X&#124;Y)_Omega-1 for every frozen noisy two-qubit gate, including degeneracies, deficient Schmidt rank and p endpoints. This is a proposer proof awaiting fresh referee review. |
| **Proposed contribution** | Settle the frozen all-U(4), all-p in \[0,1\] noisy identity and supply explicit common optimum (1-p)(Tr sqrt(rho_U))^2+p/4 with a common TP-feasible optimizer and matching state-dual witness. |
| **Limitations / bottlenecks** | 2026-10-12: current official arXiv pages/fulltext confirm v2 for both decisive preprints; decisive local source sections re-read; exact identifier/title, author/noisy, white-noise, depolarized-pure, pseudopure and Schmidt/min-entropy queries. No later primary resolution verified; bounded searches do not establish global priority; independent referee comparison remains required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00007-p05/paper.pdf) · [TeX](../../projects/phys-00007-p05/manuscript/main.tex) · [Code / data](../../projects/phys-00007-p05) · [Author handoff](../../projects/phys-00007-p05/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00007-p05/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00007-p06 · The sharp overlap threshold for antidistinguishability of five pure states</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | The overlap-only universal guarantee for ideal single-copy five-state zero-error exclusion is sharp. Arbitrarily small increases above sqrt(3/8) admit non-excludable states, with certified positive uniform-prior error lower bound s*eta/5. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For five arbitrary normalized complex pure states in C^5, allowing dependence, the infimum t5 of maximum pairwise overlap modulus over non-antidistinguishable tuples equals sqrt(3/8), with single-copy unrestricted PSD POVMs and zero effects permitted. An explicit rank-three family has every squared overlap m and is non-antidistinguishable for every real 3/8<m<2/5. Its exact physical dual certificate gives uniform-prior optimum exclusion error at least s*eta/5>0 as defined in evidence/five-state-proof.md. The published bound includes the boundary; this is an infimum approached from above, not an attained non-excludable minimum. No n>=6 or exact optimum error claim. |
| **Proposed contribution** | An explicit rank-three five-state pure-state family with every squared pairwise overlap m in (3/8,2/5), and an exact positive-trace physical exclusion dual witness for every such m, proves t5=sqrt(3/8). |
| **Limitations / bottlenecks** | 2026-10-12 primary recheck of arXiv:2609.17411v1 Section 1.1 and Section 3; retained publisher Quantum 9,1622 full PDF, Corollary 5.4, Section 6 and equation (2). Bounded targeted searches and precise comparison are preserved; no later exact resolution found, but exhaustive priority is not certified. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00007-p06/paper.pdf) · [TeX](../../projects/phys-00007-p06/manuscript/main.tex) · [Code / data](../../projects/phys-00007-p06) · [Author handoff](../../projects/phys-00007-p06/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00007-p06/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00007-p14 · Extreme excursions and terminal-sign retention in stationary Brownian resetting</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Quantifies retention of a stationary extreme excursion by endpoint-sign monitoring; reset-position dependence enters through terminal-sign renewal, and at zero reset the coefficient is halfway between the two published neighboring coefficients. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every fixed T>0,r>0,a real in the stationary zero-drift variance-t reset Brownian model, exp(alpha u)P(M_T>u,Y_T>0) converges to exp(alpha a)\[Phi(alpha sqrt(T))+r integral_0^T Phi(alpha sqrt(s))q_a(T-s)ds\], with the explicit remainder (2) in joint-tail-proof.md for u>max(a,0), proving the published conjectured bounds. |
| **Proposed contribution** | Explicit all-fixed-parameter joint maximum/positive-terminal coefficient with post-reset sign probability q_a, plus a Gaussian-tail finite-u remainder; establishes the named conjecture and its bounds within the frozen zero-drift stationary Brownian model. |
| **Limitations / bottlenecks** | 2026-10-12 fresh arXiv version history and v3 Remark 3 and publisher Remark 3, exact title/identifier and stationary joint-tail resolution searches; local fulltext NJP sections 3.1.2, 4.1 and 5 and equations 22-30,78-92. No later resolution identified; priority beyond this bounded coverage remains unverified. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00007-p14/paper.pdf) · [TeX](../../projects/phys-00007-p14/manuscript/main.tex) · [Code / data](../../projects/phys-00007-p14) · [Author handoff](../../projects/phys-00007-p14/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00007-p14/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00032-p01 · A resource-dependent thermodynamic uncertainty relation for three-port coherent conductors</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Knowing that the hardware has only three single-channel normal leads gives a strictly stronger lower bound on actual total dissipated heat entropy from one measured particle-current mean and full count variance. The bound includes all reservoirs and does not require event entropy, extra activity, a reversed experiment, small bias or hidden probes. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every stationary elastic number-preserving noninteracting normal-fermion conductor in the exact C3 class of source.md/problem.md, with three physical reservoirs, at most one open channel per lead, a finite Hermitian sample and causal normal leads, fixed finite chemical potentials and strictly positive temperatures, finite J=abs(chi0 prime(0))>0, full count-variance rate C2=chi0 double-prime(0)>0 and actual total reservoir heat entropy sigma>0, sigma/k_B >= (9/10) J asinh(J/C2). The complete analytic-plus-integer-interval argument covers both current signs, both three-cycle orientations, every 3x3 unitary scattering matrix including reflected closed channels, arbitrary legal energy dependence, and signed energy integration. An enclosed exact rational psi0 witness is below 9/10, hence kappa3>=9/10>psi0. This proposed proof answers the original strict-improvement question without determining optimal kappa3 or claiming saturation; fresh referee acceptance is pending. |
| **Proposed contribution** | A proposed computer-assisted full-scope bound sigma/k_B >= (9/10) J asinh(J/C2) for every legal normal elastic noninteracting three-reservoir conductor with at most one channel per lead, arbitrary finite thermal/chemical biases, generic broken-reciprocity scattering and signed energy integration. Exact psi0 is below 9/10 by a certified rational witness. Optimal kappa3 is not determined. |
| **Limitations / bottlenecks** | Bounded current primary recheck on 14 October 2026 UTC: S1 current v2, S5 v1 and S4 July-2026 v1 histories/full defining statements; S3 current v3 and October-2026 publisher abstract retaining linear-response/probe premises; previously preserved S2,S6,S7 defining scopes; fresh primary published S8 PDF/current arXiv v3, including its nonlinear Eqs.(84)-(87),(95)-(96). Exact titles and three-terminal/nonlinear/single-channel/asinh/9/10/Birkhoff/cycle terms searched. No exact restricted resolution was identified; absence of hits is not exhaustive openness or priority proof. Fresh referee and eventual human review must assess novelty/significance independently. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00032-p01/paper.pdf) · [TeX](../../projects/phys-00032-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00032-p01) · [Author handoff](../../projects/phys-00032-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00032-p01/manuscript/REPRODUCIBILITY.md) |

**Related results / preserved versions**

- [phys-00030-p01](../../projects/phys-00030-p01): A finite nonreciprocal full-current large-deviation counterexample is not the resource-dependent three-port noise/entropy theorem. The target bound, observable and hypothesis sets differ.

</details>

<details>
<summary><strong>phys-00036-p01 · Algebraic endpoint densities are the transfer-matrix charges in regular Yang–Baxter chains</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Identifies the quantum-group algebraic densities with the actual prescribed local conservation-law hierarchy, excluding untracked lower-charge or scalar mixing and removing the unproved identification in applications of the source's undeformed recurrence. No new particle, phase, experiment, all-order long-range deformation or measured algorithmic speedup is asserted. |
| **Original question** | proved at the stated scope |
| **Result and exact original-problem scope** | For every finite-dimensional complex V and every formal/analytic source-regular Yang--Baxter R(u,v) with R(u,u)=P and R12(u,v)R21(v,u)=I, for every k>=2, BOTH Conjecture 2.7 block-R endpoint density differences are equivalent to a density of Q_k^(L)=partial_u^(k-2)(t_L^-1 t_L prime)&#124;0 modulo exactly I tensor m - m tensor I. Their cyclic sums equal the prescribed raw transfer charges on every homogeneous untwisted periodic chain L>=k. This is the complete undeformed source identity, including general non-difference R and minimal L=k; no higher-order long-range or other-boundary extension is claimed. |
| **Proposed contribution** | A finite-chain ordered-product and rooted connected-coefficient proof of BOTH endpoint formulas for every source-allowed finite-dimensional regular braiding-normalized Yang--Baxter R, every k>=2 and every periodic L>=k, plus a constructive tensor-word proof of the exact local-gradient equivalence. |
| **Limitations / bottlenecks** | On 14 October 2026 checked current arXiv original history (still v2, 5 June 2026), bounded exact identifier/title/conjecture and neighbour searches, and inspected the defining source loci, BBL Eq.(2.16), 2021 Appendix A Eqs.(A.1)--(A.7), and older Links/Takizawa ladder constructions. Raw retrievals and selected primary full texts are preserved. No later resolution was verified; search absence is not proof of openness and comprehensive priority is not established. Candidate novelty requires fresh referee assessment. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00036-p01/paper.pdf) · [TeX](../../projects/phys-00036-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00036-p01) · [Author handoff](../../projects/phys-00036-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00036-p01/REPRODUCIBILITY.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

The act of packaging grants no additional license to manuscripts, code or data. Consult the original author handoff and applicable rights. No submission, peer-review or acceptance is implied.
