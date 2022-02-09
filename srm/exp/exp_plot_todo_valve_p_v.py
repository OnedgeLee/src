import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

POS = False
if POS:
    df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/p_v/pcb_p_v_res.csv')
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
    c104 = -4.1484
    c103 = 7.0742
    c102 = 2.8924
    c101 = 6.9909
    shift_10 = 3.3 # start at 3.3 V
else:
    df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/p_v/pcb_p_v_res.csv')
    # ch6, ch5 -> 6 -
    c65 = -0.0652
    c64 = 0.9013
    c63 = -3.9804
    c62 = 5.219
    c61 = -2.4879
    c60 = 0

    # ch3, ch4 -> 2 -
    c25 = -0.0678
    c24 = 0.9
    c23 = -3.7846
    c22 = 4.5082
    c21 = -2.204
    c20 = 0

    # ch2, ch1 -> 10 -
    c105 = -0.081
    c104 = 1.0365
    c103 = -4.2025
    c102 = 4.8663
    c101 = -2.2107
    c100 = 0

# df_new = df.rename(columns={'Voltage': 'Voltage (V)', 'Pressure': 'Pressure (MPa)'})
print(df)

fig = plt.figure()
ax  = fig.add_subplot(111)

if POS :
    X = np.linspace(0.0, 1.8, 181)
    x_tick_list = [0.2, 0.7, 1.2, 1.7]
    y_tick_list = [2.5, 7.5, 12.5, 17.5, 22.5]
else :
    X = np.linspace(0.0, 5.0, 501)
    x_tick_list = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
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
            y3 = c104 * _x ** 4 + c103 * _x ** 3 + c102 * _x ** 2 + c101 * _x
            X1.append(_x)
            X2.append(_x)
            X3.append(_x)
            Y1.append(y1)
            Y2.append(y2)
            Y3.append(y3)
        elif _x < 1.701 :
            y1 = c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x
            y3 = c104 * _x ** 4 + c103 * _x ** 3 + c102 * _x ** 2 + c101 * _x
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
        y1 = c25 * _x ** 5 + c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x + c20
        y2 = c65 * _x ** 5 + c64 * _x ** 4 + c63 * _x ** 3 + c62 * _x ** 2 + c61 * _x + c60
        y3 = c105 * _x ** 5 + c104 * _x ** 4 + c103 * _x ** 3 + c102 * _x ** 2 + c101 * _x + c100
        X1.append(_x)
        X2.append(_x)
        X3.append(_x)
        Y1.append(y1)
        Y2.append(y2)
        Y3.append(y3)
        """
        if _x < 0.651 :
            y1 = c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x + c20
            y2 = c64 * _x ** 4 + c63 * _x ** 3 + c62 * _x ** 2 + c61 * _x + c60
            y3 = c104 * _x ** 4 + c103 * _x ** 3 + c102 * _x ** 2 + c101 * _x + c100
            X1.append(_x)
            X2.append(_x)
            X3.append(_x)
            Y1.append(y1)
            Y2.append(y2)
            Y3.append(y3)
        # elif _x < 0.651 :
        #     y3 = c104 * _x ** 4 + c103 * _x ** 3 + c102 * _x ** 2 + c101 * _x + c100
        #     y1 = c24 * _x ** 4 + c23 * _x ** 3 + c22 * _x ** 2 + c21 * _x + c20
        #     X3.append(_x)
        #     Y3.append(y3)
        #     X1.append(_x)
        #     Y1.append(y1)
        else :
            y3 = c104 * _x ** 4 + c103 * _x ** 3 + c102 * _x ** 2 + c101 * _x + c100
            Y3.append(y3)
            X3.append(_x)
        """
if POS :
    eq = r'$p_{n}(v)=c_{n4}\cdot v^{4} + c_{n3}\cdot v^{3} + c_{n2}\cdot v^{2} + c_{n1}\cdot v$'
    ax.text(0.5, 0.01, eq, fontsize=11)
else :
    eq = r'$p_{n}(v)=c_{n5}\cdot v^{5} + c_{n4}\cdot v^{4} + c_{n3}\cdot v^{3} + c_{n2}\cdot v^{2} + c_{n1}\cdot v + ' \
         r'c_{n0}$ '
    ax.text(0.0, -20.5, eq, fontsize=10)
plt.rcParams["figure.autolayout"] = True
# df.set_index('Voltage').plot()
ax0 = df.plot(kind='scatter', x='v', c='r', y='p34', ax=ax, xticks=x_tick_list, yticks=y_tick_list)
ax1 = df.plot(kind='scatter', x='v', c='g', y='p65', ax=ax)
ax2 = df.plot(kind='scatter', x='v', c='b', y='p21', ax=ax)

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
ax.xaxis.set_minor_locator(plt.MultipleLocator(1/2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(2.5/1))

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

# change font size of the ticks
plt.setp(ax.get_yticklabels(), fontsize=10)
plt.setp(ax.get_xticklabels(), fontsize=10)

ax.legend(['Bellow 2', 'Bellow 6', 'Bellow 10'], fontsize=10, edgecolor='black')

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
