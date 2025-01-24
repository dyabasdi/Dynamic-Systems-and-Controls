import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
import rkcode

# Read a data file and plot the data
# currently just reads (time,voltage) data from potentiometer example

plt.close('all') # close all plots

# --------------------------------------
# Load and select data
# --------------------------------------
fileName = "TA_Data.csv" # set to your specific filename

# Read csv file
data = pd.read_csv(fileName)

# Extract data from dataframe
t  = np.array(data.Time)
v = np.array(data.voltage)
theta = v*(-62.70) + 168.66

# Set T1 and T2 to plot data over times of interest
# Plot all data: 
T1,T2 = 1, t[-1]
# or choose specific endpoints as below:
#T1,T2 = 1.05, 3.8
# the next lines determine the index values for your specified times
it1 = np.nonzero(t > T1)[0][0]
it2 = np.nonzero(t < T2)[0][-1]

# create new arrays for values between T1 and T2
T  = t[it1:it2] - t[it1] # Resets time to zero seconds
V = v[it1:it2]
Theta = theta[it1:it2]

####simulated data
def comp_pen(x, t, m, g, lc, j, b, t0):
	xdot1 = x[1]
	xdot2 = - (m*g*lc*np.sin(x[0]) + b*x[1] + t0*np.sign(x[1])) / j #t0 is the most dominant
	# specify outputs
	y = 0

	return np.array([xdot1, xdot2]), y


m = 0.157
g = 9.81
j = 0.00675
lc = 0.19925
b = 0.00001
t0 = 0.007
# initially deflect and release mass from rest
x0 = np.array([np.pi/2, 0.0])

t4 = np.linspace(1.6, 20, 1001)
sol4 = rkcode.rk4fixed(comp_pen, x0, t4, args=(m, g, lc, j, b, t0))

plt.plot(t4-2, (sol4[:, 0]*180/np.pi) + 49.5, 'r--', label='rk4fixed')

# --------------------------------------
# Plots
# --------------------------------------
# Plot voltage vs time
plt.plot(T,Theta)
plt.xlabel('Time [s]')
plt.ylabel('Theta [deg]')
plt.show()