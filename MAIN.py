import numpy as np; import runge_kutta as r_k
import matplotlib.pyplot as plt; import pulse_ode as po
import integrated_ode as so; import datetime
import stenosis
from scipy.integrate import solve_ivp


def cal(HR, PF):
    try:
        nn = datetime.datetime.now()
        branch_list = open('branch_list.txt', 'r')
        b = branch_list.readlines()
        rlcnewval = np.genfromtxt('RLCtru.csv', delimiter=",")
        eqn_no = np.genfromtxt('eqn_no.txt', delimiter='')
        #print(rlcnewval)

        print("pass")
        Rs = rlcnewval[:, 0]
        L = rlcnewval[:, 1]
        C = rlcnewval[:, 2]
        Rp = rlcnewval[:, 3]

        #f = open("RLCtru.csv", "w")
        #f.truncate()
        #f.close()

        HR = int(HR)
        PF = int(PF)
        print(HR)
        print(PF)
        dt = 0.002
        clock = np.arange(0.0, 10.0, dt)

        T = 60 / HR
        t1 = clock / T
        t2 = t1 - np.floor(t1)
        t3 = np.multiply(T, t2)
        x1 = PF * (np.square(np.sin(3.14 * t3 / (0.3))))
        x2 = np.floor(t3 + 0.7)
        it = np.multiply((1 - x2), x1)
        print("all crct")
        R1 = 0.11
        L = 0.011
        R2 = 1.11
        C = 0.91

        # GENERATION OF PULSE
        # initial value
        pulse_initial = np.zeros(2)
        print('pulse')
        pulse_generator = lambda t, x: po.pulsegen(t, x, R1, L, R2, C, clock, it)  # input for solver function
        t, x = r_k.rungekutta4(pulse_generator,pulse_initial,0.0,10,dt)
        #soln = solve_ivp(pulse_generator,[0, 10], pulse_initial,method='RK45')  # solving the ODEs
        #t = soln.t
        #x = soln.y
        pu = it.transpose()                                           # plotting the output
        pulse = (pu - x[0, :]) * R1 + x[1, :]
        print('pulse-gen')
        print(datetime.datetime.now() - nn)

        s = datetime.datetime.now()
        print('pass')
        system_initial = np.zeros(256)
        system_finder = lambda t, x: so.integrated_ode(t, x, pulse, clock)
        print('pass-2', system_finder)
        sol = solve_ivp(system_finder,[0, 10],system_initial,method='Radau',t_eval=np.linspace(0,10,1000))
        t = sol.t
        x = sol.y
        #t, x = r_k.rungekutta4(system_finder, system_initial, 0.0, 10.0, dt)
        print('ode-solver')
        print(datetime.datetime.now() - s)

        return (t, x)
    except:
        return (-1,-10000)


if __name__ == "__main__":
    c,p = cal(70,350)