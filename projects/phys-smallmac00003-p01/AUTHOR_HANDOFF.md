# 作者交接：双 qutrit APPT 的最大纯度

已整理本地英文稿 *Maximum purity of absolutely PPT states of two qutrits*。
稿件主文件 `manuscript/main.tex`，编译目标 `build/clean/main.pdf`。
这是已完成本次引用、清洁构建和逐页视觉核查，仍待作者科学审阅的本地草稿；没有对外提交、上传或宣称期刊接受。

核心结果：所有 C³⊗C³ APPT 密度算符的最大纯度为17/121，唯一有序等号谱为
(3,1,1,1,1,1,1,1,1)/11。它给出不可下调的纯度充分阈值：P>17/121 时，存在
某个全局 U(9) 将态变为NPT；APPT集合围绕I₉/9的最大HS距离为4√2/33。
这是当前科学审稿已经接受的完整原题范围，不是向一般3×n外推的结果。

最难的检查有三处。第一，三条切面须真由完整Hildebrand条件推出，且使用
K⊆Q的外包方向；达到性仍需两张LMI。第二，49个顶点必须完备：正间隙支持维数
论证把每个顶点包含在495个活跃基中，退化基不漏点；严格凸性再给唯一等号。
第三，新意须与已知达到谱和内接多面体下界区分。本稿仅解决AKW预印本
Conjecture 6.7 的3×3实例，并如实引用Tran的25/169旧上界。

证据索引在 `manuscript/SOURCE_MAP.md`。全体49行有理顶点已放入PDF附录；
`supplement/README.md` 给出两种精确算法及清洁编译命令，使用Python标准库即可
复算，无需优化器、联网或软件安装。投稿版程序的全部谱、纯度和松弛量已与冻结
证书及已接受的独立裁切结果比较一致；日志在 `evidence/write/reproduction.log`。
写作及本次release只处理稿件、程序包装和发布核查，原始科学证据和接受记录保持不变。

完整构建过程保存为 `build/clean-build.log`；其中首轮出现待BibTeX和重编译解决的
引用提示属于实际构建历史。最终轮次编译日志是 `build/clean/main.log`，供发布审查
核对最终引用/标签状态；不能把首轮提示误报为最终未定义引用，也不能删除原始日志。
最终保留一条REVTeX/nameref的label兼容性提示；实际页码、公式和引用呈现正常，
未对该提示作静默过滤。

文献限制仍保留：Song–Chen出版全文与v1的完整差异未核对；Wang等全部分类表及
AKW其余几何证明没有逐式重验。稿中所有具体公式/定理编号明确属于已核对的
arXiv版本。没有把APPT等同绝对可分，没有声称NPT可蒸馏，也没有将有限精确算术
说成形式证明助手认证。

拟投定位为 Physical Review A 的 Regular Article。当前范围、文章类型、邻近
论文和AI政策来源见 `venue/aims-and-policy.md`。该定位不是录用保证；SCIE索引
和任何JCR/CAS/SJR分区未验证，不作等级承诺。AI政策状态保持
`needs_author_judgment`。

作者待决事项：

- 确认草稿所列 Xiaojian Zeng、PBC School of Finance, Tsinghua University, 100190、
  xiaojianzeng@foxmail.com，以及作者资格、顺序和是否需要其他贡献者。
- 亲自审阅完整域量词、三条切面、顶点完备性、两个精确程序和文献定位，并判断
  能否承担全部科学责任。当前AI科学审查不替代人类同行评议或作者核验。
- 核对实际AI部署版本及研究指挥记录。正文如实披露OpenAI Codex参与文献搜索、
  选择向量、推导、代码和执行、内部检查及写作；没有声称作者已经核验。
  本次分配的 role.json 不含精确部署版本，因此未捏造模型版本/CLI版本。
  APS要求工具/版本、用途和作者如何指导/验证，须由作者补全真实事实。
- 按现行APS政策核对AI工具使用条款、权利、隐私和全部实质性披露。
  若不能满足人类作者的专业判断和责任要求，不应提交。
- 确认期刊选择、资金/利益冲突声明、数据公开方式和最终投稿附件。
  尚未取得的人工作者同意、经费、利益冲突或公开数据DOI均未编造。

`publication.json` 明确列出可交接文件，只包括自写TeX/Bib、代码、数学数据和
说明。实际范围核对见 `evidence/write/redistribution-scope.md`；第三方全文PDF、
截图、网页完整记录和私人任务日志均不进入投稿文件列表。这是文件范围检查，
不等于替作者作出版权或AI条款法律判断。

下一步：监督器在release返回ready且门禁复检通过后，执行本地publish，再执行bundle.py make/check。作者科学/政策审阅仍须随后完成。任何科学性改动均需重新科学审查；任何稿件改动均需重新冻结和受影响的发布审查。

本次release作业phys-smallmac00003-p01-release-ad9ca707e123：固定107条主张后逐项核查一手文献和接受证明；两个补充程序复得全部49顶点并与接受的独立复算逐项一致。重新清洁编译四命令均成功，实际查看最终六页，正文TeX/Bib/表格无须修改。详细中文报告audit/citations.md、audit/build.md、audit/visual.md仅在本地审计档案；可移交包不自动包含内部审计和第三方来源全文。

出版全文与v1差异仍待核查。APS政策的精确AI版本、作者指导核验和权利责任尚待本人完成；FAQ还规定其他值得披露的用途应放于Acknowledgment，定稿时请按实际用途补充并重新检查。当前只准备draft_ready_author_review_required状态的本地交接，不代表投稿条件已全部满足。
