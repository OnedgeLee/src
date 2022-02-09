"""
    Chord Length Difference Calculation
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter


A_ALL = False
MODE_LIST = ["F_COMPLIANCE", "F_STIFFNESS", "P_DISP", "DISP_P"]
MODE = MODE_LIST[1]
df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_bend_chord_length_neo575.csv')

cm = 1/2.54

plt.rcParams["figure.autolayout"] = True
# ax1 = df.plot(kind='scatter', x='strain', y='stress_60', marker = '^', color='b', s = 3)
# ax2 = df.plot(kind='scatter', x='strain', y='stress_20', ax=ax1, color='r', s = 3)
"""
# ax = df.plot.line(x='pressure', y='displacement', c='black', figsize=(7.2*cm, 5.4*cm))
# ax = df.plot.line(x='strain', y='20 min. curing', ax=ax1, ls='--', c='black')
# ax = df.plot.line(x='pressure', y='displacement', c='black')
ax = df.plot.line(x='z_t', y='f3_3_t', c='black')
ax2 = df.plot.line(x='z_p', y='f3_3_p', c='blue', ax=ax)
ax3 = df.plot.line(x='z_n', y='f3_3_n', c='red', ax=ax)
ax.get_legend().remove()
# ax.xaxis.set_minor_locator(AutoMinorLocator())
# ax.yaxis.set_minor_locator(AutoMinorLocator())

plt.axvline(0, 0, 1, c='darkgray')
plt.axhline(0, 0, 1, c='darkgray')
# Add comma to Tick
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# ax.set_xlabel('Stretch \u03B5')


ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')
"""
x_tick = [-25, -20, -15, -10, -5, 0]
y_tick = [0, 2, 4, 6, 8]

slope = -0.325
X = np.linspace(-24, 0, 25)
Y = list()
for _x in X :
    _y = slope * _x
    Y.append(_y)

ax  = df.plot.scatter(x='p_t_kpa', y='delta_t_l', c='black')
ax.plot(X, Y, c='black', linestyle='--')
ax.set_xlim([-26, 2])
ax.set_ylim([-0.9, 8.5])
# ax1 = df2.plot.line(x='f_mean', y='d_mean_k', c='red', ax=ax)
# x_tick = [-75, -60, -45, -30, -15, 0]
# y_tick = [105, 125, 145, 165]
# ax.get_legend().remove()

# plt.axvline(0, 0, 1, c='darkgray')
# plt.axhline(0, 0, 1, c='darkgray')

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

ax.set_xticks(x_tick)
ax.set_yticks(y_tick)
ax.xaxis.set_minor_locator(plt.MultipleLocator(5 / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(2 / 2))
ax.set_xlabel('Pressure (kPa)', fontsize=12)
# ax.set_ylabel('Displacement (mm)', fontsize=12)  # \u03BB
ax.set_ylabel('Displacement (mm)', fontsize=12)  # \u03BB

# ax.legend(['Area 1', 'Area 2', 'Area 3'], edgecolor='black', fontsize=12)

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

ax.legend(['Estimated line', 'Model-simulation difference'], edgecolor='black', fontsize=12)

plt.show()