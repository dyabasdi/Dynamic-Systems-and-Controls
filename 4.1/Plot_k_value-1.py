import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from sklearn.linear_model import LinearRegression 

Vol1 = np.array([0,100,200,300,400,500])
T1=np.array([0,14.07,22.58,28.47,32.32,39.58]).reshape(-1, 1)

Vol2 = np.array([0,100,200,300,400,500])
T2=np.array([0,19.78,40.08,56.86,68.92,79.44]).reshape(-1, 1)

Vol_sqrt1 = np.sqrt(Vol1)
Vol_sqrt2 = np.sqrt(Vol2)

model    = LinearRegression().fit(T1, Vol_sqrt1 )
Rsquared = model.score(T1, Vol_sqrt1)
slope, intercept = model.coef_, model.intercept_
print('intercept =', intercept)
print('slope =', slope)
print('coefficient of determination =', Rsquared)

K1 = slope*2
print('K1:', K1)

plt.figure(1)
plt.scatter(T1,Vol_sqrt1, c="r", marker='x')
plt.plot(T1,slope*T1 + intercept)
plt.xlabel('Time(s)')
plt.ylabel('sqrt of Vol')
plt.legend(['Lin. Reg.','Raw Data'])
plt.title('Regression of Sensor Data')
plt.grid()
plt.show()

model    = LinearRegression().fit(T2, Vol_sqrt2 )
Rsquared = model.score(T2, Vol_sqrt2)
slope, intercept = model.coef_, model.intercept_
print('intercept =', intercept)
print('slope =', slope)
print('coefficient of determination =', Rsquared)

K2 = slope*2

print('K2:', K2)
plt.figure(2)
plt.scatter(T2,Vol_sqrt2, c="r", marker='x')
plt.show()
plt.plot(T2,slope*T2 + intercept)
plt.xlabel('Time(s)')
plt.ylabel('sqrt of Vol')
plt.legend(['Lin. Reg.','Raw Data'])
plt.title('Regression of Sensor Data')
plt.grid()
plt.show()