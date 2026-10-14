"""Input B: independently derived Pauli tensor / reflection representation.

Construct matrices from ket outer products, use order I,Z,X,Y. No import of A,
no reading input-a.json. Same agent derivation; no claim of independent referee.
"""
import numpy as np

e0, e1 = np.array([1,0],complex), np.array([0,1],complex)
E00, E01 = np.outer(e0,e0.conj()), np.outer(e0,e1.conj())
E10, E11 = np.outer(e1,e0.conj()), np.outer(e1,e1.conj())
B = [E00+E11, E00-E11, E01+E10, 1j*(E10-E01)]
TENSORS = np.array([[np.kron(s,t) for t in B] for s in B])

def coeffs(rho):
    return np.einsum('abij,ji->ab',TENSORS,rho).real

def reconstruct(c):
    return np.einsum('ab,abij->ij',c,TENSORS)/4

def dephase(rho):
    c = coeffs(rho)
    r = c[1:,0]
    g = np.linalg.norm(r)
    if g <= 1e-8:
        raise ValueError('Marginal degeneracy/conditioning cutoff')
    n = r/g
    d = c.copy()
    d[1:,:] = np.outer(n,n) @ c[1:,:]
    return reconstruct(d)

def reflect_dephase(rho):
    # Alternate B implementation, derived from P+-=(I+-n.sigma)/2.
    c = coeffs(rho)
    r = c[1:,0]
    n = r/np.linalg.norm(r)
    k = np.kron(sum(n[j]*B[j+1] for j in range(3)),B[0])
    return (rho+k@rho@k)/2

def hadamard_transfer():
    # H conjugation is a pi rotation about n=(Z+X)/sqrt(2).
    n = np.array([1,1,0])/np.sqrt(2)
    r = 2*np.outer(n,n)-np.eye(3)
    t = np.zeros((4,4))
    t[0,0] = 1
    t[1:,1:] = np.eye(3)/3+2*r/3
    return t

def channel(rho, t):
    return reconstruct(t @ coeffs(rho))

def hadamard(rho):
    return channel(rho,hadamard_transfer())

def isotropic(rho, lam):
    return channel(rho,np.diag([1,lam,lam,lam]))

def antiisotropic(rho, a):
    # Computational transposition reverses the Y coordinate only.
    return channel(rho,np.diag([1,a,a,-a]))

def rot3(axis, theta):
    # Input axis in conventional xyz; reorder to B's zxy coordinates.
    n = np.asarray(axis,float)[[2,0,1]]
    n /= np.linalg.norm(n)
    x,y,z = n
    cross = np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
    return np.cos(theta)*np.eye(3)+(1-np.cos(theta))*np.outer(n,n)+np.sin(theta)*cross

def pauli_transfer(p, axis_u, theta_u, axis_v, theta_v):
    # Independently derived from sigma_j sigma_k sigma_j = +-sigma_k.
    p0,px,py,pz = p
    d = np.diag([p0-px-py+pz,p0+px-py-pz,p0-px+py-pz])
    t = np.zeros((4,4)); t[0,0] = 1
    t[1:,1:] = rot3(axis_u,theta_u)@d@rot3(axis_v,theta_v)
    return t

def inputs():
    # Derive eigenvector of E(|0><0|) from output Bloch r=(z,x,y)=(1/3,2/3,0).
    r = np.array([1/3,2/3,0])
    norm = np.linalg.norm(r)
    projector = (B[0]+sum((r/norm)[j]*B[j+1] for j in range(3)))/2
    # Coefficients of |1><0|=(X-iY)/2 in B order.
    c = np.array([0,0,1,-1j],complex)
    mapped = sum(x*s for x,s in zip(hadamard_transfer()@c/2,B))
    coefficient = np.trace(projector@mapped)
    def enc(m):
        return [[[float(x.real),float(x.imag)] for x in row] for row in m]
    return {
        'source_locator':'arXiv:1708.09076v2 rendered pp6-7, then independent Bloch derivation',
        'method':'Outer-product Pauli construction; pi rotation / tensor coefficient projection',
        'basis':['00','01','10','11'], 'pauli_order':['I','Z','X','Y'],
        'pauli_matrices':[enc(s) for s in B],
        'hadamard_transfer':hadamard_transfer().tolist(),
        'hadamard_transfer_exact':[['1','0','0','0'],['0','1/3','2/3','0'],['0','2/3','1/3','0'],['0','0','0','-1/3']],
        'convention_map':'A coefficients (I,X,Y,Z) -> B (I,Z,X,Y), index permutation [0,3,1,2] on both subsystems',
        'dephasing':'c0k unchanged; cjk -> n_j sum_l n_l c_lk, j,l in Z,X,Y; equivalent to (rho+N rho N)/2',
        'isotropic':'T=diag(1,lambda,lambda,lambda) in I,Z,X,Y order',
        'antiisotropic':'T=diag(1,a,a,-a) in I,Z,X,Y order',
        'general_pauli':'Tspatial=R_U diag(p0-px-py+pz,p0+px-py-pz,p0-px+py-pz) R_V',
        'paper_eta_plus_projector':enc(projector),
        'paper_noncommuting_coefficient':float(coefficient.real),
        'paper_coefficient_formula':'2/(3*sqrt(5))'
    }
