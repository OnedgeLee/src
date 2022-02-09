"""
    Module Internal Pressure Response Simulation Result Plot
    - Module' total Stiffness
    - Module' total Compliance
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter


A_ALL = False
MODE_LIST = ["F_COMPLIANCE", "F_STIFFNESS", "P_DISP", "DISP_P"]
MODE = MODE_LIST[3]
df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_res_lin_neo575.csv')
df2 = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/p_res_neo700/exp_p_res_lin_mod.csv')

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
if MODE == "F_COMPLIANCE":
    x_tick = [-30, -15, 0, 15, 30, 45, 60]
    y_tick = [-60, -45, -30, -15, 0, 15, 30]

    if A_ALL :
        pass
    else :
        ax = df.plot.line(x='f_3_t', y='z_t_d', c='black')
        # ax1 = df2.plot.line(x='f_mean', y='d_mean_k', c='red', ax=ax)
        # x_tick = [-75, -60, -45, -30, -15, 0]
        # y_tick = [105, 125, 145, 165]
    ax.get_legend().remove()

    plt.axvline(0, 0, 1, c='darkgray')
    plt.axhline(0, 0, 1, c='darkgray')

    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=3, color='black')

    ax.set_xlim([-44, 63])
    ax.set_ylim([-74, 37])

    ax.set_xticks(x_tick)
    ax.set_yticks(y_tick)
    ax.xaxis.set_minor_locator(plt.MultipleLocator(15 / 2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(15 / 2))
    ax.set_xlabel('Force (N)', fontsize=12)
    # ax.set_ylabel('Displacement (mm)', fontsize=12)  # \u03BB
    ax.set_ylabel('Displacement (mm)', fontsize=12)  # \u03BB

elif MODE == "F_STIFFNESS" :
    y_tick = [-30, -15, 0, 15, 30, 45, 60]
    x_tick = [-60, -45, -30, -15, 0, 15, 30]

    if A_ALL :
        ax = df.plot.line(x='z_t_d', y='f_3_a1_t', c='black')
        ax2 = df.plot.line(x='z_t_d', y='f_3_a2_t', c='blue', ax=ax)
        ax3 = df.plot.line(x='z_t_d', y='f_3_a3_t', c='red', ax=ax)
    else :
        ax = df.plot.line(x='z_t_d', y='f_3_t', c='black')
    ax.get_legend().remove()

    plt.axvline(0, 0, 1, c='darkgray')
    plt.axhline(0, 0, 1, c='darkgray')

    ax.set_ylim([-44, 63])
    ax.set_xlim([-74, 37])

    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=3, color='black')

    ax.set_xticks(x_tick)
    ax.set_yticks(y_tick)
    ax.xaxis.set_minor_locator(plt.MultipleLocator(15/2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(15/2))
    ax.set_ylabel('Force (N)', fontsize=12)
    ax.set_xlabel('Displacement (mm)', fontsize=12)  # \u03BB

    if A_ALL :
        ax.legend(['Area 1', 'Area 2', 'Area 3'], edgecolor='black', fontsize=12)
elif MODE == "P_DISP" :
    ax = df.plot.line(x='p_kpa_t', y='z_t_d', c='black')

    y_tick = [-60, -45, -30, -15, 0, 15, 30]
    x_tick = [-20, -10, 0, 10, 20, 30, 40]

    ax.set_xticks(x_tick)
    ax.set_yticks(y_tick)

    ax.set_xlim([-28, 44])
    ax.set_ylim([-74, 37.3])

    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=3, color='black')

    plt.axvline(0, 0, 1, c='darkgray')
    plt.axhline(0, 0, 1, c='darkgray')

    ax.set_xlabel('Pressure (kPa)', fontsize=12)
    ax.set_ylabel('Displacement (mm)', fontsize=12)  # \u03BB
    ax.xaxis.set_minor_locator(plt.MultipleLocator(10/2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(15/2))
    ax.get_legend().remove()
else :
    ax = df.plot.line(y='p_kpa_t', x='z_t_d', c='black')

    x_tick = [-60, -45, -30, -15, 0, 15, 30]
    y_tick = [-20, -10, 0, 10, 20, 30, 40]

    ax.set_xticks(x_tick)
    ax.set_yticks(y_tick)

    ax.set_ylim([-28, 44])
    ax.set_xlim([-74, 37.3])

    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=3, color='black')

    plt.axvline(0, 0, 1, c='darkgray')
    plt.axhline(0, 0, 1, c='darkgray')

    ax.set_ylabel('Pressure (kPa)', fontsize=12)
    ax.set_xlabel('Displacement (mm)', fontsize=12)  # \u03BB
    ax.yaxis.set_minor_locator(plt.MultipleLocator(10/2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(15/2))
    ax.get_legend().remove()


plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.show()