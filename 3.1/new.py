import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression

plt.close('all')

# %% Section 1: Beam Parameters and Calculations

L = 0.36  # [m] put your own value pls 
h = 0.0025   # [m]
w = 0.025    # [m]
E = 68.9e9        # [Pa]
I = (1/12)*w*h**3 # [m^3]
rho = 2700        # [kg/m^3]
Mbeam = L*h*w*rho # [kg]
Mlump = (65 + 3.5)/1000 
# Calculate Theoretical Stiffness
Kth = 3*E*I/(L**3)


# Calculate Natural Frequency Bounds
wn_th_min = np.sqrt(Kth/(Mlump + Mbeam))
wn_th_DH  = np.sqrt(Kth/(Mlump + 0.23*Mbeam))
wn_th_max = np.sqrt(Kth/(Mlump + 0 * Mbeam))



# %% Section 2: Read CSV File and Calibrate Raw Data

filename = 'beamtest.csv'
data = pd.read_csv(filename)

time = np.array(data.Time)
z = np.array(data.accZ) # [counts]


# convert counts to gs
conv_accel =  0.244e-3 # 2g range; convert from int to float in [g]
# NOTE: 0.061 for 2g, 0.122 for 4g, 0.244 for 8g, 0.488 for 16g

accz_g = conv_accel*z  # [g]



accz_g = accz_g - np.mean(accz_g)



# %% Section 3: Analyze Data Subset


#T1, T2 = 0, time[-1]
T1, T2 = 4.69, 25
it1 = np.nonzero(time > T1)[0][0]
it2 = np.nonzero(time < T2)[0][-1]

Tz, Az = time[it1:it2], accz_g[it1:it2]


dist = 5

Az_its, _ = find_peaks(Az, height=0, distance = dist)
Az_peaks  = Az[Az_its] # Solves for peak values using wx_its iteration values
Tz_peaks  = Tz[Az_its]
Tz_avg    = np.mean(np.diff(Tz_peaks))
wd_exp    = 2*np.pi / Tz_avg


# Solve for zeta:
    
N      = 30
Nvec   = np.arange(1,N+1,1)
A0     = Az_peaks[0]
lnA0An = np.log(A0/Az_peaks[Nvec])

# Reshape Nvec and LnA0An for Linear Regression
Nvec   = Nvec.reshape(-1, 1)
lnA0An = lnA0An.reshape(-1, 1)

# Linear Regression
Zmodel = LinearRegression(fit_intercept = False).fit(Nvec, lnA0An)
ZR2    = Zmodel.score(Nvec, lnA0An)
Beta, Zint = float(Zmodel.coef_), float(Zmodel.intercept_)

# # Solve for zeta
# zeta = 

# # Equation for wd = wn*sqrt(1 - zeta^2)
# wn_exp =  # [rad/s]

# # Solve for effective mass
# m_eff   = 
# m_diff  = 
# mb_diff = 

# # Solve for damping coefficient (b) value
# bexp = 




# # # %% All Print Commands
# # #---------------------------
# print('---------------------------------------------------------')
# print('Theoretical Stiffness and Natural Frequency Bounds:')
# print("Theoretical Stiffness [N/m] = %3.2f" %(Kth))
# print("Omega_n Min [rad/s] = %3.6f" %(wn_th_min))
# print("Omega_n DH  [rad/s] = %3.6f" %(wn_th_DH))
# print("Omega_n Max [rad/s] = %3.6f" %(wn_th_max))
# print('---------------------------------------------------------')
# print('---------------------------------------------------------')
# print("Experimental Signal Freq. [Hz] = %3.4f" %(1/Tz_avg))
# print("Experimental period [s]        = %3.4f" %(Tz_avg))
# print("Damped Natural Freq. [rad/s]   = %3.4f" %(wd_exp))
# print('---------------------------------------------------------')
# print('---------------------------------------------------------')
# print("Beta (slope) = % 3.5f" %(Beta))
# print("R squared    = % 3.5f" %(ZR2))
# print("Zeta         = % 3.5f" %(zeta))
# print('---------------------------------------------------------')
# print('---------------------------------------------------------')
# print('Experimental Damped and Natural Frequencies Results:')
# print("Omega_d Exp [rad/s] = %3.6f" %(wd_exp))
# print("Omega_n Exp [rad/s] = %3.6f" %(wn_exp))
# print('---------------------------------------------------------')
# print('---------------------------------------------------------')
# print("Effective Mass [kg] = %3.6f" %(m_eff))
# print("Percentage of beam mass in Effective Mass [%%] = %3.2f" %(mb_diff))
# print("(Compare to DH Method value of 23%)")
# print('---------------------------------------------------------')
# print('---------------------------------------------------------')
# print("Damping Coefficient, b [N*s/m] = %3.5f" %(bexp))
# print('---------------------------------------------------------')

# %% Section 4: Print all calculated values

plt.figure()
plt.plot(Tz, Az, label='z')
plt.plot(Tz_peaks,Az_peaks,'rx')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel("Acceleration Z [g]")
plt.title("Acceleration vs Time")
plt.show()

# plt.figure()
# plt.plot(Nvec, lnA0An,'o')
# plt.plot(Nvec,Nvec*Beta)
# plt.grid()
# plt.xlim([0, N+1])
# plt.xlabel('Peak Number')
# plt.ylabel('ln(A0/An)')
# plt.legend(["ln(A0/An)","Regression"])
# plt.show()

