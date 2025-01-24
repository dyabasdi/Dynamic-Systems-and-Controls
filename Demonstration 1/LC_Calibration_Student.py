# Linear Regression of Load Cell Data
# Demonstration 1 - Calibrated Scale
# ME 144L

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression 


# Raw Data - To be filled in
Mass    = np.array([0, 10, 20, 50, 100]) # [g]
LC_data = np.array([69583, 101477, 131410, 224209, 378904]) # [int]


# Reshape Data (no adjustment required here)
LC_data = LC_data.reshape(-1, 1)

# Fit intercept value - Choose one option.
FIT = True
# FIT = False

# Linear Regression - fill in parentheses with correct data arrays
LCmodel     = LinearRegression(fit_intercept = FIT).fit(LC_data , Mass)
R2          = LCmodel.score(LC_data, Mass) 
Slope, Intc = float(LCmodel.coef_), float(LCmodel.intercept_)

# Print Slope, Int, and R2 outputs here with all corresponding units:
print('Slope:', Slope)
print('Intercept:', Intc)
print('R2:', R2)


# Figures
plt.figure()
plt.plot(LC_data, Mass,'o')
plt.plot(LC_data,LCmodel*Slope + Intc)
plt.grid()
plt.xlabel('')
plt.ylabel('')
plt.legend(["Raw Data","Regression"])
plt.title('Load Cell Calibration Regression')
plt.show()




# Unknown Weight Determination: 
# Record the integer value from measuring the unknown mass in the Int_Reading space
# Use the linear regression (y = m*x + b) to determine the unknown mass value

Int_Reading = 

Unknown_Mass = 

print("Unknown Mass [g] = ", Unknown_Mass)
