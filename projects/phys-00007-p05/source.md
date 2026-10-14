## phys-00007-p05｜任意双qubit酉门叠加白噪声，其条件信道min-entropy能否直接由Choi态求得？

**1．冻结模型与精确命题。** 四个端口 \(A',B',A,B\simeq\mathbb C^2\)，\(U\in U(4)\)，\(p\in[0,1]\)，单次CPTP信道
\[
\mathcal N_{p,U}(X)=(1-p)UXU^\dagger+p\operatorname{Tr}(X)I_4/4.
\]
不假设该离散信道可嵌入时间无关GKSL半群。令 \(|\Phi_2\rangle=(|00\rangle+|11\rangle)/\sqrt2\)，归一化Choi态
\[
\Omega=(\mathrm{id}_{R_AR_B}\otimes\mathcal N_{p,U})(\Phi_{R_AA'}\otimes\Phi_{R_BB'}),\quad\operatorname{Tr}\Omega=1.
\]
取双边划分 \(X=R_AA,Y=R_BB\)。完整可执行SDP为
\[
s(\Omega)=\min_{Y_0\succeq0}\{\operatorname{Tr}Y_0:I_X\otimes Y_0\succeq\Omega\},
\]
\[
t(\Omega)=\min_{Y_0\succeq0}\{\operatorname{Tr}Y_0:I_X\otimes Y_0\succeq\Omega,\quad
\operatorname{Tr}_{B}Y_0=\tfrac12\operatorname{Tr}(Y_0)I_{R_B}\}.
\]
问题：是否对所有 \(U,p\)，\(s=t\)？等价原文 \(S_\infty[A|B]_{\mathcal N}=S_\infty(R_AA|R_BB)_\Omega-1\)，其中态条件min-entropy为 \(-\log_2s\)，信道条件min-entropy为 \(-\log_2t-1\)。约束中的边缘归一化不能丢掉。

**2．一手原文。** Himanshu Badhani、Siddhartha Das，*Conditional channel entropy sets fundamental limits on thermodynamic quantum information processing*，[arXiv:2604.01217v2](https://arxiv.org/html/2604.01217v2)，2026-06-23，当前版本页最新v2；未登记已核期刊DOI。实际读取§II定义、§IV条件min-entropy、§VI.1 Proposition 10及Eqs.(166)–(170)、Figure 2和其后明确open段、Appendix D。其他热力学定理证明未逐段全读。原文配有 [ancillary matrix.txt](https://arxiv.org/src/2604.01217v2/anc/matrix.txt) 线索，本轮未确认其是否用于此图，不能假定为完整复现代码。

**3．已知与差异。** Proposition 10已证明无噪声双qubit酉门；Fig.2只展示CNOT、SWAP、identity与白噪声的数值吻合，随后明确猜想可推广到全部带白噪声酉门。已查v2与Badhani/Das近期题名，未取得后续证明；第一新意杀手是同作者 *Conditional entropy and information of quantum processes*（Siddhartha Das、Kaumudibikash Goswami、Vivek Pandey，[arXiv:2410.01740v2](https://arxiv.org/abs/2410.01740v2)，2024-10-30）的一般对称性结论与v2 Appendix D的证明能否直接扩张到噪声。该前作本轮仅作为引用线索，尚未完整读取；因此 **status-uncertain**。若只是现有twirling定理的常规推论，应停放，不宣称新机制。

**4．基准与判别设计。** 最小已发表基准采用 Robert König、Renato Renner、Christian Schaffner，*The Operational Meaning of Min- and Max-Entropy*，IEEE Trans.Inf.Theory55,4337–4347(2009)，[DOI:10.1109/TIT.2009.2025545](https://doi.org/10.1109/TIT.2009.2025545)，[机构公开出版PDF](https://ir.cwi.nl/pub/14805/14805A.pdf)；本次已读取§I-A Definition 1与§I-C2、Theorem 2的纯态/最大纠缠操作含义。其标准态SDP在归一化 \(\Phi_4\) 上 \(H_{\min}(X|Y)=-2\)、\(I_{16}/16\) 上为 \(+2\)；这是已发表态熵定理的具体维数基准，不声称2009已定义当前条件信道熵。用2026信道定义的 \(-1\) 因子再校验SWAP与替换端点。然后对Fig.2的三个门，在 \(p=0,1/2,1\) 重算两个独立SDP；无噪声SWAP的信道熵 \(-3\)、完全混合替换 \(p=1\) 的 \(+1\) 也检验所有维数因子。这组2026带噪声图仍是公开预印本基准，区别于前述2009期刊态熵基准。A：直接按4阶Kraus/矩阵元重建16阶归一化Choi；B：对 \(|U\rangle\!\rangle/2\) 构造 \(\Omega=(1-p)|U\rangle\!\rangle\langle\!\langle U|/4+pI_{16}/16\)，按独立索引重排计算。首个35分钟块可在两qubit Cartan非局部门的三角参数域选点、求 \(t-s\)，找严格正值；用态SDP上界和信道SDP对偶下界的严格分离认证。若所有点等号，则检查最优 \(Y_0\) 是否由对称平均强制满足TP边缘，以确定证明或直接前作覆盖路线。16阶LMI、4阶辅助变量，现有CVXPY/SCS或CLARABEL可用；浮点 \(10^{-8}\) 差不能作反例。

**5．最小成果与用途。** 一条精确关系把额外带TP边缘约束的信道资源优化降为标准态min-entropy SDP；若反例，则量化仅查看归一化Choi态时对单次条件纯度形成代价的误判。此处Hamiltonian平凡；不跨称一般有限温热浴、LOCC容量或正则化通信容量。

**6．去重与状态。** 与旧退相位—擦除信道私有信息是不同操作资源、不同约束、不同目标；不是量子电池振幅阻尼能量优化或Doeblin重置权重。状态：**待核验／status-uncertain；核心公开输入完整，优先可复现**。


