#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

df = pd.read_csv('/Users/user/Downloads/max_bend.csv')

print(df)
X1 = [-58.87, -27.35, 30.57, 57.72, 30.57, -27.35, -58.87]
Y1 = [1.31, 50.86, 50.33, -1.74, -50.33, -50.86, 1.31]

X2 = [-45.66, -10.26, 23.23, 20.94, 23.23, -10.26, -45.66]
Y2 = [0.46, 18.25, 39.32, -0.67, -39.32, -18.25, 0.46]
fig = plt.figure()
# ax  = fig.add_subplot(111, projection='3d')
ax  = fig.add_subplot(111)
ax.set_aspect('equal')
ax.set_ylim(-65, 65)
ax.set_xlim(-65, 65)

ax.set_xlabel('degree ($^\circ$)', fontsize=18)
ax.set_ylabel('degree ($^\circ$)', fontsize=18)

x_tick = [-60, -30, 0, 30, 60]
y_tick = [-60, -30, 0, 30, 60]

ax.set_yticks(y_tick)
ax.set_xticks(x_tick)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=3, color='black')

ax.plot(X1, Y1, c='black')
ax.plot(X2, Y2, c='darkgray')
ax.legend(['Both pressure sources', 'Single pressure source'], edgecolor='black', fontsize=14)
plt.show()