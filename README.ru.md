# PROMETHEUS-10

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

Проверяемый архив исследований по физике с помощью ИИ. **Сохранены 93 PDF; проиндексированы 90 канонических исследовательских записей.** Три ранних результата, охваченных более общими или сильными утверждениями, сохранены как связанные исторические версии без двойного счёта. «10» — название исходной коллекции.

Это исследовательские черновики, требующие человеческой проверки науки, приоритета и авторства. Доказательства и опровержения относятся только к точной области зафиксированного утверждения. Частичные и вычислительные результаты не означают полного решения исходной задачи. Независимые контексты ИИ — внутренние проверки, а не внешнее рецензирование или принятие журналом. Исторический пробел проверки привязки рукописи о boundariness сохраняется.

Научные утверждения и названия сохраняют язык источника. Навигация, статус, инструкции и исходные десять описаний локализованы; математический смысл цитируемых утверждений не меняется.

[Полный каталог с поиском](catalog.html) · [Семантическое сравнение и удаление дублей](SEMANTIC_DEDUPLICATION.md) · [Руководство по воспроизведению](reproducibility/README.md)

## Четыре категории результатов

| | Канонические записи |
|---|---:|
| [Доказательство](categories/proofs/README.ru.md) | **32** |
| [Опровержение](categories/disproofs/README.ru.md) | **18** |
| [Частичный результат](categories/partial-results/README.ru.md) | **38** |
| [Вычислительный результат](categories/computational-papers/README.ru.md) | **2** |

Контролируемый процесс проверяет первоисточники, независимо восстанавливает уравнения, воспроизводит опубликованный эталон и передаёт ограниченный результат свежей внутренней проверке перед написанием и выпуском. Короткие пакеты доказательств и общие инструменты уменьшают повторы. Кэш — часть входа; неизмеренная экономия токенов или вероятность успеха не заявляется.

## Доказательство

<details>
<summary><strong>phys-00002-p02 · Four qubit measurements: the exact compatibility threshold</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Шумные квантовые измерения иногда реализуются как маргинальные измерения одного общего измерения. Где проходит порог шума? |
| **Результат и охват исходной задачи** | Рукопись доказывает порог 1/D для четырёх строго упорядоченных плоских несмещённых бинарных измерений кубита с общей видимостью. |
| **Предлагаемый вклад** | Совпадающие конструктивная и двойственная оценки дают аналитический порог; проверки SOCP/SDP подтверждают формулу. |
| **Ограничения** | Результат ограничен указанной геометрией четырёх измерений и моделью шума; это не теорема для произвольных POVM или любого числа измерений. |
| **PDF и исходники** | [PDF](projects/phys-00002-p02/paper.pdf) · [TeX](projects/phys-00002-p02/manuscript/main.tex) · [Bib](projects/phys-00002-p02/manuscript/references.bib) · [Код / данные](projects/phys-00002-p02) · `python reproducibility/reproduce.py --project phys-00002-p02` |

> Novelty reassessment remains required because a later primary answer arXiv:2609.38836v1, dated 30 September 2026, was recorded. Preserve the historical proof and source; do not relabel it as a newly open or priority-established result.

</details>

<details>
<summary><strong>phys-00002-p15 · Critical resetting erases coherence—at a controlled rate</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Случайный сброс меняет долговременную квантовую динамику. Критический показатель Сибуи разделяет качественно различные режимы процесса восстановления. |
| **Результат и охват исходной задачи** | Для alpha=1 и фиксированного конечномерного унитарного регистра рукопись доказывает сходимость в следовой норме к спектральному пинчингу со скоростями при фиксированных спектральных зазорах. |
| **Предлагаемый вклад** | Асимптотическая теорема для критического случая связывает коэффициенты процесса восстановления с затуханием внедиагональной квантовой когерентности. |
| **Ограничения** | Фиксированы размерность и спектральные зазоры; не доказаны равномерные утверждения при закрывающемся зазоре, в термодинамическом пределе или для произвольных правил сброса. |
| **PDF и исходники** | [PDF](projects/phys-00002-p15/paper.pdf) · [TeX](projects/phys-00002-p15/manuscript/main.tex) · [Bib](projects/phys-00002-p15/manuscript/references.bib) · [Код / данные](projects/phys-00002-p15) · `python reproducibility/reproduce.py --project phys-00002-p15` |

</details>

<details>
<summary><strong>phys-00003-p01 · Can torque lower the noise of a Gaussian particle?</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Неравновесное воздействие меняет флуктуации токов. Сравнение с той же равновесной ловушкой проверяет возможность подавления шума. |
| **Результат и охват исходной задачи** | Для устойчивой недодемпфированной модели Орнштейна–Уленбека с вращающим моментом и нулевым магнитным полем шум позиционных токов степени один и три ограничен снизу соответствующим равновесным значением. |
| **Предлагаемый вклад** | Точные полиномиальные вычисления и независимые расчёты по формулам Вика и уравнению Пуассона выделяют неотрицательный избыток шума и случаи равенства для градиентных граничных токов. |
| **Ограничения** | Ограничены динамика и класс полиномиальных токов; нелинейные силы, магнитные поля и более высокие степени находятся вне теоремы. |
| **PDF и исходники** | [PDF](projects/phys-00003-p01/paper.pdf) · [TeX](projects/phys-00003-p01/manuscript/main.tex) · [Bib](projects/phys-00003-p01/manuscript/references.bib) · [Код / данные](projects/phys-00003-p01) · `python reproducibility/reproduce.py --project phys-00003-p01` |

</details>

<details>
<summary><strong>phys-00004-p01 · Two noisy quantum batteries: can joint inputs help?</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Корреляции могут влиять на извлечение работы из квантовых батарей. Обобщённое амплитудное затухание моделирует канал релаксации при конечной температуре. |
| **Результат и охват исходной задачи** | Рукопись доказывает W2(e)=2W1(e) для указанной задачи с двумя использованиями и ограничением энергии, включая комплексные входные состояния и извлечение работы глобальным унитарным преобразованием. |
| **Предлагаемый вклад** | Сведение фаз и точный сертификат полиномиальной положительности завершают оптимизацию двух использований в этой модели. |
| **Ограничения** | Нет утверждения для произвольных семейств каналов, любого числа использований или иных операционных определений работы. |
| **PDF и исходники** | [PDF](projects/phys-00004-p01/paper.pdf) · [TeX](projects/phys-00004-p01/manuscript/main.tex) · [Bib](projects/phys-00004-p01/manuscript/references.bib) · [Код / данные](projects/phys-00004-p01) · `python reproducibility/reproduce.py --project phys-00004-p01` |

</details>

<details>
<summary><strong>phys-smallmac00002-p01 · Absence of reflection-symmetric two-periodic boundary laws in the competing three-state SOS model</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 竞争 SOS 树模型：是否严格不存在反射对称二周期 Gibbs 相？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For all t,h,u>0, f(f(u))=u implies f(u)=u, with f(u)=(u^2+4thu+2t^2(h^2+1))/(t^2u^2+2th(t^2+1)u+t^4+2t^2h^2+1). Equivalently the positive reflection-symmetric level-message update has no nonfixed two-cycle. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00002-p01/paper.pdf) · [TeX](projects/phys-smallmac00002-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00002-p01) · [Author handoff](projects/phys-smallmac00002-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00002-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00003-p01 · Maximum purity of absolutely PPT states of two qutrits</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 双qutrit绝对PPT态：最大纯度是否恰为 \(17/121\)？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every density operator rho on C^3 tensor C^3 that remains PPT under every global U in U(9), Tr(rho^2)<=17/121. Equality holds if and only if its decreasingly ordered spectrum is (3,1,1,1,1,1,1,1,1)/11. Equivalently, this is the exact maximum over all nonnegative ordered trace-one nine-spectra satisfying BOTH source LMIs. The proposed proof uses exact exhaustive vertices of a three-cut outer polytope, analytic completeness and strict convexity, and both-LMI attainment. This is a proof candidate awaiting a fresh scientific referee. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00003-p01/paper.pdf) · [TeX](projects/phys-smallmac00003-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00003-p01) · [Author handoff](projects/phys-smallmac00003-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00003-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00005-p01 · Three-copy universal qubit purification under complete stabilizer preservation</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三份未知噪声qubit：完全稳定子保持操作能否提高普适提纯保真度？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For a normalized-Haar pure qubit psi and three copies independently subjected to D_delta(X)=(1-delta)X+(delta/2)Tr(X)I, every completely positive trace-nonincreasing map E:M8->M2 that, tensored with any finite qubit identity, preserves the stabilizer positive cone has success-weighted conditional Haar fidelity F_delta(E)<=1-delta/2 whenever its average success is s>0. For every 0<delta<1 and every 0<s<=1, E_s=s Tr_(two inputs) is admissible and attains equality. Therefore the maximum in the unchanged source.md is exactly 1-delta/2 throughout its full stated domain. This three-input proof candidate does not assert the source paper's broader arbitrary-copy conjecture. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00005-p01/paper.pdf) · [TeX](projects/phys-smallmac00005-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00005-p01) · [Author handoff](projects/phys-smallmac00005-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00005-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00005-p03 · A third magnetic Neumann level below the Dirichlet ground state on the disk</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 磁圆盘的第三个Neumann能级，是否始终不高于Dirichlet基态？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For the spinless magnetic Laplacian H_b=(-i nabla-b(-y,x)/2)^2 on the unit disk, with Dirichlet eigenvalues lambda_k(b) and magnetic-Neumann eigenvalues mu_k(b) ordered with multiplicity, mu_3(b)<=lambda_1(b) for every b>0. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00005-p03/paper.pdf) · [TeX](projects/phys-smallmac00005-p03/manuscript/main.tex) · [Code / data](projects/phys-smallmac00005-p03) · [Author handoff](projects/phys-smallmac00005-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00005-p03/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00006-p04 · 指定两浓度幂律反应系统，能否严格认证四条嵌套极限环？</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 指定两浓度幂律反应系统，能否严格认证四条嵌套极限环？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | Existence of admissible parameters in the original source ODE with a hyperbolically stable unique positive equilibrium and at least four nested hyperbolic periodic orbits, repelling/attracting/repelling/attracting outward, all in a compact positive annulus. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00006-p04/paper.pdf) · [TeX](projects/phys-smallmac00006-p04/manuscript/main.tex) · [Code / data](projects/phys-smallmac00006-p04) · [Author handoff](projects/phys-smallmac00006-p04/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00006-p04/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00009-p01 · Unique spanning-tree families bound the static response of every complete four-state Markov network</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 四态反应网络的稳态灵敏度，是否落在唯一生成树家族的凸包内？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every strictly positive finite set of twelve directed rates k on K4 with sum k=1 and every d in \[-1,1\]^12 in the original column-generator model, r_j=partial_lambda log pi_j&#124;0 lies in the convex hull of v^alpha_j=G^alpha_j-sum_l pi_l G^alpha_l over exactly the families unique under the full directed-edge multiplicity vector. More strongly, the 4x12 rooted-tree edge-marginal matrix H(k) is a convex combination of the unique-family incidence matrices with nonnegative normalized weights depending on k only. Proof: research/proof.md and the complete 93-coefficient exact certificate. This resolves only the full K4 source claim, not the general-graph conjecture, full-hull attainability or full-tree coupling. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00009-p01/paper.pdf) · [TeX](projects/phys-smallmac00009-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00009-p01) · [Author handoff](projects/phys-smallmac00009-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00009-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00009-p02 · Pure-state uniqueness under common-axis measurements of three qubits excludes mixed-state impostors</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三qubit均匀旋转测量：纯态唯一性是否足以排除所有混态仿冒？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every complex unit vector psi in C^8, under the complete labeled three-qubit common-axis effects E_b(n)=tensor_j(I+b_j n.sigma)/2 for all unit n and all b, uniqueness of P=&#124;psi><psi&#124; among pure states implies uniqueness among all complex density matrices. More strongly, every nontrivial density-matrix competitor rho with the same data has K=rho-P of rank two with eigenvalues +/-s, and P,rho share its two-dimensional range; Q=P-2Tr(PK)K/Tr(K^2) is a distinct pure competitor. This is an exact three-qubit identifiability theorem, not an all-N or finite-error certification claim. A complete proposed computer-assisted proof is submitted for fresh review. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00009-p02/paper.pdf) · [TeX](projects/phys-smallmac00009-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00009-p02) · [Author handoff](projects/phys-smallmac00009-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00009-p02/manuscript/REPRODUCE.md) |

</details>

<details>
<summary><strong>phys-smallmac00012-p01 · Order-three unistochastic matrices form a monoid: exact compression of measured qutrit dynamics</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三能级的两段“酉演化后测量”，能否总压缩成一段？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every U,V in U(3), there exists W in U(3) such that &#124;W_ij&#124;^2 equals \[B(V)B(U)\]_ij for all i,j. Equivalently, the order-three unistochastic set U_3 is a monoid under ordinary matrix multiplication. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00012-p01/paper.pdf) · [TeX](projects/phys-smallmac00012-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00012-p01) · [Author handoff](projects/phys-smallmac00012-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00012-p01/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00014-p01 · The third magnetic Neumann eigenvalue does not exceed the Dirichlet ground state on an annulus</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 均匀磁场圆环上的第三 Neumann 能级是否仍低于 Dirichlet 基态？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For the dimensionless homogeneous-field magnetic Laplacian H_{a,b}=(-i nabla-A_b)^2 on every concentric annulus A_a={a<r<1}, with 0<a<1, b>0, no added harmonic Aharonov--Bohm flux, and respectively magnetic Neumann or Dirichlet conditions on both boundary circles, the globally ordered eigenvalues counted with multiplicity satisfy mu_3(A_a,b) <= lambda_1(A_a,b). |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00014-p01/paper.pdf) · [TeX](projects/phys-smallmac00014-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00014-p01) · [Author handoff](projects/phys-smallmac00014-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00014-p01/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00014-p11 · No history advantage in repeated environment-assisted qubit recovery</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三次固定环境测量时，历史反馈首次产生优势吗？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every qubit CPTP map with positive-definite Choi matrix, using the same four-outcome orthogonal projective measurement on each fresh minimal environment, the separately optimized current-outcome Markovian polar-recovery and full-history/final-only Bayesian entanglement fidelities are equal at three uses. More strongly, within the same physical model they are equal for every positive integer n and have common value (1+&#124;&#124;Q&#124;&#124;_*^n)/2, where Q is the determinant polarization matrix of any minimal Kraus frame. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00014-p11/paper.pdf) · [TeX](projects/phys-smallmac00014-p11/manuscript/main.tex) · [Code / data](projects/phys-smallmac00014-p11) · [Author handoff](projects/phys-smallmac00014-p11/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00014-p11/reproducibility/README.md) |

**Связанные результаты / ранние версии**

- [phys-smallmac00008-p02](projects/phys-smallmac00008-p02): Охваченная ранняя версия; сохранена без отдельного счёта. The earlier optimized two-use equality for full-Choi-rank qubit channels is included in the later all-positive-integer-use theorem under the same fresh minimal environment, fixed full four-outcome measurement and recovery conventions. The all-n determinant-polarization result subsumes n=2.

</details>

<details>
<summary><strong>phys-smallmac00015-p01 · A sharp weak-driving phase bound for symmetric complete Markov networks</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 对称完全图 K_N 的弱驱动相位常数是否统一等于二态极限？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | In the frozen symmetric-splitting complete-graph model, for every integer N>=3, k0>0, finite offset vector, period T>0, and finite real Fourier drive, the weak coefficients satisfy A2>=2k0 B2. At finite offsets the inequality is strict whenever at least one energy difference varies in time; equality is exactly the zero-response class A2=B2=0. The coefficient 2 is optimal but is attained by a response-active system only at the excluded offset boundary, approached by x1=x2=1 and x3=...=xN=delta down to zero. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00015-p01/paper.pdf) · [TeX](projects/phys-smallmac00015-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00015-p01) · [Author handoff](projects/phys-smallmac00015-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00015-p01/reproducibility/README.md) |

**Связанные результаты / ранние версии**

- [phys-smallmac00014-p03](projects/phys-smallmac00014-p03): Охваченная ранняя версия; сохранена без отдельного счёта. The earlier finite-offset symmetric K3 weak-drive inequality and sharp factor 2 are the N=3 specialization of the later complete-K_N weak-Fourier-drive theorem. Neither proves a finite-amplitude phase bound. The earlier specialized calculation remains available.

</details>

<details>
<summary><strong>phys-smallmac00016-p01 · Exact current-bit optimum and a robust history advantage for coarse-grained generalized-amplitude-damping feedback</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 粗粒化 GAD 反例中两步 current-bit 恢复的精确最优值是多少？ |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For the ordered full-Choi-rank generalized-amplitude-damping qubit instrument, the incoherent 03&#124;12 one-bit readout, two independent uses, and arbitrary clock-dependent qubit CPTP recoveries conditioned only on the current bit: (i) at p=18/25 and gamma=3/10 the exact optimum is F_2^M=289/400, attained by identity recovery, while the fixed feasible history policy attains 1831/2500 and therefore has exact advantage 99/10000; and (ii) on the closed rectangle R=\[71/100,723/1000\] x \[29/100,303/1000\], the same history policy attains H=1-gamma+p gamma^2/2 and every admissible current-bit policy obeys F_2^M<=H-1/1000, hence F_2^B-F_2^M>=1/1000 throughout R. The rectangle is a sufficient certified region, not a maximality claim, and no off-center exact optimum or exact Bayesian optimum is asserted. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00016-p01/paper.pdf) · [TeX](projects/phys-smallmac00016-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00016-p01) · [Author handoff](projects/phys-smallmac00016-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00016-p01/manuscript/REPRODUCIBILITY.md) |

**Связанные результаты / ранние версии**

- [phys-smallmac00015-p06](projects/phys-smallmac00015-p06): Охваченная ранняя версия; сохранена без отдельного счёта. Both use the same ordered GAD instrument, incoherent 03|12 bit, p=18/25, gamma=3/10 and two-use policy distinction. The later exact current-bit optimum 289/400 and history value 1831/2500 give 99/10000 advantage, strengthening the earlier 7/2500 witness, and add a certified rectangle. The n=1 equality also settles earliest onset.

</details>

<details>
<summary><strong>phys-smallmac00018-p01 · Exact indirect-gap boundary in a flux-one-third Harper–Hofstadter model with a period-three mass</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 磁通 1/3 Harper–Hofstadter 三带模型的间接绝缘隙边界 |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For the frozen Hamiltonian in problem.md, G1(r,m)=G2(r,m)=G(r,m). Let rc=sqrt((69-11sqrt(33))/8). For 1/2<=r<=rc, G is positive for every m except m=+/-sqrt(3)r, where G=0. For rc<r<=2 there are unique 0<m_-(r)<sqrt(3)r<m_+(r), given by the two physical branches X in (Xc,1) and X in (3/4,Xc) of equations (1)-(2) in evidence/global-boundary-certification.md with Xc=(7+sqrt(33))/16, such that G<0 exactly when m_-(r)<&#124;m&#124;<m_+(r), G=0 at &#124;m&#124;=m_-(r),m_+(r), and G>0 otherwise. Hence the relative insulating boundary consists exactly of the two direct segments m=+/-sqrt(3)r for 1/2<=r<=rc joined at their cusps to four mass-reflected indirect branches for rc<=r<=2. The extremizers are exactly those parametrized in Section 4 of that evidence file and their spectral/mass reflections; no other momentum or exceptional Laurent-factor sector occurs. The isolated-band Chern tuple is (+1,-2,+1) for &#124;m&#124;<sqrt(3)r and (0,0,0) for &#124;m&#124;>sqrt(3)r, with the nonzero tuple negated under flux/orientation reversal. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00018-p01/paper.pdf) · [TeX](projects/phys-smallmac00018-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00018-p01) · [Author handoff](projects/phys-smallmac00018-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00018-p01/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00013-p03 · Exact unrestricted Gaussian rank of two canonical matchgate magic states</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 两份 canonical matchgate magic state 的 unrestricted Gaussian rank |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For &#124;M>=(&#124;0000>+&#124;1111>)/sqrt(2), the exact unrestricted fermionic Gaussian rank over C of &#124;M> tensor &#124;M> is chi_G=4, with no particle-number, reality, blockwise ZZ, copy-exchange, or Pfaffian-chart restriction. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00013-p03/paper.pdf) · [TeX](projects/phys-smallmac00013-p03/manuscript/main.tex) · [Code / data](projects/phys-smallmac00013-p03) · [Author handoff](projects/phys-smallmac00013-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00013-p03/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00013-p04 · An exact criterion for removing an elementary amplitude-damping factor from a quantum channel</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 相位协变 qutrit 的 elementary 右除必要条件是否充分 |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every phase-covariant CPTP map Phi:M3->M3 with H=diag(0,1,2), Choi rank 2 through 8, and every ordered pair of distinct energy levels (a,b), condition (N) implies the existence of lambda in (0,1) and a CPTP Theta such that Phi=Theta composed with Psi_{lambda,a->b}. In fact, for any finite-dimensional CPTP Phi and orthogonal x,y, (N) is necessary and sufficient for such an elementary right quotient; if ZV=VA for a linearly independent minimal Kraus synthesis V, the quotient is CP exactly when 0<=lambda<1 and lambda<=&#124;&#124;A&#124;&#124;_2^{-2}. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00013-p04/paper.pdf) · [TeX](projects/phys-smallmac00013-p04/manuscript/main.tex) · [Code / data](projects/phys-smallmac00013-p04) · [Author handoff](projects/phys-smallmac00013-p04/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00013-p04/manuscript/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00013-p07 · The third boundary coefficient of even off-diagonally symmetric alternating-sign matrices</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 偶阶 OSASM 的第三列加权边界系数公式 |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every integer n>=2, the even-order OSASM boundary polynomial satisfies \[t^3\]X^O_{2n}(r,t)=r(1+(n-2)r^2)X^O_{2n-2}(r,1) in Z\[r\], under the definitions and BFK normalization frozen in problem.md and physics.json. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00013-p07/paper.pdf) · [TeX](projects/phys-smallmac00013-p07/manuscript/main.tex) · [Code / data](projects/phys-smallmac00013-p07) · [Author handoff](projects/phys-smallmac00013-p07/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00013-p07/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00020-p03 · Two-scale finite-size edge splitting at a repeated root of an extended Su–Schrieffer–Heeger chain</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | extended-SSH 重复衰减根线上的四个有限链边缘能级 |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For the finite open extended-SSH family H_N with u2=1, u0=r^2, u1=2r and r in \[1/5,4/5\], the exact confluent four-state pencil has positive energies r^{N+1}/phi_{1,N} and r^{N+1}/phi_{2,N} with the finite sums defined in the evidence. For every integer N>=61 the exact two positive in-gap energies obey the explicit uniform error functions R_a(N,r), these errors are relative o(1) uniformly in r, the leading laws are E_{N,1}=(1-r^2)r^{N+1}/N\[1+o(1)\] and E_{N,2}=N(1-r^2)^3r^{N-1}\[1+o(1)\], and no third positive level lies below the bulk-band distance (1-r)^2. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00020-p03/paper.pdf) · [TeX](projects/phys-smallmac00020-p03/manuscript/main.tex) · [Code / data](projects/phys-smallmac00020-p03) · [Author handoff](projects/phys-smallmac00020-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00020-p03/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00021-p01 · Exact finite-depth crossings in a Sierpinski–Hanoi free-fermion spin model</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Sierpinski–Hanoi 自由费米近简并的精确有限尺度递推 |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | In the finite open Sierpinski-Hanoi model defined in problem.md, restricted to the all-canonical-cycle-+1 single-particle sector and using the source normalization, the k=5 Figure-5 landmarks are exact transverse crossings at J=+/-1/3 and lambda=1/6. Their unique nonzero continuation exists for every k>=3 at J_k=+/-3^(-(k-3)/2), x_k=&#124;J_k&#124; and lambda_k=&#124;J_k&#124;/2; the generic flat multiplicity c_k=(3^(k-2)-1)/2 becomes c_k+1 and &#124;J_(k+1)/J_k&#124;=1/sqrt(3). On fixed I_+=\[1/4,1/2\] and I_-=-I_+, Delta_k is zero iff k=5; for k=3,4 and k>=6 it obeys the explicit positive coefficient-norm bound in evidence/fixed-interval-gap-salvage-result.md. Separately named moving windows W_k^+=\[J_k/2,3J_k/2\] and W_k^-=-W_k^+ have zero minima for every k>=3. The characteristic polynomial is generated by the signed three-scalar recurrence and exact quotient in the evidence. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00021-p01/paper.pdf) · [TeX](projects/phys-smallmac00021-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00021-p01) · [Author handoff](projects/phys-smallmac00021-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00021-p01/manuscript/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00023-p03 · An exact anti-degradability threshold for the three-level bosonic loss–dephasing channel</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 固定 (e^{-\gamma}=1/2) 时三 Fock 能级 loss–dephasing 信道的精确反可降阈值 |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For N^(3)_(lambda,ln2) defined exactly in immutable source.md, with lambda in\[0,1\] and normalized A,B Choi, anti-degradability holds if and only if lambda<=r, where r is the unique root in\[66454426803/10^11,66454426804/10^11\] of601r^6-714r^5+113r^4-1040r^3+2080r^2-1280r+256 (approximately0.664544268033). The exact rank4 X_r supplied in evidence/research-endpoint-proof.md is PSD, trace1, swap invariant and has both marginalsJ_r. That proof supplies explicit Hermitian strict separating H_lambda with W_Hlambda PSD in the full27-dimensional space and Tr(H_lambda J_lambda)<0 for every lambda>r, and exact post-loss extensions for every lambda<=r. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is proved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00023-p03/paper.pdf) · [TeX](projects/phys-smallmac00023-p03/manuscript/main.tex) · [Code / data](projects/phys-smallmac00023-p03) · [Author handoff](projects/phys-smallmac00023-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00023-p03/supplementary/README.md) |

</details>

<details>
<summary><strong>phys-00004-p05 · Diagonal quantum discord under unital qubit noise: a relative-entropy proof for two-qubit states</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Within the stated finite-dimensional single-use noise model, local unital noise cannot increase diagonal discord despite a moving marginal eigenbasis. This supplies the resource monotonicity left numerically supported in S1 for the frozen two-qubit domain. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every two-qubit density operator rho_AB and every unital CPTP channel E_A, provided both rho_A and E_A(rho_A) are nondegenerate, the entropy-based diagonal discord S(pi_A rho_AB)-S(rho_AB), using each state's own marginal spectral projections, is nonincreasing under E_A tensor id_B. This settles precisely the frozen source.md/problem.md domain, including rank-deficient global states and arbitrarily small positive marginal gaps. |
| **Предлагаемый вклад** | Exact proof of the entire frozen nondegenerate two-qubit/unital-CPTP inequality via channel-image compatibility with output marginal pinching and the quantum relative-entropy Pythagorean identity. Channel/dephasing commutation is unnecessary for this entropy-based claim. |
| **Ограничения / нерешённые трудности** | 2026-10-12 exact-title and diagonal-discord/unital/monotonicity/counterexample/conjecture/proof/relative-entropy/pinching/noncommuting/Pythagorean searches; latest S1 version record and relevant full primary passages checked; S2 actual v4 primary PDF/text rechecked. No later exact resolution identified, but no exhaustive citation graph or priority guarantee. Primary and raw query evidence preserved. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00004-p05/paper.pdf) · [TeX](projects/phys-00004-p05/manuscript/main.tex) · [Code / data](projects/phys-00004-p05) · [Author handoff](projects/phys-00004-p05/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00004-p05/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00004-p06 · Global optimality of every-jump resetting for a Cauchy flight: a computer-assisted survival comparison</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Within the reset-before-jump Cauchy search model, Q2>=Q1^2 selects reset before every jump as the unique optimum among constant Bernoulli resetting rates; interior reset-rate optimization cannot lower the mean passage time, even at equality of the two-step criterion. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every finite b>=0 in the unit Cauchy reset-before-jump killed walk, Q2(b)>=Q1(b)^2 implies T_b(r)>T_b(1)=1/\[1-F(b)\] for every0<r<1; r=1 is equality. |
| **Предлагаемый вклад** | Computer-assisted proof of the complete frozen unit-Cauchy implication for every finite b>=0 and every 0<r<=1, strengthened to strict interior comparison. A finite survival enclosure for orders3..9 plus exact zero-barrier induction gives all-order coefficient dominance; a separate finite/analytic exclusion proves the antecedent cannot hold for b>=1.809. |
| **Ограничения / нерешённые трудности** | Current exact-title/identifier, Cauchy/global/sufficient/proof/conjecture and later-result searches on2026-10-12; primary originalv1 full HTML, Bonomo-Pal geometric convention and later2507.11196v1 full HTML rechecked. No exact later resolution located. Journal fulltext retrieval failed; targeted primary-PDF indexing still locates the conjecture, but no full version comparison is claimed. Abstract-only newer lead and inaccessible neighboring2D paper are recorded. Novelty/priority remain provisional for fresh referee review. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00004-p06/paper.pdf) · [TeX](projects/phys-00004-p06/manuscript/main.tex) · [Code / data](projects/phys-00004-p06) · [Author handoff](projects/phys-00004-p06/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00004-p06/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00004-p08 · Arbitrarily clustered hot spots on bridgeless quantum graphs</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | For homogeneous standard-Kirchhoff network diffusion, the hottest/coldest set of the unique slowest nonconstant mode does not impose any positive universal lower bound relative to network metric diameter, even when every edge lies on a cycle. This is a model prediction with constant diffusivity, without a fixed-volume or bounded-degree constraint. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every real epsilon>0 there is a finite connected compact positive-length standard-Kirchhoff metric multigraph Gamma with every edge on a cycle, diameter 1, simple first positive eigenvalue mu2, and complete global maximum/minimum union M satisfying diam(M)<epsilon. Explicit witness: for m=max(4,ceil(36/(pi^2*epsilon^2))), h=atan(1/sqrt(m))/pi, take a central tree with two long arms 1/2, two stems h to fan hubs, and m leaves of length 2h per hub; replace every edge by two equal parallel copies. Its simple mu2=\[atan(1/sqrt(2m+1))/h\]^2, its full metric diameter is 1, and its complete extrema union is exactly the 2m fan leaf vertices of diameter 6h<epsilon. This is the original Conjecture 8.9 no-bridge scope, allowing articulation vertices and no fixed volume/degree restriction. |
| **Предлагаемый вклад** | An explicit one-integer uniformly doubled lengthened split-tree family proves the full printed existence statement: for m>=4, h=atan(1/sqrt(m))/pi, mu2=\[atan(1/sqrt(2m+1))/h\]^2 is simple, the exact complete extrema union has diameter 6h, and the actual doubled metric diameter is 1. m=max(4,ceil(36/(pi^2*epsilon^2))) makes 6h<epsilon for every epsilon>0. |
| **Ограничения / нерешённые трудности** | Fresh bounded primary-source searches and exact-transfer comparison on 2026-10-12, recorded in evidence/research-pass1-literature.md and raw web-01 through -08. Current official original v4, survey v3, and same-authors higher-dimensional v2 were checked. No direct later resolution was identified; incomplete indexing and other terminology limit any priority claim. candidate_novel is provisional and requires a fresh referee novelty/significance check. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00004-p08/paper.pdf) · [TeX](projects/phys-00004-p08/manuscript/main.tex) · [Code / data](projects/phys-00004-p08) · [Author handoff](projects/phys-00004-p08/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00004-p08/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00005-p06 · An eighth-order inverse-response filter in a ten-site quantum walk</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The same autonomous ten-site model and tau=2pi achieve one higher absolute response order, hence seventh rather than sixth conditional inverse-state power in gamma under the stated spectral and normalization factors. Couplings remain of order one, with a larger leading scalar success coefficient. Matched full-propagation samples show much smaller error at similar norm(H)*t; no complete algorithmic or hardware speedup is asserted. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For the exact R=4 ten-site zero-diagonal open Hermitian Jacobi chain of source.md/problem.md, there exist fixed positive couplings specified by the unique cancellation root in evidence/research-root-certificate.json, tau=2pi, a nonzero real linear coefficient ell in (-1.078612,-1.078611), x0=1/16 and C=131072002 such that &#124;<10&#124;exp(-i tau T4(x;J))&#124;1>-i ell x&#124;<=C*x^8 for every 0<x<=x0. This is the precise R=4 existence resolution, including the high-energy branch; it does not settle the original author all-R conjecture. |
| **Предлагаемый вклад** | An explicit exact-root specification of positive fixed R=4 couplings cancels cubic, quintic and septic low-energy coefficients simultaneously, retains a nonzero linear response, and gives the full-amplitude bound &#124;a4-i ell x&#124;<=131072002*x^8 for every 0<x<=1/16. Root existence is certified by interval contraction; the oscillatory high branch is bounded separately. |
| **Ограничения / нерешённые трудности** | Primary version pages were reopened on 2026-10-12 around 17:32-17:34 UTC: 2508.06611v1, 2512.08141v1 and 2510.06316v3. Reread the original Conjecture 1/Table I/Appendix A, successor Theorem 4.1/Sections 4.2 and 6, and competitor v3 Section 4.4/Proposition 19/Corollary 20. Targeted exact-title/identifier/author searches identified no direct later resolution in this limited screen. The competitor uses repeated Hamiltonian-QSVT queries. Coverage is not exhaustive, absence of a hit does not prove priority, and candidate_novel requests independent novelty/significance review. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00005-p06/paper.pdf) · [TeX](projects/phys-00005-p06/manuscript/main.tex) · [Code / data](projects/phys-00005-p06) · [Author handoff](projects/phys-00005-p06/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00005-p06/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00007-p05 · Exact conditional min-entropy of two-qubit unitary channels with white noise</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The conditioning-channel TP restriction has zero cost for this single-use family; its conditional channel min-entropy is computed exactly from the pure-unitary Choi Schmidt spectrum rather than by a constrained SDP. Units are bits and the resource interpretation uses trivial output Hamiltonians. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every U in U(4) and real p in \[0,1\], let Omega=(1-p)&#124;u><u&#124;+p I16/16 be the normalized Choi state in the grouped X=RA A,Y=RB B order, rho_U=Tr_X &#124;u><u&#124; and L=Tr sqrt(rho_U). For the exact SDPs in problem.md, including Tr_B Q=(Tr Q)I_RB/2 in t, s(Omega)=t(Omega)=(1-p)L^2+p/4. A common optimizer is Q=(1-p)L sqrt(rho_U)+(p/16)I4. Hence S_infty\[A&#124;B\]_N=H_min(X&#124;Y)_Omega-1 for every frozen noisy two-qubit gate, including degeneracies, deficient Schmidt rank and p endpoints. This is a proposer proof awaiting fresh referee review. |
| **Предлагаемый вклад** | Settle the frozen all-U(4), all-p in \[0,1\] noisy identity and supply explicit common optimum (1-p)(Tr sqrt(rho_U))^2+p/4 with a common TP-feasible optimizer and matching state-dual witness. |
| **Ограничения / нерешённые трудности** | 2026-10-12: current official arXiv pages/fulltext confirm v2 for both decisive preprints; decisive local source sections re-read; exact identifier/title, author/noisy, white-noise, depolarized-pure, pseudopure and Schmidt/min-entropy queries. No later primary resolution verified; bounded searches do not establish global priority; independent referee comparison remains required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00007-p05/paper.pdf) · [TeX](projects/phys-00007-p05/manuscript/main.tex) · [Code / data](projects/phys-00007-p05) · [Author handoff](projects/phys-00007-p05/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00007-p05/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00007-p06 · The sharp overlap threshold for antidistinguishability of five pure states</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The overlap-only universal guarantee for ideal single-copy five-state zero-error exclusion is sharp. Arbitrarily small increases above sqrt(3/8) admit non-excludable states, with certified positive uniform-prior error lower bound s*eta/5. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For five arbitrary normalized complex pure states in C^5, allowing dependence, the infimum t5 of maximum pairwise overlap modulus over non-antidistinguishable tuples equals sqrt(3/8), with single-copy unrestricted PSD POVMs and zero effects permitted. An explicit rank-three family has every squared overlap m and is non-antidistinguishable for every real 3/8<m<2/5. Its exact physical dual certificate gives uniform-prior optimum exclusion error at least s*eta/5>0 as defined in evidence/five-state-proof.md. The published bound includes the boundary; this is an infimum approached from above, not an attained non-excludable minimum. No n>=6 or exact optimum error claim. |
| **Предлагаемый вклад** | An explicit rank-three five-state pure-state family with every squared pairwise overlap m in (3/8,2/5), and an exact positive-trace physical exclusion dual witness for every such m, proves t5=sqrt(3/8). |
| **Ограничения / нерешённые трудности** | 2026-10-12 primary recheck of arXiv:2609.17411v1 Section 1.1 and Section 3; retained publisher Quantum 9,1622 full PDF, Corollary 5.4, Section 6 and equation (2). Bounded targeted searches and precise comparison are preserved; no later exact resolution found, but exhaustive priority is not certified. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00007-p06/paper.pdf) · [TeX](projects/phys-00007-p06/manuscript/main.tex) · [Code / data](projects/phys-00007-p06) · [Author handoff](projects/phys-00007-p06/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00007-p06/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00007-p14 · Extreme excursions and terminal-sign retention in stationary Brownian resetting</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Quantifies retention of a stationary extreme excursion by endpoint-sign monitoring; reset-position dependence enters through terminal-sign renewal, and at zero reset the coefficient is halfway between the two published neighboring coefficients. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every fixed T>0,r>0,a real in the stationary zero-drift variance-t reset Brownian model, exp(alpha u)P(M_T>u,Y_T>0) converges to exp(alpha a)\[Phi(alpha sqrt(T))+r integral_0^T Phi(alpha sqrt(s))q_a(T-s)ds\], with the explicit remainder (2) in joint-tail-proof.md for u>max(a,0), proving the published conjectured bounds. |
| **Предлагаемый вклад** | Explicit all-fixed-parameter joint maximum/positive-terminal coefficient with post-reset sign probability q_a, plus a Gaussian-tail finite-u remainder; establishes the named conjecture and its bounds within the frozen zero-drift stationary Brownian model. |
| **Ограничения / нерешённые трудности** | 2026-10-12 fresh arXiv version history and v3 Remark 3 and publisher Remark 3, exact title/identifier and stationary joint-tail resolution searches; local fulltext NJP sections 3.1.2, 4.1 and 5 and equations 22-30,78-92. No later resolution identified; priority beyond this bounded coverage remains unverified. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00007-p14/paper.pdf) · [TeX](projects/phys-00007-p14/manuscript/main.tex) · [Code / data](projects/phys-00007-p14) · [Author handoff](projects/phys-00007-p14/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00007-p14/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00032-p01 · A resource-dependent thermodynamic uncertainty relation for three-port coherent conductors</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Knowing that the hardware has only three single-channel normal leads gives a strictly stronger lower bound on actual total dissipated heat entropy from one measured particle-current mean and full count variance. The bound includes all reservoirs and does not require event entropy, extra activity, a reversed experiment, small bias or hidden probes. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every stationary elastic number-preserving noninteracting normal-fermion conductor in the exact C3 class of source.md/problem.md, with three physical reservoirs, at most one open channel per lead, a finite Hermitian sample and causal normal leads, fixed finite chemical potentials and strictly positive temperatures, finite J=abs(chi0 prime(0))>0, full count-variance rate C2=chi0 double-prime(0)>0 and actual total reservoir heat entropy sigma>0, sigma/k_B >= (9/10) J asinh(J/C2). The complete analytic-plus-integer-interval argument covers both current signs, both three-cycle orientations, every 3x3 unitary scattering matrix including reflected closed channels, arbitrary legal energy dependence, and signed energy integration. An enclosed exact rational psi0 witness is below 9/10, hence kappa3>=9/10>psi0. This proposed proof answers the original strict-improvement question without determining optimal kappa3 or claiming saturation; fresh referee acceptance is pending. |
| **Предлагаемый вклад** | A proposed computer-assisted full-scope bound sigma/k_B >= (9/10) J asinh(J/C2) for every legal normal elastic noninteracting three-reservoir conductor with at most one channel per lead, arbitrary finite thermal/chemical biases, generic broken-reciprocity scattering and signed energy integration. Exact psi0 is below 9/10 by a certified rational witness. Optimal kappa3 is not determined. |
| **Ограничения / нерешённые трудности** | Bounded current primary recheck on 14 October 2026 UTC: S1 current v2, S5 v1 and S4 July-2026 v1 histories/full defining statements; S3 current v3 and October-2026 publisher abstract retaining linear-response/probe premises; previously preserved S2,S6,S7 defining scopes; fresh primary published S8 PDF/current arXiv v3, including its nonlinear Eqs.(84)-(87),(95)-(96). Exact titles and three-terminal/nonlinear/single-channel/asinh/9/10/Birkhoff/cycle terms searched. No exact restricted resolution was identified; absence of hits is not exhaustive openness or priority proof. Fresh referee and eventual human review must assess novelty/significance independently. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00032-p01/paper.pdf) · [TeX](projects/phys-00032-p01/manuscript/main.tex) · [Code / data](projects/phys-00032-p01) · [Author handoff](projects/phys-00032-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00032-p01/manuscript/REPRODUCIBILITY.md) |

**Связанные результаты / ранние версии**

- [phys-00030-p01](projects/phys-00030-p01): A finite nonreciprocal full-current large-deviation counterexample is not the resource-dependent three-port noise/entropy theorem. The target bound, observable and hypothesis sets differ.

</details>

<details>
<summary><strong>phys-00036-p01 · Algebraic endpoint densities are the transfer-matrix charges in regular Yang–Baxter chains</strong> — Доказательство · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Identifies the quantum-group algebraic densities with the actual prescribed local conservation-law hierarchy, excluding untracked lower-charge or scalar mixing and removing the unproved identification in applications of the source's undeformed recurrence. No new particle, phase, experiment, all-order long-range deformation or measured algorithmic speedup is asserted. |
| **Исходная задача** | доказана в указанной области |
| **Результат и точная область утверждения** | For every finite-dimensional complex V and every formal/analytic source-regular Yang--Baxter R(u,v) with R(u,u)=P and R12(u,v)R21(v,u)=I, for every k>=2, BOTH Conjecture 2.7 block-R endpoint density differences are equivalent to a density of Q_k^(L)=partial_u^(k-2)(t_L^-1 t_L prime)&#124;0 modulo exactly I tensor m - m tensor I. Their cyclic sums equal the prescribed raw transfer charges on every homogeneous untwisted periodic chain L>=k. This is the complete undeformed source identity, including general non-difference R and minimal L=k; no higher-order long-range or other-boundary extension is claimed. |
| **Предлагаемый вклад** | A finite-chain ordered-product and rooted connected-coefficient proof of BOTH endpoint formulas for every source-allowed finite-dimensional regular braiding-normalized Yang--Baxter R, every k>=2 and every periodic L>=k, plus a constructive tensor-word proof of the exact local-gradient equivalence. |
| **Ограничения / нерешённые трудности** | On 14 October 2026 checked current arXiv original history (still v2, 5 June 2026), bounded exact identifier/title/conjecture and neighbour searches, and inspected the defining source loci, BBL Eq.(2.16), 2021 Appendix A Eqs.(A.1)--(A.7), and older Links/Takizawa ladder constructions. Raw retrievals and selected primary full texts are preserved. No later resolution was verified; search absence is not proof of openness and comprehensive priority is not established. Candidate novelty requires fresh referee assessment. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00036-p01/paper.pdf) · [TeX](projects/phys-00036-p01/manuscript/main.tex) · [Code / data](projects/phys-00036-p01) · [Author handoff](projects/phys-00036-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00036-p01/REPRODUCIBILITY.md) |

</details>

## Опровержение

<details>
<summary><strong>phys-00004-p02 · An exact qutrit counterexample to an uncertainty conjecture</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Энтропийная неопределённость описывает ограничения совместной предсказуемости несовместимых измерений. Сводные спектральные характеристики могут терять существенную структуру. |
| **Результат и охват исходной задачи** | Точная рациональная трёхмерная унитарная конструкция опровергает проверяемую гипотезу extended-MUB. |
| **Предлагаемый вклад** | Краткий сертификат в рациональной арифметике показывает, почему второе сингулярное число само по себе не обеспечивает предложенное универсальное утверждение. |
| **Ограничения** | Это контрпример к конкретной гипотезе, а не к принципу неопределённости. Новое точное заменяющее неравенство ещё предстоит найти. |
| **PDF и исходники** | [PDF](projects/phys-00004-p02/paper.pdf) · [TeX](projects/phys-00004-p02/manuscript/main.tex) · [Bib](projects/phys-00004-p02/manuscript/references.bib) · [Код / данные](projects/phys-00004-p02) · `python reproducibility/reproduce.py --project phys-00004-p02` |

</details>

<details>
<summary><strong>phys-00005-p01 · A 16-vertex graph defeats path minimality</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Среднее смешивание квантового блуждания отражает устойчивую структуру возврата. Экстремальные утверждения о графах помогают исследовать перенос и локализацию. |
| **Результат и охват исходной задачи** | Связный простой невзвешенный граф с 16 вершинами и 62 рёбрами имеет показатель ленивости 1673/1192 против 23/16 у пути; разность равна -81/2384. |
| **Предлагаемый вклад** | Два точных представления сертифицируют конечный контрпример к указанному утверждению о минимальности пути для лапласианного квантового блуждания. |
| **Ограничения** | Не классифицированы минимизаторы для всех размеров графов и не решены задачи для иных гамильтонианов и соглашений о нормировке. |
| **PDF и исходники** | [PDF](projects/phys-00005-p01/paper.pdf) · [TeX](projects/phys-00005-p01/manuscript/main.tex) · [Bib](projects/phys-00005-p01/manuscript/references.bib) · [Код / данные](projects/phys-00005-p01) · `python reproducibility/reproduce.py --project phys-00005-p01` |

</details>

<details>
<summary><strong>phys-00006-p01 · A qubit memory breaks a universal contraction proposal</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Оценки сжатия канала количественно описывают потерю различимости. Квантовая память может нарушить интуицию, основанную на входах без вспомогательной системы. |
| **Результат и охват исходной задачи** | Точный пример амплитудного затухания с допустимыми запутанными входами и одинаковыми маргинальными состояниями опровергает предложенную универсальную замену alpha-Doeblin для hockey-stick оценки. |
| **Предлагаемый вклад** | Сертификат выявляет конкретный механизм нарушения, чувствительный к памяти и удовлетворяющий исходным ограничениям на входы. |
| **Ограничения** | Опровергнута конкретная усиленная оценка; это не опровергает все неравенства Дёблина и не даёт оптимальной замены. |
| **PDF и исходники** | [PDF](projects/phys-00006-p01/paper.pdf) · [TeX](projects/phys-00006-p01/manuscript/main.tex) · [Bib](projects/phys-00006-p01/manuscript/references.bib) · [Код / данные](projects/phys-00006-p01) · `python reproducibility/reproduce.py --project phys-00006-p01` |

</details>

<details>
<summary><strong>phys-smallmac00001-p06 · A missing spectral arc at finite cycle affinity in four-state Markov generators</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 有限热力学力下 Markov 谱集合是否等于 Karpelevich 区域的纵向缩放 |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | At B*=log(3)/2 there exists eta>0 such that every four-state generator with escape rates <=1 and both oriented cycle-product bounds product_forward<=3^n_c product_reverse obeys &#124;Im(lambda)&#124;<=1/2-delta/2+delta^2/4 whenever delta=-1-Re(lambda) is in (0,eta). The exact-alpha unrestricted companion supplies compressed points Lambda(delta)=-1-delta+(i/2)sqrt(1-2delta+3delta^2), all strictly above that bound for 0<delta<min(eta,1/2). Thus the affine-image equality H_eq fails by nonattainment, including the closure of the larger bounded-affinity class. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00001-p06/paper.pdf) · [TeX](projects/phys-smallmac00001-p06/manuscript/main.tex) · [Code / data](projects/phys-smallmac00001-p06) · [Author handoff](projects/phys-smallmac00001-p06/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00001-p06/manuscript/README.md) · [Replay](projects/phys-smallmac00001-p06/manuscript/repro/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00002-p09 · A counterexample to the forward waiting-time entropy bound in periodically driven Markov networks</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 周期驱动中，正向相位平均等待时间是否仍给熵产生下界？ |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | Counterexample to the universal upper bound hat_sigma_Psi<=bar_sigma exactly as quantified in immutable source.md and problem.md. On the complete three-state graph, observe only 1->2 and 2->1; take symmetric edge triples (k12,k23,k31)=(r,1,1),(1,r,1),(1,1,r)/t_star in consecutive segments of length t_star, with r>0,r!=1. The unique periodic distribution is uniform and bar_sigma=0, whereas the finite same-forward-protocol waiting estimator is strictly positive. The same-direction waiting-density difference has dimensionless x^3 coefficient -(r-1)^2/\[6(r+2)\]. For r=10, t_star*hat_sigma_Psi>=27/5734400000000000000000000000000000>0, with normalized joint waiting laws and controlled infinite logarithmic tail. This resolves the original conjunction by violating its upper half; no separate universal lower-bound theorem, smooth/fixed-prefactor claim, controller-cost claim, or independent acceptance is included. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00002-p09/paper.pdf) · [TeX](projects/phys-smallmac00002-p09/manuscript/main.tex) · [Code / data](projects/phys-smallmac00002-p09) · [Author handoff](projects/phys-smallmac00002-p09/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00002-p09/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00005-p02 · A computer-assisted three-state counterexample to a nonlinear phase-lag bound</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三态非线性周期响应的相位滞后，是否受最慢跃迁前因子约束？ |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | The frozen universal complete-three-state positive-branch phase bound is false. For the exact terminating-decimal M=2 parameters in evidence/counterexample-parameters.json, the unique strictly positive periodic state satisfies A>0 and B>0, while A-k0,min B<0; specifically the primary outward-rounded certificate gives A in \[0.1913253462459419,0.8081296470533585\], B in \[6.1034541204110998,6.1582195856729802\], and A-k0,min B in \[-5.966894239630766,-5.295324473154014\]. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00005-p02/paper.pdf) · [TeX](projects/phys-smallmac00005-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00005-p02) · [Author handoff](projects/phys-smallmac00005-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00005-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00006-p01 · Activity above one half in finite Glauber annealing</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 单调降温的Glauber退火，每步跳跃概率是否始终不超过 \(1/2\)？ |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | For the layered graph A(3),B(4),C(4), complete A-B edges, a B-C matching and C clique, with E/epsilon=(0x3,1x4,64x4), q=(10001/10000,33/32,64), beta epsilon=log q, K=2 and exact Gibbs initial state, A1>63/125 and (A0+A1)/2>251/500. For all independent perturbations &#124;delta(E_i/epsilon)&#124;<=1/1000 with the same temperatures and a redefined Gibbs initial state, A1>1003737/2000000 and the mean>8014821/16000000, both >1/2. This admissible finite example disproves the original all-regular-graph single-step activity bound in source.md/problem.md. It also violates its two-step averaged counterpart. Both are research claims submitted for fresh review, not an accepted scientific audit. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00006-p01/paper.pdf) · [TeX](projects/phys-smallmac00006-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00006-p01) · [Author handoff](projects/phys-smallmac00006-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00006-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00006-p02 · Coherent information in uniformly noisy graph states is not ordered by subsystem size</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 均匀噪声图态中，节点较多的一侧是否总有较高的相干信息？ |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | For the exact independent uniform phase-noise graph-state model of source.md/problem.md, the connected 5x4 biadjacency matrix with rows (1001),(1001),(1001),(0101),(0011) at P=199/200 has GF(2) rank3, no zero rows/columns, n_A=5>4=n_B>=3, and -0.0043<S_A-S_B<-0.0042 bits, with I_A>2.7 and I_B>2.7 bits. This is a strict counterexample to the frozen universal node-count ordering. More generally, for every integer r>=3, Gamma_r has rows v1,v1,v1,v2,...,vr, vi=ei+e_(r+1) in F2^(r+1); it is connected of size(r+2)x(r+1), rankr, and at the same P has Delta_r<=Delta_3<-0.0042 and I_B(r)>I_A(r)>2.7. These are coherent-information lower bounds, not equalities for optimal distillable entanglement. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00006-p02/paper.pdf) · [TeX](projects/phys-smallmac00006-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00006-p02) · [Author handoff](projects/phys-smallmac00006-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00006-p02/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00007-p01 · Common output bias matters in randomness certification from quantum speed limits</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 量子速度极限的随机性认证：固定相关差，输出共同偏置是否真的无关？ |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | In the exact average branch-speed-budget relaxation defined in source.md and problem.md, take e=1/2, C_off=(sin(3/5),-sin(2/5)), and d=(sin(3/5)+sin(2/5))/2. Both C_off and (d,-d) lie in Q_(1/2). The submitted computer-assisted proof gives H*(C_off,1/2)>0.7758 bits and H*((d,-d),1/2)<0.7653 bits, so their difference exceeds 0.0105 bits. This counterexample disproves the original universal common-bias equality. It does not refute the proven midpoint lower-bound lemma or assert an optimal physical attack under a true total-state-variance constraint. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00007-p01/paper.pdf) · [TeX](projects/phys-smallmac00007-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00007-p01) · [Author handoff](projects/phys-smallmac00007-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00007-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00008-p01 · Comment on “Distinguishing graph states by the properties of their marginals”</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 图态凝聚：内部顶点各接至多一个外部顶点，是否足以保留局部Clifford等价？ |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | 原始固定标签双端外度≤1的Boolean OR凝聚保持LC等价的全称命题为假。完整证书：V={1,…,6}，C={1,2,3}，E(G)={13,16,24,35,46}，E(G′)={13,15,24,36,46,56}；G′=τ5τ1τ3G，两端连通且C外度均(1,1,1)、r_C=3。凝聚后B={4,5}对{6,c}的切割矩阵分别\[\[1,1\],\[0,1\]\]与\[\[1,1\],\[1,1\]\]，GF(2)秩2与1，边缘谱(1/4×4)与(1/2×2,0×2)，因此不LU等价，特别不LC等价。此反例允许C不连通；不主张无标签版本、C连通修正版或最小性。 |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is disproved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00008-p01/paper.pdf) · [TeX](projects/phys-smallmac00008-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00008-p01) · [Author handoff](projects/phys-smallmac00008-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00008-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-00002-p04 · Comment on “Bounds on skewness and kurtosis of steady-state currents”</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Under the stated assumptions, negative fourth heat cumulants cannot exclude purely thermally driven classical Markov dynamics. This removes the proposed universal nonnegative-kurtosis diagnostic outside equilibrium. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | The frozen three-state two-positive-temperature, fully paired detailed-balance model has strictly positive c2 and strictly negative long-time hot-bath c4. It is an exact counterexample to the universal nonnegative thermal fourth-cumulant assertion. |
| **Предлагаемый вклад** | A fully specified finite three-microstate, two-positive-temperature network with exact negative fourth long-time bath heat cumulant, obeying the stated thermal local detailed-balance premises. The full finite generator, not a residence-current approximation, is certified by two distinct exact calculations. |
| **Ограничения / нерешённые трудности** | provisional; no equivalent purely thermal counterexample or later exact resolution found in targeted current primary-literature checks; absence of hits does not prove novelty No fresh referee or exhaustive citation-network search has occurred; raw web evidence consists of returned primary passages rather than complete downloaded source PDF bytes. Proposed physical intermittency explanation is not a certified singular-limit mechanism. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00002-p04/paper.pdf) · [TeX](projects/phys-00002-p04/manuscript/main.tex) · [Code / data](projects/phys-00002-p04) · [Author handoff](projects/phys-00002-p04/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00002-p04/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00002-p10 · A balanced beam-splitter counterexample to the low-order Wigner–Rényi vacuum bound</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Balanced mixing of two independent non-Gaussian low-energy states does not preserve the vacuum minimum for all low-order Wigner–Rényi entropies; the proposed extension to every alpha in (0,1/2) fails. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | The universal low-order Wigner–Rényi vacuum bound for independently prepared balanced beam-splitter inputs is false. With \[x,p\]=i and Wvac=exp(-(x²+p²))/pi, prepare psi=(20&#124;0>+&#124;2>)/sqrt401 independently on both modes, trace one output after the balanced lossless mixer, and set alpha=1/4. Its exact retained Wigner function is exp(-R)\[(401-2R+R²/2+20sqrt2(x²-p²))/401\]²/pi, R=x²+p². A directed full-plane upper bound proves I_1/4(Wout)<9.43718<9.43892<I_1/4(Wvac)=4pi^(3/4), hence h_1/4(Wout)<h_1/4(Wvac). No other alpha range or optimum is claimed. |
| **Предлагаемый вклад** | Exact independent product input psi=(20&#124;0>+&#124;2>)/sqrt401 yields an admissible beam-splitter state violating the vacuum bound at alpha=1/4; directed full-plane upper I<9.43718, vacuum I>9.43892. |
| **Ограничения / нерешённые трудности** | 2026-10-12 official full text and version histories of 2411.05562v2 and 2609.24670v1; preserved 2601.16898v2 context; bounded searches for Wigner Rényi beam-splitter low-alpha counterexamples, cross-Wigner p<1 and squeezed alpha=1/4. No matching resolution located; absence of hit is not exhaustive priority proof. Referee novelty audit remains mandatory. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00002-p10/paper.pdf) · [TeX](projects/phys-00002-p10/manuscript/main.tex) · [Code / data](projects/phys-00002-p10) · [Author handoff](projects/phys-00002-p10/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00002-p10/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00005-p05 · An even first excitation in a phase-shifted EPR-like Hamiltonian</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The true first excitation is even and the gap is Ee2-Ee1; substituting the lowest odd energy overestimates it by more than3/10 in the fixed edge energy unit. Odd-parity probes cannot couple the even ground state to this even excitation; no response intensity asserted. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | The universal Eo1<=Ee2 question frozen in source.md/problem.md is false. For the exact negative unnormalized pairing-projector Hamiltonian on K4, s=3/4, theta13=theta23=pi and all other phases0, the graph is legal and phase-obstructed, Ee2<-89/20<-83/20<Eo1. Its unique ground and first excitation are even. Reversal persists when &#124;s-3/4&#124;<1/1000 and every wrapped phase deviation is<1/1000, with Eo1-Ee2>252/1000. This answers negatively the restricted phase extension, not the phase-free Conjecture2. |
| **Предлагаемый вклад** | A legal unweighted nonbipartite K4 at s=3/4 and phases pi on edges13,23 has Ee2<-89/20 and Eo1>-83/20, exactly disproving the project universal phase-obstructed ordering; a legal open amplitude/phase neighborhood retains reversal. |
| **Ограничения / нерешённые трудности** | 2026-10-12: reopened current official arXiv histories and February/July fulltexts; reread October Section6.3 and preserved primary excerpts. All four histories list v1. Five focused parity/phased-EPR/counterexample searches found no explicit resolution. Older flux-model equivalences and complete citation networks were not exhaustively searched; candidate priority remains subject to fresh referee and author review. Exact terms and raw records in comparison files. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00005-p05/paper.pdf) · [TeX](projects/phys-00005-p05/manuscript/main.tex) · [Code / data](projects/phys-00005-p05) · [Author handoff](projects/phys-00005-p05/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00005-p05/supplement/README.md) |

</details>

<details>
<summary><strong>phys-00007-p19 · An exact counterexample to the reported spin-9/2 anticoherence extremum</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The corrected attainable A3 changes the next-order directional-isotropy benchmark after fixing lower moments. Two complete exact fidelity representations and rational coefficient enclosures show F_witness(eta)<F_published_chi(eta) for all 0<=chi<=pi/2 and 0<eta<=2 asin(1/10) radians; the leading difference is -(252/5)D eta^6. The shared eta^2 sensitivity and general multiparameter QFI optimality are not changed or inferred. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | The original conditioned spin-9/2 bound is disproved: in normalized Dicke convention k=m+j, the pure vector with c0=c9=-1/sqrt(6), c3=c6=1/sqrt(3), all other coefficients zero, has rho1=I2/2, rho2=I_sym,2/3, and P3=4253/15876-10sqrt(42)/3969<789/3136, equivalently A3=(11623+40sqrt(42))/11907>2347/2352. The strict gap is (640sqrt(42)-4139)/254016. Supporting physical result: its uniform unknown-axis rotation-average fidelity is lower than that of every member of Martin et al. Eq.(65), for all 0<=chi<=pi/2 and 0<eta<=2 asin(1/10) radians. No claim of the true global A3 or finite-angle optimum is made. |
| **Предлагаемый вклад** | An exactly normalized phase alteration with c0=c9=-1/sqrt(6), c3=c6=1/sqrt(3) obeys the original rho1/rho2 constraints and has P3*=4253/15876-10sqrt(42)/3969<789/3136, equivalently A3*=(11623+40sqrt(42))/11907>2347/2352. The strict purity gap is (640sqrt(42)-4139)/254016, certified by the integer difference 71879. This disproves the original universal bound without asserting the true global maximum. |
| **Ограничения / нерешённые трудности** | Rechecked current primary histories and relevant full-text portions on 2026-10-12 before extending legacy work: 1909.08355v2, 1503.03446v3, 1509.08300v2, 1707.01246v2, 2509.18533v3, 2404.15548v3, 2605.29436v1, 2505.06154v2 and the retained published PDFs. Exact threshold, phase/radical and correction searches are saved. No identified earlier exact extremal correction appeared in this bounded screen; absence of hits is not proof of priority. State catalogs and equivalent previously parametrized states remain a specific novelty question for the fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00007-p19/paper.pdf) · [TeX](projects/phys-00007-p19/manuscript/main.tex) · [Code / data](projects/phys-00007-p19) · [Author handoff](projects/phys-00007-p19/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00007-p19/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00016-p01 · Comment on “Ergotropy and entanglement in critical spin chains”</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | For this exact finite model, the published aligned work underestimates unrestricted extractable work and overestimates bound energy. A legal interaction among physical subsystem modes extracts extra work even while particle number and parity are conserved. The correction is small, approximately 15-31 ppm of aligned bound energy over N12-24; occupation alignment retains its explicit number-preserving Gaussian optimum meaning. No thermodynamic/CFT coefficient or experimental gain is claimed. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | For the exact open homogeneous H_N=-sum(c_j^dagger c_(j+1)+h.c.), N=4m, its unique half-filled ground-state marginal on the first l=N/2 sites and unrestricted U(2^l), the original universal equality E_pass=E_align=sum_j nu_desc,j epsilon_ascending,j is false. At N12 a legal number/parity-preserving swap between physical-mode kets {2,3} and {1,4}, after legal orbital alignment, reduces energy by strictly more than 6.71114703278e-7 J. The full N12 correction lies in (0.000001356396207356,0.000001356396207357) J. Analytic particle-hole excitation ordering proves equality at N4/N8, so N12 is the first failing N=4m. Complete certified finite-sort corrections are supplied at N16,20,24 and a quartic N12 extraction gate. No claim is made about all larger sizes, locality/control time, thermodynamic entropy scaling or source Eqs41/42. |
| **Предлагаемый вклад** | Exact rational actual-input N12 population inversion, explicit number/parity-preserving Fock-state swap and quartic mode gate; complete unrestricted/number/parity sorting through N24; analytic N4/N8 passivity identifies the first N=4m failure. The universal finite equality is false, with full N12 correction in (1.356396207356e-6,1.356396207357e-6) J. |
| **Ограничения / нерешённые трудности** | Fresh 2026-10-13 official original/successor/version reads and exact-title/arXiv/finite-spectrum/correction screens, primary PRB final and author-v2 Eq34, PRE generic examples/Theorem1, NJP full-sort/single-mode/AppendixB passages, and a 2026 ancilla theorem operation-set comparison. Same-date cached official update records reread without claiming refetch. No exhaustive forward-citation search, final-byte comparison of the NJP successor or guaranteed priority; novelty and significance await fresh referee/author scrutiny. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00016-p01/paper.pdf) · [TeX](projects/phys-00016-p01/manuscript/main.tex) · [Code / data](projects/phys-00016-p01) · [Author handoff](projects/phys-00016-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00016-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00029-p01 · A periodic planar counterexample to the Apollonian Ising temperature bound</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Maximum coordination alone does not enforce the proposed logarithmic Apollonian design ceiling in the unrestricted source graph class. Selectively concentrated uniform-J paths change the actual infinite-volume ordering threshold; any corrected ceiling needs a different bound or additional physical/geometric assumptions. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | For every bare uniform ferromagnetic J>0 and zero field, let Lambda_1024 retain every triangular-grid bond and put N1024 finite fan spins in each up triangle A=z,B=z+e1,C=z+e2, e1=(1,0),e2=(1/2,sqrt(3)/2), at x_j=z+(1/2,sqrt(3)/(6j)), adding A-x_j,B-x_j for every j,C-x_1,and x_(j-1)-x_j for j>=2, all with the same J and no duplicate bond. This is a simple connected locally finite periodic Euclidean triangulation with1025-site primitive cell and q_max2055. Its actual infinite-volume Ising transition obeys T_c(Lambda_1024)/J>2/log(11/10)>20, while the exact canonical Apollonian function defined in immutable source.md obeys T_c_star(2055)/J<=T_c_star(3072)/J<20. Hence the original all-periodic-planar uniform-J inequality T_c<=T_c_star(q_max) is false within its full stated premises. |
| **Предлагаемый вклад** | A concrete uniformly coupled Euclidean periodic fan with N1024 and qmax2055 satisfies T_c/J>20>T_c_star(2055)/J by strict exact certificates, disproving the original universal finite-q ceiling inside its premises. N1 is a reproduced prior baseline, not a claimed contribution. |
| **Ограничения / нерешённые трудности** | 13October2026 UTC current arXiv2605.10017 and2601.02502 version histories, current source full v2 HTML and final APS abstract, exact identifier/title/author counterexample-comment-correction searches, and nested/fan/parallel/decorated triangular neighbors. Relevant primary full texts of the two2026 sources and final EJP criticality paper are preserved/read at exact locators. Background abstracts and failed1993 publisher opener are labelled; no exhaustive worldwide priority or unread full-body graph equivalence claimed. The exact older decoration comparison remains a referee priority issue rather than an input to the proof. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00029-p01/paper.pdf) · [TeX](projects/phys-00029-p01/manuscript/main.tex) · [Code / data](projects/phys-00029-p01) · [Author handoff](projects/phys-00029-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00029-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00030-p01 · A finite nonreciprocal counterexample to a noise-matched current large-deviation bound</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The proved variance constraint cannot be extended to the proposed full rate-function shape merely by substituting its noise-matching psi_0 dissipation factor. Magnetic circulation and an intermediate reservoir reduce actual entropy per selected mean particle while the rare reversal count samples a much lower-chemical-potential reservoir. This obstructs that specific use of measured mean dissipation to constrain rare currents. Other single-current shapes and the joint-current conjecture remain untested. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | The exact curvature-matching universal assertion frozen in source.md and problem.md is refuted by the finite stationary normal 387-dot conductor in evidence/research/r1-tightbinding-model.md, with exact semi-infinite tight-binding leads (band \[0,40000\]epsilon), three fixed Fermi reservoirs at common T_ref>0 and mu=(5001,4997,4976)epsilon, n=128 filter branches of finite width 0.02epsilon, E0=5000epsilon and Hermitian flux-ring core Gamma_c=200000epsilon. For extracted lead-0 counting, J>0 and total physical sigma>0, j=-J is strictly inside the asserted domain, and I_0(-J)-B_psi0(-J)>0.019epsilon/h. A completed outward full-energy certificate encloses Delta=24J-chi_0(-24)-4sigma/k_B inside \[0.019447,0.024248\]epsilon/h, with actual width below 0.005. Exact psi_0>=1/2, B_psi(-J)=2sigma/(psi k_B), and Fenchel at s=-24 prove the rate-function gap without a rounded infimum or a numerical saddle. This resolves only the frozen formalization of the first proposed nonreciprocal extension; it does not refute the reciprocal theorem or variance bound or settle the joint-current alternative. |
| **Предлагаемый вклад** | A fixed physically realizable stationary finite 387-dot conductor with exact normal tight-binding leads, three fixed positive-temperature Fermi reservoirs and all-reservoir heat entropy yields a computer-assisted strict counterexample to the exact curvature-matching assertion frozen in source.md: I_0(-J)-B_psi0(-J)>0.019 epsilon/h. It uses the exact psi_0 definition through the proved conservative bound psi_0>=1/2, not a numerical minimizer or an ideal one-energy unitary array. |
| **Ограничения / нерешённые трудности** | Fresh bounded primary screen on 2026-10-13 at 19:51-19:53 UTC checked exact-title/identifier/conjecture/nonreciprocity/counterexample and Brandner-Saito rate-function successor terms. Current histories show 2507.01214v1,2502.07917v2,2607.06190v1; the exact final JPA conjecture and successor entropy distinction were reread from retained full primary documents. No exact later resolution was identified. This is not exhaustive priority certification; the target is our frozen curvature-matching interpretation of the first author speculation, not a formula quoted verbatim as a published theorem. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00030-p01/paper.pdf) · [TeX](projects/phys-00030-p01/manuscript/main.tex) · [Code / data](projects/phys-00030-p01) · [Author handoff](projects/phys-00030-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00030-p01/evidence/research/r3-README.md) · [Replay](projects/phys-00030-p01/reproducibility/README.md) |

**Связанные результаты / ранние версии**

- [phys-00032-p01](projects/phys-00032-p01): A finite nonreciprocal full-current large-deviation counterexample is not the resource-dependent three-port noise/entropy theorem. The target bound, observable and hypothesis sets differ.

</details>

<details>
<summary><strong>phys-00034-p01 · Replica twist entropy fails strong monotonicity under fermionic Gaussian measurements</strong> — Опровержение · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Replica twist entropy cannot be used as a strong monotone to upper-bound average pure-state Gaussian resource-conversion yield. Its source diagnostic and dynamical properties are unaffected. This gives an exact operational limitation for the actual high-order two-copy observable, including fermion-parity and graded-copy constraints. |
| **Исходная задача** | опровергнута в указанной области |
| **Результат и точная область утверждения** | In the fixed-parity finite-mode graded-CAR model of problem.md, replica twist entropy at alpha=pi/4 is not a strong pure-state Gaussian monotone. The normalized even-parity N=34 state sqrt(3)/2 &#124;00>&#124;0000>^tensor8 + 1/2 &#124;11>\[(&#124;0000>+&#124;1111>)/sqrt(2)\]^tensor8 followed by occupation measurement of its first mode, retaining both outcomes with probabilities 3/4 and 1/4, has exact average increase log(25836385/25165824)>0. More generally the explicit N=4m+2 flagged family has the exact all-angle formula in evidence/flagged-twist-proof.md and, at every fixed 0<alpha<pi/2 and 0<q<1, violates strong monotonicity for sufficiently large finite m with unbounded average increase as m grows. |
| **Предлагаемый вклад** | An exact fixed-parity fermionic family N=4m+2 has F=p^2+q^2 f(alpha)^m+2pq K_m(alpha), with explicit f and K. At alpha=pi/4, m=8,q=1/4 gives a finite N=34 two-outcome violation Delta=log(25836385/25165824)>0. For every fixed interior angle, parent P remains bounded but average measured-branch P grows linearly with m. |
| **Ограничения / нерешённые трудности** | Current primary version records and targeted defining/proof sections rechecked 2026-10-14, including the newly identified current bridge-degree v2 and stabilizer counterexample v2/v3. Existing covariance and convolution comparisons retained. Bounded search cannot certify priority; candidate_novel is a proposer hypothesis for fresh review, not acceptance. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00034-p01/paper.pdf) · [TeX](projects/phys-00034-p01/manuscript/main.tex) · [Code / data](projects/phys-00034-p01) · [Author handoff](projects/phys-00034-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00034-p01/reproducibility/README.md) |

</details>

## Частичный результат

<details>
<summary><strong>phys-00002-p01 · How much noise does a qubit need?</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Генераторы Линдблада описывают марковскую динамику открытых систем. Может ли один оператор скачка достичь всей границы области переноса населённостей кубита? |
| **Результат и охват исходной задачи** | Сертифицирована локальная оптимальность в области конечного радиуса около стационарной точки a=1/2 с одним скачком против возмущений ранга не выше двух. Исходная глобальная задача остаётся открытой. |
| **Предлагаемый вклад** | Явный интервальный сертификат превращает численно найденную стационарную точку в проверяемую локальную область исключения конкурирующих генераторов. |
| **Ограничения** | Локальный радиус 10^-4; результат не устанавливает глобальную границу вложимости и не исключает удалённые конкурирующие решения. |
| **PDF и исходники** | [PDF](projects/phys-00002-p01/paper.pdf) · [TeX](projects/phys-00002-p01/manuscript/main.tex) · [Bib](projects/phys-00002-p01/manuscript/references.bib) · [Код / данные](projects/phys-00002-p01) · `python reproducibility/reproduce.py --project phys-00002-p01` |

</details>

<details>
<summary><strong>phys-00007-p01 · When channel boundariness multiplies exactly</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | Граничность характеризует близость к границе выпуклого множества каналов. Тензорные произведения могут выявлять структуру, незаметную для одной копии. |
| **Результат и охват исходной задачи** | Точная мультипликативность доказана внутри явного двухпараметрического семейства полноранговых неунитальных матриц Чои кубитных каналов при &#124;s&#124;, &#124;t&#124; ≤ 1/5. |
| **Предлагаемый вклад** | Символьные проверки Чои, Штурма и LDL подтверждают явное семейство, в котором оптимум тензорного произведения поддаётся точному анализу. |
| **Ограничения** | Общая задача остаётся открытой. Историческая проверка пакета для подачи выявила несоответствие привязки доказательств к рукописи; PDF включён как архивный черновик, а не как выпуск, прошедший эту проверку. |
| **PDF и исходники** | [PDF](projects/phys-00007-p01/paper.pdf) · [TeX](projects/phys-00007-p01/manuscript/main.tex) · [Bib](projects/phys-00007-p01/manuscript/references.bib) · [Код / данные](projects/phys-00007-p01) · `python reproducibility/reproduce.py --project phys-00007-p01` |

</details>

<details>
<summary><strong>phys-smallmac00000-p13 · Finite total dephasing and an isolated natural occupation in an open XX chain</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 开放 XX/XY 链加入最小可控非均匀耗散后，哪些耗散剖面仍允许协方差矩阵谱的闭式表达？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the open XX spin chain and stationary covariance specified in problem.md, odd N with centered dephasing defect, J=1, kappa=4, mu=1/2, eta=5, and either gamma_0=c/N or c/(N-1), every fixed finite c>0 has nearest natural-occupation spacing from 1/2 tending to 1/(36+4c) and central-orbital IPR tending to 51/125 as stationarity is taken before N tends to infinity. Explicit finite bounds (A),(B) are in evidence/salvage-aefa2c1a93e3/bounded-noise-derivation.md. No claim about a Liouvillian gap, full-state Gaussianity, experiment, or the full XX/XY profile classification. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00000-p13/paper.pdf) · [TeX](projects/phys-smallmac00000-p13/manuscript/main.tex) · [Code / data](projects/phys-smallmac00000-p13) · [Author handoff](projects/phys-smallmac00000-p13/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00000-p13/manuscript/repro/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00000-p14 · A second-order obstruction to localized edge-mode continuation in a non-Hermitian interacting Kitaev chain</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 非厄米相互作用 Kitaev 链在已知可解区域之外，能否得到一个新的精确相边界、例外点条件或反例？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | At t=1, g=(1-i)/5, eta=1/5, mu=0 on the original odd-left-dimerized half-line, Q0=sqrt(1-rho^2) sum_(n>=0) rho^n alpha_(2n+1), rho=3(1-i)/10, has a unique exponentially localized parity-odd normalized first-order continuation Q1. No exponentially localized Q2 solves \[H0,Q2\]=-\[V,Q1\]. Thus there is no twice-differentiable exact commutator-zero-mode continuation from Q0 whose first two Taylor coefficients are exponentially localized and whose square normalization holds to first order. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00000-p14/paper.pdf) · [TeX](projects/phys-smallmac00000-p14/manuscript/main.tex) · [Code / data](projects/phys-smallmac00000-p14) · [Author handoff](projects/phys-smallmac00000-p14/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00000-p14/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00004-p01 · Optimal single-letter private information of the dephrasure channel on a noise interval</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 退相位—擦除信道：对称双混合态编码是否已经达到单字母私有信息最优？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For every p in \[27/250,221/2000\] and q=3p, and every finite ensemble of legal qubit density matrices with arbitrary nonnegative normalized weights and arbitrary mean, the full-environment dephrasure private information obeys Pi(E)<=B(p)-(3/250)Var_w(z_a)-(1/1000)(sum_a w_a z_a)^2, where z_a=Tr(Z rho_a) and B is the immutable source symmetric-code maximum. In particular P^(1)(N_p,3p)=B(p) on this subinterval. The rest of the original p interval and regularized private capacity remain unresolved. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00004-p01/paper.pdf) · [TeX](projects/phys-smallmac00004-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00004-p01) · [Author handoff](projects/phys-smallmac00004-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00004-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00003-p02 · A rank-three projection bound for the quantumness of spin-1 states</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | spin-1混合态：相干态凸包距离是否受同最小Bloch本征值的纯态控制？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | The rank3 nearest-Bloch projection bound Q<=sqrt(3/8)(-lambda), equality iff its unit kernel vector has v0=0, and consequent restriction of any source Eq41 counterexample to rank2 nearest Bloch matrices. Ranks concern the 4x4 real moment matrix of the unique closest state in the complete spin-coherent hull. The source all-state inequality is unresolved; zero-dipole formulas are illustrative corollaries and rank2 exploratory formulas are outside the claim. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00003-p02/paper.pdf) · [TeX](projects/phys-smallmac00003-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00003-p02) · [Author handoff](projects/phys-smallmac00003-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00003-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00007-p03 · A two-pineapple envelope for split-core threshold random walks</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 阈值输运网络中，单核心菠萝结构是否已经最慢？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For every positive integer s,q,t, put n=s+t+q+3. In the frozen non-lazy threshold-graph random-walk model, each construction code 01 0^t 1^s 0^q 1 and 0 1^s 0^t 1 0^q 1 has Kemeny's constant strictly less than max{F_n(s+1),F_n(s+t+1)}, and hence strictly less than or equal to the global pineapple bound B_n. The original conjecture for all legal threshold codes remains unresolved. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00007-p03/paper.pdf) · [TeX](projects/phys-smallmac00007-p03/manuscript/main.tex) · [Code / data](projects/phys-smallmac00007-p03) · [Author handoff](projects/phys-smallmac00007-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00007-p03/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00010-p01 · Exact flat-noise transition rays from Hadamard involutions in four-level systems</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 四能级酉跃迁掺入均匀噪声后，能否总由另一个单次酉跃迁实现？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For any order n with a real normalized Hadamard F and any real orthogonal projector P, U=F(I-2P) has the exact flat-noise transition ray &#124;V_lambda,ij&#124;^2=(1-lambda)&#124;U_ij&#124;^2+lambda/n for every lambda in \[0,1\], with V_lambda=sqrt(1-lambda)U+i sqrt(lambda)F unitary. Within this fixed real quadrature ansatz the condition is also necessary: F^T U is a symmetric orthogonal involution. At n=4 the rank-two projector component contains a locally four-dimensional image of noncirculant B(U) matrices. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00010-p01/paper.pdf) · [TeX](projects/phys-smallmac00010-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00010-p01) · [Author handoff](projects/phys-smallmac00010-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00010-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00010-p04 · A seven-$T$ fixed measurement accessing 220 four-qubit Pauli directions</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 四qubit的单设置完整层析，七个T门是否仍然不够？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the explicitly specified fixed four-input-qubit, seven-&#124;0>-ancilla Clifford+T circuit in evidence/seven-t-witness.json, using seven T or T-dagger gates and retaining all 2048 terminal computational-basis outcomes, the effective POVM operator span and frame have exact real rank 220. The original universal seven-T informational-incompleteness question remains unresolved. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00010-p04/paper.pdf) · [TeX](projects/phys-smallmac00010-p04/manuscript/main.tex) · [Code / data](projects/phys-smallmac00010-p04) · [Author handoff](projects/phys-smallmac00010-p04/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00010-p04/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00010-p02 · Weak regulation increases stationary abundance noise in a three-species stochastic feedback ring</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三组分随机生化反馈环，是否至多一个组分能低于Poisson噪声？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the exact infinite-state three-species unit-birth feedback ring with fixed a_i,tau_i>0 and bounded nonconstant h_i:N_0->R, put f_i(n)=a_i+epsilon h_i(n). For &#124;epsilon&#124; H_k<=a_k/2, each stationary Fano factor obeys F_i(epsilon)-1=epsilon^2 S_i/a_i+R_i(epsilon), where S_i=integral_0^infty exp(-t/tau_i) Cov_0(h_i(Y_{i-1}(0)),h_i(Y_{i-1}(t)))dt>0, Y_{i-1} is a stationary baseline immigration-death chain, and &#124;R_i(epsilon)&#124;<=K_i&#124;epsilon&#124;^3 for the explicit finite K_i in evidence/research-pass3.md. Consequently all three F_i>1 for each fixed triple at sufficiently small nonzero epsilon. No claim is made for arbitrary coupling strength; the original conjecture remains unresolved. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00010-p02/paper.pdf) · [TeX](projects/phys-smallmac00010-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00010-p02) · [Author handoff](projects/phys-smallmac00010-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00010-p02/REPRODUCE.md) |

**Связанные результаты / ранние версии**

- [phys-00018-p01](projects/phys-00018-p01): The two-gene finite-RNA-lifetime matched-baseline theorem is not the three-species direct-abundance feedback-ring weak-regulation result. The intermediate RNA state, number of species, baseline and whole-space remainder are different.

</details>

<details>
<summary><strong>phys-smallmac00011-p02 · Directional stability of the reverse-depolarizing entanglement-assistance benchmark for qubit entanglement-breaking channels</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 完全破坏纠缠的 qubit 信道，预共享纠缠的容量增益是否仍不超过已知反向去极化基准？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | Let D be the reverse-depolarizing qubit channel D_(4/3), and let Psi be any fixed qubit entanglement-breaking channel. For Phi_e=(1-e)D+e Psi as e decreases to zero through positive values, put c=<Omega&#124;J_Psi/2&#124;Omega>. If c>0, then K_* chi(Phi_e)-C_E(Phi_e)=c e log2(1/e)+O_Psi(e). If c=0, Psi has Bloch action r -> -Q r with Q positive semidefinite and trace one, and the gap is \[K_*/2\](lambda_max(Q)-1/3)e+O_Psi(e^2). The gap is strictly positive for all sufficiently small e>0 whenever Psi differs from D; if Psi=D, equality holds identically. All capacities are fully optimized and C=chi for these EB maps. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00011-p02/paper.pdf) · [TeX](projects/phys-smallmac00011-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00011-p02) · [Author handoff](projects/phys-smallmac00011-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00011-p02/manuscript/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00012-p02 · A hypocycloid spectral bound for circulant unistochastic matrices without symmetric amplitudes</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 五站点环的转移概率具有平移对称性，是否总能选择同样对称的酉实现？ |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | Let d>=2 and let B be a d-by-d circulant bistochastic matrix with B\[i,j\]=b\[(i-j) mod d\]. If B\[i,j\]=&#124;U\[i,j\]&#124;^2 for some arbitrary U in U(d), then for every Fourier mode k, lambda_k(B)=tr(D_k U D_k^dagger U^dagger)/d belongs to the closed unit d-hypocycloid H_d. For d=5, the circulant matrix generated by b=(209/500,3/40,7/500,3/40,209/500) satisfies every row and column bracelet inequality but is not unistochastic, because lambda_1=((465+343*sqrt(5))/2000) exp(i*pi/5) lies strictly outside H_5. Consequently, a five-hypocycloid violation cannot supply the general-unitary-versus-circulant-unitary separator required to disprove P_5. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00012-p02/paper.pdf) · [TeX](projects/phys-smallmac00012-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00012-p02) · [Author handoff](projects/phys-smallmac00012-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00012-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00019-p01 · Exact signed-sum spectral locus of a six-term three-qubit Pauli Hamiltonian</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三比特 Pauli 模型出现自由费米谱的完整耦合流形 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For every real coupling vector (a,b,c,d,e,f), the eight-level spectrum of H=a Z_2+b Y_1 X_2+c X_1 Y_2+d Z_1 Y_3+e Y_1 X_3+f Z_3 is, with multiplicity, the signed-sum spectrum of three nonnegative one-particle energies if and only if c d (a^2-f^2)(b^2-e^2)=0; equivalently the locus is exactly c=0, d=0, a=plus-or-minus f, or b=plus-or-minus e. This claim is spectral and does not claim a uniform structural CAR-mode construction. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00019-p01/paper.pdf) · [TeX](projects/phys-smallmac00019-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00019-p01) · [Author handoff](projects/phys-smallmac00019-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00019-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00020-p01 · The largest Liouvillian exceptional point need not maximize the spectral gap: An exact two-qubit counterexample</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 固定两比特 XYZ Liouvillian 的谱隙最优耗散是否落在最大例外点 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the fixed two-qubit XYZ GKSL generator in problem.md with gamma=3/5, Delta=2/5, and Gamma>0, the complete nonzero Liouvillian spectral gap satisfies g(73/10)>3/2>1>g(8). Since the reproduced largest positive Liouvillian exceptional point is Gamma_cr=8, Gamma=8 is not a global maximizer of g. The actual global maximizer is not determined by this claim. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00020-p01/paper.pdf) · [TeX](projects/phys-smallmac00020-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00020-p01) · [Author handoff](projects/phys-smallmac00020-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00020-p01/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00020-p02 · Strict separable non-saturation for a seven-state prepare-and-measure witness</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 最小绝对纠缠集见证的可分上界能否严格低于四分之三 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the exact seven-state extended ensemble and prepare-and-measure witness of arXiv:2609.13075v1 Sec. VI.D in the two-qubit separable-preparation domain, Q_SEP is strictly smaller than 3/4. This result proves non-saturation but neither computes Q_SEP nor supplies an explicit numerical lower bound on the positive gap. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00020-p02/paper.pdf) · [TeX](projects/phys-smallmac00020-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00020-p02) · [Author handoff](projects/phys-smallmac00020-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00020-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00021-p02 · A unique cubic-coupling cancellation locus for collinear constant-vorticity capillary–gravity triads</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 常涡度共振三波的涡度公式与耦合零点符号审计 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | In the reproduced Ivanov-Martin arXiv:1911.05213v1 co-propagating cubic model, for every g>0, sigma>0 and distinct k1,k2>0 with k3=k1+k2, the unrestricted real dispersion-plus-resonance system has exactly the two common-sign frequency solutions in Eq. (3) of evidence/resonance-classification.md, related by (omega_j,gamma)->(-omega_j,-gamma). With q_j=k_j(g+sigma*k_j^2), ell=q3-q1-q2, N=ell^2-4q1q2 and D=2ell\[q3^2-(q1-q2)^2\], the selected positive-frequency sheet has the unique physical vorticity gamma=-N/sqrt(D); the companion root belongs to the genuine all-negative-frequency sheet, not an algebraic artifact. On either sheet C=\[16q1q2(q3-q1)(q3-q2)-ell^4\]/D. For every positive pair (k1,k2), exactly one positive r=g/sigma makes C=0, namely the unique positive root of Eq. (9) in the proof; at that zero gamma<0 on the positive-frequency sheet and gamma>0 on its sign-reversed companion. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00021-p02/paper.pdf) · [TeX](projects/phys-smallmac00021-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00021-p02) · [Author handoff](projects/phys-smallmac00021-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00021-p02/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-smallmac00021-p03 · Comment on “Band topology of the breathing kagome lattice”</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Breathing-kagome 角态的 A 子晶格公共核 iff 扰动判据 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the Fig. 3 interpolation of Geschner et al. at t=0 and t'=1, the author-raster 15-site invariant corner component has chi(E,lambda)=(E-1)^2 P6(E,lambda)P7(E,lambda), coefficient gcd exactly (E-1)^2 in Q\[E\], chi(E,0)=E(E-1)^8(E+1)^4(E+2)^2, and chi(E,1)=(E-1)^8(E+1)^6(E+2). Thus exactly 13 eigenvalue roots per corner, counted with algebraic multiplicity, are nonconstant under the interpolation, correcting the source's count 12; the three pairwise-disjoint D3-related components verified in the N=20 flake give 39 rather than 36. Secondarily, for the separate t=0.1, t'=1 N=20 system, the previously certified opposite-mirror-parity crossing and exact uniform-edge transfer equations remain at their finite/restricted scopes. No thermodynamic result or solution of the original general connectivity iff is claimed. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00021-p03/paper.pdf) · [TeX](projects/phys-smallmac00021-p03/manuscript/main.tex) · [Code / data](projects/phys-smallmac00021-p03) · [Author handoff](projects/phys-smallmac00021-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00021-p03/README_REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00022-p01 · Local stability of a two-copy entanglement-of-purification ansatz at the von Neumann boundary</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 经典二比特态在冯诺依曼阶的二副本纯化局部稳定性 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the Eq. (15) state rho_r at r=1/2 and base-2 von Neumann order alpha=1, in the fixed minimal ancillary split (d_A',d_B')=(4,4), the product-canonical two-copy purification W_0=I_16 is a strict local minimum modulo the local ancillary U(4) x U(4) orbit over the complete complex orthonormal-flag manifold U(16), including support-opening directions. This does not assert global optimality, larger-ancilla local stability, or additivity. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00022-p01/paper.pdf) · [TeX](projects/phys-smallmac00022-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00022-p01) · [Author handoff](projects/phys-smallmac00022-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00022-p01/manuscript/README.md) |

**Связанные результаты / ранние версии**

- [phys-00004-p09](projects/phys-00004-p09): Both concern two-copy binary-state entanglement of purification. big_mac proves pathwise positivity for every positive nonproduct binary table without a common neighborhood; small_mac proves a full U(16) strict local minimum modulo gauge at r=1/2. Neither recorded statement contains the other complete statement. Keep both, link them, and do not infer global additivity.

</details>

<details>
<summary><strong>phys-smallmac00022-p02 · Exact Tsirelson bound for a three-output Bell functional</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 三输出 Bell 泛函 I3 的精确 Tsirelson 证书与等号刚性 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the no-dagger three-output Bell functional I3 of arXiv:2606.21362v3 Eq. (6), every tensor-product strategy of arbitrary local dimension with three-output projective measurements satisfies I3<=4. The bound is attained by the stated maximally entangled qutrit strategy. Equivalently, 4*1-I3 has the submitted exact rank-16 Q(omega) noncommutative SOS on the 35-word 1+AB span. Equality rigidity, self-testing, robustness and randomness certification are not claimed. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00022-p02/paper.pdf) · [TeX](projects/phys-smallmac00022-p02/manuscript/main.tex) · [Code / data](projects/phys-smallmac00022-p02) · [Author handoff](projects/phys-smallmac00022-p02/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00022-p02/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-smallmac00022-p03 · Exact all-parameter spectral-gap certificates for deformed-EPR Hamiltonians on small subdivided stars</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 树上变形 EPR 哈密顿量的谱隙下界与等号分类 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | Let T_q be the tree with q ordinary leaves adjacent to C and two further edges C--A--B. For every q in {1,2,3,4,5,6} and every real 0<s<1, the coefficient-one Hamiltonian H_s=-sum_e (&#124;00>+s&#124;11>)(<00&#124;+s<11&#124;)_e has finite-volume spectral gap Delta(T_q,s)>1-s^2. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00022-p03/paper.pdf) · [TeX](projects/phys-smallmac00022-p03/manuscript/main.tex) · [Code / data](projects/phys-smallmac00022-p03) · [Author handoff](projects/phys-smallmac00022-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00022-p03/reproducibility/README.md) |

**Связанные результаты / ранние версии**

- [phys-00035-p01](projects/phys-00035-p01): The small_mac result is an all-s certificate for q=1..6 one-hub subdivided stars. big_mac proves a full-gap, tail-controlled two-hub family for k>=100 in eta=theta/k, theta in [1/2,2]. Different topology, size and parameter quantifiers; neither is an all-graph proof.

</details>

<details>
<summary><strong>phys-00002-p08 · A resource obstruction for qubit measurement self-testing with matched kernel preparations</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Reweighting all probabilities at the established four matched-exclusion-state reference cannot reduce auxiliary settings from three to two. Any such reduced-resource protocol must depart from those reference preparations or change the physical resources/premises. The obstruction addresses target-only certification, not merely separate state self-testing. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For any extremal four-outcome complex-qubit reference POVM with four matched pure kernel-state preparations, and any binary auxiliary collection whose reference observable Bloch vectors span a space of dimension at most two, every real linear functional on the complete prepare-and-measure probability table that is globally maximized at that reference has an admissible maximizing realization with the same auxiliary measurements and a target having at most three nonzero effects. Thus no such witness self-tests the four-outcome target, even when only the target is to be certified. This includes two projective auxiliaries and two arbitrary binary POVMs. The reference kernel-state restriction is essential to the claimed scope; the unrestricted resource conjecture remains unresolved. |
| **Предлагаемый вклад** | Necessary supporting-witness normal form c_ij=l_i-k_j delta_ij with k_j>=0 for arbitrary target probability coefficients at any four matched kernel-state reference; using it, a universal explicit <=3-nonzero-effect same-score target replacement whenever the auxiliary Bloch span has dimension<=2. Includes arbitrary binary POVMs and zero auxiliary-state-gradient cases; original unrestricted minimality remains unresolved. |
| **Ограничения / нерешённые трудности** | Fresh primary screen2026-10-12UTC before legacy extension:2406.08661v1/current official record;2020 publisher fulltext;2306.07248v5 including official2025-11-01 revision;2306.00730v4;2603.01802v1;2503.13282v2/current2026-07-01 revision. Exact-ID and minimal/two/four-outcome/antipodal/state-exclusion/lower-bound searches. No equivalent result identified in checked passages; bounded screen, incomplete forward-citation coverage, no proof of priority or unrestricted openness. Novelty/significance remain for fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00002-p08/paper.pdf) · [TeX](projects/phys-00002-p08/manuscript/main.tex) · [Code / data](projects/phys-00002-p08) · [Author handoff](projects/phys-00002-p08/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00002-p08/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00002-p12 · Sharp lower bounds on current cumulant ratios in Markov rings with an irreversible bond</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Validates the proposed third/fourth current-ratio transport diagnostics throughout an irreversible-bond classical single-cycle class, including strong backward excursions elsewhere. It identifies a rigorously safe boundary sector; all-positive finite-affinity universality remains unresolved. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For every finite simple nearest-neighbor time-homogeneous Markov ring with N>=3, finite forward rates u_i>0, nonnegative finite reverse rates w_i and at least one w_i=0, the long-time signed one-cycle count cumulant rates satisfy c3/c1>=-1/16 and c4/c2>=-(1+sqrt(5))/10. Here c1,c2>0; arbitrary initial law and any counted bond yield the same ratios. Both constants are sharp over unbounded finite N. The original strictly positive bidirectional conjecture remains unresolved; no finite-N extremizer or interior bound is asserted. |
| **Предлагаемый вклад** | An ansatz-free analytic proof of both winding-ratio lower bounds for every positive exponential-stage vector, mapped by the known passage-time theorem to every finite Markov ring with at least one irreversible bond and arbitrary remaining backward rates. Both constants are asymptotically sharp. |
| **Ограничения / нерешённые трудности** | Targeted primary/current recheck on 2026-10-12, arXiv latest v4 and exact Appendix, author Fill theorem/remark, prior 2023 modular and 2025 heat/entropy neighbors, exact constants with proof/erratum/renewal/hypoexponential searches. No direct priority conflict found; this is bounded coverage, not a priority guarantee. Fresh referee must assess novelty and significance of proof upgrade. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00002-p12/paper.pdf) · [TeX](projects/phys-00002-p12/manuscript/main.tex) · [Code / data](projects/phys-00002-p12) · [Author handoff](projects/phys-00002-p12/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00002-p12/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00002-p13 · Sharp first-passage skewness and excess-kurtosis bounds for three-state cycles at large affinity</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Replaces rate-space numerical maximization by algebraic sharp limits on entropy-threshold timing asymmetry and excess tails in three-step dissipative cycles. Identifies an attaining half-affinity tilted-spectrum degeneracy and allows direct envelope evaluation at fixed dissipation. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the strictly positive finite-rate time-homogeneous N=3 periodic Markov ring and the large-threshold entropy-current FPT conventions of problem.md, at every finite A>=log(64), the separate sharp envelopes are U_S=sqrt(A) N(p_S)/V(p_S)^(3/2) and U_K=A Q(p_K)/V(p_K)^2. Here d=coth(A/4), H=(d^2+1)/(2d), t(p)=d p(2+p)/(1+2p)^2, zeta(p)=d^2 p^2/(1+2p)^3, V=H-2t, N=3H^2-1-6Ht+6zeta, and Q=3H(5H^2-3)-12(3H^2-1)t+12Ht^2+24Hzeta. p_S is the unique positive root of 4(d^2-1)p^2+(12d^2-4)p-(d^2-1)^2=0; p_K is the unique positive root of 8(d^2-1)p^3+(-4d^4+24d^2-12)p^2+(2d^4+12d^2-6)p-(d^2-1)^2(d^2+1)=0. Both bounds are attained by strictly positive finite rate vectors constructed in spectral-envelope-proof.md Section 5. This does not settle the original all-N/all-affinity problem or the kink locations. |
| **Предлагаемый вклад** | Exact sharp upper envelopes for both large-threshold scaled FPT skewness and scaled excess kurtosis for every strictly positive three-state ring at every finite A>=log(64). They are specified by unique positive quadratic/cubic roots in d=coth(A/4), and explicit strictly positive rate vectors attain each bound. |
| **Ограничения / нерешённые трудности** | Current primary arXiv history/HTML 2110.14540 and exact-claim/later-resolution searches rechecked 2026-10-12 before extension. Compared retained 1510.03279v1, full 2204.08421v4 definitions/Section III E/Appendix A, and 2025 JSP 192,126 publisher fulltext definitions. No equivalent envelope found in this bounded screen. Publisher version of the 2021 source and exhaustive citation tracking remain incomplete; priority is proposed, not certified. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00002-p13/paper.pdf) · [TeX](projects/phys-00002-p13/manuscript/main.tex) · [Code / data](projects/phys-00002-p13) · [Author handoff](projects/phys-00002-p13/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00002-p13/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00003-p07 · Uniform indexed spectral bounds near the five-photon resonance of the quantum Rabi model</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Certifies how the avoided-crossing lower branch stays below the conjectured indexed ceiling when the leading diagonal margin vanishes. Gives a rigorous gap envelope with relative error <=G/(3kappa), below 19.5% at G=0.1 and improving as G->0; no optical selection-rule or transfer-rate claim. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | In the exact unbiased quantum Rabi model of problem.md, write G=g/omega,d=Delta/omega,e_n^s=E_n^s/omega with omega>0. For every 0<G<=1/10 and -1<=c<=1, d=5/2-(5/4)G^2+cG^4 implies e_2^+<5/2-G^2. On d=5/2-(5/4)G^2-(5/64)G^4, the sorted full-operator levels satisfy &#124;e_2^+-(5/2-G^2-sqrt120*G^5/64)&#124;<=G^6/3 and &#124;e_3^+-(5/2-G^2+sqrt120*G^5/64)&#124;<=G^6/3. Delta sign reversal exchanges parity. No all-n, opposite-parity, universal spacing, exact-stationarity or experimental transition claim. |
| **Предлагаемый вклад** | Explicit continuous-domain certificate for the sorted n=2 plus-parity upper bound near the five-photon resonance, with infinite-tail and index control; on fourth-order tuning, two indexed eigenvalue enclosures with uniform absolute error G^6/3 for 0<G<=0.1. No novelty claimed for the known sqrt(5!)/64 coefficient or the resonance mechanism. |
| **Ограничения / нерешённые трудности** | Primary v3 and current abstract rechecked 2026-10-12; exact identifier/title plus proof/resolution queries and weak-coupling/five-photon/Bloch-Siegert neighbors. Springer 2026 small-gap successor and arXiv:2608.09562v1 Sec.5 checked. No verified later global resolution or matching explicit uniform certificate; priority is not exhaustive and novelty/significance require fresh referee assessment. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00003-p07/paper.pdf) · [TeX](projects/phys-00003-p07/manuscript/main.tex) · [Code / data](projects/phys-00003-p07) · [Author handoff](projects/phys-00003-p07/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00003-p07/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00003-p10 · Weak periodic phase shaping lowers the worst-case sensitivity of coherent-state qubit readout</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Rules out all fixed weak periodic same-axis phase shaping, including multiharmonic and discontinuous profiles, as an infinitesimal route to improving the established uniform single-mode qubit readout. Any improvement must evade this restricted perturbative conclusion. No improved interaction, hardware benefit or unrestricted optimum is asserted. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | In the one-real-coherent-mode, fixed-ground-state-qubit, alpha-independent-unitary, qubit-only SLD-QFI model of source.md/problem.md, for every fixed L>0 and fixed real bounded Borel L-periodic function g nonconstant almost everywhere, set V_epsilon=exp\[-i sigma_y(Q/sqrt(2)+epsilon g(Q))\]. There exists epsilon0(g,L)>0 such that for every real epsilon with 0<abs(epsilon)<epsilon0, of either sign, the outputs are uniformly full rank and inf_{alpha in R} F_Q\[rho_epsilon(alpha)\]<4/e. Explicitly epsilon0=min(h/M,gamma/(2KM^2)), where M bounds abs(g), G is the exact first-variation response, gamma=min(-min G,max G)>0, and h,K are the uniform-rank/remainder constants in evidence/research/periodic-variation-proof.md. Constant g preserves 4/e. The profile and period are fixed before taking epsilon small; no common radius, norm-neighborhood maximum, finite-strength no-go or unrestricted optimum is asserted. |
| **Предлагаемый вклад** | A restricted exact directionwise obstruction: for every one fixed real bounded Borel periodic phase profile g, nonconstant almost everywhere, f_epsilon(x)=x/sqrt(2)+epsilon g(x) has inf over every real alpha of qubit QFI strictly below 4/e for both sufficiently small signs of epsilon. The radius depends on the profile and period. Explicit first-variation Fourier multipliers have no nonzero-frequency nulls; uniform full rank and a quadratic remainder establish the continuum conclusion. |
| **Ограничения / нерешённые трудности** | Checked current official arXiv:2509.22361 history and full v2 primary Sections III.1 and III.6 on 2026-10-12; no later version listed. Existing full publisher and preprint sources and preprocessing/compression/repeated-query neighbors were read at their decisive premises. Current exact-title/identifier/author, coherent/qubit/worst-case/Fisher, 4/e/nonlinear and Gaussian/minimax/qubit/encoding searches identified no checked primary reporting this obstruction. Absence of hits is not priority proof. The source's in-preparation reference remains inaccessible and could affect novelty; fresh independent significance/novelty review remains required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00003-p10/paper.pdf) · [TeX](projects/phys-00003-p10/manuscript/main.tex) · [Code / data](projects/phys-00003-p10) · [Author handoff](projects/phys-00003-p10/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00003-p10/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00004-p09 · Positive pathwise entropy curvature at the canonical two-copy purification of a binary classical state</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Every fixed non-gauge exponential auxiliary-unitary direction increases the purification entropy for sufficiently small nonzero parameter in this split. Infinitesimal descent cannot provide collective preparation savings there; finite-distance or larger-split mechanisms remain possible. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For every strictly positive normalized binary probability table P with det(sqrt(P)) nonzero, consider the canonical two-copy purification in the fixed auxiliary split R=S=C^4 and U(t)=exp(i t H) on RS. On the 112-real-dimensional Hermitian-generator subspace with no first-order null-to-null Schmidt block, S(AR;t)=2 h2((1+sqrt(1-4 det(sqrt(P))^2))/2)+c_P(H)t^2+o(t^2). The exact quadratic form c_P is nonnegative with kernel precisely H=H_R tensor I+I tensor H_S, a 31-dimensional local auxiliary-unitary gauge. Thus its 81-dimensional quotient is strictly positive. The phase sector has the explicit sum-of-squares form and the controlled-rotation sectors the graph-Laplacian forms in quadratic-form.md. Outside this subspace, the positive leading t^2 log(1/t^2) coefficient implies entropy increase along every fixed non-gauge exponential-unitary path for sufficiently small nonzero t. This does not assert a common quantitative neighborhood, global additivity, boundary/product-table coverage, or a result for larger auxiliary splits. |
| **Предлагаемый вклад** | Exact entropy quadratic form on the 112-dimensional no-first-order-Schmidt-rank-growth auxiliary-generator space at the canonical two-copy purification; its quotient by 31 local auxiliary-unitary gauge directions is strictly positive in all 81 remaining dimensions for every strictly positive nonproduct binary probability table in R=S=C^4. |
| **Ограничения / нерешённые трудности** | Primary records and relevant full-text locations checked 2026-10-12 before continuation, plus exact claim/local-curvature/local-additivity queries. August 2608.28897v1, October 2610.03630v1, norm-compression 2410.21961v4, and related 1105.6122 and 2111.11385v4 were screened. Bounded coverage cannot certify priority; a fresh referee must assess possible constrained variants and significance. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00004-p09/paper.pdf) · [TeX](projects/phys-00004-p09/manuscript/main.tex) · [Code / data](projects/phys-00004-p09) · [Author handoff](projects/phys-00004-p09/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00004-p09/reproducibility/README.md) |

**Связанные результаты / ранние версии**

- [phys-smallmac00022-p01](projects/phys-smallmac00022-p01): Both concern two-copy binary-state entanglement of purification. big_mac proves pathwise positivity for every positive nonproduct binary table without a common neighborhood; small_mac proves a full U(16) strict local minimum modulo gauge at r=1/2. Neither recorded statement contains the other complete statement. Keep both, link them, and do not infer global additivity.

</details>

<details>
<summary><strong>phys-00007-p09 · Local robustness of commuting-reflection encoding near the three-qubit W state</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Eight perfectly distinguishable messages from coordinated commuting product reflections remain possible under arbitrary sufficiently small pure-state perturbations of W3, with joint decoding. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | There exist epsilon>0 and C<infinity such that every normalized complex three-qubit pure-state ray with phase-fixed chart psi=(W3+eta)/sqrt(1+&#124;&#124;eta&#124;&#124;^2), <W3&#124;eta>=0, &#124;&#124;eta&#124;&#124;<epsilon admits a commuting-reflection encoding with the triangle graph and a local SU2 change V(theta)=exp(-i theta.sigma/2)q^tensor3 satisfying &#124;&#124;theta&#124;&#124;<=C&#124;&#124;eta&#124;&#124;^(1/3). On psi(t)=(W3+t delta)/sqrt(1+13t^2), delta=V0^dag O V0 W3, an exact branch has theta=s v1+O(s^2), t=(40ab/39)s^3+O(s^4), whereas no C1 branch through V0 exists. No universal claim away from the neighborhood or numerical radius is asserted. |
| **Предлагаемый вклад** | An exact open neighborhood of arbitrary complex pure-state perturbations of W3 is encodable with the fixed triangle graph. A nonzero cubic reduced moment yields an anchored O(distance^(1/3)) encoder-control bound and cube-root continuation on a specified legal state path. |
| **Ограничения / нерешённые трудности** | 2026-10-12 primary arXiv history/current fulltext and retained v1/v2 PDFs checked; title/resolution, W neighborhood, three-qubit commuting encodability and successor searches preserved. No verified successor located, but unpublished work and complete forward citations remain unchecked; no absolute priority claim. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00007-p09/paper.pdf) · [TeX](projects/phys-00007-p09/manuscript/main.tex) · [Code / data](projects/phys-00007-p09) · [Author handoff](projects/phys-00007-p09/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00007-p09/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00008-p03 · Exact local spectrum and a residual-rate obstruction for quantum Latin-square normalization</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | For this measurement-array generator, excellent individual Gram conditioning does not guarantee a strict uniform one-cycle residual reduction. The family gap collapses quadratically near a classical endpoint. This identifies a geometric obstruction to a conditioning-only progress guarantee; no nonlinear iteration budget or probability law is claimed. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the explicit n=4 Q(theta) block-rotation quantum Latin square in evidence/research/local-spectrum-proof.md, the real derivative of one source row-then-column normalization cycle restricted to the 64-dimensional column-unitary tangent space has spectrum 0 (16), 1 (32), (1+cos(theta))/2 (8), (1-cos(theta))/2 (8), with degeneracies combined for all real theta. For every q in (0,1), delta in (0,1), eta>0, some theta in (0,pi/2) and legal column-unitary x with 0<&#124;&#124;x-Q(theta)&#124;&#124;_F<eta satisfy e(F(x))>q e(x)>0 while all eight inverted Gram spectra lie in \[1-delta,1+delta\]. This is a local one-cycle rate obstruction only and leaves the original almost-sure arbitrary-precision question unresolved. |
| **Предлагаемый вклад** | Exact complete spectrum 0^16, 1^32, ((1+cos(theta))/2)^8, ((1-cos(theta))/2)^8 of the n=4 family derivative restricted to the column-unitary tangent space, including classical endpoint degeneracies. Prove legal arbitrarily close curves with source-residual ratio tending to the slow eigenvalue and all inverted Grams arbitrarily close to I, excluding a uniform one-cycle q<1. |
| **Ограничения / нерешённые трудности** | 2026-10-12 primary version/conjecture, original Sections 3-4, 2016 Sections 5-6, 2017 strictly positive-block theorem domain, 2023 Problem 3.13, current author bibliography and limited 2026 v3 successor screen; Lewis-Malick Lemma 2.1/equation (11)/Theorem 4.3 and Musto-Vicary Definition 1/Example 2. Exact-title, alternating-projection, linear-convergence, principal-angle and quantum Sinkhorn rate searches. No matching explicit family spectrum identified in bounded checked sources; equivalent older results and priority remain a fresh-review question. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00008-p03/paper.pdf) · [TeX](projects/phys-00008-p03/manuscript/main.tex) · [Code / data](projects/phys-00008-p03) · [Author handoff](projects/phys-00008-p03/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00008-p03/manuscript/REPRODUCIBILITY.md) |

</details>

<details>
<summary><strong>phys-00009-p01 · Exact two-particle relaxation crossover for the symmetric inclusion process on hypercubes</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Determines when a pair-separation relaxation mode is strictly slower than every one-particle mode, at finite diffusivity. Provides a dimension-dependent crossover boundary and its scaling. Published monotonicity then excludes one-particle reduction of the full conservative SIP below the threshold, while its all-k gap above the threshold remains undetermined. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the conservative SIP with exactly two particles on the D-dimensional Boolean hypercube Q_D, every finite integer D>=1, homogeneous site weight a>0 and common edge conductance c>0, lambda_2=c*min(2a,rho_D(a)), where rho_D(a) is the smallest positive eigenvalue of the D+1-state birth-death negative generator with downward rates 2*d*a+2*1_{d=1} and upward rates 2*(D-d)*a. The one-particle gap is 2*c*a. With a_D=(D-1)*2^{-(D-1)}*integral_0^1(1+u^2)^{D-1}du-1, lambda_2<lambda_1 iff 0<a<a_D for D>=4; for D<=3 lambda_2=lambda_1 for all a>0. The threshold satisfies a_4=1/35, a_(D+1)=(D^2*a_D+1)/((D-1)*(2D+1)) for D>=2, and D^2*a_D tends to 1. No k>=3 identity is claimed. |
| **Предлагаемый вклад** | Exact full two-particle gap reduction for every homogeneous hypercube Q_D and every finite positive a to a D+1-state distance chain, including rigorous bounds on omitted sectors. An exact finite-a crossover formula, a_4=1/35, an all-D recurrence and D^2*a_D->1 are obtained. |
| **Ограничения / нерешённые трудности** | Primary current versions, relevant journal sections, the 2024 institutional published PDF and bounded hypercube/Hamming/1-over-35 searches checked on 2026-10-12, before and during research. The inspected texts and searches did not yield this formula. No exhaustive global priority claim; novelty and significance require a fresh referee. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00009-p01/paper.pdf) · [TeX](projects/phys-00009-p01/manuscript/main.tex) · [Code / data](projects/phys-00009-p01) · [Author handoff](projects/phys-00009-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00009-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00013-p01 · Exact pure-state contraction spectrum of a three-qubit Haar circuit</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Identifies centered single-qubit purity as the slowest state-observable mode at every symmetric moment order, excludes higher symmetric moments as slower counterexamples, and gives exact stationary L2 contraction for random pure-state preparation. The pure-state quotient is faster than the known group-level fourth-moment cosine1/2. It does not settle the original unitary-group mixing constant or imply a total-variation mixing time from a delta initial law. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the specified three-qubit adjacent normalized Haar-SU4 circuit, the complete nonzero principal cosines on L2(CP7, normalized Haar) are c_r=6/((r+2)(2r+3)), r>=0. In conjugation on End(Sym^k C8), k>=0 integer, the cosines truncate to0<=r<=floor(k/2). Removing the whole global invariant gives norm0 for k<=1 and2/5 for every k>=2, and pure-state ordered m-step norm(2/5)^(2m-1), m>=1. This is a natural state quotient/symmetric-moment result; the original all-PU8 equality c_*=1/2 remains unresolved. |
| **Предлагаемый вклад** | For the same adjacent Haar-SU4 three-qubit circuit, derive the complete principal-cosine sequence c_r=6/((r+2)(2r+3)) on L2(CP7), r>=0, and its exact truncation to every End(Sym^k C8), r<=floor(k/2). The stationary pure-state nonfixed norm is2/5, and the ordered m-step norm is(2/5)^(2m-1). This is an all-degree quotient result; the number2/5 at degree2 and the finite k7/k8 tables are not the novelty claim. |
| **Ограничения / нерешённые трудности** | Current official metadata and decisive primary full-text passages checked2026-10-12:2609.40164v2,2012.05259v1,2411.13739v2,2408.11201v2,1809.00642v1,math-ph/0610045v2,quant-ph/0012101v3,2606.11438v1. Searches covered exact original constant, later resolutions, pure-state/all-symmetric-moment spectra, joint purity correlations and Jacobi/projective-space equivalents. No examined primary source gives this exact local-circuit all-degree sequence. This is bounded proposer novelty analysis, not exhaustive priority proof; the older Haferkamp-Hunter-Jones publisher body remains unexamined. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00013-p01/paper.pdf) · [TeX](projects/phys-00013-p01/manuscript/main.tex) · [Code / data](projects/phys-00013-p01) · [Author handoff](projects/phys-00013-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00013-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00014-p01 · Exact single-use Bayesian Nagaoka–Hayashi attainment for noisy qubit rotations</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | A fixed single-qubit pre-rotation followed by a Bell measurement achieves the ultimate three-axis Bayesian mean-square precision for one noisy channel use. Only the posterior estimator shrinks with known noise, so the measurement needs no noise-dependent redesign. The finite Bayesian incompatibility penalty relative to the reproduced SLD value is 8B Q^2/(A+B) for lambda<1. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For k=1 in the frozen fixed-Bell-probe model U_theta=exp(-i theta dot sigma) followed by known depolarization 0<=lambda<=1, with uniform Cartesian-volume prior on &#124;&#124;theta&#124;&#124;<=pi/4 and R=E\[&#124;&#124;hat theta-theta&#124;&#124;^2\]/3, the optimum over all system-ancilla physical POVMs and finite-second-moment estimators equals the source Bayesian Nagaoka-Hayashi SDP: R_1(lambda)=C_NH(1,lambda)=pi^2/80-4(1-lambda)^2(3/(2pi)-12/pi^3)^2. It is attained by four orthonormal vectors (&#124;0>-i sum_i s_ji&#124;i>)/2 in the source spin basis, for tetrahedral signs s=(+++),(+--),(-+-),(--+), with posterior estimates 2(1-lambda)(3/(2pi)-12/pi^3)s. Equivalently, one fixed local pre-rotation followed by a Bell measurement implements this PVM. A normalized covariant sphere measurement also attains it. Exact continuum physical-risk and NH PSD dual certificates establish the all-noise equality, including endpoints. No claim for k=2,3,4 or optimized/adaptive probes; the frozen original remains unresolved. |
| **Предлагаемый вклад** | Exact k=1 fixed-Bell attainment for the full continuum 0<=lambda<=1 under the specified pi/4 volume prior: closed optimal risk pi^2/80-4(1-lambda)^2(3/(2pi)-12/pi^3)^2; four-outcome noise-independent rotated-Bell projective measurement; exact posterior estimates; distinct all-estimate physical-risk and NH SDP dual certificates. The original k=1,2,3,4 question remains unresolved. |
| **Ограничения / нерешённые трудности** | 2026-10-12 21:10-21:19 UTC: current 2607.15398 v1 and 2511.16645 v4 metadata/bodies; selected current author fulltext 2008.02612v2 and previous exact-scope Suzuki/Zhao/Andre source records. Exact identifier/title, Bayesian NH exact/proof/attainment, depolarization/SU(2), tetrahedral/simplex, Hadamard/projective, phase-imaging/N00N queries. No verified later exact resolution found. Bounded coverage is not a proof of priority; Nature publisher redirect failure and incomplete old-method appendices are disclosed. Fresh referee must assess novelty/significance. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00014-p01/paper.pdf) · [TeX](projects/phys-00014-p01/manuscript/main.tex) · [Code / data](projects/phys-00014-p01) · [Author handoff](projects/phys-00014-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00014-p01/manuscript/REPRODUCE.md) |

</details>

<details>
<summary><strong>phys-00015-p01 · Local dissipation optimality at the spectral coherence threshold of unicyclic clocks</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Small kinetic heterogeneity cannot reduce the homogeneous dissipation cost once the leading spectral coherence is restored to the source's eligibility threshold. Any improvement or counterexample must leave the n-dependent local neighborhood. This is a finite-model response result, not an experimental entropy estimate or a global bound. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For each integer n>=5 put t=tan(pi/n). The homogeneous strictly positive single-cycle rates u=c(1+t), d=c(1-t), c>0, have a simple globally leading conjugate pair with b/a=1. In a sufficiently small n-dependent neighborhood modulo common time scaling, every legal rate tuple with b/a>=1 satisfies Y=sigma*a/b^2 >= (1+t^2)*atanh(t)/t>1, with equality only at that homogeneous threshold ring up to scale. The full fixed-b/a=1 heterogeneous tangent Hessian is positive definite, including even-n Nyquist modes. No explicit or uniform-in-n radius, arbitrary-coherence optimality or global heterogeneous inequality is claimed. |
| **Предлагаемый вклад** | Exact positive full heterogeneous tangent Hessian at b/a=1 for every n>=5, and resulting strict local minimum of Y=sigma*a/b^2 among nearby positive-rate single cycles on b/a>=1, modulo time scale. Stationary probabilities and edge flows both vary freely. Nyquist modes and the local spectral ordering are included. |
| **Ограничения / нерешённые трудности** | Bounded primary checks on 2026-10-12: OBS 2112.01607v2, Gu 2606.05498v1, Shiraishi 2609.34352v1, Kolchinsky 2510.14101v3, winding paper 2605.15884v3, current Jason author TeX scope and Uhl--Seifert 1907.04260v1 Section 4. Searches included entropy/coherence, unicyclic/heterogeneous, uniform rates, perturbation, second order and local minimum. No exact predecessor for this restricted entropy-cost statement was identified. Priority and significance remain candidate assessments; publisher-final-body comparison and a complete forward-citation census are not completed. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00015-p01/paper.pdf) · [TeX](projects/phys-00015-p01/manuscript/main.tex) · [Code / data](projects/phys-00015-p01) · [Author handoff](projects/phys-00015-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00015-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00018-p01 · A local noise tradeoff for two cross-regulated genes with unequal finite RNA lifetimes</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | At unregulated RNA/protein mean one and finite unequal RNA lifetimes, arbitrary cross-transcription shaping cannot reduce both stationary protein Fano factors below their correctly mean-matched two-stage baselines within the stated response-dependent weak-feedback neighborhood. This excludes a whole nonlinear low-copy design route without LNA or a burst approximation. Searches for a legal simultaneous-suppression example must leave this neighborhood, change parent kinetics or consider larger networks. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the exact infinite-state two-stage N=2 gene-expression CTMC with parent tuples (c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1), let h1,h2 be any real bounded whole-lattice protein functions with &#124;h_i&#124;<=1, and a,b>0. Set g=max(a,b), f1=1+epsilon*a*h2(P2), f2=2-epsilon*b*h1(P1), with all other reaction channels unchanged. The exact independent-parent forms defined in evidence/research-pass2/operator-certificate-and-tail.md satisfy &#124;V1&#124;,&#124;V2&#124;<=4/5*sqrt(U1*U2) for all such response functions, without monotonicity or a finite plateau. For S=a^2*U1+b^2*U2>0, every 0<epsilon<min(1/g,S/(4480*g^3)) gives an admissible network with at least one stationary protein Fano factor strictly above its mean-matched finite-lifetime baseline B1=3/2 or B2=4/3. If both responses are constant, both Fano factors equal their baselines. This computer-assisted local theorem covers all response shapes for this fixed unequal-lifetime low-copy pair only; epsilon is response-dependent. The original arbitrary-N, arbitrary-kinetics, strong-feedback problem remains unresolved. |
| **Предлагаемый вклад** | A computer-assisted exact local no-simultaneous-output-suppression result for the finite-RNA parent pair (c,delta,beta,gamma)=(1,1,1,1),(2,2,1,1), uniform over every real bounded whole-lattice response shape, including nonmonotone and arbitrarily rare tails. A new weaker whole-space weighted generator bound and finite Riesz residual enclosures remove the earlier artificial finite-plateau restriction, yielding &#124;V_i&#124;<=4/5 sqrt(U1 U2), with an explicit finite-feedback stationary covariance remainder. |
| **Ограничения / нерешённые трудности** | Rechecked official arXiv histories 2607.20823,2605.15401,2512.20887 and the current burst-paper Discussion and official author list on 2026-10-13 UTC before legacy extension. Compared decisive pages in preserved primary PDFs/texts and targeted exact-title, finite-intermediate, finite-mRNA, two-stage weak-feedback, nonlinear cross-regulation and simultaneous-suppression searches. No matching later primary theorem was identified in this bounded screen. Current general resolution and global priority remain uncertain; absence of a hit is not proof of openness or novelty. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00018-p01/paper.pdf) · [TeX](projects/phys-00018-p01/manuscript/main.tex) · [Code / data](projects/phys-00018-p01) · [Author handoff](projects/phys-00018-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00018-p01/reproducibility/README.md) |

**Связанные результаты / ранние версии**

- [phys-smallmac00010-p02](projects/phys-smallmac00010-p02): The two-gene finite-RNA-lifetime matched-baseline theorem is not the three-species direct-abundance feedback-ring weak-regulation result. The intermediate RNA state, number of species, baseline and whole-space remainder are different.

</details>

<details>
<summary><strong>phys-00024-p01 · Local stability of a sharp q-deformed commutator response for conditional quantum operations</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The already reconstructed conditional-Kraus ordered-amplitude response has a locally stable sharp upper envelope: general operator errors normal to the saturation family, including spectator-level coupling, reduce the optimized response quadratically. A violating tuple cannot approach this orbit at fixed n,q. No explicit neighborhood radius or new relaxation-rate prediction is claimed. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For each finite n>=3 and each real q not equal to -1 or 1, set R=sqrt(2(1+q^2)), c=(1+q+R)/2, u=sqrt(c-1), b=sign(1+q)sqrt(c-q), A_q=diag(u,-b,0,...,0). For g_q(A)=lambda_max(H_q(A))/&#124;&#124;A&#124;&#124;_F^2, where vec(B)^dagger H_q(A) vec(B)=Re Tr((BA-AB)^dagger(BA-qAB)), there exists an n,q-dependent neighborhood of A_q in M_n(C) on which g_q is real analytic with a Morse-Bott local maximum c. Its local maximum set is the smooth 4n-2 real-dimensional manifold of unitarily embedded two-plane matrices C satisfying det C+\[ub/(u-b)^2\](tr C)^2=0 near diag(u,-b). The complete negative normal Hessian spectrum at A_q is -2, -4c(c-q)/\[(2c-q)R\], -4c(c-1)/\[(2c-1)R\], -2c/R, with multiplicities 2,2(n-2),2(n-2),2(n-2)^2. For mu the smallest magnitude and Lambda the largest, a smaller tubular neighborhood satisfies (mu/8)dist_F(A,M_q)^2 <= c-g_q(A) <= Lambda dist_F(A,M_q)^2, hence the corresponding local sharp f-bound holds for every complex B. No explicit radius, global bound, or uniform n/q limit is claimed. Auxiliary q=1/2 n=2 nonzero equality matrices are exactly det A+(3/2)(3+sqrt(10))(tr A)^2=0. |
| **Предлагаемый вклад** | For every finite n>=3 and real q except -1,1, prove a full-dimensional local sharp bound near the embedded witness, classify its smooth equality manifold of dimension 4n-2, and derive the complete negative normal Hessian spectrum with multiplicities. Auxiliary q=1/2 equality determinant and curvature explain the previous flat directions. |
| **Ограничения / нерешённые трудности** | Primary-source and exact-claim rechecks on 2026-10-13: arXiv:2208.10005v1, current publisher abstract, arXiv:2608.03897v1 q-commutator norms, arXiv:2409.00436v1 averaged relaxation resolution, exact identifier/title/formula/author and equality/stability/Morse searches. No primary statement of this local all-q f-response spectrum was found; this bounded screen is not priority certification. Fresh novelty and significance review remain required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00024-p01/paper.pdf) · [TeX](projects/phys-00024-p01/manuscript/main.tex) · [Code / data](projects/phys-00024-p01) · [Author handoff](projects/phys-00024-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00024-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00027-p01 · Time-independent Lindblad embeddings of two-parameter Werner–Holevo noise</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The unrestricted reduction makes the known covariant rate inequalities decisive for calibrated symmetric and antisymmetric Werner-Holevo noise even when the underlying constant master equation is not assumed symmetric: outside the qutrit region no hidden Hamiltonian, noncovariant jumps, or logarithm branch can realize the observed channel. The two boundaries remain the zero-rate limits of the known symmetric-traceless and antisymmetric jump families. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For the frozen two-parameter noisy Werner-Holevo channel on M_d(C), write Phi=P0+s Ps+a Pa with s=1-d*x/(d-1)-d*y/(d+1) and a=1-(d-2)*x/(d-1)-(d+2)*y/(d+1). For every d>=3 in the sector s>0,a>0, there exists a finite time-independent same-system GKLS generator L with exp(L)=Phi, allowing arbitrary Hamiltonians, jumps and logarithm branches, if and only if s^((d+2)/d)<=a<=s^((d-2)/d). A valid generator has H=0 and nonnegative symmetric-traceless and imaginary-antisymmetric jump rates gamma_s=((d-2)log(s)-d log(a))/(2d) and gamma_a=(d log(a)-(d+2)log(s))/(2d). For d=3 this gives the complete classification in the frozen x>0,y>0,x+y<=1 domain: s=1-3x/2-3y/4>0, a=1-x/2-5y/4>0, and s^5<=a^3<=s. The negative even-multiplicity sectors for d>=4 are not classified. |
| **Предлагаемый вклад** | The proposed contribution is only the arbitrary-endpoint-generator necessity step and its qutrit consequence: for every d>=3 and s,a>0, any same-system time-independent GKLS logarithm of the O(d)-covariant endpoint, even if noncovariant and nonprincipal and with arbitrary Hamiltonian/jumps inside degenerate sectors, has a full-O(d) average fixed by branch-invariant real sector traces to the principal covariant logarithm. Combining this reduction with the known 2023 covariant cone gives the unrestricted positive-spectrum criterion. Odd real sector multiplicities plus singularity exclusion then give the complete frozen-domain d=3 classification. The covariant cone/exponential itself is not claimed new, and the signed d>=4 problem remains unresolved. |
| **Ограничения / нерешённые трудности** | Complete retained primary PDFs arXiv:1801.06121v3, 2301.10679v4, and 2602.08464v1 were read at the recorded locators, and live primary records plus exact-claim/later-resolution searches were rechecked on 2026-10-13. The current model record remains arXiv:2405.11216v3. No returned primary record stated the narrowed arbitrary-noncovariant O(d) endpoint reduction or complete noisy-Werner--Holevo qutrit region. This bounded result is not proof of priority or openness; a fresh referee must independently repeat the comparison. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00027-p01/paper.pdf) · [TeX](projects/phys-00027-p01/manuscript/main.tex) · [Code / data](projects/phys-00027-p01) · [Author handoff](projects/phys-00027-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00027-p01/reproducibility/README.md) |

</details>

<details>
<summary><strong>phys-00035-p01 · Near-star spectral gaps on subdivided two-star qubit networks</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | The actual lowest excitation of this leaf-rich two-hub network is a relative 1/(2k) above the star threshold at leading order, with a controlled theta-dependent correction. Uniform approach to Delta/eta=1 occurs on an infinite nonstar family as s tends to one in eta=theta/k, so removing stars does not create a fixed multiplicative excess in this specified near-endpoint regime. There is no new phase or quantum algorithm complexity claim. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | Let T_k have hubs a,b, a shared neighbor c, and k private leaves at each hub, with only ac,bc and the private hub-leaf edges; n=2k+3. For the original phase-free unnormalized unit-edge H_s, every integer k>=100 and every real theta in \[1/2,2\], eta=theta/k, s=sqrt(1-eta), have simple full ground and first excited energies in conserved-number N=2 and N=3 after X_a X_b. With full multiplicities, &#124;Delta(H_s(T_k))/eta-\[1+1/(2k)+(1-theta)/(4k^2)\]&#124;<=364/k^3, so Delta>eta and the ratio tends uniformly to one on this infinite nonstar family. Every full N>=4 sector obeys lambda_N<lambda_3-(N-3)eta/2 for B=-X_a X_b H X_a X_b; complete internal N2 modes and N0/N1 are also excluded. Original all-graph/all-s conjecture remains unresolved. This is a controlled joint size/endpoint family result, with fixed unit edge strength and growing degree, not a thermodynamic phase claim. |
| **Предлагаемый вклад** | For every subdivided two-star T_k, integer k>=100 and theta in \[1/2,2\], eta=theta/k, prove the complete ground and first excitation are simple N2/N3 levels and &#124;Delta/eta-\[1+1/(2k)+(1-theta)/(4k^2)\]&#124;<=364/k^3. The complete-star envelope supplies every N>=4 bound, including the stronger half-eta penalty; a full N2 Weyl bound supplies omitted internal irreps. The sector expansion is thereby upgraded to a full-gap result. |
| **Ограничения / нерешённые трудности** | Fresh primary metadata and decisive preserved fulltexts checked on 2026-10-14, before extending the legacy claim. Exact claim/resolution, deformed EPR/leaf/star and two-star/joint-limit searches are preserved in research-p4-current-web-1 through -4; current versions v1,v1,v1,v2,v1 confirmed. No matching full-gap formula or later sharp-leaf resolution found in this bounded coverage. Novelty/significance remain provisional for a fresh referee, without exhaustive priority or openness claims. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00035-p01/paper.pdf) · [TeX](projects/phys-00035-p01/manuscript/main.tex) · [Code / data](projects/phys-00035-p01) · [Author handoff](projects/phys-00035-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00035-p01/README_REPRODUCIBILITY.md) |

**Связанные результаты / ранние версии**

- [phys-smallmac00022-p03](projects/phys-smallmac00022-p03): The small_mac result is an all-s certificate for q=1..6 one-hub subdivided stars. big_mac proves a full-gap, tail-controlled two-hub family for k>=100 in eta=theta/k, theta in [1/2,2]. Different topology, size and parameter quantifiers; neither is an all-graph proof.

</details>

<details>
<summary><strong>phys-00037-p01 · Second-order entropy stability of a three-mode fermionic product channel</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | Rules out a quadratic non-Gaussian descent mechanism for increasing the source single-use unrestricted Holevo objective from this Gaussian encoder anywhere in the full three-mode full-rank-reference parameter chamber. Supplies an exact normal-curvature check for entropy optimization. No global optimum, new capacity formula, SSR-constrained rate, or experiment is inferred. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For Bravyi's complete n=3 qubit/Majorana attenuation channel and every ordered 0<=b6<=...<=b1<1, the output-entropy gradient at the generalized-Gaussian pure input &#124;+++> vanishes in all normalized complex pure-state directions, and the real 14-dimensional Hessian is positive semidefinite. Its Gaussian-normal cross block vanishes exactly. In the exact two-dimensional non-Gaussian normal span_R{&#124;-+->,i&#124;-+->}, H_Im>=H_Re>=2*b1^2*(1-b1^2)^4/(65*ln(2)), hence both normal eigenvalues are strictly positive for b1>0. At b1=0 the complete channel is depolarizing and the Hessian vanishes. Zero and repeated smaller attenuations are covered; rank-singular b1=1, strict local minimality along Gaussian zero modes, global entropy optimality and higher n are excluded. |
| **Предлагаемый вклад** | An exact computer-assisted all-parameter certificate for the two non-Gaussian normal Hessian eigenvalues at the three-mode Eq.(36) optimizer for every ordered 0<=b6<=...<=b1<1, including zero and repeated smaller attenuations. A uniform explicit positive lower bound when b1>0, exact cross-block selection rules, and the known Gaussian minimum imply a nonnegative full-complex 14-dimensional pure-state Hessian. |
| **Ограничения / нерешённые трудности** | Fresh primary exact-claim/title and local-Hessian searches on 2026-10-14; Bravyi v1, Arhancet radial-v6 and Fourier-v15 selected full-text comparisons, Salek et al. 2610.06758v1 endpoint/parity theorem, and Ruskai-Yard 2111.11385v4 Introduction/Theorem 2/Section 3. Current version pages and raw search/capture replies are preserved. No equivalent theorem was located; bounded searches, selected body coverage and inaccessible publisher revisions do not prove exhaustive priority or present openness. Fresh referee novelty/significance review remains required. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00037-p01/paper.pdf) · [TeX](projects/phys-00037-p01/manuscript/main.tex) · [Code / data](projects/phys-00037-p01) · [Author handoff](projects/phys-00037-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00037-p01/supplement/README.md) |

</details>

<details>
<summary><strong>phys-00040-p01 · Initial entropy-production decrease for product-profile narrow beams in the Landau–Maxwell equation</strong> — Частичный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | A natural counterstreaming route to positive initial entropy acceleration is excluded beyond Gaussian local profiles, even for arbitrary fixed longitudinal score skewness. Within the specified beam scaling/covariance class, a putative positive p->0 sequence must violate local product structure or fixed-configuration hypotheses. The original all-data/all-time question remains unresolved. |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | In the three-dimensional homogeneous Landau-Maxwell equation with a(z)=(&#124;z&#124;^2 I-zz^T)/2, mass one, mean zero and energy three, fix finite distinct real mu_j, w_j>0 with sum w=1, sum w mu=0, sum w mu^2=3. For each j fix centered normalized P_j on R^2 and R_j on R, each a polynomial globally bounded below by a positive constant multiplied by a centered nondegenerate Gaussian, with Cov(P_j)=a_j I_2, Var(R_j)=lambda_j>0 and sum w a=1. Put kappa_p^2=1-(2p+p^2 sum w lambda)/3 and f_p(v)=p^-2 sum_j w_j P_j(v_perp/sqrt(p)) R_j((v3-kappa_p mu_j)/p). For sufficiently small p>0 with kappa_p>=1/2, its actual initial right entropy-production derivative is Dprime_0(f_p)=p^-2 sum_j w_j C_j+O(p^-1), with configuration-dependent remainder, where C_j=-(mu_j^2+3)^2 JP_j/2-2(1+2a_j+U4_j/4)J_j+(9+5mu_j^2-mu_j^2 K2_j)I_j-mu_j a_j S3_j. Here JP=E_P&#124;&#124;Hess log P&#124;&#124;_F^2, U4=E_P&#124;X&#124;^4, K2=E_P(X.grad log P)^2, I=E_R((log R)prime)^2, J=E_R((log R)doubleprime)^2 and S3=E_R((log R)prime)^3. Every such coefficient satisfies C_j<=-(5/28)(mu_j^2+3)^2 JP_j<=-45/(14a_j^2), so sum w C_j<=-45/14 and Dprime_0(f_p)<0 for all sufficiently small p. The same leading functional inequality holds for any regular positive product factors with the stated finite moments and valid integrations by parts. This is an initial-data asymptotic, not a closure or a result uniform over varying configurations; the original universal monotonicity problem remains unresolved. |
| **Предлагаемый вклад** | For every fixed finite normalized separated beam configuration with centered independent local transverse/longitudinal positive polynomial-Gaussian factors and widths sqrt(p),p, derive the full original-collision initial derivative Dprime_0(f_p)=p^-2 sum w C_j+O(p^-1). The general product coefficient includes longitudinal score skewness. Projected longitudinal curvature and transverse moment-curvature inequalities prove C_j<=-45/(14a_j^2), hence sum w C_j<=-45/14. Actual-mixture posterior overlap, tails and fixed-p initial differentiability are controlled analytically. |
| **Ограничения / нерешённые трудности** | Fresh primary histories/fulltexts and bounded exact-claim/successor/product-beam neighbor searches on 2026-10-14. Actual located Villani v5 sections 7,13,24.1 and Delarue-Menozzi-Nualart v1 Proposition 2.3 checked. No matching later resolution or identical criterion located; absence is not openness/priority proof. Older Villani 1998/2000 fulltexts remain unreviewed. Candidate novelty/value are proposer assessments requiring a fresh referee; earlier acceptance covers a different scope. Exact model and scope are stated in the frozen claim. Human author review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-00040-p01/paper.pdf) · [TeX](projects/phys-00040-p01/manuscript/main.tex) · [Code / data](projects/phys-00040-p01) · [Author handoff](projects/phys-00040-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-00040-p01/repro/README.md) |

</details>

## Вычислительный результат

<details>
<summary><strong>phys-00002-p06 · A four-level Mpemba witness beyond three-level tests</strong> — Вычислительный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | В некоторых моделях тепловой релаксации более горячее начальное состояние релаксирует быстрее. Условия для трёх уровней могут не определять поведение более крупных систем. |
| **Результат и охват исходной задачи** | Четырёхуровневый свидетель при положительной температуре и детальном балансе сохраняется в независимых вычислениях с точностью 100 и 180 цифр, а проверенные трёхуровневые необходимые условия исключены. |
| **Предлагаемый вклад** | Конкретный механизм в большей размерности проверяет пределы сведения тепловой релаксации к трёхуровневой диагностике. |
| **Ограничения** | Вычислительная работа; высокая точность не равнозначна сертификации с направленным округлением или общей классификации. Исходная задача остаётся нерешённой. |
| **PDF и исходники** | [PDF](projects/phys-00002-p06/paper.pdf) · [TeX](projects/phys-00002-p06/manuscript/main.tex) · [Bib](projects/phys-00002-p06/manuscript/references.bib) · [Код / данные](projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>phys-smallmac00001-p01 · Certified local optimality of a qubit counting process over a finite mean interval</strong> — Вычислительный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст / исходная задача** | 二能级量子计数器的单 Kraus–秩一探测器是否全局最优 |
| **Исходная задача** | не решена |
| **Результат и точная область утверждения** | For every prescribed mean count m in \[3,6\], the connected stationary branch through the certified mean-4 point, defined by the exact equations and rational root boxes in evidence/choi-continuation-analysis.md and the 8433-cell certificate, is a strict local minimum of the counting-time variance at fixed mean, modulo common unitary basis changes. Local competitors include all nearby qubit completely positive no-count maps of Choi ranks 1 through 4, mixed initial states, and rank-2 count effects. The instrument is identical at each discrete step and counting is eventual. This is the saved local-sufficiency proposition, conditional on independent verification of its analytic chart and interval certificates. |
| **Предлагаемый вклад** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Ограничения / нерешённые трудности** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, исходники и воспроизведение** | [PDF](projects/phys-smallmac00001-p01/paper.pdf) · [TeX](projects/phys-smallmac00001-p01/manuscript/main.tex) · [Code / data](projects/phys-smallmac00001-p01) · [Author handoff](projects/phys-smallmac00001-p01/AUTHOR_HANDOFF.md) · [Replay](projects/phys-smallmac00001-p01/supplement/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

Упаковка не предоставляет дополнительных лицензий. См. исходные инструкции автора и применимые права. Подача, внешнее рецензирование или принятие не подразумеваются.
