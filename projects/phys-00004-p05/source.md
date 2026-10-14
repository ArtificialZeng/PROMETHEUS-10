## phys-00004-p05｜单比特unital噪声，能否增加二比特态的对角量子失谐？

**1. 模型与命题。** \(\rho_{AB}\ge0\)、\(\operatorname{Tr}\rho_{AB}=1\)，\(A,B\cong\mathbb C^2\)。要求操作前后 \(\rho_A\)均非简并，以各自本征投影定义
\[
\pi_A(\rho)=\sum_{\nu=\pm}(\Pi_\nu\otimes I)\rho(\Pi_\nu\otimes I),
\qquad
D_{\rm diag}(\rho)=S(\pi_A\rho)-S(\rho),
\]
熵以2为底。所有单比特unital CPTP通道可按适当输入输出酉写成
\[
\mathcal E(\tau)=\sum_{\mu=0}^3p_\mu U\sigma_\mu V\tau
V^\dagger\sigma_\mu U^\dagger,\quad
p_\mu\ge0,\quad\sum_\mu p_\mu=1,\quad U,V\in SU(2),
\]
其中\(\sigma_0=I\)。待判别：上述全部 \(\rho,\mathcal E\)是否满足
\[
D_{\rm diag}((\mathcal E\otimes{\rm id})(\rho))
\le D_{\rm diag}(\rho)?
\]
这是单次通道命题，不要求它可嵌入时间无关GKSL；不得额外限制为Pauli半群。简并边界不能任意挑本征基制造不连续“反例”。

**2. 原文与读取。** Zi-Wen Liu、Ryuji Takagi、Seth Lloyd，*Diagonal quantum discord*，J. Phys. A **52**,135301 (2019)，[DOI](https://doi.org/10.1088/1751-8121/ab0774)、[1708.09076v2](https://arxiv.org/html/1708.09076v2)（2019-02-25，所查最新版）。已读§II定义、§III单比特情形、Conjecture 1、Fig.2、Theorems 3和5及连续性讨论，未通读全部证明。

**3. 已知结果、差异与覆盖风险。** 原文已证明若干与本征基去相干可交换的操作及相应高维分类结果；单比特非各向同性unital通道是其特别保留的缺口。Fig.2的随机态支持不是单调性证明。本题只冻结 \(B\)也为单比特的反例入口，未将其等同于原文全部辅助维数。已检查版本页，并按题名、monotonicity/counterexample和作者后续检索；未取得解决这一例外的后作原文。最可能覆盖的是量子失谐资源理论中局部不产生失谐操作的分类定理，不能将“操作不产生失谐”直接等同于“这个特定函数必单调”。**status-uncertain**，旧论文的猜想身份不足以单独确认今日开放。

**4. 输入、基准与判别。** 无私有输入。已发表基准取Fig.2(a)明确给定的通道
\[
\mathcal E_H=\tfrac13{\rm id}+\tfrac23{\rm Ad}_H,\qquad
H=(X+Z)/\sqrt2,
\]
复现其输入/输出比较流程，并用Theorem 3覆盖的各向同性通道校验单调性；原图随机种子未给，不能声称逐点复现。两套独立去相干构造：本征投影求和；从
\(\rho_A=(I+\boldsymbol r\cdot\boldsymbol\sigma)/2\)得到
\[
\pi_A\rho=\tfrac12\left[\rho+
(\widehat{\boldsymbol r}\cdot\boldsymbol\sigma\otimes I)
\rho(\widehat{\boldsymbol r}\cdot\boldsymbol\sigma\otimes I)\right].
\]
通道另用Kraus与Bloch表示互核。最便宜攻击是完整复密度矩阵、各向异性 \(p_\mu\)和接近但不等于简并的边缘态；不只扫描X态。严格增益需同时认证前后边缘谱隙、CPTP约束和熵误差。至多 \(4\times4\) 状态，单worker、不足1 GiB；近零本征值的熵误差是主要卡点。

**5. 最小成果与用途。** 认证反例，或某个非各向同性通道族上的全态单调性定理。它决定这种无需测量优化的失谐量能否可靠跟踪局部噪声下的量子关联。反例只否定该量及其操作范围，不否定所有量子失谐定义。

**6. 历史区别与状态。** 最近邻是大Mac第03批binegativity的PPT单调性；本题对象是可能存在于可分态中的失谐，允许操作是局部unital通道，非PPT纠缠资源转换。与ACC/CQC固定测量互信息也不同，本题测量基随边缘态变化。**待核验；status-uncertain。**


