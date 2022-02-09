import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter

# df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/exp_p_res_pd_sine2.csv')
df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/exp_p_res_sine_f_vari.csv')
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()
ax  = fig.add_subplot(221)
ax1 = fig.add_subplot(222)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)
# ax = df.plot.line(x='time', y='p', c='black')
# ax1 = df.plot.line(x='time', y='g', c='red', ls='--', ax=ax)
# ax2 = df.plot.line(x='time', y='b_ang', c='blue', ax=ax, secondary_y = True)
# ax3 = ax.plot([0, 100], [0, 0], c='red', ls='--')
df.plot.line(x='t_f_10', y='p_f_10', c='k', ax=ax)
df.plot.line(x='t_f_10', y='g_f_10', c='b', ls='--', ax=ax)
# df.plot.line(x='t_f_10', y='a_f_10', c='k', ax=ax, secondary_y = True)

df.plot.line(x='t_f_12', y='p_f_12', c='k', ax=ax1)
df.plot.line(x='t_f_12', y='g_f_12', c='b', ls='--', ax=ax1)
# df.plot.line(x='t_f_12', y='a_f_12', c='k',  ax=ax1, secondary_y = True)

df.plot.line(x='t_f_15', y='p_f_15', c='k', ax=ax2)
df.plot.line(x='t_f_15', y='g_f_15', c='b', ls='--', ax=ax2)
# df.plot.line(x='t_f_15', y='a_f_15', c='k', ax=ax2, secondary_y = True)

df.plot.line(x='t_f_20', y='p_f_20', c='k', ax=ax3)
df.plot.line(x='t_f_20', y='g_f_20', c='b', ls='--', ax=ax3)
# df.plot.line(x='t_f_20', y='a_f_20', c='k', ax=ax3, secondary_y = True)


ax.plot([0, 100], [0, 0], c='b', ls='--')
ax1.plot([0, 100], [0, 0], c='b', ls='--')
ax2.plot([0, 100], [0, 0], c='b', ls='--')
ax3.plot([0, 100], [0, 0], c='b', ls='--')

ax.plot([100, 100], [-20, 0], c='b', ls='--')
ax1.plot([100, 100], [-20, 0], c='b', ls='--')
ax2.plot([100, 100], [-20, 0], c='b', ls='--')
ax3.plot([100, 100], [-20, 0], c='b', ls='--')

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='gray')
ax.get_legend().remove()
ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

ax1.tick_params(which='both', width=1)
ax1.tick_params(which='major', length=7)
ax1.tick_params(which='minor', length=3, color='gray')
ax1.get_legend().remove()
ax1.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

ax2.tick_params(which='both', width=1)
ax2.tick_params(which='major', length=7)
ax2.tick_params(which='minor', length=3, color='gray')
ax2.get_legend().remove()
ax2.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

ax3.tick_params(which='both', width=1)
ax3.tick_params(which='major', length=7)
ax3.tick_params(which='minor', length=3, color='gray')
ax3.get_legend().remove()
ax3.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))


# plt.axvline(0, 0, 1, c='darkgray')

# plt.axvline(5095, 0.86, 0.95, c='black', linestyle='--')
# plt.axvline(5234, 0.8, 0.95, c='black', ls='--')
# plt.text(5400, 0, 'Difference 130 ms')
# plt.axvline(100, 0.18, 0.67, c='green', linestyle='--')

x_tick_list = [0, 6000,  12000, 18000]
y_tick_list = [-50, -25, 0]
y_tick_r_list = [-50, -25, 0]
ax.set_xticks(x_tick_list)
ax.set_yticks(y_tick_list)
# ax.right_ax.set_yticks(y_tick_r_list)
ax.xaxis.set_minor_locator(plt.MultipleLocator(3000/3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(25/3))
# ax.right_ax.yaxis.set_minor_locator(plt.MultipleLocator(25/3))

# ax.right_ax.tick_params(which='both', width=1)
# ax.right_ax.tick_params(which='major', length=7)
# ax.right_ax.tick_params(which='minor', length=3, color='gray')

ax.set_xlabel('Time (ms)', fontsize=12)
ax.set_ylabel('Pressure (kPa)', fontsize=12)
# ax.right_ax.set_ylabel('Bending angle ($^\circ$)', fontsize=12)

ax.set_ylim([-53, 3])
# ax.right_ax.set_ylim([-53, 3])

ax1.set_xticks(x_tick_list)
ax1.set_yticks(y_tick_list)
# ax1.right_ax.set_yticks(y_tick_r_list)
ax1.xaxis.set_minor_locator(plt.MultipleLocator(3000/3))
ax1.yaxis.set_minor_locator(plt.MultipleLocator(25/3))
# ax1.right_ax.yaxis.set_minor_locator(plt.MultipleLocator(25/3))

# ax1.right_ax.tick_params(which='both', width=1)
# ax1.right_ax.tick_params(which='major', length=7)
# ax1.right_ax.tick_params(which='minor', length=3, color='gray')

ax1.set_xlabel('Time (ms)', fontsize=12)
# ax1.set_ylabel('Pressure (kPa)', fontsize=12)
# ax1.right_ax.set_ylabel('Bending angle ($^\circ$)', fontsize=12)

ax1.set_ylim([-53, 3])
# ax1.right_ax.set_ylim([-53, 3])

ax2.set_xticks(x_tick_list)
ax2.set_yticks(y_tick_list)
# ax2.right_ax.set_yticks(y_tick_r_list)
ax2.xaxis.set_minor_locator(plt.MultipleLocator(3000/3))
ax2.yaxis.set_minor_locator(plt.MultipleLocator(25/3))
# ax2.right_ax.yaxis.set_minor_locator(plt.MultipleLocator(25/3))

# ax2.right_ax.tick_params(which='both', width=1)
# ax2.right_ax.tick_params(which='major', length=7)
# ax2.right_ax.tick_params(which='minor', length=3, color='gray')

ax2.set_xlabel('Time (ms)', fontsize=12)
ax2.set_ylabel('Pressure (kPa)', fontsize=12)
# ax2.right_ax.set_ylabel('Bending angle ($^\circ$)', fontsize=12)

ax3.set_ylim([-53, 3])
# ax3.right_ax.set_ylim([-53, 3])
ax3.set_xticks(x_tick_list)
ax3.set_yticks(y_tick_list)
# ax3.right_ax.set_yticks(y_tick_r_list)
ax3.xaxis.set_minor_locator(plt.MultipleLocator(3000/3))
ax3.yaxis.set_minor_locator(plt.MultipleLocator(25/3))
# ax3.right_ax.yaxis.set_minor_locator(plt.MultipleLocator(25/3))

# ax3.right_ax.tick_params(which='both', width=1)
# ax3.right_ax.tick_params(which='major', length=7)
# ax3.right_ax.tick_params(which='minor', length=3, color='gray')

ax3.set_xlabel('Time (ms)', fontsize=12)
# ax3.set_ylabel('Pressure (kPa)', fontsize=12)
# ax3.right_ax.set_ylabel('Bending angle ($^\circ$)', fontsize=12)

ax3.set_ylim([-53, 3])
# ax3.right_ax.set_ylim([-53, 3])
# ax.legend([ax.get_lines()[0], ax.get_lines()[1], ax.right_ax.get_lines()[0]], ['Current pressure',
#                                                                        'Goal pressure',
#                                                                         'Bending angle'], edgecolor='black', fontsize=12, loc='best'
#           ,bbox_to_anchor=(0.65, 1.25))
ax.legend(['Current pressure', 'Goal pressure'], fontsize=12, loc='lower right')

plt.show()