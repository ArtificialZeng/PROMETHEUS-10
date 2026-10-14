# Explicit doubled split-tree witness for the published hot-spot claim

Proposer: phys-00004-p08-research-2ff1f8ac82b0. Research pass 1.
This is stable proposer evidence, pending a fresh scientific referee. It is
neither an acceptance nor a publication draft. No conclusion below relies
on checkpoint.md or state.json.

## Claim, scope and source relationship

For every epsilon > 0 there is a finite connected compact metric multigraph
with the standard unweighted Kirchhoff Laplacian, no bridges, diameter 1,
simple first positive eigenvalue, and complete global maximum/minimum set
of diameter strictly less than epsilon. This is precisely the existence
statement in Kennedy--Rohleder, On the hot spots of quantum graphs,
arXiv:2003.14335v4, Conjecture 8.9, PDF p.26, interpreted with their
Section 4.2 definition of doubly connected: every point lies on a cycle.
It does not require vertex-biconnectivity. Parallel edges are allowed.

The comparison tree is a concrete parameter specialization of their
Example 6.2 (pp.20--21), with the prescribed leaf lengthening. Uniform
edge doubling is a known operation (e.g. Kennedy, Geometric spectral
theory of quantum graphs, arXiv:2310.02707v3, Section 4.3). The proposed
contribution is the exact conjecture consequence, not invention of
doubling, a new diffusion law, or novelty of symmetry decomposition.

## 1. A one-integer family

Let m be any integer >= 4, and set

    h_m = atan(1/sqrt(m))/pi,
    theta_m = atan(1/sqrt(2*m+1)),
    k_m = theta_m/h_m.

Construct a tree T_m with central vertex o, two long leaves l_1,l_2,
two fan hubs p,n, and m distinct leaves p_j and n_j at each fan.
There are two edges o--l_i of length a=1/2, two stems o--p and o--n
of length h=h_m, and 2m fan leaf edges of length b=2h. All lengths
are positive and finite. Every edge carries -d^2/dx^2; all vertices
have continuity and Kirchhoff flux, with Neumann conditions at leaves.

Since atan(1/2)<pi/6 (tan(pi/6)=1/sqrt(3)>1/2),

    0 < h <= atan(1/2)/pi < 1/6,
    b=2h < 1/3 < 1/2,
    h+b=3h < 1/2.

The unlengthened source fan has leaf length
atan(cot(pi*h)/m)/pi = atan(1/sqrt(m))/pi = h.
Thus b=2h is exactly the source perturbation delta=h on every fan
leaf, leaving stems and the two long arms unchanged. The argument
below proves its ordering directly, without relying on an unspecified
small-perturbation limit.

## 2. Complete first-positive spectral ordering on T_m

First separate the m leaf functions at each fan into their common mean
and m-1 zero-sum components. Continuity forces each zero-sum component
to vanish at its hub. Its leaf endpoint is Neumann and its hub flux
cancels in the zero sum. These are independent Dirichlet--Neumann
interval sectors of length b=2h, with wave numbers

    (2r+1)*pi/(4h),  r=0,1,2,...,

each of multiplicity m-1 per fan. Their first wave number is > pi
because h<1/6<1/4. All these sectors are retained; none is discarded
by division at a secular pole. The remaining subspace has equal leaf
functions at each fan.

Impose Dirichlet data at the central root of one equal-leaf fan.
Write the stem as S*sin(k*x), x from o to its hub, and every fan leaf
as C*cos(k*(b-y)), y from hub to leaf. Hub continuity and flux give

    C*cos(k*b) = S*sin(k*h),
    m*C*sin(k*b) = S*cos(k*h).

The pole-free characteristic is

    F(k) = cos(k*h)*cos(k*b) - m*sin(k*h)*sin(k*b).

For 0<k<=pi, both kh and kb lie in (0,pi/2). The function
m*tan(kh)*tan(kb) is strictly increasing, starts at 0, and equals 2m/(m-1)
at k=pi (because tan(pi*h)=1/sqrt(m)). Hence the first Dirichlet-root
wave number is the unique k in (0,pi) with that product equal to 1.
Putting z=tan(kh) and b=2h gives

    m * 2*z^2/(1-z^2) = 1,
    z^2 = 1/(2m+1),

so it is exactly k=k_m. This is a simple root, and the corresponding
fan solution space is one-dimensional. The two long arms with a
Dirichlet central root are DN intervals of length 1/2 and start at pi.

To exclude all lower modes with nonzero central value c, first note
that the preceding leaf zero-sum sectors have no modes below k_m.
For 0<k<k_m every long arm has outgoing central derivative

    c*k*tan(k/2),

and every common-leaf fan has outgoing central derivative

    c*k * [tan(kh)+m*tan(kb)]/[1-m*tan(kh)*tan(kb)].

Both coefficients are strictly positive in this whole interval.
Kirchhoff at o therefore cannot hold for c!=0. If c=0, all four
root-Dirichlet branches are invertible below k_m, so the solution is
zero. This excludes every positive eigenvalue below k_m^2.

At k=k_m, a nonzero central value is also impossible. With stem
c*cos(k*x)+S*sin(k*x) the exact equations are

    C*cos(kb)-S*sin(kh) = c*cos(kh),
    m*C*sin(kb)-S*cos(kh) = -c*sin(kh).

At the root, the left side of the second equation is cot(kh) times
the first. Compatibility would require
 -c*sin(kh) = c*cos(kh)^2/sin(kh), hence c=0.
With c=0, the long arms are zero (k_m<pi), and the two fans each have
one free stem amplitude S_+,S_-. The sole central flux condition is
k_m*(S_+ + S_-)=0. Thus there is exactly one eigendirection:

    mu_2(T_m)=k_m^2 < pi^2, with multiplicity one.

Zero is simple by the nonnegative energy form and connectedness.
The argument covers the entire operator, not only a symmetry ansatz.

## 3. Exact mode and the complete extrema set

Choose S_+=1 and S_-=-1. The two long arms are identically zero.
On the positive stem the function is sin(k_m*x), and on each positive
fan leaf it is C_m*cos(k_m*(2h-y)), where

    C_m = sin(theta_m)/cos(2*theta_m)
        = sqrt(m+1)/(sqrt(2)*m) > 0.

The negative fan has the opposite profile. Here

    sin(theta_m)=1/sqrt(2m+2),
    cos(theta_m)=sqrt((2m+1)/(2m+2)),
    cos(2*theta_m)=m/(m+1),
    sin(2*theta_m)=sqrt(2m+1)/(m+1).

These identities directly verify hub continuity and flux. Both stems
are strictly monotone away from o with the appropriate sign, since
0<theta_m<pi/2. Each fan leaf is strictly monotone until its Neumann
endpoint, since 0<2theta_m<pi/2. The endpoint derivative alone is zero;
no leaf interior, stem interior, hub, central vertex or identically
zero long-arm point attains the nonzero global extremes. Therefore

    M(T_m) = {p_1,...,p_m,n_1,...,n_m}.

All m positive leaves attain C_m and all m negative leaves attain -C_m;
these ties are included. Same-fan distances are 4h, opposite-fan
distances are 6h. Consequently diam M(T_m)=6h exactly.

The two long endpoints realize distance 1. Any pair in a finite tree
is joined by a unique path that extends, if needed, to a leaf-to-leaf
path. Long-to-fan leaf distances are 1/2+3h<1; all other leaf distances
are 4h or 6h<1. Hence the actual metric diameter of T_m is exactly 1,
including every interior point.

## 4. Uniform doubling: full domain and all new spectral sectors

Replace EVERY edge e of T_m by two distinct parallel copies of the
same length L_e, keeping its endpoints and standard unweighted
Kirchhoff conditions. Call the resulting graph G_m. It is finite and
connected, and each copied edge belongs to the two-edge cycle formed
with its mate. Former leaves have degree 2. Articulation vertices may
remain, as permitted by the precise original claim.

For aligned edge coordinates define the unitary transformation

    g_e=(f_e,1+f_e,2)/sqrt(2),
    q_e=(f_e,1-f_e,2)/sqrt(2).

Continuity gives q_e(0)=q_e(L_e)=0, and all incident g endpoint
values agree. The pair flux at a vertex is sqrt(2) times the flux of
g on the corresponding original edge; the q derivatives cancel.
Because every original edge is doubled, the common factor cancels
from every full vertex equation. Conversely any original-domain g
and independent edgewise H^2 Dirichlet q_e give doubled-domain
f_e,1=(g_e+q_e)/sqrt(2), f_e,2=(g_e-q_e)/sqrt(2). The map preserves
the norm and intertwines the differential actions, proving

    U H(G_m) U^-1 = H(T_m) direct_sum [direct_sum_e H_DD(0,L_e)].

Thus ALL added eigenvalues (r*pi/L_e)^2, r=1,2,..., are retained,
with additive multiplicities at any collision. Here max L_e=1/2,
so the first added eigenvalue is 4*pi^2. It is strictly above
mu_2(T_m)<pi^2. Hence mu_2(G_m)=k_m^2 is simple, and its eigenfunction
has equal functions on paired copies. Multiplying it by sqrt(2) if
desired reproduces the preceding unnormalized mode exactly. The
complete extrema set of G_m is the same set of 2m leaf vertices.

## 5. Full doubled metric diameter, including opposing interiors

Folding the parallel pair to its original tree edge gives a
length-preserving map P:G_m->T_m, hence
d_T(Px,Py)<=d_G(x,y). Between original vertices there is equality,
because the unique tree path can be lifted by choosing one copy of
each edge. In particular all distances between extrema are unchanged.

For points projected to distinct original edges, the tree's unique
geodesic can likewise be lifted with the prescribed copy at each
end, so their distance is exactly the projected tree distance. The
same holds for points on a single common copy. The only additional
case is interiors of opposite copies of the SAME original edge:
if the coordinates are s,t in [0,L], paths through the two endpoints
give lengths s+t and 2L-s-t. Their minimum is <=L<=1/2. A shortest
path cannot do better through another tree route between endpoints,
because removing that original edge disconnects the tree. This also
gives the exact formula min(s+t,2L-s-t) for that case.

Every pair of doubled points therefore has distance <=1, while the
two long endpoints still have distance 1. Thus

    diam G_m=1 and diam M(G_m)=6h_m.

No diameter estimate has been based only on vertex sampling.

## 6. Uniform epsilon selection and physical conclusion

For any epsilon>0 choose the finite integer

    m = max(4, ceil(36/(pi^2*epsilon^2))).

Since atan(t)<t for every t>0,

    diam M(G_m) = 6*atan(1/sqrt(m))/pi
                < 6/(pi*sqrt(m)) <= epsilon.

All other properties proved above hold for every m>=4, independently
of epsilon. This supplies the whole existence quantifier of the
original claim. No infinite graph or zero-length edge is used.

For diffusivity D>0 the heat equation is partial_t u=-D H u. The
slowest nonconstant decay rate is D*k_m^2; lengths have units L and
k_m^2 has units L^-2. Taking the diameter as one length unit, the
construction shows that the complete hottest/coldest set of a simple
slowest mode imposes no positive universal lower bound on its fraction
of the metric diameter, even when every edge lies on a cycle. This
is a prediction of the specified network diffusion operator. It is
not a higher-dimensional domain limit or an experimental finding.
There is no fixed total-length or volume constraint: total length of
G_m is 2+4h_m+8m*h_m and grows with m.

Numerical matching and metric samples in the accompanying checker
are adversarial implementation diagnostics only. The continuum
ordering, all extrema, exact diameter and all-epsilon result rest
on the preceding exact argument. Novelty coverage and its limits
are recorded separately; fresh referee reconstruction is still needed.
