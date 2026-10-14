# Primary operator reconstruction and conventions

This is source reproduction, not a novel result or scientific acceptance.
The input operator is taken from Kennedy--Rohleder, arXiv:2003.14335v4,
Section 2.2, PDF page 6. Input A follows the primary text extraction;
input B was reconstructed from the actually viewed rendered pages 6, 8,
20 and 21 and an independent interval-sector representation. Both passes
were by the same agent, with a shared source and remembered benchmark.
This is weaker than a fresh independent referee. Neither B code nor B
data is obtained by consuming A's numerical or symbolic output.

## Operator and flux map

The Hilbert space is the direct sum of unweighted L2 edge intervals.
H=-d^2/dx^2 has edgewise H2 functions continuous at vertices, with
Kirchhoff flux zero. The source uses derivatives pointing toward each
vertex, sum f'(L) at termini minus sum f'(0) at origins. A uses the
negative of that sum, the usual derivatives directed into incident edges.
The entire vertex equation changes sign, preserving its homogeneous
zero condition. B uses the source sign. This difference is recorded,
not silently repaired. Real positive k has eigenvalue k^2. The cosine/
sine coefficient basis is used only at k>0. At zero the linear basis,
or the nonnegative quadratic form, establishes the simple constant mode.
No mass weighting, forcing, potential or nonstandard vertex condition
has been introduced.

## Pumpkin comparison including the singular wave numbers

A applies all endpoint constraints to a_e cos(kx)+b_e sin(kx), without
dividing by sin(k). Its 2E by 2E matrix contains E-1 origin-continuity
rows, E-1 terminal-continuity rows, and two flux rows scaled by k.
At k=n*pi, n>=1, continuity forces all a_e equal, while flux requires
sum b_e=0. There is one free common a and E-1 independent b values.
For sin(k) nonzero the continuity rows force all b_e equal, flux forces
them zero, and terminal flux forces all a_e zero. Thus there are no
positive roots below pi, and the multiplicity at pi^2 is exactly E.
The argument covers arbitrary finite E>=2; tested exact matrix instances
are supplementary, not a finite-scan proof of that statement.

B independently decomposes the edge vector into its mean and the
E-1 dimensional zero-sum space. The mean has Neumann endpoint conditions;
each zero-sum component has Dirichlet endpoint conditions. This gives the
same spectrum and multiplicities, including the poles where a vertex-only
Dirichlet-to-Neumann matrix would be undefined.

For the explicit basis comparison, reverse all edge coordinates,
y=1-x. With c=cos(k), s=sin(k), the coefficients map as
(alpha,beta)=(c*a+s*b, s*a-c*b). This 2 by 2 map is its own inverse
and preserves the edge solution for c^2+s^2=1. After this map, the B
origin and terminal continuity blocks equal the A terminal and origin
blocks. The B origin and terminal flux rows equal the negatives of the
A terminal and origin flux rows. The comparison script checks every
matrix entry, modulo c^2+s^2=1, not just a determinant or spectrum.

## Uniform duplication domain, with every added branch retained

Orient both copies of an original edge identically and use
g=(f1+f2)/sqrt(2), h=(f1-f2)/sqrt(2). Continuity of f1 and f2 at each
vertex gives h(0)=h(L)=0; g has a common vertex value sqrt(2)*f(v).
The pair contributes sqrt(2) times the original-edge derivative of g
to each vertex flux. Because EVERY edge is doubled, this common factor
cancels from each complete Kirchhoff equation. Derivatives of h cancel
between its two copies; no additional flux restriction on h remains.
Conversely any original-domain g and independent H2 Dirichlet h_e give
valid doubled-domain f1=(g+h)/sqrt(2), f2=(g-h)/sqrt(2). This proves a
two-sided domain map, preserving norm and edge differential action:

H_doubled is unitarily equivalent to H_original plus one Dirichlet
interval operator of the original length for EACH original edge.

For original loops both endpoint incidences are included and the same
argument applies. All antisymmetric modes (n*pi/L_e)^2, n>=1, must be
retained, including degeneracies with the original spectrum. No secular
division is used to erase them. The first positive eigenvalue of a
doubled graph cannot be assumed to be simple without checking this
ordering and coincidences. Partial edge duplication changes relative
flux weights and is outside this identity's stated input conventions.
This established linear decomposition is recorded as an input check,
not claimed as a new doubling method or a resolution of Conjecture 8.9.

## Rendered-source correction and split-tree input

The PDF page 20 actually shows the fan maximum
sqrt(A^2/m^2+F^2). The supplied text extraction drops the radical.
The rendering was inspected, and input A records the corrected
amplitude with this provenance. The actual source files are preserved.
With h=epsilon, source A=sin(pi*(1/2+h))=cos(pi*h) and
F=-cos(pi*(1/2+h))=sin(pi*h), the fan length is
b=atan(cot(pi*h)/m)/pi. This is the same positive principal-branch
arctangent in both reconstructions. B imposes leaf Neumann conditions
first, with C*cos(k*z), z measured from a leaf toward its hub, and
S*sin(k*r) on a stem measured from the central Dirichlet root.
Hub continuity and flux produce the pole-free 2 by 2 matrix recorded
in input B. Its zero at k=pi reproduces the balanced splitting input.
The source's final perturbation changes b to b+delta on ALL fan leaf
edges; it does not lengthen stems. The chosen finite reproduction
instance is h=1/6, m=5, delta=1/1000. It is not offered as an arbitrary
epsilon construction. The unperturbed eigenspace has dimension three,
so the extrema of one selected fan-supported eigenfunction do not
describe the extrema union over all unperturbed second eigenfunctions.
