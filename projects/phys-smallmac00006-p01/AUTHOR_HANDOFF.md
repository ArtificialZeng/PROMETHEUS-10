# 作者交接：有限 Glauber 退火活动率反例

这是四页本地英文草稿，作者实际科学审阅与批准仍待完成。发布审计记录在完整本地项目的 audit/citations.md、audit/build.md、audit/visual.md。请以 publication.json 指定的清洁重建 PDF 为本次审计对象；主管随后执行本地 publish 和 bundle make/check，才生成 release/main.pdf 和 release/submission.zip。没有对外投稿或宣称外部同行评审。

## 核心结论

11 个微观态构成 4 正则连通简单图：A 有 3 态，B、C 各 4 态；完整 A–B、B–C 配对、C 内 K4。固定 E/epsilon=(0×3,1×4,64×4)，beta_k epsilon=log q_k，q=(10001/10000,33/32,64)，精确 Gibbs 初态，两次严格降温。

第二步活动 A1>63/125，两步均值>251/500。每个能量独立扰动至多 epsilon/1000、温度不变并重新定义 Gibbs 初态，仍有 A1>1003737/2000000、均值>8014821/16000000，两者均超过 1/2。原一般正则图全称命题被否定；不是新粒子或实验发现。

## 最难核查的环节

1. 每步用步前分布和下一浴温的列随机矩阵；初态是真正 Gibbs 态，过程中不重新平衡。
2. C 内等能跳跃必须计入微观活动，即使其层净流为零；图中的柱高是单态概率，不是层总概率。
3. 表 I 的端点是精确有理包围。附录 Python 代码可以独立验证所有端点；完整矩阵、同步边流和 704 条事件历史都在隔离重放中相等。
4. 扰动结论覆盖整个 11 维连续实参数盒，来自完整矩阵范数与 Gibbs 比值的解析界，不是抽样、角点检查或一阶近似。

## 范围和来源

一手近邻按明确版本引用：Luo 详细文 arXiv:2311.10424v1 pp.5–6 式(30)–(33)、(38)–(41)，Letter arXiv:2311.10422v1 p.4，Burovski arXiv:1907.06776v2 Appendix, subsection B 式(24)。主要来源定位已在本交接和 reproducibility/README.md 中列出；完整内部映射 MANUSCRIPT_SOURCE_MAP.md 仅在本地科研档案中，未加入投稿白名单。

不声称 SK-only、单自旋翻转超立方体或慢冷却子类失败；不从中间活动界失败推断最终性能公式失败；不声称最小态数、最大越界量或全球首次。最终期刊 PDF 的逐式比对、完整后继及勘误检索仍待作者核对。已接受科学文件保持不变，不以写作构建替代新鲜科学审核。

## 期刊、AI 与待决事项

暂定 Physical Review E 的 Regular Article，现行范围、形式和 AI 政策在完整本地档案的 venue/aims-and-policy.md 与 venue/release-policy-check.md 中；公开依据为 https://journals.aps.org/pre/authors 和 https://journals.aps.org/authors/appropriate-use-ai-tools 。这些内部审计档案未加入投稿白名单。是否更适合 Comment、编辑新颖性/意义判断及期刊政策合规由作者确认；排名与 SCIE 未验证，不作分区承诺。

AI 实质性参与题目建议、构造和推导、代码、资料比较、核查、图代码及正文写作。当前正文/图代码阶段的环境自报 GPT-6；更早阶段的精确模型版本未从提供的元数据恢复，文稿已明确说明。请恢复所能确认的版本，核对条款与权利，并在本人实际审阅后准确描述本人如何指导和验证。不能将 AI 审查称为本人已经验证。

草稿作者信息沿用给定资料：Xiaojian Zeng；PBC School of Finance, Tsinghua University, 100190；xiaojianzeng@foxmail.com。署名、单位、邮箱、作者贡献、完整利益冲突/资助情况、最终披露、数据公开地点及许可证都需本人确认，现稿不代表机构背书。未写入虚构资助或无利益冲突声明。

## 文件和重放

manuscript/main.tex、references.bib、table-rows.tex 和 figures/occupations.pdf 构成排版源；附录实际载入 reproducibility/scalar_certificate.py。reproducibility/README.md 提供完整重放和清洁构建命令、依赖及预期结果。publication.json 的 submission_files 是显式白名单，仅包括自制稿源、图、代码、科学输入/输出和本交接，不包含第三方全文、浏览器捕获、账户资料或私有任务日志。它是未来本地交接的清单；本阶段不制作或提交外部投稿。

唯一下一检验：主管通过 release_gate.py check 后执行本地 publish，再运行 bundle.py make 和 check；作者随后实际复核科学内容、文献优先权、署名及现行期刊/AI政策。现行 APS 要求作者确认工具条款及隐私设置，本任务没有读取账户或更改设置，尚不能声明投稿政策已完全满足。
