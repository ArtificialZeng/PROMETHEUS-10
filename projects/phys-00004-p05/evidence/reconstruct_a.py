"""Input A: direct source transcription, spectral-projector implementation.

Basis |00>,|01>,|10>,|11>; Pauli order I,X,Y,Z. This module never imports B.
"""
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.array([[1, 0], [0, -1]], complex)
S = [I, X, Y, Z]
H = (X + Z) / np.sqrt(2)

def marginal(rho):
    return np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)

def dephase(rho):
    w, v = np.linalg.eigh(marginal(rho))
    if w[1] - w[0] <= 1e-8:
        raise ValueError('Marginal degeneracy/conditioning cutoff')
    out = np.zeros((4, 4), complex)
    for j in range(2):
        p = np.outer(v[:, j], v[:, j].conj())
        k = np.kron(p, I)
        out += k @ rho @ k
    return out

def hadamard(rho):
    k = np.kron(H, I)
    return rho / 3 + (2 / 3) * k @ rho @ k.conj().T

def pauli_channel(rho, p, u=None, v=None):
    u = I if u is None else u
    v = I if v is None else v
    out = np.zeros((4, 4), complex)
    for weight, s in zip(p, S):
        k = np.kron(u @ s @ v, I)
        out += weight * k @ rho @ k.conj().T
    return out

def isotropic(rho, lam):
    return pauli_channel(rho, [(1 + 3*lam)/4] + [(1-lam)/4]*3)

def antiisotropic(rho, a):
    # a*rho^T+(1-a)Tr(rho)I/2; CP range -1<=a<=1/3.
    return pauli_channel(rho, [(1+a)/4, (1+a)/4, (1-3*a)/4, (1+a)/4])

def rotation(axis, theta):
    n = np.array(axis, float)
    n /= np.linalg.norm(n)
    return np.cos(theta/2)*I - 1j*np.sin(theta/2)*sum(n[j]*S[j+1] for j in range(3))

def transfer_single(fun):
    return np.array([[np.trace(s @ fun(t)).real / 2 for t in S] for s in S])

def inputs():
    q = (np.sqrt(5)-1)/2
    n = 1+q*q
    eta = np.array([1, q])/np.sqrt(n)
    # Source p6: sum_i p_i <eta+|U_i|1><0|U_i^dag|eta+>.
    onezero = np.array([[0,0],[1,0]],complex)
    image = onezero/3 + 2*H@onezero@H/3
    coefficient = np.vdot(eta, image @ eta)
    def enc(m):
        return [[[float(x.real),float(x.imag)] for x in row] for row in m]
    return {
        'source_locator':'arXiv:1708.09076v2 pp2,6,7: Eq(2), Theorem3/Corollary4, Fig2(a)',
        'method':'Direct text/formula transcription with primary rendered pages6-7 checked',
        'basis':['00','01','10','11'], 'pauli_order':['I','X','Y','Z'],
        'pauli_matrices':[enc(s) for s in S], 'H':enc(H),
        'hadamard_weights':['1/3','2/3'],
        'hadamard_transfer':transfer_single(lambda t:t/3+2*H@t@H/3).tolist(),
        'dephasing':'sum_s (P_s tensor I) rho (P_s tensor I), P_s from eigendecomposition of Tr_B rho',
        'isotropic':'lambda rho + (1-lambda) Tr(rho)I/2; p0=(1+3lambda)/4, pi=(1-lambda)/4',
        'antiisotropic':'a rho^T + (1-a)Tr(rho)I/2; p=(1+a,1+a,1-3a,1+a)/4',
        'paper_eta_plus':[[float(x),0] for x in eta],
        'paper_noncommuting_coefficient':float(coefficient.real),
        'paper_coefficient_formula':'(sqrt(5)-1)/(3*(1+((sqrt(5)-1)/2)^2))',
        'sampling':'Source specifies 1000 random states but no seed or distribution; new complex Ginibre samples used'
    }
