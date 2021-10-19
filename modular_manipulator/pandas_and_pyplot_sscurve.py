#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
from scipy.interpolate import make_interp_spline

df = pd.read_csv('/Users/user/Downloads/srm_data_plot/ss/ss.csv')

df_new = df.rename(columns={'stress_60': '600 min. curing', 'stress_20': '20 min. curing'})

plt.rcParams["figure.autolayout"] = True
# ax1 = df.plot(kind='scatter', x='strain', y='stress_60', marker = '^', color='b', s = 3)
# ax2 = df.plot(kind='scatter', x='strain', y='stress_20', ax=ax1, color='r', s = 3)

ax1 = df_new.plot.line(x='strain', y='600 min. curing', c='black')
ax2 = df_new.plot.line(x='strain', y='20 min. curing', ax=ax1, ls='--', c='black')
# ax1.get_legend().remove()
ax1.legend(edgecolor='black')
ax1.xaxis.set_minor_locator(AutoMinorLocator())
ax1.yaxis.set_minor_locator(AutoMinorLocator())

# Add comma to Tick
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax1.set_xlabel('Strain \u03B5')
ax1.set_ylabel('Stress \u03C3 (kPa)')

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