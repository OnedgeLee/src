"""
    Module Force Response Simulation Result Plot
    - Module' total Stiffness
    - Module' total Compliance
"""

import numpy as np
import pandas as pd
from math import degrees
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

plt.rcParams["figure.autolayout"] = True
df  = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_force/sim_res_lin_force_neo575.csv')
df1 = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_res_lin_neo575.csv')


ax  = df.plot.line(x='z_d', y='f', c='black', label='Internal pressure')
ax1 = df1.plot.line(x='z_t_d', y='f_3_t', c='red', label='External force', ax=ax)
ax.get_legend().remove()
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

plt.axvline(0, 0, 1, c='darkgray')
plt.axhline(0, 0, 1, c='darkgray')

# Add comma to Tick
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# ax.set_xlabel('Stretch \u03B5')
ax.set_xlabel('Displacement (mm)', fontsize=12)
ax.set_ylabel('Force (N)', fontsize=12) # \u03BB

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

x_tick = [-60, -30, 0, 30]
ax.set_xticks(x_tick)
y_tick = [-30, 0,  30, 60]
ax.set_yticks(y_tick)

ax.set_xlim([-74, 43])
ax.set_ylim([-50, 65])

ax.xaxis.set_minor_locator(plt.MultipleLocator(30 / 3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(30 / 2))

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

cp2 = 0.0088
cp1 = 0.847

cn2 = 0.004
cn1 = 0.7948


"""
Xn = np.linspace(-72, 0, 73)
Xp = np.linspace(0, 32, 33)

Yn = list()
Yp = list()
for x in Xp :
    y = cp2 * x**2 + cp1 * x
    Yp.append(y)
for x in Xn :
    y = cn2 * x**2 + cn1 * x
    Yn.append(y)
ax.plot(Xn, Yn, c='black')
ax.plot(Xp, Yp, c='black')
"""
# ax.legend(['Fitted'], edgecolor='black', fontsize=12)
ax.legend(['External force', 'Internal pressure force'], edgecolor='black', fontsize=12)
plt.show()
"""
a = 0.3342
b = -0.1178
# eq = 2*(1-x**(-3))*(x*a+b)
X = np.linspace(1, 4, 301)
Y = list()
for _x in X :
    y = 2*(1-pow(_x, -3))*(_x*a+b)
    Y.append(y)
ax.plot(X, Y, c='blue')
# ax.legend(edgecolor='black')
ax.legend(['Test Result', 'Fitted Curve'], edgecolor='black', fontsize=12)
eq = r'$\sigma = 2\cdot(1- \lambda^{-3})\cdot(C_{01}\cdot\lambda+C_{10})$'
plt.text(1.8, 0.3, eq, fontsize=10)
"""