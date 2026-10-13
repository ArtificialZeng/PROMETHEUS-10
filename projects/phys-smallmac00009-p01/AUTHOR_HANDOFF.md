# 作者交接：完整四态稳态响应凸包

这是已完成本次引用、编译和逐页视觉检查的本地研究稿，最终机器门记录在
`audit/citations.json`、`audit/build.json`、`audit/visual.json`及
`release-audit/final-gate-check.log`。本角色不执行本地publish或外部投稿。
尚未取得期刊接收或人类作者批准；最终人类科学审阅、署名与期刊政策判断仍然必要。

稿名：*Unique spanning-tree families bound the static response of every
complete four-state Markov network*。

当前用户明确提供的草稿署名为 **Xiaojian Zeng**；单位为 **PBC School of
Finance, Tsinghua University, 100190**；邮箱为 **xiaojianzeng@foxmail.com**。
这些信息已照录，未采用技能中不同的旧默认姓名。请作者最终确认姓名、单位、
邮箱、实质贡献和署名资格；照录信息不表示机构认可，也不表示已经批准发表。

## 核心结论与范围

原始 `source.md` 明确询问的完整K4子问题已获本地独立科学审稿接受：任意12个
严格正、有限率，以及任意带符号无量纲d∈[-1,1]^12，稳态一阶对数响应落在346个唯一
生成树家族的响应凸包中。更强的4×12边边际矩阵H具有一个只依赖基点k、对全部
d共同有效的非负归一化分解。本次类别保持 `resolution-paper`、原题状态
`proved`，不是把一般图猜想宣布解决。

严格边界：完整四态图、每个方向一条边、全部率严格正、静态一阶响应。没有
详细平衡、小亲和力或循环对称性前提；没有一般图、全凸包可达、完整树分布
耦合、高阶导数、有限扰动误差或实验发现声明。协方差界公式归属Fancher–Horowitz
原文Eq.(8)；新内容是消除它在K4上的猜想依赖。界值仍依赖基点pi、Q和d。

## 最需要亲自核查的科学环节

1. 固定基点q_ij=k_ij pi_j(0)保持同根树分布。求导时不对缩放因子求导，不把
   d限制在Eulerian流锥内，最终仍按原pi居中。
2. 减去反向边最小流后，残余支持只能是强连通四顶点、三角加孤点或空图；
   完成强锦标赛与状态置换确实覆盖每个原始正率阵，零循环流不等于零原率。
3. 全65536家族的完整有向重数判定、全部93三次单项式和4464边际系数恒等式。
   特别检查ABC项的3个1/3权重，以及边边际和完整树分布的区别。
4. rho=c_m x^m/tau和theta=sum rho beta的非负性、归一化及逆置换。普遍量词
   来自解析归约加完整有限恒等式，不能由210个测试实例代替。

科学依据：`research/proof.md`、`research/eulerian-cone-probe.json`、
`audit/science.md`、`audit/science.json`、`audit/referee-abc-check.md`。
所有已接受冻结文件保持原字节。原证明/claim中历史“待审”措辞未追改；后续
接受状态由真正的独立科学审稿记录表达。

## 稿件、复现与来源

- 主稿：`manuscript/main.tex`；BibTeX：`manuscript/references.bib`；
  全部93行证书及16行树表：`manuscript/tables/`；自绘流图：`manuscript/figures/cone.tex`。
- `publication.json`给出实际最终PDF、精确源码清单与本地交接文件清单。
- `supplement/README.md`提供从空输出目录运行两个检查器和从空目录编译稿件的命令。
  标准库即可复核；无安装、下载或GPU要求。
- 便携版本只改路径、输出位置和输出中的作业标签；算法来源、原文件摘要及实际差异
  在 `writing/portability-provenance.json`、`writing/checker-portability.diff`。
  证书数据与已接受原始证书逐字节相同。
- 写作重放通过：cofactor版本5141项检查；Prüfer版本全部93项、346单例和210个
  精确正率实例。实际输出在 `writing/package-replay/`。这是包装后复现，不是
  另一次fresh referee，也不以运行时间作为方法性能结论。
- 中文逐项来源索引 `writing/source-map.md`。四条文献基于实际一手PDF与元数据；
  SciPost出版年2025和所读v2修订年2026明确区分。不捆绑第三方全文或作者代码。

## 期刊与AI使用

选刊考虑：**Journal of Physics A: Mathematical and Theoretical，Paper**。
其官方统计物理范围包括非平衡、随机过程与网络；相邻发表实例已核对题名、
期刊与摘要。见 `venue.json`、`venue/aims-and-policy.md`。分区及独立SCIE核验
状态为 `unverified`，不提供录用、SCI或分区保证。

AI的实际参与不限于语法润色：包括研究思路、解析归约、代码和精确检查程序、
文献比较、内部独立科学审稿、稿件与本交接材料。不同上下文和不同计算表示
有助于查错，但可能共享模型偏差；它们不是外部同行评审或人的科学批准。
稿件致谢如实披露这些用途，没有声称作者已亲自验证全部内容。具体模型版本
尚未确认，不能凭“Astra”、软件名或当前会话身份推定此前所有阶段的实际型号。

IOP官方政策要求模型/版本/用途披露、作者实质审阅和引文确认，并规定作者责任
和工具使用权利条件。因此当前是 `needs_author_judgment`：作者须核对真实执行
记录中的模型版本、亲读并批判性修订推导与文字、确认每条引文、审定这种AI参与
程度和权利条件，然后决定目标期刊。不能将本地科学审稿通过等同政策完全满足。
尚无作者提供的基金或利益冲突声明，稿中没有代填“无基金”或“无利益冲突”。

## 本次release核验与唯一下一步

固定173项主张后逐项核验，四条一手引用、16行树解码表和93行有理证书均已对照。
两个便携检查器实际复跑通过；最终11页PDF实际逐页查看。它们是本地AI核验，
不构成外部同行评审或人类科学批准。详细中文报告见 `audit/citations.md`、
`audit/build.md`、`audit/visual.md`。原科学冻结105项保持原字节。

本研究及写作阶段主要由AI自主执行；本工作流没有人类已完成实质科学审阅的
证据，不能把“assisted”理解为人类已经完成其余研究义务。AI也制作了文献条目。
本次重读IOP政策，其不允许条目包括“Generate reference lists”，同时要求作者
亲自核对所引资料。真实一手核验不能自动证明该研究工作流满足此政策；目前仍为
`needs_author_judgment`。作者须判断AI研究、生成条目和内部核验的实际方式，
补全真实模型版本，并完成实质审阅、修订、署名、基金/利益冲突及权利确认。

唯一下一步骤：外层supervisor重新运行release_gate check，再进行已授权的本地
publish与bundle make/check。之后保持 `draft_ready_author_review_required`，
由作者完成上述判断；没有外部提交授权或执行。
