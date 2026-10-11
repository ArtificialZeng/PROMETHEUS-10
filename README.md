# PROMETHEUS-10

**AI Physics, Made Verifiable**

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [日本語](README.ja.md)

Ten AI-driven physics manuscripts, with the code needed to inspect their claims. PROMETHEUS-10 brings automated proof search, counterexample construction and controlled computation into one inspectable research collection. The number 10 counts manuscripts—not ten universally solved problems.

Historical internal review records: **4 proofs + 3 disproofs, 2 partial-result notes and 1 computational paper**. No conjecture-only PDF. These are research drafts awaiting author review, not externally peer-reviewed or accepted publications.

AI contributed to derivations, code, numerical searches, checking and manuscript preparation under human direction. Separate AI review contexts are not external peer review. The novelty column states the manuscript’s proposed contribution; this packaging pass does not establish priority through a new comprehensive literature review.

| Project | Claim class | Details |
|---|---|---|
| [phys-00002-p01](projects/phys-00002-p01/paper.pdf) · How much noise does a qubit need? | Partial result | ↓ 01 |
| [phys-00002-p02](projects/phys-00002-p02/paper.pdf) · Four qubit measurements: the exact compatibility threshold | Proof | ↓ 02 |
| [phys-00002-p06](projects/phys-00002-p06/paper.pdf) · A four-level Mpemba witness beyond three-level tests | Computational result | ↓ 03 |
| [phys-00002-p15](projects/phys-00002-p15/paper.pdf) · Critical resetting erases coherence—at a controlled rate | Proof | ↓ 04 |
| [phys-00003-p01](projects/phys-00003-p01/paper.pdf) · Can torque lower the noise of a Gaussian particle? | Proof | ↓ 05 |
| [phys-00004-p01](projects/phys-00004-p01/paper.pdf) · Two noisy quantum batteries: can joint inputs help? | Proof | ↓ 06 |
| [phys-00004-p02](projects/phys-00004-p02/paper.pdf) · An exact qutrit counterexample to an uncertainty conjecture | Disproof | ↓ 07 |
| [phys-00005-p01](projects/phys-00005-p01/paper.pdf) · A 16-vertex graph defeats path minimality | Disproof | ↓ 08 |
| [phys-00006-p01](projects/phys-00006-p01/paper.pdf) · A qubit memory breaks a universal contraction proposal | Disproof | ↓ 09 |
| [phys-00007-p01](projects/phys-00007-p01/paper.pdf) · When channel boundariness multiplies exactly | Partial result · archived draft | ↓ 10 |

<details>
<summary><strong>01 · How much noise does a qubit need?</strong> — Partial result · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Lindblad generators describe memoryless open-system dynamics. Can a single jump operator reach the full boundary of the qubit population-transfer region? |
| **Result and original-problem scope** | A certified finite-radius local optimality result near the a=1/2 one-jump stationary point, against rank-at-most-two perturbations. The original global question remains open. |
| **Proposed contribution** | An explicit interval certificate turns a numerical stationary point into a checkable local exclusion region for competing generators. |
| **Limitations / bottlenecks** | Local radius 10^-4; this does not establish the global embedding boundary or exclude distant competitors. |
| **PDF and source** | [PDF](projects/phys-00002-p01/paper.pdf) · [TeX](projects/phys-00002-p01/manuscript/main.tex) · [Bib](projects/phys-00002-p01/manuscript/references.bib) · [Code / data](projects/phys-00002-p01) · `python reproducibility/reproduce.py --project phys-00002-p01` |

</details>

<details>
<summary><strong>02 · Four qubit measurements: the exact compatibility threshold</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Noisy quantum measurements can sometimes be implemented as marginals of a single parent measurement. Where is the noise threshold? |
| **Result and original-problem scope** | The draft proves the threshold 1/D for four strictly ordered planar, unbiased binary qubit measurements with common visibility. |
| **Proposed contribution** | Matching constructive and dual bounds give an analytic threshold; SOCP/SDP checks corroborate the formula. |
| **Limitations / bottlenecks** | Restricted to this four-measurement geometry and noise model; not a theorem for arbitrary POVMs or all measurement counts. |
| **PDF and source** | [PDF](projects/phys-00002-p02/paper.pdf) · [TeX](projects/phys-00002-p02/manuscript/main.tex) · [Bib](projects/phys-00002-p02/manuscript/references.bib) · [Code / data](projects/phys-00002-p02) · `python reproducibility/reproduce.py --project phys-00002-p02` |

</details>

<details>
<summary><strong>03 · A four-level Mpemba witness beyond three-level tests</strong> — Computational result · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | In some thermal relaxation models, a hotter preparation can relax faster. Conditions found in three levels need not govern larger systems. |
| **Result and original-problem scope** | A four-level positive-temperature detailed-balance witness survives independent 100- and 180-digit calculations while the tested three-level necessary predicates are excluded. |
| **Proposed contribution** | A concrete higher-dimensional mechanism tests the limits of reducing thermal relaxation to three-level diagnostics. |
| **Limitations / bottlenecks** | Computational paper; high precision is not directed-rounding certification or a general classification. The original question remains unresolved. |
| **PDF and source** | [PDF](projects/phys-00002-p06/paper.pdf) · [TeX](projects/phys-00002-p06/manuscript/main.tex) · [Bib](projects/phys-00002-p06/manuscript/references.bib) · [Code / data](projects/phys-00002-p06) · `python reproducibility/reproduce.py --project phys-00002-p06` |

</details>

<details>
<summary><strong>04 · Critical resetting erases coherence—at a controlled rate</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Random resetting changes long-time quantum dynamics. The critical Sibuya exponent separates qualitatively different renewal regimes. |
| **Result and original-problem scope** | For alpha=1 and a fixed finite-dimensional unitary register, the draft proves trace-norm convergence to spectral pinching, with fixed-gap rates. |
| **Proposed contribution** | A critical-case asymptotic theorem connects renewal coefficients to decay of off-diagonal quantum coherence. |
| **Limitations / bottlenecks** | Fixed dimension and fixed spectral gaps; no uniform closing-gap, thermodynamic-limit or arbitrary-reset theorem. |
| **PDF and source** | [PDF](projects/phys-00002-p15/paper.pdf) · [TeX](projects/phys-00002-p15/manuscript/main.tex) · [Bib](projects/phys-00002-p15/manuscript/references.bib) · [Code / data](projects/phys-00002-p15) · `python reproducibility/reproduce.py --project phys-00002-p15` |

</details>

<details>
<summary><strong>05 · Can torque lower the noise of a Gaussian particle?</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Nonequilibrium driving changes current fluctuations. Comparing with the same equilibrium trap tests whether a drive can suppress noise. |
| **Result and original-problem scope** | For the stable, zero-field, torque-driven underdamped Ornstein–Uhlenbeck model, degree-one/three position-current noise is bounded below by the matched equilibrium value. |
| **Proposed contribution** | Exact polynomial and independent Wick/Poisson calculations identify the nonnegative excess and gradient-boundary equality cases. |
| **Limitations / bottlenecks** | Restricted dynamics and polynomial current class; nonlinear forces, magnetic fields and higher degrees are outside the theorem. |
| **PDF and source** | [PDF](projects/phys-00003-p01/paper.pdf) · [TeX](projects/phys-00003-p01/manuscript/main.tex) · [Bib](projects/phys-00003-p01/manuscript/references.bib) · [Code / data](projects/phys-00003-p01) · `python reproducibility/reproduce.py --project phys-00003-p01` |

</details>

<details>
<summary><strong>06 · Two noisy quantum batteries: can joint inputs help?</strong> — Proof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Quantum battery work extraction may benefit from correlations. Generalized amplitude damping models a finite-temperature relaxation channel. |
| **Result and original-problem scope** | The draft proves W2(e)=2W1(e) for the stated two-use energy-constrained setting, including complex input states and global unitary extraction. |
| **Proposed contribution** | A phase reduction and exact polynomial positivity certificate close the two-use optimization in this model. |
| **Limitations / bottlenecks** | No claim for arbitrary channel families, arbitrarily many uses, or alternative operational definitions of work. |
| **PDF and source** | [PDF](projects/phys-00004-p01/paper.pdf) · [TeX](projects/phys-00004-p01/manuscript/main.tex) · [Bib](projects/phys-00004-p01/manuscript/references.bib) · [Code / data](projects/phys-00004-p01) · `python reproducibility/reproduce.py --project phys-00004-p01` |

</details>

<details>
<summary><strong>07 · An exact qutrit counterexample to an uncertainty conjecture</strong> — Disproof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Entropic uncertainty asks how incompatible measurements limit simultaneous predictability. Spectral summaries can discard relevant structure. |
| **Result and original-problem scope** | An exact rational three-dimensional unitary construction refutes the tested extended-MUB conjecture. |
| **Proposed contribution** | A compact rational-arithmetic certificate shows why the second singular value alone cannot enforce the proposed universal claim. |
| **Limitations / bottlenecks** | A counterexample to a specific conjecture, not to the uncertainty principle. A replacement sharp inequality remains to be found. |
| **PDF and source** | [PDF](projects/phys-00004-p02/paper.pdf) · [TeX](projects/phys-00004-p02/manuscript/main.tex) · [Bib](projects/phys-00004-p02/manuscript/references.bib) · [Code / data](projects/phys-00004-p02) · `python reproducibility/reproduce.py --project phys-00004-p02` |

</details>

<details>
<summary><strong>08 · A 16-vertex graph defeats path minimality</strong> — Disproof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Quantum-walk average mixing measures persistent return structure. Extremal graph claims can guide intuition about transport and localization. |
| **Result and original-problem scope** | A connected simple unweighted 16-vertex, 62-edge graph has laziness 1673/1192 versus 23/16 for the path: a difference of -81/2384. |
| **Proposed contribution** | Two exact representations certify a finite counterexample to the specified Laplacian-walk path-minimality claim. |
| **Limitations / bottlenecks** | Does not classify minimizers at all graph sizes or settle other Hamiltonians and normalization conventions. |
| **PDF and source** | [PDF](projects/phys-00005-p01/paper.pdf) · [TeX](projects/phys-00005-p01/manuscript/main.tex) · [Bib](projects/phys-00005-p01/manuscript/references.bib) · [Code / data](projects/phys-00005-p01) · `python reproducibility/reproduce.py --project phys-00005-p01` |

</details>

<details>
<summary><strong>09 · A qubit memory breaks a universal contraction proposal</strong> — Disproof · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Channel contraction bounds quantify distinguishability loss. Adding quantum memory can invalidate intuition from unassisted inputs. |
| **Result and original-problem scope** | An exact amplitude-damping example with valid equal-marginal entangled inputs refutes the proposed universal alpha-Doeblin hockey-stick replacement. |
| **Proposed contribution** | The certificate isolates a concrete memory-sensitive failure under the original input constraints. |
| **Limitations / bottlenecks** | Refutes the specified strengthened bound; does not invalidate every Doeblin inequality or provide an optimal replacement. |
| **PDF and source** | [PDF](projects/phys-00006-p01/paper.pdf) · [TeX](projects/phys-00006-p01/manuscript/main.tex) · [Bib](projects/phys-00006-p01/manuscript/references.bib) · [Code / data](projects/phys-00006-p01) · `python reproducibility/reproduce.py --project phys-00006-p01` |

</details>

<details>
<summary><strong>10 · When channel boundariness multiplies exactly</strong> — Partial result · archived draft · Click to expand the research table</summary>

| | |
|---|---|
| **Background** | Boundariness measures proximity to the boundary of a convex channel set. Tensor products may expose structure invisible in one copy. |
| **Result and original-problem scope** | Exact multiplicativity is proved within an explicit two-parameter full-rank non-unital qubit Choi family, &#124;s&#124;, &#124;t&#124; ≤ 1/5. |
| **Proposed contribution** | Symbolic Choi, Sturm and LDL checks support an explicit family where the tensor-product optimum is tractable. |
| **Limitations / bottlenecks** | The general problem remains open. Historical submission-bundle gate failed evidence/manuscript binding; PDF is included as an archived draft, not a gate-cleared release. |
| **PDF and source** | [PDF](projects/phys-00007-p01/paper.pdf) · [TeX](projects/phys-00007-p01/manuscript/main.tex) · [Bib](projects/phys-00007-p01/manuscript/references.bib) · [Code / data](projects/phys-00007-p01) · `python reproducibility/reproduce.py --project phys-00007-p01` |

</details>


## Reproduce the results

Python 3.12 was used for this replay. The qutrit example below uses only the Python standard library. For all projects, install the pinned scientific dependencies into a virtual environment. The runner copies each project into a new output directory before executing checks, keeping archived evidence unchanged. This archive does not require an AI account, API key or browser session.

```bash
# Standard-library-only exact counterexample
python3 projects/phys-00004-p02/reproducibility/verify_counterexample.py

# Full scientific environment and replay
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python reproducibility/reproduce.py --all
```

Fresh replay outcomes, commands and limitations are recorded in [reproducibility/VALIDATION.md](reproducibility/VALIDATION.md). Exit-zero alone is not a scientific certificate. Exact arithmetic, interval certificates, high-precision witnesses and floating-point stress tests have different evidential strength; the individual papers specify which is used.
Manuscript sources and figures are included with each project. See [reproducibility/README.md](reproducibility/README.md) for replay and PDF rebuilding. Archived PDF bytes are preserved; compiling on another TeX distribution need not produce identical PDF bytes.

## One historical exception

`phys-00007-p01` has a PDF and reproducible symbolic calculations, but its historical submission-bundle gate failed an evidence/manuscript binding check. It remains prominently labeled as an archived draft. Packaging and a successful code replay do not clear that gate or constitute renewed scientific approval.

## Attribution and reuse

The manuscripts list **Xiaojian Zeng**; author details and final approval remain subject to author confirmation. The collection discloses AI and computational assistance. No additional open-source or Creative Commons license is granted by this packaging step; rights remain with their respective holders. Third-party research papers are cited, not redistributed. Dependencies retain their own licenses.
