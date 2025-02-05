#
# Two-can system simulation
# ME 144L Lab - Fall 2023
# ER Update to Fall 2022 Code: Plot Dashed Lines
#
import math
import numpy as np
import matplotlib.pyplot as plt
import rkcode
import random

# define the system ODEs
def two_can(x, t, K1, K2):
	V1, V2 = x[0], x[1]
	if V1 <= 0.0:
		Q1 = 0
	else:
		Q1 = K1*np.sqrt(abs(V1))

	if V2 <= 0.0: 
		Q2 = 0
	else:
		Q2 = K2*np.sqrt(abs(V2))

	# specify outputs
	y = [Q1, Q2]

	return np.array([-Q1, +Q1-Q2]), y

V1o, V2o = 850, 0
dt, t0, tf = 0.001, 0.0, 100
N = math.floor(abs(tf-t0)/dt)
x0 = np.array([V1o, V2o])
t = np.linspace(0, tf, N)
# values for Cans 202001 and 202002
# K1, K2 = 0.6475793359183775, 0.24142018676686405 # this is K/2
K1, K2 = 1.14016665 , 0.52438293
sol1 = rkcode.rk4fixed(two_can, x0, t, args=(K1, K2))
V11 = sol1[:,0]
V21 = sol1[:,1]
# compute outputs
Q11, Q21 = [], []
for i in range(len(t)):
	_, y = two_can(sol1[i,:], t[i], K1, K2)
	Q11.append(y[0])
	Q21.append(y[1])

print("Peak volume in V2 is :" + str(max(V21)))

# run with ideal values
K1, K2 = 0.7624878 , 0.2478054
sol2 = rkcode.rk4fixed(two_can, x0, t, args=(K1, K2))
V12 = sol2[:,0]
V22 = sol2[:,1]
# compute outputs
Q12, Q22 = [], []
for i in range(len(t)):
	_, y = two_can(sol2[i,:], t[i], K1, K2)
	Q12.append(y[0])
	Q22.append(y[1])

print("Peak volume in V2-ideal is :" + str(max(V22)))

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Two-can simulation')
ax1.plot(t, V11, c='b', label='V1')
ax1.plot(t, V21, c='b', linestyle = 'dashed', label='V2')
ax1.plot(t, V12, c='r', label='V1-ideal')
ax1.plot(t, V22, c='r', linestyle = 'dashed', label='V2-ideal')
ax1.legend(loc="upper right")
ax2.plot(t, Q11, c='b', label='Q1')
ax2.plot(t, Q21, c='b', linestyle = 'dashed', label='Q2')
ax2.plot(t, Q12, c='r', label='Q1-ideal')
ax2.plot(t, Q22, c='r', linestyle = 'dashed', label='Q2-ideal')
ax2.legend(loc="upper right")
plt.xlabel('Time (sec)')
plt.grid()
plt.show()