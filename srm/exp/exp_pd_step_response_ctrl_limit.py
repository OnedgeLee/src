import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/exp_pd_control3.csv')
plt.rcParams["figure.autolayout"] = True

ax = df.plot.line(x='t_lm10', y='p_lm10', c='black')
ax1 = df.plot.line(x='t_lm10', y='g_lm10', c='black', ls='--', ax=ax)

ax2 = df.plot.line(x='t_lm20', y='p_lm20', c='blue', ax=ax)
# ax3 = df.plot.line(x='t_lm20', y='g_lm20', c='blue', ls='--', ax=ax)

ax4 = df.plot.line(x='t_lm30', y='p_lm30', c='red', ax=ax)
# ax5 = df.plot.line(x='t_lm30', y='g_lm30', c='red', ls='--', ax=ax)

ax14 = ax.plot([0, 100], [0, 0], c='black', ls='--')
ax15 = ax.plot([0, 100], [-0.7, -0.7], c='red')

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')
ax.get_legend().remove()
ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

# plt.axvline(0, 0, 1, c='darkgray')
plt.axvline(100, 0.41, 0.94, c='black', linestyle='--')
# plt.axvline(100, 0.18, 0.67, c='green', linestyle='--')

x_tick_list = [0, 100, 500, 1000, 1500, 2000]
y_tick_list = [-50, -40, -30, -20, -10, 0, 10, 20]
ax.set_xticks(x_tick_list)
ax.set_yticks(y_tick_list)

ax.set_ylim([-53, 3])

ax.xaxis.set_minor_locator(plt.MultipleLocator(500/2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(10/2))

ax.set_xlabel('Time (ms)')
ax.set_ylabel('Pressure (kPa)')

ax.legend(['Pressure (Limit 10 mV)', 'Goal pressure', 'Pressure (Limit 20 mV)', 'Pressure (Limit 30 mV)'], edgecolor='black', fontsize=12, loc='best')

plt.show()