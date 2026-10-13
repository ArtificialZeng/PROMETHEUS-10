# 作者交接：发布审计完成的本地稿，待作者实质审阅

稿名：*Coherent information in uniformly noisy graph states is not ordered by subsystem size*。主要文件为 `build/main.pdf`、`manuscript/main.tex`、`manuscript/references.bib`、`manuscript/graph.tex`。可复现代码、精确输出与说明在 `supplement/`。文件清单以 `publication.json` 为准；此时没有外部投稿或期刊接受。

核心结论是对明确公开猜想的严格反例：连通 5×4 二分矩阵的行依次为 1001、1001、1001、0101、0011，二元秩3，在每个比特相同 P=199/200 的独立相位噪声下，S_A−S_B≈−0.0042008278631112 bits，I_A≈2.72683098764303、I_B≈2.73103181550614 bits。每个有限 r≥3 都有相同 P 的连通扩展，证明依赖明确局部核与二元熵单调性。原全称排序被反驳；这是理论电路结果，没有实验数据。

作者最需要实质复核的环节是：噪声位置及 P 与错误概率的对应；边缘谱的 2^r 重数；所有 qubit 对 S_AB=(2r+3)h₂(P) 的贡献；有理对数尾界和负差；全 r 推导；I_B 对应 A→B 的方向约定。两个正数是 hashing 下界，不是最优蒸馏率，不能从本稿得出最优方向速率也如此排序。没有最小反例规模、唯一阈值或全退极化模型结论。

本地科学审计已接受上述冻结范围；独立 AI 重放从完整错误集合和实际边表求精确偏迹及字符本征方程，并使用与提出者不同的对数级数。该过程不是人类同行评议。写作阶段把可重放实现包装为仅标准库的独立脚本，7个电路测试和6740个边缘元素检查均通过，所有科学输出字段与原独立计算相同。包装重放没有增加一个新的独立审稿人。

来源与公式逐项定位见 `manuscript/source-map.md`。主反驳目标为 Sajjad 等 *Quantum* **10**, 2111 (2026), Sec.5.4；谱/码方法承认 Sajjad 及 Goodenough 等的既有结果；操作意义定位到 Devetak–Winter 原文 Theorem10。最接近文献的有界检查不能保证全球排他优先权，稿件也没有此类声称。

目标期刊是 **Quantum Information Processing / Regular Article**，范围已查，但 AI 政策存在未解决的适配问题。`venue/aims-and-policy.md` 和 `venue.json` 记录了官方依据。现有过程含 AI 参与选题、构造、证明、代码、检查、写作和图代码，不能说成仅润色。当前没有已完成人类实质监督的记录；作者应真正理解和检验工作，并判断其产生方式与期刊政策是否可接受。披露或签字不自动消除这一问题。本稿不能被直接表述为满足投稿条件。

请作者确认姓名 Xiaojian Zeng、单位 PBC School of Finance, Tsinghua University, 100190，以及邮件 xiaojianzeng@foxmail.com。资金、利益冲突、贡献与机构相关声明仍待真实填写；没有代填“无资助/无利益冲突”。作者指南两处摘要长度存在冲突，目前遵从专门段落的 80–100 词要求，使用91词和五个关键词，正式投稿时应再次确认。排名/SCIE/JCR/CAS/SJR 未核验，不作分区或录用保证。

草稿披露当前写作使用 GPT-6-based Codex；此前所有阶段的精确模型版本未建立，不猜测或补造。对研究、代码、源文献、署名和 AI 政策的实际人类判断仍待完成。没有联系任何编辑或其他人。

重新构建使用 `python3 manuscript/build.py`；重放使用 `python3 supplement/replay.py > replay-result.json`。不要在保留有效发布绑定时随意覆盖冻结的构建或科学证据。可分发清单仅含作者稿源、图代码、复现代码/数据及说明，排除第三方论文、原始浏览器记录和内部作业日志；没有替作者选择开放许可或授权外部上传。

本次 release 已固定51项主张清单，核对三篇一手文献、精确重放输出、最终编译与六页实际图像。Goodenough v2 PDF式(13)与HTML式(19)的编号差异及机构网址已在来源映射中澄清。所有科学快照文件保持不变。发布 gate 的机器记录见 audit/release-gate-check.log；它只检查结构与哈希。

唯一下一测试：主管按本次通过的绑定执行本地 publish、bundle make/check，随后由作者实质核验科学内容及政策适配。当前不包含外部投稿；不能把本地交付或今后的作者签字视为已解决AI政策问题。
