#
# Pendulum simulation
#
import numpy as np
import matplotlib.pyplot as plt
import rkcode

# define the system ODEs
def comp_pen(x, t, m, g, lc, j, b, t0):
	xdot1 = x[1]
	xdot2 = -( m*g*lc*np.sin(x[0]) + b*x[1] + t0*np.sign(x[1]) )/j
	# specify outputs
	y = 0

	return np.array([xdot1, xdot2]), y

m = 0.257
g = 9.81
j = 0.007996
lc = 0.13572
b = 0
t0 = 0


# initially deflect and release mass from rest
x0 = np.array([-np.pi/2, 0.0])

t1 = np.linspace(0, 4, 1001)
t4 = np.linspace(0, 4, 101)
sol4 = rkcode.rk4fixed(comp_pen, x0, t4, args=(m, g, lc, j, b, t0))

plt.plot(t4, sol4[:, 0], 'o', label='rk4fixed')
plt.xlabel('t')
plt.grid()
plt.show()
