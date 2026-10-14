# Reproduced published baselines

Source: Kennedy--Rohleder, arXiv:2003.14335v4, Example 3.3 (PDF page 8)
and Example 6.2 (PDF pages 20--21). These are known results. This file
supplies stable mathematical evidence for reproduction; it does not submit
a candidate, settle Conjecture 8.9, or claim an independent referee verdict.
The full operator and basis maps are in evidence/operator-reconstruction.md.

## Unit-edge equilateral pumpkin

For k>0, on each of E equal unit intervals use
f_e(x)=a_e cos(kx)+b_e sin(kx). Continuity at x=0 forces all a_e=a.
The origin flux requires sum b_e=0. If sin(k) is nonzero, continuity
at x=1 forces all b_e equal, hence all zero; terminal flux then gives
E*a*sin(k)=0, so a=0. No positive eigenvalue has 0<k<pi.
At k=n*pi, n>=1, the common a is free and the b_e satisfy just the
single zero-sum condition. The eigenspace is E-dimensional. Nonnegativity
and connectedness give the simple zero mode. Thus mu2=pi^2 with exactly
the published multiplicity E. A independently assembles exact full
matching matrices at E=2,3,5,8 and n=1,2,3. B decomposes into one NN
interval and E-1 DD intervals. Every pole n*pi is included in both.
Their complete matching matrices agree entry by entry under the stated
reversed-coordinate and derivative-sign map. The exact argument, rather
than the finite list, covers all finite E>=2.

## Split-tree family and finite reproduction instance

Write a=1/2 for the two long arms, h for each central-to-fan stem, and
b=atan(cot(pi*h)/m)/pi for each of m fan leaf edges on each side.
The finite instance used here is h=1/6, m=5, so
b=atan(sqrt(3)/5)/pi. The selected positive stem is sin(pi*r);
its fan leaf is sin(pi*h) cos(pi*x)+(cos(pi*h)/m) sin(pi*x).
The other fan has the negative of this function; the long arms are zero.
Continuity, hub flux and leaf Neumann conditions follow directly from
tan(pi*b)=cot(pi*h)/m. The selected fan-leaf magnitude is
sqrt(sin(pi*h)^2+cos(pi*h)^2/m^2), matching the rendered primary page 20.

To verify that this is the first positive eigenvalue, and not just an
eigenfunction, decompose by permutations of the m leaf arms at each hub.
Zero-sum leaf sectors vanish at the hub and have DN leaf intervals of
length b; their first wave number is pi/(2*b)>pi. The remaining fan
sector has equal functions on all its leaf arms. With a Dirichlet value
at the central root, write the stem S*sin(k*r) and the reversed-coordinate
Neumann leaf C*cos(k*z). Their matching matrix is

    [-sin(k*h), cos(k*b)]
    [-cos(k*h), m*sin(k*b)].

Its determinant is cos(k*h)cos(k*b)-m*sin(k*h)sin(k*b).
On 0<k<pi all tangent arguments lie in (0,pi/2), and
m*tan(k*h)*tan(k*b) is strictly increasing from zero to one at pi.
Thus the fan's first Dirichlet-root wave number is exactly pi.
The long arms, with central Dirichlet and leaf Neumann, also first
reach k=pi. With the central value zero, there are four independent
branch amplitudes and one central flux equation, giving multiplicity
three at pi^2. The exact A full matrix has dimension 28, rank 25.

There are no lower positive modes having a nonzero central value c.
Below the first branch Dirichlet-root wave number, each long arm's
outgoing root derivative per value is k*tan(k*a)>0. The equal-leaf
fan gives the root derivative per value

    k * [tan(k*h)+m*tan(k*b)] / [1-m*tan(k*h)*tan(k*b)],

which is positive on this interval. Kirchhoff would require the sum
of the four positive branch responses times the common nonzero c to
vanish, which is impossible. This exhausts the permutation sectors.
At k=pi the branch solvability forces c=0, also confirmed by the exact
full-matching nullity. The complete unperturbed eigenspace contains
long-arm modes, so its full extrema union is not inferred from the
selected fan eigenfunction. The source expressly retains multiplicity 3.

## Published perturbation, checked at delta=1/1000

Lengthen each fan leaf edge to b_p=b+delta, leaving the stems and long
arms fixed. For the chosen delta=1/1000, b_p<1/2 and h+b_p<1/2.
The first fan Dirichlet-root wave number k0 is the unique root in (0,pi)
of m*tan(k*h)*tan(k*b_p)=1: the product is strictly increasing,
starts at zero, and its value at pi exceeds one. The pole-free matrix
above with b_p in place of b gives the same characteristic equation.
Both fan branches have this first eigenvalue. The long DN branches
start at pi; leaf zero-sum DN sectors start at pi/(2*b_p)>pi.
For 0<k<k0, the branch responses above are all positive, excluding
any central-nonzero mode. At k0, central-nonzero data are incompatible
with the first fan's root matching: the second matrix row is cot(k0*h)
times the first, but its inhomogeneous data for central value c would
require -c*sin(k0*h)=c*cos(k0*h)^2/sin(k0*h), hence c=0.
The two fan amplitudes then obey one central flux equation and are
opposites. All long-arm coefficients vanish. Therefore mu2=k0^2<pi^2
is simple for this finite published-family instance.

A finds k0 from the complete 28 by 28 matching determinant in binary
double precision. B reconstructs the leaf-rooted two by two problem
independently and bisects at 70 decimal digits. The logs record their
agreement, not a fictitious interval enclosure. The high-precision
residual and bisection width are reproducibility diagnostics. Actual
firstness and simplicity at this instance use the preceding analytic
argument, not floating-point multiplicity.

All edge extrema are controlled for this simple mode: k0*h<pi/2 and
k0*b_p<pi/2, so each positive stem and each positive fan leaf increases
strictly toward its fan leaf endpoint; the other fan has the negative
profile. The long arms are identically zero and are not global extrema.
There are precisely m positive and m negative global-extremum vertices.
The maximum pairwise distance in their union is 2*(h+b_p). Every
distance on a tree between interior points is bounded by a leaf-to-leaf
path extending that pair's path. Leaf distances are at most 1: the
two long tips realize 1, long-to-fan distances are 1/2+h+b_p<1,
and opposite fan distances are 2*(h+b_p)<1. Thus the actual tree
diameter is 1, without ignoring interior edge points.

## Duplication sanity checks, without an existence claim

The complete domain equivalence in evidence/operator-reconstruction.md
adds one DD interval spectrum per original edge. For the source
half-length four-star, A full matching and B's sectors both give
multiplicity 3 at k=pi. At k=2*pi, the original multiplicity is 1,
and four added DD modes give doubled multiplicity 5. This deliberate
collision check ensures the added branches are not dropped at a pole.

For the finite perturbed split-tree instance, the longest edge length
is 1/2, so the added DD threshold is 4*pi^2. It lies strictly above
the reproduced mu2<pi^2. A also evaluates the complete doubled 56 by
56 matching matrix at the finite root. These are operator/baseline
checks. The universal epsilon construction, doubled metric geometry,
uniform parameter selection and candidate novelty remain a research
task, and no original problem resolution is claimed by reproduction.
