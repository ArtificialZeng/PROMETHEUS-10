# 作者交接：三份未知 qubit 的普适提纯上界

本地稿件已完成本轮引用、洁净构建及逐页视觉核查，准备供作者审阅，**尚未投稿，尚无人类作者科学批准**。题名为 *Three-copy universal qubit purification under complete stabilizer preservation*。拟署名 Xiaojian Zeng；PBC School of Finance, Tsinghua University, Beijing 100190, China；xiaojianzeng@foxmail.com。请作者最终核实名字、机构、地址、贡献资格、利益关系及资助信息；本轮未替作者作任何机构声明或签署。

核心结论：同一 Haar 未知纯 qubit 的三份独立局部退极化输入，在 CP/TNI 且完全稳定子正锥保持的成功支路类内，对所有 `0<delta<1`、`0<s<=1`，成功概率加权的条件平均保真度最优值是 `1-delta/2`。舍弃两份并随机接受达到该值。结论覆盖原三份问题，没有解决任意份数猜想。

最需要作者亲自检查的三处是：输入偏转置和Choi归一化；纯稳定子态最多三个非零交换星形关联；精确见证 `H(t)=t(1-t^2)(B-3I)/48-t^3 P/5` 中的端点正性与真实成功分母。正文与 `research/proof.md` 给出论证；`writing/source-map.md` 索引接受证据。独立审稿是本地AI复核，不能代替人类同行评议。

原接受的科学文件保持不变。写作期另在 `writing/reproduction-run/` 完整顺序执行了七个复现脚本，全部成功；重放得到36720射线、36系数类、180恒零项，并核对全部256个见证矩阵元和仿射相位表示。最大矩阵16×16，精确有理数/高斯整数；未测峰值内存，无随机误差或连续极限估计。导出代码只改输出路径和描述元数据，变换见 `supplement/code-provenance.json`。

三篇参考文献各有明确用途，来源定位见 `writing/source-map.md`。PRL正式正文与补充材料尚未取得，不能宣称已与预印本完全比较，也不能无条件宣布全球首次证明。稿件保留这一限制。作者应在任何投稿前核对该出版版本和后续更新，决定贡献定位是否仍成立；如果发现科学范围改变，须重新审查。

暂定目标为 **Physical Review A，Regular Article**；主题/类型与官方页面核对，证据见 `venue/aims-and-policy.md`。不宣称编辑接受、SCI分区或已核实SCIE。当前APS政策要求实质AI用途、工具版本及作者指导/核查方式的披露。此稿的AI参与包括研究推导、代码、来源比较、复核和撰写，已在方法相关段落说明，未伪装成单纯润色。早期会话的全部模型版本在本輪所用材料中不可确认，作者需根据真实记录补足或与编辑明确说明；不可编造。工具条款/隐私适配和作者承担责任均待本人判断。

再生成计算和PDF的方法见 `supplement/README.md`。代码只在新的本地目录顺序运行，不联网，不安装软件，也不改写接受的记录。显式交接文件清单在 `publication.json` 的 `submission_files`；第三方全文、浏览器来源对话、作业转录、账户信息及完整审计日志不在清单中。`writing/redistribution-review.md` 记录了实际范围核对，这不是对AI内容版权或作者授权的法律认定。

本轮RELEASE作业phys-smallmac00005-p01-release-fb20d8f962b2固定并核对48项声明，查验三条文献归因与来源版本，在新目录构建4页PDF并实际查看所有页面。最终受审PDF为build/release-fb20d8f962b2/main.pdf。7个附件脚本在另一隔离目录顺序复跑，完整算符与射线数据和冻结证据一致；这不是新的独立科学审稿。发布报告为audit/citations.md、audit/build.md、audit/visual.md；本轮政策核对见venue/release-policy.md。

监督器在收到ready且最终门禁通过后，才执行本地publish及bundle make/check；本作业没有激活发布清单或外部上传。正式bundle检查在激活前没有对应的release/bundle.json，不能伪报成功。随后仍需作者科学审阅、核对正式PRL正文及后续版本、补足模型版本与声明，并决定是否投稿。任何外部提交均未执行。
