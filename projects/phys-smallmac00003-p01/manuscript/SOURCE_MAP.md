# 稿件来源与接受范围映射

此文件是写作交接依据，不是新的引用审计或科学接受记录。
Bib数据库中apsrev42Control只是apsrev4-2的题名显示控制项，不是第七篇文献。
nocite{*}用于加载该控制项；六篇实质文献均已经在正文逐一引用。
稿件：`manuscript/main.tex`、`manuscript/references.bib`、`manuscript/vertices.tex`。
科学依据：当前已接受的 `audit/science.json`、`audit/science.md`，绑定
`audit/snapshot.json` 中的92个文件；科学输入在写作中没有修改。

| 编号/稿件位置 | 主张及类型 | 实际一手定位或接受证据 | 明确保留项 |
|---|---|---|---|
| W01，§I–II、Eq. L1/L2 | 已知谱判据、两张完整LMI | Hildebrand, quant-ph/0502170v1 第2页 Lemmas 1、3，第4页 Theorem 1，第6页 Eq.(5)、Corollary 4；`literature/hildebrand-0502170v1.pdf/.txt` | Bib引用出版题名和DOI，但编号明确只归v1；不把本稿必要切面当充分判据。 |
| W02，§I | 已知达到谱及极点判据 | Song–Chen, 2409.14347v1 第6页 Theorem 15、Corollary 16 Eq.(10)；`literature/song-chen-2409.14347v1.pdf/.txt` | 达到谱不是新构造。出版全文差异仍 `journal_fulltext_difference_pending`；本次仅查出版元数据和摘要。 |
| W03，§I | 恰好三种不同本征值的极点分类范围 | Wang–Chen–Song, 2603.20717v1 引言及 §VII Conclusions；`audit/referee-cf42853670ee/novelty-review.md`、其 `web-classification.json` 与 `web-locators.json`；本次作者/题名/版本见 `venue/policy-primary-20260912.json` | 不声称逐式复算48页分类表，也不据一次关键词未命中断言新意。 |
| W04，§I | 0.1405 是既有数值估计 | Dung–Khoi, 2510.19508v1 §3.3 Table 2 的3×3行及 fmincon说明；`evidence/research-web-novelty.txt`、`audit/referee-cf42853670ee/novelty-review.md` | 原论文题名涉及绝对可分，本稿只引用其明确标为APPT的数值行；不把数值提升为证明。 |
| W05，§I、IV、VI | 已证上界25/169及其三维未决范围 | Tran, 2608.09832v1 第2页 Theorem 1、Remark 1.1；§2 Theorem 2.2 的总维数9放松；`literature/tran-2608.09832v1.pdf/.txt`、本次 `evidence/write/policy-metadata.json` | 是改善已知上界，不是对该上界给反例。 |
| W06，§I、IV、VI | 最近猜想及本稿解决的3×3特例 | Ahiable–Kothakonda–Winter, 2608.03390v1 §6.1 Theorem 6.3 Eq.(34)、Conjecture 6.7 和随后SLSQP段；`evidence/research-web-primary-sections.txt`、`evidence/write/policy-metadata.json` | Eq.(34)只优化内接多面体；全部几何证明未逐式重验；一般维数猜想没有被本稿解决。 |
| W07，Theorem 1、§III–V、附录 | 新的完整域锐上界、唯一等号及计算辅助证明 | `evidence/research-proof.md` §§1–3；`evidence/outer-exact-certificate.json`、`evidence/outer-independent-replay.json`；独立接受证据 `audit/referee-cf42853670ee/source-review.md`、`replay-results.json`、`replay.log` | 新结果依据证明和独立复算，不虚构外部引用支持。无形式证明助手/人类同行评审完成声明。 |
| W08，§IV、Tables I–II | 495基、72奇异、63可行、49顶点、分组、次大5/36及差7/4356 | 同W07的精确证书；当前 `supplement/verify_vertices.py`、`supplement/vertices.json`；`evidence/write/reproduction.log`、`repackaging-check.json` | 表格为同一集合的重新排序，平手行次序可不同；不是新实验或新科学候选。 |
| W09，§IV | 裁切15→31→49及25/169→1/7→17/121 | 已接受独立 `audit/referee-cf42853670ee/replay.py` 和 `replay-results.json`；投稿改装版 `supplement/verify_clipping.py`；当前复跑与原结果一致 | 改装只变输出路径、描述性元数据；当前重跑不冒称新的独立科学审稿。 |
| W10，§V | NPT可达性的最优纯度充分阈值与HS半径4√2/33 | 已接受 `evidence/research-proof.md` §3、`audit/science.md`，稿件 Eq. NPT、radius 的直接推导 | 不证明可蒸馏性、APPT=绝对可分或低于阈值者必APPT。 |
| W11，§IV.C | 实质性AI研究/写作披露及未完成人工审阅 | 本项目真实工作流、当前写作记录；`venue.json`、`venue/aims-and-policy.md` | 工具部署版本和作者实际审阅/指导仍待确认，政策状态为 needs_author_judgment。 |

上述文献检查是有界核对，不能表达为穷尽查重。最终逐条引用及实际PDF引用呈现
仍须由新鲜release角色核验；此索引不代替其固定编号抽取与原文验证。

本索引中的audit/evidence/literature路径指向完整本地研究档案；可移交的论文
来源包不附带这些第三方全文或内部日志。正文、完整表格和两个复算程序可独立使用。
