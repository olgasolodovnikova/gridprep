from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

import numpy as np
import qutip as q
from definitions import *
from gate_activation import Hcoeff_list, activate


def plot_wigner(ax, ax_x, ax_p, W, x, p):
    
    scale = np.max(W.real)
    nrm = Normalize(-scale, scale)
    
    im = ax.contourf(x,p, W.real, 100, cmap = cm.RdBu, norm =nrm)
    ax.set_xlabel('x')
    ax.set_ylabel('p')
    ax.yaxis.set_label_position('right')
    ax.yaxis.set_ticks_position('right')
    ax.set_aspect('equal')
    
    marginal_x = np.sum(W,axis=0)*np.diff(p)[0]
    marginal_p = np.sum(W,axis=1)*np.diff(x)[0]
    ax.set_aspect("equal")
    ax_x.plot(x, marginal_x)
    ax_p.plot(marginal_p, p)
    ax_x.tick_params(axis = 'x',labelbottom = False)
    ax_p.yaxis.set_ticks_position('right')
    ax_p.tick_params(axis = 'y', labelright=False)
    ax_x.grid('on')
    ax.grid('on')
    ax_p.grid('on')
    ax_x.set_ylabel(r'$P(x)$')
    ax_p.set_xlabel(r'$P(p)$')
    ax_p.invert_xaxis()

def plot_activation_funcs(ax, settings, t, legend = False):
    
    M, T, dT, Tdelay, z = settings.values()
    
    Hcoeffs = Hcoeff_list(settings)
    labels = [f'$U_{k}$' if g == 0 else f'$V_{k}$' if g == 1 else f'$W_{k}$' for k in range(M) for g in range(3)]
    
    for i, fun in enumerate(Hcoeffs):
        ax.plot(t, fun(t), label = labels[i], alpha = 1, color = cm.tab20(i))

    if legend: 
        ax.legend()
    ax.set_title('Gate activation functions', fontsize=10)
    ax.set_ylabel('Value')
    ax.set_xlabel('Time')


def make_sim_plot(SimGKP, time_index): 
    """Plot the Wigner function plus marginals for a particular time step
    """
    time_index = int(time_index)
    wig_xlim = SimGKP.wigner_xlim
    wig_res = SimGKP.wigner_res

    xvec = np.linspace(-wig_xlim, wig_xlim, wig_res)
    

    res = SimGKP.res
    
    #Prepare figure layout
    fig = plt.figure( figsize = (10,4.5))
    
    gs = GridSpec(1,2, figure = fig) 
    
    gs.update(left=0.1, right=0.9, bottom=0.1, top=0.9)
    
    gs_wigner = GridSpecFromSubplotSpec(2,2, subplot_spec = gs[1], width_ratios=(1,4), height_ratios=(1,4),
                              wspace=0.2, hspace=0.2)
    
    ax = fig.add_subplot(gs_wigner[1, 1] )
    ax_x = fig.add_subplot(gs_wigner[0, 1], sharex = ax)
    ax_p = fig.add_subplot(gs_wigner[1, 0], sharey = ax)

    
    gs_gates = gs[0].subgridspec(2,1 )
   
    ax1 = fig.add_subplot(gs_gates[0])
    ax2 = fig.add_subplot(gs_gates[1],sharex = ax1)
    
    ax1.grid('on')
    ax2.grid('on')
    ax1.set_xlabel('')

    #Gate activation plot
    plot_activation_funcs(ax1, SimGKP.gate_settings, np.array(res.times))


    #Plot average number of photons in the cavity
    ax2.plot(res.times, [q.expect(ad*a, s) for s in res.states], linestyle = 'dashed', label ='cavity photon number')
    ax2.set_xlabel(r'Time, $t$')
    ax2.set_ylabel(r'$\langle\hat{a}^\dagger \hat{a}\rangle$')
    ax2.legend()

    #Plot Wigner function of cavity and marginals
    state = (res.states)[time_index] 
    plot_wigner(ax, ax_x, ax_p, SimGKP.wigner[time_index], xvec, xvec)    


    #Plot the time specific things
    ax2.scatter(res.times[time_index], q.expect(ad*a,state), marker='o')
    ax2.vlines(res.times[time_index], 0, np.max([q.expect(ad*a, s) for s in res.states]))
    ax1.vlines(res.times[time_index], 0, 0.5 )

    ax.text(0.7,0.75, f't={np.round(res.times[time_index],1)}',transform=ax.transAxes, fontsize = 12)
            
    plt.show()