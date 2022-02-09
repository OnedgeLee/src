"""
    Module' Bending Response Plot
    - 1 Chamber Negative Gauge Pressure Response
    - 1 Chamber Negative + 2 Chamber Positive Gauge Pressure Response
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

X1 = [-58.87, -27.35, 30.57, 57.72, 30.57, -27.35, -58.87]
Y1 = [1.31, 50.86, 50.33, -1.74, -50.33, -50.86, 1.31]

X2 = [-45.66, -24.38, 23.23, 46.03, 23.23, -24.38, -45.66]
Y2 = [0.46, 40.01, 39.32, -0.67, -39.32, -40.01, 0.46]

fig = plt.figure()
# ax  = fig.add_subplot(111, projection='3d')
ax  = fig.add_subplot(111)
ax.set_aspect('equal')
ax.set_ylim(-80, 80)
ax.set_xlim(-80, 80)

ax.set_xlabel('degree ($^\circ$)', fontsize=24)
ax.set_ylabel('degree ($^\circ$)', fontsize=24)

x_tick = [-60, -30, 0, 30, 60]
y_tick = [-60, -30, 0, 30, 60]

ax.set_yticks(y_tick)
ax.set_xticks(x_tick)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=10)
ax.tick_params(which='minor', length=5, color='black')

ax.plot(X1, Y1, c='black')
ax.plot(X2, Y2, c='darkgray')
# ax.legend(['Both pressure sources', 'Single pressure source'], edgecolor='black', fontsize=18)
ax.legend(['Both pressure sources', 'Single pressure source'], frameon=False, fontsize=18)
plt.show()