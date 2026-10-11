# PROMETHEUS-10

**KI-Physik, die sich überprüfen lässt**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md)

Zehn KI-gestützte Physikmanuskripte mit Code zur Prüfung ihrer Aussagen. PROMETHEUS-10 verbindet automatisierte Beweissuche, Gegenbeispiele und kontrollierte Rechnungen in einer nachvollziehbaren Sammlung. Die 10 zählt Manuskripte, nicht zehn vollständig gelöste allgemeine Probleme.

Historische interne Prüfprotokolle: **4 Beweise, 3 Widerlegungen, 2 Beiträge mit Teilergebnissen und 1 numerischer Beitrag**. Kein reines Vermutungs-PDF. Alle sind Entwürfe zur abschließenden Autorenprüfung, keine extern begutachteten oder angenommenen Veröffentlichungen.

KI half unter menschlicher Anleitung bei Herleitungen, Code, numerischen Suchen, Prüfungen und Texten. Getrennte KI-Prüfkontexte sind kein externes Peer-Review. Die Beitragsspalte beschreibt beanspruchte Neuerungen; diese Paketierung enthält keine neue vollständige Prioritätsprüfung der Literatur.

| Projekt | Aussagentyp | Details |
|---|---|---|
| [phys-00002-p01](projects/phys-00002-p01/paper.pdf) · Wie viele Rauschkanäle braucht ein Qubit? | Teilergebnis | ↓ 01 |
| [phys-00002-p02](projects/phys-00002-p02/paper.pdf) · Vier Qubit-Messungen: die exakte Kompatibilitätsschwelle | Beweis | ↓ 02 |
| [phys-00002-p06](projects/phys-00002-p06/paper.pdf) · Ein Vier-Niveau-Mpemba-Beispiel jenseits von Drei-Niveau-Tests | Numerisches Ergebnis | ↓ 03 |
| [phys-00002-p15](projects/phys-00002-p15/paper.pdf) · Kritisches Zurücksetzen und der Verlust von Kohärenz | Beweis | ↓ 04 |
| [phys-00003-p01](projects/phys-00003-p01/paper.pdf) · Kann ein Drehmoment das Stromrauschen senken? | Beweis | ↓ 05 |
| [phys-00004-p01](projects/phys-00004-p01/paper.pdf) · Zwei verrauschte Quantenbatterien: helfen gemeinsame Eingaben? | Beweis | ↓ 06 |
| [phys-00004-p02](projects/phys-00004-p02/paper.pdf) · Ein exaktes Qutrit-Gegenbeispiel zu einer Unschärfevermutung | Widerlegung | ↓ 07 |
| [phys-00005-p01](projects/phys-00005-p01/paper.pdf) · 16 Knoten widerlegen die Minimalität des Pfades | Widerlegung | ↓ 08 |
| [phys-00006-p01](projects/phys-00006-p01/paper.pdf) · Qubit-Gedächtnis bricht eine universelle Kontraktionsbehauptung | Widerlegung | ↓ 09 |
| [phys-00007-p01](projects/phys-00007-p01/paper.pdf) · Wann multipliziert sich die Boundariness exakt? | Teilergebnis · archivierter Entwurf | ↓ 10 |

<details>
<summary><strong>01 · Wie viele Rauschkanäle braucht ein Qubit?</strong> — Teilergebnis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Lindblad-Generatoren beschreiben gedächtnislose offene Quantendynamik. Erreicht ein einzelner Sprungoperator den gesamten Rand der möglichen Populationstransfers? |
| **Ergebnis und Umfang** | Zertifizierte lokale Optimalität mit endlichem Radius nahe dem Ein-Sprung-Punkt a=1/2, gegenüber Störungen vom Rang höchstens zwei. Das globale Problem bleibt offen. |
| **Beanspruchter Beitrag** | Ein Intervallzertifikat macht aus einem numerischen stationären Punkt einen überprüfbaren lokalen Ausschlussbereich. |
| **Grenzen und offene Punkte** | Radius 10^-4; weder der globale Einbettungsrand noch entfernte bessere Generatoren sind damit ausgeschlossen. |
| **PDF und Quellcode** | [PDF](projects/phys-00002-p01/paper.pdf) · [TeX](projects/phys-00002-p01/manuscript/main.tex) · [Bib](projects/phys-00002-p01/manuscript/references.bib) · [Code / data](projects/phys-00002-p01) · `python reproducibility/reproduce.py --project phys-00002-p01` |

</details>

<details>
<summary><strong>02 · Vier Qubit-Messungen: die exakte Kompatibilitätsschwelle</strong> — Beweis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Verrauschte Messungen können gemeinsame Randmessungen einer übergeordneten Messung sein. Gesucht ist die erforderliche Rauschstärke. |
| **Ergebnis und Umfang** | Der Entwurf beweist 1/D für vier streng geordnete, planare, unverzerrte binäre Qubit-Messungen mit gemeinsamer Sichtbarkeit. |
| **Beanspruchter Beitrag** | Eine Konstruktion und eine passende duale Schranke liefern die analytische Schwelle; SOCP/SDP dienen als Gegenprüfung. |
| **Grenzen und offene Punkte** | Gilt nur für diese Geometrie und dieses Rauschmodell, nicht für beliebige POVMs oder Messungsanzahlen. |
| **PDF und Quellcode** | [PDF](projects/phys-00002-p02/paper.pdf) · [TeX](projects/phys-00002-p02/manuscript/main.tex) · [Bib](projects/phys-00002-p02/manuscript/references.bib) · [Code / data](projects/phys-00002-p02) · `python reproducibility/reproduce.py --project phys-00002-p02` |

</details>

<details>
<summary><strong>03 · Ein Vier-Niveau-Mpemba-Beispiel jenseits von Drei-Niveau-Tests</strong> — Numerisches Ergebnis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | In manchen thermischen Modellen relaxiert ein heißerer Anfangszustand schneller. Kriterien für drei Niveaus müssen in höheren Dimensionen nicht ausreichen. |
| **Ergebnis und Umfang** | Ein Vier-Niveau-Beispiel bei positiver Temperatur und detailliertem Gleichgewicht besteht unabhängige Rechnungen mit 100 und 180 Stellen; die geprüften Drei-Niveau-Prädikate sind ausgeschlossen. |
| **Beanspruchter Beitrag** | Ein konkreter Mechanismus zeigt die Grenzen der Reduktion auf Drei-Niveau-Diagnostik. |
| **Grenzen und offene Punkte** | Numerischer Beitrag: hohe Präzision ist kein Zertifikat mit gerichteter Rundung und keine allgemeine Klassifikation. Das Ausgangsproblem bleibt offen. |
| **PDF und Quellcode** | [PDF](projects/phys-00002-p06/paper.pdf) · [TeX](projects/phys-00002-p06/manuscript/main.tex) · [Bib](projects/phys-00002-p06/manuscript/references.bib) · [Code / data](projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>04 · Kritisches Zurücksetzen und der Verlust von Kohärenz</strong> — Beweis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Zufälliges Zurücksetzen verändert die Langzeitdynamik. Der kritische Sibuya-Exponent kennzeichnet einen besonderen Erneuerungsprozess. |
| **Ergebnis und Umfang** | Für alpha=1 und ein festes endlichdimensionales unitäres Register wird Konvergenz in Spurnorm zur spektralen Pinching-Abbildung mit Raten bei festen Spektrallücken bewiesen. |
| **Beanspruchter Beitrag** | Der kritische asymptotische Satz verbindet Erneuerungskoeffizienten mit dem Abklingen von Quantenkohärenz. |
| **Grenzen und offene Punkte** | Keine gleichmäßige Aussage bei sich schließenden Lücken, im thermodynamischen Limes oder für beliebige Reset-Regeln. |
| **PDF und Quellcode** | [PDF](projects/phys-00002-p15/paper.pdf) · [TeX](projects/phys-00002-p15/manuscript/main.tex) · [Bib](projects/phys-00002-p15/manuscript/references.bib) · [Code / data](projects/phys-00002-p15) · `python reproducibility/reproduce.py --project phys-00002-p15` |

</details>

<details>
<summary><strong>05 · Kann ein Drehmoment das Stromrauschen senken?</strong> — Beweis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Antrieb außerhalb des Gleichgewichts verändert Fluktuationen. Der Vergleich mit derselben Gleichgewichtsfalle trennt den Antriebseffekt ab. |
| **Ergebnis und Umfang** | Für das stabile, feldfreie, drehmomentgetriebene unterdämpfte OU-Modell liegt das Rauschen von Positionsströmen ersten/dritten Grades mindestens auf dem passenden Gleichgewichtswert. |
| **Beanspruchter Beitrag** | Exakte Polynome sowie unabhängige Wick- und Poisson-Rechnungen bestimmen den nichtnegativen Überschuss und Gleichheitsfälle für Gradienten-Randströme. |
| **Grenzen und offene Punkte** | Beschränktes Modell und Stromklasse; nichtlineare Kräfte, Magnetfelder und höhere Grade sind nicht abgedeckt. |
| **PDF und Quellcode** | [PDF](projects/phys-00003-p01/paper.pdf) · [TeX](projects/phys-00003-p01/manuscript/main.tex) · [Bib](projects/phys-00003-p01/manuscript/references.bib) · [Code / data](projects/phys-00003-p01) · `python reproducibility/reproduce.py --project phys-00003-p01` |

</details>

<details>
<summary><strong>06 · Zwei verrauschte Quantenbatterien: helfen gemeinsame Eingaben?</strong> — Beweis · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Korrelationen können die Arbeitsentnahme beeinflussen. Verallgemeinerte Amplitudendämpfung modelliert Relaxation bei endlicher Temperatur. |
| **Ergebnis und Umfang** | Für zwei Nutzungen unter der angegebenen Energiebeschränkung gilt laut Beweis W2(e)=2W1(e), einschließlich komplexer Zustände und globaler unitärer Arbeitsentnahme. |
| **Beanspruchter Beitrag** | Phasenreduktion und ein exaktes Positivitätszertifikat schließen die Optimierung dieses Modells ab. |
| **Grenzen und offene Punkte** | Keine Aussage über beliebige Kanäle, beliebig viele Nutzungen oder andere Arbeitsdefinitionen. |
| **PDF und Quellcode** | [PDF](projects/phys-00004-p01/paper.pdf) · [TeX](projects/phys-00004-p01/manuscript/main.tex) · [Bib](projects/phys-00004-p01/manuscript/references.bib) · [Code / data](projects/phys-00004-p01) · `python reproducibility/reproduce.py --project phys-00004-p01` |

</details>

<details>
<summary><strong>07 · Ein exaktes Qutrit-Gegenbeispiel zu einer Unschärfevermutung</strong> — Widerlegung · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Entropische Unschärfe begrenzt die gemeinsame Vorhersagbarkeit inkompatibler Messungen. Spektrale Kennzahlen können entscheidende Information verlieren. |
| **Ergebnis und Umfang** | Eine exakt rationale unitäre 3×3-Matrix widerlegt die untersuchte extended-MUB-Vermutung. |
| **Beanspruchter Beitrag** | Ein kurzes rationales Zertifikat zeigt, weshalb der zweite Singulärwert die vorgeschlagene universelle Aussage nicht trägt. |
| **Grenzen und offene Punkte** | Widerlegt eine bestimmte Vermutung, nicht das Unschärfeprinzip; eine scharfe Ersatzungleichung fehlt. |
| **PDF und Quellcode** | [PDF](projects/phys-00004-p02/paper.pdf) · [TeX](projects/phys-00004-p02/manuscript/main.tex) · [Bib](projects/phys-00004-p02/manuscript/references.bib) · [Code / data](projects/phys-00004-p02) · `python reproducibility/reproduce.py --project phys-00004-p02` |

</details>

<details>
<summary><strong>08 · 16 Knoten widerlegen die Minimalität des Pfades</strong> — Widerlegung · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Die zeitlich gemittelte Mischung eines Quantenwalks erfasst langfristige Rückkehrstrukturen und Extremalfragen des Transports. |
| **Ergebnis und Umfang** | Ein zusammenhängender einfacher ungewichteter Graph mit 16 Knoten und 62 Kanten hat Laziness 1673/1192 statt 23/16 beim Pfad, also eine Differenz von -81/2384. |
| **Beanspruchter Beitrag** | Zwei exakte Darstellungen zertifizieren ein endliches Gegenbeispiel für die angegebene Laplace-Quantenwalk-Behauptung. |
| **Grenzen und offene Punkte** | Keine Klassifikation aller Minimierer, Graphgrößen, Hamiltonoperatoren oder Normierungen. |
| **PDF und Quellcode** | [PDF](projects/phys-00005-p01/paper.pdf) · [TeX](projects/phys-00005-p01/manuscript/main.tex) · [Bib](projects/phys-00005-p01/manuscript/references.bib) · [Code / data](projects/phys-00005-p01) · `python reproducibility/reproduce.py --project phys-00005-p01` |

</details>

<details>
<summary><strong>09 · Qubit-Gedächtnis bricht eine universelle Kontraktionsbehauptung</strong> — Widerlegung · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Kontraktionsschranken quantifizieren den Verlust von Unterscheidbarkeit. Quantengedächtnis kann Schlussfolgerungen ohne Hilfssystem entkräften. |
| **Ergebnis und Umfang** | Ein exaktes Amplitudendämpfungsbeispiel mit verschränkten Eingaben und gleichen Randzuständen widerlegt den vorgeschlagenen universellen alpha-Doeblin-hockey-stick-Ersatz. |
| **Beanspruchter Beitrag** | Das Zertifikat isoliert den Gedächtniseffekt unter den ursprünglichen Eingabebedingungen. |
| **Grenzen und offene Punkte** | Nicht alle Doeblin-Ungleichungen sind widerlegt; eine optimale Ersatzschranke wird nicht geliefert. |
| **PDF und Quellcode** | [PDF](projects/phys-00006-p01/paper.pdf) · [TeX](projects/phys-00006-p01/manuscript/main.tex) · [Bib](projects/phys-00006-p01/manuscript/references.bib) · [Code / data](projects/phys-00006-p01) · `python reproducibility/reproduce.py --project phys-00006-p01` |

</details>

<details>
<summary><strong>10 · Wann multipliziert sich die Boundariness exakt?</strong> — Teilergebnis · archivierter Entwurf · Forschungstabelle aufklappen</summary>

| | |
|---|---|
| **Hintergrund** | Boundariness beschreibt die Lage eines Kanals relativ zum Rand seiner konvexen Menge. Tensorprodukte schaffen zusätzliche Optimierungsstruktur. |
| **Ergebnis und Umfang** | Exakte Multiplikativität in einer expliziten zweiparametrigen Familie vollrangiger, nicht-unitaler Qubit-Choi-Matrizen für &#124;s&#124;, &#124;t&#124; ≤ 1/5. |
| **Beanspruchter Beitrag** | Symbolische Choi-, Sturm- und LDL-Prüfungen stützen eine Familie mit exakt behandelbarem Tensorproduktoptimum. |
| **Grenzen und offene Punkte** | Die allgemeine Frage bleibt offen. Das historische Paket-Gate scheiterte an der Evidenz/Manuskript-Bindung; das PDF ist ein archivierter Entwurf, keine damals freigegebene Version. |
| **PDF und Quellcode** | [PDF](projects/phys-00007-p01/paper.pdf) · [TeX](projects/phys-00007-p01/manuscript/main.tex) · [Bib](projects/phys-00007-p01/manuscript/references.bib) · [Code / data](projects/phys-00007-p01) · `python reproducibility/reproduce.py --project phys-00007-p01` |

</details>


## Ergebnisse reproduzieren

Der erneute Lauf verwendete Python 3.12. Das Qutrit-Beispiel benötigt nur die Standardbibliothek. Für alle Projekte werden die festgelegten wissenschaftlichen Abhängigkeiten in einer virtuellen Umgebung installiert. Der Runner arbeitet auf neuen Kopien und verändert keine archivierten Belege. Weder KI-Konto noch API-Schlüssel oder Browser-Anmeldung sind erforderlich.

```bash
# Standard-library-only exact counterexample
python3 projects/phys-00004-p02/reproducibility/verify_counterexample.py

# Full scientific environment and replay
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python reproducibility/reproduce.py --all
```

Befehle, Ergebnisse und Grenzen stehen in [reproducibility/VALIDATION.md](reproducibility/VALIDATION.md). Ein Exitcode null ist kein wissenschaftlicher Beweis. Exakte Arithmetik, Intervallzertifikate, Hochpräzisionsbeispiele und Gleitkommatests haben unterschiedliche Aussagekraft.
TeX, Bib und Abbildungen liegen bei jedem Projekt. Hinweise zum Replay und PDF-Bau: [reproducibility/README.md](reproducibility/README.md). Die archivierten PDF-Bytes bleiben erhalten; andere TeX-Versionen können abweichende PDF-Dateien erzeugen.

## Eine historische Freigabe-Ausnahme

Für `phys-00007-p01` existieren PDF und ausführbare symbolische Prüfungen. Das historische Paket-Gate scheiterte jedoch an der Zuordnung von Evidenz und Manuskript. Es bleibt ein archivierter Entwurf. Neuverpackung oder erfolgreiches Replay ersetzen weder dieses Gate noch eine neue wissenschaftliche Begutachtung.

## Urheberschaft und Nutzung

Die Manuskripte nennen **Xiaojian Zeng**; Angaben und Freigabe müssen vom Autor bestätigt werden. KI- und Rechenunterstützung werden offengelegt. Diese Paketierung erteilt keine zusätzliche Open-Source- oder Creative-Commons-Lizenz; Rechte verbleiben bei den jeweiligen Rechteinhabern. Fremde Aufsätze werden zitiert, nicht mitverteilt. Abhängigkeiten behalten ihre Lizenzen.
