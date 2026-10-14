# Frozen finite physical diagnostic model, research pass 1

This file records the actual stationary model behind the new numerical lead.
It is not a claim of a certified universal disproof. Complete parameter output
and calculations are r1-tightbinding-validation.py/.json/.log. This model uses
exact semi-infinite normal tight-binding leads, rather than a wide-band contact
approximation. No reservoir or controller is attached at the internal joins.

## Hamiltonian and boundaries

Units are epsilon=k_B T_ref, time h/epsilon, k_B=h=T_ref=1. There are
three identical one-channel semi-infinite leads a=0,1,2. Each has onsite
2 t_lead=20000 and nearest-neighbor hopping -t_lead=-10000, with spectrum
[0,40000]. Outside that band there are no propagating channels. Boundary
conditions are incoming thermal modes from the reservoir, and outgoing
retarded modes absorbed by it. The lead surface Green function is

    g_lead(E)=[E-2t_lead-i sqrt(E(4t_lead-E))]/(2t_lead^2)

inside the band, with the usual retarded analytic continuation outside.
It follows independently from the quadratic surface recurrence and from
the outgoing Bloch ratio exp(ik), E=2t_lead-2t_lead cos(k).

The finite sample contains three n=128 site filter chains and three core
dots, 387 sites total. Let E0=5000, w=0.02, Gamma_c=200000,

    Gamma_f=w/[4 sin(pi/(2n))],
    h_l=w/[4 sqrt(sin((2l+1)pi/(2n)) sin((2l-1)pi/(2n)))],
    l=1,...,n-1, lambda=sqrt(Gamma_f Gamma_c).

These h_l and Gamma_f use the reproduced PRL Eq. (24) convention, not the
inconsistent literal JPA Eq. (67). Label filter sites (a,l) and core sites c_a.
All sample onsite energies are E0, except the outer filter site (a,1),
whose onsite is E0-Re Sigma(E0), where

    V_contact^2=2 t_lead^2 Gamma_f/sqrt(E0(4t_lead-E0)),
    Sigma(E)=V_contact^2 g_lead(E).

Real nearest-neighbor filter hoppings are h_l. Real hopping lambda joins
(a,n) to c_a. Each outer site (a,1) couples by real V_contact to the end
of lead a. On the three core sites add the Hermitian flux ring

    H_core-E0 I=i Gamma_c(P-P^T),
    P=[[0,0,1],[1,0,0],[0,1,0]].

Its directed hopping product has nonzero magnetic flux (a phase of magnitude
pi/2); time reversal conjugates and reverses the ring. H_sample is explicitly
Hermitian, finite, time independent and particle-number preserving. There is
no interaction, anomalous pairing, driving or extra bath. Bound sample modes
outside the lead band carry no reservoir current in this noninteracting model.

At E inside the lead band define Gamma(E)=-Im Sigma(E)>0 and let G be the
sample retarded resolvent, with Sigma on all three outer sites. The
flux-normalized scattering matrix is

    S_ab(E)=delta_ab-2i Gamma(E) G_[(a,1),(b,1)](E).

The resolvent identity G-G^dagger=-2i Gamma G P_outer G^dagger proves
unitarity. This uses the actual energy-dependent contact self-energy.

## Reservoirs and measured statistics

Every reservoir has T_a=1>0, with fixed finite chemical potentials
mu=(5001,4997,4976). At each energy f_a=1/[1+exp(E-mu_a)]. All three
currents are injected into the sample, using the source outgoing-row
transmissions. The entropy is exactly sigma=-sum Q_a/T_a, with all three
reservoirs included. Since temperatures agree and sum J_a=0, it also equals
sum(mu_a-E0)J_a. That latter identity is merely a numerically stable
evaluation of the same actual entropy; no event-reversal entropy is used.

Count extracted particles from lead 0. Because that lead has one channel,
at a fixed energy the possible count is -1,0,1, with

    p_+=f_0 sum_(b!=0) |S_0b|^2(1-f_b),
    p_-=(1-f_0) sum_(b!=0) |S_0b|^2 f_b,
    p_0=1-p_+-p_-.

This marginal is independently checked against the original Levitov
determinant and the exterior-power Fock probabilities in
r1-tightbinding-input-checks.json. The counting field is s=-24. The CGF
is the energy integral of log[p_0+p_+ exp(s)+p_- exp(-s)], divided by h.

## Independent numerical representations

A eliminates the filter chains by a banded retarded Green solve and then
a 3x3 core Schur complement. B reconstructs the outer lead self-energy
from the outward Bloch solution and uses three Fourier-sector backward
continuant recurrences. The two programs use independent equivalent trig
forms of the PRL hoppings. A uses composite Gauss panels; B uses an adaptive
integral with an independently selected panel grid. B does not consume
A's cached answers. Their parameters, libraries, sources and proposer are
shared; this is weaker than a fresh independent referee.

The finite-width calculation is exact at the Hamiltonian/model level. Its
integration is numerical. It is not a narrow-width truncation, a replacement
of reservoirs by freely chosen energy occupations, or an infinite-chain
limit. n changes in the discovery records are different physical samples;
quadrature-order/tolerance changes at fixed n test numerical convergence.

## Tails and current-domain conversion

The numeric integral uses delta=E-E0 in [-80,160], which lies inside the
lead band. For delta<-80 all three hole probabilities are bounded by
exp(delta+24). For delta>160 all particle probabilities are bounded by
exp(1-delta). A nonzero extracted count requires at least one hole or one
particle respectively; its absolute magnitude is <=1. For these small
tail probabilities, |log M|<=2 exp(|s|) times their sum. Thus the absolute
CGF tail outside the numerical interval is bounded by

    6 exp(24-56)+6 exp(24+1-160),

less than 8e-14 in epsilon/h. Current tails are bounded by the corresponding
unamplified particle/hole probabilities. Entropy tails can be bounded by
sum |mu_a-E0|=28 times a conservative current bound, so are negligible
relative to the discovered gap. The physical integration remains E>=0,
with no channels above 40000; extending the exponential tail estimate
beyond the actual lead band only makes the estimate larger.

The exact dual and conservative psi_0 control are in
r1-legendre-cycle-derivation.md and r1-exact-psi-control.md. If a strict
chi(-24)<H_(1/2)(-24) is rigorously enclosed, those arguments transfer it
to the exact psi_0 and to the interior current j_B(psi_0,-24). The actual
Legendre saddle of chi need not be presumed equal to that current.

Remaining gap: sharp filter-edge structures need an independent integrated
error enclosure. Adaptive error estimates and order agreement alone are
not certified enclosures; early numerical differences are preserved rather
than silently passed. No original-problem resolution is asserted here.
