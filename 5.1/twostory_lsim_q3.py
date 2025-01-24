# two story model
# ME 144L Spring 2022

import math
import numpy as np
from numpy.linalg import eig
from scipy.signal import lsim, lti
import matplotlib.pyplot as plt

# Sample values
m1 = 0.65
m2 = 0.65
k1 = 111
k2 = 111
b1 = 0.001
b2 = 0.001

# Space Eqnt 1: X dot = Ax + Bu
# A = 4 x 4 matrix (coefficients ahead of x1, v1, x2, v2)
# x = [[x1],[v1],[x2],[v2]] (vertical 4x1 matrix)
# B = coefficients ahead of F(t)
# u = F(t)

amat = np.array([[0,1,0,0],[-k1/m1,-(b1+b2)/m1,k2/m1,b2/m1],
                 [0,-1,0,1],[0,b2/m2,-k2/m2,-b2/m2]]) #coefficients ahead of x1, v1, x2, and v2

bmat = np.array([[0],[0],[0],[0]]) #(vertical 4x1 matrix, coefficients ahead of F(t))

# displacements as outputs

# State Space Eqnt 2: y = Cx + Du
# C = 2 x 4 matrix for v1dot and v2dot
# x = [[x1],[v1],[x2],[v2]] (vertical 4x1 matrix)
# D = 2 x 1 matrix
cmat = np.array([[-k1/m1,-(b1+b2)/m1,k2/m1,b2/m1],[0,b2/m2,-k2/m2,-b2/m2]])

dmat = np.array([[0],[0]])

# linear simulation

sys = lti(amat,bmat,cmat,dmat)

t = np.linspace(0,5, num = 500)
u = np.zeros_like(t)
x0 = np.array([0.01,0.0,0.005,0])

tout, y, x = lsim(sys, u, t, x0)

plt.plot(t,y)
plt.legend(['Acceleration 1', 'Acceleration 2'])
plt.xlabel('Time [s]')
plt.ylabel("Acceleration [m/s^2]")
plt.title("Acceleration vs Time (Simulated)")
plt.grid()
plt.show()