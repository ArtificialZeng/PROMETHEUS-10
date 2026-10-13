# 作者交接：共同偏置反例

本地稿题为 *Common output bias matters in randomness certification from quantum speed limits*。
本次清洁构建 PDF：`build/release-fbca9ca8/main.pdf`；正文与文献：`manuscript/main.tex`、`manuscript/references.bib`。
新鲜 release 任务已完成固定主张/引用核验、清洁构建、两套证书重放以及最终 PDF 全部6页的实际图像审查。监管流程随后负责本地激活与最终打包；尚未对外提交。

核心结果仅针对平均分支速度预算松弛：取 e=1/2，偏心点
(sin(3/5),−sin(2/5)) 与同相关差中心点 (d,−d)，前者 H⋆>0.7758，后者 H⋆<0.7653，严格差>0.0105 bits。
它否定 Jones 等的恒取等猜想；原有中心保守下界继续成立。没有求出最优熵，也未证明真实总态方差限制下的最优攻击、量子旁信息安全性或有限轮安全性。

作者最需复核三点：全角度域的仿射不等式及端点误差控制；中心三分支的精确相关/预算等式；平均分支标准差与真实总态方差的方向关系。正文给出完整论证，附录给出第二种连续区间覆盖。证明相关代码均可直接重算，不依赖发现阶段的 LP。

`supplement/README.md` 给出一个顺序命令重放 Decimal 节点证书和整数区间证书，以及绘图和清洁构建方法。实测两种重放均通过，约需14秒及9秒；只是本机观测，不是速度保证。公开交接文件不需要下载论文全文或私有日志。

来源定位：Jones et al. arXiv:2506.14526v3 第4页式(8)–(9)、第13页式(27)、第15页式(32)、第16页 Lemma 3 后猜想、第21页下界传播；Van Himbeeck–Pironio v1 第11–14页式(26)–(29)及第18页 Remark 9；空间对称性论文v4附录E式(55)–(58)。逐项来源与本稿新结果的区分见 `supplement/SOURCE_MAP.md`。文献检查有界，不宣称绝对首创。

拟投定位为 [Physical Review A 的 Regular Article](https://journals.aps.org/pra/authors)，范围符合其量子信息栏目；重要性与具体投稿选择待作者判断。见 `venue.json` 和 `venue/aims-and-policy.md`。SCIE及任何分区/排名均未核实。

请作者确认姓名 Xiaojian Zeng、单位 PBC School of Finance, Tsinghua University, Beijing 100190, China 和邮箱 xiaojianzeng@foxmail.com，并亲自审查结果与全部引用。
AI 实质参与了比较文献、选点、推导、代码、检查、解释、图代码与写作。稿中已披露；写作环境识别为GPT-6，以往各阶段确切模型修订未独立确认。应补齐真实版本记录与作者本人指导、验证方式，并根据[APS现行政策](https://journals.aps.org/authors/appropriate-use-ai-tools)完成权利及投稿合规判断。现状不是已完成的人类审阅。

下一步由监管流程运行 release_gate.py publish，再运行 bundle.py make 和 bundle.py check，生成本地 release/main.pdf 与 submission.zip。当前完成的是 draft_ready_author_review_required 草稿审计；任何新的中央科学结果必须重新进入科学审查。最终对外发布、开放许可和提交均仍待作者决定。
