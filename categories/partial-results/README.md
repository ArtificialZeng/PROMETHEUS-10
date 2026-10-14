# PROMETHEUS-10 · Partial result

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

## Partial result

<details>
<summary><strong>phys-00002-p01 · How much noise does a qubit need?</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Lindblad generators describe memoryless open-system dynamics. Can a single jump operator reach the full boundary of the qubit population-transfer region? |
| **Result and original-problem scope** | A certified finite-radius local optimality result near the a=1/2 one-jump stationary point, against rank-at-most-two perturbations. The original global question remains open. |
| **Proposed contribution** | An explicit interval certificate turns a numerical stationary point into a checkable local exclusion region for competing generators. |
| **Limitations / bottlenecks** | Local radius 10^-4; this does not establish the global embedding boundary or exclude distant competitors. |
| **PDF and source** | [PDF](../../projects/phys-00002-p01/paper.pdf) · [TeX](../../projects/phys-00002-p01/manuscript/main.tex) · [Bib](../../projects/phys-00002-p01/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p01) · `python reproducibility/reproduce.py --project phys-00002-p01` |

</details>

<details>
<summary><strong>phys-00007-p01 · When channel boundariness multiplies exactly</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Boundariness measures proximity to the boundary of a convex channel set. Tensor products may expose structure invisible in one copy. |
| **Result and original-problem scope** | Exact multiplicativity is proved within an explicit two-parameter full-rank non-unital qubit Choi family, &#124;s&#124;, &#124;t&#124; ≤ 1/5. |
| **Proposed contribution** | Symbolic Choi, Sturm and LDL checks support an explicit family where the tensor-product optimum is tractable. |
| **Limitations / bottlenecks** | The general problem remains open. Historical submission-bundle gate failed evidence/manuscript binding; PDF is included as an archived draft, not a gate-cleared release. |
| **PDF and source** | [PDF](../../projects/phys-00007-p01/paper.pdf) · [TeX](../../projects/phys-00007-p01/manuscript/main.tex) · [Bib](../../projects/phys-00007-p01/manuscript/references.bib) · [Code / data](../../projects/phys-00007-p01) · `python reproducibility/reproduce.py --project phys-00007-p01` |

</details>

<details>
<summary><strong>phys-smallmac00000-p13 · Finite total dephasing and an isolated natural occupation in an open XX chain</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 开放 XX/XY 链加入最小可控非均匀耗散后，哪些耗散剖面仍允许协方差矩阵谱的闭式表达？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the open XX spin chain and stationary covariance specified in problem.md, odd N with centered dephasing defect, J=1, kappa=4, mu=1/2, eta=5, and either gamma_0=c/N or c/(N-1), every fixed finite c>0 has nearest natural-occupation spacing from 1/2 tending to 1/(36+4c) and central-orbital IPR tending to 51/125 as stationarity is taken before N tends to infinity. Explicit finite bounds (A),(B) are in evidence/salvage-aefa2c1a93e3/bounded-noise-derivation.md. No claim about a Liouvillian gap, full-state Gaussianity, experiment, or the full XX/XY profile classification. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00000-p13/paper.pdf) · [TeX](../../projects/phys-smallmac00000-p13/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00000-p13) · [Author handoff](../../projects/phys-smallmac00000-p13/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00000-p13/manuscript/repro/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00000-p14 · A second-order obstruction to localized edge-mode continuation in a non-Hermitian interacting Kitaev chain</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 非厄米相互作用 Kitaev 链在已知可解区域之外，能否得到一个新的精确相边界、例外点条件或反例？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | At t=1, g=(1-i)/5, eta=1/5, mu=0 on the original odd-left-dimerized half-line, Q0=sqrt(1-rho^2) sum_(n>=0) rho^n alpha_(2n+1), rho=3(1-i)/10, has a unique exponentially localized parity-odd normalized first-order continuation Q1. No exponentially localized Q2 solves \[H0,Q2\]=-\[V,Q1\]. Thus there is no twice-differentiable exact commutator-zero-mode continuation from Q0 whose first two Taylor coefficients are exponentially localized and whose square normalization holds to first order. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00000-p14/paper.pdf) · [TeX](../../projects/phys-smallmac00000-p14/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00000-p14) · [Author handoff](../../projects/phys-smallmac00000-p14/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00000-p14/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00004-p01 · Optimal single-letter private information of the dephrasure channel on a noise interval</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 退相位—擦除信道：对称双混合态编码是否已经达到单字母私有信息最优？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For every p in \[27/250,221/2000\] and q=3p, and every finite ensemble of legal qubit density matrices with arbitrary nonnegative normalized weights and arbitrary mean, the full-environment dephrasure private information obeys Pi(E)<=B(p)-(3/250)Var_w(z_a)-(1/1000)(sum_a w_a z_a)^2, where z_a=Tr(Z rho_a) and B is the immutable source symmetric-code maximum. In particular P^(1)(N_p,3p)=B(p) on this subinterval. The rest of the original p interval and regularized private capacity remain unresolved. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00004-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00004-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00004-p01) · [Author handoff](../../projects/phys-smallmac00004-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00004-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00003-p02 · A rank-three projection bound for the quantumness of spin-1 states</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | spin-1混合态：相干态凸包距离是否受同最小Bloch本征值的纯态控制？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | The rank3 nearest-Bloch projection bound Q<=sqrt(3/8)(-lambda), equality iff its unit kernel vector has v0=0, and consequent restriction of any source Eq41 counterexample to rank2 nearest Bloch matrices. Ranks concern the 4x4 real moment matrix of the unique closest state in the complete spin-coherent hull. The source all-state inequality is unresolved; zero-dipole formulas are illustrative corollaries and rank2 exploratory formulas are outside the claim. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00003-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00003-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00003-p02) · [Author handoff](../../projects/phys-smallmac00003-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00003-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00007-p03 · A two-pineapple envelope for split-core threshold random walks</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 阈值输运网络中，单核心菠萝结构是否已经最慢？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For every positive integer s,q,t, put n=s+t+q+3. In the frozen non-lazy threshold-graph random-walk model, each construction code 01 0^t 1^s 0^q 1 and 0 1^s 0^t 1 0^q 1 has Kemeny's constant strictly less than max{F_n(s+1),F_n(s+t+1)}, and hence strictly less than or equal to the global pineapple bound B_n. The original conjecture for all legal threshold codes remains unresolved. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00007-p03/paper.pdf) · [TeX](../../projects/phys-smallmac00007-p03/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00007-p03) · [Author handoff](../../projects/phys-smallmac00007-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00007-p03/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00010-p01 · Exact flat-noise transition rays from Hadamard involutions in four-level systems</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 四能级酉跃迁掺入均匀噪声后，能否总由另一个单次酉跃迁实现？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For any order n with a real normalized Hadamard F and any real orthogonal projector P, U=F(I-2P) has the exact flat-noise transition ray &#124;V_lambda,ij&#124;^2=(1-lambda)&#124;U_ij&#124;^2+lambda/n for every lambda in \[0,1\], with V_lambda=sqrt(1-lambda)U+i sqrt(lambda)F unitary. Within this fixed real quadrature ansatz the condition is also necessary: F^T U is a symmetric orthogonal involution. At n=4 the rank-two projector component contains a locally four-dimensional image of noncirculant B(U) matrices. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00010-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00010-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00010-p01) · [Author handoff](../../projects/phys-smallmac00010-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00010-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00010-p04 · A seven-$T$ fixed measurement accessing 220 four-qubit Pauli directions</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 四qubit的单设置完整层析，七个T门是否仍然不够？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the explicitly specified fixed four-input-qubit, seven-&#124;0>-ancilla Clifford+T circuit in evidence/seven-t-witness.json, using seven T or T-dagger gates and retaining all 2048 terminal computational-basis outcomes, the effective POVM operator span and frame have exact real rank 220. The original universal seven-T informational-incompleteness question remains unresolved. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00010-p04/paper.pdf) · [TeX](../../projects/phys-smallmac00010-p04/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00010-p04) · [Author handoff](../../projects/phys-smallmac00010-p04/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00010-p04/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00010-p02 · Weak regulation increases stationary abundance noise in a three-species stochastic feedback ring</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 三组分随机生化反馈环，是否至多一个组分能低于Poisson噪声？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the exact infinite-state three-species unit-birth feedback ring with fixed a_i,tau_i>0 and bounded nonconstant h_i:N_0->R, put f_i(n)=a_i+epsilon h_i(n). For &#124;epsilon&#124; H_k<=a_k/2, each stationary Fano factor obeys F_i(epsilon)-1=epsilon^2 S_i/a_i+R_i(epsilon), where S_i=integral_0^infty exp(-t/tau_i) Cov_0(h_i(Y_{i-1}(0)),h_i(Y_{i-1}(t)))dt>0, Y_{i-1} is a stationary baseline immigration-death chain, and &#124;R_i(epsilon)&#124;<=K_i&#124;epsilon&#124;^3 for the explicit finite K_i in evidence/research-pass3.md. Consequently all three F_i>1 for each fixed triple at sufficiently small nonzero epsilon. No claim is made for arbitrary coupling strength; the original conjecture remains unresolved. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00010-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00010-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00010-p02) · [Author handoff](../../projects/phys-smallmac00010-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00010-p02/REPRODUCE.md) |

**Related results / preserved versions**

- [phys-00018-p01](../../projects/phys-00018-p01): The two-gene finite-RNA-lifetime matched-baseline theorem is not the three-species direct-abundance feedback-ring weak-regulation result. The intermediate RNA state, number of species, baseline and whole-space remainder are different.

</details>

<details>
<summary><strong>phys-smallmac00011-p02 · Directional stability of the reverse-depolarizing entanglement-assistance benchmark for qubit entanglement-breaking channels</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 完全破坏纠缠的 qubit 信道，预共享纠缠的容量增益是否仍不超过已知反向去极化基准？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | Let D be the reverse-depolarizing qubit channel D_(4/3), and let Psi be any fixed qubit entanglement-breaking channel. For Phi_e=(1-e)D+e Psi as e decreases to zero through positive values, put c=<Omega&#124;J_Psi/2&#124;Omega>. If c>0, then K_* chi(Phi_e)-C_E(Phi_e)=c e log2(1/e)+O_Psi(e). If c=0, Psi has Bloch action r -> -Q r with Q positive semidefinite and trace one, and the gap is \[K_*/2\](lambda_max(Q)-1/3)e+O_Psi(e^2). The gap is strictly positive for all sufficiently small e>0 whenever Psi differs from D; if Psi=D, equality holds identically. All capacities are fully optimized and C=chi for these EB maps. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00011-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00011-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00011-p02) · [Author handoff](../../projects/phys-smallmac00011-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00011-p02/manuscript/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00012-p02 · A hypocycloid spectral bound for circulant unistochastic matrices without symmetric amplitudes</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 五站点环的转移概率具有平移对称性，是否总能选择同样对称的酉实现？ |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | Let d>=2 and let B be a d-by-d circulant bistochastic matrix with B\[i,j\]=b\[(i-j) mod d\]. If B\[i,j\]=&#124;U\[i,j\]&#124;^2 for some arbitrary U in U(d), then for every Fourier mode k, lambda_k(B)=tr(D_k U D_k^dagger U^dagger)/d belongs to the closed unit d-hypocycloid H_d. For d=5, the circulant matrix generated by b=(209/500,3/40,7/500,3/40,209/500) satisfies every row and column bracelet inequality but is not unistochastic, because lambda_1=((465+343*sqrt(5))/2000) exp(i*pi/5) lies strictly outside H_5. Consequently, a five-hypocycloid violation cannot supply the general-unitary-versus-circulant-unitary separator required to disprove P_5. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00012-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00012-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00012-p02) · [Author handoff](../../projects/phys-smallmac00012-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00012-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00019-p01 · Exact signed-sum spectral locus of a six-term three-qubit Pauli Hamiltonian</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 三比特 Pauli 模型出现自由费米谱的完整耦合流形 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For every real coupling vector (a,b,c,d,e,f), the eight-level spectrum of H=a Z_2+b Y_1 X_2+c X_1 Y_2+d Z_1 Y_3+e Y_1 X_3+f Z_3 is, with multiplicity, the signed-sum spectrum of three nonnegative one-particle energies if and only if c d (a^2-f^2)(b^2-e^2)=0; equivalently the locus is exactly c=0, d=0, a=plus-or-minus f, or b=plus-or-minus e. This claim is spectral and does not claim a uniform structural CAR-mode construction. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00019-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00019-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00019-p01) · [Author handoff](../../projects/phys-smallmac00019-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00019-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00020-p01 · The largest Liouvillian exceptional point need not maximize the spectral gap: An exact two-qubit counterexample</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 固定两比特 XYZ Liouvillian 的谱隙最优耗散是否落在最大例外点 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the fixed two-qubit XYZ GKSL generator in problem.md with gamma=3/5, Delta=2/5, and Gamma>0, the complete nonzero Liouvillian spectral gap satisfies g(73/10)>3/2>1>g(8). Since the reproduced largest positive Liouvillian exceptional point is Gamma_cr=8, Gamma=8 is not a global maximizer of g. The actual global maximizer is not determined by this claim. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00020-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00020-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00020-p01) · [Author handoff](../../projects/phys-smallmac00020-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00020-p01/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00020-p02 · Strict separable non-saturation for a seven-state prepare-and-measure witness</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 最小绝对纠缠集见证的可分上界能否严格低于四分之三 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the exact seven-state extended ensemble and prepare-and-measure witness of arXiv:2609.13075v1 Sec. VI.D in the two-qubit separable-preparation domain, Q_SEP is strictly smaller than 3/4. This result proves non-saturation but neither computes Q_SEP nor supplies an explicit numerical lower bound on the positive gap. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00020-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00020-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00020-p02) · [Author handoff](../../projects/phys-smallmac00020-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00020-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00021-p02 · A unique cubic-coupling cancellation locus for collinear constant-vorticity capillary–gravity triads</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 常涡度共振三波的涡度公式与耦合零点符号审计 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | In the reproduced Ivanov-Martin arXiv:1911.05213v1 co-propagating cubic model, for every g>0, sigma>0 and distinct k1,k2>0 with k3=k1+k2, the unrestricted real dispersion-plus-resonance system has exactly the two common-sign frequency solutions in Eq. (3) of evidence/resonance-classification.md, related by (omega_j,gamma)->(-omega_j,-gamma). With q_j=k_j(g+sigma*k_j^2), ell=q3-q1-q2, N=ell^2-4q1q2 and D=2ell\[q3^2-(q1-q2)^2\], the selected positive-frequency sheet has the unique physical vorticity gamma=-N/sqrt(D); the companion root belongs to the genuine all-negative-frequency sheet, not an algebraic artifact. On either sheet C=\[16q1q2(q3-q1)(q3-q2)-ell^4\]/D. For every positive pair (k1,k2), exactly one positive r=g/sigma makes C=0, namely the unique positive root of Eq. (9) in the proof; at that zero gamma<0 on the positive-frequency sheet and gamma>0 on its sign-reversed companion. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00021-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00021-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00021-p02) · [Author handoff](../../projects/phys-smallmac00021-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00021-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00021-p03 · Comment on “Band topology of the breathing kagome lattice”</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Breathing-kagome 角态的 A 子晶格公共核 iff 扰动判据 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the Fig. 3 interpolation of Geschner et al. at t=0 and t'=1, the author-raster 15-site invariant corner component has chi(E,lambda)=(E-1)^2 P6(E,lambda)P7(E,lambda), coefficient gcd exactly (E-1)^2 in Q\[E\], chi(E,0)=E(E-1)^8(E+1)^4(E+2)^2, and chi(E,1)=(E-1)^8(E+1)^6(E+2). Thus exactly 13 eigenvalue roots per corner, counted with algebraic multiplicity, are nonconstant under the interpolation, correcting the source's count 12; the three pairwise-disjoint D3-related components verified in the N=20 flake give 39 rather than 36. Secondarily, for the separate t=0.1, t'=1 N=20 system, the previously certified opposite-mirror-parity crossing and exact uniform-edge transfer equations remain at their finite/restricted scopes. No thermodynamic result or solution of the original general connectivity iff is claimed. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00021-p03/paper.pdf) · [TeX](../../projects/phys-smallmac00021-p03/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00021-p03) · [Author handoff](../../projects/phys-smallmac00021-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00021-p03/README_REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00022-p01 · Local stability of a two-copy entanglement-of-purification ansatz at the von Neumann boundary</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 经典二比特态在冯诺依曼阶的二副本纯化局部稳定性 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the Eq. (15) state rho_r at r=1/2 and base-2 von Neumann order alpha=1, in the fixed minimal ancillary split (d_A',d_B')=(4,4), the product-canonical two-copy purification W_0=I_16 is a strict local minimum modulo the local ancillary U(4) x U(4) orbit over the complete complex orthonormal-flag manifold U(16), including support-opening directions. This does not assert global optimality, larger-ancilla local stability, or additivity. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00022-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00022-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00022-p01) · [Author handoff](../../projects/phys-smallmac00022-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00022-p01/manuscript/README.md) |

**Related results / preserved versions**

- [phys-00004-p09](../../projects/phys-00004-p09): Both concern two-copy binary-state entanglement of purification. big_mac proves pathwise positivity for every positive nonproduct binary table without a common neighborhood; small_mac proves a full U(16) strict local minimum modulo gauge at r=1/2. Neither recorded statement contains the other complete statement. Keep both, link them, and do not infer global additivity.

</details>

<details>
<summary><strong>phys-smallmac00022-p02 · Exact Tsirelson bound for a three-output Bell functional</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 三输出 Bell 泛函 I3 的精确 Tsirelson 证书与等号刚性 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the no-dagger three-output Bell functional I3 of arXiv:2606.21362v3 Eq. (6), every tensor-product strategy of arbitrary local dimension with three-output projective measurements satisfies I3<=4. The bound is attained by the stated maximally entangled qutrit strategy. Equivalently, 4*1-I3 has the submitted exact rank-16 Q(omega) noncommutative SOS on the 35-word 1+AB span. Equality rigidity, self-testing, robustness and randomness certification are not claimed. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00022-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00022-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00022-p02) · [Author handoff](../../projects/phys-smallmac00022-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00022-p02/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00022-p03 · Exact all-parameter spectral-gap certificates for deformed-EPR Hamiltonians on small subdivided stars</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | 树上变形 EPR 哈密顿量的谱隙下界与等号分类 |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | Let T_q be the tree with q ordinary leaves adjacent to C and two further edges C--A--B. For every q in {1,2,3,4,5,6} and every real 0<s<1, the coefficient-one Hamiltonian H_s=-sum_e (&#124;00>+s&#124;11>)(<00&#124;+s<11&#124;)_e has finite-volume spectral gap Delta(T_q,s)>1-s^2. |
| **Proposed contribution** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limitations / bottlenecks** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-smallmac00022-p03/paper.pdf) · [TeX](../../projects/phys-smallmac00022-p03/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00022-p03) · [Author handoff](../../projects/phys-smallmac00022-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00022-p03/reproducibility/README.md) |

**Related results / preserved versions**

- [phys-00035-p01](../../projects/phys-00035-p01): The small_mac result is an all-s certificate for q=1..6 one-hub subdivided stars. big_mac proves a full-gap, tail-controlled two-hub family for k>=100 in eta=theta/k, theta in [1/2,2]. Different topology, size and parameter quantifiers; neither is an all-graph proof.

</details>

<details>
<summary><strong>phys-00002-p08 · A resource obstruction for qubit measurement self-testing with matched kernel preparations</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Reweighting all probabilities at the established four matched-exclusion-state reference cannot reduce auxiliary settings from three to two. Any such reduced-resource protocol must depart from those reference preparations or change the physical resources/premises. The obstruction addresses target-only certification, not merely separate state self-testing. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For any extremal four-outcome complex-qubit reference POVM with four matched pure kernel-state preparations, and any binary auxiliary collection whose reference observable Bloch vectors span a space of dimension at most two, every real linear functional on the complete prepare-and-measure probability table that is globally maximized at that reference has an admissible maximizing realization with the same auxiliary measurements and a target having at most three nonzero effects. Thus no such witness self-tests the four-outcome target, even when only the target is to be certified. This includes two projective auxiliaries and two arbitrary binary POVMs. The reference kernel-state restriction is essential to the claimed scope; the unrestricted resource conjecture remains unresolved. |
| **Proposed contribution** | Necessary supporting-witness normal form c_ij=l_i-k_j delta_ij with k_j>=0 for arbitrary target probability coefficients at any four matched kernel-state reference; using it, a universal explicit <=3-nonzero-effect same-score target replacement whenever the auxiliary Bloch span has dimension<=2. Includes arbitrary binary POVMs and zero auxiliary-state-gradient cases; original unrestricted minimality remains unresolved. |
| **Limitations / bottlenecks** | Fresh primary screen2026-10-12UTC before legacy extension:2406.08661v1/current official record;2020 publisher fulltext;2306.07248v5 including official2025-11-01 revision;2306.00730v4;2603.01802v1;2503.13282v2/current2026-07-01 revision. Exact-ID and minimal/two/four-outcome/antipodal/state-exclusion/lower-bound searches. No equivalent result identified in checked passages; bounded screen, incomplete forward-citation coverage, no proof of priority or unrestricted openness. Novelty/significance remain for fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00002-p08/paper.pdf) · [TeX](../../projects/phys-00002-p08/manuscript/main.tex) · [Code / data](../../projects/phys-00002-p08) · [Author handoff](../../projects/phys-00002-p08/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00002-p08/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00002-p12 · Sharp lower bounds on current cumulant ratios in Markov rings with an irreversible bond</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Validates the proposed third/fourth current-ratio transport diagnostics throughout an irreversible-bond classical single-cycle class, including strong backward excursions elsewhere. It identifies a rigorously safe boundary sector; all-positive finite-affinity universality remains unresolved. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For every finite simple nearest-neighbor time-homogeneous Markov ring with N>=3, finite forward rates u_i>0, nonnegative finite reverse rates w_i and at least one w_i=0, the long-time signed one-cycle count cumulant rates satisfy c3/c1>=-1/16 and c4/c2>=-(1+sqrt(5))/10. Here c1,c2>0; arbitrary initial law and any counted bond yield the same ratios. Both constants are sharp over unbounded finite N. The original strictly positive bidirectional conjecture remains unresolved; no finite-N extremizer or interior bound is asserted. |
| **Proposed contribution** | An ansatz-free analytic proof of both winding-ratio lower bounds for every positive exponential-stage vector, mapped by the known passage-time theorem to every finite Markov ring with at least one irreversible bond and arbitrary remaining backward rates. Both constants are asymptotically sharp. |
| **Limitations / bottlenecks** | Targeted primary/current recheck on 2026-10-12, arXiv latest v4 and exact Appendix, author Fill theorem/remark, prior 2023 modular and 2025 heat/entropy neighbors, exact constants with proof/erratum/renewal/hypoexponential searches. No direct priority conflict found; this is bounded coverage, not a priority guarantee. Fresh referee must assess novelty and significance of proof upgrade. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00002-p12/paper.pdf) · [TeX](../../projects/phys-00002-p12/manuscript/main.tex) · [Code / data](../../projects/phys-00002-p12) · [Author handoff](../../projects/phys-00002-p12/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00002-p12/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00002-p13 · Sharp first-passage skewness and excess-kurtosis bounds for three-state cycles at large affinity</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Replaces rate-space numerical maximization by algebraic sharp limits on entropy-threshold timing asymmetry and excess tails in three-step dissipative cycles. Identifies an attaining half-affinity tilted-spectrum degeneracy and allows direct envelope evaluation at fixed dissipation. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the strictly positive finite-rate time-homogeneous N=3 periodic Markov ring and the large-threshold entropy-current FPT conventions of problem.md, at every finite A>=log(64), the separate sharp envelopes are U_S=sqrt(A) N(p_S)/V(p_S)^(3/2) and U_K=A Q(p_K)/V(p_K)^2. Here d=coth(A/4), H=(d^2+1)/(2d), t(p)=d p(2+p)/(1+2p)^2, zeta(p)=d^2 p^2/(1+2p)^3, V=H-2t, N=3H^2-1-6Ht+6zeta, and Q=3H(5H^2-3)-12(3H^2-1)t+12Ht^2+24Hzeta. p_S is the unique positive root of 4(d^2-1)p^2+(12d^2-4)p-(d^2-1)^2=0; p_K is the unique positive root of 8(d^2-1)p^3+(-4d^4+24d^2-12)p^2+(2d^4+12d^2-6)p-(d^2-1)^2(d^2+1)=0. Both bounds are attained by strictly positive finite rate vectors constructed in spectral-envelope-proof.md Section 5. This does not settle the original all-N/all-affinity problem or the kink locations. |
| **Proposed contribution** | Exact sharp upper envelopes for both large-threshold scaled FPT skewness and scaled excess kurtosis for every strictly positive three-state ring at every finite A>=log(64). They are specified by unique positive quadratic/cubic roots in d=coth(A/4), and explicit strictly positive rate vectors attain each bound. |
| **Limitations / bottlenecks** | Current primary arXiv history/HTML 2110.14540 and exact-claim/later-resolution searches rechecked 2026-10-12 before extension. Compared retained 1510.03279v1, full 2204.08421v4 definitions/Section III E/Appendix A, and 2025 JSP 192,126 publisher fulltext definitions. No equivalent envelope found in this bounded screen. Publisher version of the 2021 source and exhaustive citation tracking remain incomplete; priority is proposed, not certified. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00002-p13/paper.pdf) · [TeX](../../projects/phys-00002-p13/manuscript/main.tex) · [Code / data](../../projects/phys-00002-p13) · [Author handoff](../../projects/phys-00002-p13/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00002-p13/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00003-p07 · Uniform indexed spectral bounds near the five-photon resonance of the quantum Rabi model</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Certifies how the avoided-crossing lower branch stays below the conjectured indexed ceiling when the leading diagonal margin vanishes. Gives a rigorous gap envelope with relative error <=G/(3kappa), below 19.5% at G=0.1 and improving as G->0; no optical selection-rule or transfer-rate claim. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | In the exact unbiased quantum Rabi model of problem.md, write G=g/omega,d=Delta/omega,e_n^s=E_n^s/omega with omega>0. For every 0<G<=1/10 and -1<=c<=1, d=5/2-(5/4)G^2+cG^4 implies e_2^+<5/2-G^2. On d=5/2-(5/4)G^2-(5/64)G^4, the sorted full-operator levels satisfy &#124;e_2^+-(5/2-G^2-sqrt120*G^5/64)&#124;<=G^6/3 and &#124;e_3^+-(5/2-G^2+sqrt120*G^5/64)&#124;<=G^6/3. Delta sign reversal exchanges parity. No all-n, opposite-parity, universal spacing, exact-stationarity or experimental transition claim. |
| **Proposed contribution** | Explicit continuous-domain certificate for the sorted n=2 plus-parity upper bound near the five-photon resonance, with infinite-tail and index control; on fourth-order tuning, two indexed eigenvalue enclosures with uniform absolute error G^6/3 for 0<G<=0.1. No novelty claimed for the known sqrt(5!)/64 coefficient or the resonance mechanism. |
| **Limitations / bottlenecks** | Primary v3 and current abstract rechecked 2026-10-12; exact identifier/title plus proof/resolution queries and weak-coupling/five-photon/Bloch-Siegert neighbors. Springer 2026 small-gap successor and arXiv:2608.09562v1 Sec.5 checked. No verified later global resolution or matching explicit uniform certificate; priority is not exhaustive and novelty/significance require fresh referee assessment. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00003-p07/paper.pdf) · [TeX](../../projects/phys-00003-p07/manuscript/main.tex) · [Code / data](../../projects/phys-00003-p07) · [Author handoff](../../projects/phys-00003-p07/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00003-p07/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00003-p10 · Weak periodic phase shaping lowers the worst-case sensitivity of coherent-state qubit readout</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Rules out all fixed weak periodic same-axis phase shaping, including multiharmonic and discontinuous profiles, as an infinitesimal route to improving the established uniform single-mode qubit readout. Any improvement must evade this restricted perturbative conclusion. No improved interaction, hardware benefit or unrestricted optimum is asserted. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | In the one-real-coherent-mode, fixed-ground-state-qubit, alpha-independent-unitary, qubit-only SLD-QFI model of source.md/problem.md, for every fixed L>0 and fixed real bounded Borel L-periodic function g nonconstant almost everywhere, set V_epsilon=exp\[-i sigma_y(Q/sqrt(2)+epsilon g(Q))\]. There exists epsilon0(g,L)>0 such that for every real epsilon with 0<abs(epsilon)<epsilon0, of either sign, the outputs are uniformly full rank and inf_{alpha in R} F_Q\[rho_epsilon(alpha)\]<4/e. Explicitly epsilon0=min(h/M,gamma/(2KM^2)), where M bounds abs(g), G is the exact first-variation response, gamma=min(-min G,max G)>0, and h,K are the uniform-rank/remainder constants in evidence/research/periodic-variation-proof.md. Constant g preserves 4/e. The profile and period are fixed before taking epsilon small; no common radius, norm-neighborhood maximum, finite-strength no-go or unrestricted optimum is asserted. |
| **Proposed contribution** | A restricted exact directionwise obstruction: for every one fixed real bounded Borel periodic phase profile g, nonconstant almost everywhere, f_epsilon(x)=x/sqrt(2)+epsilon g(x) has inf over every real alpha of qubit QFI strictly below 4/e for both sufficiently small signs of epsilon. The radius depends on the profile and period. Explicit first-variation Fourier multipliers have no nonzero-frequency nulls; uniform full rank and a quadratic remainder establish the continuum conclusion. |
| **Limitations / bottlenecks** | Checked current official arXiv:2509.22361 history and full v2 primary Sections III.1 and III.6 on 2026-10-12; no later version listed. Existing full publisher and preprint sources and preprocessing/compression/repeated-query neighbors were read at their decisive premises. Current exact-title/identifier/author, coherent/qubit/worst-case/Fisher, 4/e/nonlinear and Gaussian/minimax/qubit/encoding searches identified no checked primary reporting this obstruction. Absence of hits is not priority proof. The source's in-preparation reference remains inaccessible and could affect novelty; fresh independent significance/novelty review remains required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00003-p10/paper.pdf) · [TeX](../../projects/phys-00003-p10/manuscript/main.tex) · [Code / data](../../projects/phys-00003-p10) · [Author handoff](../../projects/phys-00003-p10/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00003-p10/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00004-p09 · Positive pathwise entropy curvature at the canonical two-copy purification of a binary classical state</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Every fixed non-gauge exponential auxiliary-unitary direction increases the purification entropy for sufficiently small nonzero parameter in this split. Infinitesimal descent cannot provide collective preparation savings there; finite-distance or larger-split mechanisms remain possible. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For every strictly positive normalized binary probability table P with det(sqrt(P)) nonzero, consider the canonical two-copy purification in the fixed auxiliary split R=S=C^4 and U(t)=exp(i t H) on RS. On the 112-real-dimensional Hermitian-generator subspace with no first-order null-to-null Schmidt block, S(AR;t)=2 h2((1+sqrt(1-4 det(sqrt(P))^2))/2)+c_P(H)t^2+o(t^2). The exact quadratic form c_P is nonnegative with kernel precisely H=H_R tensor I+I tensor H_S, a 31-dimensional local auxiliary-unitary gauge. Thus its 81-dimensional quotient is strictly positive. The phase sector has the explicit sum-of-squares form and the controlled-rotation sectors the graph-Laplacian forms in quadratic-form.md. Outside this subspace, the positive leading t^2 log(1/t^2) coefficient implies entropy increase along every fixed non-gauge exponential-unitary path for sufficiently small nonzero t. This does not assert a common quantitative neighborhood, global additivity, boundary/product-table coverage, or a result for larger auxiliary splits. |
| **Proposed contribution** | Exact entropy quadratic form on the 112-dimensional no-first-order-Schmidt-rank-growth auxiliary-generator space at the canonical two-copy purification; its quotient by 31 local auxiliary-unitary gauge directions is strictly positive in all 81 remaining dimensions for every strictly positive nonproduct binary probability table in R=S=C^4. |
| **Limitations / bottlenecks** | Primary records and relevant full-text locations checked 2026-10-12 before continuation, plus exact claim/local-curvature/local-additivity queries. August 2608.28897v1, October 2610.03630v1, norm-compression 2410.21961v4, and related 1105.6122 and 2111.11385v4 were screened. Bounded coverage cannot certify priority; a fresh referee must assess possible constrained variants and significance. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00004-p09/paper.pdf) · [TeX](../../projects/phys-00004-p09/manuscript/main.tex) · [Code / data](../../projects/phys-00004-p09) · [Author handoff](../../projects/phys-00004-p09/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00004-p09/reproducibility/README.md) |

**Related results / preserved versions**

- [phys-smallmac00022-p01](../../projects/phys-smallmac00022-p01): Both concern two-copy binary-state entanglement of purification. big_mac proves pathwise positivity for every positive nonproduct binary table without a common neighborhood; small_mac proves a full U(16) strict local minimum modulo gauge at r=1/2. Neither recorded statement contains the other complete statement. Keep both, link them, and do not infer global additivity.

</details>

<details>
<summary><strong>phys-00007-p09 · Local robustness of commuting-reflection encoding near the three-qubit W state</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Eight perfectly distinguishable messages from coordinated commuting product reflections remain possible under arbitrary sufficiently small pure-state perturbations of W3, with joint decoding. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | There exist epsilon>0 and C<infinity such that every normalized complex three-qubit pure-state ray with phase-fixed chart psi=(W3+eta)/sqrt(1+&#124;&#124;eta&#124;&#124;^2), <W3&#124;eta>=0, &#124;&#124;eta&#124;&#124;<epsilon admits a commuting-reflection encoding with the triangle graph and a local SU2 change V(theta)=exp(-i theta.sigma/2)q^tensor3 satisfying &#124;&#124;theta&#124;&#124;<=C&#124;&#124;eta&#124;&#124;^(1/3). On psi(t)=(W3+t delta)/sqrt(1+13t^2), delta=V0^dag O V0 W3, an exact branch has theta=s v1+O(s^2), t=(40ab/39)s^3+O(s^4), whereas no C1 branch through V0 exists. No universal claim away from the neighborhood or numerical radius is asserted. |
| **Proposed contribution** | An exact open neighborhood of arbitrary complex pure-state perturbations of W3 is encodable with the fixed triangle graph. A nonzero cubic reduced moment yields an anchored O(distance^(1/3)) encoder-control bound and cube-root continuation on a specified legal state path. |
| **Limitations / bottlenecks** | 2026-10-12 primary arXiv history/current fulltext and retained v1/v2 PDFs checked; title/resolution, W neighborhood, three-qubit commuting encodability and successor searches preserved. No verified successor located, but unpublished work and complete forward citations remain unchecked; no absolute priority claim. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00007-p09/paper.pdf) · [TeX](../../projects/phys-00007-p09/manuscript/main.tex) · [Code / data](../../projects/phys-00007-p09) · [Author handoff](../../projects/phys-00007-p09/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00007-p09/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00008-p03 · Exact local spectrum and a residual-rate obstruction for quantum Latin-square normalization</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | For this measurement-array generator, excellent individual Gram conditioning does not guarantee a strict uniform one-cycle residual reduction. The family gap collapses quadratically near a classical endpoint. This identifies a geometric obstruction to a conditioning-only progress guarantee; no nonlinear iteration budget or probability law is claimed. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the explicit n=4 Q(theta) block-rotation quantum Latin square in evidence/research/local-spectrum-proof.md, the real derivative of one source row-then-column normalization cycle restricted to the 64-dimensional column-unitary tangent space has spectrum 0 (16), 1 (32), (1+cos(theta))/2 (8), (1-cos(theta))/2 (8), with degeneracies combined for all real theta. For every q in (0,1), delta in (0,1), eta>0, some theta in (0,pi/2) and legal column-unitary x with 0<&#124;&#124;x-Q(theta)&#124;&#124;_F<eta satisfy e(F(x))>q e(x)>0 while all eight inverted Gram spectra lie in \[1-delta,1+delta\]. This is a local one-cycle rate obstruction only and leaves the original almost-sure arbitrary-precision question unresolved. |
| **Proposed contribution** | Exact complete spectrum 0^16, 1^32, ((1+cos(theta))/2)^8, ((1-cos(theta))/2)^8 of the n=4 family derivative restricted to the column-unitary tangent space, including classical endpoint degeneracies. Prove legal arbitrarily close curves with source-residual ratio tending to the slow eigenvalue and all inverted Grams arbitrarily close to I, excluding a uniform one-cycle q<1. |
| **Limitations / bottlenecks** | 2026-10-12 primary version/conjecture, original Sections 3-4, 2016 Sections 5-6, 2017 strictly positive-block theorem domain, 2023 Problem 3.13, current author bibliography and limited 2026 v3 successor screen; Lewis-Malick Lemma 2.1/equation (11)/Theorem 4.3 and Musto-Vicary Definition 1/Example 2. Exact-title, alternating-projection, linear-convergence, principal-angle and quantum Sinkhorn rate searches. No matching explicit family spectrum identified in bounded checked sources; equivalent older results and priority remain a fresh-review question. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00008-p03/paper.pdf) · [TeX](../../projects/phys-00008-p03/manuscript/main.tex) · [Code / data](../../projects/phys-00008-p03) · [Author handoff](../../projects/phys-00008-p03/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00008-p03/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00009-p01 · Exact two-particle relaxation crossover for the symmetric inclusion process on hypercubes</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Determines when a pair-separation relaxation mode is strictly slower than every one-particle mode, at finite diffusivity. Provides a dimension-dependent crossover boundary and its scaling. Published monotonicity then excludes one-particle reduction of the full conservative SIP below the threshold, while its all-k gap above the threshold remains undetermined. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the conservative SIP with exactly two particles on the D-dimensional Boolean hypercube Q_D, every finite integer D>=1, homogeneous site weight a>0 and common edge conductance c>0, lambda_2=c*min(2a,rho_D(a)), where rho_D(a) is the smallest positive eigenvalue of the D+1-state birth-death negative generator with downward rates 2*d*a+2*1_{d=1} and upward rates 2*(D-d)*a. The one-particle gap is 2*c*a. With a_D=(D-1)*2^{-(D-1)}*integral_0^1(1+u^2)^{D-1}du-1, lambda_2<lambda_1 iff 0<a<a_D for D>=4; for D<=3 lambda_2=lambda_1 for all a>0. The threshold satisfies a_4=1/35, a_(D+1)=(D^2*a_D+1)/((D-1)*(2D+1)) for D>=2, and D^2*a_D tends to 1. No k>=3 identity is claimed. |
| **Proposed contribution** | Exact full two-particle gap reduction for every homogeneous hypercube Q_D and every finite positive a to a D+1-state distance chain, including rigorous bounds on omitted sectors. An exact finite-a crossover formula, a_4=1/35, an all-D recurrence and D^2*a_D->1 are obtained. |
| **Limitations / bottlenecks** | Primary current versions, relevant journal sections, the 2024 institutional published PDF and bounded hypercube/Hamming/1-over-35 searches checked on 2026-10-12, before and during research. The inspected texts and searches did not yield this formula. No exhaustive global priority claim; novelty and significance require a fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00009-p01/paper.pdf) · [TeX](../../projects/phys-00009-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00009-p01) · [Author handoff](../../projects/phys-00009-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00009-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00013-p01 · Exact pure-state contraction spectrum of a three-qubit Haar circuit</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Identifies centered single-qubit purity as the slowest state-observable mode at every symmetric moment order, excludes higher symmetric moments as slower counterexamples, and gives exact stationary L2 contraction for random pure-state preparation. The pure-state quotient is faster than the known group-level fourth-moment cosine1/2. It does not settle the original unitary-group mixing constant or imply a total-variation mixing time from a delta initial law. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the specified three-qubit adjacent normalized Haar-SU4 circuit, the complete nonzero principal cosines on L2(CP7, normalized Haar) are c_r=6/((r+2)(2r+3)), r>=0. In conjugation on End(Sym^k C8), k>=0 integer, the cosines truncate to0<=r<=floor(k/2). Removing the whole global invariant gives norm0 for k<=1 and2/5 for every k>=2, and pure-state ordered m-step norm(2/5)^(2m-1), m>=1. This is a natural state quotient/symmetric-moment result; the original all-PU8 equality c_*=1/2 remains unresolved. |
| **Proposed contribution** | For the same adjacent Haar-SU4 three-qubit circuit, derive the complete principal-cosine sequence c_r=6/((r+2)(2r+3)) on L2(CP7), r>=0, and its exact truncation to every End(Sym^k C8), r<=floor(k/2). The stationary pure-state nonfixed norm is2/5, and the ordered m-step norm is(2/5)^(2m-1). This is an all-degree quotient result; the number2/5 at degree2 and the finite k7/k8 tables are not the novelty claim. |
| **Limitations / bottlenecks** | Current official metadata and decisive primary full-text passages checked2026-10-12:2609.40164v2,2012.05259v1,2411.13739v2,2408.11201v2,1809.00642v1,math-ph/0610045v2,quant-ph/0012101v3,2606.11438v1. Searches covered exact original constant, later resolutions, pure-state/all-symmetric-moment spectra, joint purity correlations and Jacobi/projective-space equivalents. No examined primary source gives this exact local-circuit all-degree sequence. This is bounded proposer novelty analysis, not exhaustive priority proof; the older Haferkamp-Hunter-Jones publisher body remains unexamined. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00013-p01/paper.pdf) · [TeX](../../projects/phys-00013-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00013-p01) · [Author handoff](../../projects/phys-00013-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00013-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00014-p01 · Exact single-use Bayesian Nagaoka–Hayashi attainment for noisy qubit rotations</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | A fixed single-qubit pre-rotation followed by a Bell measurement achieves the ultimate three-axis Bayesian mean-square precision for one noisy channel use. Only the posterior estimator shrinks with known noise, so the measurement needs no noise-dependent redesign. The finite Bayesian incompatibility penalty relative to the reproduced SLD value is 8B Q^2/(A+B) for lambda<1. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For k=1 in the frozen fixed-Bell-probe model U_theta=exp(-i theta dot sigma) followed by known depolarization 0<=lambda<=1, with uniform Cartesian-volume prior on &#124;&#124;theta&#124;&#124;<=pi/4 and R=E\[&#124;&#124;hat theta-theta&#124;&#124;^2\]/3, the optimum over all system-ancilla physical POVMs and finite-second-moment estimators equals the source Bayesian Nagaoka-Hayashi SDP: R_1(lambda)=C_NH(1,lambda)=pi^2/80-4(1-lambda)^2(3/(2pi)-12/pi^3)^2. It is attained by four orthonormal vectors (&#124;0>-i sum_i s_ji&#124;i>)/2 in the source spin basis, for tetrahedral signs s=(+++),(+--),(-+-),(--+), with posterior estimates 2(1-lambda)(3/(2pi)-12/pi^3)s. Equivalently, one fixed local pre-rotation followed by a Bell measurement implements this PVM. A normalized covariant sphere measurement also attains it. Exact continuum physical-risk and NH PSD dual certificates establish the all-noise equality, including endpoints. No claim for k=2,3,4 or optimized/adaptive probes; the frozen original remains unresolved. |
| **Proposed contribution** | Exact k=1 fixed-Bell attainment for the full continuum 0<=lambda<=1 under the specified pi/4 volume prior: closed optimal risk pi^2/80-4(1-lambda)^2(3/(2pi)-12/pi^3)^2; four-outcome noise-independent rotated-Bell projective measurement; exact posterior estimates; distinct all-estimate physical-risk and NH SDP dual certificates. The original k=1,2,3,4 question remains unresolved. |
| **Limitations / bottlenecks** | 2026-10-12 21:10-21:19 UTC: current 2607.15398 v1 and 2511.16645 v4 metadata/bodies; selected current author fulltext 2008.02612v2 and previous exact-scope Suzuki/Zhao/Andre source records. Exact identifier/title, Bayesian NH exact/proof/attainment, depolarization/SU(2), tetrahedral/simplex, Hadamard/projective, phase-imaging/N00N queries. No verified later exact resolution found. Bounded coverage is not a proof of priority; Nature publisher redirect failure and incomplete old-method appendices are disclosed. Fresh referee must assess novelty/significance. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00014-p01/paper.pdf) · [TeX](../../projects/phys-00014-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00014-p01) · [Author handoff](../../projects/phys-00014-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00014-p01/manuscript/REPRODUCE.md) |

</details>

<details>
<summary><strong>phys-00015-p01 · Local dissipation optimality at the spectral coherence threshold of unicyclic clocks</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Small kinetic heterogeneity cannot reduce the homogeneous dissipation cost once the leading spectral coherence is restored to the source's eligibility threshold. Any improvement or counterexample must leave the n-dependent local neighborhood. This is a finite-model response result, not an experimental entropy estimate or a global bound. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For each integer n>=5 put t=tan(pi/n). The homogeneous strictly positive single-cycle rates u=c(1+t), d=c(1-t), c>0, have a simple globally leading conjugate pair with b/a=1. In a sufficiently small n-dependent neighborhood modulo common time scaling, every legal rate tuple with b/a>=1 satisfies Y=sigma*a/b^2 >= (1+t^2)*atanh(t)/t>1, with equality only at that homogeneous threshold ring up to scale. The full fixed-b/a=1 heterogeneous tangent Hessian is positive definite, including even-n Nyquist modes. No explicit or uniform-in-n radius, arbitrary-coherence optimality or global heterogeneous inequality is claimed. |
| **Proposed contribution** | Exact positive full heterogeneous tangent Hessian at b/a=1 for every n>=5, and resulting strict local minimum of Y=sigma*a/b^2 among nearby positive-rate single cycles on b/a>=1, modulo time scale. Stationary probabilities and edge flows both vary freely. Nyquist modes and the local spectral ordering are included. |
| **Limitations / bottlenecks** | Bounded primary checks on 2026-10-12: OBS 2112.01607v2, Gu 2606.05498v1, Shiraishi 2609.34352v1, Kolchinsky 2510.14101v3, winding paper 2605.15884v3, current Jason author TeX scope and Uhl--Seifert 1907.04260v1 Section 4. Searches included entropy/coherence, unicyclic/heterogeneous, uniform rates, perturbation, second order and local minimum. No exact predecessor for this restricted entropy-cost statement was identified. Priority and significance remain candidate assessments; publisher-final-body comparison and a complete forward-citation census are not completed. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00015-p01/paper.pdf) · [TeX](../../projects/phys-00015-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00015-p01) · [Author handoff](../../projects/phys-00015-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00015-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00018-p01 · A local noise tradeoff for two cross-regulated genes with unequal finite RNA lifetimes</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | At unregulated RNA/protein mean one and finite unequal RNA lifetimes, arbitrary cross-transcription shaping cannot reduce both stationary protein Fano factors below their correctly mean-matched two-stage baselines within the stated response-dependent weak-feedback neighborhood. This excludes a whole nonlinear low-copy design route without LNA or a burst approximation. Searches for a legal simultaneous-suppression example must leave this neighborhood, change parent kinetics or consider larger networks. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the exact infinite-state two-stage N=2 gene-expression CTMC with parent tuples (c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1), let h1,h2 be any real bounded whole-lattice protein functions with &#124;h_i&#124;<=1, and a,b>0. Set g=max(a,b), f1=1+epsilon*a*h2(P2), f2=2-epsilon*b*h1(P1), with all other reaction channels unchanged. The exact independent-parent forms defined in evidence/research-pass2/operator-certificate-and-tail.md satisfy &#124;V1&#124;,&#124;V2&#124;<=4/5*sqrt(U1*U2) for all such response functions, without monotonicity or a finite plateau. For S=a^2*U1+b^2*U2>0, every 0<epsilon<min(1/g,S/(4480*g^3)) gives an admissible network with at least one stationary protein Fano factor strictly above its mean-matched finite-lifetime baseline B1=3/2 or B2=4/3. If both responses are constant, both Fano factors equal their baselines. This computer-assisted local theorem covers all response shapes for this fixed unequal-lifetime low-copy pair only; epsilon is response-dependent. The original arbitrary-N, arbitrary-kinetics, strong-feedback problem remains unresolved. |
| **Proposed contribution** | A computer-assisted exact local no-simultaneous-output-suppression result for the finite-RNA parent pair (c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1), uniform over every real bounded whole-lattice response shape, including nonmonotone and arbitrarily rare tails. A new weaker whole-space weighted generator bound and finite Riesz residual enclosures remove the earlier artificial finite-plateau restriction, yielding &#124;V_i&#124;<=4/5 sqrt(U1 U2), with an explicit finite-feedback stationary covariance remainder. |
| **Limitations / bottlenecks** | Rechecked official arXiv histories 2607.20823,2605.15401,2512.20887 and the current burst-paper Discussion and official author list on 2026-10-13 UTC before legacy extension. Compared decisive pages in preserved primary PDFs/texts and targeted exact-title, finite-intermediate, finite-mRNA, two-stage weak-feedback, nonlinear cross-regulation and simultaneous-suppression searches. No matching later primary theorem was identified in this bounded screen. Current general resolution and global priority remain uncertain; absence of a hit is not proof of openness or novelty. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00018-p01/paper.pdf) · [TeX](../../projects/phys-00018-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00018-p01) · [Author handoff](../../projects/phys-00018-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00018-p01/reproducibility/README.md) |

**Related results / preserved versions**

- [phys-smallmac00010-p02](../../projects/phys-smallmac00010-p02): The two-gene finite-RNA-lifetime matched-baseline theorem is not the three-species direct-abundance feedback-ring weak-regulation result. The intermediate RNA state, number of species, baseline and whole-space remainder are different.

</details>

<details>
<summary><strong>phys-00024-p01 · Local stability of a sharp q-deformed commutator response for conditional quantum operations</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | The already reconstructed conditional-Kraus ordered-amplitude response has a locally stable sharp upper envelope: general operator errors normal to the saturation family, including spectator-level coupling, reduce the optimized response quadratically. A violating tuple cannot approach this orbit at fixed n,q. No explicit neighborhood radius or new relaxation-rate prediction is claimed. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For each finite n>=3 and each real q not equal to -1 or 1, set R=sqrt(2(1+q^2)), c=(1+q+R)/2, u=sqrt(c-1), b=sign(1+q)sqrt(c-q), A_q=diag(u,-b,0,...,0). For g_q(A)=lambda_max(H_q(A))/&#124;&#124;A&#124;&#124;_F^2, where vec(B)^dagger H_q(A) vec(B)=Re Tr((BA-AB)^dagger(BA-qAB)), there exists an n,q-dependent neighborhood of A_q in M_n(C) on which g_q is real analytic with a Morse-Bott local maximum c. Its local maximum set is the smooth 4n-2 real-dimensional manifold of unitarily embedded two-plane matrices C satisfying det C+\[ub/(u-b)^2\](tr C)^2=0 near diag(u,-b). The complete negative normal Hessian spectrum at A_q is -2, -4c(c-q)/\[(2c-q)R\], -4c(c-1)/\[(2c-1)R\], -2c/R, with multiplicities 2,2(n-2),2(n-2),2(n-2)^2. For mu the smallest magnitude and Lambda the largest, a smaller tubular neighborhood satisfies (mu/8)dist_F(A,M_q)^2 <= c-g_q(A) <= Lambda dist_F(A,M_q)^2, hence the corresponding local sharp f-bound holds for every complex B. No explicit radius, global bound, or uniform n/q limit is claimed. Auxiliary q=1/2 n=2 nonzero equality matrices are exactly det A+(3/2)(3+sqrt(10))(tr A)^2=0. |
| **Proposed contribution** | For every finite n>=3 and real q except -1,1, prove a full-dimensional local sharp bound near the embedded witness, classify its smooth equality manifold of dimension 4n-2, and derive the complete negative normal Hessian spectrum with multiplicities. Auxiliary q=1/2 equality determinant and curvature explain the previous flat directions. |
| **Limitations / bottlenecks** | Primary-source and exact-claim rechecks on 2026-10-13: arXiv:2208.10005v1, current publisher abstract, arXiv:2608.03897v1 q-commutator norms, arXiv:2409.00436v1 averaged relaxation resolution, exact identifier/title/formula/author and equality/stability/Morse searches. No primary statement of this local all-q f-response spectrum was found; this bounded screen is not priority certification. Fresh novelty and significance review remain required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00024-p01/paper.pdf) · [TeX](../../projects/phys-00024-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00024-p01) · [Author handoff](../../projects/phys-00024-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00024-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00027-p01 · Time-independent Lindblad embeddings of two-parameter Werner–Holevo noise</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | The unrestricted reduction makes the known covariant rate inequalities decisive for calibrated symmetric and antisymmetric Werner-Holevo noise even when the underlying constant master equation is not assumed symmetric: outside the qutrit region no hidden Hamiltonian, noncovariant jumps, or logarithm branch can realize the observed channel. The two boundaries remain the zero-rate limits of the known symmetric-traceless and antisymmetric jump families. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For the frozen two-parameter noisy Werner-Holevo channel on M_d(C), write Phi=P0+s Ps+a Pa with s=1-d*x/(d-1)-d*y/(d+1) and a=1-(d-2)*x/(d-1)-(d+2)*y/(d+1). For every d>=3 in the sector s>0,a>0, there exists a finite time-independent same-system GKLS generator L with exp(L)=Phi, allowing arbitrary Hamiltonians, jumps and logarithm branches, if and only if s^((d+2)/d)<=a<=s^((d-2)/d). A valid generator has H=0 and nonnegative symmetric-traceless and imaginary-antisymmetric jump rates gamma_s=((d-2)log(s)-d log(a))/(2d) and gamma_a=(d log(a)-(d+2)log(s))/(2d). For d=3 this gives the complete classification in the frozen x>0,y>0,x+y<=1 domain: s=1-3x/2-3y/4>0, a=1-x/2-5y/4>0, and s^5<=a^3<=s. The negative even-multiplicity sectors for d>=4 are not classified. |
| **Proposed contribution** | The proposed contribution is only the arbitrary-endpoint-generator necessity step and its qutrit consequence: for every d>=3 and s,a>0, any same-system time-independent GKLS logarithm of the O(d)-covariant endpoint, even if noncovariant and nonprincipal and with arbitrary Hamiltonian/jumps inside degenerate sectors, has a full-O(d) average fixed by branch-invariant real sector traces to the principal covariant logarithm. Combining this reduction with the known 2023 covariant cone gives the unrestricted positive-spectrum criterion. Odd real sector multiplicities plus singularity exclusion then give the complete frozen-domain d=3 classification. The covariant cone/exponential itself is not claimed new, and the signed d>=4 problem remains unresolved. |
| **Limitations / bottlenecks** | Complete retained primary PDFs arXiv:1801.06121v3, 2301.10679v4, and 2602.08464v1 were read at the recorded locators, and live primary records plus exact-claim/later-resolution searches were rechecked on 2026-10-13. The current model record remains arXiv:2405.11216v3. No returned primary record stated the narrowed arbitrary-noncovariant O(d) endpoint reduction or complete noisy-Werner--Holevo qutrit region. This bounded result is not proof of priority or openness; a fresh referee must independently repeat the comparison. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00027-p01/paper.pdf) · [TeX](../../projects/phys-00027-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00027-p01) · [Author handoff](../../projects/phys-00027-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00027-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00035-p01 · Near-star spectral gaps on subdivided two-star qubit networks</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | The actual lowest excitation of this leaf-rich two-hub network is a relative 1/(2k) above the star threshold at leading order, with a controlled theta-dependent correction. Uniform approach to Delta/eta=1 occurs on an infinite nonstar family as s tends to one in eta=theta/k, so removing stars does not create a fixed multiplicative excess in this specified near-endpoint regime. There is no new phase or quantum algorithm complexity claim. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | Let T_k have hubs a,b, a shared neighbor c, and k private leaves at each hub, with only ac,bc and the private hub-leaf edges; n=2k+3. For the original phase-free unnormalized unit-edge H_s, every integer k>=100 and every real theta in \[1/2,2\], eta=theta/k, s=sqrt(1-eta), have simple full ground and first excited energies in conserved-number N=2 and N=3 after X_a X_b. With full multiplicities, &#124;Delta(H_s(T_k))/eta-\[1+1/(2k)+(1-theta)/(4k^2)\]&#124;<=364/k^3, so Delta>eta and the ratio tends uniformly to one on this infinite nonstar family. Every full N>=4 sector obeys lambda_N<lambda_3-(N-3)eta/2 for B=-X_a X_b H X_a X_b; complete internal N2 modes and N0/N1 are also excluded. Original all-graph/all-s conjecture remains unresolved. This is a controlled joint size/endpoint family result, with fixed unit edge strength and growing degree, not a thermodynamic phase claim. |
| **Proposed contribution** | For every subdivided two-star T_k, integer k>=100 and theta in \[1/2,2\], eta=theta/k, prove the complete ground and first excitation are simple N2/N3 levels and &#124;Delta/eta-\[1+1/(2k)+(1-theta)/(4k^2)\]&#124;<=364/k^3. The complete-star envelope supplies every N>=4 bound, including the stronger half-eta penalty; a full N2 Weyl bound supplies omitted internal irreps. The sector expansion is thereby upgraded to a full-gap result. |
| **Limitations / bottlenecks** | Fresh primary metadata and decisive preserved fulltexts checked on 2026-10-14, before extending the legacy claim. Exact claim/resolution, deformed EPR/leaf/star and two-star/joint-limit searches are preserved in research-p4-current-web-1 through -4; current versions v1,v1,v1,v2,v1 confirmed. No matching full-gap formula or later sharp-leaf resolution found in this bounded coverage. Novelty/significance remain provisional for a fresh referee, without exhaustive priority or openness claims. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00035-p01/paper.pdf) · [TeX](../../projects/phys-00035-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00035-p01) · [Author handoff](../../projects/phys-00035-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00035-p01/README_REPRODUCIBILITY.md) |

**Related results / preserved versions**

- [phys-smallmac00022-p03](../../projects/phys-smallmac00022-p03): The small_mac result is an all-s certificate for q=1..6 one-hub subdivided stars. big_mac proves a full-gap, tail-controlled two-hub family for k>=100 in eta=theta/k, theta in [1/2,2]. Different topology, size and parameter quantifiers; neither is an all-graph proof.

</details>

<details>
<summary><strong>phys-00037-p01 · Second-order entropy stability of a three-mode fermionic product channel</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | Rules out a quadratic non-Gaussian descent mechanism for increasing the source single-use unrestricted Holevo objective from this Gaussian encoder anywhere in the full three-mode full-rank-reference parameter chamber. Supplies an exact normal-curvature check for entropy optimization. No global optimum, new capacity formula, SSR-constrained rate, or experiment is inferred. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | For Bravyi's complete n=3 qubit/Majorana attenuation channel and every ordered 0<=b6<=...<=b1<1, the output-entropy gradient at the generalized-Gaussian pure input &#124;+++> vanishes in all normalized complex pure-state directions, and the real 14-dimensional Hessian is positive semidefinite. Its Gaussian-normal cross block vanishes exactly. In the exact two-dimensional non-Gaussian normal span_R{&#124;-+->,i&#124;-+->}, H_Im>=H_Re>=2*b1^2*(1-b1^2)^4/(65*ln(2)), hence both normal eigenvalues are strictly positive for b1>0. At b1=0 the complete channel is depolarizing and the Hessian vanishes. Zero and repeated smaller attenuations are covered; rank-singular b1=1, strict local minimality along Gaussian zero modes, global entropy optimality and higher n are excluded. |
| **Proposed contribution** | An exact computer-assisted all-parameter certificate for the two non-Gaussian normal Hessian eigenvalues at the three-mode Eq.(36) optimizer for every ordered 0<=b6<=...<=b1<1, including zero and repeated smaller attenuations. A uniform explicit positive lower bound when b1>0, exact cross-block selection rules, and the known Gaussian minimum imply a nonnegative full-complex 14-dimensional pure-state Hessian. |
| **Limitations / bottlenecks** | Fresh primary exact-claim/title and local-Hessian searches on 2026-10-14; Bravyi v1, Arhancet radial-v6 and Fourier-v15 selected full-text comparisons, Salek et al. 2610.06758v1 endpoint/parity theorem, and Ruskai-Yard 2111.11385v4 Introduction/Theorem 2/Section 3. Current version pages and raw search/capture replies are preserved. No equivalent theorem was located; bounded searches, selected body coverage and inaccessible publisher revisions do not prove exhaustive priority or present openness. Fresh referee novelty/significance review remains required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00037-p01/paper.pdf) · [TeX](../../projects/phys-00037-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00037-p01) · [Author handoff](../../projects/phys-00037-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00037-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-00040-p01 · Initial entropy-production decrease for product-profile narrow beams in the Landau–Maxwell equation</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background / original question** | A natural counterstreaming route to positive initial entropy acceleration is excluded beyond Gaussian local profiles, even for arbitrary fixed longitudinal score skewness. Within the specified beam scaling/covariance class, a putative positive p->0 sequence must violate local product structure or fixed-configuration hypotheses. The original all-data/all-time question remains unresolved. |
| **Original question** | unresolved |
| **Result and exact original-problem scope** | In the three-dimensional homogeneous Landau-Maxwell equation with a(z)=(&#124;z&#124;^2 I-zz^T)/2, mass one, mean zero and energy three, fix finite distinct real mu_j, w_j>0 with sum w=1, sum w mu=0, sum w mu^2=3. For each j fix centered normalized P_j on R^2 and R_j on R, each a polynomial globally bounded below by a positive constant multiplied by a centered nondegenerate Gaussian, with Cov(P_j)=a_j I_2, Var(R_j)=lambda_j>0 and sum w a=1. Put kappa_p^2=1-(2p+p^2 sum w lambda)/3 and f_p(v)=p^-2 sum_j w_j P_j(v_perp/sqrt(p)) R_j((v3-kappa_p mu_j)/p). For sufficiently small p>0 with kappa_p>=1/2, its actual initial right entropy-production derivative is Dprime_0(f_p)=p^-2 sum_j w_j C_j+O(p^-1), with configuration-dependent remainder, where C_j=-(mu_j^2+3)^2 JP_j/2-2(1+2a_j+U4_j/4)J_j+(9+5mu_j^2-mu_j^2 K2_j)I_j-mu_j a_j S3_j. Here JP=E_P&#124;&#124;Hess log P&#124;&#124;_F^2, U4=E_P&#124;X&#124;^4, K2=E_P(X.grad log P)^2, I=E_R((log R)prime)^2, J=E_R((log R)doubleprime)^2 and S3=E_R((log R)prime)^3. Every such coefficient satisfies C_j<=-(5/28)(mu_j^2+3)^2 JP_j<=-45/(14a_j^2), so sum w C_j<=-45/14 and Dprime_0(f_p)<0 for all sufficiently small p. The same leading functional inequality holds for any regular positive product factors with the stated finite moments and valid integrations by parts. This is an initial-data asymptotic, not a closure or a result uniform over varying configurations; the original universal monotonicity problem remains unresolved. |
| **Proposed contribution** | For every fixed finite normalized separated beam configuration with centered independent local transverse/longitudinal positive polynomial-Gaussian factors and widths sqrt(p),p, derive the full original-collision initial derivative Dprime_0(f_p)=p^-2 sum w C_j+O(p^-1). The general product coefficient includes longitudinal score skewness. Projected longitudinal curvature and transverse moment-curvature inequalities prove C_j<=-45/(14a_j^2), hence sum w C_j<=-45/14. Actual-mixture posterior overlap, tails and fixed-p initial differentiability are controlled analytically. |
| **Limitations / bottlenecks** | Fresh primary histories/fulltexts and bounded exact-claim/successor/product-beam neighbor searches on 2026-10-14. Actual located Villani v5 sections 7,13,24.1 and Delarue-Menozzi-Nualart v1 Proposition 2.3 checked. No matching later resolution or identical criterion located; absence is not openness/priority proof. Older Villani 1998/2000 fulltexts remain unreviewed. Candidate novelty/value are proposer assessments requiring a fresh referee; earlier acceptance covers a different scope. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, source and replay** | [PDF](../../projects/phys-00040-p01/paper.pdf) · [TeX](../../projects/phys-00040-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00040-p01) · [Author handoff](../../projects/phys-00040-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00040-p01/repro/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

The act of packaging grants no additional license to manuscripts, code or data. Consult the original author handoff and applicable rights. No submission, peer-review or acceptance is implied.
