"""
    One Layer Internal Pressure Response Simulation Result Plot
    - One layer' Stiffness
    - One layer' Compliance
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
A_ALL = True

COMPLIANCE = 2
df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_one_layer/sim_1_layer_neo610.csv')

cm = 1/2.54

plt.rcParams["figure.autolayout"] = True
# ax1 = df.plot(kind='scatter', x='strain', y='stress_60', marker = '^', color='b', s = 3)
# ax2 = df.plot(kind='scatter', x='strain', y='stress_20', ax=ax1, color='r', s = 3)

# ax = df.plot.line(x='pressure', y='displacement', c='black', figsize=(7.2*cm, 5.4*cm))
# ax = df.plot.line(x='strain', y='20 min. curing', ax=ax1, ls='--', c='black')
# ax = df.plot.line(x='pressure', y='displacement', c='black')

# ax.xaxis.set_minor_locator(AutoMinorLocator())
# ax.yaxis.set_minor_locator(AutoMinorLocator())

# plt.axvline(0, 0, 1, c='darkgray')
# plt.axhline(0, 0, 1, c='darkgray')
# Add comma to Tick
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# ax.set_xlabel('Stretch \u03B5')

if COMPLIANCE == 1:
    if A_ALL :
        ax = df.plot.line(x='f_a1', y='z_t_d', c='black')
        ax2 = df.plot.line(x='f_a2', y='z_t_d', c='blue', ax=ax)
        ax3 = df.plot.line(x='f_a3', y='z_t_d', c='red', ax=ax)
        x_tick = [-15, -10, -5, 0, 5, 10, 15]
    else :
        ax = df.plot.line(x='f_a3', y='z_t_d', c='black')
        x_tick = [-12, -8, -4, 0, 4, 8, 12]
    # ax2 = df.plot.line(x='f1', y='z1', c='blue', ax=ax)
    # ax3 = df.plot.line(x='f2', y='z2', c='red', ax=ax)
    ax.get_legend().remove()
    y_tick = [-8, -4, 0, 4]

    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=3, color='black')

    ax.set_xticks(x_tick)
    ax.set_yticks(y_tick)
    if A_ALL :
        ax.xaxis.set_minor_locator(plt.MultipleLocator(5 / 2))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(4 / 2))
    else :
        ax.xaxis.set_minor_locator(plt.MultipleLocator(4 / 2))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(4 / 2))
    ax.set_xlabel('Force (N)', fontsize=12)
    ax.set_ylabel('Displacement (mm)', fontsize=12)  # \u03BB

    if A_ALL :
        ax.legend(['Area 1', 'Area 2', 'Area 3'], edgecolor='black', fontsize=12)
    plt.axvline(0, 0, 1, c='darkgray')
    plt.axhline(0, 0, 1, c='darkgray')

elif COMPLIANCE == 2 :
    if A_ALL :
        ax = df.plot.line(x='z_t_d', y='f_a1', c='black')
        ax2 = df.plot.line(x='z_t_d', y='f_a2', c='blue', ax=ax)
        ax3 = df.plot.line(x='z_t_d', y='f_a3', c='red', ax=ax)
        y_tick = [-15, -10, -5, 0, 5, 10, 15]
    else :
        ax = df.plot.line(x='z_t_d', y='f_a3', c='black')
        y_tick = [-12, -6, 0, 6, 12]
    # ax2 = df.plot.line(x='f1', y='z1', c='blue', ax=ax)
    # ax3 = df.plot.line(x='f2', y='z2', c='red', ax=ax)
    ax.get_legend().remove()
    x_tick = [-8, -4, 0, 4]

    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=3, color='black')

    ax.set_xticks(x_tick)
    ax.set_yticks(y_tick)
    if A_ALL :
        ax.xaxis.set_minor_locator(plt.MultipleLocator(4 / 2))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(5 / 2))
    else :
        ax.xaxis.set_minor_locator(plt.MultipleLocator(4 / 2))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(6 / 2))
    ax.set_ylabel('Force (N)', fontsize=12)
    ax.set_xlabel('Displacement (mm)', fontsize=12)  # \u03BB

    if A_ALL :
        ax.legend(['Area 1', 'Area 2', 'Area 3'], edgecolor='black', fontsize=12)
    plt.axvline(0, 0, 1, c='darkgray')
    plt.axhline(0, 0, 1, c='darkgray')

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.show()