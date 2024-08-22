import numpy as np
import qutip as q
import itertools

# Main system settings

N = 70 #Boson photon number cutoff 
hbar = 1
pi = np.pi

# Qubit operators
sz = q.tensor(q.sigmaz(), q.identity(N))
sy = q.tensor(q.sigmay(), q.identity(N))
sx = q.tensor(q.sigmax(), q.identity(N))

sm = q.tensor(q.sigmam(), q.identity(N))
sp = q.tensor(q.sigmap(), q.identity(N))


# Cavity operators
ad = q.tensor(q.identity(2), q.create(N))
a = q.tensor(q.identity(2), q.destroy(N))

x = q.tensor(q.identity(2), q.position(N))
p = q.tensor(q.identity(2), q.momentum(N))

# Identity
I = q.tensor(q.identity(2), q.identity(N))


# Rabi gate list for the GKP generation scheme in 
# Hastrup, J., Park, K., Brask, J.B. et al. Measurement-free preparation of grid states. 
# npj Quantum Inf 7, 17 (2021). https://doi.org/10.1038/s41534-020-00353-3

U = x*sy #Preparation gate
V = p*sx #Displacement gate
W = x*sy #Disentangling gate

# Gate parameters
def us(k : int, M: int, method = 1):
    """Preparation gate parameter for the kth gate for a total of M steps in prep protocol
    """
    #From Table 1 in Supplementary material of Hastrup, J. et al. (2021) https://doi.org/10.1038/s41534-020-00353-3
    us1 = {1: [0], 2: [0,0.045], 3: [0,0.053, 0.033], 4: [0,0.038,0.027,0.015]}
    us2 = {1: [0], 2: [0,0.043], 3: [0,0.04, 0.026], 4: [0,0.024,0.015,0.008]}

    if M > 4:
        return NotImplemented
    if k > M: 
        raise ValueError('k must be less than or equal to M')
    
    if method == 1: 
        return us1[M][k]
    else: 
        return us2[M][k]  

def vs(k : int, M: int): 
    """Displacement gate parameter for the kth gate for a total of M steps in prep protocol
    """
    if k == 0:
        return -np.sqrt(np.pi)*2**(M-1)
    else: 
        return np.sqrt(np.pi)*2**(M-(k+1))

def ws(k : int, M: int):
    """Disentangling gate parameter for the kth gate for a total of M steps in prep protocol
    """
    if k == M:
        return np.sqrt(np.pi)/4
    else: 
        return -np.sqrt(np.pi)/4*2**(-(M-(k+1)))


def get_Hlist(M : int, out = False):
    """Get full gate list for M step prep protocol
    """
    U_list = [us(k,M)*U for k in range(M)]
    V_list = [vs(k,M)*V for k in range(M)] 
    W_list = [ws(k,M)*W for k in range(M)]
    
    H_list = itertools.chain.from_iterable([[us(k,M)*U, vs(k,M)*V, ws(k,M)*W] for k in range(M)])

    if out:
        ordering_check = list(itertools.chain.from_iterable([[f'u{k}{M}U', 
                                                          f'v{k}{M}V',
                                                          f'w{k}{M}W'] for k in range(M)]))
        print(ordering_check)
    return list(H_list)