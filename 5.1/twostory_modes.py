# two story model (damped)

import math
import numpy as np
from numpy.linalg import eig
from scipy.signal import lsim, lti
import matplotlib.pyplot as plt

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

print('Imaginary v0:', v0)
print('Imaginary v1:', v1)
print('Imaginary v2:', v2)
print('Imaginary v3:', v3)

IC_2 = np.real(v0)/np.real(v0[1])
IC_1 = np.real(v3)/np.real(v3[1])

print('IC_1 = ', IC_1)
print('IC_2 = ', IC_2)

IC = IC_1


plt.plot([1.5,1+IC_1[1],1+IC_1[3]],[0,1,2],'o')
plt.plot([5+0.5,5+IC_2[1],5+IC_2[3]],[0,1,2],'o')
plt.xlim([0,8])
plt.ylim([0,3])
plt.show()


