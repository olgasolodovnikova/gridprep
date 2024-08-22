from scipy.special import erf
from functools import partial

def activate(t0, tf, z, t):
    """Activation function for the Rabi interaction
    
    t0: activation time
    tf: deavtivation time
    z: sensitivity 
    t: time
    """
    return 0.25*(1+erf(z*(t-t0)))*(1+erf(-z*(t-tf)))/(tf-t0) #Normalised wtr. to the total interaction time

def Hcoeff_list(settings : dict):
    """Get a list of the 3*M activation functions
    settings: dict with following keys, 
    
    M : number of steps in protocol
    T : Time required to implement Rabi gate
    dT : Time delay between each gate
    Tdelay : Time delay beween each 3-gate step 
    z: sensitivity of the activation function
    """
    M, T, dT, Tdelay, z = settings.values()

    def t0(gate : int, k : int):
        """Start time of gate
        """
        return float(k*Tdelay + gate*(T+dT))
        
    def tf(gate: int, k: int):
        """Stop time of gate
        """
        return float(t0(gate, k) + T)

    Hcoeffs = [partial(activate, t0(gate, k), tf(gate, k), z) for k in range(M) for gate in range(3)]
    return Hcoeffs
