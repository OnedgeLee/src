"""
    Stress Stretch Curve Plot
    note : Tick Formatter (1000 -> 1,000)
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
from scipy.interpolate import make_interp_spline
import matplotlib

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_resin_property/stress_stretch.csv')

# df_new = df.rename(columns={'stress_60': '600 min. curing', 'stress_20': '20 min. curing'})

plt.rcParams["figure.autolayout"] = True
# ax1 = df.plot(kind='scatter', x='strain', y='stress_60', marker = '^', color='b', s = 3)
# ax2 = df.plot(kind='scatter', x='strain', y='stress_20', ax=ax1, color='r', s = 3)

ax = df.plot.line(x='stretch', y='stress', c='black')

# ax1 = df_new.plot.line(x='strain', y='600 min. curing', c='black')
# ax2 = df_new.plot.line(x='strain', y='20 min. curing', ax=ax1, ls='--', c='black')
ax.get_legend().remove()
ax.legend(edgecolor='black')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

# Add comma to Tick
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# ax.set_xlabel('Stretch \u03B5', fontsize=12)
ax.set_xlabel('Stretch \u03BB', fontsize=12)
ax.set_ylabel('Stress \u03C3 (kPa)', fontsize=12)

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

mu  = 575
mu2 = 575

X = np.linspace(1, 4, 301)
Y  = list()
Y2 = list()
for _x in X :
    _y = mu * (_x - _x**(-2))
    _y2 = mu2 * (_x - _x**(-2))
    Y2.append(_y2)
    Y.append(_y)
x_tick = [1, 2, 3, 4]
y_tick = [0, 500, 1000, 1500, 2000, 2500]
ax.set_xticks(x_tick)
ax.set_yticks(y_tick)

ax.plot(X, Y, c='black', linestyle='--')
# ax.plot(X, Y2, c='red')
ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax.xaxis.set_minor_locator(plt.MultipleLocator(1 / 3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(500 / 3))
ax.legend(['Experiment', 'Neohookian'], edgecolor='black', fontsize=12)
# ax.get_legend().remove()

plt.show()
"""
X1 = list()
X2 = list()
Y1 = list()
Y2 = list()
for val in df.values :
    _x = val[0]
    if not np.isnan(val[1]) :
        X1.append(_x)
        _y1 = val[1]
    if not np.isnan(val[2]) :
        X2.append(_x)
        _y2 = val[2]
    Y1.append(_y1)
    Y2.append(_y2)

X1 = np.array(X1)
X2 = np.array(X2)
Y1 = np.array(Y1)
Y2 = np.array(Y2)

xs=np.linspace(0,0.8,500)

model1 = make_interp_spline(X1, Y1)
model2 = make_interp_spline(X2, Y2)

y1 = model1(xs)
y2 = model2(xs)

plt.scatter(X1, y1)
"""