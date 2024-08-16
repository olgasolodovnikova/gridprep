import numpy as np
import qutip as q

#Setting of main system parameters

N = 100
hbar = 1
pi = np.pi
oma = pi/2
omc = pi/2

#Qubit ops
sz = q.tensor(q.sigmaz(), q.identity(N))
sy = q.tensor(q.sigmay(), q.identity(N))
sx = q.tensor(q.sigmax(), q.identity(N))

sm = q.tensor(q.sigmam(), q.identity(N))
sp = q.tensor(q.sigmap(), q.identity(N))


#Cavity ops
ad = q.tensor(q.identity(2), q.create(N))
a = q.tensor(q.identity(2), q.destroy(N))

x = q.tensor(q.identity(2), q.position(N))
p = q.tensor(q.identity(2), q.momentum(N))