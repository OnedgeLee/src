import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi, sin, cos, atan, degrees
from sympy import *
from matplotlib.ticker import MultipleLocator, AutoMinorLocator


DF = True

IS_SCATTER = False

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_res_1ch_bend_neo575.csv')

d  = 48.735  # in mm
lb = 17
lu = 13
l0 = 171.5 - (lb + lu) # in mm

x_tick_list = [0, 20, 40, 60]
y_tick_list = [135, 150, 165]

# Variables to store result
X  = list()
Y  = list()
Z  = list()
L1 = list()
L2 = list()
L3 = list()

p1 = [1000 * i for i in range(0, -37, -1)]
p2 = [0]
p3 = [0]

print(p1)
# A_avg = 545.575319 / 1000000
# A_avg = 530.93 / 1000000 # Force Equilibrium Area
A_avg = 494 / 1000000
# A_avg = 430 / 1000000

l1 = symbols('l1')
l2 = symbols('l2')
l3 = symbols('l3')

cdf_p2 = 0.0232/3
cdf_p1 = 1.0348/3
cdf_n2 = 0.0061/3
cdf_n1 = 0.9374/3

cfd_p2 = -0.0041
cfd_p1 = 0.729
cfd_n2 = -0.0247
cfd_n1 = 0.5549

cdp_p2 = -0.0105
cdp_p1 = 1.258

# Displacement vs Pressure
cdp_n2 = -0.0807
cdp_n1 = 1

cdp_n1_ = 0.325
cdp_n0_ = -61.975

# Chord length adjustment coeff.
'''
c_chord_1 = -0.459
c_chord_0 = -3.3349

c_chord_1_ = 0.1809
c_chord_0_ = 0
'''
c_chord_1 = -0.325
c_chord_0 = 0

c_chord_1_ = -0.325
c_chord_0_ = 0

'''
c_chord_2 = 0.0016
c_chord_1 = 0.0358
c_chord_0 = 0

c_chord_2_ = c_chord_2
c_chord_1_ = c_chord_1
c_chord_0_ = c_chord_0
'''
c_chord_const = 6

def calc_forward_kinematics(p1, p2, p3):
    f_l1 = p1 * A_avg * 3
    f_l2 = p2 * A_avg * 3
    f_l3 = p3 * A_avg * 3

    p_thr = -4000/1000
    p_thr2 = -24500/1000
    p1 = p1/1000
    p2 = p2/1000
    p3 = p3/1000
    if p1 > 0:
        dl1 = cdp_p2 * p1**2 + cdp_p1 * p1
        # dl1 = cfd_p2 * f_l1 ** 2 + cfd_p1 * f_l1
        # f1 = cp2 * l1 ** 2 + cp1 * l1 - f_l1
    elif p1 > p_thr2:
        dl1 = cdp_n2 * p1 ** 2 + cdp_n1 * p1
        # dl1 = cfd_n2 * f_l1 ** 2 + cfd_n1 * f_l1
        # f1= cn2 * l1 ** 2 + cn1 * l1 - f_l1
    else :
        dl1 = cdp_n1_ * p1 + cdp_n0_
    if p2 > 0:
        dl2 = cdp_p2 * p2 ** 2 + cdp_p1 * p2
        # dl2 = cfd_p2 * f_l2 ** 2 + cfd_p1 * f_l2
        # f2 = cp2 * l2 ** 2 + cp1 * l2 - f_l2
    elif p2 > p_thr2:
        dl2 = cdp_n2 * p2 ** 2 + cdp_n1 * p2
        # dl2 = cfd_n2 * f_l2 ** 2 + cfd_n1 * f_l2
        # f2 = cn2 * l2 ** 2 + cn1 * l2 - f_l2
    else :
        dl2 = cdp_n1_ * p2 + cdp_n0_
    if p3 > 0:
        dl3 = cdp_p2 * p3 ** 2 + cdp_p1 * p3
        # dl3 = cfd_p2 * f_l3 ** 2 + cfd_p1 * f_l3
        # f3 = cp2 * l3 ** 2 + cp1 * l3 - f_l3
    elif p3 > p_thr2 :
        dl3 = cdp_n2 * p3 ** 2 + cdp_n1 * p3
        # dl3 = cfd_n2 * f_l3 ** 2 + cfd_n1 * f_l3
        # f3 = cn2 * l3 ** 2 + cn1 * l3 - f_l3
    else :
        dl3 = cdp_n1_ * p3 + cdp_n0_

    if p1 >= p_thr :
        # dm1 = c_chord_2_ * p1 ** 2 + c_chord_1_ * p1 + c_chord_0_
        dm1 = c_chord_1_ * p1 + c_chord_0_
        # dm1 = 0
    elif p_thr2 <= p1 < p_thr:
        # dm1 = c_chord_2 * p1 ** 2 + c_chord_1 * pi + c_chord_0
        dm1 = c_chord_1 * p1 + c_chord_0
    else :
        dm1 = c_chord_const
    if p2 > p_thr :
        # dm2 = c_chord_2_ * p2 ** 2 + c_chord_1_ * p2 + c_chord_0_
        dm2 = c_chord_1_ * p2 + c_chord_0_
        # dm2 = 0
    elif p_thr2 <= p2 < p_thr:
        # dm2 = c_chord_2 * p2 ** 2 + c_chord_1 * p2 + c_chord_0
        dm2 = c_chord_1 * p2 + c_chord_0
    else:
        dm2 = c_chord_const
    if p3 > p_thr :
        dm3 = c_chord_1_ * p3 + c_chord_0_
        # dm3 = c_chord_2_ * p3 ** 2 + c_chord_1_ * p3 + c_chord_0_
        # dm3 = 0
        # dm2 = 0.0005 * p_thr2 ** 3 - 0.0022 * p_thr2 ** 2 + 0.0686 * p_thr2
    elif p_thr2 <= p3 < p_thr:
        # dm3 = c_chord_2 * p3 ** 2 + c_chord_1 * p3 + c_chord_0
        dm3 = c_chord_1 * p3 + c_chord_0
    else:
        dm3 = c_chord_const

    """
    f1_d = f1.diff(l1)
    f2_d = f2.diff(l2)
    f3_d = f3.diff(l3)

    l1n = 0
    l2n = 0
    l3n = 0

    for i in range(20):
        l1n = l1n - np.float32(f1.evalf(subs={l1: l1n})) / np.float32(f1_d.evalf(subs={l1: l1n}))
        # print(f'The {i+1} iteration ln is {l1n:.4} and f(xln) is {np.float(f1.evalf(subs= {l1:l1n})):.3}')
    for i in range(20):
        l2n = l2n - np.float32(f2.evalf(subs={l2: l2n})) / np.float32(f2_d.evalf(subs={l2: l2n}))
        # print(f'The {i+1} iteration ln is {l1n:.4} and f(xln) is {np.float(f1.evalf(subs= {l1:l1n})):.3}')
    for i in range(20):
        l3n = l3n - np.float32(f3.evalf(subs={l3: l3n})) / np.float32(f3_d.evalf(subs={l3: l3n}))
        # print(f'The {i+1} iteration ln is {l1n:.4} and f(xln) is {np.float(f1.evalf(subs= {l1:l1n})):.3}')
    """
    # d1 = (8.25 - d1)
    # d2 = (8.25 - d2)
    # d3 = (8.25 - d3)

    # print(dl1, dl2, dl3, d1, d2, d3)
    # print(dm1, dm2, dm3)
    # print(dl1, dm1)
    l1_res = dl1 + l0 + dm1  # + d1
    l2_res = dl2 + l0 + dm2  # + d2
    l3_res = dl3 + l0 + dm3  # + d3

    l1_wo_adj = dl1 + l0
    l2_wo_adj = dl2 + l0
    l3_wo_adj = dl3 + l0
    # print(l1_res, l2_res, l3_res)

    # l1_res = dl1 + l0
    # l2_res = dl2 + l0
    # l3_res = dl3 + l0

    # l1_ = dl1 + l0
    # l2_ = dl2 + l0
    # l3_ = dl3 + l0

    # print(dl1, dl2, dl3, d1, d2, d3, l1_res, l2_res, l3_res)

    l_q = 1/3 * (l1_res + l2_res + l3_res)
    l_q_wo_adj = 1/3 * (l1_wo_adj + l2_wo_adj + l3_wo_adj)
    # l_q = 1/3 * (l1_ + l2_ + l3_)
    if abs(l2_res - l3_res) < 0.001:
        # assume l2 = l3 then
        phi_q = 0
    else:
        phi_q = atan(sqrt(3) * (l2_res + l3_res - 2 * l1_res) / (3 * (l2_res - l3_res)))

    if abs(l2_wo_adj - l3_wo_adj) < 0.001 :
        phi_q_wo_adj = 0
    else :
        phi_q_wo_adj = atan(sqrt(3) * (l2_wo_adj + l3_wo_adj - 2 * l1_wo_adj) / (3 * (l2_wo_adj - l3_wo_adj)))

    kappa_q = 2 * sqrt(
        l1_res ** 2 + l2_res ** 2 + l3_res ** 2 - l1_res * l2_res - l1_res * l3_res - l2_res * l3_res) / (
                          d * (l1_res + l2_res + l3_res))
    kappa_q_wo_adj = 2 * sqrt(
        l1_wo_adj ** 2 + l2_wo_adj ** 2 + l3_wo_adj ** 2 - l1_wo_adj * l2_wo_adj - l1_wo_adj * l3_wo_adj - l2_wo_adj * l3_wo_adj) / (
                      d * (l1_wo_adj + l2_wo_adj + l3_wo_adj))

    theta_q = l_q * kappa_q
    theta_q_wo_adj = l_q_wo_adj * kappa_q_wo_adj

    if kappa_q < 0.000001 :
        c = 0
        x = 0
        y = 0
        z = 171.5
    else :
        c = 2 * (1 / kappa_q) * sin(theta_q / 2)
        x = c * sin(theta_q / 2) * cos(phi_q) + lu * sin(theta_q) * cos(phi_q)
        y = c * sin(theta_q / 2) * sin(phi_q) + lu * sin(theta_q) * sin(phi_q)
        z = c * cos(theta_q / 2) + lb + lu * cos(theta_q)

    if kappa_q_wo_adj < 0.000001 :
        c_wo_adj = 0
        x_wo_adj = 0
        y_wo_adj = 0
        z_wo_adj = 171.5
    else :
        c_wo_adj = 2 * (1 / kappa_q_wo_adj) * sin(theta_q_wo_adj / 2)
        x_wo_adj = c_wo_adj * sin(theta_q_wo_adj / 2) * cos(phi_q_wo_adj) + lu * sin(theta_q_wo_adj) * cos(phi_q_wo_adj)
        y_wo_adj = c_wo_adj * sin(theta_q_wo_adj / 2) * sin(phi_q_wo_adj) + lu * sin(theta_q_wo_adj) * sin(phi_q_wo_adj)
        z_wo_adj = c_wo_adj * cos(theta_q_wo_adj / 2) + lb + lu * cos(theta_q_wo_adj)

    print(degrees(theta_q), ",")
    return (x, y, z, l1_res, l2_res, l3_res, degrees(theta_q), degrees(theta_q_wo_adj))

X  = list()
Y  = list()
Z  = list()
L1 = list()
L2 = list()
L3 = list()
ang_list  = list()
ang_list_ = list()
for _p in p1 :
    res = calc_forward_kinematics(_p, 0, 0)
    if np.isnan(float(res[0])):
        X.append(0.0)
    else :
        X.append(res[0])
    if np.isnan(float(res[2])) :
        Z.append(1/3*(res[3]+res[4]+res[5]))
    else :
        Z.append(res[2])
    Y.append(res[1])
    L1.append(res[3])
    L2.append(res[4])
    L3.append(res[5])
    ang_list.append(res[6])
    ang_list_.append(res[7])

print(ang_list)
print(",")
print(ang_list_)
plt.rcParams["figure.autolayout"] = True

if IS_SCATTER :
    ax = df.plot.scatter(x='y0', y='z0', c='blue', s=12)
    ax.scatter(x=X, y=Z, c='black', s=12)
else :
    ax = df.plot.line(x='y0', y='z0', c='blue')
    ax.plot(X, Z, 'black')
# ax.scatter(x=X, y=Z, c='black', label='kinematic model')

ax.set_xticks(x_tick_list)
ax.set_yticks(y_tick_list)

ax.xaxis.set_minor_locator(plt.MultipleLocator(20/2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(15/3))

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=3, color='black')

ax.set_xlabel('x (mm)', fontsize=12)
ax.set_ylabel('z (mm)', fontsize=12)
ax.legend(['Simulation result', 'Kinematic model'], edgecolor='black', fontsize=12)
plt.show()

# print(X)