# PROMETHEUS-10

**让 AI 的物理结论经得起复算**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md)

十份由 AI 参与推导、反例搜索和计算的物理论文草稿，以及用于检查结论的源代码。PROMETHEUS-10 希望把自动研究的突破口留在可检验的公式与程序里。“10”指十份文稿，并不等于十个问题全部解决。

历史内部审查记录：**4 项证明、3 项反证、2 篇局部结果稿、1 篇计算稿**；没有纯猜想 PDF。全部仍需作者最终审核，不代表外部同行评审通过或期刊接收。

AI 在人类设定的目标和约束下参与推导、编程、数值搜索、检查及写作。独立 AI 上下文不等于外部同行评审。“创新”列描述文稿提出的贡献，本次整理未重新进行覆盖全部后续文献的新颖性审计。

| 课题 | 结论类别 | 展开详情 |
|---|---|---|
| [phys-00002-p01](projects/phys-00002-p01/paper.pdf) · 一个量子比特究竟需要多少噪声通道？ | 局部结果 | ↓ 01 |
| [phys-00002-p02](projects/phys-00002-p02/paper.pdf) · 四个量子比特测量的精确兼容阈值 | 证明 | ↓ 02 |
| [phys-00002-p06](projects/phys-00002-p06/paper.pdf) · 四能级 Mpemba 见证：三能级判据的边界 | 计算结果 | ↓ 03 |
| [phys-00002-p15](projects/phys-00002-p15/paper.pdf) · 临界重置如何抹去量子相干 | 证明 | ↓ 04 |
| [phys-00003-p01](projects/phys-00003-p01/paper.pdf) · 力矩驱动能否降低高斯粒子的流噪声？ | 证明 | ↓ 05 |
| [phys-00004-p01](projects/phys-00004-p01/paper.pdf) · 两次噪声量子电池：联合输入能多取功吗？ | 证明 | ↓ 06 |
| [phys-00004-p02](projects/phys-00004-p02/paper.pdf) · 一个三能级精确反例，击中不确定性猜想 | 反证 | ↓ 07 |
| [phys-00005-p01](projects/phys-00005-p01/paper.pdf) · 16 个顶点，击破路径图最小性命题 | 反证 | ↓ 08 |
| [phys-00006-p01](projects/phys-00006-p01/paper.pdf) · 量子记忆让一个普遍收缩界失效 | 反证 | ↓ 09 |
| [phys-00007-p01](projects/phys-00007-p01/paper.pdf) · 信道边界度何时严格相乘？ | 局部结果 · 存档草稿 | ↓ 10 |

<details>
<summary><strong>01 · 一个量子比特究竟需要多少噪声通道？</strong> — 局部结果 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | Lindblad 生成元描述无记忆开放量子动力学。单个跳跃算符能否覆盖量子比特布居转移区域的整个边界？ |
| **结果及原问题解决程度** | 在 a=1/2 的单跳跃驻点附近，得到对秩至多为二的扰动成立的有限半径局部最优性证书。原始全局问题未解决。 |
| **拟议创新与用途** | 将数值驻点转化为可检查的区间算术证书，排除一小片邻域内的竞争生成元。 |
| **卡点、缺憾与适用边界** | 认证半径为 10^-4；不能推导全局可嵌入边界，也不能排除远处更优构造。 |
| **PDF 与源码** | [PDF](projects/phys-00002-p01/paper.pdf) · [TeX](projects/phys-00002-p01/manuscript/main.tex) · [Bib](projects/phys-00002-p01/manuscript/references.bib) · [Code / data](projects/phys-00002-p01) · `python reproducibility/reproduce.py --project phys-00002-p01` |

</details>

<details>
<summary><strong>02 · 四个量子比特测量的精确兼容阈值</strong> — 证明 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 加入噪声后，不同量子测量有时可以由同一个母测量实现。关键是噪声达到多大才足够。 |
| **结果及原问题解决程度** | 在四个严格有序、共面、无偏二元量子比特测量且可见度相同的条件下，草稿证明阈值为 1/D。 |
| **拟议创新与用途** | 构造与对偶界相吻合，给出解析阈值；SOCP/SDP 数值检查提供交叉验证。 |
| **卡点、缺憾与适用边界** | 只覆盖指定的四测量几何与噪声模型，不能外推为任意 POVM 或任意测量数的定理。 |
| **PDF 与源码** | [PDF](projects/phys-00002-p02/paper.pdf) · [TeX](projects/phys-00002-p02/manuscript/main.tex) · [Bib](projects/phys-00002-p02/manuscript/references.bib) · [Code / data](projects/phys-00002-p02) · `python reproducibility/reproduce.py --project phys-00002-p02` |

</details>

<details>
<summary><strong>03 · 四能级 Mpemba 见证：三能级判据的边界</strong> — 计算结果 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 某些热弛豫模型中，更热的初态反而更快接近平衡。三能级系统的判据能否直接推广到更高维？ |
| **结果及原问题解决程度** | 构造正温、满足细致平衡的四能级见证；100 位和 180 位独立计算支持结果，同时排除所测试的三能级必要条件。 |
| **拟议创新与用途** | 提供一个具体高维机制，用来检验将热弛豫压缩为三能级诊断的局限。 |
| **卡点、缺憾与适用边界** | 属于计算论文；高精度不等于定向舍入认证，也不是完整分类。原问题仍未解决。 |
| **PDF 与源码** | [PDF](projects/phys-00002-p06/paper.pdf) · [TeX](projects/phys-00002-p06/manuscript/main.tex) · [Bib](projects/phys-00002-p06/manuscript/references.bib) · [Code / data](projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>04 · 临界重置如何抹去量子相干</strong> — 证明 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 随机重置会改变量子系统的长时动力学。Sibuya 更新过程的临界指数对应特殊的渐近行为。 |
| **结果及原问题解决程度** | 在 alpha=1、固定有限维酉寄存器条件下，草稿证明迹范数收敛到谱投影去相干，并给出固定谱隙下的速率。 |
| **拟议创新与用途** | 把临界更新系数的渐近规律连接到量子非对角相干的衰减，给出可计算的速率。 |
| **卡点、缺憾与适用边界** | 限于固定维数和固定谱隙；未覆盖谱隙闭合、热力学极限或任意重置规则。 |
| **PDF 与源码** | [PDF](projects/phys-00002-p15/paper.pdf) · [TeX](projects/phys-00002-p15/manuscript/main.tex) · [Bib](projects/phys-00002-p15/manuscript/references.bib) · [Code / data](projects/phys-00002-p15) · `python reproducibility/reproduce.py --project phys-00002-p15` |

</details>

<details>
<summary><strong>05 · 力矩驱动能否降低高斯粒子的流噪声？</strong> — 证明 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 非平衡驱动会改变涨落。与同一个平衡势阱比较，可以检验驱动是否真正降低电流式观测量的噪声。 |
| **结果及原问题解决程度** | 对稳定、零磁场、力矩驱动的欠阻尼 Ornstein–Uhlenbeck 模型，证明一次/三次位置流的噪声不低于匹配平衡值。 |
| **拟议创新与用途** | 精确多项式计算以及独立 Wick/Poisson 表示识别非负超额噪声和梯度边界流的等号情形。 |
| **卡点、缺憾与适用边界** | 动力学和多项式次数受限；非线性力、磁场及更高次数不在定理范围。 |
| **PDF 与源码** | [PDF](projects/phys-00003-p01/paper.pdf) · [TeX](projects/phys-00003-p01/manuscript/main.tex) · [Bib](projects/phys-00003-p01/manuscript/references.bib) · [Code / data](projects/phys-00003-p01) · `python reproducibility/reproduce.py --project phys-00003-p01` |

</details>

<details>
<summary><strong>06 · 两次噪声量子电池：联合输入能多取功吗？</strong> — 证明 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 量子电池中的关联可能改变可提取功。广义振幅阻尼信道描述有限温度弛豫。 |
| **结果及原问题解决程度** | 在文中规定的两次使用和能量约束下，草稿证明 W2(e)=2W1(e)，覆盖复数输入态与全局酉操作提取功。 |
| **拟议创新与用途** | 通过相位约化和精确多项式非负性证书，完成该模型的两次使用优化。 |
| **卡点、缺憾与适用边界** | 不涉及任意信道、任意多次使用，也不覆盖所有功的操作定义。 |
| **PDF 与源码** | [PDF](projects/phys-00004-p01/paper.pdf) · [TeX](projects/phys-00004-p01/manuscript/main.tex) · [Bib](projects/phys-00004-p01/manuscript/references.bib) · [Code / data](projects/phys-00004-p01) · `python reproducibility/reproduce.py --project phys-00004-p01` |

</details>

<details>
<summary><strong>07 · 一个三能级精确反例，击中不确定性猜想</strong> — 反证 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 熵不确定性关系研究不兼容测量如何限制同时预测。过度压缩的谱指标可能遗漏关键结构。 |
| **结果及原问题解决程度** | 用精确有理数三维酉矩阵反驳所测试的 extended-MUB 猜想。 |
| **拟议创新与用途** | 简短的有理算术证书表明，第二奇异值不足以支撑所提出的普遍结论。 |
| **卡点、缺憾与适用边界** | 反驳的是特定猜想，不是量子不确定性原理；新的最优替代不等式仍待研究。 |
| **PDF 与源码** | [PDF](projects/phys-00004-p02/paper.pdf) · [TeX](projects/phys-00004-p02/manuscript/main.tex) · [Bib](projects/phys-00004-p02/manuscript/references.bib) · [Code / data](projects/phys-00004-p02) · `python reproducibility/reproduce.py --project phys-00004-p02` |

</details>

<details>
<summary><strong>08 · 16 个顶点，击破路径图最小性命题</strong> — 反证 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 量子行走的平均混合反映长期回返结构，图上的极值问题有助于理解输运与局域化。 |
| **结果及原问题解决程度** | 构造 16 顶点、62 边的连通简单无权图：惰性为 1673/1192，路径图为 23/16，差值为 -81/2384。 |
| **拟议创新与用途** | 两种精确表示共同认证一个有限反例，针对指定 Laplacian 量子行走的路径最小性命题。 |
| **卡点、缺憾与适用边界** | 没有分类任意规模图的最小者，也未解决其他哈密顿量和归一化约定下的问题。 |
| **PDF 与源码** | [PDF](projects/phys-00005-p01/paper.pdf) · [TeX](projects/phys-00005-p01/manuscript/main.tex) · [Bib](projects/phys-00005-p01/manuscript/references.bib) · [Code / data](projects/phys-00005-p01) · `python reproducibility/reproduce.py --project phys-00005-p01` |

</details>

<details>
<summary><strong>09 · 量子记忆让一个普遍收缩界失效</strong> — 反证 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 信道收缩界量化可区分性的损失。辅助量子记忆可能使无辅助输入下的直觉失效。 |
| **结果及原问题解决程度** | 在振幅阻尼信道中构造满足等边缘态约束的纠缠输入，精确反驳所提议的普遍 alpha-Doeblin hockey-stick 替换界。 |
| **拟议创新与用途** | 证书在原始输入约束内定位一个对量子记忆敏感的失败机制。 |
| **卡点、缺憾与适用边界** | 不意味着所有 Doeblin 不等式都无效；最优替代界尚未给出。 |
| **PDF 与源码** | [PDF](projects/phys-00006-p01/paper.pdf) · [TeX](projects/phys-00006-p01/manuscript/main.tex) · [Bib](projects/phys-00006-p01/manuscript/references.bib) · [Code / data](projects/phys-00006-p01) · `python reproducibility/reproduce.py --project phys-00006-p01` |

</details>

<details>
<summary><strong>10 · 信道边界度何时严格相乘？</strong> — 局部结果 · 存档草稿 · 点击展开课题详表</summary>

| | |
|---|---|
| **物理背景** | 边界度刻画信道在凸集合中距边界的结构；张量积可能揭示单份系统中看不到的优化机制。 |
| **结果及原问题解决程度** | 对显式二参数、满秩、非保幺的量子比特 Choi 族，在 &#124;s&#124;、&#124;t&#124; ≤ 1/5 内证明精确乘法性。 |
| **拟议创新与用途** | Choi、Sturm 与 LDL 符号检查支持一个可精确求解张量积最优值的具体模型族。 |
| **卡点、缺憾与适用边界** | 一般问题仍开放。历史投稿打包门禁因证据/文稿绑定失败；此 PDF 作为存档草稿收录，不能标作原门禁已通过。 |
| **PDF 与源码** | [PDF](projects/phys-00007-p01/paper.pdf) · [TeX](projects/phys-00007-p01/manuscript/main.tex) · [Bib](projects/phys-00007-p01/manuscript/references.bib) · [Code / data](projects/phys-00007-p01) · `python reproducibility/reproduce.py --project phys-00007-p01` |

</details>


## 复现结果

本次复跑使用 Python 3.12。下方三能级反例只需 Python 标准库；全部课题则需要在虚拟环境内安装固定版本的科学计算依赖。运行器先复制项目，再在独立输出目录执行检查，保留归档证据原样。复现这些成果不需要 AI 账号、API 密钥或浏览器登录。

```bash
# Standard-library-only exact counterexample
python3 projects/phys-00004-p02/reproducibility/verify_counterexample.py

# Full scientific environment and replay
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python reproducibility/reproduce.py --all
```

本次执行命令、结果和局限见 [复现验证记录](reproducibility/VALIDATION.md)。退出码为零本身不是科学正确性的证书。精确算术、区间认证、高精度见证和浮点压力测试的证明力不同，须结合各论文判断。
每题附 TeX、Bib 与相关图表；复跑及 PDF 编译说明见 [复现指南](reproducibility/README.md)。归档 PDF 保持原始字节，换用其他 TeX 发行版编译不保证字节完全一致。

## 一项历史发布例外

`phys-00007-p01` 已有 PDF 和可执行的符号计算，但历史投稿包因证据/文稿绑定失败而未通过门禁。此处明确作为存档草稿收录。重新打包或复跑代码成功，不等于消除该历史失败，也不等于重新完成科学审查。

## 作者与使用权

论文署名为 **Xiaojian Zeng**；署名信息与最终稿仍待作者确认。项目披露 AI 与计算辅助。本次打包没有额外授予开源或 Creative Commons 许可，权利保留于各权利人；第三方论文只引用，不随包分发。依赖库遵循各自许可。
