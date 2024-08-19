from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
from definitions import hbar

def plot_wigner(ax, W, x, p):

    scale = np.max(W.real)
    nrm = Normalize(-scale, scale)

    im = ax.contourf(x,x, W.real, 100, cmap = cm.RdBu, norm =nrm)
    ax.set_xlabel('x')
    ax.set_ylabel('p')
    ax.set_aspect('equal')
    return im


def plot_wigner_marginals(W, x, p, title, GKP='rect'):
    ## To do: add colorbar
    
    # Start with a square Figure.
    fig = plt.figure(figsize=(6,6))
    # Add a gridspec with two rows and two columns and a ratio of 1 to 4 between
    # the size of the marginal Axes and the main Axes in both directions.
    # Also adjust the subplot parameters for a square plot.
    gs = fig.add_gridspec(2,2,  width_ratios=(1,4), height_ratios=(1,4),
                          left=0.1, right=0.9, bottom=0.1, top=0.9,
                          wspace=0.1, hspace=0.1)
    # Create the Axes.
    ax = fig.add_subplot(gs[1, 1])
    ax_x = fig.add_subplot(gs[0, 1], sharex = ax)
    ax_p = fig.add_subplot(gs[1, 0], sharey = ax)
    
    marginal_x = np.sum(W,axis=0)*np.diff(p)[0]
    marginal_y = np.sum(W,axis=1)*np.diff(x)[0]

    W = np.round(W.real, 4)
    scale = np.max(W.real)
    nrm = mpl.colors.Normalize(-scale, scale)

    if GKP == 'rect':
        grid = np.sqrt(hbar*np.pi)
        ax.contourf(x /grid, p/grid, W, 100, cmap=cm.RdBu, norm = nrm)
        ax.set_xlabel(r"$x(\sqrt{\hbar\pi})^{-1}$", fontsize=15)
        #ax.set_ylabel(r"$p(\sqrt{\hbar\pi})^{-1}$", fontsize=12)
        ax_p.set_ylabel(r"$p(\sqrt{\hbar\pi})^{-1}$", fontsize=15)
        ax.grid('on')
    elif GKP =='square':
        grid = np.sqrt(hbar*np.pi/2)
        ax.contourf(x/grid, p/grid, W, 100, cmap=cm.RdBu, norm = nrm)
        ax.set_xlabel(r"$x(\sqrt{\hbar\pi/2})^{-1}$", fontsize=15)
        #ax.set_ylabel(r"$p(\sqrt{\hbar\pi/2})^{-1}$", fontsize=12)
        ax_p.set_ylabel(r"$p(\sqrt{\hbar\pi/2})^{-1}$", fontsize=15)
        ax.grid('on')
    else:
        ax.contourf(x, p, W, 100, cmap=cm.RdBu, norm = nrm)
        grid = 1
        ax.set_xlabel(r"$x$", fontsize=15)
        ax_p.set_ylabel(r"$p$", fontsize=15)

    ax.set_aspect("equal")

    
    ax_x.plot(x/grid, marginal_x)
    ax_p.plot(marginal_y, x/grid)
    
    ax_x.tick_params(axis = 'x',labelbottom = False)
    ax.tick_params(axis = 'y', labelleft=False)
    ax_x.grid('on')
    ax_p.grid('on')
    ax_x.set_ylabel(r'$P(x)$')
    ax_p.set_xlabel(r'$P(p)$')
    ax_p.invert_xaxis()
    plt.suptitle(title)
    fig.tight_layout()
    
    return fig, ax, ax_x, ax_p