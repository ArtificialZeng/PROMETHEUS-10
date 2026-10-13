# 作者交接：竞争 SOS 树模型的二周期排除

本文是本地英文作者审阅草稿。独立 RELEASE 已完成引用核验、清洁构建和逐页视觉检查；
最终状态由 audit/citations.json、audit/build.json、audit/visual.json 与真实 release_gate 检查共同确定。
主管须在 ready 后执行本地 publish，再 make/check 投稿文件包；作者实际审阅仍待完成。
未投稿、未上传、未对外联系。目标期刊暂定 Journal of Physics A: Mathematical and
Theoretical，Paper；篇幅与意义是否满足编辑标准仍需作者判断。

## 核心结果与最难核对处

对正文给出的精确 f，所有 t,h,u>0 都有 f(f(u))=u => f(u)=u。
适用于有限实 J,J1、有限 beta>0、每个顶点有两个子节点且兄弟边只计一次的 Hamiltonian；
只排除 (1,u,1) 形式、按层齐次的正边界消息的非固定二周期。
不证明任意 Gibbs 测度的唯一性、极端性、稳定性、任意迭代收敛或零温结论。

请重点核对正文 (3.3)–(3.7) 的二变量消元、B>1-t^4 与 B<0 => t>1 的逻辑，
以及 B²<(t^4−1)²<t^8<4t^14<4AC 的严格不等式链。
Appendix A 给出另一条恒等式 H=P Q 和 Q>1，避免在固定点处除以 P。
§4 必须保留跨边界兄弟因子；根的概率取 m0 除以分量和，消息在内部顶点消去。

原始目标已由独立新上下文科学审计接受为 resolution-paper/proved；这不是外部同行评审。
接受报告为 `audit/science.md`，快照为 `audit/snapshot.json`。
本文采用接受审计中的和/积消元写法，附录保留接受证明中的平方证书；没有扩大科学范围。

## 来源和可复现文件

全部引用与新主张映射在 `writing/source-map.md`。
[2025 出版论文](https://doi.org/10.17586/2220-8054-2025-16-2-134-141)
Eq.(12), p.137 与 §5、Conjecture 1, p.139 是直接目标；必须按其排除固定点的上下文阅读。
[2026 后续](https://doi.org/10.29229/uzmj.2026-1-18) 只用于 p.166 的最近邻 Hamiltonian
和分支递推，接受审计已核对 m=g² 的变量约定。不使用该文其他相变或动力学结论。

2025 期刊版只有真实网页解析正文，没有本地成功下载的出版 PDF；预印本全文和公式图像
已保存。前向引文页仍有访问缺口，不能把有限查重说成穷尽性优先权保证。
请人类作者亲自核查两篇正文、完成必要的后续引用检索；不因 BibTeX 已能编译就视为完成。

`reproducibility/README.md` 给出无需联网的精确复算和干净构建命令。
两个移植程序沿用接受稿的不同表示：整数权重枚举及符号矩阵/和积消元；只改输出目录、
安全断言与元数据。原程序未改写。`writing/checker-adaptation.diff` 保存实际差异。
`reproducibility/expected/` 是实际重跑输出，符号程序 87 项检查通过。
这些是复现程序，重新运行不构成另一次独立审稿。

## 作者信息、AI 参与及待决定项

草稿署名按给定默认值：Xiaojian Zeng；PBC School of Finance, Tsinghua University,
100190；xiaojianzeng@foxmail.com。请确认其真实性、适当性、通讯地址和署名资格；
此处没有自动的机构背书。未自行声明经费、利益冲突、ORCID 或已完成的人类贡献。

OpenAI Codex 实质参与问题分析、证明探索、代数、代码、一手来源核查、内部 AI 审计
和英文写作，致谢已披露这些用途。必须由作者完成批判性审阅，并补全各阶段准确模型及版本；
当前授权角色/科学证据不能唯一证明所有阶段的实际服务模型版本，故未猜测。
IOP 政策的生成参考文献、人工核查、原始结果及服务权利条款还需要作者判断。
详见 `venue/aims-and-policy.md`；`venue.json` 保留 needs_author_judgment 与 pending。

作者仍需确认目标期刊/文章类型、最新优先权检索、模型/版本披露、平台服务权利条件、
经费和利益冲突、最终署名及是否对外公开/采用何种许可证。所有排序和分区保持未核实。

## 交付范围与下一步

`publication.json` 明确列出稿件、构建脚本、复现代码、必要输出和本交接文件；
不会把第三方整篇 PDF、来源缓存、内部审计、网页响应或运行日志混入投稿文件集。
`writing/redistribution-scope.md` 记录逐类检查。

下一步：主管依据真实 RELEASE 结果执行本地 publish 与 bundle make/check，然后由作者
亲自阅读证明及两篇引用原文、补全 AI 模型/版本和政策判断，再决定是否投稿。
本次 RELEASE 修正引言中一个来源定位词：排除 f(u)=u 的条件在原文式(16)之后；
数学公式和全部科学冻结输入未改变。审计报告为中文，固定编号清单为 audit/claim-inventory.md。
