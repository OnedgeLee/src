import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/p_response_time/time_response.csv')

POS = True
if POS :
    x_tick_list = [0.0, 0.2, 0.4, 0.6]
    y_tick_list = [0, 5, 10, 15, 20]
else :
    x_tick_list = [0.0, 0.4, 0.8, 1.2, 1.6]
    y_tick_list = [-20, -15, -10, -5, 0]

fig = plt.figure()
ax  = fig.add_subplot(111)

plt.rcParams["figure.autolayout"] = True
# df.set_index('Voltage').plot()
if POS :
    ax4 = df.plot(kind='scatter', x='tp5', c='r', y='pp5', label='5 kPa', ax=ax, xticks=x_tick_list, yticks=y_tick_list)
    ax5 = df.plot(kind='scatter', x='tp10', c='g', y='pp10', label='10 kPa', ax=ax)
    ax6 = df.plot(kind='scatter', x='tp15', c='b', y='pp15', label='15 kPa', ax=ax)
    ax7 = df.plot(kind='scatter', x='tp20', c='black', y='pp20', label='20 kPa', ax=ax)
else :
    ax0 = df.plot(kind='scatter', x='tn5', c='r', y='pn5', label='-5 kPa', ax=ax, xticks=x_tick_list, yticks=y_tick_list)
    ax1 = df.plot(kind='scatter', x='tn10', c='g', y='pn10', label='-10 kPa', ax=ax)
    ax2 = df.plot(kind='scatter', x='tn15', c='b', y='pn15', label='-15 kPa', ax=ax)
    ax3 = df.plot(kind='scatter', x='tn20', c='black', y='pn20', label='-20 kPa', ax=ax)

# ax0 = df.plot.line(x='tn5', c='black', y='pn5', ax=ax, xticks=x_tick_list, yticks=y_tick_list)
# ax1 = df.plot.line(x='tn10', c='black', y='pn10', ax=ax)
# ax2 = df.plot.line(x='tn15', c='black', y='pn15', ax=ax)
# ax3 = df.plot.line(x='tn20', c='black', y='pn20', ax=ax)
# ax4 = df.plot.line(x='tp5', c='black', y='pp5', ax=ax)
# ax5 = df.plot.line(x='tp10', c='black', y='pp10', ax=ax)
# ax6 = df.plot.line(x='tp15', c='black', y='pp15', ax=ax)
# ax7 = df.plot.line(x='tp20', c='black', y='pp20', ax=ax)


# ax.xaxis.set_major_locator(plt.MaxNLocator(5))
ax.set_xlabel('Time (s)', fontsize=12)
ax.set_ylabel('Pressure (kPa)', fontsize=12)

# minor tick interval setting
if POS :
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.2/2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(5/2))
else :
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.4 / 2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(2.5 / 1))

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

# change font size of the ticks
plt.setp(ax.get_yticklabels(), fontsize=10)
plt.setp(ax.get_xticklabels(), fontsize=10)


# plt.axhline(0, 0, 1, c='darkgray')
# plt.axhline(0, 0, 1, c='darkgray')
# plt.axhline(y=5, color='darkgray', linewidth=1)
# plt.axhline(y=10, color='darkgray', linewidth=1)
# plt.axhline(y=15, color='darkgray', linewidth=1)

# ax.legend(['Bellow 2', 'Bellow 6', 'Bellow 10'], fontsize=10, edgecolor='black')

ax.legend(edgecolor='black', fontsize=11)

plt.show()

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
