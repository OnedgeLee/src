#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
from scipy.interpolate import make_interp_spline


df = pd.read_csv('/Users/user/Downloads/srm_data_plot/ss/stress_stretch.csv')

plt.rcParams["figure.autolayout"] = True
# ax1 = df.plot(kind='scatter', x='strain', y='stress_60', marker = '^', color='b', s = 3)
# ax2 = df.plot(kind='scatter', x='strain', y='stress_20', ax=ax1, color='r', s = 3)

ax = df.plot.line(x='stretch', y='stress', c='black')
# ax = df.plot.line(x='strain', y='20 min. curing', ax=ax1, ls='--', c='black')
ax.get_legend().remove()
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

# Add comma to Tick
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# ax.set_xlabel('Stretch \u03B5')
ax.set_xlabel('Stretch \u03BB', fontsize=16)
ax.set_ylabel('Stress \u03C3 (MPa)', fontsize=16)

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

x_tick = [1.0, 2.0, 3.0, 4.0]
ax.set_xticks(x_tick)
y_tick = [0.0, 0.8, 1.6, 2.4]
ax.set_yticks(y_tick)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


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
ax.legend(['Test Result', 'Fitted Curve'], edgecolor='black', fontsize=14)

eq = r'$\sigma = 2\cdot(1- \lambda^{-3})\cdot(C_{01}\cdot\lambda+C_{10})$'
plt.text(2.1, 0.3, eq, fontsize=15)
