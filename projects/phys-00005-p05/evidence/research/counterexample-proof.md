# Exact phase-obstructed K4 parity reversal

Proposer: phys-00005-p05-research-209d50c0d18e, 2026-10-12. This is a proposed resolution of the universal question in source.md/problem.md, not referee acceptance. Source.md is unchanged. All decisive arguments are in stable files; mutable handoffs are not inputs.

## Model and legal witness

Take V={0,1,2,3}, all six unordered edges, in order 01,02,03,12,13,23. Set s=3/4 and u=exp(i theta)=(1,1,1,1,-1,-1). Every edge still has weight +1 in the negative unnormalized projector Hamiltonian. A minus phase is an off-diagonal pairing phase, not a negative edge weight. The graph is simple, connected, nonbipartite (triangle 012), and contains the even cycle 01230. Its alternating phase product u01*u23/(u12*u03)=-1, so its alternating angle is pi modulo 2pi. Under vertex Z rotations uij multiplies by eta_i eta_j, which cancels in that product. Thus the phase cannot be eliminated by those rotations. The strict interior parameter, all boundary interactions, units and parity are exactly those of problem.md. No weights, additional fields, truncation or bath are introduced.

On each edge -|phi><phi| sends 00 to -00-s*u*11, and 11 to -s*conjugate(u)*00-s^2*11, annihilating 01 and 10. This is Hermitian and changes Hamming weight only by two. Hence the full 16-dimensional Hamiltonian separates into 8-dimensional even/odd sectors, including all multiplicities.

Two reconstruction paths are retained: matrix-unit Kronecker embedding (A, vertex 0 MSB) and bitstring ket-bra action (B, vertex 0 LSB). code/certify_k4.py proves their exact entry equality under bit reversal and their sector polynomial equality, saves both matrices, and checks exact parity and Hermiticity. These implementations are distinct, but performed by the same proposer with shared model and SymPy; fresh scientific review remains mandatory.

## Exact sector reduction

Write x for the energy variable and d=1+s^2. In the even sector, order the vacuum, six weight-two strings, and full string. The diagonal is (-6,-d I6,-6s^2). The two coupling vectors into the middle layer are a=(-s,-s,-s,-s,s,s) and b=(s,s,-s,-s,-s,-s) in B's ordered weight-two basis [3,5,6,9,10,12]. Their squared norms are 6s^2 each and a dot b=-2s^2. The four-dimensional common orthogonal complement has energy -d. A Schur complement yields

p_e(x)=(x+d)^4 {[(x+6)(x+d)-6s^2][(x+6s^2)(x+d)-6s^2]-4s^4}.

In the odd sector reorder weight-one strings before weight-three strings. The diagonal blocks are -3 I4 and -3s^2 I4. The pairing block C has CC^T eigenvalues 5s^2,5s^2,s^2,s^2 (this is directly checkable from the saved matrix). Consequently

p_o(x)=[x^2+3(1+s^2)x+4s^2]^2 [x^2+3(1+s^2)x+8s^2]^2.

Both formulas are also verified by symbolic characteristic polynomials directly from the two full matrices, without relying on this reduction.

At s=3/4, define

Q(x)=2048x^4+25600x^3+92648x^2+90075x+20736.

Then

p_e(x)=(16x+25)^4 Q(x)/134217728,
p_o(x)=(16x^2+75x+36)^2(16x^2+75x+72)^2/65536.

## Certified ordering

Exact rational Sturm counts give one root of Q in each of

(-669/100,-667/100), (-449/100,-447/100), (-51/50,-1), (-17/50,-33/100).

These four disjoint intervals exhaust its degree. The other four even eigenvalues are -25/16. Thus Ee1 is the first quartic root, and Ee2 the second. In particular Ee1<-6<Ee2<-89/20.

The lowest odd energy is Eo1=(-75-sqrt(3321))/32. Because 3321<(289/5)^2 and both square roots are positive, Eo1>-83/20. Therefore

Ee2 < -89/20 < -83/20 < Eo1,
Eo1-Ee2 > 3/10.

As a separate exact certificate, LDL congruences at rational thresholds give inertia(H_even+89 I/20)=(2 negative,6 positive,0 zero), and inertia(H_odd+83 I/20)=(0 negative,8 positive,0 zero). The exact pivots and checked L D L^T identities are in exact-certificate.json/exact-check.log. Sylvester inertia therefore confirms two even eigenvalues below -89/20 and no odd eigenvalue below -83/20. This supplies a second exact checking method rather than an eigensolver fit.

The first quartic root is simple and lower than every other level, including all odd levels. The global ground state is uniquely even; the global first excitation is also even. The universal Eo1<=Ee2 statement of this project is disproved by this legal witness. This does not refute the phase-free Conjecture 2 in Wong et al.; it answers negatively its proposed phase extension within the project's explicit restricted domain. Neither a global gap bound nor ground-state uniqueness is refuted.

## Robustness to amplitude and phase perturbations

Keep K4 and let |s'-3/4|<1/1000 and each wrapped angle deviation |theta'_e-theta_e|<1/1000. Throughout this box 0<s'<1. For an edge, triangle inequalities on the 00/11 block give

||h(s',u')-h(s,u)|| <= |s'^2-s^2|+|s'u'-su| <= 3|s'-s|+|theta'-theta|.

Here |s'^2-s^2|<=2|s'-s| and |s'u'-su|<=|s'-s|+s|u'-u|, with |u'-u|<=|delta theta|. Tensoring the block by spectator identities preserves its norm. Summing the six edges gives ||Delta H||<24/1000. The perturbation preserves parity, so Weyl's eigenvalue bound applies separately to both sectors, with multiplicities. Thus

Eo1'-Ee2' > 3/10 - 48/1000 = 252/1000 > 0.

The alternating angle on cycle 01230 remains within 4/1000 of pi and cannot be zero modulo 2pi. The witness therefore lies inside a legal open set, including complex unit phases, not only a discrete sign pattern or endpoint degeneracy. Ground-state uniqueness also persists: the certified initial separation exceeds 2 energy units, much larger than 48/1000.

## Physical consequence and limits

The true spectral gap here is Ee2-Ee1. Using only the lowest odd level produces Eo1-Ee1 and overestimates the gap by more than 3/10 in the edge energy unit. This matters when applying the suggested odd-sector reduction to phase-frustrated pairing Hamiltonians. An odd-parity probe acting on the even ground state cannot access an even first excitation. No nonzero probe matrix element, response intensity, thermodynamic phase transition, experimental state, all-graph classification or phase-free disproof is claimed.

The invariant middle-layer couplings expose the role of pairing interference: obstruction changes coupling overlaps and sector spectra. No general mechanism theorem beyond these explicit reductions is asserted. Numerical approximations are only illustrative: Ee1 about -6.67805, Ee2 about -4.47731, Eo1 about -4.14463. The strict statements depend on exact rational certificates, not those decimal values.

## Reproduction

From the project root, using an existing Python with SymPy 1.14.0:

    python3 code/certify_k4.py

The discovery scan separately requires NumPy and runs code/search_parity.py. It enumerated 48 legal sign assignments times 99 sampled s values, 4752 matrices, with 1488 floating reversals above 1e-9. That finite scan is discovery data only. Its entire table is preserved in k4-sign-scan.json. The exact proof uses the single specified witness and the analytic perturbation bound.
