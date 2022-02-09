"""
    Module Internal Pressure Response Simulation Result Plot
    - Module' total Stiffness
    - Module' total Compliance
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter

plt.rcParams["figure.autolayout"] = True
x_tick = [-60, -45, -30, -15, 0, 15, 30]
y_tick = [0, 1]

fig = plt.figure()
ax  = fig.add_subplot(111)

plt.axvline(0, 0, 1, c='darkgray')
plt.axvline(-69, 0.02, 0.93, c='black', linestyle='--')

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

ax.set_ylim([0, 1.6])
ax.set_xlim([-74, 37])

ax.set_xticks(x_tick)
ax.set_yticks(y_tick)
ax.xaxis.set_minor_locator(plt.MultipleLocator(15 / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(1 / 3))
ax.set_ylabel('Stiffness (N/mm)', fontsize=12)
# ax.set_ylabel('Displacement (mm)', fontsize=12)  # \u03BB
ax.set_xlabel('Displacement (mm)', fontsize=12)  # \u03BB

Xp  = np.linspace(0, 34, 35)
Xn1 = np.linspace(-69, 0, 70)
Xn2 = np.linspace(-73, -69, 15)

Yp  = list()
Yn1 = list()
Yn2 = list()
for x in Xp :
    y = 0.0076*2*x + 0.3192
    Yp.append(y)
for x in Xn1 :
    y = 0.0019*2*x + 0.2923
    Yn1.append(y)
for x in Xn2 :
    y = 1.4935
    Yn2.append(y)

ax.plot(Xp, Yp, c='black')
ax.plot(Xn1, Yn1, c='red')
ax.plot(Xn2, Yn2, c='blue')


plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.show()