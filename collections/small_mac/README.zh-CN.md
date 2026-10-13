# small_mac 物理成果集

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

[PROMETHEUS-10 首页](../../README.zh-CN.md)

本成果集收录 48 篇由 AI 辅助完成、可检查的物理研究草稿。

每个 small_mac 项目均通过已记录的本地科学、文稿和发布门禁，但仍须作者人工审阅；这不等于外部同行评审或期刊接收。

分类依据冻结的发布记录。“证明”与“反证”针对文稿所述命题及其假设；部分结果与计算结果不代表原题已完全解决。具体科学范围和局限须查阅各篇 PDF 与作者交接文件。

## 按已记录的成果类型浏览

| 成果类型 | 篇数 |
|---|---:|
| [证明](categories/proofs/README.zh-CN.md) | **21** |
| [反证](categories/disproofs/README.zh-CN.md) | **7** |
| [部分结果](categories/partial-results/README.zh-CN.md) | **19** |
| [计算结果](categories/computational-papers/README.zh-CN.md) | **1** |

论文题名保留各冻结文稿中的原始语言。

保留显示序号 11–58、批次编号和原始内部项目 ID。公开 `phys-smallmac` ID 均指向同一项目目录，映射记录见 [`id-map.json`](id-map.json).

[按批次查看原题、解决程度、续研信心与未解决原因](BATCH_STATUS.zh-CN.md).

## 证明 (21)

[证明](categories/proofs/README.zh-CN.md)

| 序号 | 批次 | 公开项目 ID | 原始内部 ID | 论文题名 / PDF | 原题状态 | 代码 / 复现 |
|---:|---|---|---|---|---|---|
| 15 | `small_mac / 00002` | [phys-smallmac00002-p01](../../projects/phys-smallmac00002-p01/) | `phys-smallmac00002-p01` | [Absence of reflection-symmetric two-periodic boundary laws in the competing three-state SOS model](../../projects/phys-smallmac00002-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00002-p01/reproducibility/check_integer.py) (3)<br>[复现指南](../../projects/phys-smallmac00002-p01/reproducibility/README.md) |
| 17 | `small_mac / 00003` | [phys-smallmac00003-p01](../../projects/phys-smallmac00003-p01/) | `phys-smallmac00003-p01` | [Maximum purity of absolutely PPT states of two qutrits](../../projects/phys-smallmac00003-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00003-p01/supplement/verify_clipping.py) (3)<br>[复现指南](../../projects/phys-smallmac00003-p01/supplement/README.md) |
| 20 | `small_mac / 00005` | [phys-smallmac00005-p01](../../projects/phys-smallmac00005-p01/) | `phys-smallmac00005-p01` | [Three-copy universal qubit purification under complete stabilizer preservation](../../projects/phys-smallmac00005-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00005-p01/reproduction/check_physics_inputs.py) (9)<br>[复现指南](../../projects/phys-smallmac00005-p01/supplement/README.md) |
| 22 | `small_mac / 00005` | [phys-smallmac00005-p03](../../projects/phys-smallmac00005-p03/) | `phys-smallmac00005-p03` | [A third magnetic Neumann level below the Dirichlet ground state on the disk](../../projects/phys-smallmac00005-p03/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00005-p03/evidence/verify-variational-identities.py) (1)<br>[复现指南](../../projects/phys-smallmac00005-p03/REPRODUCIBILITY.md) |
| 25 | `small_mac / 00006` | [phys-smallmac00006-p04](../../projects/phys-smallmac00006-p04/) | `phys-smallmac00006-p04` | [指定两浓度幂律反应系统，能否严格认证四条嵌套极限环？](../../projects/phys-smallmac00006-p04/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00006-p04/supplement/code/dyadic_interval.py) (7)<br>[复现指南](../../projects/phys-smallmac00006-p04/supplement/README.md) |
| 29 | `small_mac / 00008` | [phys-smallmac00008-p02](../../projects/phys-smallmac00008-p02/) | `phys-smallmac00008-p02` | [No optimized history gain in two-use environment feedback for full-rank qubit channels](../../projects/phys-smallmac00008-p02/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00008-p02/evidence/compare_inputs.py) (6)<br>[复现指南](../../projects/phys-smallmac00008-p02/reproducibility/README.md) |
| 30 | `small_mac / 00009` | [phys-smallmac00009-p01](../../projects/phys-smallmac00009-p01/) | `phys-smallmac00009-p01` | [Unique spanning-tree families bound the static response of every complete four-state Markov network](../../projects/phys-smallmac00009-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00009-p01/supplement/check_cofactors.py) (4)<br>[复现指南](../../projects/phys-smallmac00009-p01/supplement/README.md) |
| 31 | `small_mac / 00009` | [phys-smallmac00009-p02](../../projects/phys-smallmac00009-p02/) | `phys-smallmac00009-p02` | [Pure-state uniqueness under common-axis measurements of three qubits excludes mixed-state impostors](../../projects/phys-smallmac00009-p02/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00009-p02/code/check_antipodal_rotation.py) (2)<br>[复现指南](../../projects/phys-smallmac00009-p02/manuscript/REPRODUCE.md) |
| 36 | `small_mac / 00012` | [phys-smallmac00012-p01](../../projects/phys-smallmac00012-p01/) | `phys-00012-p01` | [Order-three unistochastic matrices form a monoid: exact compression of measured qutrit dynamics](../../projects/phys-smallmac00012-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00012-p01/code/compare_inputs.py) (4)<br>[复现指南](../../projects/phys-smallmac00012-p01/REPRODUCIBILITY.md) |
| 38 | `small_mac / 00014` | [phys-smallmac00014-p01](../../projects/phys-smallmac00014-p01/) | `phys-00014-p01` | [The third magnetic Neumann eigenvalue does not exceed the Dirichlet ground state on an annulus](../../projects/phys-smallmac00014-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00014-p01/scripts/check_universal_annulus_ordering.py) (1)<br>[复现指南](../../projects/phys-smallmac00014-p01/manuscript/REPRODUCIBILITY.md) |
| 39 | `small_mac / 00014` | [phys-smallmac00014-p11](../../projects/phys-smallmac00014-p11/) | `phys-00014-p11` | [No history advantage in repeated environment-assisted qubit recovery](../../projects/phys-smallmac00014-p11/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00014-p11/code/reproduce.py) (3)<br>[复现指南](../../projects/phys-smallmac00014-p11/reproducibility/README.md) |
| 41 | `small_mac / 00015` | [phys-smallmac00015-p01](../../projects/phys-smallmac00015-p01/) | `phys-00015-p01` | [A sharp weak-driving phase bound for symmetric complete Markov networks](../../projects/phys-smallmac00015-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00015-p01/evidence/check_spectral_proof.py) (3)<br>[复现指南](../../projects/phys-smallmac00015-p01/reproducibility/README.md) |
| 42 | `small_mac / 00015` | [phys-smallmac00015-p06](../../projects/phys-smallmac00015-p06/) | `phys-00015-p06` | [A two-use history advantage under one-bit coarse-grained environment feedback](../../projects/phys-smallmac00015-p06/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00015-p06/scripts/verify_gad_global_bound.py) (1)<br>[复现指南](../../projects/phys-smallmac00015-p06/REPRODUCIBILITY.md) |
| 43 | `small_mac / 00016` | [phys-smallmac00016-p01](../../projects/phys-smallmac00016-p01/) | `phys-00016-p01` | [Exact current-bit optimum and a robust history advantage for coarse-grained generalized-amplitude-damping feedback](../../projects/phys-smallmac00016-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00016-p01/merged/phys-00016-p02/scripts/verify_robust_rectangle.py) (5)<br>[复现指南](../../projects/phys-smallmac00016-p01/manuscript/REPRODUCIBILITY.md) |
| 44 | `small_mac / 00018` | [phys-smallmac00018-p01](../../projects/phys-smallmac00018-p01/) | `phys-00018-p01` | [Exact indirect-gap boundary in a flux-one-third Harper–Hofstadter model with a period-three mass](../../projects/phys-smallmac00018-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00018-p01/manuscript/generate_phase_diagram.py) (6)<br>[复现指南](../../projects/phys-smallmac00018-p01/manuscript/REPRODUCIBILITY.md) |
| 45 | `small_mac / 00013` | [phys-smallmac00013-p03](../../projects/phys-smallmac00013-p03/) | `phys-00013-p03` | [Exact unrestricted Gaussian rank of two canonical matchgate magic states](../../projects/phys-smallmac00013-p03/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00013-p03/scripts/certify_clifford_rank_gap.py) (2)<br>[复现指南](../../projects/phys-smallmac00013-p03/REPRODUCIBILITY.md) |
| 46 | `small_mac / 00013` | [phys-smallmac00013-p04](../../projects/phys-smallmac00013-p04/) | `phys-00013-p04` | [An exact criterion for removing an elementary amplitude-damping factor from a quantum channel](../../projects/phys-smallmac00013-p04/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00013-p04/code/compare_reconstructions.py) (4)<br>[复现指南](../../projects/phys-smallmac00013-p04/manuscript/README.md) |
| 47 | `small_mac / 00013` | [phys-smallmac00013-p07](../../projects/phys-smallmac00013-p07/) | `phys-00013-p07` | [The third boundary coefficient of even off-diagonally symmetric alternating-sign matrices](../../projects/phys-smallmac00013-p07/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00013-p07/code/compare_order16.py) (7)<br>[复现指南](../../projects/phys-smallmac00013-p07/REPRODUCIBILITY.md) |
| 51 | `small_mac / 00020` | [phys-smallmac00020-p03](../../projects/phys-smallmac00020-p03/) | `phys-00020-p03` | [Two-scale finite-size edge splitting at a repeated root of an extended Su–Schrieffer–Heeger chain](../../projects/phys-smallmac00020-p03/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00020-p03/evidence/check_confluent_exact.py) (3)<br>[复现指南](../../projects/phys-smallmac00020-p03/reproducibility/README.md) |
| 52 | `small_mac / 00021` | [phys-smallmac00021-p01](../../projects/phys-smallmac00021-p01/) | `phys-00021-p01` | [Exact finite-depth crossings in a Sierpinski–Hanoi free-fermion spin model](../../projects/phys-smallmac00021-p01/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00021-p01/evidence/check_cycle_schur_pass3.py) (8)<br>[复现指南](../../projects/phys-smallmac00021-p01/manuscript/README.md) |
| 58 | `small_mac / 00023` | [phys-smallmac00023-p03](../../projects/phys-smallmac00023-p03/) | `phys-00023-p03` | [An exact anti-degradability threshold for the three-level bosonic loss–dephasing channel](../../projects/phys-smallmac00023-p03/paper.pdf) | 已证明 | [代码](../../projects/phys-smallmac00023-p03/supplementary/code/reproduction/compare_inputs.py) (9)<br>[复现指南](../../projects/phys-smallmac00023-p03/supplementary/README.md) |

## 反证 (7)

[反证](categories/disproofs/README.zh-CN.md)

| 序号 | 批次 | 公开项目 ID | 原始内部 ID | 论文题名 / PDF | 原题状态 | 代码 / 复现 |
|---:|---|---|---|---|---|---|
| 14 | `small_mac / 00001` | [phys-smallmac00001-p06](../../projects/phys-smallmac00001-p06/) | `phys-smallmac00001-p06` | [A missing spectral arc at finite cycle affinity in four-state Markov generators](../../projects/phys-smallmac00001-p06/paper.pdf) | 已反证 | [代码](../../projects/phys-smallmac00001-p06/manuscript/repro/verify_rational.py) (3)<br>[复现指南](../../projects/phys-smallmac00001-p06/manuscript/README.md)<br>[复现指南](../../projects/phys-smallmac00001-p06/manuscript/repro/README.md) |
| 16 | `small_mac / 00002` | [phys-smallmac00002-p09](../../projects/phys-smallmac00002-p09/) | `phys-smallmac00002-p09` | [A counterexample to the forward waiting-time entropy bound in periodically driven Markov networks](../../projects/phys-smallmac00002-p09/paper.pdf) | 已反证 | [代码](../../projects/phys-smallmac00002-p09/reproducibility/plot.py) (8)<br>[复现指南](../../projects/phys-smallmac00002-p09/reproducibility/README.md) |
| 21 | `small_mac / 00005` | [phys-smallmac00005-p02](../../projects/phys-smallmac00005-p02/) | `phys-smallmac00005-p02` | [A computer-assisted three-state counterexample to a nonlinear phase-lag bound](../../projects/phys-smallmac00005-p02/paper.pdf) | 已反证 | [代码](../../projects/phys-smallmac00005-p02/evidence/certify_counterexample.py) (1)<br>[复现指南](../../projects/phys-smallmac00005-p02/reproducibility/README.md) |
| 23 | `small_mac / 00006` | [phys-smallmac00006-p01](../../projects/phys-smallmac00006-p01/) | `phys-smallmac00006-p01` | [Activity above one half in finite Glauber annealing](../../projects/phys-smallmac00006-p01/paper.pdf) | 已反证 | [代码](../../projects/phys-smallmac00006-p01/code/compare_layered.py) (11)<br>[复现指南](../../projects/phys-smallmac00006-p01/reproducibility/README.md) |
| 24 | `small_mac / 00006` | [phys-smallmac00006-p02](../../projects/phys-smallmac00006-p02/) | `phys-smallmac00006-p02` | [Coherent information in uniformly noisy graph states is not ordered by subsystem size](../../projects/phys-smallmac00006-p02/paper.pdf) | 已反证 | [代码](../../projects/phys-smallmac00006-p02/supplement/replay.py) (2)<br>[复现指南](../../projects/phys-smallmac00006-p02/supplement/README.md) |
| 26 | `small_mac / 00007` | [phys-smallmac00007-p01](../../projects/phys-smallmac00007-p01/) | `phys-smallmac00007-p01` | [Common output bias matters in randomness certification from quantum speed limits](../../projects/phys-smallmac00007-p01/paper.pdf) | 已反证 | [代码](../../projects/phys-smallmac00007-p01/supplement/decimal_grid.py) (5)<br>[复现指南](../../projects/phys-smallmac00007-p01/supplement/README.md) |
| 28 | `small_mac / 00008` | [phys-smallmac00008-p01](../../projects/phys-smallmac00008-p01/) | `phys-smallmac00008-p01` | [Comment on “Distinguishing graph states by the properties of their marginals”](../../projects/phys-smallmac00008-p01/paper.pdf) | 已反证 | [代码](../../projects/phys-smallmac00008-p01/evidence/research-pass1/check_witness.py) (5)<br>[复现指南](../../projects/phys-smallmac00008-p01/supplement/README.md) |

## 部分结果 (19)

[部分结果](categories/partial-results/README.zh-CN.md)

| 序号 | 批次 | 公开项目 ID | 原始内部 ID | 论文题名 / PDF | 原题状态 | 代码 / 复现 |
|---:|---|---|---|---|---|---|
| 11 | `legacy / PHY-13` | [phys-smallmac00000-p13](../../projects/phys-smallmac00000-p13/) | `PHY-13` | [Finite total dephasing and an isolated natural occupation in an open XX chain](../../projects/phys-smallmac00000-p13/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00000-p13/manuscript/repro/reproduce.py) (2)<br>[复现指南](../../projects/phys-smallmac00000-p13/manuscript/repro/README.md) |
| 12 | `legacy / PHY-14` | [phys-smallmac00000-p14](../../projects/phys-smallmac00000-p14/) | `PHY-14` | [A second-order obstruction to localized edge-mode continuation in a non-Hermitian interacting Kitaev chain](../../projects/phys-smallmac00000-p14/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00000-p14/reproducibility/checker_core.py) (4)<br>[复现指南](../../projects/phys-smallmac00000-p14/reproducibility/README.md) |
| 18 | `small_mac / 00004` | [phys-smallmac00004-p01](../../projects/phys-smallmac00004-p01/) | `phys-smallmac00004-p01` | [Optimal single-letter private information of the dephrasure channel on a noise interval](../../projects/phys-smallmac00004-p01/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00004-p01/supplement/code/adaptive_certificate.py) (6)<br>[复现指南](../../projects/phys-smallmac00004-p01/supplement/README.md) |
| 19 | `small_mac / 00003` | [phys-smallmac00003-p02](../../projects/phys-smallmac00003-p02/) | `phys-smallmac00003-p02` | [A rank-three projection bound for the quantumness of spin-1 states](../../projects/phys-smallmac00003-p02/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00003-p02/reproducibility/verify_exact.py) (3)<br>[复现指南](../../projects/phys-smallmac00003-p02/reproducibility/README.md) |
| 27 | `small_mac / 00007` | [phys-smallmac00007-p03](../../projects/phys-smallmac00007-p03/) | `phys-smallmac00007-p03` | [A two-pineapple envelope for split-core threshold random walks](../../projects/phys-smallmac00007-p03/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00007-p03/code/check_surgery_exact.py) (2)<br>[复现指南](../../projects/phys-smallmac00007-p03/manuscript/REPRODUCIBILITY.md) |
| 32 | `small_mac / 00010` | [phys-smallmac00010-p01](../../projects/phys-smallmac00010-p01/) | `phys-00010-p01` | [Exact flat-noise transition rays from Hadamard involutions in four-level systems](../../projects/phys-smallmac00010-p01/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00010-p01/research/hadamard_involution.py) (1)<br>[复现指南](../../projects/phys-smallmac00010-p01/reproducibility/README.md) |
| 33 | `small_mac / 00010` | [phys-smallmac00010-p04](../../projects/phys-smallmac00010-p04/) | `phys-00010-p04` | [A seven-$T$ fixed measurement accessing 220 four-qubit Pauli directions](../../projects/phys-smallmac00010-p04/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00010-p04/evidence/certify_220_exact.py) (2)<br>[复现指南](../../projects/phys-smallmac00010-p04/REPRODUCIBILITY.md) |
| 34 | `small_mac / 00010` | [phys-smallmac00010-p02](../../projects/phys-smallmac00010-p02/) | `phys-00010-p02` | [Weak regulation increases stationary abundance noise in a three-species stochastic feedback ring](../../projects/phys-smallmac00010-p02/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00010-p02/evidence/weak_feedback_bounds.py) (2)<br>[复现指南](../../projects/phys-smallmac00010-p02/REPRODUCE.md) |
| 35 | `small_mac / 00011` | [phys-smallmac00011-p02](../../projects/phys-smallmac00011-p02/) | `phys-00011-p02` | [Directional stability of the reverse-depolarizing entanglement-assistance benchmark for qubit entanglement-breaking channels](../../projects/phys-smallmac00011-p02/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00011-p02/manuscript/reproducibility/make_figure.py) (1)<br>[复现指南](../../projects/phys-smallmac00011-p02/manuscript/reproducibility/README.md) |
| 37 | `small_mac / 00012` | [phys-smallmac00012-p02](../../projects/phys-smallmac00012-p02/) | `phys-00012-p02` | [A hypocycloid spectral bound for circulant unistochastic matrices without symmetric amplitudes](../../projects/phys-smallmac00012-p02/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00012-p02/code/hypocycloid_gate_no_go.py) (1)<br>[复现指南](../../projects/phys-smallmac00012-p02/reproducibility/README.md) |
| 40 | `small_mac / 00014` | [phys-smallmac00014-p03](../../projects/phys-smallmac00014-p03/) | `phys-00014-p03` | [A sharp weak-driving phase-lag bound for a symmetric three-state Markov cycle](../../projects/phys-smallmac00014-p03/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00014-p03/evidence/search_k3_phase.py) (3)<br>[复现指南](../../projects/phys-smallmac00014-p03/reproducibility/README.md) |
| 48 | `small_mac / 00019` | [phys-smallmac00019-p01](../../projects/phys-smallmac00019-p01/) | `phys-00019-p01` | [Exact signed-sum spectral locus of a six-term three-qubit Pauli Hamiltonian](../../projects/phys-smallmac00019-p01/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00019-p01/scripts/input_a_direct.py) (6)<br>[复现指南](../../projects/phys-smallmac00019-p01/reproducibility/README.md) |
| 49 | `small_mac / 00020` | [phys-smallmac00020-p01](../../projects/phys-smallmac00020-p01/) | `phys-00020-p01` | [The largest Liouvillian exceptional point need not maximize the spectral gap: An exact two-qubit counterexample](../../projects/phys-smallmac00020-p01/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00020-p01/manuscript/make_figure.py) (6)<br>[复现指南](../../projects/phys-smallmac00020-p01/REPRODUCIBILITY.md) |
| 50 | `small_mac / 00020` | [phys-smallmac00020-p02](../../projects/phys-smallmac00020-p02/) | `phys-00020-p02` | [Strict separable non-saturation for a seven-state prepare-and-measure witness](../../projects/phys-smallmac00020-p02/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00020-p02/scripts/check_product_saturation.py) (2)<br>[复现指南](../../projects/phys-smallmac00020-p02/reproducibility/README.md) |
| 53 | `small_mac / 00021` | [phys-smallmac00021-p02](../../projects/phys-smallmac00021-p02/) | `phys-00021-p02` | [A unique cubic-coupling cancellation locus for collinear constant-vorticity capillary–gravity triads](../../projects/phys-smallmac00021-p02/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00021-p02/scripts/resonance_classification.py) (1)<br>[复现指南](../../projects/phys-smallmac00021-p02/reproducibility/README.md) |
| 54 | `small_mac / 00021` | [phys-smallmac00021-p03](../../projects/phys-smallmac00021-p03/) | `phys-00021-p03` | [Comment on “Band topology of the breathing kagome lattice”](../../projects/phys-smallmac00021-p03/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00021-p03/manuscript/make_core_spectrum.py) (6)<br>[复现指南](../../projects/phys-smallmac00021-p03/README_REPRODUCIBILITY.md) |
| 55 | `small_mac / 00022` | [phys-smallmac00022-p01](../../projects/phys-smallmac00022-p01/) | `phys-00022-p01` | [Local stability of a two-copy entanglement-of-purification ansatz at the von Neumann boundary](../../projects/phys-smallmac00022-p01/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00022-p01/evidence/analyze_u16_tangent.py) (6)<br>[复现指南](../../projects/phys-smallmac00022-p01/manuscript/README.md) |
| 56 | `small_mac / 00022` | [phys-smallmac00022-p02](../../projects/phys-smallmac00022-p02/) | `phys-00022-p02` | [Exact Tsirelson bound for a three-output Bell functional](../../projects/phys-smallmac00022-p02/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00022-p02/evidence/verify_exact_sos_independent.py) (1)<br>[复现指南](../../projects/phys-smallmac00022-p02/REPRODUCIBILITY.md) |
| 57 | `small_mac / 00022` | [phys-smallmac00022-p03](../../projects/phys-smallmac00022-p03/) | `phys-00022-p03` | [Exact all-parameter spectral-gap certificates for deformed-EPR Hamiltonians on small subdivided stars](../../projects/phys-smallmac00022-p03/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00022-p03/evidence/certify_subdivided_star_continuum.py) (2)<br>[复现指南](../../projects/phys-smallmac00022-p03/reproducibility/README.md) |

## 计算结果 (1)

[计算结果](categories/computational-papers/README.zh-CN.md)

| 序号 | 批次 | 公开项目 ID | 原始内部 ID | 论文题名 / PDF | 原题状态 | 代码 / 复现 |
|---:|---|---|---|---|---|---|
| 13 | `small_mac / 00001` | [phys-smallmac00001-p01](../../projects/phys-smallmac00001-p01/) | `phys-smallmac00001-p01` | [Certified local optimality of a qubit counting process over a finite mean interval](../../projects/phys-smallmac00001-p01/paper.pdf) | 仍未完全解决 | [代码](../../projects/phys-smallmac00001-p01/supplement/code/algebra.py) (4)<br>[复现指南](../../projects/phys-smallmac00001-p01/supplement/README.md) |

## 复现

每个项目均含冻结 PDF、论文源码、发布门禁选定的代码/数据、作者交接、包来源记录和 SHA-256 校验。从仓库根目录运行：

```bash
python3 reproducibility/verify_small_mac.py --all
python3 reproducibility/build_small_mac_papers.py --all
```

[`small_mac_projects.json`](../../reproducibility/small_mac_projects.json) · [SHA-256](../../reproducibility/SHA256SUMS)
