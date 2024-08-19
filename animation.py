import qutip as q
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import ArtistAnimation
from wigner import plot_wigner

from definitions import *


def plot_cavity_evolution(res, x = np.linspace(-8,8,100)):
    ims = []
    fig, axes = plt.subplots(1, 2, figsize = (8,4))

    axes[0].plot(res.times, [q.expect(ad*a, s) for s in res.states], linestyle = 'dashed', label ='cavity photon number')
    axes[0].set_xlabel(r'Time, $t$')
    axes[0].set_ylabel(r'$\langle\hat{a}^\dagger \hat{a}\rangle$')
    axes[0].legend()
    

    for i, s in enumerate(res.states): 

        rho_cavity = s.ptrace(1)
        W_cavity = q.wigner(rho_cavity, x,x)
        im1 = axes[0].scatter(res.times[i], q.expect(ad*a,s), color = 'b')
        
        im2 = plot_wigner(axes[1], W_cavity, x, x)
        
        ims.append([im1,im2])

    return ArtistAnimation(fig, ims, interval=50, blit=True)