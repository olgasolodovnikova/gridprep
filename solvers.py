import qutip as q
import numpy as np
from definitions import *
from gate_activation import Hcoeff_list

def solve_timedep_H(zeta, settings, alpha = 0, noise_sources = None, t = np.linspace(0, 50, 301)):

    #H0 = oma/2*sz + omc*ad*a
    H0 = I
    Hlist = get_Hlist(settings['M'])
    Hcoeffs = Hcoeff_list(settings)
    
    Htimedep =  list(map(list, zip(Hlist, Hcoeffs)))

    H = [H0, *Htimedep]
    c_ops = []
    if noise_sources != None:
        gamma_bl, gamma_bdp, (gamma_c, nbar), gamma_ql, gamma_qdp = noise_sources.values()
        if gamma_bl != 0:
            c_ops.append(np.sqrt(gamma_bl)*a) #Boson loss
        if gamma_bdp != 0: 
            c_ops.append(np.sqrt(gamma_bdp)*(a*ad + ad*a)) #Boson dephasing
        if gamma_c != 0: 
            c_ops.append(np.sqrt(gamma_c*(nbar+1))*a) #Boson heating
            c_ops.append(np.sqrt(gamma_c*nbar)*ad) #Boson heating 2
        if gamma_ql != 0:
            c_ops.append(np.sqrt(gamma_ql)*sm) #Qubit decay
        if gamma_qdp != 0:
            c_ops.append(np.sqrt(gamma_qdp)*sz) #Qubit dephasing
            
    #Initial state (squeeze the coherent state with zero displacement)
    rho0 = q.tensor(q.basis(2,0), q.squeeze(N, zeta) @ q.coherent(N, alpha))
    res = q.mesolve(H, rho0, c_ops = c_ops, tlist= t)

    return res