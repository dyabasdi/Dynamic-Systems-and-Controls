#
# PMDC motor model
# R.G. Longoria 8-4-20 v1
import math
import numpy as np
import matplotlib.pyplot as plt
import rk

# define the system ODEs
def pmdc(x, t, rm, Rm, Bm, Jm, To, vin):
    omegam, thetam = x[0], x[1]
    # input to this model in input voltage vin
    im = (vin - rm*omegam)/Rm
    omegamdot = (rm*im - Bm*omegam - To*np.tanh(omegam/60))/Jm
    thetamdot = omegam
	# specify outputs

    y = im

    return np.array([omegamdot, thetamdot]), y

# all parameter units in SI
rm = 0.0107		# motor constant, N*m/A
Rm = 30 		# motor armature resistance, ohms
Bm = 0.000178475e-3	# motor damping
Jm = 0.5*0.009*(0.25/39.37)**2	# motor inertia, kg*m^2, ignores gears
# print("Jm = " + str(Jm))
GR = 45			# gear ratio
Tmo = 1*0.1838e-3 # coulombic bearing torque in motor

# set up for simulation
t, vin, im, omega, theta, e_omega, omegar = [], [], [], [], [], [], []
sum_ev = [] # for discrete PID I control

vb = 5		# bus voltage
dt = 0.05
# control loop
i = 1 # tracking index
tc, vinc, imc, omegac, thetac, omegarc, e_omegac = 0, 0, 0, 0, 0, 0, 0 # initial conditions
# save all these initial values in lists
t.append(tc)
vin.append(vinc)
im.append(imc)
omega.append(omegac)
theta.append(thetac)
e_omega.append(e_omegac)
omegar.append(omegarc)

# This code simulates a simple experiment where you want to drive the motor in open-loop
# and let it run over a time interval so the output shaft turns by a desired amount.
# If the model relation works well, then the speed is achieved and so is the angular displacement.

# First, choose a speed. For the motor tested, it was found that the PWM level needed to be
# at least 145 or the motor would not 'un-stick'. At this PWM, an empirical PWM-speed correlation
# gives that the speed is 182 rad/sec or 29 rev/sec. Use this as the 'desired' speed. 
omega_d = 182 # desired speed in rad/sec
# (note: I chose the lowest speed value just to maximize the time interval for turning a given amount)
# Second, determine the *motor* angle interval to turn in this simulation.
theta_d = 180*GR # this is desired OUTPUT motor shaft angle times the GR to give motor shaft angle in degrees 
# Third, solve for the time interval to achived theta_d, 
# assuming you are turning at constant speed omega_d
tinterval = (theta_d*math.pi/180)/omega_d # this is an approximation; ignores rise time / fall time.
print(tinterval)

# Now set the simulation parameters. Turn on at ton, add tinterval to get toff
ton = 0.1
toff = ton + tinterval
tend = 3 # time in seconds to run the 'big loop', should be larger than toff

# the while loop below runs and takes time steps 'dt'
# choose dt to experiment with the time step you would take in the Arduino loop
# the loop first determines the PWM (here using mcc for PWM)
# In Arduino PWM for the H-bridge driver used ranges from -255 to 255
# here, we model this with mcc which ranges from -1 to 1 to modify bus voltage vb
# the key difference in this simulation from other simulations is that we don't
# just simulate over some time range. Rather, we simulate with RK4 fixed over each
# time interval, dt. So you need to keep updating the initial conditions. Then,
# we just keep the last point at the end of the small interval of dt.
# The values at the end of each dt are saved in a list using append (I like lists)
PWM = [0]
omega_r_list = [0]
omega_d_list = [0]
while tc < 2:
	# determine next step
    if (tc>ton) and (tc<toff):
        # look at slides to get explanation for this next line:
        omega_r = omega_d
        mcc = (Rm*(Tmo*math.tanh(omega_d)+Bm*omega_d)/rm + rm*omega_d)/vb
        PWM.append(255*mcc)
        omega_r_list.append(omega_r)
        omega_d_list.append(omega_d)
    else:
        mcc = 0
        omega_r = 0
        PWM.append(0)
        omega_r_list.append(omega_r)
        omega_d_list.append(omega_d)

    # Simple model of H-bridge voltage conversion
    omegar.append(omega_r) # store the reference value of omega for plotting
    vinc = mcc*vb # this is voltage input to armature of motor

    # now, run a simulation over dt with the vinc held constant
    # In a control loop, this is what you would do: you'd compute a command
    # then send it to the motor drive; it would then run over the 'loop time'
    # Here we run an RK4 simulation of the pmdc motor over that dt
    to = tc # set the initial time
    tend = to + dt # the final time is dt later
    x0 = np.array([omegac, thetac]) # set initial conditions for this interval
    N = 100 # choose how many steps over dt for RK4 simulation. Can adjust.
    ts = np.linspace(to, tend, N) # time array over dt
    # call the RK4
    sol = rk.rk4fixed(pmdc, x0, ts, args=(rm, Rm, Bm, Jm, Tmo, vinc))
    # now, we don't want all the results, just what is at the end of the dt
    N = len(ts)
    omegac = sol[N-1,0] # grab the value of omega at end of dt
    thetac = sol[N-1,1] # grab the value of theta at end of dt
    tc = ts[N-1] # grab the time value - we know this, of course
    # now start storing these away so we can plot them later
    omega.append(omegac) # store motor shaft speed, rad/sec
    theta.append(180*thetac/GR/math.pi) # store output shaft angle, deg
    t.append(tc) # store the time value
    e_omega.append(omega_r-omegac) # error in omega
    # grab any outputs; here the current and input voltage
    _, y = pmdc(sol[N-1,:], ts[N-1], rm, Rm, Bm, Jm, Tmo, vinc)

    im.append(1000*y) 	# store current at end of interval, mA
    vin.append(vinc)	# store input voltage, volts

    i = i+1

# end of big loop

# plot the stored results
fig1, (ax1, ax2, ax3, ax4) = plt.subplots(4)
ax1.plot(t, vin, '.-', label='vin')
ax1.legend(loc="upper right")
ax1.set_ylabel('volts')
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
ax4.plot(t, PWM, '.-', label='PWM')
ax4.set_ylabel('PWM')
ax4.legend(loc="upper right")
ax4.set_xlabel('Time (sec)')
plt.tight_layout()
plt.show()


fig2 = plt.figure(2)
plt.plot(t,theta,'.-', label='theta')
plt.xlabel('Time (sec)')
plt.show()

print("PWM:", PWM)
print("Omega R:", omegar)
print("Experimental Omega:", omega)