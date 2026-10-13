# 作者接手说明

稿件 **Four nested limit cycles in a planar power-law reaction system**
保持已接受的完整存在性命题：原无量纲幂律系统的唯一正平衡双曲稳定，
同时有至少四条嵌套双曲周期轨道，由内向外排斥、吸引、排斥、吸引。
它说明该模型能同时容纳稳定静息态和两个稳定振荡。
本地科学接受不是外部同行评审，尚没有真实作者完成科学复核的记录。

## 文件与重放

- 正文与文献：`manuscript/main.tex`、`manuscript/references.bib`。
- PDF 路径与完整依赖：以 `publication.json` 的 `pdf` 和 `source_files` 为准。
- 补充材料：`supplement/README.md`、`supplement/ENVIRONMENT.md`、两套代码、精确
  输入和参考端点。严格重放只需 Python 3.9+ 标准库，无需安装软件。
- 接受证明：`evidence/research/proof.md`；独立检查：`audit/science.md`、
  `audit/independent_certificate.py`、`audit/replay.log`。
- 稿件逐项来源：`evidence/write/manuscript-source-map.md`；两套代码副本的字节对应
  在 `evidence/write/supplement-copy-map.json`。

在项目根目录执行（输出目录必须为空或不存在）：

```sh
python3 -S supplement/replay.py --output build/author-replay-1
python3 manuscript/build.py --output build/author-clean-1
```

程序只在新输出树重放，不改接受包。当前写作轮已成功重放两套证书：
`build/certificate-replay/replay-summary.json` 中每个科学字段与参考输出一致。
运行时间和平台字段不要求相同。若断言、目录或时间限制失败，不能解释为通过。

## 最需要作者理解的检查

1. 核对第 3 节的复正规形规范、原时间与来源焦点值的正因子；完整九阶递推
   与附录的实标量递推是不同算法。独立算法仍由另一 AI 会话生成，不等于独立人类复核。
2. 检查固定有理中心的区间压缩、第四系数负号和全部分母非零。
   表中小数只是严格外包；精确整数/十进制端点可重放。
3. 检查第 5 节满秩的参数顺序及 Schur 补；改变 a,b,d 包括改变反应级数/向量，
   不能当作固定网络只改变速率。
4. 检查第 6 节参数依赖和统一 C1 余项：四个简单回返根来自原解析方程，
   不是九阶截断模型。没有给显式 epsilon、有限振幅参数、周期或全局最大环数。

原文 notebook 未取得，其内容仍未知；正文限定贡献到该具体族，未宣称一般多环共存
首次发现或穷尽优先权。Craciun–Erban 的其他多环模型在引言明确引用。
原题和 67 个冻结科学文件均应保持不变；新的科学修改必须回到新的独立审查。

## 目标期刊与真实作者决定

拟定 **Journal of Dynamics and Differential Equations / OriginalPaper**，
官方范围与原文同刊先例见 `venue/aims-and-policy.md`。出版方当前首页列 SCIE，
但未独立查询 Clarivate；JCR/CAS/SJR 年度分区未核查，不报告分区保证。

**AI 政策适配未通过自动确认：needs_author_judgment。** 当前政策对无人监督的
核心学术生成有限制。本项目实质性 AI 推导、代码、自动审查和写作均已披露；
这些不能代替人的学术判断，事后签名也不被假定足够。真实作者须理解并核验结果，
决定可承担的贡献/责任，并判断目标期刊政策是否容纳实际过程；有疑义时应由作者
决定是否咨询编辑。本轮没有联系任何人。

待真实确认的作者资料：Xiaojian Zeng；PBC School of Finance, Tsinghua University,
100190；xiaojianzeng@foxmail.com。没有自动声称机构背书。作者贡献、资助、利益冲突、
ORCID（若有）、AI 工具准确版本和最终批准均待作者确认；没有编造“无资助/无冲突”声明。
代码公开许可证和可能的外部数据仓库也由作者决定。

## 本轮发布审计与后续激活

2026-09-12，fresh release 作业 phys-smallmac00006-p04-release-8a737b5fcecf
完成四篇文献的出版方全文定位、两套证书的新目录重放、实际 TeX 数值的 33 项
精确转录检查、四步干净编译，以及最新 PDF 全部 9 页的实际图像检查。
固定的 70 项主张清单、逐项核查和三份审计报告位于 `audit/release-evidence/`
以及 `audit/citations.md`、`audit/build.md`、`audit/visual.md`。

本说明引用的 `audit/`、`evidence/` 和 `build/` 审查资料属于本地档案，
不随明确列出的待移交材料自动分发。完整存在性证明在正文，有限证书的可重放
材料在 `supplement/`；仅持有最终压缩包也不需要下载本地审查档案来重放证书。

监督进程仍须执行 `release_gate.py check`、`release_gate.py publish`、
`bundle.py make` 及 `bundle.py check`，才会激活本地 `release/main.pdf` 和
`release/submission.zip`。本发布审计作业不调用 publish，也不对外提交。
所有本地交付均为 `draft_ready_author_review_required`。期刊政策适配、真实作者
科学复核和上述个人声明继续待办，审计通过不等于已经可以投稿。
