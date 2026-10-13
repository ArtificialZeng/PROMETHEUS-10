from fractions import Fraction as F
r = F(10000, 10001); s = r**64
Z = 3 + 4*r + 4*s
u, v, w = 1/Z, r/Z, s/Z
h = F(33, 65)
ell = F(33**63, 33**63 + 32**63)
j = (h*v - (1-h)*u)/4
L = (ell*w - (1-ell)*v)/4
x, y, t = u + 4*j, v - 3*j + L, w - L
a0 = 3*u*(1-h) + v*(3*h + 1-ell)
a0 += w*(F(3, 2) + ell)
rho = F(1, 1 + 64**63)
a1 = 3*x/65 + (F(192, 65) + rho)*y
a1 += (F(5, 2) - rho)*t
vals = [a0, a1, (a0+a1)/2, x, y, t]
nums = [499785676488, 504349849005,
        502067762747, 92521064942,
        106989212896, 73619988396]
for a, m in zip(vals, nums):
    assert F(m, 10**12) <= a
    assert a < F(m+1, 10**12)
assert a1 > F(63, 125)
assert (a0+a1)/2 > F(251, 500)
