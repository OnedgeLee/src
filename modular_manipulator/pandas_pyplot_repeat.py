#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

df = pd.read_csv('/Users/shetshield/Downloads/repeat_res.csv')

# df_new = df.rename(columns={'stress_60': '600 min. curing', 'stress_20': '20 min. curing'})

plt.rcParams["figure.autolayout"] = True
# ax1 = df.plot(kind='scatter', x='strain', y='stress_60', marker = '^', color='b', s = 3)
# ax2 = df.plot(kind='scatter', x='strain', y='stress_20', ax=ax1, color='r', s = 3)

ax = df.plot.line(x='cycle', y='height', c='grey')
axins = inset_axes(ax, width=2.4, height=1.8)

clc = list(df.loc[:,'cycle'].values)
h   = list(df.loc[:, 'height'].values)[:9]

axins.plot(np.arange(9), h, c='black')
axins.axes.get_xaxis().set_visible(False)

y_tick = [80, 120, 160]

axins.set_yticks(y_tick)

ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
# ax1 = df_new.plot.line(x='strain', y='600 min. curing', c='black')
# ax2 = df_new.plot.line(x='strain', y='20 min. curing', ax=ax1, ls='--', c='black')
# ax1.get_legend().remove()
ax.legend().remove()
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

ax.add_patch(plt.Rectangle((.42, .03), .01, 0.94, ls="--", ec="black", fc="None",
                           transform=ax.transAxes, zorder=3))

ax.set_xlabel('Cycle', fontsize=12)
ax.set_ylabel('Module height (mm)', fontsize=12)

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