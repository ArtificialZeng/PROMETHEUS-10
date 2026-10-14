# PROMETHEUS-10 · Numerisches Ergebnis

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

Ein überprüfbares Archiv KI-gestützter Physikforschung. **93 PDFs bleiben erhalten; 90 kanonische Forschungseinträge werden indexiert.** Drei ältere Ergebnisse, die durch allgemeinere oder stärkere Aussagen abgedeckt sind, bleiben als verknüpfte historische Fassungen erhalten und werden nicht doppelt gezählt. „10“ bezeichnet die ursprüngliche Sammlung.

Alle Texte sind Forschungsentwürfe und benötigen menschliche Prüfung von Wissenschaft, Priorität und Autorenschaft. Beweis und Widerlegung gelten nur im exakt angegebenen Umfang. Teil- und numerische Ergebnisse lösen die ursprüngliche Frage nicht vollständig. Getrennte KI-Prüfkontexte sind interne Kontrollen, kein externes Peer-Review und keine Zeitschriftenannahme. Die historische Einschränkung der Bindungsprüfung des Boundariness-Entwurfs bleibt bestehen.

Wissenschaftliche Aussagen und Titel bleiben in ihrer Quellsprache. Navigation, Status und Nutzung sowie die ursprünglichen zehn Beschreibungen sind lokalisiert; die mathematische Bedeutung der zitierten Aussagen bleibt unverändert.

[PROMETHEUS-10](../../README.de.md)

[Durchsuchbarer Gesamtkatalog](../../catalog.html) · [Semantischer Vergleich und Deduplizierung](../../SEMANTIC_DEDUPLICATION.md) · [Reproduktionsanleitung](../../reproducibility/README.md)

## Die vier Ergebnisklassen

| | Kanonische Einträge |
|---|---:|
| [Beweis](../proofs/README.de.md) | **32** |
| [Widerlegung](../disproofs/README.de.md) | **18** |
| [Teilergebnis](../partial-results/README.de.md) | **38** |
| [Numerisches Ergebnis](../computational-papers/README.de.md) | **2** |

Der überwachte Ablauf prüft Primärquellen, rekonstruiert Gleichungen unabhängig, reproduziert publizierte Referenzen und lässt begrenzte Ergebnisse vor Manuskript und Freigabe frisch intern prüfen. Kurze Evidenzpakete und gemeinsame Werkzeuge vermeiden Wiederholungen. Cache-Eingaben sind Teil der Eingaben; unbelegte Token-Einsparungen oder Erfolgsquoten werden nicht behauptet.

## Numerisches Ergebnis

<details>
<summary><strong>phys-00002-p06 · A four-level Mpemba witness beyond three-level tests</strong> — Numerisches Ergebnis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | In manchen thermischen Modellen relaxiert ein heißerer Anfangszustand schneller. Kriterien für drei Niveaus müssen in höheren Dimensionen nicht ausreichen. |
| **Ergebnis und Umfang** | Ein Vier-Niveau-Beispiel bei positiver Temperatur und detailliertem Gleichgewicht besteht unabhängige Rechnungen mit 100 und 180 Stellen; die geprüften Drei-Niveau-Prädikate sind ausgeschlossen. |
| **Beanspruchter Beitrag** | Ein konkreter Mechanismus zeigt die Grenzen der Reduktion auf Drei-Niveau-Diagnostik. |
| **Grenzen und offene Punkte** | Numerischer Beitrag: hohe Präzision ist kein Zertifikat mit gerichteter Rundung und keine allgemeine Klassifikation. Das Ausgangsproblem bleibt offen. |
| **PDF und Quellcode** | [PDF](../../projects/phys-00002-p06/paper.pdf) · [TeX](../../projects/phys-00002-p06/manuscript/main.tex) · [Bib](../../projects/phys-00002-p06/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>phys-smallmac00001-p01 · Certified local optimality of a qubit counting process over a finite mean interval</strong> — Numerisches Ergebnis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund / ursprüngliche Frage** | 二能级量子计数器的单 Kraus–秩一探测器是否全局最优 |
| **Ursprüngliche Frage** | ungelöst |
| **Ergebnis und genauer Geltungsbereich** | For every prescribed mean count m in \[3,6\], the connected stationary branch through the certified mean-4 point, defined by the exact equations and rational root boxes in evidence/choi-continuation-analysis.md and the 8433-cell certificate, is a strict local minimum of the counting-time variance at fixed mean, modulo common unitary basis changes. Local competitors include all nearby qubit completely positive no-count maps of Choi ranks 1 through 4, mixed initial states, and rank-2 count effects. The instrument is identical at each discrete step and counting is eventual. This is the saved local-sufficiency proposition, conditional on independent verification of its analytic chart and interval certificates. |
| **Vorgeschlagener Beitrag** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Grenzen / offene Schwierigkeiten** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, Quelltext und Reproduktion** | [PDF](../../projects/phys-smallmac00001-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00001-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00001-p01) · [Author handoff](../../projects/phys-smallmac00001-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00001-p01/supplement/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

Die Zusammenstellung gewährt keine zusätzlichen Nutzungsrechte. Maßgeblich sind die ursprüngliche Autorenübergabe und die geltenden Rechte. Einreichung, Peer-Review oder Annahme werden nicht behauptet.
