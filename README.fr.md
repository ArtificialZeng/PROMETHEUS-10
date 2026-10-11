# PROMETHEUS-10

**Une physique par l’IA que l’on peut vérifier**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md)

Dix manuscrits de physique assistés par IA, accompagnés du code permettant d’examiner leurs conclusions. PROMETHEUS-10 réunit recherche de preuves, construction de contre-exemples et calcul contrôlé dans une collection vérifiable. Le nombre 10 désigne les manuscrits, pas dix problèmes généraux entièrement résolus.

Bilans des contrôles internes historiques : **4 preuves, 3 réfutations, 2 notes de résultats partiels et 1 article computationnel**. Aucun PDF uniquement conjectural. Tous sont des brouillons soumis à validation finale de l’auteur, sans prétendre à une évaluation externe ou à une acceptation éditoriale.

Sous direction humaine, l’IA a participé aux dérivations, au code, aux recherches numériques, aux contrôles et à la rédaction. Des contextes IA distincts ne constituent pas une évaluation externe. La colonne contribution expose les nouveautés revendiquées ; ce conditionnement ne refait pas une revue exhaustive de priorité bibliographique.

| Projet | Type de conclusion | Détails |
|---|---|---|
| [phys-00002-p01](projects/phys-00002-p01/paper.pdf) · Combien de canaux de bruit faut-il à un qubit ? | Résultat partiel | ↓ 01 |
| [phys-00002-p02](projects/phys-00002-p02/paper.pdf) · Quatre mesures de qubit : le seuil exact de compatibilité | Preuve | ↓ 02 |
| [phys-00002-p06](projects/phys-00002-p06/paper.pdf) · Un témoin Mpemba à quatre niveaux au-delà des tests à trois niveaux | Résultat computationnel | ↓ 03 |
| [phys-00002-p15](projects/phys-00002-p15/paper.pdf) · Réinitialisation critique et disparition de la cohérence | Preuve | ↓ 04 |
| [phys-00003-p01](projects/phys-00003-p01/paper.pdf) · Un couple moteur peut-il réduire le bruit des courants ? | Preuve | ↓ 05 |
| [phys-00004-p01](projects/phys-00004-p01/paper.pdf) · Deux batteries quantiques bruitées : les entrées conjointes aident-elles ? | Preuve | ↓ 06 |
| [phys-00004-p02](projects/phys-00004-p02/paper.pdf) · Un contre-exemple exact de qutrit à une conjecture d’incertitude | Réfutation | ↓ 07 |
| [phys-00005-p01](projects/phys-00005-p01/paper.pdf) · Un graphe à 16 sommets bat le chemin | Réfutation | ↓ 08 |
| [phys-00006-p01](projects/phys-00006-p01/paper.pdf) · Une mémoire quantique invalide une contraction universelle proposée | Réfutation | ↓ 09 |
| [phys-00007-p01](projects/phys-00007-p01/paper.pdf) · Quand la boundariness se multiplie-t-elle exactement ? | Résultat partiel · brouillon archivé | ↓ 10 |

<details>
<summary><strong>01 · Combien de canaux de bruit faut-il à un qubit ?</strong> — Résultat partiel · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Les générateurs de Lindblad décrivent une dynamique ouverte sans mémoire. Un seul opérateur de saut atteint-il toute la frontière des transferts de population ? |
| **Résultat et portée** | Optimalité locale certifiée dans un rayon fini près du point à un saut a=1/2, face aux perturbations de rang au plus deux. La question globale reste ouverte. |
| **Contribution proposée** | Un certificat par intervalles transforme un point stationnaire numérique en région locale vérifiable excluant des générateurs concurrents. |
| **Limites et obstacles** | Rayon 10^-4 ; ni la frontière globale de plongement ni les concurrents éloignés ne sont éliminés. |
| **PDF et sources** | [PDF](projects/phys-00002-p01/paper.pdf) · [TeX](projects/phys-00002-p01/manuscript/main.tex) · [Bib](projects/phys-00002-p01/manuscript/references.bib) · [Code / data](projects/phys-00002-p01) · `python reproducibility/reproduce.py --project phys-00002-p01` |

</details>

<details>
<summary><strong>02 · Quatre mesures de qubit : le seuil exact de compatibilité</strong> — Preuve · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Des mesures bruitées peuvent provenir des marginales d’une même mesure mère. Quelle quantité de bruit suffit ? |
| **Résultat et portée** | Le manuscrit démontre le seuil 1/D pour quatre mesures binaires de qubit, planes, non biaisées, strictement ordonnées et de même visibilité. |
| **Contribution proposée** | Une construction et une borne duale concordantes donnent le seuil analytique, corroboré par SOCP/SDP. |
| **Limites et obstacles** | Limité à cette géométrie et à ce modèle de bruit ; ne couvre pas tous les POVM ni tous les nombres de mesures. |
| **PDF et sources** | [PDF](projects/phys-00002-p02/paper.pdf) · [TeX](projects/phys-00002-p02/manuscript/main.tex) · [Bib](projects/phys-00002-p02/manuscript/references.bib) · [Code / data](projects/phys-00002-p02) · `python reproducibility/reproduce.py --project phys-00002-p02` |

</details>

<details>
<summary><strong>03 · Un témoin Mpemba à quatre niveaux au-delà des tests à trois niveaux</strong> — Résultat computationnel · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Dans certains modèles thermiques, une préparation plus chaude relaxe plus vite. Les critères à trois niveaux ne gouvernent pas nécessairement les dimensions supérieures. |
| **Résultat et portée** | Un témoin à quatre niveaux, à température positive et sous bilan détaillé, est confirmé par des calculs indépendants à 100 et 180 chiffres, avec exclusion des prédicats à trois niveaux testés. |
| **Contribution proposée** | Un mécanisme concret révèle les limites d’une réduction aux diagnostics à trois niveaux. |
| **Limites et obstacles** | Résultat computationnel : haute précision ne signifie ni arrondi dirigé certifié ni classification générale. La question initiale reste ouverte. |
| **PDF et sources** | [PDF](projects/phys-00002-p06/paper.pdf) · [TeX](projects/phys-00002-p06/manuscript/main.tex) · [Bib](projects/phys-00002-p06/manuscript/references.bib) · [Code / data](projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>04 · Réinitialisation critique et disparition de la cohérence</strong> — Preuve · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Les réinitialisations aléatoires modifient la dynamique à long terme. L’exposant critique de Sibuya définit un régime de renouvellement particulier. |
| **Résultat et portée** | Pour alpha=1 et un registre unitaire de dimension finie fixée, convergence en norme trace vers le pincement spectral, avec vitesses à écarts spectraux fixés. |
| **Contribution proposée** | Le théorème asymptotique critique relie les coefficients de renouvellement à la décroissance de la cohérence hors diagonale. |
| **Limites et obstacles** | Pas de résultat uniforme lorsque les écarts se ferment, à la limite thermodynamique ou pour toute règle de réinitialisation. |
| **PDF et sources** | [PDF](projects/phys-00002-p15/paper.pdf) · [TeX](projects/phys-00002-p15/manuscript/main.tex) · [Bib](projects/phys-00002-p15/manuscript/references.bib) · [Code / data](projects/phys-00002-p15) · `python reproducibility/reproduce.py --project phys-00002-p15` |

</details>

<details>
<summary><strong>05 · Un couple moteur peut-il réduire le bruit des courants ?</strong> — Preuve · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Un entraînement hors équilibre modifie les fluctuations. Comparer au même piège à l’équilibre isole son effet. |
| **Résultat et portée** | Dans le modèle OU sous-amorti stable, sans champ et soumis à un couple, le bruit des courants de position de degrés un/trois est au moins celui de l’équilibre correspondant. |
| **Contribution proposée** | Calculs polynomiaux exacts et représentations indépendantes de Wick/Poisson identifient l’excès positif et les cas d’égalité des courants de bord gradients. |
| **Limites et obstacles** | Modèle et degrés limités ; forces non linéaires, champs magnétiques et degrés supérieurs restent hors du théorème. |
| **PDF et sources** | [PDF](projects/phys-00003-p01/paper.pdf) · [TeX](projects/phys-00003-p01/manuscript/main.tex) · [Bib](projects/phys-00003-p01/manuscript/references.bib) · [Code / data](projects/phys-00003-p01) · `python reproducibility/reproduce.py --project phys-00003-p01` |

</details>

<details>
<summary><strong>06 · Deux batteries quantiques bruitées : les entrées conjointes aident-elles ?</strong> — Preuve · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Les corrélations peuvent modifier le travail extractible. L’amortissement d’amplitude généralisé décrit une relaxation à température finie. |
| **Résultat et portée** | Le manuscrit prouve W2(e)=2W1(e) dans le cadre énergétique à deux utilisations, avec états complexes et extraction unitaire globale. |
| **Contribution proposée** | Réduction des phases et certificat polynomial exact de positivité ferment cette optimisation. |
| **Limites et obstacles** | Ne couvre ni tous les canaux, ni un nombre arbitraire d’utilisations, ni toutes les définitions opérationnelles du travail. |
| **PDF et sources** | [PDF](projects/phys-00004-p01/paper.pdf) · [TeX](projects/phys-00004-p01/manuscript/main.tex) · [Bib](projects/phys-00004-p01/manuscript/references.bib) · [Code / data](projects/phys-00004-p01) · `python reproducibility/reproduce.py --project phys-00004-p01` |

</details>

<details>
<summary><strong>07 · Un contre-exemple exact de qutrit à une conjecture d’incertitude</strong> — Réfutation · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | L’incertitude entropique limite la prédictibilité simultanée de mesures incompatibles. Un résumé spectral peut perdre une information essentielle. |
| **Résultat et portée** | Une matrice unitaire rationnelle de dimension trois réfute la conjecture extended-MUB étudiée. |
| **Contribution proposée** | Un certificat arithmétique compact montre pourquoi la deuxième valeur singulière ne suffit pas à garantir l’énoncé universel proposé. |
| **Limites et obstacles** | Réfutation d’une conjecture précise, pas du principe d’incertitude ; une inégalité optimale de remplacement reste à trouver. |
| **PDF et sources** | [PDF](projects/phys-00004-p02/paper.pdf) · [TeX](projects/phys-00004-p02/manuscript/main.tex) · [Bib](projects/phys-00004-p02/manuscript/references.bib) · [Code / data](projects/phys-00004-p02) · `python reproducibility/reproduce.py --project phys-00004-p02` |

</details>

<details>
<summary><strong>08 · Un graphe à 16 sommets bat le chemin</strong> — Réfutation · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Le mélange moyen des marches quantiques décrit les retours persistants et éclaire les questions extrémales de transport. |
| **Résultat et portée** | Un graphe connexe simple non pondéré de 16 sommets et 62 arêtes a une laziness de 1673/1192 contre 23/16 pour le chemin, soit -81/2384 de différence. |
| **Contribution proposée** | Deux représentations exactes certifient un contre-exemple fini à la minimalité proposée du chemin pour la marche laplacienne considérée. |
| **Limites et obstacles** | Ne classe pas tous les minimiseurs, tailles de graphes, hamiltoniens ou conventions de normalisation. |
| **PDF et sources** | [PDF](projects/phys-00005-p01/paper.pdf) · [TeX](projects/phys-00005-p01/manuscript/main.tex) · [Bib](projects/phys-00005-p01/manuscript/references.bib) · [Code / data](projects/phys-00005-p01) · `python reproducibility/reproduce.py --project phys-00005-p01` |

</details>

<details>
<summary><strong>09 · Une mémoire quantique invalide une contraction universelle proposée</strong> — Réfutation · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | Les bornes de contraction quantifient la perte de distinguabilité. Une mémoire quantique peut changer ce qui est vrai sans système auxiliaire. |
| **Résultat et portée** | Un exemple exact d’amortissement d’amplitude, avec entrées intriquées à marginales égales, réfute le remplacement alpha-Doeblin hockey-stick universel proposé. |
| **Contribution proposée** | Le certificat isole un mécanisme sensible à la mémoire en respectant les contraintes initiales. |
| **Limites et obstacles** | Ne réfute pas toutes les inégalités de Doeblin et ne fournit pas une borne optimale de remplacement. |
| **PDF et sources** | [PDF](projects/phys-00006-p01/paper.pdf) · [TeX](projects/phys-00006-p01/manuscript/main.tex) · [Bib](projects/phys-00006-p01/manuscript/references.bib) · [Code / data](projects/phys-00006-p01) · `python reproducibility/reproduce.py --project phys-00006-p01` |

</details>

<details>
<summary><strong>10 · Quand la boundariness se multiplie-t-elle exactement ?</strong> — Résultat partiel · brouillon archivé · Déplier le tableau scientifique</summary>

| | |
|---|---|
| **Contexte** | La boundariness caractérise la position d’un canal dans son ensemble convexe. Les produits tensoriels font apparaître une structure supplémentaire. |
| **Résultat et portée** | Multiplicativité exacte pour une famille explicite de matrices de Choi de qubit, non unitales, de rang plein, à deux paramètres &#124;s&#124;, &#124;t&#124; ≤ 1/5. |
| **Contribution proposée** | Les vérifications symboliques de Choi, Sturm et LDL rendent l’optimum tensoriel accessible dans cette famille. |
| **Limites et obstacles** | La question générale reste ouverte. Le contrôle historique du paquet a échoué sur la liaison preuve/manuscrit ; le PDF est conservé comme brouillon archivé, sans validation de cette porte de sortie. |
| **PDF et sources** | [PDF](projects/phys-00007-p01/paper.pdf) · [TeX](projects/phys-00007-p01/manuscript/main.tex) · [Bib](projects/phys-00007-p01/manuscript/references.bib) · [Code / data](projects/phys-00007-p01) · `python reproducibility/reproduce.py --project phys-00007-p01` |

</details>


## Reproduire les résultats

Les nouveaux essais utilisent Python 3.12. L’exemple du qutrit nécessite seulement la bibliothèque standard. Pour tous les projets, installer les dépendances scientifiques figées dans un environnement virtuel. Le programme travaille sur des copies et préserve les preuves archivées. Aucun compte IA, clé API ou navigateur connecté n’est nécessaire.

```bash
# Standard-library-only exact counterexample
python3 projects/phys-00004-p02/reproducibility/verify_counterexample.py

# Full scientific environment and replay
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python reproducibility/reproduce.py --all
```

Commandes, résultats et limites figurent dans [reproducibility/VALIDATION.md](reproducibility/VALIDATION.md). Un code de sortie nul n’est pas une preuve scientifique. Arithmétique exacte, certificats par intervalles, haute précision et tests flottants ont des forces probantes différentes.
Chaque projet contient TeX, Bib et figures. Voir [reproducibility/README.md](reproducibility/README.md) pour les essais et la compilation. Les PDF archivés restent inchangés ; une autre distribution TeX peut produire des octets différents.

## Une exception historique de validation

`phys-00007-p01` possède un PDF et des calculs symboliques exécutables, mais son contrôle historique de paquet a échoué sur la correspondance entre preuves et manuscrit. Il reste signalé comme brouillon archivé. Un nouveau paquet ou un essai réussi ne remplace ni ce contrôle ni une nouvelle validation scientifique.

## Attribution et réutilisation

Les manuscrits portent le nom de **Xiaojian Zeng** ; informations et approbation finale restent à confirmer par l’auteur. L’assistance IA et informatique est déclarée. Ce conditionnement n’accorde aucune licence supplémentaire open source ou Creative Commons ; les droits restent aux titulaires concernés. Les articles tiers sont cités, sans redistribution. Les dépendances conservent leurs licences.
