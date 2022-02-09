import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/exp_pd_control2.csv')
plt.rcParams["figure.autolayout"] = True

ax = df.plot.line(x='t_m10', y='p_m10', c='black')
ax1 = df.plot.line(x='t_m10', y='g_m10', c='black', ls='--', ax=ax)

ax2 = df.plot.line(x='t_m20', y='p_m20', c='blue', ax=ax)
ax3 = df.plot.line(x='t_m20', y='g_m20', c='blue', ls='--', ax=ax)

ax4 = df.plot.line(x='t_m30', y='p_m30', c='red', ax=ax)
ax5 = df.plot.line(x='t_m30', y='g_m30', c='red', ls='--', ax=ax)

ax6 = df.plot.line(x='t_m40', y='p_m40', c='green', ax=ax)
ax7 = df.plot.line(x='t_m40', y='g_m40', c='green', ls='--', ax=ax)

ax8 = df.plot.line(x='t_p10', y='p_p10', c='darkgray', ax=ax)
ax9 = df.plot.line(x='t_p10', y='g_p10', c='darkgray', ls='--', ax=ax)

ax10 = df.plot.line(x='t_p20', y='p_p20', c='brown', ax=ax)
ax11 = df.plot.line(x='t_p20', y='g_p20', c='brown', ls='--', ax=ax)

ax12 = df.plot.line(x='t_m0', y='p_m0', c='orange', ax=ax)
ax13 = df.plot.line(x='t_m0', y='g_m0', c='orange', ls='--', ax=ax)


ax14 = ax.plot([0, 100], [0, 0], c='black', ls='--')

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')
ax.get_legend().remove()
ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

# plt.axvline(0, 0, 1, c='darkgray')
plt.axvline(100, 0.67, 0.92, c='brown', linestyle='--')
plt.axvline(100, 0.18, 0.67, c='green', linestyle='--')

x_tick_list = [0, 100, 500, 1000, 1500, 2000]
y_tick_list = [-50, -40, -30, -20, -10, 0, 10, 20]
ax.set_xticks(x_tick_list)
ax.set_yticks(y_tick_list)

ax.xaxis.set_minor_locator(plt.MultipleLocator(500/2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(10/2))

ax.set_xlabel('Time (ms)')
ax.set_ylabel('Pressure (kPa)')


plt.show()