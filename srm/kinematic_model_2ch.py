import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi, sin, cos, atan
from sympy import *
from matplotlib.ticker import MultipleLocator, AutoMinorLocator


IS_SCATTER = True

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_bend_2ch_res.csv')

d = 48.735  # in mm
l0 = 171.5  # in mm

x_tick_list = [-50, -25, 0]
y_tick_list = [120, 135, 150, 165]

# Variables to store result
X  = list()
Y  = list()
Z  = list()
L1 = list()
L2 = list()
L3 = list()

p1 = [0]
p2 = [1000 * i for i in range(0, -18, -1)]
p3 = [1000 * i for i in range(0, -18, -1)]

print(p2)
# A_avg = 545.575319 / 1000000
A_avg = 530.93 / 1000000

l1 = symbols('l1')
l2 = symbols('l2')
l3 = symbols('l3')

cp2 = 0.0173 / 3
cp1 = 0.7973 / 3
cn2 = 0.0048 / 3
cn1 = 0.7347 / 3


def calc_forward_kinematics(p1, p2, p3):
    f_l1 = p1 * A_avg
    f_l2 = p2 * A_avg
    f_l3 = p3 * A_avg

    """
    x = -68
    print(0.0048*x**2+0.7179*x, 171.5-68.7812)
    """

    if p1 > 0:
        f1 = cp2 * l1 ** 2 + cp1 * l1 - f_l1
    else:
        f1 = cn2 * l1 ** 2 + cn1 * l1 - f_l1

    if p2 > 0:
        f2 = cp2 * l2 ** 2 + cp1 * l2 - f_l2
    else:
        f2 = cn2 * l2 ** 2 + cn1 * l2 - f_l2

    if p3 > 0:
        f3 = cp2 * l3 ** 2 + cp1 * l3 - f_l3
    else:
        f3 = cn2 * l3 ** 2 + cn1 * l3 - f_l3

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

    l1_res = l1n + l0
    l2_res = l2n + l0
    l3_res = l3n + l0
    # print(l1_res, l2_res, l3_res)

    l_q = 1 / 3 * (l1_res + l2_res + l3_res)
    if abs(l2_res - l3_res) < 0.001:
        # assume l2 = l3 then
        phi_q = 0
    else:
        phi_q = atan(sqrt(3) * (l2_res + l3_res - 2 * l1_res) / (3 * (l2_res - l3_res)))

    kappa_q = 2 * sqrt(
        l1_res ** 2 + l2_res ** 2 + l3_res ** 2 - l1_res * l2_res - l1_res * l3_res - l2_res * l3_res) / (
                          d * (l1_res + l2_res + l3_res))
    theta_q = l_q * kappa_q

    c = 2 * (1 / kappa_q) * sin(theta_q / 2)
    x = c * sin(theta_q / 2) * cos(phi_q)
    y = c * sin(theta_q / 2) * sin(phi_q)
    z = c * cos(theta_q / 2)

    # print(np.float(f3.evalf(subs= {l1:l1n})))
    print(f'The last iteration l1n is {l1n:.4} and f(l1n) is {np.float32(f1.evalf(subs={l1: l1n})):.3}')
    print(f'The last iteration l1n is {l2n:.4} and f(l1n) is {np.float32(f2.evalf(subs={l2: l2n})):.3}')
    print(f'The last iteration l1n is {l3n:.4} and f(l1n) is {np.float32(f3.evalf(subs={l3: l3n})):.3}')
    # print(l1_res, l2_res, l3_res)
    # print(x, y, z)
    return (x, y, z, l1_res, l2_res, l3_res)

X  = list()
Y  = list()
Z  = list()
L1 = list()
L2 = list()
L3 = list()
for _p in p2 :
    res = calc_forward_kinematics(0, _p, _p)
    print(res)
    if np.isnan(float(res[0])):
        X.append(0.0)
    else :
        X.append(-res[0])
    if np.isnan(float(res[2])) :
        Z.append(1/3*(res[3]+res[4]+res[5]))
    else :
        Z.append(res[2])
    Y.append(res[1])
    L1.append(res[3])
    L2.append(res[4])
    L3.append(res[5])

plt.rcParams["figure.autolayout"] = True

if IS_SCATTER :
    ax = df.plot.scatter(x='x', y='z', c='blue', s=12)
    ax.scatter(x=X, y=Z, c='black', s=12)
else :
    ax = df.plot.line(x='x', y='z', c='blue')
    ax.plot(X, Z, 'black')
# ax.scatter(x=X, y=Z, c='black', label='kinematic model')

ax.set_xticks(x_tick_list)
ax.set_yticks(y_tick_list)

ax.xaxis.set_minor_locator(plt.MultipleLocator(25/3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(15/3))

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=3, color='black')

ax.set_xlabel('x (mm)', fontsize=12)
ax.set_ylabel('z (mm)', fontsize=12)
ax.legend(['Simulation result', 'Kinematic model'], edgecolor='black', fontsize=12)
plt.show()

# print(X)