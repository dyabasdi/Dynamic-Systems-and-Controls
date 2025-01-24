import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spectrum_tools

# Make sure to update the data filename
# Also make sure this file is update for the data collected
# This version assumes collection of IMU data from two daisy-chained LSM6DSO devices
# All data may not have been collected, depending on what you did in lab

plt.close('all')
filename = 'top-1cm.csv'
data = pd.read_csv(filename)

time = np.array(data.Time)
# x1 = np.array(data.accX1) # [counts]
y1 = np.array(data.accY1) # [counts]
# z1 = np.array(data.accZ1) # [counts]
# wx1 = np.array(data.wx1)  # [counts]
# wy1 = np.array(data.wy1)  # [counts]
# wz1 = np.array(data.wz1)  # [counts]
# x2 = np.array(data.accX2) # [counts]
y2 = np.array(data.accY2) # [counts]
# z2 = np.array(data.accZ2) # [counts]
# wx2 = np.array(data.wx2)  # [counts]
# wy2 = np.array(data.wy2)  # [counts]
# wz2 = np.array(data.wz2)  # [counts]

# convert counts to gs
conv_accel =  0.061e-3 # 2g range; convert from int to float in [g]
# NOTE: 0.061 for 2g, 0.122 for 4g, 0.244 for 8g, 0.488 for 16g
# accx1_g = conv_accel*x1  # [g]
accy1_g = conv_accel*y1   # [g] 
# accz1_g = conv_accel*z1  # [g]
# accx2_g = conv_accel*x2   # [g]
accy2_g = conv_accel*y2   # [g] 
# accz2_g = conv_accel*z2  # [g]

conv_gyro =  4.375e-3   #  125 dps range; convert from int to float in [dps]
# NOTE: 4.375 for 125 dps, 8.75 for 250, 17.50 for 500, 35 for 1000, 70 for 2000
# wx1_dps = conv_gyro*wx1   # [dps]
# wy1_dps = conv_gyro*wy1   # [dps]
# wz1_dps = conv_gyro*wz1   # [dps]
# wx2_dps = conv_gyro*wx2   # [dps]
# wy2_dps = conv_gyro*wy2   # [dps]
# wz2_dps = conv_gyro*wz2   # [dps]

plt.figure()
plt.plot(time, accy1_g*9.81, label='Acceleration 1')
plt.plot(time, accy2_g*9.81, label='Acceleration 2')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel("Acceleration [m/s^2]")
plt.title("Acceleration vs Time (Experimental)")

# plt.figure()
# plt.plot(time, wx1_dps, label='wx1')
# plt.plot(time, wy1_dps, label='wy1')
# plt.plot(time, wz1_dps, label='wz1')
# plt.plot(time, wx2_dps, label='wx2')
# plt.plot(time, wy2_dps, label='wy2')
# plt.plot(time, wz2_dps, label='wz2')
# plt.grid()
# plt.legend()
# plt.xlabel('Time [s]')
# plt.ylabel('Angular velocity [deg/sec]')
# plt.title('Gyro Data vs Time')
plt.show()

fp1, Gy1y1p = spectrum_tools.compare_modes(time, accy1_g, 0.005)
fp2, Gy2y2p = spectrum_tools.compare_modes(time, accy2_g, 0.005)

fig, (ax1, ax2, ax3) = plt.subplots(3)
fig.suptitle('Single Mode Response Simulation')
ax1.plot(time, accy1_g, label='Mode 1: xk1')
ax1.plot(time, accy2_g, label='Mode 1: xk2')
ax1.set_ylabel("Acceleration [m/s^2]")
ax1.legend(loc='upper right')

ax2.bar(fp1, Gy1y1p, color = 'b', width = 0.25)
ax2.set_xlim(0,6)
ax2.set_ylim(0,0.5)
ax3.bar(fp2, Gy2y2p, color = 'k', width = 0.25)
ax3.set_xlim(0,6)
ax3.set_ylim(0,0.5)

plt.xlabel("Frequency (rad/s)")
plt.show()