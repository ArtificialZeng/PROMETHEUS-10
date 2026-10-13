# PROMETHEUS-10

**AI の物理学を、検証できる形に**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

AI が推論・反例探索・計算に参加した十本の物理学草稿と、主張を調べるためのコードをまとめました。PROMETHEUS-10 は自動研究を検証可能な成果として残す試みです。「10」は原稿数であり、十個の一般問題をすべて解決したという意味ではありません。

過去の内部審査記録は **証明 4 件、反証 3 件、部分結果 2 件、計算論文 1 件**。猜想のみの PDF はありません。すべて著者の最終確認を要する草稿で、外部査読や掲載承認を意味しません。

人間が定めた目標の下、AI が導出、プログラミング、数値探索、検査、執筆を支援しました。別の AI コンテキストによる検査は外部査読ではありません。「貢献」は原稿が提案する内容で、本パッケージ化で文献全体の先取性を再審査したわけではありません。

<!-- SMALL_MAC_COLLECTION -->

## small_mac 拡張：成果区分別の 48 本の原稿

このリポジトリには **58 本の原稿**、すなわち元の PROMETHEUS-10 の 10 プロジェクトと **48 本の small_mac 物理学草稿**が含まれます。元の 10 プロジェクトと科学的範囲は以下に記載されています。

small_mac の各項目は記録されたローカルの科学・原稿・公開ゲートを通過していますが、著者による最終確認が必要です。外部査読や掲載受理を意味しません。

分類は凍結済みの公開記録に基づきます。「証明」と「反証」は記載された命題と仮定に対するものです。部分結果と計算結果は元の問題の完全解決を意味しません。科学的範囲と限界は各 PDF と著者引継ぎ資料をご確認ください。

[small_mac 全コレクション](collections/small_mac/README.ja.md)

| 成果区分 | 原稿数 |
|---|---:|
| [証明](collections/small_mac/categories/proofs/README.ja.md) | **21** |
| [反証](collections/small_mac/categories/disproofs/README.ja.md) | **7** |
| [部分結果](collections/small_mac/categories/partial-results/README.ja.md) | **19** |
| [計算結果](collections/small_mac/categories/computational-papers/README.ja.md) | **1** |

表示番号 11–58、バッチ番号、元の内部プロジェクト ID を保持しています。公開 `phys-smallmac` ID は共通のプロジェクトディレクトリを指します。対応表： [`id-map.json`](collections/small_mac/id-map.json).

<!-- END_SMALL_MAC_COLLECTION -->

| 課題 | 結論の種類 | 詳細 |
|---|---|---|
| [phys-00002-p01](projects/phys-00002-p01/paper.pdf) · 量子ビットに必要なノイズ経路はいくつか | 部分結果 | ↓ 01 |
| [phys-00002-p02](projects/phys-00002-p02/paper.pdf) · 四つの量子ビット測定の厳密な両立可能性閾値 | 証明 | ↓ 02 |
| [phys-00002-p06](projects/phys-00002-p06/paper.pdf) · 三準位の判定を超える四準位 Mpemba 例 | 計算結果 | ↓ 03 |
| [phys-00002-p15](projects/phys-00002-p15/paper.pdf) · 臨界リセットは量子コヒーレンスをどう消すか | 証明 | ↓ 04 |
| [phys-00003-p01](projects/phys-00003-p01/paper.pdf) · トルク駆動はガウス粒子の流れのノイズを減らせるか | 証明 | ↓ 05 |
| [phys-00004-p01](projects/phys-00004-p01/paper.pdf) · 二つのノイズ付き量子電池に共同入力の利点はあるか | 証明 | ↓ 06 |
| [phys-00004-p02](projects/phys-00004-p02/paper.pdf) · 不確定性の猜想を破る厳密な三準位反例 | 反証 | ↓ 07 |
| [phys-00005-p01](projects/phys-00005-p01/paper.pdf) · 16 頂点のグラフがパス最小性を破る | 反証 | ↓ 08 |
| [phys-00006-p01](projects/phys-00006-p01/paper.pdf) · 量子メモリが普遍的収縮界の提案を破る | 反証 | ↓ 09 |
| [phys-00007-p01](projects/phys-00007-p01/paper.pdf) · チャネルの境界度はいつ厳密に乗法的になるか | 部分結果・保存草稿 | ↓ 10 |

<details>
<summary><strong>01 · 量子ビットに必要なノイズ経路はいくつか</strong> — 部分結果 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | Lindblad 生成子は記憶のない開放量子系を記述する。単一のジャンプ演算子で占有確率移行領域の境界全体を実現できるだろうか。 |
| **結果と元の問題の解決範囲** | a=1/2 の単一ジャンプ停留点近傍で、ランクが高々二の摂動に対する有限半径の局所最適性を認証。元の大域的問題は未解決。 |
| **提案する貢献** | 数値的な停留点を区間演算の証明書に変換し、近傍の競合生成子を排除する。 |
| **限界・残された課題** | 認証半径は 10^-4。大域的な埋め込み可能性の境界や遠方の改善例は扱わない。 |
| **PDF とソース** | [PDF](projects/phys-00002-p01/paper.pdf) · [TeX](projects/phys-00002-p01/manuscript/main.tex) · [Bib](projects/phys-00002-p01/manuscript/references.bib) · [Code / data](projects/phys-00002-p01) · `python reproducibility/reproduce.py --project phys-00002-p01` |

</details>

<details>
<summary><strong>02 · 四つの量子ビット測定の厳密な両立可能性閾値</strong> — 証明 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | ノイズを加えた測定は、一つの親測定の周辺測定として実現できる場合がある。必要なノイズ量はどこで決まるか。 |
| **結果と元の問題の解決範囲** | 厳密に順序付けられた共面・不偏・二値の四測定で、共通の可視度を持つ場合の閾値 1/D を証明する草稿。 |
| **提案する貢献** | 構成と双対上界の一致により解析的閾値を導き、SOCP/SDP で照合する。 |
| **限界・残された課題** | この四測定の幾何とノイズモデルに限定。任意の POVM や測定数には一般化していない。 |
| **PDF とソース** | [PDF](projects/phys-00002-p02/paper.pdf) · [TeX](projects/phys-00002-p02/manuscript/main.tex) · [Bib](projects/phys-00002-p02/manuscript/references.bib) · [Code / data](projects/phys-00002-p02) · `python reproducibility/reproduce.py --project phys-00002-p02` |

</details>

<details>
<summary><strong>03 · 三準位の判定を超える四準位 Mpemba 例</strong> — 計算結果 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | 熱緩和の一部では、より高温の初期状態が速く平衡に近づく。三準位の条件が高次元でも十分とは限らない。 |
| **結果と元の問題の解決範囲** | 正温・詳細釣り合いを満たす四準位の例を、100 桁と 180 桁の独立計算で確認し、検査対象の三準位必要条件を排除した。 |
| **提案する貢献** | 三準位診断への還元の限界を調べる具体的な高次元機構を示す。 |
| **限界・残された課題** | 計算結果であり、高精度計算は丸め方向を保証する厳密認証や一般的分類ではない。元の問題は未解決。 |
| **PDF とソース** | [PDF](projects/phys-00002-p06/paper.pdf) · [TeX](projects/phys-00002-p06/manuscript/main.tex) · [Bib](projects/phys-00002-p06/manuscript/references.bib) · [Code / data](projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>04 · 臨界リセットは量子コヒーレンスをどう消すか</strong> — 証明 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | ランダムなリセットは長時間の量子ダイナミクスを変える。Sibuya 更新過程の臨界指数には特別な漸近挙動がある。 |
| **結果と元の問題の解決範囲** | alpha=1、固定有限次元のユニタリ・レジスタについて、スペクトル・ピンチングへのトレースノルム収束と固定スペクトルギャップでの速度を証明。 |
| **提案する貢献** | 臨界更新係数の漸近式を非対角コヒーレンスの減衰と結び付ける。 |
| **限界・残された課題** | ギャップが閉じる極限、熱力学極限、任意のリセット規則に一様な定理ではない。 |
| **PDF とソース** | [PDF](projects/phys-00002-p15/paper.pdf) · [TeX](projects/phys-00002-p15/manuscript/main.tex) · [Bib](projects/phys-00002-p15/manuscript/references.bib) · [Code / data](projects/phys-00002-p15) · `python reproducibility/reproduce.py --project phys-00002-p15` |

</details>

<details>
<summary><strong>05 · トルク駆動はガウス粒子の流れのノイズを減らせるか</strong> — 証明 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | 非平衡駆動は揺らぎを変える。同じ平衡トラップとの比較により駆動の効果を切り分ける。 |
| **結果と元の問題の解決範囲** | 安定・無磁場・トルク駆動の不足減衰 OU モデルで、一次/三次の位置電流のノイズは対応する平衡値以上と証明。 |
| **提案する貢献** | 厳密な多項式計算と独立な Wick/Poisson 表現により、非負の超過分と勾配境界流の等号条件を特定。 |
| **限界・残された課題** | 非線形力、磁場、高次の電流は定理の対象外。 |
| **PDF とソース** | [PDF](projects/phys-00003-p01/paper.pdf) · [TeX](projects/phys-00003-p01/manuscript/main.tex) · [Bib](projects/phys-00003-p01/manuscript/references.bib) · [Code / data](projects/phys-00003-p01) · `python reproducibility/reproduce.py --project phys-00003-p01` |

</details>

<details>
<summary><strong>06 · 二つのノイズ付き量子電池に共同入力の利点はあるか</strong> — 証明 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | 相関は取り出せる仕事を変え得る。一般化振幅減衰は有限温度での緩和を表す。 |
| **結果と元の問題の解決範囲** | 指定された二回使用・エネルギー制約の下で W2(e)=2W1(e) を証明。複素入力状態と大域的ユニタリ操作による仕事抽出を含む。 |
| **提案する貢献** | 位相の縮約と厳密な多項式非負性証明書で、このモデルの最適化を完結させる。 |
| **限界・残された課題** | 任意のチャネル、任意回数の使用、あらゆる仕事の定義に対する結果ではない。 |
| **PDF とソース** | [PDF](projects/phys-00004-p01/paper.pdf) · [TeX](projects/phys-00004-p01/manuscript/main.tex) · [Bib](projects/phys-00004-p01/manuscript/references.bib) · [Code / data](projects/phys-00004-p01) · `python reproducibility/reproduce.py --project phys-00004-p01` |

</details>

<details>
<summary><strong>07 · 不確定性の猜想を破る厳密な三準位反例</strong> — 反証 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | エントロピー的不確定性は、両立しない測定の同時予測可能性を制限する。スペクトルの要約だけでは情報が不足する場合がある。 |
| **結果と元の問題の解決範囲** | 有理数による厳密な三次元ユニタリ行列で、対象の extended-MUB 猜想を反証。 |
| **提案する貢献** | 短い有理算術の証明書により、第二特異値だけでは提案された普遍的主張を支えられないと示す。 |
| **限界・残された課題** | 特定の猜想の反証であり、不確定性原理の否定ではない。最適な代替不等式は未確立。 |
| **PDF とソース** | [PDF](projects/phys-00004-p02/paper.pdf) · [TeX](projects/phys-00004-p02/manuscript/main.tex) · [Bib](projects/phys-00004-p02/manuscript/references.bib) · [Code / data](projects/phys-00004-p02) · `python reproducibility/reproduce.py --project phys-00004-p02` |

</details>

<details>
<summary><strong>08 · 16 頂点のグラフがパス最小性を破る</strong> — 反証 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | 量子ウォークの平均混合は長期的な帰還構造を表し、輸送と局在に関する極値問題につながる。 |
| **結果と元の問題の解決範囲** | 16 頂点・62 辺の連結単純無重みグラフの laziness は 1673/1192、パスは 23/16。その差は -81/2384。 |
| **提案する貢献** | 二つの厳密表現により、指定された Laplacian 量子ウォークのパス最小性に有限反例を与える。 |
| **限界・残された課題** | 全サイズでの最小グラフの分類や、他のハミルトニアン・規格化は未解決。 |
| **PDF とソース** | [PDF](projects/phys-00005-p01/paper.pdf) · [TeX](projects/phys-00005-p01/manuscript/main.tex) · [Bib](projects/phys-00005-p01/manuscript/references.bib) · [Code / data](projects/phys-00005-p01) · `python reproducibility/reproduce.py --project phys-00005-p01` |

</details>

<details>
<summary><strong>09 · 量子メモリが普遍的収縮界の提案を破る</strong> — 反証 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | チャネルの収縮界は識別可能性の損失を定量化する。補助量子メモリがあると、補助系なしの直感は通用しないことがある。 |
| **結果と元の問題の解決範囲** | 等しい周辺状態を持つ有効なエンタングル入力と振幅減衰の厳密例で、提案された普遍的 alpha-Doeblin hockey-stick 置換界を反証。 |
| **提案する貢献** | 元の入力条件を満たしたまま、メモリ依存の破綻機構を特定する証明書。 |
| **限界・残された課題** | すべての Doeblin 不等式を否定するわけではなく、最適な代替界は与えていない。 |
| **PDF とソース** | [PDF](projects/phys-00006-p01/paper.pdf) · [TeX](projects/phys-00006-p01/manuscript/main.tex) · [Bib](projects/phys-00006-p01/manuscript/references.bib) · [Code / data](projects/phys-00006-p01) · `python reproducibility/reproduce.py --project phys-00006-p01` |

</details>

<details>
<summary><strong>10 · チャネルの境界度はいつ厳密に乗法的になるか</strong> — 部分結果・保存草稿 · 研究内容の表を開く</summary>

| | |
|---|---|
| **背景** | 境界度は凸集合内でのチャネルと境界との関係を測る。テンソル積は単体にはない最適化構造を示し得る。 |
| **結果と元の問題の解決範囲** | &#124;s&#124;、&#124;t&#124; ≤ 1/5 の明示的二パラメータ・フルランク・非ユニタル量子ビット Choi 族で厳密な乗法性を証明。 |
| **提案する貢献** | Choi、Sturm、LDL の記号検査により、テンソル積最適値を厳密に扱える具体的な族を示す。 |
| **限界・残された課題** | 一般問題は未解決。過去の提出パッケージ検査は証拠/原稿の対応付けで失敗しており、PDF は検査済み公開版ではなく保存草稿として収録。 |
| **PDF とソース** | [PDF](projects/phys-00007-p01/paper.pdf) · [TeX](projects/phys-00007-p01/manuscript/main.tex) · [Bib](projects/phys-00007-p01/manuscript/references.bib) · [Code / data](projects/phys-00007-p01) · `python reproducibility/reproduce.py --project phys-00007-p01` |

</details>


## 結果を再現する

今回の再実行には Python 3.12 を使用しました。下記の三準位反例は標準ライブラリだけで動きます。全課題には仮想環境へ固定版の科学計算依存関係を導入してください。ランナーは新しいコピーで計算し、保存済み証拠を変更しません。AI アカウント、API キー、ブラウザのログインは不要です。

```bash
# Standard-library-only exact counterexample
python3 projects/phys-00004-p02/reproducibility/verify_counterexample.py

# Full scientific environment and replay
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python reproducibility/reproduce.py --all
```

実行コマンド・結果・限界は [reproducibility/VALIDATION.md](reproducibility/VALIDATION.md) に記録しています。終了コード 0 だけでは科学的証明になりません。厳密算術、区間認証、高精度例、浮動小数点テストは証拠としての強さが異なります。
各課題に TeX、Bib、図を同梱。[reproducibility/README.md](reproducibility/README.md) に再実行と PDF ビルド手順があります。保存 PDF のバイト列は維持し、別の TeX 環境での完全なバイト一致は保証しません。

## 過去の公開検査に関する例外

`phys-00007-p01` には PDF と実行可能な記号計算がありますが、過去の提出パッケージ検査は証拠と原稿の対応付けで失敗しました。保存草稿として明示しています。再パッケージ化やコードの成功は、この失敗の解消や新たな科学審査を意味しません。

## 著者と利用権

原稿の著者名は **Xiaojian Zeng** で、著者情報と最終承認は本人の確認が必要です。AI・計算支援を明示しています。今回の作業で追加のオープンソースまたは Creative Commons ライセンスは付与していません。権利は各権利者に留保されます。第三者の論文は引用のみで再配布せず、依存ライブラリはそれぞれのライセンスに従います。
