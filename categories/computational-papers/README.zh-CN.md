# PROMETHEUS-10 · 计算结果

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

可检查的 AI 辅助物理研究档案。**保留 93 份 PDF，按 90 个规范研究条目索引。** 三项被后续更一般或更强结论覆盖的早期结果保留为关联历史版本，不重复计数。“10”沿用首批项目名称，不是当前论文数。

全部为待人类科学、新颖性和署名审核的研究草稿。证明、反证仅针对冻结命题的精确范围；部分结果、计算结果不表示原题完整解决。全新 AI 审查是内部检查，不是外部同行评审或期刊接收。原信道 boundariness 稿件仍保留历史绑定门禁缺口。

科学命题和论文标题保留原文语言。导航、状态和使用说明已本地化，首批十篇保留原多语言详解；不会在翻译中悄悄改变数学范围。

[PROMETHEUS-10](../../README.zh-CN.md)

[可搜索完整成果总表](../../catalog.html) · [语义比较与去重记录](../../SEMANTIC_DEDUPLICATION.md) · [复现指南](../../reproducibility/README.md)

## 按四大结果类别浏览

| | 规范条目 |
|---|---:|
| [证明](../proofs/README.zh-CN.md) | **32** |
| [反证](../disproofs/README.zh-CN.md) | **18** |
| [部分结果](../partial-results/README.zh-CN.md) | **38** |
| [计算结果](../computational-papers/README.zh-CN.md) | **2** |

监督流程核验一手原文，独立重建方程，复现发表基准，开展有界研究，再由全新内部审查角色核验后成文和发布检查。短证据索引、共用工具及语义去重减少重复工作；缓存输入属于输入的子集，不重复相加。不编造 token 节省比例或成功率。

## 计算结果

<details>
<summary><strong>phys-00002-p06 · A four-level Mpemba witness beyond three-level tests</strong> — 计算结果 · 点击展开研究表格</summary>

| | |
|---|---|
| **物理背景** | 某些热弛豫模型中，更热的初态反而更快接近平衡。三能级系统的判据能否直接推广到更高维？ |
| **结果及原问题解决程度** | 构造正温、满足细致平衡的四能级见证；100 位和 180 位独立计算支持结果，同时排除所测试的三能级必要条件。 |
| **拟议创新与用途** | 提供一个具体高维机制，用来检验将热弛豫压缩为三能级诊断的局限。 |
| **卡点、缺憾与适用边界** | 属于计算论文；高精度不等于定向舍入认证，也不是完整分类。原问题仍未解决。 |
| **PDF 与源码** | [PDF](../../projects/phys-00002-p06/paper.pdf) · [TeX](../../projects/phys-00002-p06/manuscript/main.tex) · [Bib](../../projects/phys-00002-p06/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>phys-smallmac00001-p01 · Certified local optimality of a qubit counting process over a finite mean interval</strong> — 计算结果 · 点击展开研究表格</summary>

| | |
|---|---|
| **物理背景 / 原始课题** | 二能级量子计数器的单 Kraus–秩一探测器是否全局最优 |
| **原题状态** | 未解决 |
| **结论及原题解决的精确范围** | For every prescribed mean count m in \[3,6\], the connected stationary branch through the certified mean-4 point, defined by the exact equations and rational root boxes in evidence/choi-continuation-analysis.md and the 8433-cell certificate, is a strict local minimum of the counting-time variance at fixed mean, modulo common unitary basis changes. Local competitors include all nearby qubit completely positive no-count maps of Choi ranks 1 through 4, mixed initial states, and rank-2 count effects. The instrument is identical at each discrete step and counting is eventual. This is the saved local-sufficiency proposition, conditional on independent verification of its analytic chart and interval certificates. |
| **拟议贡献与创新点** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **卡点、缺憾及适用限制** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF、源码与复现** | [PDF](../../projects/phys-smallmac00001-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00001-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00001-p01) · [Author handoff](../../projects/phys-smallmac00001-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00001-p01/supplement/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

整理入库不自动授予论文、代码或数据的额外许可。请查看原作者交接和适用权利说明；不表示投稿、同行评审或接收。
