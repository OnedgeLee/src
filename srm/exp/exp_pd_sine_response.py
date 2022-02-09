import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/exp_p_res_pd_sine2.csv')
# df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/exp_p_res_pd_sine1.csv')
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()
# ax = df.plot.line(x='time', y='p', c='black')
# ax1 = df.plot.line(x='time', y='g', c='red', ls='--', ax=ax)
# ax2 = df.plot.line(x='time', y='b_ang', c='blue', ax=ax, secondary_y = True)
# ax3 = ax.plot([0, 100], [0, 0], c='red', ls='--')
df.plot.line(x='time', y='p', c='black', ax=ax)
df.plot.line(x='time', y='g', c='red', ls='--', ax=ax)
df.plot.line(x='time', y='b_ang', c='blue', ax=ax, secondary_y = True)

ax.plot([0, 100], [0, 0], c='red', ls='--')
ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='gray')
ax.get_legend().remove()
ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

# plt.axvline(0, 0, 1, c='darkgray')
plt.axvline(100, 0.6, 0.95, c='red', linestyle='--')
# plt.axvline(5095, 0.86, 0.95, c='black', linestyle='--')
# plt.axvline(5234, 0.8, 0.95, c='black', ls='--')
# plt.text(5400, 0, 'Difference 130 ms')
# plt.axvline(100, 0.18, 0.67, c='green', linestyle='--')

x_tick_list = [0, 6000,  12000, 18000]
y_tick_list = [-50, -25, 0]
y_tick_r_list = [-50, -25, 0]
ax.set_xticks(x_tick_list)
ax.set_yticks(y_tick_list)
ax.right_ax.set_yticks(y_tick_r_list)
ax.xaxis.set_minor_locator(plt.MultipleLocator(3000/3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(25/3))
ax.right_ax.yaxis.set_minor_locator(plt.MultipleLocator(25/3))

ax.right_ax.tick_params(which='both', width=1)
ax.right_ax.tick_params(which='major', length=7)
ax.right_ax.tick_params(which='minor', length=3, color='gray')

ax.set_xlabel('Time (ms)', fontsize=12)
ax.set_ylabel('Pressure (kPa)', fontsize=12)
ax.right_ax.set_ylabel('Bending angle ($^\circ$)', fontsize=12)

ax.set_ylim([-53, 3])
ax.right_ax.set_ylim([-53, 3])

ax.legend([ax.get_lines()[0], ax.get_lines()[1], ax.right_ax.get_lines()[0]], ['Current pressure',
                                                                        'Goal pressure',
                                                                        'Bending angle'], edgecolor='black', fontsize=12, loc='upper right')

plt.show()