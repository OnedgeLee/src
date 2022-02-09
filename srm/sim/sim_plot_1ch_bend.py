"""
    Module' 1 Chamber Internal Negative Gauge Pressure
    Response Simulation Result Plot (Bending)
"""

import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import numpy as np
import pandas as pd
from math import degrees
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_res_1ch_bend_neo610.csv')
x0 = list(df.loc[:, 'x0'].values)
x1 = list(df.loc[:, 'x1'].values)
x2 = list(df.loc[:, 'x2'].values)
x3 = list(df.loc[:, 'x3'].values)

y0 = list(df.loc[:, 'y0'].values)
y1 = list(df.loc[:, 'y1'].values)
y2 = list(df.loc[:, 'y2'].values)
y3 = list(df.loc[:, 'y3'].values)

z0 = list(df.loc[:, 'z0'].values)
z1 = list(df.loc[:, 'z1'].values)
z2 = list(df.loc[:, 'z2'].values)
z3 = list(df.loc[:, 'z3'].values)


# equation_plane(x1[0], y1[0], z1[0], x3[0], y3[0], z3[0], x4[0], y4[0], z4[0])
# equation_plane(x1[3], y1[3], z1[3], x3[3], y3[3], z3[3], x4[3], y4[3], z4[3])

from sympy import Plane, Point3D, Line3D

p = Plane(Point3D(x2[0], y2[0], z2[0]), Point3D(x1[0], y1[0], z1[0]), Point3D(x3[0], y3[0], z3[0]))
# p = Plane(Point3D(x2[5], y2[5], z2[5]), Point3D(x1[5], y1[5], z1[5]), Point3D(x3[5], y3[5], z3[5]))
L = Line3D(Point3D(0, 0, 0), Point3D(0, 0, 1))
theta_angle = list()
bend_angle  = list()
for i in range(len(x1)):
    p = Plane(Point3D(x2[i], y2[i], z2[i]), Point3D(x1[i], y1[i], z1[i]), Point3D(x3[i], y3[i], z3[i]))
    _angle  = abs(degrees(p.angle_between(L)))
    d_angle = 90 - _angle
    bend_angle.append(d_angle)
    theta_angle.append(_angle)
    # print(_angle, d_angle)

X = np.linspace(-30, 0, 31)
# print(angle)
# print(angle2)

fig = plt.figure()
ax  = fig.add_subplot(111)
ax.minorticks_on()
x_tick_list = [0, 5, 10, 15, 20]
x_tick_list = [-30, -20, -10, 0]
y_tick_list = [0, 10, 20, 30, 40, 50]

ax.set_yticks(y_tick_list)
ax.set_xticks(x_tick_list)

plt.setp(ax.get_yticklabels(), fontsize=10)
plt.setp(ax.get_xticklabels(), fontsize=10)

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=3, color='black')

ax.set_xlabel('Pressure (kPa)', fontsize=12)
ax.set_ylabel('Bending angle ($^\circ$)', fontsize=12)

ax.xaxis.set_minor_locator(plt.MultipleLocator(10/3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(10/3))

ax.plot(X, list(reversed(bend_angle)), c='black')
"""
ax.plot(v_list, ang_list, c='blue')
ax.plot(v, list(reversed(angle_list)), c='red')
err = plt.errorbar(x=v, y=list(reversed(angle_list)), yerr=stddev_list, linestyle='None', ecolor='black', mfc='black', mec='black',
                            capsize=4, capthick=1)

axins = inset_axes(ax, width=1.2, height=1.4, loc=5)

axins.scatter(-10, angle_list[6], c='red')
err = plt.errorbar(x=-10, y=angle_list[6], yerr=stddev_list[6], linestyle='None', ecolor='black', mfc='black', mec='black',
                            capsize=4, capthick=1)
# axins.axes.get_xaxis().set_visible(False)

# print(angle_list[6])
x_tick = [-10]
y_tick = [22.44, 22.48]

# axins.set_xticklabels(x_tick, fontsize=18)
# axins.set_yticklabels(y_tick, fontsize=18)
axins.set_yticks(y_tick)
axins.set_xticks(x_tick)
"""
# ax.plot(X, list(reversed(angle2)), c='gray')
# ax.legend(['Both pressure sources', 'Single pressure source'], frameon=False, fontsize=18)
# ax.legend(['Simulation', 'Kinematic model', 'Experiment'], edgecolor='black', fontsize=12)
print(bend_angle)
print(theta_angle)
plt.show()