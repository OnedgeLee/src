#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
from scipy.interpolate import make_interp_spline


df = pd.read_csv('/Users/user/Downloads/srm_fig/comsol_linear_sim_res/comsol_linear_sim_res.csv')

cm = 1/2.54

plt.rcParams["figure.autolayout"] = True
# ax1 = df.plot(kind='scatter', x='strain', y='stress_60', marker = '^', color='b', s = 3)
# ax2 = df.plot(kind='scatter', x='strain', y='stress_20', ax=ax1, color='r', s = 3)

# ax = df.plot.line(x='pressure', y='displacement', c='black', figsize=(7.2*cm, 5.4*cm))
# ax = df.plot.line(x='strain', y='20 min. curing', ax=ax1, ls='--', c='black')
ax = df.plot.line(x='pressure', y='displacement', c='black')
ax.get_legend().remove()
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

plt.axvline(0, 0, 1, c='darkgray')
# Add comma to Tick
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# ax.set_xlabel('Stretch \u03B5')
ax.set_xlabel('Pressure (kPa)', fontsize=12)
ax.set_ylabel('Displacement (mm)', fontsize=12) # \u03BB

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

x_tick = [-40, -20, 0, 20, 40, 60]
ax.set_xticks(x_tick)
y_tick = [-50, -25, 0, 25]
ax.set_yticks(y_tick)

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

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