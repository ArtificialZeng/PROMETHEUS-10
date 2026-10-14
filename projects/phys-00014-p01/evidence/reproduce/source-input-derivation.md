# Source input reconstruction and conventions

Job: phys-00014-p01-reproduce-71ca019db8ac. This is a reproduction dossier,
not a new result, attainment proof, or scientific acceptance. Its arguments
and computations are preserved in the stable files named below.

Primary input: Bia and Gagatsos, arXiv:2607.15398v1, local immutable
`literature/2607.15398v1.pdf`. Eqs. (3)-(8), (10), (13)-(20), (24)-(27),
and Section VI fix the quantities reproduced. The rendered PDF p.4 was
actually inspected at Eqs. (15)-(20); the minus-i sign, Pauli rather than
half-Pauli exponent, trace-two Choi operator, and tensor order were checked.
`evidence/reproduce/primary-page4.png` is that rendering. The existing
HTML/PDF date-header discrepancy is preserved without inferring a version.

## Independent input A

`input_a.py` transcribes the source channel and constructs every 2 by 2
matrix-unit output directly. For E_ab=|a><b|,

    Lambda(E_ab)=(1-lambda) U E_ab Udag + lambda delta_ab I_2/2,
    J=sum_ab E_ab tensor Lambda(E_ab),
    rho=W J Wdag/2.

Using delta_ab in the noise term is essential for a linear channel on
off-diagonal matrix units. U is evaluated by a matrix exponential of the
three explicitly transcribed Pauli matrices. The script does not use the
spin coefficients, their closed formulas, input B, or its producer code.
It integrates the matrices and theta_i-weighted matrices over independent
r, mu=cos(polar angle), phi coordinates, with radial density 3r^2/a^3,
mu density 1/2, phi density 1/(2pi), and a=pi/4. It also records the r^2
moment, allowing the prior cost to be checked directly from a state integral.
Three increasing quadratures are saved. The angular dependence of rho and
theta_i rho has degrees two and three; the smallest product rule integrates
the necessary directional monomials exactly in exact arithmetic. Matrix
exponentials and summation here are double precision, so actual numerical
convergence and comparison to B, rather than a hash, provide error evidence.

## Independent input B

`input_b.py` starts separately from the source's Eq. (20),

    v=cos(r)|0> - i sin(r) sum_i n_i |i>.

The spin columns are transcribed independently in source input-output
computational order 00,01,10,11:

    |0>=(1,0,0,1)/sqrt(2), |x>=(0,1,1,0)/sqrt(2),
    |y>=(0,i,-i,0)/sqrt(2), |z>=(1,0,0,-1)/sqrt(2).

These follow directly from (I tensor sigma_i)|Phi+>, not from an inferred
matrix in a summary. The producer reads none of A's files. Angular identities
E[n_i]=0, E[n_i n_j]=delta_ij/3, and vanishing odd direction moments give

    Gamma0=A E00+B(E11+E22+E33),
    Gamma_i=i Q(E0i-Ei0),
    A=(1-lambda) C+lambda/4,
    B=(1-lambda)(1-C)/3+lambda/4,
    Q=(1-lambda) q,
    C=(3/a^3) integral_0^a r^2 cos^2(r) dr,
    q=(1/a^3) integral_0^a r^3 sin(r)cos(r) dr.

Closed primitives at a=pi/4 give

    C=1/2+3/(4a)-3/(8a^3), q=3/(8a)-3/(16a^3).

For C, integrate r^2 cos(2r) to
r^2 sin(2r)/2+r cos(2r)/2-sin(2r)/4. For q, integrate
r^3 sin(2r) to -r^3 cos(2r)/2+3r^2 sin(2r)/4+
3r cos(2r)/4-3sin(2r)/8, and divide by 2a^3. The script
compares independent 80-digit radial quadrature with these primitives.
The r^2 state moment is obtained by an independent radial quadrature too.
This is same-worker independence of transcription/representation, weaker
than a fresh independent referee reconstruction. No referee is claimed.

## Exact convention map and optimized/Bell baseline map

W swaps the two qubits: W|a,o>=|o,a>. If S is the matrix of the four
source spin columns, T=W S maps spin coordinates to output-ancilla
computational coordinates. Consequently

    rho=W J Wdag/2, Gamma_A=T Gamma_B Tdag,
    M=2 W T_tester Wdag, Tr(M rho)=Tr(T_tester J).

All 16 entries of each of the four moments are compared row by row in
`input-comparison.json` and its actual command log. The pointwise Choi
operators are independently compared before integration; this catches a
wrong sigma_y transpose, swap, noise factor, or first-moment sign.

`exact_input_map.py` also reconstructs the source Choi matrix from the
matrix-unit channel and, separately, from the source spin columns using
real symbolic c=cos(r), h=sin(r) and direction components. Its angular
averaging of the computational matrix gives an exact entrywise match to
the spin moments for symbolic C, q and lambda. Every one of the 16 Choi
entries and 64 moment entries has zero symbolic residual, as do spin
orthonormality and separately integrated radial primitives. The complete
row-by-row result is in `exact-input-map.json` and its actual command log.

The source optimized probe is rotation invariant. At k=1 its marginal
sigma is a trace-one operator commuting with the irreducible fundamental
SU(2) input representation. Schur's lemma gives sigma=I_2/2. Eq. (13)
then gives exactly |Phi+>, up to an irrelevant ancillary unitary. This
specific source class is therefore the fixed-Bell class for k=1, so its
noiseless NH/SLD ratio can be reproduced in the Bell convention. This does
not say fixed Bell is optimal among all probes for k>1 or that arbitrary
noninvariant NH probe optimizations have been performed.

## Input admissibility, endpoints, dimensions, and units

All rotation parameters and cost are dimensionless. The model is the
exact finite-dimensional channel, with no perturbative order or truncation.
The defining domain is the compact Cartesian ball; the prior is not Haar
on SU(2) or uniform in radius. Normalization gives E[r^2]=3a^2/5 and
R_prior=E[r^2]/3=a^2/5=pi^2/80. At k copies every factor encodes the same
theta; products of separately averaged states cannot replace the joint
prior integral. Only k=1 has been numerically reconstructed in this job.

For every 0<=lambda<=1, rho is a convex combination of a rank-one
projector and I_4/4, with eigenvalues 1-3lambda/4 and lambda/4 (multiplicity
three). Thus positivity and trace one hold. J has twice these eigenvalues,
trace two, and partial trace over output I_2; U is unitary, and unitary
conjugation followed by depolarization is CPTP. Parallel tensor powers
preserve these input properties. Their measurements are physical joint
POVMs, not adaptive/sequential strategies. Individual outputs at lambda=0
are rank one. Nonetheless Gamma0 has A>0 and B>0 throughout [0,1]: both
cos^2 and sin^2 have positive radial prior average. The averaged matrix
needed in the source's SLD Lyapunov equation is therefore full rank even
at zero noise. This input fact is distinct from a theorem requiring every
individual output to have full rank. At lambda=1, all first moments vanish.

No essential matrix is missing for this k=1 reconstruction. Author code,
radial estimator grids, and a machine-readable Figure 1 are unavailable/
unverified; none is fabricated or needed to compare the rounded baseline.
