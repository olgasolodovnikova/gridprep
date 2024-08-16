from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np


def plot_wigner(ax, W, x, p):

    scale = np.max(W.real)
    nrm = Normalize(-scale, scale)

    im = ax.contourf(x,x, W.real, 100, cmap = cm.RdBu, norm =nrm)
    ax.set_xlabel('x')
    ax.set_ylabel('p')
    ax.set_aspect('equal')
    return im