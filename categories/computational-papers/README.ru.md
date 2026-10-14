# PROMETHEUS-10 · Вычислительный результат

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

Проверяемый архив исследований по физике с помощью ИИ. **Сохранены 93 PDF; проиндексированы 90 канонических исследовательских записей.** Три ранних результата, охваченных более общими или сильными утверждениями, сохранены как связанные исторические версии без двойного счёта. «10» — название исходной коллекции.

Это исследовательские черновики, требующие человеческой проверки науки, приоритета и авторства. Доказательства и опровержения относятся только к точной области зафиксированного утверждения. Частичные и вычислительные результаты не означают полного решения исходной задачи. Независимые контексты ИИ — внутренние проверки, а не внешнее рецензирование или принятие журналом. Исторический пробел проверки привязки рукописи о boundariness сохраняется.

Научные утверждения и названия сохраняют язык источника. Навигация, статус, инструкции и исходные десять описаний локализованы; математический смысл цитируемых утверждений не меняется.

[PROMETHEUS-10](../../README.ru.md)

[Полный каталог с поиском](../../catalog.html) · [Семантическое сравнение и удаление дублей](../../SEMANTIC_DEDUPLICATION.md) · [Руководство по воспроизведению](../../reproducibility/README.md)

## Четыре категории результатов

| | Канонические записи |
|---|---:|
| [Доказательство](../proofs/README.ru.md) | **32** |
| [Опровержение](../disproofs/README.ru.md) | **18** |
| [Частичный результат](../partial-results/README.ru.md) | **38** |
| [Вычислительный результат](../computational-papers/README.ru.md) | **2** |

Контролируемый процесс проверяет первоисточники, независимо восстанавливает уравнения, воспроизводит опубликованный эталон и передаёт ограниченный результат свежей внутренней проверке перед написанием и выпуском. Короткие пакеты доказательств и общие инструменты уменьшают повторы. Кэш — часть входа; неизмеренная экономия токенов или вероятность успеха не заявляется.

## Вычислительный результат

<details>
<summary><strong>phys-00002-p06 · A four-level Mpemba witness beyond three-level tests</strong> — Вычислительный результат · Развернуть исследовательскую таблицу</summary>

| | |
|---|---|
| **Контекст** | В некоторых моделях тепловой релаксации более горячее начальное состояние релаксирует быстрее. Условия для трёх уровней могут не определять поведение более крупных систем. |
| **Результат и охват исходной задачи** | Четырёхуровневый свидетель при положительной температуре и детальном балансе сохраняется в независимых вычислениях с точностью 100 и 180 цифр, а проверенные трёхуровневые необходимые условия исключены. |
| **Предлагаемый вклад** | Конкретный механизм в большей размерности проверяет пределы сведения тепловой релаксации к трёхуровневой диагностике. |
| **Ограничения** | Вычислительная работа; высокая точность не равнозначна сертификации с направленным округлением или общей классификации. Исходная задача остаётся нерешённой. |
| **PDF и исходники** | [PDF](../../projects/phys-00002-p06/paper.pdf) · [TeX](../../projects/phys-00002-p06/manuscript/main.tex) · [Bib](../../projects/phys-00002-p06/manuscript/references.bib) · [Код / данные](../../projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

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
| **PDF, исходники и воспроизведение** | [PDF](../../projects/phys-smallmac00001-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00001-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00001-p01) · [Author handoff](../../projects/phys-smallmac00001-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00001-p01/supplement/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

Упаковка не предоставляет дополнительных лицензий. См. исходные инструкции автора и применимые права. Подача, внешнее рецензирование или принятие не подразумеваются.
