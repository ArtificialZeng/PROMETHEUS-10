## phys-00007-p06｜五个纯态的零错误排除，已知重叠阈值是否真正锐？

**1．模型与命题。** 五个归一化复纯态 \(\psi_i\in\mathbb C^5\)，允许线性相关。可排除意为存在 \(M_i\succeq0,\sum_iM_i=I\)，且 \(\langle\psi_i|M_i|\psi_i\rangle=0\)；按原文允许零效果。令 \(G_{ij}=\langle\psi_i|\psi_j\rangle\)，
\[
t_5=\inf_{\{\psi_i\}\ {\rm 不可排除}}\max_{i<j}|G_{ij}|.
\]
判断 \(t_5=\sqrt{3/8}\) 是否成立，等价于每个 \(\varepsilon>0\) 都存在不可排除五态，最大重叠小于 \(\sqrt{3/8}+\varepsilon\)。单份、无后选择，不是多份最小错误判别。

**2．一手与阅读。** Nathaniel Johnston、Vincent Russo、Jamie Sikora，*Tight bounds for antidistinguishability and circulant sets of pure quantum states*，[arXiv:2311.17047v2](https://arxiv.org/pdf/2311.17047v2)，Quantum 9,1622(2025)，[DOI](https://doi.org/10.22331/q-2025-02-04-1622)。实际读定义、Theorem 3.2、Corollary 5.4 和 §6；§6 末段明确 \(n\ge5\) 锐性未知，Example 6.1 给四态锐例。

**3．已知与后续。** 最大重叠 \(\le\sqrt{(n-2)/(2n-2)}\) 已足够，边界包含在内；\(n\le4\) 已锐。同作者 Nathaniel Johnston、Benjamin Lovitz、Vincent Russo、Jamie Sikora 的 *The complexity of perfect quantum state classification*，[2510.20789v1](https://arxiv.org/html/2510.20789v1)，已核框架和主要结果，未给五态阈值。Debanjan Roy、Tathagata Gupta、Pratik Ghosal、Samrat Sen、Somshubhro Bandyopadhyay，*Quantum state exclusion with many copies*，[2601.14410v2](https://arxiv.org/html/2601.14410v2)，最新版2026-02-05，已读§II定义、§III主要结果和结论；它处理多份，并另要求每个效果对至少一个输入有非零概率，不覆盖本五态阈值。仍须排查 factor-width 文献，status-uncertain。

**4．输入、基准、双构造与测试。** [作者代码](https://github.com/vprusso/circulant_antidist) 可取但本次未运行。复现 Example 6.1 的四态参数族及其对偶证书。独立路线：直接态上的 POVM 可行性；Gram 矩阵分解 \(G=\sum_iV_iX_iV_i^\dagger,\ X_i\succeq0\)，\(V_i\) 嵌入除第 \(i\) 坐标外的四维子空间。最便宜测试找 \(G\succeq0,\operatorname{diag}G=1\) 和见证 \(Y\)，每个四阶主子矩阵 \(Y_{\hat i}\succeq0\)、但 \(\operatorname{Tr}YG<0\)。锐性需把这样的点连成趋阈值的认证族；一个点只给上界，不能“解决锐性”。反向攻击须证明更强统一充分阈值。小型 SDP、\(5\times5\) 矩阵、<1 GiB；卡点为边界退化和严格不可行证书。

**5．最小成果与用途。** 一个新的认证不可排除族或严格改进的统一阈值，能决定仅凭两两重叠何时保证零错误排除，减少完整 POVM 优化和实验校准。

**6．历史差异与状态。** 最近的 JRF 题研究最小错误迭代收敛；本题是精确排除的可行性与最坏重叠门槛，不能由前者直接推出。状态：待核验／status-uncertain。


