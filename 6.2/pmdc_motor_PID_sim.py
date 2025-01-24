#
# PMDC motor model
# R.G. Longoria 8-4-20 v1
import math
import numpy as np
import matplotlib.pyplot as plt
import rk
import random

# define the system ODEs
def pmdc(x, t, rm, Rm, Bm, Jm, To, vin):
    omegam, thetam = x[0], x[1]
    im = (vin - rm*omegam)/Rm
    omegamdot = (rm*im - Bm*omegam - To*np.tanh(omegam/1))/Jm
    thetamdot = omegam
	# specify outputs

    y = im

    return np.array([omegamdot, thetamdot]), y

# all parameter units in SI
rm = 0.0107		# motor constant, N*m/A
Rm = 30 		# motor armature resistance, ohms
Bm = 0.000178475e-3	# motor damping
Jm = 0.5*0.009*(0.25/39.37)**2		# motor inertia, kg*m^2, ignores gears
# print("Jm = " + str(Jm))
GR = 48			# gear ratio
Tmo = 1*0.1838e-3 # coulombic bearing torque in motor

# set up for simulation
t, vin, im, omega, theta, e_omega, omegar = [], [], [], [], [], [], []
sum_ev = [] # for discrete PID I control

vb = 4.5		# bus voltage
Kp = 2.75       # P-control gain
Ki = 0.01       # I-control gain
Kd = 4*0.5      # D-control gain
# control loop
i = 1 # tracking index
tc, vinc, imc, omegac, thetac = 0, 0, 0, 0, 0 # initial conditions
t.append(tc)
vin.append(vinc)
im.append(imc)
omega.append(omegac)
theta.append(thetac)
e_omegac, sum_e = 0, 0
e_omega.append(e_omegac)
omegar.append(0)
omegac_p = 0

omega_d = 182 # desired velocity for testing; equal to 29 rev/sec (low speed)

theta_d = 180*GR # desired angle to turn, 180 degrees on output converted to motor side
tinterval = (theta_d*math.pi/180)/omega_d # estimate time 'on' to achieve theta_d
print(tinterval)

dt = 0.05
ton = 0.1
toff = ton + tinterval # note, this tinterval also used in experiments

while tc < 2:
	# determine next step
    # note: use rev/sec to match with Arduino code
    # first, the feedforward part
    if (tc>ton) and (tc<toff):
        omega_r = omega_d
        rps_r = omega_d/(2*math.pi)
        uff = (Rm*(Tmo*math.tanh(omega_d/500)+Bm*omega_d)/rm + rm*omega_d)/vb
    else:
        omega_r = 0
        rps_r = 0
        uff = 0
 
    omegar.append(omega_r) # smae the reference / command 
    rpsc = omegac/(2*math.pi) # find current omega in rev/sec
    e_omegac = omega_r - omegac # error in rad/sec
    e_rpsc = e_omegac/(2*math.pi) # error in rev/sec - as in Arduino code

    sum_e = sum_e + (e_omegac + e_omega[i-1])/2
    sum_erps = sum_e/(2*math.pi) # scale sum_e to rev/sec units
    # select control either with rad/sec or rps (rps is used in Arduino)
    # going with rps is meant to see if I can get gains to match with
    # the experimental setup
    u = Kp*e_omegac + Ki*sum_e - Kd*(omegac - omegac_p) # PWM based on rad/sec
    u = Kp*e_rpsc + Ki*sum_erps - Kd*(rpsc - omegac_p/(2*math.pi)) # PWM based on rev/sec

    mcc = u/255 + uff # normalize u; uff already normalized
    vinc = mcc*vb # watch for saturation
    if np.abs(vinc)>vb:
        vinc = np.sign(vinc)*vb


    # integrate over dt with control inputs
    to = tc
    tend = to + dt
    x0 = np.array([omegac, thetac]) # initial condition
    N = 100
    ts = np.linspace(to, tend, N) # time array over dt
    sol = rk.rk4fixed(pmdc, x0, ts, args=(rm, Rm, Bm, Jm, Tmo, vinc))
    # compute outputs
    N = len(ts)
    omegac_p = omegac # store the omega in last step as previous value
    omegac = sol[N-1,0] # rad/sec
    thetac = sol[N-1,1] # deg of output
    tc = ts[N-1]
    omega.append(omegac)
    theta.append(180*thetac/GR/math.pi)
    t.append(tc)
    _, y = pmdc(sol[N-1,:], ts[N-1], rm, Rm, Bm, Jm, Tmo, vinc)

    im.append(1000*y) 	# current in mA
    vin.append(vinc)		# input voltage
    e_omega.append(e_omegac)

    i = i+1

fig, (ax1, ax2, ax3) = plt.subplots(3)
#ax1.step(t, vin, where='post')
ax1.plot(t, vin, '.-', label='vin')
ax1.legend(loc="upper right")
ax1.set_ylabel('volts')
ax1.set_ylim([-2,5])
ax2.plot(t, omega, '.-', label='omega')
ax2.plot(t, omegar, '--', label='omega_r')
ax2.set_ylabel('rad/sec')
ax2.legend(loc="upper right")
ax2.set_ylim([-10,250])
ax3.plot(t, e_omega, '.-', label='e_omega')
ax3.set_ylabel('error rad/sec')
ax3.legend(loc="upper right")
ax3.set_ylim([-400,400])
ax3.set_xlabel('Time (sec)')
plt.tight_layout()
plt.show()


fig2 = plt.figure(2)
plt.plot(t,theta,'.-', label='theta')
plt.xlabel('Time (sec)')
plt.show()