import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')
filename = 'zero_g_test1695673150.csv'
data = pd.read_csv(filename)

time = np.array(data.Time)
x = np.array(data.accX) # [counts]
y = np.array(data.accY) # [counts]
z = np.array(data.accZ) # [counts]
wx = np.array(data.wx)  # [counts]
wy = np.array(data.wy)  # [counts]
wz = np.array(data.wz)  # [counts]

# convert counts to gs
conv_accel =  0.061e-3 # 2g range; convert from int to float in [g]
# NOTE: 0.061 for 2g, 0.122 for 4g, 0.244 for 8g, 0.488 for 16g
accx_g = conv_accel*x   # [g]
accy_g = conv_accel*y   # [g] 
accz_g = conv_accel*z  # [g]

conv_gyro =  4.375e-3   #  125 dps range; convert from int to float in [dps]
# NOTE: 4.375 for 125 dps, 8.75 for 250, 17.50 for 500, 35 for 1000, 70 for 2000
wx_dps = conv_gyro*wx   # [dps]
wy_dps = conv_gyro*wy   # [dps]
wz_dps = conv_gyro*wz   # [dps]

acc_mean_x = np.mean(accx_g)
acc_mean_y = np.mean(accy_g)
acc_mean_z = np.mean(accz_g)

accel_std_x = np.std(accx_g)
accel_std_y = np.std(accy_g)
accel_std_z = np.std(accz_g)

gyro_mean_x = np.mean(wx_dps)
gyro_mean_y = np.mean(wy_dps)
gyro_mean_z = np.mean(wz_dps)

gyro_std_x = np.std(wx_dps)
gyro_std_y = np.std(wy_dps)
gyro_std_z = np.std(wz_dps)

print('Accel Avg:', acc_mean_x, acc_mean_y, acc_mean_z)
print('Accel STD:', accel_std_x, accel_std_y, accel_std_z)

print('Gyro Avg:', gyro_mean_x, gyro_mean_y, gyro_mean_z)
print('Gyro STD:', gyro_std_x, gyro_std_y, gyro_std_z)


plt.figure()
plt.plot(time, accx_g, label='x')
plt.plot(time, accy_g, label='y')
plt.plot(time, accz_g, label='z')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel("Acceleration [g]")
plt.title("Acceleration vs Time")

plt.figure()
plt.plot(time, wx_dps, label='wx')
plt.plot(time, wy_dps, label='wy')
plt.plot(time, wz_dps, label='wz')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [deg/sec]')
plt.title('Gyro Data vs Time')
plt.show()