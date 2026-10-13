# 作者交接：图态凝聚的固定标签反例

本地两页PRA Comment草稿已完成本次fresh release的引用、清洁构建与逐页视觉审计，供作者本人审阅。
当前报告为audit/citations.md、audit/build.md、audit/visual.md；45条固定论断逐项核对记录在audit/release-9affe250d2c0。
最终结构门结果见该目录的check-final.json；本地激活与最终ZIP由supervisor在ready后执行。
未投稿、未上传，未取得编辑接受或人类作者批准。当前范围是resolution-paper，
原冻结全称命题为disproved；这仅指允许C不连通的固定标签双端版本。

核心证书：E={13,16,24,35,46}，E′={13,15,24,36,46,56}，C={1,2,3}。
三步LC(3,1,5)连接两张六点连通图，两端C内各点外度均为1。
凝聚后B={4,5}的边缘态分别为I/4与(I+X4 tensor X5)/4，秩4与2、熵2与1 bit。
正文给出完整输入、三步当前邻域及边变化、两端矩阵、偏迹和不等价证明。
这是有限理想图态中的精确结果，没有微扰/截断误差或实验发现主张。

必须核查的科学环节：出版稿Conjecture 1及其标签语境；OR而非模2邻接；LC每一步使用当前邻域；单比特Clifford的旋转符号与全局相位；两个凝聚态始终在同一外部子系统比较。来源位置及当前接受证据见manuscript-source-map.md。

范围限制：C由{1,3}和{2}组成，不连通；中间图允许暂时违反外度条件；交换外部标签5与6后两输出LC等价。该例不否定无标签或连通C修正版，不证明最小性、最短LC词、新复杂度或新纠缠类。已证秩一和foliage凝聚规则不受影响。文献比较是有界的，最终优先权检查仍应由作者完成。

当前科学审稿为audit/science.json及science.md，任务末尾0f50c3c6c5f1。
稿件、复现说明及公开代码已改为对应这份接受报告；不沿用旧审稿程序来声称当前验收。
补充材料中的referee_replay.py是当前独立程序的原样副本。写作阶段实际运行了它和两套发现阶段程序，全部精确断言通过。独立实现共享待审边集与物理定义；由另一个AI上下文生成不等于外部同行评审，也不能排除相关错误。重放不是新的科学验收。

复现入口：supplement/README.md；实际环境和计算规模在supplement/environment.json。
程序只写新的build目录，不修改冻结科学证据。当前稿件PDF为build/release-9affe250d2c0/main.pdf，
两页，本次release亦独立重新渲染并实际查看两页。最终日志没有未定义引用、未定义交叉引用或overfull/underfull框。
nameref对label定义的兼容性提示及APS BibTeX的jnrlst控制警告仍在原日志中，均已记录，
没有通过隐藏告警制造零警告报告。本次release再次保留并评估了这两条非致命警告，没有屏蔽；最终14条方程标号和2条文献均已解析。

拟投Physical Review A / Comment；量子信息范围、同刊评论类型及3500词上限已核官网。
最新独立复核见venue/release-9affe250d2c0-policy.md。没有验证SCIE具体记录、JCR/CAS/SJR分区或期刊录用机会。
请作者确认编辑价值、正式字数、补充材料引用和最终存储方式。

AI实际参与：OpenAI Codex实质参与候选搜索、推导、代码生成、文献比较、自动交叉核对和写作。
主文方法段保留这些用途披露，不以AI声明作为科学证明，也不说作者已经验证。
当前写作运行时的说明为GPT-6；本地证据不足以给出各阶段全部精确model build/version，
不得补造。提交前应补全可验证版本记录、实际作者指导过程和亲自完成的核验说明，
并判断当前APS政策、工具条款、机构权利及代码许可证。ai_policy_status保留needs_author_judgment。
若这些要求无法满足，不应把本地ready状态理解为允许提交。

本稿署名依据本次用户明确资料：Xiaojian Zeng；PBC School of Finance, Tsinghua University,
100190, China；xiaojianzeng@foxmail.com。姓名、署名顺序、单位和联系方式仍待本人最终确认。
稿件日期采用本工作UTC日期September 12, 2026，待最终定稿时确认。没有自动增加共同作者、
资助、机构背书或自引，也未声称人类已批准。

publication.json的submission_files为逐文件白名单：自产TeX/Bib、构建与复现脚本、输入、说明、
来源定位和本交接；不含第三方整篇论文、浏览器捕获或私有审稿日志。旧Fig.15只以明确归属的
边集数据用于核对，没有复制原图。redistribution_checked表示已检查这份清单的内容和范围，
不代替作者对所有权、AI条款及最终公开许可的判断。旧稿件和旧稿件快照完整保存在
manuscript-history/pre-write-c6b53d7ee525；原source.md及60个科学冻结文件保持不变。

唯一下一测试：supervisor执行release_gate.py publish，再执行bundle.py make与bundle.py check，核对被激活PDF和归档内容；本release不调用publish。作者仍须亲自审查科学证书、优先权与AI披露，补全可验证模型版本/作者指导核验说明及补充材料引用。作者批准pending，禁止把本地ready当作提交许可。

来源核查：原论文p052449-6的平方关系rho_M^2=(2^{d_M}/2^{|M|})rho_M已在放大原图中确认，与本稿Eq.(11)等价。PDF文本抽取可能串接相邻指数，作者核对时宜以原图及明确的归一化群和计算为准。
