import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

POS = False
if POS:
    df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/p_v/p.csv')
    c64 = 2.8151
    c63 = -20.106
    c62 = 32.553
    c61 = 2.1583
    shift_6 = 3.4 # shift 3.4 V
    c24 = 1.7366
    c23 = -12.352
    c22 = 23.031
    c21 = 1.973
    shift_2 = 3.2 # start 3.2 V
    c114 = -4.1484
    c113 = 7.0742
    c112 = 2.8924
    c111 = 6.9909
    shift_11 = 3.3 # start at 3.3 V
else:
    df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/p_v/n_.csv')
    c64 = -57.947
    c63 = -33.997
    c62 = 87.346
    c61 = 27.258
    c60 = -32.5
    shift_6 = 3.35 # shift 3.35 V
    c24 = 77.486
    c23 = -291.77
    c22 = 205.23
    c21 = 9.3263
    c20 = -26.5
    shift_2 = 3.2 # start 3.2 V end 3.8
    c114 = 179.89
    c113 = -310.34
    c112 = 168.42
    c111 = 5.0462
    shift_11 = 3.25 # start at 3.25 (0)
    c110 = -23

# df_new = df.rename(columns={'Voltage': 'Voltage (V)', 'Pressure': 'Pressure (MPa)'})
print(df)

fig = plt.figure()
ax  = fig.add_subplot(111)

if POS :
    X = np.linspace(0.0, 1.8, 181)
    x_tick_list = [0.2, 0.7, 1.2, 1.7]
    y_tick_list = [2.5, 7.5, 12.5, 17.5, 22.5]
else :
    X = np.linspace(0.0, 0.7, 71)
    x_tick_list = [0.0, 0.35, 0.7]
    y_tick_list = [-30, -20, -10, 0]

Y1 = list()
Y2 = list()
Y3 = list()
X1 = list()
X2 = list()
X3 = list()
if POS :
    for _x in X :
        if _x < 1.601 :
            y1 = c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x
            y2 = c64 * _x ** 4 + c63 * _x ** 3 + c62 * _x ** 2 + c61 * _x
            y3 = c114 * _x ** 4 + c113 * _x ** 3 + c112 * _x ** 2 + c111 * _x
            X1.append(_x)
            X2.append(_x)
            X3.append(_x)
            Y1.append(y1)
            Y2.append(y2)
            Y3.append(y3)
        elif _x < 1.701 :
            y1 = c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x
            y3 = c114 * _x ** 4 + c113 * _x ** 3 + c112 * _x ** 2 + c111 * _x
            X1.append(_x)
            X3.append(_x)
            Y1.append(y1)
            Y3.append(y3)
        else :
            y1 = c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x
            X1.append(_x)
            Y1.append(y1)
else :
    for _x in X :
        if _x < 0.601 :
            y1 = c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x + c20
            y2 = c64 * _x ** 4 + c63 * _x ** 3 + c62 * _x ** 2 + c61 * _x + c60
            y3 = c114 * _x ** 4 + c113 * _x ** 3 + c112 * _x ** 2 + c111 * _x + c110
            X1.append(_x)
            X2.append(_x)
            X3.append(_x)
            Y1.append(y1)
            Y2.append(y2)
            Y3.append(y3)
        else :
            y3 = c114 * _x ** 4 + c113 * _x ** 3 + c112 * _x ** 2 + c111 * _x + c110
            X3.append(_x)
            Y3.append(y3)
if POS :
    eq = r'$p_{n}(v)=c_{n4}\cdot v^{4} + c_{n3}\cdot v^{3} + c_{n2}\cdot v^{2} + c_{n1}\cdot v$'
    ax.text(0.5, 0.01, eq, fontsize=11)
else :
    eq = r'$p_{n}(v)=c_{n4}\cdot v^{4} + c_{n3}\cdot v^{3} + c_{n2}\cdot v^{2} + c_{n1}\cdot v + c_{n0}$'
    ax.text(0.15, -32, eq, fontsize=11)
plt.rcParams["figure.autolayout"] = True
# df.set_index('Voltage').plot()
ax0 = df.plot(kind='scatter', x='v2', c='r', y='p2', ax=ax, xticks=x_tick_list, yticks=y_tick_list)
ax1 = df.plot(kind='scatter', x='v6', c='g', y='p6', ax=ax)
ax2 = df.plot(kind='scatter', x='v11', c='b', y='p11', ax=ax)

ax.plot(X1, Y1, c='r')
ax.plot(X2, Y2, c='g')
ax.plot(X3, Y3, c='b')

# get data frame values
# v_2 = list(df.loc[:,'v2'].values)
# p_2 = list(df.loc[:,'p2'].values)
# v_11 = list(df.loc[:,'v11'].values)
# p_11 = list(df.loc[:,'p11'].values)
# v_6 = list(df.loc[:,'v6'].values)
# p_6 = list(df.loc[:,'p6'].values)

# ax.xaxis.set_major_locator(plt.MaxNLocator(5))
ax.set_xlabel('Voltage (V)', fontsize=12)
ax.set_ylabel('Pressure (kPa)', fontsize=12)

# minor tick interval setting
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.2/2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(2.5/1))

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

# change font size of the ticks
plt.setp(ax.get_yticklabels(), fontsize=10)
plt.setp(ax.get_xticklabels(), fontsize=10)

ax.legend(['valve 2', 'valve 6', 'valve 11'], fontsize=10, edgecolor='black')

plt.show()
""""""
# if not ALL:
#     if not POS:
#         """ Negative Gauge Pressure """
#         x_tick_list = [3.4, 3.5, 3.6]
#         y_tick_list = [-0.04, -0.02, 0]
#         """ Positive Gauge Pressure """
#     else:
#         x_tick_list = [3.4, 3.9, 4.4, 4.9]
#         y_tick_list = [0.00, 0.02, 0.04, 0.06]
# else:
#     x_tick_list = [3.4, 3.9, 4.4, 4.9]
#     y_tick_list = [-0.04, -0.02, 0.00, 0.02, 0.04, 0.06]
#
# # ax.set_xticks(x_tick_list, minor=True)
# # ax.set_yticks(y_tick_list, minor=True)
# ax.set_xticks(x_tick_list)
# ax.set_yticks(y_tick_list)
# # ax.minorticks_on()
#
# ax.tick_params(which='both', width=1)
# ax.tick_params(which='major', length=6)
# ax.tick_params(which='minor', length=3, color='black')
#
# cnt = 0
# voltage = 0
# pressure = 0
# v = list()
# p = list()
# X = list()
# Y = list()
# mean_list = []
# for val in df.values:
#     voltage = val[0]
#     pressure += val[1]
#     cnt += 1
#     X.append(voltage)
#     Y.append(val[1])
#     # print(cnt)
#     if cnt == 20:
#         pressure = pressure / cnt
#
#         X = np.array(X)
#         Y = np.array(Y)
#         e = np.std(Y)
#         err = plt.errorbar(x=voltage, y=pressure, yerr=e, linestyle='None', ecolor='black', mfc='black', mec='black',
#                            capsize=4, capthick=1)
#         # err = plt.errorbar(x=voltage, y=pressure, yerr=e, fmt="none")
#         X = list()
#         Y = list()
#         v.append(voltage)
#         p.append(pressure)
#         # mean_list.append([voltage, pressure])
#         pressure = 0
#         cnt = 0
#
# """ legend frame color handle """
#
# """
# legend = ax.legend(frameon=1)
# frame  = legend.get_frame()
# frame.set_edgecolor('black')
# """
# v = np.array(v)
# p = np.array(p)
# ax.scatter(v, p, c='red')
# if TYPE == 2:
#     ax.legend(['measured', 'mean', 'std'], edgecolor='black')
# else:
#     ax.legend(['measured', 'mean'], edgecolor='black')
# # ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
#
# plt.show()
