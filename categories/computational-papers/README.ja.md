# PROMETHEUS-10 · 計算結果

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

検証可能な AI 支援物理研究アーカイブです。**93 件の PDF を保持し、90 件の代表研究項目を索引化しました。** 後の一般的・強い結果に含まれる初期の 3 件は関連する旧版として保持し、重複して数えません。「10」は最初のコレクション名です。

すべて人間による科学的内容、先取権、著者情報の確認が必要な研究草稿です。証明と反証は凍結された命題の明示範囲に限られます。部分結果・計算結果は元の問題の完全解決を意味しません。別の AI コンテキストでの審査は内部確認であり、外部査読や雑誌の採択ではありません。boundariness の旧草稿には過去の整合性ゲートの欠落が残ります。

科学的命題と論文名は原文言語を保持します。ナビゲーション、状態、利用方法、および最初の十件の説明は現地語化され、引用命題の数学的範囲を翻訳で変更しません。

[PROMETHEUS-10](../../README.ja.md)

[検索可能な全成果一覧](../../catalog.html) · [意味に基づく比較・重複整理](../../SEMANTIC_DEDUPLICATION.md) · [再現ガイド](../../reproducibility/README.md)

## 四つの結果分類

| | 代表項目数 |
|---|---:|
| [証明](../proofs/README.ja.md) | **32** |
| [反証](../disproofs/README.ja.md) | **18** |
| [部分結果](../partial-results/README.ja.md) | **38** |
| [計算結果](../computational-papers/README.ja.md) | **2** |

監督付きの工程は一次文献を確認し、方程式を独立に再構成し、公開済み基準を再現して、有界の研究を新しい内部審査に回します。短い証拠索引と共通ツールは反復を減らします。キャッシュ入力は入力の一部であり、未測定のトークン節約率や成功率は示しません。

## 計算結果

<details>
<summary><strong>phys-00002-p06 · A four-level Mpemba witness beyond three-level tests</strong> — 計算結果 · 研究表を展開</summary>

| | |
|---|---|
| **背景** | 熱緩和の一部では、より高温の初期状態が速く平衡に近づく。三準位の条件が高次元でも十分とは限らない。 |
| **結果と元の問題の解決範囲** | 正温・詳細釣り合いを満たす四準位の例を、100 桁と 180 桁の独立計算で確認し、検査対象の三準位必要条件を排除した。 |
| **提案する貢献** | 三準位診断への還元の限界を調べる具体的な高次元機構を示す。 |
| **限界・残された課題** | 計算結果であり、高精度計算は丸め方向を保証する厳密認証や一般的分類ではない。元の問題は未解決。 |
| **PDF とソース** | [PDF](../../projects/phys-00002-p06/paper.pdf) · [TeX](../../projects/phys-00002-p06/manuscript/main.tex) · [Bib](../../projects/phys-00002-p06/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>phys-smallmac00001-p01 · Certified local optimality of a qubit counting process over a finite mean interval</strong> — 計算結果 · 研究表を展開</summary>

| | |
|---|---|
| **物理的背景 / 元の課題** | 二能级量子计数器的单 Kraus–秩一探测器是否全局最优 |
| **元の問題の状態** | 未解決 |
| **結果と元の問題を解決した正確な範囲** | For every prescribed mean count m in \[3,6\], the connected stationary branch through the certified mean-4 point, defined by the exact equations and rational root boxes in evidence/choi-continuation-analysis.md and the 8433-cell certificate, is a strict local minimum of the counting-time variance at fixed mean, modulo common unitary basis changes. Local competitors include all nearby qubit completely positive no-count maps of Choi ranks 1 through 4, mixed initial states, and rank-2 count effects. The instrument is identical at each discrete step and counting is eventual. This is the saved local-sufficiency proposition, conditional on independent verification of its analytic chart and interval certificates. |
| **提案された貢献** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **制約 / 残る課題** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF・ソース・再現方法** | [PDF](../../projects/phys-smallmac00001-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00001-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00001-p01) · [Author handoff](../../projects/phys-smallmac00001-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00001-p01/supplement/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

整理によって論文、コード、データへの追加の利用許諾は付与されません。著者引き継ぎと適用される権利を確認してください。投稿、外部査読、採択を意味しません。
