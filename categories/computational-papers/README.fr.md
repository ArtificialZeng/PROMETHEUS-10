# PROMETHEUS-10 · Résultat numérique

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

Une archive vérifiable de recherche en physique assistée par IA. **93 PDF sont conservés ; 90 entrées canoniques sont indexées.** Trois résultats antérieurs couverts par des conclusions plus générales ou plus fortes restent accessibles comme versions historiques, sans double comptage. « 10 » désigne la collection initiale.

Ce sont des manuscrits de recherche nécessitant une vérification humaine de la science, de la priorité et des auteurs. Preuve et réfutation concernent uniquement la portée exacte de la proposition figée. Les résultats partiels et numériques ne résolvent pas entièrement la question initiale. Les contextes IA séparés sont des contrôles internes, pas une évaluation externe ni une acceptation éditoriale. La limitation historique du contrôle de liaison du manuscrit sur la boundariness demeure.

Les énoncés scientifiques et les titres gardent leur langue source. Navigation, statut, utilisation et les dix descriptions initiales sont localisés ; les affirmations citées ne sont pas modifiées par traduction.

[PROMETHEUS-10](../../README.fr.md)

[Catalogue complet consultable](../../catalog.html) · [Comparaison sémantique et dédoublonnage](../../SEMANTIC_DEDUPLICATION.md) · [Guide de reproduction](../../reproducibility/README.md)

## Les quatre catégories de résultats

| | Entrées canoniques |
|---|---:|
| [Preuve](../proofs/README.fr.md) | **32** |
| [Réfutation](../disproofs/README.fr.md) | **18** |
| [Résultat partiel](../partial-results/README.fr.md) | **38** |
| [Résultat numérique](../computational-papers/README.fr.md) | **2** |

Le processus supervisé vérifie les sources primaires, reconstruit indépendamment les équations, reproduit un résultat publié et fait contrôler chaque contribution limitée avant rédaction et validation. Des dossiers courts et des outils partagés réduisent les répétitions. Le cache est une partie de l’entrée ; aucune économie de tokens ou probabilité de succès non mesurée n’est annoncée.

## Résultat numérique

<details>
<summary><strong>phys-00002-p06 · A four-level Mpemba witness beyond three-level tests</strong> — Résultat numérique · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte** | Dans certains modèles thermiques, une préparation plus chaude relaxe plus vite. Les critères à trois niveaux ne gouvernent pas nécessairement les dimensions supérieures. |
| **Résultat et portée** | Un témoin à quatre niveaux, à température positive et sous bilan détaillé, est confirmé par des calculs indépendants à 100 et 180 chiffres, avec exclusion des prédicats à trois niveaux testés. |
| **Contribution proposée** | Un mécanisme concret révèle les limites d’une réduction aux diagnostics à trois niveaux. |
| **Limites et obstacles** | Résultat computationnel : haute précision ne signifie ni arrondi dirigé certifié ni classification générale. La question initiale reste ouverte. |
| **PDF et sources** | [PDF](../../projects/phys-00002-p06/paper.pdf) · [TeX](../../projects/phys-00002-p06/manuscript/main.tex) · [Bib](../../projects/phys-00002-p06/manuscript/references.bib) · [Code / data](../../projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>phys-smallmac00001-p01 · Certified local optimality of a qubit counting process over a finite mean interval</strong> — Résultat numérique · Déplier le tableau de recherche</summary>

| | |
|---|---|
| **Contexte / question initiale** | 二能级量子计数器的单 Kraus–秩一探测器是否全局最优 |
| **Question initiale** | non résolue |
| **Résultat et portée exacte** | For every prescribed mean count m in \[3,6\], the connected stationary branch through the certified mean-4 point, defined by the exact equations and rational root boxes in evidence/choi-continuation-analysis.md and the 8433-cell certificate, is a strict local minimum of the counting-time variance at fixed mean, modulo common unitary basis changes. Local competitors include all nearby qubit completely positive no-count maps of Choi ranks 1 through 4, mixed initial states, and rank-2 count effects. The instrument is identical at each discrete step and counting is eventual. This is the saved local-sufficiency proposition, conditional on independent verification of its analytic chart and interval certificates. |
| **Contribution proposée** | The scoped contribution is the frozen scientific statement below. The complete argument and physical use are in the PDF and author handoff; this synchronization does not establish priority anew. |
| **Limites / difficultés restantes** | Only the stated model, quantifiers and assumptions are covered. The source original-question status is unresolved. Human scientific, priority and authorship review remains required. |
| **PDF, sources et reproduction** | [PDF](../../projects/phys-smallmac00001-p01/paper.pdf) · [TeX](../../projects/phys-smallmac00001-p01/manuscript/main.tex) · [Code / data](../../projects/phys-smallmac00001-p01) · [Author handoff](../../projects/phys-smallmac00001-p01/AUTHOR_HANDOFF.md) · [Replay](../../projects/phys-smallmac00001-p01/supplement/README.md) |

</details>

## Reproduction

```bash
python3 reproducibility/verify_portfolio.py
python3 reproducibility/verify_package.py
```

Le regroupement ne concède aucune licence supplémentaire. Consulter les instructions des auteurs et les droits applicables. Aucune soumission, évaluation externe ou acceptation n’est impliquée.
