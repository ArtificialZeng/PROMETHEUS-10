# PROMETHEUS-10 · Réfutation

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

Une archive vérifiable de recherche en physique assistée par IA. **93 PDF sont conservés ; 90 entrées canoniques sont indexées.** Trois résultats antérieurs couverts par des conclusions plus générales ou plus fortes restent accessibles comme versions historiques, sans double comptage. « 10 » désigne la collection initiale.

Ce sont des manuscrits de recherche nécessitant une vérification humaine de la science, de la priorité et des auteurs. Preuve et réfutation concernent uniquement la portée exacte de la proposition figée. Les résultats partiels et numériques ne résolvent pas entièrement la question initiale. Les contextes IA séparés sont des contrôles internes, pas une évaluation externe ni une acceptation éditoriale. La limitation historique du contrôle de liaison du manuscrit sur la boundariness demeure.

Les énoncés scientifiques et les titres gardent leur langue source. Navigation, statut, utilisation et les dix descriptions initiales sont localisés ; les affirmations citées ne sont pas modifiées par traduction.

[PROMETHEUS-10](../../README.fr.md)

[Catalogue complet consultable](../../catalog.html) · [Comparaison sémantique et dédoublonnage](../../SEMANTIC_DEDUPLICATION.md) · [Guide de reproduction](../../reproducibility/README.md)

## Les quatre catégories de résultats

| | Entrées canoniques |
|---|---:|
| [Preuve](../proofs/README.fr.md) | **32** |
| [Réfutation](../disproofs/README.fr.md) | **18** |
| [Résultat partiel](../partial-results/README.fr.md) | **38** |
| [Résultat numérique](../computational-papers/README.fr.md) | **2** |

Le processus supervisé vérifie les sources primaires, reconstruit indépendamment les équations, reproduit un résultat publié et fait contrôler chaque contribution limitée avant rédaction et validation. Des dossiers courts et des outils partagés réduisent les répétitions. Le cache est une partie de l’entrée ; aucune économie de tokens ou probabilité de succès non mesurée n’est annoncée.

## Réfutation

<details>
<summary><strong>phys-00004-p02 · An exact qutrit counterexample to an uncertainty conjecture</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte** | L’incertitude entropique limite la prédictibilité simultanée de mesures incompatibles. Un résumé spectral peut perdre une information essentielle. |
| **Résultat et portée** | Une matrice unitaire rationnelle de dimension trois réfute la conjecture extended-MUB étudiée. |
| **Contribution proposée** | Un certificat arithmétique compact montre pourquoi la deuxième valeur singulière ne suffit pas à garantir l’énoncé universel proposé. |
| **Limites et obstacles** | Réfutation d’une conjecture précise, pas du principe d’incertitude ; une inégalité optimale de remplacement reste à trouver. |
| **PDF et sources** | [PDF](../../projects/phys-00004-p02/paper.pdf) · [TeX](../../projects/phys-00004-p02/manuscript/main.tex) · [Bib](../../projects/phys-00004-p02/manuscript/references.bib) · [Code / data](../../projects/phys-00004-p02) · `python reproducibility/reproduce.py --project phys-00004-p02` |

</details>

<details>
<summary><strong>phys-00005-p01 · A 16-vertex graph defeats path minimality</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte** | Le mélange moyen des marches quantiques décrit les retours persistants et éclaire les questions extrémales de transport. |
| **Résultat et portée** | Un graphe connexe simple non pondéré de 16 sommets et 62 arêtes a une laziness de 1673/1192 contre 23/16 pour le chemin, soit -81/2384 de différence. |
| **Contribution proposée** | Deux représentations exactes certifient un contre-exemple fini à la minimalité proposée du chemin pour la marche laplacienne considérée. |
| **Limites et obstacles** | Ne classe pas tous les minimiseurs, tailles de graphes, hamiltoniens ou conventions de normalisation. |
| **PDF et sources** | [PDF](../../projects/phys-00005-p01/paper.pdf) · [TeX](../../projects/phys-00005-p01/manuscript/main.tex) · [Bib](../../projects/phys-00005-p01/manuscript/references.bib) · [Code / data](../../projects/phys-00005-p01) · `python reproducibility/reproduce.py --project phys-00005-p01` |

</details>

<details>
<summary><strong>phys-00006-p01 · A qubit memory breaks a universal contraction proposal</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte** | Les bornes de contraction quantifient la perte de distinguabilité. Une mémoire quantique peut changer ce qui est vrai sans système auxiliaire. |
| **Résultat et portée** | Un exemple exact d’amortissement d’amplitude, avec entrées intriquées à marginales égales, réfute le remplacement alpha-Doeblin hockey-stick universel proposé. |
| **Contribution proposée** | Le certificat isole un mécanisme sensible à la mémoire en respectant les contraintes initiales. |
| **Limites et obstacles** | Ne réfute pas toutes les inégalités de Doeblin et ne fournit pas une borne optimale de remplacement. |
| **PDF et sources** | [PDF](../../projects/phys-00006-p01/paper.pdf) · [TeX](../../projects/phys-00006-p01/manuscript/main.tex) · [Bib](../../projects/phys-00006-p01/manuscript/references.bib) · [Code / data](../../projects/phys-00006-p01) · `python reproducibility/reproduce.py --project phys-00006-p01` |

</details>

<details>
<summary><strong>phys-smallmac00001-p06 · A missing spectral arc at finite cycle affinity in four-state Markov generators</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 有限热力学力下 Markov 谱集合是否等于 Karpelevich 区域的纵向缩放 |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | At B*=log(3)/2 there exists eta>0 such that every four-state generator with escape rates <=1 and both oriented cycle-product bounds product_forward<=3^n_c product_reverse obeys &#124;Im(lambda)&#124;<=1/2-delta/2+delta^2/4 whenever delta=-1-Re(lambda) is in (0,eta). The exact-alpha unrestricted companion supplies compressed points Lambda(delta)=-1-delta+(i/2)sqrt(1-2delta+3delta^2), all strictly above that bound for 0<delta<min(eta,1/2). Thus the affine-image equality H_eq fails by nonattainment, including the closure of the larger bounded-affinity class. |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00001-p06/paper.pdf) · [TeX](../../projects/phys-smallmac00001-p06/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00001-p06) · [Author handoff](../../projects/phys-smallmac00001-p06/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00001-p06/manuscript/README.md) · [Replay](../../projects/phys-smallmac00001-p06/manuscript/repro/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00002-p09 · A counterexample to the forward waiting-time entropy bound in periodically driven Markov networks</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 周期驱动中，正向相位平均等待时间是否仍给熵产生下界？ |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | Counterexample to the universal upper bound hat_sigma_Psi<=bar_sigma exactly as quantified in immutable source.md and problem.md. On the complete three-state graph, observe only 1->2 and 2->1; take symmetric edge triples (k12,k23,k31)=(r,1,1),(1,r,1),(1,1,r)/t_star in consecutive segments of length t_star, with r>0,r!=1. The unique periodic distribution is uniform and bar_sigma=0, whereas the finite same-forward-protocol waiting estimator is strictly positive. The same-direction waiting-density difference has dimensionless x^3 coefficient -(r-1)^2/\[6(r+2)\]. For r=10, t_star*hat_sigma_Psi>=27/5734400000000000000000000000000000>0, with normalized joint waiting laws and controlled infinite logarithmic tail. This resolves the original conjunction by violating its upper half; no separate universal lower-bound theorem, smooth/fixed-prefactor claim, controller-cost claim, or independent acceptance is included. |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00002-p09/paper.pdf) · [TeX](../../projects/phys-smallmac00002-p09/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00002-p09) · [Author handoff](../../projects/phys-smallmac00002-p09/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00002-p09/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00005-p02 · A computer-assisted three-state counterexample to a nonlinear phase-lag bound</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 三态非线性周期响应的相位滞后，是否受最慢跃迁前因子约束？ |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | The frozen universal complete-three-state positive-branch phase bound is false. For the exact terminating-decimal M=2 parameters in evidence/counterexample-parameters.json, the unique strictly positive periodic state satisfies A>0 and B>0, while A-k0,min B<0; specifically the primary outward-rounded certificate gives A in \[0.1913253462459419,0.8081296470533585\], B in \[6.1034541204110998,6.1582195856729802\], and A-k0,min B in \[-5.966894239630766,-5.295324473154014\]. |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00005-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00005-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00005-p02) · [Author handoff](../../projects/phys-smallmac00005-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00005-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00006-p01 · Activity above one half in finite Glauber annealing</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 单调降温的Glauber退火，每步跳跃概率是否始终不超过 \(1/2\)？ |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | For the layered graph A(3),B(4),C(4), complete A-B edges, a B-C matching and C clique, with E/epsilon=(0x3,1x4,64x4), q=(10001/10000,33/32,64), beta epsilon=log q, K=2 and exact Gibbs initial state, A1>63/125 and (A0+A1)/2>251/500. For all independent perturbations &#124;delta(E_i/epsilon)&#124;<=1/1000 with the same temperatures and a redefined Gibbs initial state, A1>1003737/2000000 and the mean>8014821/16000000, both >1/2. This admissible finite example disproves the original all-regular-graph single-step activity bound in source.md/problem.md. It also violates its two-step averaged counterpart. Both are research claims submitted for fresh review, not an accepted scientific audit. |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00006-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00006-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00006-p01) · [Author handoff](../../projects/phys-smallmac00006-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00006-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00006-p02 · Coherent information in uniformly noisy graph states is not ordered by subsystem size</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 均匀噪声图态中，节点较多的一侧是否总有较高的相干信息？ |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | For the exact independent uniform phase-noise graph-state model of source.md/problem.md, the connected 5x4 biadjacency matrix with rows (1001),(1001),(1001),(0101),(0011) at P=199/200 has GF(2) rank3, no zero rows/columns, n_A=5>4=n_B>=3, and -0.0043<S_A-S_B<-0.0042 bits, with I_A>2.7 and I_B>2.7 bits. This is a strict counterexample to the frozen universal node-count ordering. More generally, for every integer r>=3, Gamma_r has rows v1,v1,v1,v2,...,vr, vi=ei+e_(r+1) in F2^(r+1); it is connected of size(r+2)x(r+1), rankr, and at the same P has Delta_r<=Delta_3<-0.0042 and I_B(r)>I_A(r)>2.7. These are coherent-information lower bounds, not equalities for optimal distillable entanglement. |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00006-p02/paper.pdf) · [TeX](../../projects/phys-smallmac00006-p02/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00006-p02) · [Author handoff](../../projects/phys-smallmac00006-p02/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00006-p02/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00007-p01 · Common output bias matters in randomness certification from quantum speed limits</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 量子速度极限的随机性认证：固定相关差，输出共同偏置是否真的无关？ |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | In the exact average branch-speed-budget relaxation defined in source.md and problem.md, take e=1/2, C_off=(sin(3/5),-sin(2/5)), and d=(sin(3/5)+sin(2/5))/2. Both C_off and (d,-d) lie in Q_(1/2). The submitted computer-assisted proof gives H*(C_off,1/2)>0.7758 bits and H*((d,-d),1/2)<0.7653 bits, so their difference exceeds 0.0105 bits. This counterexample disproves the original universal common-bias equality. It does not refute the proven midpoint lower-bound lemma or assert an optimal physical attack under a true total-state-variance constraint. |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00007-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00007-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00007-p01) · [Author handoff](../../projects/phys-smallmac00007-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00007-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00008-p01 · Comment on “Distinguishing graph states by the properties of their marginals”</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 图态凝聚：内部顶点各接至多一个外部顶点，是否足以保留局部Clifford等价？ |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | 原始固定标签双端外度≤1的Boolean OR凝聚保持LC等价的全称命题为假。完整证书：V={1,…,6}，C={1,2,3}，E(G)={13,16,24,35,46}，E(G′)={13,15,24,36,46,56}；G′=τ5τ1τ3G，两端连通且C外度均(1,1,1)、r_C=3。凝聚后B={4,5}对{6,c}的切割矩阵分别\[\[1,1\],\[0,1\]\]与\[\[1,1\],\[1,1\]\]，GF(2)秩2与1，边缘谱(1/4×4)与(1/2×2,0×2)，因此不LU等价，特别不LC等价。此反例允许C不连通；不主张无标签版本、C连通修正版或最小性。 |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00008-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00008-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00008-p01) · [Author handoff](../../projects/phys-smallmac00008-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00008-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-00002-p04 · Comment on “Bounds on skewness and kurtosis of steady-state currents”</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | Under the stated assumptions, negative fourth heat cumulants cannot exclude purely thermally driven classical Markov dynamics. This removes the proposed universal nonnegative-kurtosis diagnostic outside equilibrium. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | The frozen three-state two-positive-temperature, fully paired detailed-balance model has strictly positive c2 and strictly negative long-time hot-bath c4. It is an exact counterexample to the universal nonnegative thermal fourth-cumulant assertion. |
| **Contribution proposée** | A fully specified finite three-microstate, two-positive-temperature network with exact negative fourth long-time bath heat cumulant, obeying the stated thermal local detailed-balance premises. The full finite generator, not a residence-current approximation, is certified by two distinct exact calculations. |
| **Limites / difficultés restantes** | provisional; no equivalent purely thermal counterexample or later exact resolution found in targeted current primary-literature checks; absence of hits does not prove novelty No fresh referee or exhaustive citation-network search has occurred; raw web evidence consists of returned primary passages rather than complete downloaded source PDF bytes. Proposed physical intermittency explanation is not a certified singular-limit mechanism. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00002-p04/paper.pdf) · [TeX](../../projects/phys-00002-p04/manuscript/main.tex) · [Code / data](../../projects/phys-00002-p04) · [Author handoff](../../projects/phys-00002-p04/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00002-p04/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00002-p10 · A balanced beam-splitter counterexample to the low-order Wigner–Rényi vacuum bound</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | Balanced mixing of two independent non-Gaussian low-energy states does not preserve the vacuum minimum for all low-order Wigner–Rényi entropies; the proposed extension to every alpha in (0,1/2) fails. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | The universal low-order Wigner–Rényi vacuum bound for independently prepared balanced beam-splitter inputs is false. With \[x,p\]=i and Wvac=exp(-(x²+p²))/pi, prepare psi=(20&#124;0>+&#124;2>)/sqrt401 independently on both modes, trace one output after the balanced lossless mixer, and set alpha=1/4. Its exact retained Wigner function is exp(-R)\[(401-2R+R²/2+20sqrt2(x²-p²))/401\]²/pi, R=x²+p². A directed full-plane upper bound proves I_1/4(Wout)<9.43718<9.43892<I_1/4(Wvac)=4pi^(3/4), hence h_1/4(Wout)<h_1/4(Wvac). No other alpha range or optimum is claimed. |
| **Contribution proposée** | Exact independent product input psi=(20&#124;0>+&#124;2>)/sqrt401 yields an admissible beam-splitter state violating the vacuum bound at alpha=1/4; directed full-plane upper I<9.43718, vacuum I>9.43892. |
| **Limites / difficultés restantes** | 2026-10-12 official full text and version histories of 2411.05562v2 and 2609.24670v1; preserved 2601.16898v2 context; bounded searches for Wigner Rényi beam-splitter low-alpha counterexamples, cross-Wigner p<1 and squeezed alpha=1/4. No matching resolution located; absence of hit is not exhaustive priority proof. Referee novelty audit remains mandatory. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00002-p10/paper.pdf) · [TeX](../../projects/phys-00002-p10/manuscript/main.tex) · [Code / data](../../projects/phys-00002-p10) · [Author handoff](../../projects/phys-00002-p10/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00002-p10/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00005-p05 · An even first excitation in a phase-shifted EPR-like Hamiltonian</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | The true first excitation is even and the gap is Ee2-Ee1; substituting the lowest odd energy overestimates it by more than3/10 in the fixed edge energy unit. Odd-parity probes cannot couple the even ground state to this even excitation; no response intensity asserted. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | The universal Eo1<=Ee2 question frozen in source.md/problem.md is false. For the exact negative unnormalized pairing-projector Hamiltonian on K4, s=3/4, theta13=theta23=pi and all other phases0, the graph is legal and phase-obstructed, Ee2<-89/20<-83/20<Eo1. Its unique ground and first excitation are even. Reversal persists when &#124;s-3/4&#124;<1/1000 and every wrapped phase deviation is<1/1000, with Eo1-Ee2>252/1000. This answers negatively the restricted phase extension, not the phase-free Conjecture2. |
| **Contribution proposée** | A legal unweighted nonbipartite K4 at s=3/4 and phases pi on edges13,23 has Ee2<-89/20 and Eo1>-83/20, exactly disproving the project universal phase-obstructed ordering; a legal open amplitude/phase neighborhood retains reversal. |
| **Limites / difficultés restantes** | 2026-10-12: reopened current official arXiv histories and February/July fulltexts; reread October Section6.3 and preserved primary excerpts. All four histories list v1. Five focused parity/phased-EPR/counterexample searches found no explicit resolution. Older flux-model equivalences and complete citation networks were not exhaustively searched; candidate priority remains subject to fresh referee and author review. Exact terms and raw records in comparison files. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00005-p05/paper.pdf) · [TeX](../../projects/phys-00005-p05/manuscript/main.tex) · [Code / data](../../projects/phys-00005-p05) · [Author handoff](../../projects/phys-00005-p05/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00005-p05/supplement/README.md) |

</details>

<details>
<summary><strong>phys-00007-p19 · An exact counterexample to the reported spin-9/2 anticoherence extremum</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | The corrected attainable A3 changes the next-order directional-isotropy benchmark after fixing lower moments. Two complete exact fidelity representations and rational coefficient enclosures show F_witness(eta)<F_published_chi(eta) for all 0<=chi<=pi/2 and 0<eta<=2 asin(1/10) radians; the leading difference is -(252/5)D eta^6. The shared eta^2 sensitivity and general multiparameter QFI optimality are not changed or inferred. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | The original conditioned spin-9/2 bound is disproved: in normalized Dicke convention k=m+j, the pure vector with c0=c9=-1/sqrt(6), c3=c6=1/sqrt(3), all other coefficients zero, has rho1=I2/2, rho2=I_sym,2/3, and P3=4253/15876-10sqrt(42)/3969<789/3136, equivalently A3=(11623+40sqrt(42))/11907>2347/2352. The strict gap is (640sqrt(42)-4139)/254016. Supporting physical result: its uniform unknown-axis rotation-average fidelity is lower than that of every member of Martin et al. Eq.(65), for all 0<=chi<=pi/2 and 0<eta<=2 asin(1/10) radians. No claim of the true global A3 or finite-angle optimum is made. |
| **Contribution proposée** | An exactly normalized phase alteration with c0=c9=-1/sqrt(6), c3=c6=1/sqrt(3) obeys the original rho1/rho2 constraints and has P3*=4253/15876-10sqrt(42)/3969<789/3136, equivalently A3*=(11623+40sqrt(42))/11907>2347/2352. The strict purity gap is (640sqrt(42)-4139)/254016, certified by the integer difference 71879. This disproves the original universal bound without asserting the true global maximum. |
| **Limites / difficultés restantes** | Rechecked current primary histories and relevant full-text portions on 2026-10-12 before extending legacy work: 1909.08355v2, 1503.03446v3, 1509.08300v2, 1707.01246v2, 2509.18533v3, 2404.15548v3, 2605.29436v1, 2505.06154v2 and the retained published PDFs. Exact threshold, phase/radical and correction searches are saved. No identified earlier exact extremal correction appeared in this bounded screen; absence of hits is not proof of priority. State catalogs and equivalent previously parametrized states remain a specific novelty question for the fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00007-p19/paper.pdf) · [TeX](../../projects/phys-00007-p19/manuscript/main.tex) · [Code / data](../../projects/phys-00007-p19) · [Author handoff](../../projects/phys-00007-p19/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00007-p19/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00016-p01 · Comment on “Ergotropy and entanglement in critical spin chains”</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | For this exact finite model, the published aligned work underestimates unrestricted extractable work and overestimates bound energy. A legal interaction among physical subsystem modes extracts extra work even while particle number and parity are conserved. The correction is small, approximately 15-31 ppm of aligned bound energy over N12-24; occupation alignment retains its explicit number-preserving Gaussian optimum meaning. No thermodynamic/CFT coefficient or experimental gain is claimed. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | For the exact open homogeneous H_N=-sum(c_j^dagger c_(j+1)+h.c.), N=4m, its unique half-filled ground-state marginal on the first l=N/2 sites and unrestricted U(2^l), the original universal equality E_pass=E_align=sum_j nu_desc,j epsilon_ascending,j is false. At N12 a legal number/parity-preserving swap between physical-mode kets {2,3} and {1,4}, after legal orbital alignment, reduces energy by strictly more than 6.71114703278e-7 J. The full N12 correction lies in (0.000001356396207356,0.000001356396207357) J. Analytic particle-hole excitation ordering proves equality at N4/N8, so N12 is the first failing N=4m. Complete certified finite-sort corrections are supplied at N16,20,24 and a quartic N12 extraction gate. No claim is made about all larger sizes, locality/control time, thermodynamic entropy scaling or source Eqs41/42. |
| **Contribution proposée** | Exact rational actual-input N12 population inversion, explicit number/parity-preserving Fock-state swap and quartic mode gate; complete unrestricted/number/parity sorting through N24; analytic N4/N8 passivity identifies the first N=4m failure. The universal finite equality is false, with full N12 correction in (1.356396207356e-6,1.356396207357e-6) J. |
| **Limites / difficultés restantes** | Fresh 2026-10-13 official original/successor/version reads and exact-title/arXiv/finite-spectrum/correction screens, primary PRB final and author-v2 Eq34, PRE generic examples/Theorem1, NJP full-sort/single-mode/AppendixB passages, and a 2026 ancilla theorem operation-set comparison. Same-date cached official update records reread without claiming refetch. No exhaustive forward-citation search, final-byte comparison of the NJP successor or guaranteed priority; novelty and significance await fresh referee/author scrutiny. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00016-p01/paper.pdf) · [TeX](../../projects/phys-00016-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00016-p01) · [Author handoff](../../projects/phys-00016-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00016-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00029-p01 · A periodic planar counterexample to the Apollonian Ising temperature bound</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | Maximum coordination alone does not enforce the proposed logarithmic Apollonian design ceiling in the unrestricted source graph class. Selectively concentrated uniform-J paths change the actual infinite-volume ordering threshold; any corrected ceiling needs a different bound or additional physical/geometric assumptions. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | For every bare uniform ferromagnetic J>0 and zero field, let Lambda_1024 retain every triangular-grid bond and put N1024 finite fan spins in each up triangle A=z,B=z+e1,C=z+e2, e1=(1,0),e2=(1/2,sqrt(3)/2), at x_j=z+(1/2,sqrt(3)/(6j)), adding A-x_j,B-x_j for every j,C-x_1,and x_(j-1)-x_j for j>=2, all with the same J and no duplicate bond. This is a simple connected locally finite periodic Euclidean triangulation with1025-site primitive cell and q_max2055. Its actual infinite-volume Ising transition obeys T_c(Lambda_1024)/J>2/log(11/10)>20, while the exact canonical Apollonian function defined in immutable source.md obeys T_c_star(2055)/J<=T_c_star(3072)/J<20. Hence the original all-periodic-planar uniform-J inequality T_c<=T_c_star(q_max) is false within its full stated premises. |
| **Contribution proposée** | A concrete uniformly coupled Euclidean periodic fan with N1024 and qmax2055 satisfies T_c/J>20>T_c_star(2055)/J by strict exact certificates, disproving the original universal finite-q ceiling inside its premises. N1 is a reproduced prior baseline, not a claimed contribution. |
| **Limites / difficultés restantes** | 13October2026 UTC current arXiv2605.10017 and2601.02502 version histories, current source full v2 HTML and final APS abstract, exact identifier/title/author counterexample-comment-correction searches, and nested/fan/parallel/decorated triangular neighbors. Relevant primary full texts of the two2026 sources and final EJP criticality paper are preserved/read at exact locators. Background abstracts and failed1993 publisher opener are labelled; no exhaustive worldwide priority or unread full-body graph equivalence claimed. The exact older decoration comparison remains a referee priority issue rather than an input to the proof. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00029-p01/paper.pdf) · [TeX](../../projects/phys-00029-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00029-p01) · [Author handoff](../../projects/phys-00029-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00029-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00030-p01 · A finite nonreciprocal counterexample to a noise-matched current large-deviation bound</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | The proved variance constraint cannot be extended to the proposed full rate-function shape merely by substituting its noise-matching psi_0 dissipation factor. Magnetic circulation and an intermediate reservoir reduce actual entropy per selected mean particle while the rare reversal count samples a much lower-chemical-potential reservoir. This obstructs that specific use of measured mean dissipation to constrain rare currents. Other single-current shapes and the joint-current conjecture remain untested. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | The exact curvature-matching universal assertion frozen in source.md and problem.md is refuted by the finite stationary normal 387-dot conductor in evidence/research/r1-tightbinding-model.md, with exact semi-infinite tight-binding leads (band \[0,40000\]epsilon), three fixed Fermi reservoirs at common T_ref>0 and mu=(5001,4997,4976)epsilon, n=128 filter branches of finite width 0.02epsilon, E0=5000epsilon and Hermitian flux-ring core Gamma_c=200000epsilon. For extracted lead-0 counting, J>0 and total physical sigma>0, j=-J is strictly inside the asserted domain, and I_0(-J)-B_psi0(-J)>0.019epsilon/h. A completed outward full-energy certificate encloses Delta=24J-chi_0(-24)-4sigma/k_B inside \[0.019447,0.024248\]epsilon/h, with actual width below 0.005. Exact psi_0>=1/2, B_psi(-J)=2sigma/(psi k_B), and Fenchel at s=-24 prove the rate-function gap without a rounded infimum or a numerical saddle. This resolves only the frozen formalization of the first proposed nonreciprocal extension; it does not refute the reciprocal theorem or variance bound or settle the joint-current alternative. |
| **Contribution proposée** | A fixed physically realizable stationary finite 387-dot conductor with exact normal tight-binding leads, three fixed positive-temperature Fermi reservoirs and all-reservoir heat entropy yields a computer-assisted strict counterexample to the exact curvature-matching assertion frozen in source.md: I_0(-J)-B_psi0(-J)>0.019 epsilon/h. It uses the exact psi_0 definition through the proved conservative bound psi_0>=1/2, not a numerical minimizer or an ideal one-energy unitary array. |
| **Limites / difficultés restantes** | Fresh bounded primary screen on 2026-10-13 at 19:51-19:53 UTC checked exact-title/identifier/conjecture/nonreciprocity/counterexample and Brandner-Saito rate-function successor terms. Current histories show 2507.01214v1,2502.07917v2,2607.06190v1; the exact final JPA conjecture and successor entropy distinction were reread from retained full primary documents. No exact later resolution was identified. This is not exhaustive priority certification; the target is our frozen curvature-matching interpretation of the first author speculation, not a formula quoted verbatim as a published theorem. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00030-p01/paper.pdf) · [TeX](../../projects/phys-00030-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00030-p01) · [Author handoff](../../projects/phys-00030-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00030-p01/evidence/research/r3-README.md) · [Replay](../../projects/phys-00030-p01/reproducibility/README.md) |

**Résultats liés / versions antérieures**

- [phys-00032-p01](../../projects/phys-00032-p01): A finite nonreciprocal full-current large-deviation counterexample is not the resource-dependent three-port noise/entropy theorem. The target bound, observable and hypothesis sets differ.

</details>

<details>
<summary><strong>phys-00034-p01 · Replica twist entropy fails strong monotonicity under fermionic Gaussian measurements</strong> — Réfutation · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | Replica twist entropy cannot be used as a strong monotone to upper-bound average pure-state Gaussian resource-conversion yield. Its source diagnostic and dynamical properties are unaffected. This gives an exact operational limitation for the actual high-order two-copy observable, including fermion-parity and graded-copy constraints. |
| **Question initiale** | réfutée dans la portée indiquée |
| **Résultat et portée exacte** | In the fixed-parity finite-mode graded-CAR model of problem.md, replica twist entropy at alpha=pi/4 is not a strong pure-state Gaussian monotone. The normalized even-parity N=34 state sqrt(3)/2 &#124;00>&#124;0000>^tensor8 + 1/2 &#124;11>\[(&#124;0000>+&#124;1111>)/sqrt(2)\]^tensor8 followed by occupation measurement of its first mode, retaining both outcomes with probabilities 3/4 and 1/4, has exact average increase log(25836385/25165824)>0. More generally the explicit N=4m+2 flagged family has the exact all-angle formula in evidence/flagged-twist-proof.md and, at every fixed 0<alpha<pi/2 and 0<q<1, violates strong monotonicity for sufficiently large finite m with unbounded average increase as m grows. |
| **Contribution proposée** | An exact fixed-parity fermionic family N=4m+2 has F=p^2+q^2 f(alpha)^m+2pq K_m(alpha), with explicit f and K. At alpha=pi/4, m=8,q=1/4 gives a finite N=34 two-outcome violation Delta=log(25836385/25165824)>0. For every fixed interior angle, parent P remains bounded but average measured-branch P grows linearly with m. |
| **Limites / difficultés restantes** | Current primary version records and targeted defining/proof sections rechecked 2026-10-14, including the newly identified current bridge-degree v2 and stabilizer counterexample v2/v3. Existing covariance and convolution comparisons retained. Bounded search cannot certify priority; candidate_novel is a proposer hypothesis for fresh review, not acceptance. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-00034-p01/paper.pdf) · [TeX](../../projects/phys-00034-p01/manuscript/main.tex) · [Code / data](../../projects/phys-00034-p01) · [Author handoff](../../projects/phys-00034-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-00034-p01/reproducibility/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

Le regroupement ne concède aucune licence supplémentaire. Consulter les instructions des auteurs et les droits applicables. Aucune soumission, évaluation externe ou acceptation n’est impliquée.
