# 作者移交：局部计数最优性稿件

已准备本地英文稿件 **Certified local optimality of a qubit counting process over a finite mean interval**，拟投 Physical Review A 的 Regular Article。当前已完成 fresh release 的引文、构建和逐页视觉审计，供作者科学核验并等待监督者本地激活；没有提交、发表、外部同行评审或作者批准。

## 核心结论及边界

对每个固定均值 m∈[3,6]，经均值 4 的认证锚点连接的指定平稳支，是所有附近合法 qubit CP 无计数映射及初态中的严格局部方差极小，模共同酉基变换。竞争者包括 Choi 秩 1–4、混合初态和秩二计数效应。它是 computational-paper 范围的计算机辅助结果。原始“所有 m>2 的全局极小可由单 Kraus/秩一探测结构实现”问题仍 unresolved。

新意是连续均值区间上对完整附近 CP/态/效应域的局部充分性认证；数值机制、量子优势和较大 ansatz 对旧两参数族的改善属于既有来源。没有全局下界、数值盆地半径、器件实现、热力学代价或连续时间极限结论。

## 最需要作者核验的部分

1. 正文 Sec. IV 的完整边界图：初态和效应的光滑谱分解、首 Choi 本征向量分解、任意 3×3 Hermitian Q≥0，以及隐式极分解的局部覆盖性。若这一覆盖失败，单独正 Hessian 不足以支持主结论。
2. 输入在前的 Choi 约定和效应乘子正号；Hk=0、状态互补性必须由严格驻点给出，不能由很小的残差替代。固定均值 Hessian 为 Hess(E2−λμ) 的切向限制，已包含均值补偿曲率。
3. Banach 映入/收缩、相邻凸包上的单射拼接、均值 4 锚点，以及全部 8,433 格符号。完整重放的覆盖和数值小数均须与正文比较。
4. T*²(I)<0.999 I 保证无限尾、归一化与有限矩，并在附近全 CP 域开放。步数、物理时间和方差单位不可混用；不存在有限时间截断或事后筛选成功事件。

接受范围和原始独立科学审查保存在 `claim.json`、`audit/science.json`、`audit/science.md`；主证明在 `evidence/choi-continuation-analysis.md`。这些文件和全部冻结科学输入保持原样。逐条稿件来源映射见 `manuscript/SOURCE_MAP.md`。原始第三方 PDF 只保留于本地 literature/，不进入提交包。

## 文件与复现

- 主文 `manuscript/main.tex`，完整书目 `manuscript/references.bib`，数据生成表 `manuscript/values.tex`，PDF `build/main.pdf`。
- `python3 manuscript/build.py` 从空的 build/clean 目录进行 pdflatex / BibTeX / 两次 pdflatex，保存 `build/write-build.log`。需要已有 TeX Live/REVTeX 与标准宏包；构建脚本不安装软件。
- `supplement/README.md` 给出完整离线重放命令，`supplement/requirements.txt` 记录包版本。先 algebra.py，再 cover.py，最后 make_table.py；只有输出目录和显式表格被重写。保持当前冻结版本时，请在副本中重放。
- 写作阶段实际重放 40 项符号恒等、m=3,4,6 的已发表基准，以及全部 8,433 格和相邻拼接。通过的是便携包装复现，不是新的独立审稿。日志在 `evidence/write/packaged-algebra.log`、`evidence/write/packaged-cover.log`，结果在 `supplement/results/`。
- 新包装仅调整接受版 checker 的路径、输出名称、运行元数据和开头说明；数学运算不变。完整 cell/functions 数据保持原字节；锚点保留原三个精确有理字段。追溯见 `evidence/write/package-map.json`。

已验证环境为 Python 3.12.14、SymPy 1.14.0、python-flint 0.9.0、macOS arm64；重放 Arb 精度为 100 位。写作重放符号阶段约 276 秒，区间阶段约 176 秒。没有并行科研 worker、GPU、外部服务计算或安装系统软件。峰值内存、API 成本和精确 token 用量为 unknown。

## 期刊、AI 与作者待决事项

目标期刊范围、文章类型和现行 AI 政策已从官方页面核查，依据见 `venue.json`、`venue/aims-and-policy.md`。主题匹配不等于达到编辑显著性门槛。SCIE/排名与分区未核验，ranking_status=unverified；无录用或分区保证。

实际使用 OpenAI Codex 协助科研推理、推导、代码与调试、文献比较、独立实现重建和写作。单独 AI 科学审查是自动化核验，不是外部同行评审；没有把人类作者的核验虚构为已完成。当前写作助手标识为 Codex / GPT-6；项目配置未提供明确 model 值。不得据此推断全部历史阶段的部署子版本。具体工具版本与各阶段使用记录需作者根据本地原始记录确认。政策要求的人工指导/核验、内容权利与工具条款判断也尚未完成，因此 ai_policy_status=needs_author_judgment。正文方法和致谢已披露实际用途。

供作者最终确认的署名资料为：Xiaojian Zeng；PBC School of Finance, Tsinghua University, 100190；xiaojianzeng@foxmail.com。姓名、单位、邮箱、作者身份、利益冲突、资金支持、许可与公共数据仓库选择均由作者决定；没有自动生成机构背书、资助编号或完成声明。

本次发布审查由 `phys-smallmac00001-p01-release-43b4b0b1af95` 完成：先冻结69项主张，再逐项核对一手原文或已接受证明/独立重放；独立清洁构建后实际查看最终PDF全部5页。正式报告为 `audit/citations.md`、`audit/build.md`、`audit/visual.md`，数值展示和完整文件范围检查在 `evidence/release/`。没有改变科学冻结文件或扩张已接受结论，也没有将本次发布核查称作又一次全量独立科学重放。

后续操作由监督者运行 `release_gate.py publish` 进行本地激活，再运行 `bundle.py make` 和 `bundle.py check`。本地激活的状态只能为 `draft_ready_author_review_required`。预览压缩包若存在，仅供检查文件范围；它不是已激活的正式归档。正式 bundle 在激活前尚不存在，提前执行 check 的缺文件状态不是科学失败，也不是打包通过。

之后仍须人类作者实际审阅并批准，补全历史工具版本、人工指导和验证说明，以及期刊/工具条款和内容权利判断。期刊编辑的显著性判断、排名、公开许可与公共仓库选择均未被自动代决。本任务没有外部上传、提交、账号修改或系统软件安装。
