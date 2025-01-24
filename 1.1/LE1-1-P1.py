import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

filename  = 'LE1-1_pt1.csv'
# --------------------
# Insert code here:
Voltage   = np.array([1.176, 1.648, 1.874, 2.175, 2.438, 2.503, 2.925, 3.067, 3.450, 3.686, 4.014]).reshape((-1,1))
Angles = np.array([-1.57, -1.26, -0.94, -0.63, -0.31, 0., 0.31, 0.65, 0.96, 1.23, 1.52])

# Linear Regression
model    = LinearRegression().fit(Voltage, Angles.reshape(-1, 1))
Rsquared = model.score(Voltage, Angles)
slope, intercept = model.coef_, model.intercept_
print('intercept =', intercept)
print('slope =', slope)
print('coefficient of determination =', Rsquared)

# Plot the raw data and regression using a scatter plot
plt.figure(2)
plt.scatter(Voltage,Angles, c="r", marker='x')
plt.plot(Voltage,slope*Voltage + intercept)
plt.xlabel('Voltage [V]')
plt.ylabel('Angles [radians]')
plt.legend(['Raw Data','Lin. Reg.'])
plt.title('Regression of Sensor Data')
plt.grid()
plt.show()