#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

ALL  = False
POS  = False
TYPE = 1
csv_dir = '/Users/user/Downloads/srm_data_plot/np_p_volt/'
if not ALL :
    if POS :
        df = pd.read_csv(csv_dir + 'pv.csv')
    else :
        df = pd.read_csv(csv_dir + 'np.csv')
else :
    df = pd.read_csv(csv_dir + 'np_p_v.csv')
# df_new = df.rename(columns={'Voltage': 'Voltage (V)', 'Pressure': 'Pressure (MPa)'})
# print(df_new)

plt.rcParams["figure.autolayout"] = True
# df.set_index('Voltage').plot()
ax = df.plot(kind='scatter', x='Voltage', y='Pressure')
ax.set_xlabel('Voltage (V)', fontsize=12)
ax.set_ylabel('Pressure (MPa)', fontsize=12)

if not ALL :
    if not POS :
        """ Negative Gauge Pressure """
        x_tick_list = [0.05, 0.15, 0.25]
        y_tick_list = [-0.04, -0.02, 0]
        """ Positive Gauge Pressure """
    else :
        x_tick_list = [0.4, 0.8, 1.2, 1.6]
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
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

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
        print(pressure)
        
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

if POS :
    a4 = 0.0423
    a3 = -0.1335
    a2 = 0.0951
    a1 = 0.0548
    a0 = 0
else :
    a4 = -28.748
    a3 = 18.345
    a2 = -4.2732
    a1 = 0.5673
    a0 = -0.0509

if POS :
    X = np.linspace(0.0, 1.7, 171)
else :
    X = np.linspace(0.0, 0.28, 141)
Y = list()
for _x in X :
    y = a4*_x**4 + a3*_x**3 + a2*_x**2 + a1*_x + a0
    Y.append(y)

# ax.legend(edgecolor='black')
# ax.legend(['Test Result', 'Fitted Curve'], edgecolor='black', fontsize=12)

# eq = r'$\sigma = 2\cdot(1- \lambda^{-3})\cdot(C_{01}\cdot\lambda+C_{10})$'
if POS :
    eq = r'$p(v)= a_{p4}\cdot v^{4} + a_{p3}\cdot v^{3} + a_{p2}\cdot v^{2} + a_{p1}\cdot v + a_{p0}$'
    ax.text(0.5, 0.01, eq, fontsize=11)
else :
    eq = r'$p(v)= a_{n4}\cdot v^{4} + a_{n3}\cdot v^{3} + a_{n2}\cdot v^{2} + a_{n1}\cdot v + a_{n0}$'
    ax.text(0.08, -0.04, eq, fontsize=11)
    # ax.text(0.5, 0.01, eq, fontsize=11)


""" legend frame color handle """

"""
legend = ax.legend(frameon=1)
frame  = legend.get_frame()
frame.set_edgecolor('black')
"""
v = np.array(v)
p = np.array(p)
ax.scatter(v, p, c='red')
ax.plot(X, Y, c='darkgray')
if TYPE == 2 :
    ax.legend(['measured', 'mean', 'std'], edgecolor='black')
else :
    ax.legend(['Fitted curve', 'mean', 'Measured'], edgecolor='black', fontsize=10)
# ax.yaxis.set_minor_locator(tck.AutoMinorLocator())

plt.show()