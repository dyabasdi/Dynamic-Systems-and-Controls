# Student Edition of Lab 9: Motor Characterization
# Updated 4/9/21

# Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression 

plt.close('all')

#%% Section 0: Variables
GR   = 45
Rm   = 38.5 # [Ohm], Measured Motor Resistance

# %% Section 1: Read CSV File and collect data

#---------------------------
# Import file and read data
#---------------------------
filename = 'Data/PWM_Step_20Hz-New.csv'  
data = pd.read_csv(filename)

# dataNames = ['Time', 'load', 'Xacc','Yacc','Zacc']
time    = np.array(data.Time)   # [s]
Pulses  = np.array(data.Pulses) # [int]
wm_test = np.array(data.wm)     # [rad/s]
PWM     = np.array(data.PWM)    # [int]
Vbus    = np.array(data.Vbus)   # [V]

# Moving AVG of Vbus
numbers_series = pd.Series(Vbus)
windows = numbers_series.rolling(20)
Vbus_ma = windows.mean()

# Raw Data Figures
fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(time, wm_test, label='$\omega_m$')
ax1.plot(time,PWM,label='PWM')
ax1.set_title("Motor Speed [rad/s] and PWM output [int] vs Time [s]")
ax1.grid()
ax1.legend()
ax1.set_ylabel("Amplitude")

# Plot Vbus and Moving AVG of Vbus
ax2.plot(time, Vbus, label='$Vbus$')
ax2.plot(time, Vbus_ma, label='Moving Avg')
ax2.set_title("Bus Voltage [V] vs Time [s]")
ax2.grid()
ax2.legend()
ax2.set_ylabel("Amplitude")
ax2.set_xlabel("Time [s]")
plt.show()

#%% Section 2: Build table with with test results
PWM = [0, 20, 40,  60,  80, 100]
Im  = [0,3.4,9.2,17.6,27.9,39.5]
#------------
# Begin PWM at value that it begins to spin
PWM = np.array([140, 160, 180, 200, 220, 240, 255]) # [PWM Int]
wm  = np.array([200,230, 275, 305, 350, 385, 415]) # [rad/s]
Im  = np.array([27.5, 27.5, 27.9, 28.3, 29.4, 30.5, 31.7])/1000 # [A]
vB  = np.array([5, 5, 5, 5, 5, 5, 5]) # vbus corresponding to PWM values [V]
wm_OS = wm/GR # [rad/s]

# Calculate Back EMF voltage
Vm  = []
Veq = [] # Veq = Vbus*PWM/PWMmax 
for i in range(len(PWM)):
    PWMratio = PWM[i]/255
    Vin_calc = PWMratio * vB[i]
    Vm_calc  = Vin_calc - Rm * Im[i]
    Veq.append(Vin_calc)
    Vm.append(Vm_calc)


#----------------------------------------------------------------------------
# Linear Regressions for rm
#----------------------------------------------------------------------------
# Use this if you do not have a DMM for current measurements
wmval = wm.reshape(-1,1)
model = LinearRegression().fit(wmval,Veq)
R2    = model.score(wmval,Veq)
slope1, intc1 = float(model.coef_), float(model.intercept_)
print('Vin slope [V/(rad/s)]:', slope1)
print('Vin intercept [V]:', intc1)
print('Vin R^2:', R2)


# Use this if you have your own current measurements
model = LinearRegression().fit(wmval, Vm)
R2   = model.score(wmval, Veq)
slope2, intc2 = float(model.coef_), float(model.intercept_)
print('Vm slope [V/(rad/s)]:', slope2)
print('Vm intercept [V]:', intc2)
print('Vm R^2:', R2)




#----------------------------------------------------------------------------
# Solve for Motor Constant and Motor Torque
#----------------------------------------------------------------------------
rm_veq = slope1 # [V/(rad/s)]
rm     = slope2 # [V/(rad/s)]
Tm     = ([27.5*rm/1000, 27.5*rm/1000, 27.9*rm/1000, 28.3*rm/1000, 29.4*rm/1000, 30.5*rm/1000, 31.7*rm/1000]) # [N*m]

# Voltage (Input and Equivalent) vs Motor Speed
plt.figure()
plt.plot(wm, Veq,'-o')
plt.plot(wm, Vm,'-o')
plt.plot(wm, wm*rm_veq + intc1,'--r')
plt.plot(wm, wm*rm + intc2,'--k')
plt.title('$V_{in}$ and $V_{m}$ vs $\omega_m$')
plt.legend(['$V_{in}$','$V_{m}$','$V_{in}$ reg.','$V_{m}$ reg.'])
plt.grid()
plt.xlabel('$\omega_m$ [$rad/s$]')
plt.ylabel('Voltage [V]')
plt.axis([0, wm[-1]+10, 0, Veq[-1]+0.5])
plt.show()

#----------------------------------------------------------------------------
# Linear Regression for Bm
#----------------------------------------------------------------------------
model = LinearRegression(fit_intercept=True).fit(wmval, Tm)
R2   = model.score(wmval, Tm)
slope, intc = float(model.coef_), float(model.intercept_)
print('Tm slope [N*m/(rad/s)]:', slope)
print('Tm intercept [N*m]:', intc)
print('Tm R^2:', R2)
Tc = intc
Bm = slope # [N*m*s/rad]
print('Bm value [N*m*s/rad]:', Bm)


#%% Figures

# Stall Torque
Ts = rm/Rm*Veq[-1]
wm_noload = (Ts + Tc)/(rm**2/Rm + Bm)

# Combine data points for figure
X = [0, wm_noload]
Y = [Ts, 0]

# Stall Torque
Ts1 = rm/Rm*Veq[-2]
wm_noload1 = (Ts1 + Tc)/(rm**2/Rm + Bm)

# Combine data points for figure
X1 = [0, wm_noload1]
Y1 = [Ts1, 0]

# Stall Torque
Ts2 = rm/Rm*Veq[-3]
wm_noload2 = (Ts2 + Tc)/(rm**2/Rm + Bm)

# Combine data points for figure
X2 = [0, wm_noload2]
Y2 = [Ts2, 0]


# Motor Torque vs Motor Speed
plt.figure()
plt.plot(wm, Tm,'-o')
plt.plot(wm, Bm*wm + intc,'--r')
plt.plot(X,Y,'-o')
plt.plot(X1,Y1,'-o')
plt.plot(X2,Y2,'-o')
plt.title('$T_m$ vs $\omega_m$')
plt.grid()
plt.xlabel('$\omega_m$ [$rad/s$]')
plt.ylabel('$T_m$ [N*m]')
plt.legend(['Tm','Tm reg.', f'T-w curve:{Veq[-1]:.2f}V', f'T-w curve:{Veq[-2]:.2f}V', f'T-w curve:{Veq[-3]:.2f}V'])
plt.show()