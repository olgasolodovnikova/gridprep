import numpy as np
import qutip as q
from matplotlib import pyplot as plt

from definitions import *
from solvers import solve_timedep_H
from plotting import plot_activation_funcs


class SimulateGKP:
    """Simulate the GKP preparation protocol with cavity QED from Hastrup, J., Park, K., Brask, J.B. et al. Measurement-free preparation of grid states. npj Quantum Inf 7, 17 (2021). https://doi.org/10.1038/s41534-020-00353-3
        
        init_sqz(complex) : initial squeezing of cavity mode
        init_disp(complex): initial displacement of cavity mode
        gate_settings(dict): 
        
            gate_settings = {'M': number of steps in protocol, 'T': duration of gate, 'dT': time between gates, 'Tdelay': time between steps,'z': sensitivity of gate activation function}
            
        noise_settings(dict): 
        
            noise_settings = {'boson loss': gamma_bl, 'boson dephasing': gamma_bdp, 'boson heating': [gamma_c, nbar], 'qubit loss': gamma_ql, 'qubit dephasing': gamma_qdp}

            all gammas should be between 0 and 1. 
        """
    def __init__(self, init_sqz=1, init_disp=0, gate_settings=None, noise_settings=None):
        self.init_sqz = init_sqz
        self.init_disp = init_disp 
        
        if gate_settings == None:
            M = 1
            T = 2
            dT = T
            Tdelay = 6*T+3*dT 
            z = pi
            gate_settings = {'M': M, 'T': T, 'dT': dT, 'Tdelay': Tdelay, 'z': z}

        if gate_settings['M'] > 4: 
            raise ValueError('Protocol not implemented for more than 4 steps.')
            
        self.gate_settings = gate_settings

        if noise_settings == None:
            gamma_bl = 0
            gamma_bdp = 0
            gamma_c = 0
            nbar = 0
            gamma_ql = 0
            gamma_qdp = 0
            
            noise_settings = {'boson loss': gamma_bl, 'boson dephasing': gamma_bdp, 'boson heating': [gamma_c, nbar], 
                     'qubit loss': gamma_ql, 'qubit dephasing': gamma_qdp}
     
        self.noise_settings = noise_settings

    def show_gate_settings(self, time_res = 200):
        """Plot the activation functions for all the gates in the protocol
        time_res(int): Number of time steps
        """
        fig, ax = plt.subplots()
        M, T, dT, Tdelay, z = self.gate_settings.values()
        times = np.linspace(0,M*Tdelay, time_res)
        plot_activation_funcs(ax, self.gate_settings, times, legend=True)
        

    def run_sim(self, time_res = 200):
        """Solve the Lindblad Master equation 
        time_res(int): Number of time steps
        """
        M, T, dT, Tdelay, z = self.gate_settings.values()
        times = np.linspace(0,M*Tdelay, time_res)
        
        self.res = solve_timedep_H(self.init_sqz, self.gate_settings, self.init_disp, self.noise_settings, times)
        self.time_res = time_res

    def compute_wigner(self, xlim = 15, res = 150):
        """Compute the cavity field's Wigner function for all times. First do SimulateGKP.run_sim().
        xlim(float): the x and p boundary (symmetric here)
        res(int): Wigner grid resolution
        """
        xvec = np.linspace(-xlim,xlim,res)
        self.wigner = [q.wigner(s.ptrace(1), xvec, xvec) for s in self.res.states]
        self.wigner_xlim = xlim
        self.wigner_res = res