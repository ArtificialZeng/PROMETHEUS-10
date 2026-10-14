# Conservative analytic control of the exact infimum

The frozen psi_0 is defined by the infimum in source.md and PRL (S5).
The following elementary bound is sufficient for a conservative witness test;
it does not certify the reported decimal minimum 0.85246.

For binary probabilities, let D(y||x) be the numerator in (S5). Jensen's
inequality applied to the square-root likelihood ratio gives

    D(y||x) >= -2 log C,
    C=sqrt(x y)+sqrt((1-x)(1-y)).

Put x=sin^2(alpha), y=sin^2(beta) with alpha,beta in (0,pi/2).
Take x>y without loss for the denominator, and define

    r=sin(alpha-beta)>0, A=sin(alpha+beta), r<=A<=1.

Then C=sqrt(1-r^2), x-y=A r, and

    v=x+y-x^2-y^2=[A^2(1-2r^2)+r^2]/2>0.

For fixed r, define F(A)=A r asinh(2 A r/[A^2(1-2r^2)+r^2]).
Writing u=2 A r/[A^2(1-2r^2)+r^2] and c=1-2r^2, differentiation gives

    F'(A)/r=asinh(u)+u/sqrt(1+u^2)*(r^2-c A^2)/(r^2+c A^2)
            >=asinh(u)-u/sqrt(1+u^2)>=0.

The first inequality uses (r^2-c A^2)/(r^2+c A^2)>=-1; the second
follows by differentiating asinh(u)-u/sqrt(1+u^2) from u=0.
Consequently the denominator in (S5) is at most

    F(1)=r asinh(2r/(1-r^2))=2r atanh(r).

Finally, g(r)=-log(1-r^2)-r atanh(r) has g(0)=0 and

    g'(r)=r/(1-r^2)-atanh(r)>=0,

since the latter difference has derivative 2r^2/(1-r^2)^2>=0 and
vanishes at zero. Therefore

    D(y||x) >= -log(1-r^2) >= r atanh(r)
              >= (1/2)(x-y) asinh((x-y)/v).

The argument also covers x<y: C and the denominator are symmetric, while
the Jensen bound holds in either KL direction. By continuous limits,

    psi_0 >= 1/2

exactly, including the diagonal/boundary limiting values of the infimum.
No numerical minimization, quoted lower-bound decimal or assumption of the
authors' numerical optimizer is needed.

## Monotonicity of the conjugate

For fixed J>0 and s, write b=s/2, L(t)=log cosh(t), and
H(t)=2J coth(t)[L(t+b)-L(t)]. Set z=cosh(t+b)/cosh(t)>0.
Direct differentiation gives

    (sinh^2(t)/(2J)) H'(t)=1-cosh(b)/z-log(z)
                              <=1-1/z-log(z)<=0.

The last inequality follows from log(z)>=1-1/z for z>0. Hence H is
nonincreasing in t>0 and nondecreasing in psi when t=d/(2psi).
The exact psi_0 bound above implies, for every finite real s,

    H_psi0(s) >= H_(1/2)(s).

A strict physical CGF gap already below H_(1/2) thus survives the full
unknown exact infimum. This is an analytic supporting derivation. A
physical strict gap still needs independent computation and error control.
