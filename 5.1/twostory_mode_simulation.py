# two story model - selective mode simulation
# DSC Lab Spring 2022

import math
import numpy as np
from numpy.linalg import eig
from scipy.signal import lsim, lti
import matplotlib.pyplot as plt
import spectrum_tools


# mass = 0.65 kg
# force = 2.0 N
# stiffness = force/delta
# 
m1 = 0.65
m2 = 0.65
k1 = 111
k2 = 111
b1 = 0.001
b2 = 0.001
#
# eigenvalue analysis
# 
amat = np.array([[0,1,0,0],[-k1/m1,-(b1+b2)/m1,k2/m1,b2/m1],
                 [0,-1,0,1],[0,b2/m2,-k2/m2,-b2/m2]])

w,v = eig(amat)
print('E-values:', w)
# absolute values give wn (rad/sec) 
w0Hz = np.abs(w[0]/(2*math.pi))
print('w0Hz:',w0Hz)
w1Hz = np.abs(w[1]/(2*math.pi))
print('w1Hz:',w1Hz)
w2Hz = np.abs(w[2]/(2*math.pi))
print('w2Hz:',w2Hz)
w3Hz = np.abs(w[3]/(2*math.pi))
print('w3Hz:',w3Hz)

# column v[:,i] is the eigenvector corresponding to the eigenvalue w[i]
v0 = v[:,0]
v1 = v[:,1]
v2 = v[:,2]
v3 = v[:,3]

print(np.real(v0))
print(np.real(v1))
print(np.real(v2))
print(np.real(v3))

IC_2 = np.real(v0)/np.real(v0[1])
IC_1 = np.real(v3)/np.real(v3[1])

print('IC_1 = ', IC_1)
print('IC_2 = ', IC_2)

# linear simulation

bmat = np.array([[0],[0],[0],[0]])
# accelerations as outputs
cmat = np.array([[-k1/m1,-(b1+b2)/m1,k2/m1,b2/m1],[0,b2/m2,-k2/m2,-b2/m2]])
# displacements as outputs
# cmat = np.array([[0,1,0,0],[0,0,0,1]])
dmat = np.array([[0],[0]])

sys = lti(amat,bmat,cmat,dmat)

t = np.linspace(0,10, num = 1000)
u = np.zeros_like(t)
x01 = IC_1 # initial conditions for Mode 1
x02 = IC_2 # initial conditions for Mode 2

# run both simulations
tout1, y1, x1 = lsim(sys, u, t, x01)
tout2, y2, x2 = lsim(sys, u, t, x02)

fig, (ax1, ax2,ax3) = plt.subplots(3)
fig.suptitle('Single Mode Response Simulation')
fp1,Gy1y1p=spectrum_tools.compare_modes(tout1,y1[:,0],0.005)
fp2,Gy2y2p=spectrum_tools.compare_modes(tout1,y1[:,1],0.005)
ax1.plot(tout1, y1[:,0], label='Mode 1: xk1')
ax1.plot(tout1, y1[:,1], label='Mode 1: xk2')
ax1.legend(loc="upper right")
ax2.bar(fp1,Gy1y1p,color='b',width=0.25)
ax2.set_xlim(0,5)
ax2.set_ylim(0,1.5)
ax3.bar(fp2,Gy2y2p,color='g',width=0.25)
ax3.set_xlim(0,5)
ax3.set_ylim(0,1.5)
plt.show()


fig, (ax1, ax2,ax3) = plt.subplots(3)
fig.suptitle('Single Mode Response Simulation')
fp1,Gy1y1p=spectrum_tools.compare_modes(tout2,y2[:,0],0.005)
fp2,Gy2y2p=spectrum_tools.compare_modes(tout2,y2[:,1],0.005)
ax1.plot(tout2, y2[:,0], label='Mode 1: xk1')
ax1.plot(tout2, y2[:,1], label='Mode 1: xk2')
ax1.legend(loc="upper right")
ax2.bar(fp1,Gy1y1p,color='b',width=0.25)
ax2.set_xlim(0,5)
ax2.set_ylim(0,1.5)
ax3.bar(fp2,Gy2y2p,color='g',width=0.25)
ax3.set_xlim(0,5)
ax3.set_ylim(0,1.5)
plt.show()