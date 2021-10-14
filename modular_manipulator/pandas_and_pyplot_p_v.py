#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

ALL  = True
POS  = False
TYPE = 1
if not ALL :
    if POS :
        df = pd.read_csv('/Users/user/Downloads/pv.csv')
    else :
        df = pd.read_csv('/Users/user/Downloads/np.csv')
else :
    df = pd.read_csv('/Users/user/Downloads/np_p_v.csv')
# df_new = df.rename(columns={'Voltage': 'Voltage (V)', 'Pressure': 'Pressure (MPa)'})
# print(df_new)

plt.rcParams["figure.autolayout"] = True
# df.set_index('Voltage').plot()
ax = df.plot(kind='scatter', x='Voltage', y='Pressure')
ax.set_xlabel('Voltage (V)')
ax.set_ylabel('Pressure (MPa)')

if not ALL :
    if not POS :
        """ Negative Gauge Pressure """
        x_tick_list = [3.4, 3.5, 3.6]
        y_tick_list = [-0.04, -0.02, 0]
        """ Positive Gauge Pressure """
    else :
        x_tick_list = [3.4, 3.9, 4.4, 4.9]
        y_tick_list = [0.00, 0.02, 0.04, 0.06]
else :
    x_tick_list = [3.4, 3.9, 4.4, 4.9]
    y_tick_list = [-0.04, -0.02, 0.00, 0.02, 0.04, 0.06]

# ax.set_xticks(x_tick_list, minor=True)
# ax.set_yticks(y_tick_list, minor=True)
ax.set_xticks(x_tick_list)
ax.set_yticks(y_tick_list)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
# ax.minorticks_on()

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=3, color='black')

cnt = 0
voltage  = 0
pressure = 0
v = list()
p = list()
X = list()
Y = list()
mean_list = []
for val in df.values :
    voltage = val[0]
    pressure += val[1]
    cnt += 1
    X.append(voltage)
    Y.append(val[1])
    # print(cnt)
    if cnt == 20 :
        pressure = pressure / cnt
        
        X = np.array(X)
        Y = np.array(Y)
        e = np.std(Y)
        err = plt.errorbar(x=voltage, y=pressure, yerr=e, linestyle='None', ecolor='black', mfc='black', mec='black', capsize=4, capthick=1)
        # err = plt.errorbar(x=voltage, y=pressure, yerr=e, fmt="none")
        X = list()
        Y = list()
        v.append(voltage)
        p.append(pressure)
        # mean_list.append([voltage, pressure])
        pressure = 0
        cnt = 0

""" legend frame color handle """

"""
legend = ax.legend(frameon=1)
frame  = legend.get_frame()
frame.set_edgecolor('black')
"""
v = np.array(v)
p = np.array(p)
ax.scatter(v, p, c='red')
if TYPE == 2 :
    ax.legend(['measured', 'mean', 'std'], edgecolor='black')
else :
    ax.legend(['measured', 'mean'], edgecolor='black')
# ax.yaxis.set_minor_locator(tck.AutoMinorLocator())

plt.show()